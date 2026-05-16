# 概念库

遵循全局 CLAUDE.md 的通用规则（称呼、语言、交互风格），以下为本项目补充。

## 每次对话必读

对话开始时，读取 `memory/MEMORY.md`——词汇表、字段规范、行为规则全部在里面，不读不开工。

---

## 目录结构

- `概念页/` — 全部概念 .md 文件 + INDEX.md（Dataview 自动索引），可单独作为 Obsidian vault 打开
- `memory/` — MEMORY.md（规则索引）+ workflow_obsidian_concepts.md（设计原则、背景参考）
- skills 统一在 `个人总部/skills/`，不在项目级维护
- `CLAUDE.md` — 本项目入口指令

这是麦橘的个人知识资产库，用 Obsidian 管理。存放跨领域的概念沉淀，供长期积累和检索使用。

## 工作目标

- 用寓言故事将新概念转化为结构化页面
- 用圆桌讨论探索概念之间的张力和关联
- 用 knowledge-cards 将概念做成可传播的内容

## 概念页格式规范

5 个固定字段，顺序和名称不得增减或改名：

```yaml
---
name: 概念名称（English Name）
domain: [经济学]
date: YYYY-MM-DD
source: 寓言故事
tags: [pattern/循环, apply/商业, discipline/行为经济学]
---
```

**禁用字段：** `title` `slug` `created` `related` `updated` `aliases` `name_en` `status`

词汇表（domain / pattern / apply / discipline 的固定值和扩展权限）在 `memory/MEMORY.md` 中。

## 关联 Skills（全局，个人总部/skills/）

- parable-story：寓言故事写概念
- roundtable：多视角圆桌讨论
- knowledge-cards：知识卡片传播
- cognitive-map-explorer：认知地图漫游
- humanizer-zh：去 AI 痕迹
