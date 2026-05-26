---
name: "knowledge-cards"
description: "将知识内容（哲学概念、圆桌讨论、寓言故事、方法论等）改写为可传播的卡片格式 HTML，内置逐张导出 JPG 和分页 PDF 功能。用户说\"传播版\"\"知识卡片\"\"做成卡片\"\"可传播格式\"\"发到小红书\"时触发。"
---

# Knowledge Cards · 知识传播卡片

## 触发条件

用户说以下任意内容时执行本 skill：
- "传播版""做成可传播的格式"
- "知识卡片""卡片格式"
- "小红书卡片""做成图文"
- "发到小红书""传播用"

---

## Step 1：理解内容

分析传入的内容，识别：

1. **内容类型**：哲学概念 / 圆桌讨论 / 寓言故事 / 方法论 / 其他
2. **核心论点**：每张卡片承载一个核心观点，不堆砌
3. **卡片数量**：根据内容深度，一般 10–15 张

---

## Step 2：选择设计系统

**格式统一，风格不统一。** 所有系统共用相同的卡片结构和导出方式，视觉语言根据内容选择。

用户有指定时优先使用，否则按下方判断逻辑自动选择。

| ID | CSS 文件路径 | 字体 | 适用场景 |
|----|-------------|------|---------|
| `xhs-card` | `skills/report-to-html-pdf/references/xhs-card-style.css` | 楷体 + Caveat | 哲学叙事、寓言故事、带温度的人文内容；适合「说故事」型内容 |
| `structured-dark` | `skills/report-to-html-pdf/references/structured-dark-card-style.css` | Noto Sans + JetBrains Mono | 分析性强、AI/技术/认识论/数据类内容；多轮圆桌有结构图时优先考虑 |
| `roundtable-card` | `skills/report-to-html-pdf/references/roundtable-card-style.css` | 楷体 + Caveat | 暖奶油底 + 嘉宾彩色左边框，适合轻松的多人对话/心理/社科类圆桌 |
| `orange-card` | `skills/report-to-html-pdf/references/orange-card-style.css` | system-ui + ZY LOYALTY（MERJIC品牌水印） | **麦橘品牌默认风格**。奶油白底 + 麦橘橘 #E85D1C，支持故事+圆桌混合内容，发言人名字内联加粗，无列对齐问题，手机直接可读。除非有特殊指定，优先选此风格。 |
| `merjic-card` | `skills/concept-studio/modules/merjic-card-style.css` | Noto Serif SC + Noto Sans SC + JetBrains Mono + ZY LOYALTY | **麦橘固定版式系统**。三区锚点（抬头/签名/页码绝对定位），内容区硬约束不溢出。适用于寓言故事 + 圆桌讨论（多轮次）+ 尾声三板块组合内容。封面：大标题 + 一句话副标题。内容页（圆桌）：引言引用框 + 第三人称诠释（禁用「简言之」总结框）。内容页（寓言）：纯叙事，无引用框。 |
| `merjic-swiss` | 内联生成，无外链 CSS | Inter + Noto Sans SC + JetBrains Mono + ZY LOYALTY（仅品牌水印） | **麦橘瑞士风卡片**。竖向 375×500px（3:4），直角无阴影无圆角无渐变。单一强调色 `#e0620a`（MERJIC Orange）。`--ink: #0a0a0a` / `--paper: #fafaf8`。四种卡面：light / dark / accent / grey。全程无衬线。适合寓言故事 + 圆桌讨论混排，小红书首选。 |
| `merjic-swiss-dark` | `skills/concept-studio/modules/merjic-swiss-dark-card-style.css` | Inter + Noto Sans SC + JetBrains Mono + ZY LOYALTY（品牌水印 9px） | **麦橘瑞士风·黑橙白圆桌专用**。竖向 375×500px（3:4），直角无阴影无圆角无渐变。三种底色：dark(#0A0A0A) / paper(#FAFAF8) / accent(#E0620A)。严格深浅交替，综述位用橘色。人物颜色系统：每位参与者分配固定色，贯穿圆点+竖线+高亮词。黑底白字、白底黑字。封面用钩子问句，不写人名。圆桌讨论/多人对话首选。 |

**自动选择判断逻辑：**
- 默认 → `orange-card`（麦橘品牌标准卡片）
- 圆桌讨论/多人对话，明确需要黑橙白风格 → `merjic-swiss-dark`
- 内容含大量技术术语、AI话题、结构图表、认识论/逻辑分析 → `structured-dark`
- 内容以故事为主、人文叙事、温暖情感 → `xhs-card`
- 内容是轻松多人对话、心理/生活/社科类圆桌 → `roundtable-card`
- 内容是寓言故事 + 圆桌讨论（多轮）+ 尾声的组合，或明确要求固定版式 → `merjic-card`
- 用户说「瑞士风」「黑橙白」→ `merjic-swiss` 或 `merjic-swiss-dark`

**扩展方式：** 新设计系统出现后，在上方注册表新增一行，CSS 文件放入对应 skill 的 `references/` 目录。skill 核心逻辑不需要改动。

---

## Step 3：内容改写规范

传播版和留档版的核心区别在于表达方式，不在于内容深度。

### 专业词汇

- 保留专业术语，目标是让读者理解这些词，不是回避它们
- 第一次出现时，紧跟破折号或括号解释一句话
- 后续出现直接使用，不重复解释

### 叙述视角

- 人物卡片里，人物发言用**第一人称**——代入感更强，读者更能感受到各方立场和情绪
- 叙述者（主持/综述）用第三人称或无人称
- 一张卡片内不混用第一/第三人称
- 人物姓名在卡片头部标注，正文直接用"我"，不需要"法兰克福认为"这类前缀

### 内容密度

- 每张卡片一个核心观点，不压缩也不稀释
- 开头用场景或具体问题引入，不直接抛结论
- 高认知读者能看出论证深度，普通读者能跟上基本逻辑
- 相邻卡片的逻辑关系要清晰，读者知道下一张在做什么

### 禁用结构

- 否定排比："不是…而是…""不仅…而且…"
- 公式化结尾："挑战与未来展望"等
- 学术标注："核心命题""核心挑战"等词——结论直接写进正文
- 简言之 / 总而言之总结框：去掉，核心观点直接融入正文段落
- 解释性语气："这种 X 就是 Y 的问题"——改成直接陈述，不解释自己在解释
- 论点条目化：不要把哲学家的立场变成要点列表，还原成发言现场

---

## Step 3.5：故事改写专项规范

内容含寓言故事时额外检查：

### 普世性要求

- 场景对任何背景的人都能代入，不靠职业/阶级/特定经历才能共情
- 避免升职、出国、高消费、精英职场等有门槛的触发点——这些场景让一部分读者出戏
- 自检标准：初中生能跟上情节发展吗？不行则重写场景
- 人物用普通名字 + 普通处境（上班族、室友、家庭对话），不用研究员/学者等专业角色

### 故事结尾

- 结尾是行动或感受的描写，不是修辞性反问句
- 反问句（"你有多少个……其实是……？"）放在结尾显说教，去掉或改成叙述
- 转折靠情节本身，不靠总结句兜底

### 圆桌语气分化

- 每位发言者有不同的语气节奏：有的干脆、有的迂回、有的带刺、有的冷静
- 不要让每个人的段落读起来像同一个人在用不同观点说话
- 第一人称发言：直接说立场，不需要"我认为""我觉得"等缓冲前缀

---

## Step 4：卡片结构参考

根据内容类型灵活组合，不必全部使用：

| 卡片类型 | 用途 | 说明 |
|---------|------|------|
| 封面 | 开篇 | 钩子问句 + 主题词 + 来源/时间标注 |
| 概念引入 | 核心词首次出场 | 一句话定义 + 生活类比 |
| 黑底登场卡 | 多人物场景 | 列出全部角色 + 各自一句话立场，深色背景区分 |
| 人物卡 | 单人论点 | 全名 + 一句话身份背景 + 论点 + 结论框 |
| 综述卡 | 阶段收口 | 指出分歧在哪、裂缝有几条，不下结论 |
| 结尾卡 | 收尾 | 未竟之问 / 留给读者的开放性问题 |

**人物卡格式要求：**
- 必须有全名（中文名 + 外文名）
- 必须有一句话背景，说明他们为什么出现在这里
- 例：`Gary Watson · 分析哲学家，首先质疑欲望层级框架`

**圆桌发言人排版规范（`merjic-swiss-dark` 专用）：**
- 人名格式：`中文简称 · 英文简称`（发言卡/对话卡），`中文全名  英文全名`（阵容卡）
- 发言正文：纯中文简称，不出英文
- 每位发言人分配固定颜色，贯穿圆点+竖线+高亮词
- 阵容卡圆点用人物专属色，不用灰色/黑色方块
- 对话卡内两位发言人之间用 dialogue-divider 分隔

**圆桌发言人排版规范（其他风格）：**
- 人名下方单独一行写英文名，再下一行写一句话介绍
- 不内联在括号里，不塞进圆圈/浮标，每位发言者格式一致
- 例：
  ```
  奥诺拉·奥尼尔
  Onora O'Neill
  信任与问责理论家，质疑"可信度差异即不正义"的预设
  ```

**卡片抬头标签规范：**
- 揭示/定义某个概念或原理的卡片 → 标 `核心概念`
- 其他所有卡片（叙事、圆桌发言、综述等）→ 统一用系列主题（即封面大标题，如「寓言故事 · 圆桌讨论」）
- **禁止**写英文学科名（如 EPISTEMOLOGY、PHILOSOPHY 等），也不写中文学科名（如「哲学」「认识论」）
- 无法归类时，回归系列主题，不要另造分类

---

## Step 5：生成 HTML

将选定设计系统的 CSS **内联到 `<style>` 标签**（不用外链，保证离线可用和截图完整）。

**PDF 导出必须用 html2canvas + jsPDF，不能用 `window.print()`。** 浏览器打印引擎和屏幕渲染引擎不同，颜色、字体、间距都会偏移，只有截图方式才能做到所见即所得。

标准 HTML 骨架：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>[主题] · 图文系列</title>
  <link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Caveat:wght@400;600;700&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
  <style>
    /* 内联设计系统 CSS */
    /* 必须在 .card 上加：print-color-adjust: exact; -webkit-print-color-adjust: exact; */
  </style>
</head>
<body>
  <div class="page-header">[主题] · 图文系列 · 共 N 张</div>
  <div class="stack">
    <!-- 卡片列表，每张 <div class="card"> -->
  </div>
  <div class="hint">点「导出 PDF」保存整份 PDF（每卡一页，所见即所得）<br>或点「导出图片」逐张保存 JPG</div>
  <div class="export-bar">
    <button class="btn btn-o" onclick="exportPDF()">导出 PDF</button>
    <button class="btn" onclick="exportAll()">导出图片</button>
    <span class="export-status" id="status"></span>
  </div>
  <script>
  // 截图前把「」包进带 padding 的 span，强制 layout 引擎撑开间距
  // 截图后还原 innerHTML，不影响页面显示
  // 原因：html2canvas 渲染 canvas 文字时，CJK 字体的内置 kern 规则会把「」压紧
  // letterRendering: true 对全角括号无效；只有 DOM 层的物理间距才可靠
  function wrapBrackets(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    const nodes = [];
    let n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(node => {
      if (!/[「」]/.test(node.textContent)) return;
      const frag = document.createDocumentFragment();
      node.textContent.split(/(「|」)/).forEach(part => {
        if (part === '「' || part === '」') {
          const s = document.createElement('span');
          s.style.cssText = 'display:inline-block;padding:0 2px;letter-spacing:0;';
          s.textContent = part;
          frag.appendChild(s);
        } else if (part) {
          frag.appendChild(document.createTextNode(part));
        }
      });
      node.parentNode.replaceChild(frag, node);
    });
  }

  async function captureCard(card) {
    const saved = card.innerHTML;
    wrapBrackets(card);
    await new Promise(r => requestAnimationFrame(r));
    const canvas = await html2canvas(card, { scale: 3, useCORS: true, backgroundColor: null });
    card.innerHTML = saved;
    return canvas;
  }

  async function exportPDF() {
    const { jsPDF } = window.jspdf;
    const cards = document.querySelectorAll('.card');
    const status = document.getElementById('status');
    status.textContent = '生成中…';
    const pw = 180, ph = 240; // 3:4
    const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: [pw, ph] });
    for (let i = 0; i < cards.length; i++) {
      status.textContent = 'PDF: ' + (i + 1) + ' / ' + cards.length;
      const canvas = await captureCard(cards[i]);
      const imgData = canvas.toDataURL('image/jpeg', 0.95);
      if (i > 0) doc.addPage([pw, ph]);
      doc.addImage(imgData, 'JPEG', 0, 0, pw, ph);
    }
    doc.save('[主题].pdf');
    status.textContent = '完成 ✓';
    setTimeout(() => { status.textContent = ''; }, 3000);
  }

  async function exportAll() {
    const cards = document.querySelectorAll('.card');
    const status = document.getElementById('status');
    status.textContent = '生成中…';
    const zip = new JSZip();
    for (let i = 0; i < cards.length; i++) {
      status.textContent = (i + 1) + ' / ' + cards.length;
      const canvas = await captureCard(cards[i]);
      const base64 = canvas.toDataURL('image/jpeg', 0.92).split(',')[1];
      zip.file(String(i + 1).padStart(2, '0') + '.jpg', base64, { base64: true });
    }
    status.textContent = '打包中…';
    const blob = await zip.generateAsync({ type: 'blob' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = '[主题]-麦橘知识卡片.zip';
    link.click();
    status.textContent = '完成 ✓';
    setTimeout(() => { status.textContent = ''; }, 3000);
  }
  </script>
</body>
</html>
```

---

## Step 6：质检

- [ ] `.card` 上有 `print-color-adjust: exact; -webkit-print-color-adjust: exact`，否则 PDF 导出背景色会消失
- [ ] 每张卡片内容在 `aspect-ratio: 3/4` 固定高度内不溢出——flex 容器满载时所有子项会被等比压缩，文字挤成一团。**解决方式：去掉该卡的 `.spacer`，降低字号（至少 1px），收紧段落 margin**
- [ ] 人物卡有全名 + 一句话背景
- [ ] 叙述视角统一，无第一/第三人称混用
- [ ] 专业术语首次出现有解释
- [ ] 相邻卡片逻辑关系清晰
- [ ] 结尾有开放性问题

**视觉格式专项（`merjic-swiss` 风格）：**
- [ ] 页脚 `brand-mark` 只写 `MERJIC`，字体 `ZY LOYALTY`，无其他文字（禁止「知识系列」「XXX系列」等系列标识，禁止日期）
- [ ] 封面页眉左上角无文字（封面不需要系列标记，标签留给内容页）
- [ ] 卡片内部无横向分割线（间距靠 `margin`/`gap`，不靠线条）
- [ ] 无结构性边框（边框不传递信息时不加）
- [ ] 直角无阴影无圆角无渐变（`border-radius: 0`，无 `box-shadow`，无 `linear-gradient`）
- [ ] 封面 `.t-hero` 的 `margin-top: auto` 在 footer 生效——不被内联 `style="margin-top:Xpx"` 覆盖

**`merjic-swiss-dark` 硬性规范（全部必须遵守，无例外）：**

### 底色规则
- 只有三种底色：`dark`(#0A0A0A) / `paper`(#FAFAF8) / `accent`(#E0620A)。禁止 `grey`，禁止任何其他中间色
- 严格深浅交替：dark → paper → dark → paper → …
- 综述卡（轮次综述、最终共识）用 `accent`(橘色)，打断交替节奏
- 首页（封面）和末页（结尾）必须是 `dark`

### 底色序列模板（18张）
```
01 dark    封面/钩子
02 paper   概念引入
03 dark    人物阵容（深色撑信息密度）
04 paper   发言1
05 dark    发言2
06 paper   发言3
07 dark    发言4
08 paper   发言5
09 accent  轮次综述1（打断交替）
10 paper   对话1
11 dark    对话2
12 paper   对话3
13 accent  轮次综述2（打断交替）
14 paper   对话4
15 dark    对话5
16 paper   收束
17 accent  最终综述（打断交替）
18 dark    结尾
```

### 文字颜色规则
- dark 底 → 白字（rgba(255,255,255,0.82) 正文，#fff 标题）
- paper 底 → 黑字（#525252 正文，#0a0a0a 标题）
- accent(橘)底 → 白字（rgba(255,255,255,0.9) 正文，#fff 标题）
- 禁止在任何底色上出现灰字(#737373)——accent 底上的灰字必须覆盖为白色(0.6~0.8 透明度)
- paper 卡上禁止出现白色文字——如果改过底色 class，必须同步清理 inline style 中的白色 color

### 人物颜色系统
- 每位参与者分配固定颜色，生成卡片时一次性确定，贯穿全系列所有卡片
- 默认色板（可按人物气质调整，但五色必须和谐且有区分度）：
  - 角色1：#e0620a（橙）
  - 角色2：#c0392b（红）
  - 角色3：#f1c40f（金黄，dark 底上用 #d4a500 提亮）
  - 角色4：#3498db（蓝）
  - 角色5：#27ae60（绿）
- 颜色必须出现在以下所有位置：
  1. 阵容卡的圆点（participant-initial.c1~c5）
  2. 发言卡/对话卡的 speaker-dot 圆点（.dot-xxx）
  3. 发言卡的 quote-block 左竖线（.quote-block.xxx）
  4. 正文中的高亮关键词（.text-xxx）
- dark 底上自动提亮人物色（确保白底可读）
- accent(橘)底上人物色降级为白色（橘底上对比度不够）

### 人名格式
- 阵容卡（人物介绍页）：`中文全名  英文全名`（双空格分隔，不用 `·`）
- 发言卡/对话卡 speaker-name：`中文简称 · 英文简称`
- 发言正文内容：纯中文简称，不出英文（如「韦伯的框架」而非「韦伯 · Weber的框架」）
- 阵容卡中，中文全名和英文全名之间不用点号，用空格
- 圆点用人物专属色，不用灰色/黑色方块

### 封面（首页）规范
- 封面不写人名列表
- 用钩子问句做大标题——直击核心困惑，让读者想翻下去
- 格式：`<div class="t-hero">一句话钩子<br><span style="color:#ff8040;">关键词高亮</span></div>`
- 底部只写「N位不同领域的声音，追问同一个问题」（或类似），不列人名

### 品牌水印
- 字体：ZY LOYALTY（fallback JetBrains Mono）
- 字号：9px
- 字间距：0.06em
- 颜色：paper 底 #737373，dark 底 rgba(255,255,255,0.35)，accent 底 rgba(255,255,255,0.6)
- 位置：每张卡右下角 card-footer 内

### 人物选择
- 不限于 scholar-dict 中的学者，拒绝信息茧房
- 可加入 influencer、公众人物、行业实践者——任何对该议题有独立见解的人
- scholar-dict 仅用于名字拼写对照，不是人物准入名单

### 排版硬约束
- 固定宽高 375×500px，不用 aspect-ratio（浏览器兼容性不稳定）
- 每张卡 2-3 段 t-body 文字，绝不多塞
- 字重：hero/xl = 200（极细），body = 300，标题禁止用 400 以上
- 禁止使用 ASCII 图表/frame-box（小卡片上排版不可控）
- 禁止使用 Noto Serif SC（标题统一用 Noto Sans SC）
- 对话分隔线：dark 底用 `rgba(255,255,255,0.12)`，paper 底用 `rgba(0,0,0,0.06)`

---

## Step 7：输出

文件保存到 `个人总部/output/知识卡片/YYYY-MM-DD-[主题]-cards.html`。

**字体文件**：`个人总部/output/知识卡片/fonts/` 目录下已有所需字体（ZY Loyalty.ttf / Inter / Noto Sans SC / JetBrains Mono）。HTML 中 @font-face 使用相对路径 `fonts/ZY Loyalty.ttf`。

**ZY LOYALTY 字体注意**：
- 字体文件来源：剪映缓存目录 `/Users/myke/Movies/JianyingPro/User Data/Cache/effect/66322554/1e9b242443a9943a43ccf30604243978/ZY Loyalty.ttf`
- 该字体是剪映内置字体，版权属字节跳动，跨平台分发（小红书等）存在法律风险
- 仅用于品牌水印 MERJIC（6个字母），实际追偿概率极低，但风险确实存在
- 如果缓存被清空，在剪映中重新使用该字体效果即可恢复缓存

告知用户：
- 浏览器打开，点「导出图片」逐张保存 JPG
- 或点「导出 PDF」导出多页 PDF（每卡一页，所见即所得，走 html2canvas 截图而非浏览器打印）
