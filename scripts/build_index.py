#!/usr/bin/env python3
"""
概念库索引生成器 — build_index.py

三种模式：
  python3 scripts/build_index.py               全量扫描，重建索引
  python3 scripts/build_index.py --incremental  只处理变动文件，重算派生数据
  python3 scripts/build_index.py --check        校验 frontmatter 词汇表合规

输出：memory/concept_index.json
依赖：纯 Python 标准库，无需 pip install
"""

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Optional

# ── 路径常量 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_ROOT = os.path.dirname(SCRIPT_DIR)  # 概念库/
CONCEPT_DIR = os.path.join(LIB_ROOT, "概念页")
MEMORY_DIR = os.path.join(LIB_ROOT, "memory")
INDEX_PATH = os.path.join(MEMORY_DIR, "concept_index.json")
ALIASES_PATH = os.path.join(MEMORY_DIR, "name_aliases.json")
RELATIONS_PATH = os.path.join(MEMORY_DIR, "concept_relations.md")

# ── 词汇表白名单 ──────────────────────────────────────────
VOCABULARY = {
    "domain": [
        "哲学", "心理学", "经济学", "社会学", "传播学",
        "管理学", "生物学", "物理学", "人类学", "政治学", "艺术",
    ],
    "discipline": [
        # 哲学
        "伦理学", "行动哲学", "认识论", "心灵哲学", "形而上学",
        "语言哲学", "科学哲学", "政治哲学", "逻辑学", "美学",
        "中式哲学", "批判理论", "技术哲学", "存在主义",
        # 心理学
        "社会心理学", "认知心理学", "动机心理学", "发展心理学", "临床心理学",
        # 经济学
        "行为经济学", "制度经济学", "信息经济学", "金融学",
        # 社会学
        "社会学", "文化社会学", "组织社会学",
        # 传播学
        "传播学",
        # 管理学
        "组织行为学", "知识管理", "系统思维",
        # 生物学
        "行为生物学", "控制论",
        # 物理学
        "量子物理", "热力学", "复杂系统",
        # 认知科学（跨域）
        "认知科学",
        # 政治学
        "国际关系",
        # 艺术
        "视觉理论", "叙事学", "文学理论", "音乐理论",
    ],
    "pattern": [
        "悖论", "盲区", "冲突", "渐变", "反转", "循环", "错位", "缺位",
    ],
    "apply": [
        "自我", "关系", "制度", "创作", "自媒体",
        "商业", "组织", "决策", "领导", "教育",
    ],
    "source": [
        "寓言故事", "概念跳跃", "对话整理", "阅读沉淀", "圆桌讨论",
    ],
}

# ── Frontmatter 解析 ─────────────────────────────────────

def parse_frontmatter(content: str) -> Optional[dict]:
    """提取 YAML frontmatter，返回字段字典。不依赖 PyYAML。"""
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return None

    raw = m.group(1)
    result = {}

    for line in raw.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # key: value
        colon_idx = line.find(':')
        if colon_idx < 0:
            continue

        key = line[:colon_idx].strip()
        val = line[colon_idx + 1:].strip()

        # 解析值
        if val.startswith('[') and val.endswith(']'):
            # 行内数组 [X, Y, Z]
            items = re.findall(r'[^\[\],\s]+', val)
            result[key] = items
        elif val.startswith('"') or val.startswith("'"):
            result[key] = val.strip('"').strip("'")
        else:
            result[key] = val

    return result


def extract_wikilinks(content: str) -> List[str]:
    """提取所有 [[目标名]] 链接，处理 [[名|显示文本]] 和 [[名#章节]]。"""
    # 匹配 [[...]]，内部可含 |显示文本 或 #章节
    raw = re.findall(r'\[\[([^\]]+)\]\]', content)
    targets = []
    for r in raw:
        # 取 | 和 # 之前的部分
        target = re.split(r'[|#]', r)[0].strip()
        if target:
            targets.append(target)

    # 去重但保序
    seen = set()
    unique = []
    for t in targets:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def parse_tags(tags_value) -> dict:
    """拆分 tags 为 discipline/pattern/apply 三组。"""
    if isinstance(tags_value, str):
        tags_value = [tags_value]

    disciplines = []
    pattern = None
    applies = []

    for tag in tags_value:
        if tag.startswith("discipline/"):
            disciplines.append(tag[len("discipline/"):])
        elif tag.startswith("pattern/"):
            pattern = tag[len("pattern/"):]
        elif tag.startswith("apply/"):
            applies.append(tag[len("apply/"):])

    return {"discipline": disciplines, "pattern": pattern, "apply": applies}


