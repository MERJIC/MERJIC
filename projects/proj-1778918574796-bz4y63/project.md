# 概念库维护与关联分析

## 目标

持续维护 `概念页/` 的数据质量，定期运行关联分析，确保概念之间的隐性关联被发现并通过 [[]] 链接显性化。

## 当前状态（2026-05-23）

- 总概念数：421+
- 已确认集群：14 个（A-N）
- 断链：0
- 章节完整性：421+/421+ 四段齐全（100%） ✅
- 板块排序：全部统一为 核心机制→入口场景→现实锚点→适用边界→圆桌沉淀 ✅
- 入口场景规范：所有来源统一故事体，概念跳跃路径移至核心机制 ✅
- 现实锚点格式：统一为 bullet point ✅
- 索引层：分片架构，全量构建 ~0.1s ✅

**概念页格式规范、自检规则、词汇表以 `skills/concept-studio/`（概念库项目内）为唯一权威。** 本项目不再重复记录规范细节。

## 工具

- `build_index.py`：索引生成脚本（全量/增量/校验三种模式），路径 `scripts/build_index.py`
- **索引分片**（旧 `concept_index.json` 标记 deprecated）：
  - `concept_lite.json`：轻量索引（names + name_en_index + nodes_lite + 倒排索引 + orphan_nodes + vocabulary），ingest/hop/parable 只读此文件
  - `concept_graph.json`：图结构索引（nodes_graph + edges + broken_links + clusters + potential_duplicates），analyze 读此文件 + lite
  - `concept_meta.json`：管理元数据（nodes_meta: file/source/date），按需读取
- concept-studio skill：统一工作台（7个模块：寓言故事 / 摄入 / 跳跃 / 关联分析 / 知识卡片 / 寓言重写 / 圆桌讨论）
- Noosphere 插件 v0.2.0：自动索引 + 全文格式校验（frontmatter/正文/修辞三层），源码在 `概念页/.obsidian/plugins/noosphere/`
- 缓存文件：`memory/concept_relations.md`

## 工作节奏

- **每次新增概念后**：concept-studio 建页时自动查集群（从 lite 分片读取），建页后运行 `build_index.py --incremental` 刷新索引
- **每月**：运行一次增量分析，处理上月新增概念，更新集群归属和孤立列表
- **每季度**：全量重跑 `build_index.py` + analyze 模块，重建关联基准

## 数据质量检查清单

格式校验由 Noosphere 插件自动执行（frontmatter 6项 + 正文 4项 + 修辞 1项）。以下为人工关注项：

1. 断链（[[概念]] 指向不存在的页面）
2. 重复概念（不同翻译/叫法的同一概念被重复建页）
3. domain/discipline 归属错误
4. 章节结构不合规（缺核心机制/入口场景/现实锚点/适用边界）
5. 写作质量问题（「不是A，而是B」滥用 — 阈值5次以上进待整理）
6. 入口场景非故事体（概念跳跃路径应移至核心机制，入口场景统一写故事）

运行 `python3 scripts/build_index.py --check` 可自动检测 1-3 类问题。Noosphere 插件在 Obsidian 保存时自动检测全部 11 项。
