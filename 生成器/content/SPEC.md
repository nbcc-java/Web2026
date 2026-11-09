# 《网页制作（HTML5+CSS3）》课件内容编写规范（SPEC）

每个教学单元（40 分钟）对应一个 JSON 文件，如 `U03.json`。生成器会把同一份 JSON
渲染成「带动画特效的单文件 HTML 课件」和「对应 PPTX 课件」。

**先读范例**：`U01.json`、`U02.json`（同目录）是已定稿的样板，请严格模仿其结构、
语气、详略程度与字段写法。

## 一、顶层字段

| 字段 | 必填 | 说明 |
|---|---|---|
| id | ✓ | 单元编号，如 `U03` |
| project | ✓ | 如 `项目2` |
| project_name | ✓ | 如 `HTML 基础` |
| unit | ✓ | 如 `第 3 单元` |
| title | ✓ | 单元标题（会被渲染成大标题） |
| subtitle | ✓ | 一句话说明本单元主线 |
| duration | ✓ | 固定写 `40` |
| cover_tags | ✓ | 封面标签 3～5 个（短词） |
| ref_book | ✓ | 固定写 `电子工业出版社 · 2025 年 1 月第 1 版` |
| objectives | ✓ | `{knowledge:[], skill:[], literacy:[]}`，来自教材各项目扉页 |
| slides | ✓ | 幻灯片数组，见下 |

## 二、支持的幻灯片类型（只能用这些）

| type | 必要字段 | 用途 |
|---|---|---|
| `objectives` | title, objectives | 学习目标（每个单元第 1 张） |
| `ideology` | title, text, topic? | 思政课堂（引用教材原文，可加 `<strong>`） |
| `outline` | title, items[4~6] | 本单元导览 |
| `section` | no, title, text? | 章节过渡页（一个大单元内分 2～3 个小节时使用） |
| `bullets` | title, items | 知识要点（可含 `<strong>` `<code>`） |
| `cards` | title, items[{title,text}], cols? | 要点分解（2/3 列卡片） |
| `table` | title, head[], rows[[]] | 对照表 |
| `compare` | title, a{title,items}, b{title,items} | 左右对比辨析 |
| `steps` | title, items[{title,text?}] | 操作步骤 |
| `flow` | title, items[{title,text}], note? | 原理流程图解 |
| `code` | title, code, lang, file?, caption? | 代码示例 |
| `codebullets` | title, items, code, lang, file? | 代码 + 要点（左右分栏） |
| `task` | title, goal, steps[], code?, lang? | 任务驱动 |
| `demo` | title, items[], html, code?, lang?, hint? | **实时效果演示**（HTML 里内嵌可运行页面） |
| `ai` | title, text, items[] | AI 前沿知识 |
| `quiz` | title, items[{q,type,options,answer,tip?}] | 随堂检测（每单元 2~5 题，至少 1 道多选；`type` 为 `single`/`multi`，多选答案写多个字母如 `ABD`；HTML 版可点选判分，PPTX 版答案写入演讲者备注） |
| `summary` | title, items[] | 本课小结 |
| `homework` | title, items[] | 课后作业 |
| `refs` | title, items[{t,u}] | 出处与参考 |
| `end` | title, text | 结束页（每单元最后一张） |

每个 slide 都可加可选字段 `nav`（目录里的短标题）和 `subtitle`。

## 三、单元的固定结构（顺序）

1. `objectives` — 目标（照抄教材项目扉页的学习/技能/素养目标，允许精简到 3～4 条/组）
2. `ideology` — 思政课堂（教材项目扉页原文）
3. `outline` — 导览
4. 若干 `section` + 知识页（`bullets`/`cards`/`table`/`compare`/`code`/`codebullets`/`steps`/`flow`/`task`/`demo`）
5. `ai` — AI 前沿（每单元 1 张，必须与本单元主题强相关，不得泛泛而谈）
6. `quiz` — 随堂检测（每单元 2~5 题、至少 1 道多选；优先用教材课后选择题，多选可用
   `{"type":"multi","q":"……正确的有（　　）","options":["A. …","B. …","C. …","D. …"],"answer":"ABD","tip":"解析"}`）
7. `summary` — 本课小结（4~5 条）
8. `homework` — 课后作业（尽量用教材原作业）
9. `refs` — 出处与参考（第 1 条必须是教材对应项目与小节；其余 3~5 条为权威出处）
10. `end` — 结束页

总张数控制在 **18～24 张**（含首尾）。

## 四、硬性要求

1. **内容必须忠于教材笔记**（会提供 notes 文件），技术表述准确；笔记中标注的教材印刷疑误，
   按**正确写法**表述，并可在 caption 中用一句话说明「教材原文为 X，此处按标准表述为 Y」。
2. **权威出处**：技术结论优先引用 MDN Web Docs（中文）、W3C/WHATWG 官方规范、
   官方文档（如 developer.mozilla.org、www.w3.org）。URL 必须真实可信、指向对应主题页。
3. **代码**：教材里的代码片段要保留；`lang` 只能是 `html` / `css` / `text`。
   代码中的 `<`、`>`、`"` 按原始代码写（JSON 里正常转义）。
4. **demo 页的 `html` 字段**：必须是一段**自包含**的 HTML 片段（含 `<style>`），
   不引用任何外部资源（不用外链图片/字体/JS），在 660px 宽、约 300～400px 高的区域内
   自适应展示。鼓励使用 CSS 动画，让课堂演示「动起来」。演示内容必须与本单元知识直接相关。
5. **文字内联标记**：只允许 `<strong>`、`<code>`、`<br>`；不要用其他标签。
   `esc` 之外的字段都按 HTML 渲染，所以**不要写裸的 `<` `>` 数学符号**（写成「小于」或 `&lt;`）。
6. **语言风格**：面向高职学生，简洁、严谨、口语适度；每个要点尽量不超过 60 字；
   关键术语加 `<strong>`，代码/属性名加 `<code>`。
7. **思政**：引用教材项目扉页原文（笔记里有），`topic` 给一个结合岗位的课堂讨论题。
8. **AI 前沿**：结合本单元知识讲（例如讲选择器时讲「AI 如何理解 DOM 结构」），
   可提 GitHub Copilot、通义灵码、文心快码、DeepSeek 等真实工具，不得编造不存在的产品。
9. JSON 必须 UTF-8、无注释、可直接被 `json.load` 解析；文件名 `UXX.json`。

## 五、自查清单（提交前逐条确认）

- [ ] `python -c "import json;json.load(open('UXX.json'))"` 通过
- [ ] 所有 slide 的 type 都在支持列表里
- [ ] 每个 `demo` 都有自包含 `html` 字段
- [ ] 没有 5 张以上连续纯文字页；每 3～5 页有一次互动（demo/quiz/task）
- [ ] `refs` 里至少 3 条带真实 URL 的权威出处
- [ ] 单元标题、项目名、单元编号正确