def extract_english_name(name_field: str) -> Optional[str]:
    """从 '弱意志（Akrasia）' 提取英文名。全角括号分隔。"""
    m = re.search(r'（([^）]+)）', name_field)
    if m:
        return m.group(1).strip()
    # 也尝试半角括号
    m = re.search(r'\(([^)]+)\)', name_field)
    if m:
        return m.group(1).strip()
    return None


# ── 单文件扫描 ────────────────────────────────────────────

def scan_file(filepath: str) -> Optional[dict]:
    """扫描一个概念页，返回 node dict。"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return None

    fm = parse_frontmatter(content)
    if not fm:
        return None

    filename = os.path.basename(filepath)
    # 从文件名去掉 .md 得到概念中文名
    name_cn = filename[:-3] if filename.endswith('.md') else filename

    # 跳过 INDEX.md
    if name_cn == 'INDEX':
        return None

    # name 字段
    name_field = fm.get('name', name_cn)
    name_en = extract_english_name(name_field) if name_field else None

    # domain
    domain = fm.get('domain', [])
    if isinstance(domain, str):
        domain = [domain]

    # tags
    tags = parse_tags(fm.get('tags', []))

    # source
    source = fm.get('source', '')

    # date
    date = fm.get('date', '')

    # 出链
    out_links = extract_wikilinks(content)

    return {
        "file": filename,
        "name": name_field,
        "name_en": name_en,
        "domain": domain,
        "discipline": tags["discipline"],
        "pattern": tags["pattern"],
        "apply": tags["apply"],
        "source": source,
        "date": date,
        "out_links": out_links,
        "in_links": [],
        "out_degree": len(out_links),
        "in_degree": 0,
    }


# ── 派生数据计算 ──────────────────────────────────────────

def compute_in_links(nodes: dict) -> None:
    """根据 out_links 反算 in_links 和 in_degree。"""
    # 清零
    for node in nodes.values():
        node["in_links"] = []
        node["in_degree"] = 0

    for name, node in nodes.items():
        for target in node["out_links"]:
            if target in nodes:
                nodes[target]["in_links"].append(name)
                nodes[target]["in_degree"] += 1


def compute_edges(nodes: dict) -> List[dict]:
    """生成边列表。"""
    edges = []
    for name, node in nodes.items():
        for target in node["out_links"]:
            edges.append({"source": name, "target": target})
    return edges


def compute_orphans(nodes: dict) -> dict:
    """计算孤立概念。"""
    fully = []
    semi = []
    for name, node in nodes.items():
        if node["out_degree"] == 0:
            if node["in_degree"] == 0:
                fully.append(name)
            else:
                semi.append({"name": name, "in_degree": node["in_degree"]})

    fully.sort()
    semi.sort(key=lambda x: x["in_degree"], reverse=True)
    return {"fully_isolated": fully, "semi_isolated": semi}


def compute_broken_links(nodes: dict) -> List[dict]:
    """计算断链（出链目标不在 nodes 中且不在 name_aliases 中）。"""
    broken = []
    for name, node in nodes.items():
        for target in node["out_links"]:
            if target not in nodes:
                broken.append({"source": name, "target": target})
    return broken


def compute_inverted_index(nodes: dict, field: str) -> Dict[str, List[str]]:
    """按某个字段构建倒排索引。field 可以是 'apply', 'domain', 'discipline', 'pattern'。"""
    index = defaultdict(list)
    for name, node in nodes.items():
        values = node.get(field)
        if values is None:
            continue
        if isinstance(values, str):
            values = [values]
        for v in values:
            if v:
                index[v].append(name)

    # 排序
    for k in index:
        index[k].sort()
    return dict(sorted(index.items()))


# ── 连通分量（Union-Find）─────────────────────────────────

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1


def compute_connected_components(nodes: dict) -> List[List[str]]:
    """计算图的连通分量，只返回 size >= 2 的。"""
    names = sorted(nodes.keys())
    name_to_idx = {n: i for i, n in enumerate(names)}
    uf = UnionFind(len(names))

    for name, node in nodes.items():
        src_idx = name_to_idx[name]
        for target in node["out_links"]:
            if target in name_to_idx:
                tgt_idx = name_to_idx[target]
                uf.union(src_idx, tgt_idx)

    # 分组
    groups = defaultdict(list)
    for i, n in enumerate(names):
        root = uf.find(i)
        groups[root].append(n)

    # 过滤 size >= 2，按 size 降序
    result = [sorted(g) for g in groups.values() if len(g) >= 2]
    result.sort(key=lambda g: len(g), reverse=True)
    return result


# ── 重复检测 ──────────────────────────────────────────────

def _lcs_ratio(s1: str, s2: str) -> float:
    """最长公共子序列比率（0-1）。"""
    if not s1 or not s2:
        return 0.0
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs_len = dp[m][n]
    return 2 * lcs_len / (m + n)


def detect_duplicates(nodes: dict) -> List[dict]:
    """检测潜在重复概念。同 domain+discipline 下名称相似度 > 0.7 的配对。"""
    # 按 domain+discipline 分组
    groups = defaultdict(list)
    for name, node in nodes.items():
        key = (tuple(sorted(node.get("domain", []))),
               tuple(sorted(node.get("discipline", []))))
        groups[key].append(name)

    duplicates = []
    for key, names in groups.items():
        if len(names) < 2:
            continue
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                ratio = _lcs_ratio(names[i], names[j])
                if ratio > 0.7:
                    duplicates.append({
                        "concepts": [names[i], names[j]],
                        "reason": f"同 domain+discipline, 名称相似度 {ratio:.2f}",
                    })

    # 英文名重复检测
    en_names = {}
    for name, node in nodes.items():
        en = node.get("name_en")
        if en:
            en_lower = en.lower()
            if en_lower in en_names:
                duplicates.append({
                    "concepts": [en_names[en_lower], name],
                    "reason": f"英文名重复: {en}",
                })
            else:
                en_names[en_lower] = name

    return duplicates


# ── 从 concept_relations.md 加载集群 ──────────────────────

def load_clusters_from_relations(relations_path: str) -> List[dict]:
    """解析 concept_relations.md 中的集群定义。"""
    if not os.path.exists(relations_path):
        return []

    try:
        with open(relations_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except IOError:
        return []

    clusters = []

    # 逐行扫描
    lines = content.split('\n')
    current_cluster = None
    current_members_raw = []
    members_parsed = False  # 标记成员是否已解析

    def _parse_members(raw_lines):
        """从收集的行中解析成员概念名。"""
        text = '\n'.join(raw_lines)
        members = re.findall(r'`([^`]+)`', text)
        if not members:
            members = [w.strip() for w in text.split() if w.strip()]
        return members

    def _finalize_cluster(cluster, raw_lines):
        """解析成员并保存集群。"""
        if cluster and not cluster.get("_finalized"):
            if raw_lines and not cluster["members"]:
                cluster["members"] = _parse_members(raw_lines)
            cluster["_finalized"] = True
            # 去掉内部标记
            cluster.pop("_finalized", None)
            clusters.append(cluster)

    for line in lines:
        # 匹配集群标题行: ### A · 集体意见动力学 ✅
        header_match = re.match(
            r'###\s+([A-Z])\s*[·•]\s*(.+?)(?:\s*✅)?\s*$', line
        )
        if header_match:
            # 保存上一个集群
            _finalize_cluster(current_cluster, current_members_raw)

            cluster_id = header_match.group(1)
            cluster_name = header_match.group(2).strip()
            current_cluster = {
                "id": cluster_id,
                "name": cluster_name,
                "members": [],
                "description": "",
            }
            current_members_raw = []
            members_parsed = False
            continue

        # 如果在集群内
        if current_cluster is not None:
            stripped = line.strip()

            if not stripped:
                # 空行：如果成员还没解析，现在解析
                if current_members_raw and not members_parsed:
                    current_cluster["members"] = _parse_members(current_members_raw)
                    members_parsed = True
                continue

            if stripped.startswith('>'):
                # 引用块是描述。先解析成员（如果还没解析）
                if current_members_raw and not members_parsed:
                    current_cluster["members"] = _parse_members(current_members_raw)
                    members_parsed = True
                desc = stripped.lstrip('> ').strip()
                if current_cluster["description"]:
                    current_cluster["description"] += " " + desc
                else:
                    current_cluster["description"] = desc
                continue

            if stripped.startswith('#') or stripped.startswith('---'):
                # 新章节或分隔线，结束当前集群
                _finalize_cluster(current_cluster, current_members_raw)
                current_cluster = None
                current_members_raw = []
                members_parsed = False
                continue

            # 成员行（含反引号概念名或纯文本）
            if not members_parsed:
                current_members_raw.append(stripped)

    # 文件结尾，保存最后一个集群
    _finalize_cluster(current_cluster, current_members_raw)

    return clusters


# ── 从 name_aliases.json 加载别名 ────────────────────────

def load_name_aliases(aliases_path: str) -> dict:
    """加载同义名映射。"""
    if not os.path.exists(aliases_path):
        return {}
    try:
        with open(aliases_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return {}


# ── 词汇表校验 ────────────────────────────────────────────

def validate_frontmatter(nodes: dict, vocab: dict) -> List[dict]:
    """校验每个节点的 frontmatter 是否符合词汇表白名单。"""
    violations = []

    for name, node in nodes.items():
        # domain
        for d in node.get("domain", []):
            if d not in vocab["domain"]:
                violations.append({
                    "concept": name, "field": "domain", "value": d,
                    "allowed": vocab["domain"],
                })

        # discipline
        for d in node.get("discipline", []):
            if d not in vocab["discipline"]:
                violations.append({
                    "concept": name, "field": "discipline", "value": d,
                    "allowed": f"参见 vocabulary.discipline（{len(vocab['discipline'])}个）",
                })

        # pattern
        p = node.get("pattern")
        if p and p not in vocab["pattern"]:
            violations.append({
                "concept": name, "field": "pattern", "value": p,
                "allowed": vocab["pattern"],
            })

        # apply
        for a in node.get("apply", []):
            if a not in vocab["apply"]:
                violations.append({
                    "concept": name, "field": "apply", "value": a,
                    "allowed": vocab["apply"],
                })

        # source
        s = node.get("source", "")
        if s and s not in vocab["source"]:
            violations.append({
                "concept": name, "field": "source", "value": s,
                "allowed": vocab["source"],
            })

        # name 格式
        name_field = node.get("name", "")
        if name_field and not re.search(r'（[^）]+）', name_field):
            # 宽松：不强制报错，只 warn
            pass

        # 缺 discipline
        if not node.get("discipline"):
            violations.append({
                "concept": name, "field": "discipline", "value": "(缺失)",
                "allowed": "至少一个 discipline 标签",
            })

        # 缺 pattern
        if not node.get("pattern"):
            violations.append({
                "concept": name, "field": "pattern", "value": "(缺失)",
                "allowed": vocab["pattern"],
            })

        # 缺 apply
        if not node.get("apply"):
            violations.append({
                "concept": name, "field": "apply", "value": "(缺失)",
                "allowed": vocab["apply"],
            })

        # 缺 domain
        if not node.get("domain"):
            violations.append({
                "concept": name, "field": "domain", "value": "(缺失)",
                "allowed": vocab["domain"],
            })

    return violations


# ── 全量构建 ──────────────────────────────────────────────

def build_full_index() -> dict:
    """全量扫描概念页，构建完整索引。"""
    start_time = time.time()

    # 扫描所有 .md 文件
    nodes = {}
    scanned = 0
    for fname in os.listdir(CONCEPT_DIR):
        if not fname.endswith('.md') or fname == 'INDEX.md':
            continue
        filepath = os.path.join(CONCEPT_DIR, fname)
        if not os.path.isfile(filepath):
            continue

        node = scan_file(filepath)
        if node:
            # 从文件名提取中文名作为 key
            name_cn = fname[:-3]
            nodes[name_cn] = node
            scanned += 1

    # 计算派生数据
    compute_in_links(nodes)
    edges = compute_edges(nodes)
    orphans = compute_orphans(nodes)
    broken = compute_broken_links(nodes)
    components = compute_connected_components(nodes)
    duplicates = detect_duplicates(nodes)

    # 倒排索引
    apply_idx = compute_inverted_index(nodes, "apply")
    domain_idx = compute_inverted_index(nodes, "domain")
    discipline_idx = compute_inverted_index(nodes, "discipline")
    pattern_idx = compute_inverted_index(nodes, "pattern")

    # 集群（从 concept_relations.md 加载）
    clusters = load_clusters_from_relations(RELATIONS_PATH)

    # 别名
    aliases = load_name_aliases(ALIASES_PATH)

    # 统计
    total_wikilinks = sum(n["out_degree"] for n in nodes.values())
    unique_targets = len(set(
        t for n in nodes.values() for t in n["out_links"]
    ))

    elapsed = time.time() - start_time

    return {
        "meta": {
            "version": 1,
            "total_concepts": len(nodes),
            "last_built": datetime.now(timezone.utc).isoformat(),
            "build_mode": "full",
            "source_path": CONCEPT_DIR,
            "scan_stats": {
                "files_scanned": scanned,
                "wikilinks_found": total_wikilinks,
                "unique_targets": unique_targets,
                "build_duration_seconds": round(elapsed, 3),
            },
        },
        "nodes": dict(sorted(nodes.items())),
        "edges": edges,
        "orphan_nodes": orphans,
        "broken_links": broken,
        "clusters": clusters,
        "apply_index": apply_idx,
        "domain_index": domain_idx,
        "discipline_index": discipline_idx,
        "pattern_index": pattern_idx,
        "name_aliases": aliases,
        "potential_duplicates": duplicates,
        "vocabulary": VOCABULARY,
    }


# ── 增量构建 ──────────────────────────────────────────────

def build_incremental_index() -> dict:
    """增量更新：只重扫变动文件，但重算所有派生数据。"""
    if not os.path.exists(INDEX_PATH):
        print("索引文件不存在，回退到全量构建")
        return build_full_index()

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        existing = json.load(f)

    last_built_str = existing.get("meta", {}).get("last_built", "")
    if not last_built_str:
        print("无法读取 last_built 时间戳，回退到全量构建")
        return build_full_index()

    try:
        last_built = datetime.fromisoformat(last_built_str)
    except ValueError:
        print(f"无法解析时间戳: {last_built_str}，回退到全量构建")
        return build_full_index()

    # 如果时间戳无时区，假设 UTC
    if last_built.tzinfo is None:
        last_built = last_built.replace(tzinfo=timezone.utc)

    nodes = existing.get("nodes", {})
    indexed_files = {node["file"] for node in nodes.values()}

    # 当前文件系统上的文件
    current_files = set()
    for fname in os.listdir(CONCEPT_DIR):
        if fname.endswith('.md') and fname != 'INDEX.md':
            fpath = os.path.join(CONCEPT_DIR, fname)
            if os.path.isfile(fpath):
                current_files.add(fname)

    added = current_files - indexed_files
    removed = indexed_files - current_files

    # mtime > last_built 的文件
    modified = set()
    for fname in current_files:
        filepath = os.path.join(CONCEPT_DIR, fname)
        mtime = datetime.fromtimestamp(
            os.path.getmtime(filepath), tz=timezone.utc
        )
        if mtime > last_built:
            modified.add(fname)

    to_scan = added | modified

    start_time = time.time()

    # 重扫变动文件
    for fname in to_scan:
        filepath = os.path.join(CONCEPT_DIR, fname)
        node = scan_file(filepath)
        if node:
            name_cn = fname[:-3]
            nodes[name_cn] = node

    # 删除已不存在的文件
    removed_names = []
    for name, node in nodes.items():
        if node["file"] in removed:
            removed_names.append(name)
    for name in removed_names:
        del nodes[name]

    # 重算所有派生数据
    compute_in_links(nodes)
    edges = compute_edges(nodes)
    orphans = compute_orphans(nodes)
    broken = compute_broken_links(nodes)
    components = compute_connected_components(nodes)
    duplicates = detect_duplicates(nodes)

    apply_idx = compute_inverted_index(nodes, "apply")
    domain_idx = compute_inverted_index(nodes, "domain")
    discipline_idx = compute_inverted_index(nodes, "discipline")
    pattern_idx = compute_inverted_index(nodes, "pattern")

    clusters = load_clusters_from_relations(RELATIONS_PATH)
    aliases = load_name_aliases(ALIASES_PATH)

    elapsed = time.time() - start_time

    total_wikilinks = sum(n["out_degree"] for n in nodes.values())
    unique_targets = len(set(
        t for n in nodes.values() for t in n["out_links"]
    ))

    return {
        "meta": {
            "version": 1,
            "total_concepts": len(nodes),
            "last_built": datetime.now(timezone.utc).isoformat(),
            "build_mode": "incremental",
            "source_path": CONCEPT_DIR,
            "scan_stats": {
                "files_scanned": len(to_scan),
                "files_added": len(added),
                "files_modified": len(modified),
                "files_removed": len(removed),
                "wikilinks_found": total_wikilinks,
                "unique_targets": unique_targets,
                "build_duration_seconds": round(elapsed, 3),
            },
        },
        "nodes": dict(sorted(nodes.items())),
        "edges": edges,
        "orphan_nodes": orphans,
        "broken_links": broken,
        "clusters": clusters,
        "apply_index": apply_idx,
        "domain_index": domain_idx,
        "discipline_index": discipline_idx,
        "pattern_index": pattern_idx,
        "name_aliases": aliases,
        "potential_duplicates": duplicates,
        "vocabulary": VOCABULARY,
    }


# ── 校验模式 ──────────────────────────────────────────────

def run_check() -> None:
    """校验所有概念页 frontmatter 是否合规。"""
    nodes = {}
    for fname in os.listdir(CONCEPT_DIR):
        if not fname.endswith('.md') or fname == 'INDEX.md':
            continue
        filepath = os.path.join(CONCEPT_DIR, fname)
        if not os.path.isfile(filepath):
            continue
        node = scan_file(filepath)
        if node:
            nodes[fname[:-3]] = node

    violations = validate_frontmatter(nodes, VOCABULARY)

    print(f"概念库校验报告（{len(nodes)} 概念）\n")

    if not violations:
        print("所有概念页 frontmatter 均合规。")
        return

    # 按字段分组
    by_field = defaultdict(list)
    for v in violations:
        by_field[v["field"]].append(v)

    for field, items in sorted(by_field.items()):
        print(f"### {field} 问题（{len(items)} 处）：")
        for item in items:
            val = item["value"]
            print(f"  - {item['concept']}: {field} = {val}")
        print()

    print(f"共 {len(violations)} 处问题。")


# ── 原子写入 ──────────────────────────────────────────────

def write_index(index: dict) -> None:
    """原子写入索引文件。"""
    os.makedirs(MEMORY_DIR, exist_ok=True)

    tmp_path = INDEX_PATH + ".tmp"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    os.replace(tmp_path, INDEX_PATH)


# ── 自洽性检查 ────────────────────────────────────────────

def self_check(index: dict) -> List[str]:
    """索引自洽性验证，返回警告列表。"""
    warnings = []
    nodes = index["nodes"]

    # 概念数一致
    if len(nodes) != index["meta"]["total_concepts"]:
        warnings.append(
            f"nodes 数量 {len(nodes)} ≠ meta.total_concepts {index['meta']['total_concepts']}"
        )

    # 边数一致
    total_out = sum(n["out_degree"] for n in nodes.values())
    if total_out != len(index["edges"]):
        warnings.append(
            f"edges 数量 {len(index['edges'])} ≠ sum(out_degree) {total_out}"
        )

    # 孤立节点存在于 nodes
    for name in index["orphan_nodes"].get("fully_isolated", []):
        if name not in nodes:
            warnings.append(f"孤立节点 '{name}' 不在 nodes 中")

    for item in index["orphan_nodes"].get("semi_isolated", []):
        if item["name"] not in nodes:
            warnings.append(f"半孤立节点 '{item['name']}' 不在 nodes 中")

    # 断链目标不在 nodes
    for bl in index["broken_links"]:
        if bl["target"] in nodes:
            warnings.append(f"断链 '{bl['source']}'→'{bl['target']}' 目标实际存在")

    return warnings


# ── main ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="概念库索引生成器")
    parser.add_argument(
        "--incremental", "-i",
        action="store_true",
        help="增量模式：只处理变动文件",
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="校验模式：检查 frontmatter 词汇表合规",
    )
    args = parser.parse_args()

    if args.check:
        run_check()
        return

    print(f"概念页目录: {CONCEPT_DIR}")
    print(f"索引输出: {INDEX_PATH}")

    if args.incremental:
        print("模式: 增量")
        index = build_incremental_index()
    else:
        print("模式: 全量")
        index = build_full_index()

    # 自洽性检查
    warnings = self_check(index)
    if warnings:
        print("\n⚠️ 自洽性警告：")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("\n✅ 自洽性检查通过")

    # 写入
    write_index(index)

    # 输出摘要
    meta = index["meta"]
    print(f"\n索引构建完成")
    print(f"  概念数: {meta['total_concepts']}")
    print(f"  孤立节点: {len(index['orphan_nodes']['fully_isolated'])} 完全 + "
          f"{len(index['orphan_nodes']['semi_isolated'])} 半孤立")
    print(f"  断链: {len(index['broken_links'])} 处")
    print(f"  边数: {len(index['edges'])}")
    print(f"  集群: {len(index['clusters'])} 个")
    print(f"  潜在重复: {len(index['potential_duplicates'])} 对")
    print(f"  耗时: {meta['scan_stats']['build_duration_seconds']}s")


if __name__ == "__main__":
    main()
