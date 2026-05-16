---
name: 概念知识库索引
description: 通过寓言故事沉淀的学科概念，每概念独立页面，含互链和圆桌沉淀
tags: [index, 寓言故事, 哲学]
---

# 概念知识库

通过 `/寓言故事` 沉淀的学科原理，每个概念一个页面。圆桌讨论结论写回各自页面的「圆桌沉淀」section。

## 全部概念

```dataview
TABLE join(domain, ", ") as "领域"
FROM ""
WHERE file.name != "INDEX"
SORT date DESC
```

## 按领域浏览

```dataview
TABLE rows.file.link as "概念"
FROM ""
WHERE file.name != "INDEX"
FLATTEN domain as d
GROUP BY d
```

## 按应用场景浏览

```dataview
TABLE rows.file.link as "概念"
FROM ""
WHERE file.name != "INDEX"
FLATTEN file.tags as tag
WHERE startswith(string(tag), "#apply/")
GROUP BY replace(string(tag), "#apply/", "") as 场景
SORT 场景 ASC
```
