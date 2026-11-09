# 《网页制作（HTML5+CSS3）》结构化备课笔记（B 段）

**覆盖范围**：PDF 第 83–199 页（book_all.txt 第 3933–13050 行）
**主要内容**：项目4 使用CSS高级选择器美化页面、项目5 盒子模型、项目6 表格和表单
**前置说明**：
- 第 83–92 页仍属 **项目3 使用CSS基本选择器美化页面** 的收尾（代码3-7 文字排版、3.3.5 自定义字体、3.3.6 伪类、3.3.7 伪元素、3.3.8 通用选择器、3.4 小结、3.5 作业）。正文本笔记从 **第 93 页 项目4** 起正式展开；第 83–92 页收录于文末「逐页要点索引」，其两张表格（表3-13、表3-14）见「附录 B」。
- 代码行号（如 `#014`）为教材代码清单的原始行号，便于课堂对照。
- 标注 **[教材疑误]** 处为原文印刷/OCR 明显不一致处，备课讲解时请按标注处理。

---

# 项目4 使用CSS高级选择器美化页面

## 一、项目扉页信息（P93）

### 思政课堂（原文要点）
> 经过几代航天人的接续奋斗，我国航天事业创造了以"两弹一星"、载人航天、月球探测为代表的辉煌成就，走出了一条自力更生、自主创新的发展道路，积淀了深厚博大的航天精神。继承和发扬航天精神是我们这代人的责任和义务。

### 学习目标（照抄要点）
- 掌握交集选择器语法
- 掌握并集选择器语法
- 掌握后代选择器语法
- 掌握子元素选择器语法
- 掌握相邻兄弟选择器语法
- 掌握属性选择器语法
- 掌握 Emment 语法 【**注**：原文即写作 Emment，实为 Emmet】

### 技能目标（照抄要点）
- 能使用交集选择器
- 能使用并集选择器
- 能使用后代选择器
- 能使用子元素选择器
- 能使用相邻兄弟选择器
- 能使用属性选择器
- 能使用 Emmet 语法

### 素养目标（照抄要点）
- 培养严谨求实的劳动态度
- 培养勇于探索、崇尚科学的意志和品德
- 培养科技报国的崇高理想

---

## 二、4.1 复合选择器（P94–P104）

> 复合选择器是指通过对基本选择器进行组合而形成的更为复杂的选择器。常用的复合选择器主要包括：交集选择器、并集选择器、后代选择器、子元素选择器、相邻兄弟选择器和属性选择器。

### 4.1.1 交集选择器（P94–P95）

**语法4-1 交集选择器语法**

| 定义语法 | 示例 |
|---|---|
| `标签选择器.类选择器\|#id 选择器{`<br>`属性1:属性值1;`<br>`属性2:属性值2;`<br>`}` | `div.nav{`<br>`background:#f00;`<br>`}` |

- 又称 **标签指定式选择器**。
- **构成规则**：由两个选择器拼接，第一个必须是**标签选择器**，第二个必须是**类选择器或 id 选择器**，两者**直接相连、中间不能有任何空格**。
- 语义：选中的 `<div>` 比一般 `<div>` 要求更精准，必须同时具备 `.nav` 类（或对应 id）。只有 `<div class="nav">` 会被选中。

**教材关键解释**
> 难怪它也叫标签指定式选择器，可以利用它指定具有特定类或 id 属性的标签。

**代码4-1 交集选择器（关键片段）**

```html
<style>
div{                        /* #007-#012 */
    width: 500px;
    height: 30px;
    background: antiquewhite;
    border: 2px solid darkgray;
}
div.blue{                   /* #013-#015 */
    background: aliceblue;
}
div#nav{                    /* #016-#018 */
    background: darkgoldenrod;
}
</style>

<body>
<div class="blue">交集选择器:div.blue</div>
<div id="nav">交集选择器:div#nav</div>
<div>标签选择器</div>
</body>
```

讲解：007–012 行标签选择器统一控制 3 个 div；`div.blue` 命中第 022 行；`div#nav` 命中第 023 行。效果见图4-1。

---

### 4.1.2 并集选择器（P95–P96）

**语法4-2 并集选择器语法**

| 定义语法 | 示例 |
|---|---|
| `选择器1,`<br>`选择器2,`<br>`选择器3,`<br>`…{`<br>`属性1:属性值1;`<br>`属性2:属性值2;`<br>`}` | `div,#main,.nav{`<br>`color:red;`<br>`}` |

- 又叫 **分组选择器 / 群组选择器**；由两个或两个以上**任意选择器**组成，用 **`,`** 分隔。
- 本质是样式代码的有效复用（"集体声明"），等价于：

```css
div{color:red;}
#main{ color:red;}
.nav{color:red}
```

**代码4-2 并集选择器（关键片段）**

```html
<style>
div,span,.nav{      /* #007-#009 */
    color:red;
}
</style>

<body>
<div>并集选择器div</div>
<span>并集选择器span</div>
<p class="nav">并集选择器p</div>
</body>
```

> **[教材疑误]** #015、#016 行原文闭合标签误写为 `</div>`，实际应为 `</span>`、`</p>`。上课请按正确写法示范。

---

### 4.1.3 后代选择器（P96–P98）

**语法4-3 后代选择器语法**

| 定义语法 | 示例 |
|---|---|
| `选择器1 选择器2 选择器3…{`<br>`属性1:属性值1;`<br>`属性2:属性值2;`<br>`}` | `ul a{`<br>`color:red;`<br>`}` |

- HTML 元素嵌套关系可视为父子关系，形成上下文关系，据此快速定位特定元素。
- **读法**：每个空格翻译成"xxxxx 作为 xxx 的后代"。`ul a` 读作"a 作为 ul 的后代"。

**教材关键解释 / 易错点**
1. 直接父子关系是一种**特殊的后代关系**（为子元素选择器铺垫）。
2. 书写起点无硬性要求：
   > 后代选择器相当于提供了一种特定上下文的限定，只要这个上下文关系足够覆盖你要运用规则的元素就可以了。通常，在自左向右书写时，左侧是父元素，随后可以是任何嵌套层次的后代元素。
3. **良好的编程习惯**：
   > 后代选择器在确保选中效果的前提下，以尽可能简单为原则，从而便于书写和阅读。
4. 本例 `ul a` 与 `ul li a` 选中效果等价，但复杂页面中容易误选/错选，应遵循**准确且精简**原则。

**代码4-3 后代选择器（关键片段）**

```html
<style>
ul,li{                  /* #007-#010 并集选择器做初始化 */
    margin:0px;
    padding:0px;
}
ul li{                  /* #011-#015 */
    height: 30px;
    background-color: lightgrey;
    margin-bottom:2px;
}
ul a{                   /* #016-#018 */
    color:red;
}
</style>

<body>
<ul>
    <li><a href="">link1</a></li>
    <li><a href="">link2</a></li>
    <li><a href="">link3</a></li>
    <li><a href="">link4</a></li>
    <li><a href="">link5</a></li>
</ul>
<a href="">link6</a>     <!-- #029 不在 ul 内，不被选中 -->
</body>
```

link1–link5 变红，link6 不变红。效果见图4-3。

---

### 4.1.4 子元素选择器（P98–P101）

**语法4-4 子元素选择器语法**

| 定义语法 | 示例 |
|---|---|
| `选择器1>选择器2{`<br>`属性1:属性值1;`<br>`属性2:属性值2;`<br>`}` | `h1>span{`<br>`color:red;`<br>`}` |

**教材关键解释（与后代选择器的最大区别）**
> 后代选择器是一种较为宽泛的上下文选择器，只要符合上下文关系，不管嵌套层级如何，都可以被选中；而子元素选择器是一种相对严格的上下文选择器，不仅要符合上下文关系，还要符合一定的父子关系。以上就是两者的最大区别。

**代码4-4 子元素选择器（关键片段）**

```html
<style>
ul li a{                /* #016-#018 后代：命中 ul li a 与 ul li span a */
    color:yellow;
}
/* ul li>a {             #019-#021 默认被注释
    color: red;
} */
</style>

<body>
<ul>                                        <!-- 第1组 -->
    <li><a href="">link1</a></li>
    <li><a href="">link2</a></li>
    <li><a href="">link3</a></li>
    <li><a href="">link4</a></li>
    <li><a href="">link5</a></li>
</ul>
<ul>                                        <!-- 第2组：多了一层 span -->
    <li><span><a href="">link6</a></span></li>
    <li><span><a href="">link7</a></span></li>
    <li><span><a href="">link8</a></span></li>
    <li><span><a href="">link9</a></span></li>
    <li><span><a href="">link10</a></span></li>
</ul>
</body>
```

**课堂演示流程**：
1. 初始运行 → 图4-4：**所有链接均为黄色**（`ul li a` 同时命中 `ul li a` 与 `ul li span a`）。
2. 取消 019–021 行注释、刷新 → 图4-5：**只有 link1–link5 变红色**（符合 `ul li>a` 直接父子关系）。

---

### 4.1.5 相邻兄弟选择器（P101–P102）

**语法4-5 相邻兄弟选择器语法**

| 定义语法 | 示例 |
|---|---|
| `选择器1+选择器2{`<br>`属性1:属性值1;`<br>`属性2:属性值2;`<br>`}` | `h1+p{`<br>`color:red;`<br>`}` |

**技巧（原文）**
> 相邻兄弟选择器是指由选择器1 选中的元素出发，其**后续相邻**的且符合选择器2 条件的那些元素。

**教材关键解释 / 易错点**
> 在相邻兄弟选择器中，并不是所有紧挨着的元素都是相邻的兄弟元素，确切地说是**后续相邻的兄弟元素**。（前序相邻的兄弟元素不起作用——初学者容易犯错之处。）

**代码4-5 相邻兄弟选择器（关键片段）**

```html
<style>
h1+p{                       /* #007-#012 */
    background: lemonchiffon;
    color:#f00;
    height: 30px;
    border:1px solid #ccc;
}
</style>

<body>
<h1>争创文明校园</h1>
<p>做文明人</p>
<p>办文明事</p>
<p>讲文明话</p>
</body>
```

**课堂拓展（考考你）**：
- `h1+p` → 只选中"做文明人"（图4-6）。
- 改为 `p+p` → 选中"办文明事"**和**"讲文明话"（对"办文明事"而言，后续相邻的"讲文明话"也符合条件）（图4-7）。

---

### 4.1.6 属性选择器（P103–P104）

**语法4-6 属性选择器语法**

| 定义语法 | 示例 |
|---|---|
| `[属性表达式1][属性表达式2]…{`<br>`属性1:属性值1;`<br>`属性2:属性值2;`<br>`}` | `[title]{`<br>`font-size:36px;`<br>`}` |
| `标签选择器[属性表达式1][属性表达式2]…{`<br>`属性1:属性值1;`<br>`属性2:属性值2;`<br>`}` | `a[href][title]{`<br>`font-size:36px;`<br>`}` |

> 属性选择器由**一对中括号**和一组属性表达式表示。

**表4-1 常见的属性选择器（完整还原）**

| 类型 | 选择器 | 描述 |
|---|---|---|
| 根据属性选择 | `[属性]` | 选择带有指定属性的元素 |
| 根据属性和属性值选择 | `[属性=值]` | 选择带有指定属性和属性值的元素 |
| 根据部分属性值选择 | `[属性～=值]` | 选择属性值中包含指定值的元素，注意该值必须是一个完整的单词 |
| 子串匹配属性值 | `[属性\|=值]` | 选择属性值以指定值开头的元素，注意该值必须是一个完整的单词或将"-"作为连接符连接后续内容的字符串，如"en-" |
| 子串匹配属性值 | `[属性^=值]` | 选择属性值以指定值开头的元素 |
| 子串匹配属性值 | `[属性$=值]` | 选择属性值以指定值结尾的元素 |
| 子串匹配属性值 | `[属性*=值]` | 选择属性值中包含指定值的元素 |

> **[排版说明]** 教材原表中前两行的运算符为全角"～="与"\|="，标准 CSS 写法为 `[attr~=value]`、`[attr|=value]`。

**代码4-6 属性选择器（综合示例，关键片段）**

```html
<style>
[title]{                    /* #007-#009 */
    color:#f6f;
}
a[href]{                    /* #010-#012 */
    text-decoration: none;
}
a[href][title]{             /* #013-#015 */
    font-size: 18px;
}
img[alt]{                   /* #016-#022 */
    border:1px dashed #ccc;
    float:left;
    max-width: 100px;
    padding:5px;
    margin-right:10px;
}
</style>

<body>
<h1 title="中国航天员">中国航天员</h1>
<dd>杨利伟</dd>
<dt>
    <img src="./images/astronaut.png" alt="宇航员">
    男，1965 年6 月出生，辽宁省绥中县人，共产党员。<a href="#" title="任务时间">2003
    年10 月15 日至16 日</a>执行神舟五号载人飞行任务，被授予<a href="#">"航天英雄"</a>称号。
</dt>
</body>
```

讲解要点：
- `[title]` 选中所有带 title 属性的元素 → `#f6f`。
- `a[href][title]` 只命中"2003 年10 月15 日至16 日"链接 → 18px。
- `img[alt]` 命中 astronaut.png，用 `float:left` 实现**图文混排**，`margin-right` 调整图文间距。
- 效果见图4-8。

---

## 三、4.2 应用样式的常用方式（P105–P109）

> 有 3 种方式可以将 CSS 应用到 HTML 中，分别是**行内式**（也称内联式，inline）、**内嵌式**（embeded）、**链接式**（external）。相应的样式表分别称为行内式样式表、内嵌式样式表和外部样式表。

### 4.2.1 行内式（P105）

```html
<标签名 style="属性1:属性值1;属性2:属性值2;…" …>
```
- 样式语句以 `style` **属性值**形式写在标签内部。
- **不需要选择器**，所有样式规则仅对该标签起作用。

**代码4-7 行内式（关键片段）**

```html
<h2>中国航天员</h2>
<p>杨利伟</p>
<p style="font:italic 18px ;color :#f6f">费俊龙</p>
<p>聂海胜</p>
```
只有"费俊龙"带定义样式，效果见图4-9。

---

### 4.2.2 内嵌式（P106–P107）

```html
<head>
…
<style type="text/css">
选择器{
    属性1:属性值1;
    属性2:属性值2;
    …
}
</style>
</head>
```
- 实现**同一个页面内**的样式代码复用；亦称**内部样式表**。

**常见编程错误（原文）**
> 在使用内嵌式时，没有将样式代码嵌入 `<style>` 标签、`<style>` 标签没有置于 `<head>` 标签内部，这些都是初学者在书写时常见的编程错误。

**技巧（原文）**
> 在 `<style>` 标签中，`type="text/css"` 用于定义文件的类型为样式文件。在 HTML5 中，该 type 属性可以省略，并简写为 `<style>…</style>`。

**代码4-8 内嵌式（关键片段）**

```html
<head>
<style>
.highlight{             /* #007-#010 */
    font:italic 18px ;
    color :#f6f;
}
</style>
</head>
<body>
<h2>中国航天员</h2>
<p class="highlight">杨利伟</p>
<p class="highlight">费俊龙</p>
<p class="highlight">聂海胜</p>
</body>
```
把"费俊龙"的样式抽象成 `.highlight` 类，三个段落共用。效果见图4-10。

---

### 4.2.3 链接式（P107–P109）

```html
<link rel="stylesheet" type="text/css" href="css 外部文件" />
```
- `rel="stylesheet"`：定义链接的 CSS 文件和 HTML 文档之间的关系。
- `href`：指定 CSS 文件（通常使用**相对路径**）。
- 目的：实现**多个页面**复用 CSS，保证页面风格统一。

**技巧（原文）**
> 省略 type 属性，由浏览器根据 rel 属性值猜测 type 属性值是一种常用的简化做法。（rel 为 stylesheet 时，浏览器推测 type 为 text/css。）

### 任务4-1 将内嵌式改为链接式

- **任务目标**：将 4.2.2 节中的内嵌式改为链接式。
- **核心步骤**：
  1. 新建名为 `css` 的目录，便于管理站点中的样式表文件。
  2. 创建样式表文件 `style.css`，置于 css 目录中（图4-11）。
  3. 将相关样式代码抽取定义到 `style.css` 中（图4-12）。
  4. 使用链接语法将样式表文件引入 HTML 文件。
  5. 运行并查看效果（与图4-10 一致）。
- **代码4-9 链接式**

```html
<head>
    <meta charset="utf-8">
    <title>链接式</title>
    <link rel="stylesheet" href="css/style.css">   <!-- #006 -->
</head>
<body>
    <h2>中国航天员</h2>
    <p class="highlight">杨利伟</p>
    <p class="highlight">费俊龙</p>
    <p class="highlight">聂海胜</p>
</body>
```
- 006 行用 `<link>` 取代原 `<style>`；当前文件 `4-2-3.html` 到 `style.css` 的相对路径为 `css/style.css`（图4-13）。

**良好的编程习惯（原文）**
> 在开发整站的项目中，优先使用外部样式表可以提高 CSS 代码的复用率，提升样式表的可维护性。

---

## 四、4.3 解决 CSS 冲突的问题（P109–P114）

> CSS 根据 ①优先级原则；②就近原则；③覆盖原则；④!important 原则解决 CSS 冲突的问题。

**冲突示例代码 4-10（关键片段）**

```html
<style>
p{color:red;}               /* #007 */
.highlight{color:yellow;}   /* #008 */
#p1{color: blue;}           /* #009 */
p#p1{color:green;}          /* #010 */
</style>

<body>
<h2>中国航天员</h2>
<p id="p1" class="highlight">杨利伟</p>
<p class="highlight">费俊龙</p>
<p class="highlight">聂海胜</p>
</body>
```

### 1. 优先级原则

- 冲突时以**优先级高**的样式作为最终显示效果。
- 样式类型权重：**行内式（A）> 内嵌式/链接式**。
- 选择器优先级：**id 选择器（B）> 类选择器/伪类选择器/属性选择器（C）> 标签选择器/伪元素选择器（D）> 通用选择器/子元素选择器/相邻兄弟选择器**。
- A、B、C、D 四个等级如同十进制的**千位、百位、十位、个位**。

**表4-2 优先级权重表（完整还原）**

| 选择器 | A（style） | B（id 的数目） | C（class 的数目） | D（标签的数目） | 优先级（组合值） |
|---|---|---|---|---|---|
| `*` | 0 | 0 | 0 | 0 | 0 |
| `p` | 0 | 0 | 0 | 1 | 1 |
| `p a` | 0 | 0 | 0 | 2 | 2 |
| `p a.color` | 0 | 0 | 1 | 2 | 12 |
| `p .color .text` | 0 | 0 | 2 | 1 | 21 |
| `p .color div #news` | 0 | 1 | 1 | 2 | 112 |
| `style=""` | 1 | 0 | 0 | 0 | 1000 |

**表4-3 利用优先级解决冲突（完整还原，对应代码4-10 的"杨利伟"段落）**

| 选择器 | A（style） | B（id 的数目） | C（class 的数目） | D（标签的数目） | 优先级（组合值） |
|---|---|---|---|---|---|
| `p` | 0 | 0 | 0 | 1 | 1 |
| `.highlight` | 0 | 0 | 1 | 0 | 10 |
| `#p1` | 0 | 1 | 0 | 0 | 100 |
| `p#p1` | 0 | 1 | 0 | 1 | 101 |

结论：`p#p1` 优先级最高（101），浏览器最终显示**绿色**字体（图4-14）；即使调整样式定义先后顺序，结果始终不变。

**教材对话中的关键知识点**
- 通用选择器的 id、class 及标签数目均为 0，优先级为 0。
- `p a` 含两个标签 → 2。
- `p a.color`：含一个后代选择器 + 一个 `a.color` 交集选择器，class 数 1、标签数 2 → 12。
- `p .color div #news`：1 个 id、1 个类、2 个标签 → 112。
- 行内 style 权重直接为 1000。

---

### 2. 就近原则（P111–P112）

> 就近原则主要是针对**继承关系**的，越靠近要格式化的元素，优先级越高。

**代码4-11 就近原则（关键片段）**

```html
<style>
a{color:blue;}      /* #007 */
ul{color:green;}    /* #008 */
li{color:yellow;}   /* #009 */
</style>

<body>
<h2>中国航天员</h2>
<ul>
    <li><a href="#">杨利伟</a></li>
    <li><a href="#">费俊龙</a></li>
    <li><a href="#">聂海胜</a></li>
</ul>
</body>
```

ul、li、a 优先级**相同**，此时用就近原则：a 距离显示内容最近，覆盖父元素 li 的 color → 最终显示**蓝色**（图4-15）。

---

### 3. 覆盖原则（P112–P113）

> 如果样式的优先级相同，继承层级也相同，那么**后面定义的样式会覆盖前面定义的样式**。

**代码4-12 覆盖原则（关键片段）**——在代码4-11 基础上新增第 010 行：

```css
a{color:blue;}      /* #007 */
ul{color:green;}    /* #008 */
li{color:yellow;}   /* #009 */
a{color: red;}      /* #010 新增 */
```

007 行与 010 行优先级相同 → 后者覆盖前者 → 最终显示**红色**（图4-16）。

---

### 4. !important 原则（P113–P114）

**语法4-7 `!important` 语法**

| 定义语法 | 示例 |
|---|---|
| `样式规则 !important;` | `a{color:blue !important;}` |

- 添加 `!important` 后优先级被设为**最高级**（**高过行内式**）。

**代码4-13 !important 原则（关键片段）**

```css
a{color:blue !important;}   /* #007 */
ul{color:green;}            /* #008 */
li{color:yellow;}           /* #009 */
a{color: red;}              /* #010 */
```

```html
<ul>
    <li><a href="#" style="color:yellow;">杨利伟</a></li>   <!-- #016 行内式 -->
    <li><a href="#">费俊龙</a></li>
    <li><a href="#">聂海胜</a></li>
</ul>
```

即使第 016 行有行内 `style="color:yellow;"`，最终仍显示**蓝色**（图4-17）。

---

## 五、4.4 使用 Emmet 语法（P115–P118）

- Emmet 前身叫 **Zen Coding**，是提高 HTML/CSS 编写速度的便利工具。
- 主流工具均已支持：Dreamweaver、VSCode、Atom、Sublime、Eclipse、IDEA 等。
- 使用**类似于 CSS 选择器的语法**描述 HTML 文档树结构及属性：`>` 父子、`+` 兄弟、`^` 父级。

### 4.4.1 Emmet 基础语法（P115–P116）

**语法4-8 Emmet 的基本使用语法（完整还原）**

| 定义语法 | 示例 |
|---|---|
| id 属性 id：`#` | 示例1：`#header`<br>`<div id="header"></div>`<br>示例2：`form#search.wide`<br>`<form id="search" class="wide"></form>` |
| 类属性 class：`.` | 示例1：`.title`<br>`<div class="title"></div>`<br>示例2：`p.class1.class2.class3`<br>`<p class="class1 class2 class3"></p>` |
| 属性值 attribute：`[]` | 示例1：`p[title="Hello world"]`<br>`<p title="Hello world"></p>`<br>示例2：`td[rowspan=2 colspan=3 title]`<br>`<td rowspan="2" colspan="3" title=""></td>` |
| 文本 text：`{}` | `a{click me}`<br>`<a href="">click me</a>` |
| 子元素 child：`>` | `nav>ul>li`<br>`<nav><ul><li></li></ul></nav>` |
| 兄弟元素 sibling：`+` | `div+p+bq`<br>`<div></div><p></p><blockquote></blockquote>` |
| 父级 Climb-up：`^` | `div+div>p>span+em^bq`<br>`<div></div>`<br>`<div>`<br>`  <p><span></span><em></em></p>`<br>`  <blockquote></blockquote>`<br>`</div>` |

> 课堂提示：不写标签名时默认生成 `<div>`；多个 `.class` 连写生成多个类；属性省略值时生成空串 `""`。

### 4.4.2 多重性和项目编号（P116–P117）

**语法4-9 Emmet 多重性和项目编号语法（完整还原）**

| 定义语法 | 示例 |
|---|---|
| 多重性 multiplication：`*` | `ul>li*5` → `<ul>` 内 5 个 `<li></li>` |
| 项目编号 item numbering：`$` | 示例1：`ul>li.item$*5` → `<li class="item1">…<li class="item5">`<br>示例2：`h$[title=item$]{Header $}*3` → `<h1 title="item1">Header 1</h1>`、`<h2 title="item2">Header 2</h2>`、`<h3 title="item3">Header 3</h3>`<br>示例3：`ul>li.item$$$*5` → `<li class="item001">…<li class="item005">` |

**教材关键说明**
- `$` 可用在 **HTML 标签名、属性值、元素内容**中（见示例2）。
- 多个 `$` 表示数值占位：`$$` 两位，`$$$` 三位。
- 可用 `@` 指定开始序号，`-` 表示倒序（见任务4-2）。

### 任务4-2 Emmet 语法练习1：多重性和项目编号

- **任务目标**：输入 Emmet 语法，按 **"Tab"** 键执行并观察效果。

练习①（倒序）：
```
输入：ul>li.item$@-*5
输出：
<ul>
    <li class="item5"></li>
    <li class="item4"></li>
    <li class="item3"></li>
    <li class="item2"></li>
    <li class="item1"></li>
</ul>
```

练习②（指定起始序号）：
```
输入：ul>li.item$@3*5
输出：
<ul>
    <li class="item3"></li>
    <li class="item4"></li>
    <li class="item5"></li>
    <li class="item6"></li>
    <li class="item7"></li>
</ul>
```

### 4.4.3 分组（P117–P118）

**语法4-10 Emmet 分组语法（完整还原）**

| 定义语法 | 示例 |
|---|---|
| 分组 grouping：`()` | `div>(header>ul>li*2>a)+footer>p`<br>`<div>`<br>`  <header>`<br>`    <ul>`<br>`      <li><a href=""></a></li>`<br>`      <li><a href=""></a></li>`<br>`    </ul>`<br>`  </header>`<br>`  <footer>`<br>`    <p></p>`<br>`  </footer>`<br>`</div>` |

### 任务4-3 Emmet 语法练习2：分组

- **任务目标**：输入 Emmet 语法，按 "Tab" 键执行并观察效果。
- **输入命令**：`(div>dl>(dt+dd)*3)+footer>p`
- **[教材疑误]** 教材随后给出的"执行效果"代码块仍是 `div>header>ul>li*2>a+footer>p` 的结构（`<header><ul><li><a>`），与输入命令明显不符。备课演示时请**以输入命令为准**：正确输出应为 `<div>` 内含 3 组 `<dt><dd>`，再并列 `<footer><p></p></footer>`。

**补充快捷语法**
- `html:5` 或 `!` → 快速创建 HTML5 文档框架
- `link` → 快速创建外部样式链接
- CSS 缩写 → 快速生成 CSS 样式代码
- 更多内容可查看 Emmet 官网

---

## 六、4.5 使用 LESS、SASS 和 SCSS（P118–P120）

- CSS 可通过**预处理技术**编译生成样式规则。
- 作为一种**样式表高级语言**，允许使用**变量、嵌套规则、混合（mixins）、函数**等高阶语法，并可通过命令或图形化工具编译为 CSS 文件。
- 适用场景：**需要组织大量样式表文件的项目** 或 **需要分享设计的多项目合作**。
- 常见 3 种预编译技术：**LESS、SASS 和 SCSS**。
- 类比：CSS 像机器语言，LESS/SASS/SCSS 像高级语言；CSS 预处理器通常分为 **LESS 和 SASS 两大类**。

**SASS 的两种语法实现**

| 名称 | 特点 | 文件扩展名 |
|---|---|---|
| **Sass**（syntactically awesome stylesheets） | 采用**类似 Python 的缩排语法** | `.sass` |
| **SCSS**（Sassy CSS） | Sass 发展到 **Sass3** 时大量改良形成的独立版本，兼容原语法，并采用**类似 CSS 的 `{}` 缩进** | `.scss` |

**教材关键解释**
- **SASS** 利用缩进快速编写具有上下文层次的样式代码。
- **SCSS** 使用 `{}` 表示缩进层次，并要求每个样式定义语句以**分号**结尾，整体风格类似 CSS 规则。
- 变量定义符号：**LESS 使用 `@` 定义变量；SCSS 使用 `$` 定义变量**。
- 第 3 行代码两者都通过引用变量，并使用 `*` 进行**数学运算**。
- 除数学运算、函数引用外，还可以进行**样式的分解和组合**。

**图示素材**

| 图号 | 内容 |
|---|---|
| 图4-18 | Sass 与 CSS 的代码对应关系 |
| 图4-19 | SCSS 与 CSS 的代码对应关系 |
| 图4-20 | LESS 与 CSS 的代码对应关系 |
| 图4-21 | SCSS 与 CSS 的代码对应关系（LESS 用 `@`、SCSS 用 `$` 定义变量） |

---

## 七、4.6 小结（P120）

> 本项目介绍了 CSS 选择器中的高级部分——复合选择器，并介绍了它的两种延伸用法，即 Emmet 语法，以及 LESS、SASS 和 SCSS。本项目中的相关知识在 Web 前端实战中具有非常重要的地位，需要我们熟练地掌握，为后续项目的学习奠定扎实的基础。

---

## 八、4.7 作业（P120–P121）

### 一、选择题
1. 在默认情况下，Emmet 语法中 `.container` 生成的 HTML 是（    ）。
   A．p.container　B．p#container　C．div.container　D．div#container
2. 要想生成如下代码，应使用的 Emmet 语法是（    ）。（目标结构：`<div class="container"><ul>` 内含 3 个 `<li><a href="">linkN</a></li>`）
   A．`div.container>ul*3>li a{link}`　B．`div.container>ul>li*3{a.link$}`
   C．`div.container>ul>li*3>a{link$}`　D．`div.container>ul>li*3>a*3{link$}`
3. （    ）不是 HTML 引入样式的方式。A．行内式　B．内嵌式　C．链接式　D．导入式
4. 关于 Emmet 语法 `<p>lorem*10</p>`，描述不正确的是（    ）。
   A．lorem 用于快速生成占位文字　B．lorem*10 可以生成 10 个字符
   C．lorem*10 可以生成 10 个单词　D．lorem*10 可以生成 10 个段落
5. 要想生成如下代码，应使用的 Emmet 语法是（    ）。（目标结构：`div.container` 内两组 `p>span>a` 后再跟一个 `p`）
   A．`.container>(p>span>a^p)*2`　B．`div.container>(p>span>a^p)*2`
   C．`div.container>p>span>a^p>span>a`　D．`div.container>p>span>a+p>span>a`

### 二、简述题
1. Emmet 语法 `ul li*3>a[href="#"]{link$$}` 的 HTML 结构是什么？
2. 请使用 Emmet 语法生成如下全部的 HTML 代码：`<h2> </h2>` + `<ul>` 内含 3 个 `<li><a href="#"> </a></li>` + `</ul>`

### 三、项目讨论
> 近几年来，随着我国在航天领域的快速发展，我国航天员一批批地实现了飞天。你能列举这些成功完成航天任务的航天员吗？航天精神对你的学习、生活、工作有哪些启发？

---

# 项目5 盒子模型

## 一、项目扉页信息（P122）

### 思政课堂（原文要点）
> 在数字化生活场景中，网页制作的影响十分深远。作为信息传递的重要载体，网页让各类资讯、服务触手可及，满足了人们多元化的需求。它不仅提供了丰富的视听效果，还通过个性化设计提升了用户体验。此外，网页制作推动了传统媒体的数字化转型，催生了新的商业模式，为现代生活带来了极大的便利。**支付宝、Keep、京东、淘宝**等各式应用影响着人们生活的方方面面，丰富了人们的数字化生活，为人们带来了诸多便利。

### 学习目标（照抄要点）
- 了解盒子模型的组成
- 掌握边框的常用样式定义语法
- 掌握边框风格的应用方法
- 理解和掌握内边距特性
- 理解和掌握外边距特性

### 技能目标（照抄要点）
- 能正确使用盒子模型
- 能使用边框及其相关样式属性
- 能使用内边距及其相关样式属性
- 能使用外边距及其相关样式属性

### 素养目标（照抄要点）
- 培养高尚的审美情操
- 培养严谨求实的学习态度
- 培养勇于探索、崇尚科学的劳动意识

---

## 二、5.1 盒子模型简介（P122–P129）

> CSS 假定所有 HTML 文档元素都生成了一个描述该元素在 HTML 文档布局中所占空间的矩形元素框。人们形象地将其看作一个盒子，也称其为"框"。CSS 围绕这些盒子产生了"盒子模型"（box model）概念，有些书上也称"框模型"。

### 5.1.1 盒子模型的组成（P123）

- 一个网页由许多大大小小的盒子通过不同排列方式组合而成。
- 每个盒子从内到外：**元素内容（content）→ 内边距（padding）→ 边框（border）→ 外边距（margin）**。
- 每层都形成一个矩形盒子，可形象区分为 **content 盒、padding 盒、border 盒、margin 盒**。
- body、html、div、p 等都是矩形盒子。
- **方向命名规律**：padding、border、margin 都有上右下左 4 个方向，统一用 `xxx-top`、`xxx-right`、`xxx-bottom`、`xxx-left` 表示。

**常见编程错误（原文）**
> 在默认情况下，width 和 height 是用于描述 **content 盒**的尺寸的。错误地将 width 和 height 作为整个盒子模型的宽度和高度是常见的编程错误。

**图示素材**：图5-1 盒子模型的组成示意图。

### 任务5-1 使用开发者工具查看盒子模型（P124–P125）

- **任务目标**：输入代码5-1，按步骤使用 Google Chrome 浏览器查看盒子模型。
- **核心步骤**：打开 Google Chrome 运行 HTML 文件，在浏览器窗口中**右击**，选择**"检查"**命令（图5-2），打开开发者工具（图5-3）；观察"元素"选项卡（②区）、"样式"选项卡（③区）和**盒子模型**（④区）。
- **代码5-1 盒子模型**

```html
<style>
.box{                       /* #007-#014 */
    width: 100px;
    height: 50px;
    background-color: darkkhaki;
    padding:5px;
    margin:10px 20px;
    border:3px solid #ccc;
}
</style>

<body>
<div class="box">
    盒子模型
</div>
</body>
```

- **技巧（原文）**
  > 按快捷键"Ctrl+Shift+I"（Windows）或快捷键"Opt+Cmd+I"（macOS）打开 Google Chrome 浏览器的开发者工具。
- **观察结论（引出值复制原则）**
  - width:100px、height:50px 对应的是 **content 盒**的宽高。
  - `padding:5px` → 上、右、下、左 4 个方向均为 5px。
  - `margin:10px 20px` → 上、下外边距 10px，左、右外边距 20px（4 个方向都有值）。

---

### 5.1.2 值复制原则（P126–P127）

**表5-1 内边距属性（完整还原）**

| 属性名 | 描述 |
|---|---|
| padding | 综合样式属性，同时设置4 个方向的内边距 |
| padding-top | 设置上内边距 |
| padding-right | 设置右内边距 |
| padding-bottom | 设置下内边距 |
| padding-left | 设置左内边距 |

**语法5-1 内边距语法**

| 定义语法 | 示例 |
|---|---|
| `padding:padding_value [padding_value] [padding_value] [padding_value]` | `padding:5px 10px 15px;` |
| `padding-方向:padding_value` | `padding-left:10px;` |

**表5-2 内边距参数取值（完整还原）**

| 参数值 | 描述 |
|---|---|
| auto | 浏览器计算内边距 |
| length | 以 px、em、cm 等为单位的某个具体正值作为内边距，默认为 0 |
| % | 基于父元素的宽度计算内边距 |
| inherit | 继承父元素的内边距 |

**语法5-2 值复制语法（完整还原）**

| 定义值 | 示例 | 含义 |
|---|---|---|
| 定义1 个值 | `padding:5px;` | 4 个方向的内边距都是 5px |
| 定义2 个值 | `padding:5px 10px;` | 上、下内边距均为 5px，左、右内边距均为 10px |
| 定义3 个值 | `padding:5px 10px 6px;` | 上内边距为 5px，左、右内边距均为 10px，下内边距为 6px |
| 定义4 个值 | `padding:5px 10px 6px 7px;` | 上、右、下、左内边距分别为 5px、10px、6px、7px |

> 值复制原则在 margin、padding 等很多基于盒子模型的样式属性设置中都有广泛的应用，请大家务必牢记它的使用原则和对应的具体含义。

简化示例：4 条 `padding-方向:5px;` 可直接简写成 `padding:5px;`。

---

### 5.1.3 内边距特性（P127–P129）

> 盒子的内边距定义了边框和元素内容之间的空白区域。在默认情况下，绝大部分盒子的 padding 都是 0px。但也存在一些标签自带一定的内边距，如 **`<ul>`、`<ol>`**。

#### 特性1：padding 影响元素尺寸
默认情况下 width 指 content 盒宽度，**增加 padding 会影响整个元素的尺寸**。

#### 任务5-2 设置支付宝小程序中的 padding（P127–P129）

- **任务背景素材**：图5-4 为**宁波城市职业技术学院支付宝小程序**的功能项，有 **"学生优惠指南""学生特价机票""校园兼职指南""更多服务"** 4 个主要功能项。每个功能项由**图标 + 文字**组成，装载在一个容器盒中。
- **任务目标**：请利用盒子模型，制作如图5-4 所示的功能项。
- **素材文件**：`images/nbcc-icon1.png`、`images/nbcc-icon2.png`
- **代码5-2 "学生优惠指南""学生特价机票"的功能模块（关键片段）**

```html
<style>
.box {                      /* #007-#019 */
    width: 150px;
    display: flex;
    justify-content:center;
    align-items:center;
    line-height: 30px;
    background-color: #F6F9FC;
    padding:5px 10px;
    margin-bottom:10px;
    border-radius: 5px;
    color:#666;
    overflow: hidden;
}
.box img{                   /* #020-#023 */
    width: 20px;
    margin-right: 5px;
}
</style>

<body>
<div class="box">
    <img src="images/nbcc-icon1.png"/>学生优惠指南
</div>
<div class="box">
    <img src="images/nbcc-icon2.png"/>学生特价机票
</div>
</body>
```

- **讲解要点**：008 行盒子宽度 150px；014 行 `padding:5px 10px`（上下 5px、左右 10px）→ 用户看到的矩形宽度为 **150+10+10=170px**（图5-6）。运行效果见图5-5。

#### 特性2：padding 可以显示背景
> 背景颜色不仅对 content 盒有效，还对 padding 盒有效，即**背景效果可以延伸到 padding 区域**。当给盒子添加 padding 时，padding 会撑开盒子，而且背景效果也会延伸到 padding 区域。

（本例中 `#F6F9FC` 背景色覆盖了 padding 撑开的区域，见图5-5。）

---

## 三、5.2 边框（P129–P139）

> 盒子的边框包裹了内边距和内容，形成了盒子的边界。边框主要包含**风格（style）、宽度（width）和颜色（color）** 3 个主要元素。在默认情况下，由于边框会占据空间，因此在排版、制作和计算时要充分考虑边框带来的影响。

### 5.2.1 边框风格（P129–P133）

**表5-3 边框风格样式的相关属性（完整还原）**

| 属性名 | 描述 |
|---|---|
| border-style | 综合样式属性，同时设置4 个方向的边框风格，符合值复制原则 |
| border-top-style | 设置上边框的风格 |
| border-right-style | 设置右边框的风格 |
| border-bottom-style | 设置下边框的风格 |
| border-left-style | 设置左边框的风格 |

**技巧（原文）**
> 某个特定方向的边框风格按照 `border-方向-style` 的格式进行设置。

**课堂提问（教材）**：`border-style:dashed solid` 是什么意思？
> 根据值复制原则，它表示**上、下边框均为虚线，左、右边框均为实线**。

**表5-4 边框的风格值及其应用效果（完整还原）**

| 风格值 | 描述 | 应用效果 |
|---|---|---|
| none | 无边框，默认值 | 无 |
| dashed | 虚线 | （图示） |
| solid | 实线 | （图示） |
| dotted | 点状 | （图示） |
| double | 双实线 | （图示） |
| groove | 凹槽 | （图示） |
| ridge | 脊状 | （图示） |
| inset | 边框内嵌一个立体边框 | （图示） |
| outset | 边框外嵌一个立体边框 | （图示） |
| inherit | 继承父元素的边框风格 | 无 |

#### 任务5-3 编写并查看边框风格（P131–P133）

- **任务目标**：设计一个页面，使用边框风格样式的相关属性及其属性值，并查看不同值在页面中的实际呈现效果。
- **代码5-3 边框风格（关键片段）**

```html
<style>
.box{                       /* #007-#014 公共样式 */
    width: 100px;
    height: 50px;
    padding:5px;
    margin:10px 20px;
    border:3px solid #ccc;
    float:left;             /* #013 浮动并排，便于比较 */
}
.box1{border-style: dashed;}    /* #015-#017 */
.box2{border-style: dotted;}    /* #018-#020 */
.box3{border-style: double;}    /* #021-#023 */
.box4{border-style: groove;}    /* #024-#026 */
.box5{border-style: ridge;}     /* #027-#029 */
.box6{border-style: inset;}     /* #030-#032 */
.box7{border-style: outset;}    /* #033-#035 */
</style>

<body>
<div class="box">实线</div>
<div class="box box1">虚线</div>
<div class="box box2">点状</div>
<div class="box box3">双实线</div>
<div class="box box4">凹槽</div>
<div class="box box5">脊状</div>
<div class="box box6">内嵌</div>
<div class="box box7">外嵌</div>
</body>
```

通过 `.box` 与 `.box1～.box7` 定义 **8 种**风格边框，用 `float` 浮动并排一行对比。运行效果见图5-7。

---

### 5.2.2 边框宽度（P133）

**表5-5 边框宽度样式的相关属性（完整还原）**

| 属性名 | 描述 |
|---|---|
| border-width | 综合样式属性，同时设置4 个方向的边框宽度，符合值复制原则 |
| border-top-width | 设置上边框的宽度 |
| border-right-width | 设置右边框的宽度 |
| border-bottom-width | 设置下边框的宽度 |
| border-left-width | 设置左边框的宽度 |

**表5-6 边框的宽度值（完整还原）**

| 宽度值 | 描述 |
|---|---|
| length | 具体数值，单位可以是 px 或 em |
| thin | 预设值，表示细边框 |
| medium | 预设值，表示中等边框（默认值） |
| thick | 预设值，表示粗边框 |
| inherit | 继承父元素的边框宽度 |

**易错点**
> 预设值的具体取值由浏览器厂商决定，不同浏览器厂商的取值可能不一样。例如，有些浏览器厂商将 thin、medium、thick 分别对应为 **2px、3px、5px**；而有些浏览器厂商却将它们分别对应 **1px、2px、3px**。

---

### 5.2.3 边框颜色（P133–P134）

**表5-7 边框颜色样式的相关属性（完整还原）**

| 属性名 | 描述 |
|---|---|
| border-color | 综合样式属性，同时设置4 个方向的边框颜色，符合值复制原则 |
| border-top-color | 设置上边框的颜色 |
| border-right-color | 设置右边框的颜色 |
| border-bottom-color | 设置下边框的颜色 |
| border-left-color | 设置左边框的颜色 |

> 关于颜色值，可以使用表示颜色的**英文预设单词**、对应颜色的**十六进制值**或颜色的 **RGB 值**。

---

### 5.2.4 边框综合样式（P134–P139）

定义 1px、红色的实线边框，分开写需 3 条语句：
```css
border-style:solid;
border-width:1px;
border-color:red;
```
可用**边框综合样式属性**简化。

**表5-8 边框综合样式属性（完整还原）**

| 属性名 | 描述 |
|---|---|
| border | 综合样式属性，同时设置4 个方向的边框风格、宽度、颜色 |
| border-top | 同时设置上边框的风格、宽度、颜色 |
| border-right | 同时设置右边框的风格、宽度、颜色 |
| border-bottom | 同时设置下边框的风格、宽度、颜色 |
| border-left | 同时设置左边框的风格、宽度、颜色 |

#### 任务5-4 边框的神秘之旅（P134–P139）

- **任务目标**：使用盒子模型的边框样式制作类似于**微信聊天的气泡对话框**效果。
- **应用场景素材**：图5-8 标签页、图5-9 菜单提示、图5-10 气泡对话框。
- **课堂导语**："很难想象这些指示三角形跟咱们今天学习的边框有什么关系。下面我们一起来变一个魔术。"

**步骤1：加粗边框 —— 代码5-4**

```html
<style>
div{                        /* #007-#011 */
    width: 100px;
    height: 20px;
    border:48px solid blue;
}
</style>
<body>
<div></div>
</body>
```
→ 图5-11，"好像还看不出任何三角形的痕迹。"

**步骤2：缩小宽度 —— 代码5-5**

```css
div{
    width: 0px;
    height: 0px;
    border:48px solid;
    border-color: red yellow green blue;
}
```
→ 图5-12
> 哇哦，原来三角形藏在这里，当盒子没有大小，即 width、height 都为 0px 时，边框就构成了三角形形态。

**步骤3：添加透明颜色 —— 代码5-6**

```css
div{
    width: 0px;
    height: 0px;
    border:48px solid;
    border-color: transparent transparent transparent blue;   /* 保留指向右侧的蓝色三角形 */
}
```
→ 图5-13
- `transparent` 是 color 的重要预设值，表示**透明**。
- **向上箭头**：`border-color:transparent transparent blue transparent;`

**步骤4：气泡对话框结构 —— 代码5-7**

```html
<div class="bubble">
    <div class="arrow"></div>
    <div class="msg">Hi,您好</div>
</div>
```
- 结构说明见图5-14（矩形正文框 + 三角箭头）。
- 要实现垂直居中对齐需用到后续 CSS 元素与定位知识：用 `top`、`left`、`right`、`bottom` 描述元素相对于父容器的位置关系（图5-15）。

**关键公式**
```
top = (height - 2*border-width) / 2
// border-width 是一个 CSS 属性值，表示边框宽度

化简：top = height/2 - border-width
```

**步骤5：代码5-8 气泡对话框（完整核心代码）**

```html
<style>
.arrow{                     /* #007-#015 */
    width: 0px;
    height: 0px;
    border:12px solid;
    border-color: transparent transparent transparent blue;
    position: absolute;
    left: 100%;
    top:13px;
}
.bubble{                    /* #016-#022 */
    width: 100px;
    height: 50px;
    background-color: blue;
    position: relative;
    border-radius: 5px;
}
.msg{                       /* #023-#026 */
    color:white;
    padding:10px 5px;
}
</style>

<body>
<div class="bubble">
    <div class="arrow"></div>
    <div class="msg">Hi,您好</div>
</div>
</body>
```

- `top:13px` 由 `height/2 - border-width` 得出：**50/2 − 12 = 13px**。运行效果见图5-16。
- **技巧（原文）**
  > 这里先给出完整代码和简单介绍，大家可以先模仿本例。在学完后续相关项目内容后，可以再回顾本例，会有更深刻的认识。
- 拓展：还可尝试使用 `:after` 伪类实现同样效果。

---

## 四、5.3 外边距（P139–P145）

> 与 padding 不同，margin 用于控制盒子与其他盒子之间的距离。也就是说，margin 用于定义盒子自身边框与其他盒子之间的空白区域，该空白区域被称为外边距。这里的"空白区域"有些书也称其为"透明区域"，因为**在外边距中无法显示背景**。

### 5.3.1 设置外边距（P139–P140）

**表5-9 外边距属性（完整还原；教材表头为"属性值"，实为属性名）**

| 属性名 | 描述 |
|---|---|
| margin | 综合样式属性，同时设置4 个方向的外边距 |
| margin-top | 设置上外边距 |
| margin-right | 设置右外边距 |
| margin-bottom | 设置下外边距 |
| margin-left | 设置左外边距 |

**表5-10 外边距属性的4 个值（完整还原）**

| 属性值 | 描述 |
|---|---|
| auto | 浏览器计算外边距 |
| length | 以 px、em、cm 等为单位的数值作为外边距，**可以取正值、负值** |
| % | 基于父元素的宽度来计算外边距 |
| inherit | 继承父元素的外边距 |

**易错点**
> **padding 不可以取负值，而 margin 可以取负值。**

---

### 5.3.2 外边距特性（P140–P145）

> 当两个或更多个相邻的块级元素相遇时，垂直外边距会将垂直方向上的两个外边距合并起来，形成同一个外边距。如果合并的外边距全部为正值，则合并后的外边距等于发生合并的外边距中的**较大者**；如果发生合并的外边距不全为正值，则会拉近两个块级元素的垂直距离，甚至会发生元素重叠的现象。

垂直外边距合并主要体现在两种情况：**相邻元素外边距合并**、**父子元素外边距合并**。

#### 1. 相邻元素外边距合并（P140–P142）
- 上面元素的**下外边距**和下面元素的**上外边距**合并，称为 **"margin 合并"**。
- 示例：下边距 10px、上边距 5px → 合并后取较大值（图5-17）。

**常见编程错误（原文）——margin 合并的前提要素**
> ①相邻元素为**块级元素**，不包括浮动和绝对定位元素；②只发生在和当前**标准流方向相垂直**的方向上，默认的标准流为水平方向，那么 margin 合并就在垂直方向上。

**任务5-5 相邻元素外边距合并（P141–P142）**

- **任务目标**：构造一个相邻元素外边距合并的实例，指定相邻元素的外边距，并查看外边距合并的效果。
- **代码5-9 相邻元素外边距合并（关键片段）**

```html
<style>
.box{                       /* #007-#012 公共样式 */
    width: 300px;
    height: 30px;
    text-align: center;
    border:1px solid #ccc;
}
section{                    /* #013-#016 */
    float:left;
    margin-right:50px;
}
.box1{margin-bottom:10px;}      /* #017 */
.box2{margin-top:5px;}          /* #018 */
.box3{margin-bottom: -10px;}    /* #019 */
.box4{margin-top:5px; }         /* #020 */
.box5{margin-bottom: -10px;}    /* #021 */
.box6{margin-top:-5px; }        /* #022 */
</style>

<body>
<section>
    <div class="box1 box">div1(margin-bottom:10px)</div>
    <div class="box2 box">div2(margin-top:5px)</div>
</section>
<section>
    <div class="box3 box">div1(margin-bottom:-10px)</div>
    <div class="box4 box">div2(margin-top:10px)</div>
</section>
<section>
    <div class="box5 box">div1(margin-bottom:-10px)</div>
    <div class="box6 box">div2(margin-top:-5px)</div>
</section>
</body>
```

> **[教材疑误]** CSS 中 `.box4` 写作 `margin-top:5px`，但 HTML 文本标签写作 `div2(margin-top:10px)`；后文讨论又按 `margin-top:10px` 计算（−10 + 10 = 0）。讲课时建议统一按 **10px**（"正负相加恰为 0 才出现无缝相接"的结论才成立），并指出教材前后不一致。

**margin 合并的计算规则（技巧，原文）**
> margin 合并的计算规则："**正正取大值**""**正负相加值**""**负负最负值**"。如果两个外边距中存在负值，则合并后的高度等于发生合并的外边距的和。当和为负值时，相邻元素在垂直方向上发生重叠；当和为 0 时，相邻元素无缝相接。

- 演示：上 `margin-bottom:-10px` + 下 `margin-top:10px` → 和为 0 → **两元素垂直方向无缝相接**（图5-19）。运行效果见图5-18。

#### 2. 父子元素外边距合并（P142–P145）

**原理**（图5-20）
> 父元素指定 `margin-top` 为 10px，子元素指定 `margin-top` 为 20px。此时，浏览器并没有生成 10+20=30px 的外边距，而会发生父子元素上外边距的合并。根据前面 margin 合并的计算规则，合并后的上外边距为 20px。因此，用户实际在浏览器中看到的是 20px。

**任务5-6 父子元素外边距合并（P143–P144）**

- **任务目标**：构造一个父子元素外边距合并的实例，并观察外边距合并的效果。
- **代码5-10 父子元素外边距合并（关键片段）**

```html
<style>
.box{                       /* #007-#009 */
    height: 100px;
}
.father{                    /* #010-#012 */
    margin-top: 20px;
}
.son{                       /* #013-#016 */
    margin-top: 20px;
    border:2px solid #333;
}
.outer{                     /* #017-#019 */
    border:2px dashed #666;
}
</style>

<body>
<div class="outer">
    <div class="father ">
        <div class="son box"></div>
    </div>
</div>
</body>
```

→ 图5-21，父子元素外边距合并为 **20px**。若父子元素有 `margin-bottom`，同样会合并。

**教材问答中的关键知识点**
- 对于**有多个子元素**的情况：**第一个子元素的 margin-top** 和**最后一个子元素的 margin-bottom** 会分别与父元素的 margin-top、margin-bottom 合并。
- **父子元素外边距合并的特定条件**：
  - **margin-top** 合并：父元素**没有内容或内容在子元素的后面**，且**没有内边距或边框**。
  - **margin-bottom** 合并：父元素**没有内容或内容在子元素的前面**，且**没有内边距或边框**。
  - 只要破坏其中一项，即可阻止合并发生。

**阻止 margin-top 合并发生的技巧**
- 为父元素设置 `border-top`
- 为父元素设置 `padding-top`
- 在父元素和第一个子元素之间添加**行内元素**作为分隔

**阻止 margin-bottom 合并发生的技巧**
- 为父元素设置 `border-bottom`
- 为父元素设置 `padding-bottom`
- 在父元素和最后一个子元素之间添加**行内元素**作为分隔
- 为父元素设置 `height`、`min-height` 或 `max-height`

---

## 五、5.4 背景（P145–P164）

> 在盒子模型中，content 盒不仅可以呈现主体内容，还可以添加背景颜色或图片。此时，需要使用 CSS 的背景属性，CSS 提供了功能强大且与背景控制相关的样式属性，可以实现背景图片的拉伸、平铺、定位等效果。

> **[排版说明]** 教材第 145 页标题处仅印有"背景"二字，按层级应为 **5.4 背景**，下含 5.4.1 背景颜色、5.4.2 背景图片（含 background-image / repeat / position / size / 渐变 / attachment / clip / origin）、5.4.3 背景综合样式。

### 5.4.1 背景颜色（P145）

**语法5-3 background-color 属性语法**

| 定义语法 | 示例 |
|---|---|
| `background-color:颜色预设值\|十六进制值\|RGB 值\|transparent\|inherit;` | `background-color:#ccc;` |

### 5.4.2 背景图片（P145–P159）

#### （1）background-image

**语法5-4 background-image 属性语法**

| 定义语法 | 示例 |
|---|---|
| `background-image:url(image_file_path)\|inherit;` | `background-image:url(images/01.jpg);` |

> 使用该语法可以将一张用户指定的图片添加到盒子模型中作为背景图片。但是单纯使用该语法有一定的局限性，如果要背景图片和盒子模型恰好匹配，则必须保证背景图片的大小和盒子模型的尺寸是一致的。类似于**计算机桌面**，当你为桌面指定背景图片时，如果背景图片不够大，则桌面上仅显示它的局部。

#### （2）background-repeat

**语法5-5 background-repeat 属性语法**

| 定义语法 | 示例 |
|---|---|
| `background-repeat:repeat\|repeat-x\|repeat-y\|no-repeat\|inherit;` | `background-repeat:repeat;` |

**代码5-11 background-repeat 属性示例（关键片段）**

```html
<style>
.box{                       /* #007-#014 */
    width: 300px;
    height: 300px;
    border:1px solid #666;
    float:left;
    margin-right: 20px;
    background-image:url("image/hotel-wallpaper.png");
}
.rpt-both{background-repeat: repeat;}   /* #015 */
.rpt-no{background-repeat: no-repeat;}  /* #016 */
.rpt-x{background-repeat: repeat-x;}    /* #017 */
.rpt-y{background-repeat: repeat-y;}    /* #018 */
</style>

<body>
<div class="box rpt-no"></div>
<div class="box rpt-both"></div>
<div class="box rpt-x"></div>
<div class="box rpt-y"></div>
</body>
```

**素材与讲解**：容器 300px×300px，背景图片 `hotel-wallpaper.png` 尺寸 **29px×40px**。
`no-repeat`：只显示一张；`repeat`：x、y 双向平铺；`repeat-x`：只在 x 方向平铺；`repeat-y`：只在 y 方向平铺。（图5-22）

#### （3）background-position

**引出问题**
> 如果水平的是 x 方向，垂直的是 y 方向，则为什么在使用 no-repeat 值时，背景图片在**左上角**呢？

**技术要点**：盒子模型中定位背景图片的**坐标系**见图5-23，规定容器**左上角为原点 (0,0)**。

**语法5-6 background-position 属性语法**

| 定义语法 | 示例 |
|---|---|
| `background-position:表示位置的预设关键字\|x% y%\|xpos ypos;` | `background-position:left top;` |

- 属性值由**两个位置坐标**构成，分别对应 x 方向和 y 方向，用**空格**分隔。
- 预设关键字：**top、right、bottom、left、center**；也可用 `0 0`、`0% 0%` 表示左上角起始偏移量。

**表5-11 background-position 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| 表示位置的预设关键字 | `left top`（默认值，左上角）<br>`center top`（居中靠上）<br>`right top`（右上角）<br>`left center`（靠左居中）<br>`center center`（水平垂直居中）<br>`right center`（靠右居中）<br>`left bottom`（靠左底部）<br>`center bottom`（居中底部）<br>`right bottom`（靠右底部）<br>第一个值表示水平位置，第二个值表示垂直位置，默认值为 left top。**如果只规定一个值，则另一个值默认值为 center** |
| 偏移量 xpos ypos | 第一个值表示水平位置，第二个值表示垂直位置，默认值为 0 0（对应 left top，表示左上角）。xpos 和 ypos 表示偏移量，即相对于左上角的偏移量，单位为 px 或 em。当 xpos 为正值时，表示从左向右移动，反之则表示从右向左移动；当 ypos 为正值时，表示从上向下移动，反之则表示从下向上移动。**如果只规定一个值，则另一个值是 50%（或 center）** |
| x% y% | 第一个值表示水平位置，第二个值表示垂直位置。偏移量为**相对于元素宽度和背景图片宽度之差的百分数**。默认值是 0% 0%（即左上角），右下角则是 100% 100%。**如果只规定一个值，则另一个值是 50%** |

**代码5-12 background-position 属性示例（关键片段）**

```html
<style>
.box{                       /* #007-#016 */
    width: 300px;
    height: 300px;
    border:1px solid #666;
    float:left;
    margin-right: 20px;
    background-image:url("image/HTML5-LOGO.png");
    background-repeat: no-repeat;
    background-size:50%;
}
.ps-tl{background-position: left top;}      /* #017 */
.ps-tr{background-position: 100% 0%;}       /* #018 */
.ps-br{background-position: 100% 100%;}     /* #019 */
.ps-bl{background-position: left bottom;}   /* #020 */
.ps-cc{background-position: 50% 50%;}       /* #021 */
</style>

<body>
<div class="box ps-tl"></div>
<div class="box ps-tr"></div>
<div class="box ps-br"></div>
<div class="box ps-bl"></div>
<div class="box ps-cc"></div>
</body>
```

运行效果见图5-24；定位原理见图5-25。素材说明：`HTML5-LOGO.png` 实际尺寸 **2048px×2048px**，容器 300px×300px，故用 `background-size:50%` 缩小一半便于观察。

#### （4）background-size（CSS3 新特性）

**教材关键解释（2 倍图/3 倍图）**
> 现在的电子设备屏幕分辨率越来越高，所以为了避免图像的像素点不够造成渲染模糊，开发者通常会使用 **2 倍图，甚至 3 倍图**作为背景图片。此时，要将过大的图片限制在一个小区域中就需要使用 background-size 属性了。

**语法5-7 background-size 属性语法**

| 定义语法 | 示例 |
|---|---|
| `background-size: length\|percentage\|cover\|contain;` | `background-size:cover;`<br>`background-size:contain;`<br>`background-size:50%;`<br>`background-size:20px;`<br>`background-size:auto 100%;`<br>`background-size:auto 20px;`<br>`background-size:100% 100%;`<br>`background-size:30px 50px;` |

**表5-12 background-size 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| length | 设置背景图片的高度和宽度。第一个值表示宽度，第二个值表示高度。如果只给出一个值，则第二个值为 auto（自动） |
| percentage | 计算相对于背景定位区域的百分比。第一个值表示宽度，第二个值表示高度，以空格隔开宽度和高度，以逗号隔开指定的多重背景。如果只给出一个值，则第二个值为 auto（自动） |
| cover | 保持图片的纵横比，并将图片缩放成能**完全覆盖**背景定位区域的最小大小 |
| contain | 保持图片的纵横比，并将图片缩放成**适合**背景定位区域的最大大小 |

**代码5-13 比较背景图片的 contain 和 cover（关键片段）**

```html
<style>
.box{                       /* #007-#016 */
    width: 600px;
    height: 500px;
    border:1px solid #666;
    float:left;
    margin-right: 20px;
    background-image:url("image/nbcc-pic.jpg");
    background-repeat: no-repeat;
    background-size:50%;
}
.ps-contain{background-size: contain;}  /* #017 */
.ps-cover{background-size: cover;}      /* #018 */
</style>

<body>
<div class="box ps-contain"></div>
<div class="box ps-cover"></div>
</body>
```

**对比结论（图5-26）**
> contain 具有**包含**的意思，表示将背景图片尽可能包含在容器中，同时**没有任何裁剪**，有时会留出大量空白；而 cover 表示使用背景图片**尽可能覆盖**当前容器，在必要时**裁剪**背景图片，从而**不留任何空白**。

#### （5）渐变背景（linear-gradient）

**素材/企业背景**：某健康 App 中的**打卡功能**，可见渐变背景（图5-27）。除使用渐变图片外，还可直接用 CSS 的 `linear-gradient()` 函数实现。

**语法5-8 linear-gradient()函数语法**

| 函数语法 | 示例 |
|---|---|
| `background-image: linear-gradient(direction, color-stop1, color-stop2, ...);` | `background-image:linear-gradient(45deg,red,blue);` |

- `linear-gradient()` 是一个**函数**；参数 `direction` 表示渐变的**角度和方向**，后续可接若干 CSS 颜色作为**渐变过渡的起止颜色**。

**任务5-7 制作健康打卡功能的渐变背景（P151–P153）**

- **任务目标**：根据图5-27 所示效果，使用渐变函数制作健康打卡功能的渐变背景（完成效果见图5-28）。
- **代码5-14 制作健康打卡功能的渐变背景**

```html
<style>
.box{                       /* #007-#016 */
    width: 200px;
    height: 150px;
    background-image: linear-gradient(45deg,#7ca9f0,#82d695);
    border-radius: 5px;
    line-height: 150px;
    color:white;
    font-size: 30px;
    text-align: center;
}
</style>

<body>
<div class="box">
    &gt;7 天跳绳打卡      <!-- #021 注意 > 需用实体引用 -->
</div>
</body>
```

**常见编程错误（原文）**
> （1）想在网页中显示">"字符，但不使用实体引用。
> （2）linear-gradient() 是一个函数，缺少函数参数的括号，以及参数和参数之间没有用逗号分隔。
> （3）错误地将渐变函数应用到 background-color 属性中。
> 以上都是常见的编程错误。

#### （6）background-attachment

**语法5-9 background-attachment 属性语法**

| 定义语法 | 示例 |
|---|---|
| `background-attachment:scroll\|fixed\|inherit;` | `background-attachment:fixed;` |

**代码5-15 对比 scroll 和 fixed（关键片段）**

```html
<style>
.box{                       /* #007-#019 */
    width: 500px;
    background-color: aqua;
    background-image: url("image/hotel-wallpaper.png");
    border:1px solid #666;
    border-radius: 5px;
    line-height: 50px;
    /* color:white; */
    font-size: 30px;
    text-align: center;
    float: left;
    margin-right: 10px;
}
.bg-scroll{                 /* #020-#022 */
    background-attachment: scroll;
}
.bg-fixed{                  /* #023-#025 */
    background-attachment: fixed;
}
</style>

<body>
<div class="box bg-scroll">Lorem ipsum dolor sit amet …</div>
<div class="box bg-fixed">Lorem ipsum dolor sit amet …</div>
</body>
```

**教材比喻（便于课堂讲解）**
> 当设置 `background-attachment:scroll;` 时，背景图片和前景文字就像一个**整体**，会一起滚动；而当设置 `background-attachment:fixed;` 时，背景图片和前景文字是**分离**的，背景图片就好像**墙纸**，固定不动，而前景文字就好像**窗帘**，它的滚动对墙纸不会有任何影响。

对比效果见图5-29、图5-30；素材同用 `image/hotel-wallpaper.png`。

#### （7）background-clip（CSS3 新增，背景裁剪）

**语法5-10 background-clip 属性语法**

| 定义语法 | 示例 |
|---|---|
| `background-clip: border-box\|padding-box\|content-box;` | `background-clip:content-box;` |

**代码5-16 背景剪裁属性（关键片段）**

```html
<style>
.box{                       /* #007-#017 */
    width: 300px;
    height: 300px;
    padding:30px;
    background-color: aqua;
    border:8px dotted #666;
    font-size: 16px;
    /* text-align: center; */
    float: left;
    margin-right: 10px;
}
.bgc-bb{background-clip: border-box;}     /* #018-#020 */
.bgc-pb{background-clip: padding-box;}    /* #021-#023 */
.bgc-cb{background-clip: content-box;}    /* #024-#026 */
</style>

<body>
<div class="box bgc-bb">宁波城市职业技术学院创建于2003 年…</div>
<div class="box bgc-pb">宁波城市职业技术学院创建于2003 年…</div>
<div class="box bgc-cb">宁波城市职业技术学院创建于2003 年…</div>
</body>
```

**结论（图5-31）**
- `border-box`：背景显示区域**覆盖 border 盒**
- `padding-box`：背景显示区域**覆盖整个 padding 盒**（边框线除外）
- `content-box`：背景显示区域**仅覆盖 content 盒**

#### （8）background-origin（CSS3 新增，背景图片起始定位）

**语法5-11 background-origin 属性语法**

| 定义语法 | 示例 |
|---|---|
| `background-origin: padding-box\|border-box\|content-box;` | `background-origin:content-box;` |

**与 background-clip 的区别（教材原文）**
> 从语法的使用和参数来看，background-clip 属性和 background-origin 属性非常相似。它们的区别在于 **background-origin 属性用来规定表示背景图片的定位区域，它的使用需要有背景图片的参与**。

**代码5-17 背景图片起始定位属性（关键片段）**

```html
<style>
.box{                       /* #007-#020 */
    width: 300px;
    height: 300px;
    padding:30px;
    background-color: aqua;
    background-image: url("image/hotel-wallpaper.png");
    background-position: left top;
    background-repeat: no-repeat;
    border:8px dotted #666;
    font-size: 16px;
    text-align: center;
    float: left;
    margin-right: 10px;
}
.bgo-bb{background-origin: border-box;}     /* #021-#023 */
.bgo-pb{background-origin: padding-box;}    /* #024-#026 */
.bgo-cb{background-origin: content-box;}    /* #027-#029 */
</style>
```

**结论（图5-32）**
> 将 background-origin 分别设置为 border-box、padding-box、content-box，背景图片的起始定位的基准明显不同，分别起始于 **border 盒、padding 盒和 content 盒的左上角**。

配合使用 `background-position:left top`、`background-repeat:repeat` 时也有细微差异（图5-33）。

---

### 5.4.3 背景综合样式（P160）

**语法5-12 background 综合样式属性语法**

| 定义语法 | 示例 |
|---|---|
| `background:bg-color bg-image position/bg-size bg-repeat bg-origin bg-clip bg-attachment initial\|inherit;` | `background:red url("images/bg.png") repeat-y;` |

**使用规则**
- 各属性值之间使用**空格**分隔。
- **必须设置背景颜色或背景图片**，其余参数可选，有需要时才添加，否则使用默认值。

**技巧（原文）**
> （1）**bg-size 只能紧接着 position 出现**，两者以"/"分隔，如 `center/80%`。
> （2）bg-origin 和 bg-clip 的取值都是 `<box>` 类型，可能出现 0 次、1 次或 2 次。如果出现 1 次，则它同时设置 background-origin 和 background-clip；如果出现 2 次，则在第 1 次出现时设置 background-origin，在第 2 次出现时设置 background-clip。

**常见编程错误（原文）**
> 在指定 background 综合样式属性时，没有设置颜色值也没有指定背景图片是常见的编程错误，必须指定两者中的一个。

#### 任务5-8 制作图标（P160–P162）

- **任务目标**：`icon-dot` 和 `icon-menu` 是移动应用界面中常见的两个图标，使用背景样式属性实现如图5-34 所示的图标效果。
- **代码5-18 制作图标**

```html
<style>
.icon-dot{                  /* #007-#017 */
    display: inline-block;
    width: 100px;
    height: 100px;
    padding:10px;
    border:10px solid;
    background-color: currentColor;
    background-clip:content-box;
    color:lightgrey;
    border-radius: 50%;
}
.icon-menu{                 /* #018-#028 */
    display: inline-block;
    width: 140px;
    height: 10px;
    padding:35px 0;
    border-top:10px solid;
    border-bottom:10px solid;
    color:lightgrey;
    background-color: currentColor;
    background-clip: content-box;
}
</style>

<body>
<div class="icon-dot"></div>
<div class="icon-menu"></div>
</body>
```

**技巧（原文）**
> currentColor 是 CSS3 中的变量，它表示**当前标签所继承的文字颜色**，利用它可以与当前 color 属性保持同步。

**讲解要点**
- 025 行将前景色设为 lightgrey；用 `currentColor` 让背景色与前景色同步；用 `background-clip` 把绘制区域指定为 **content 盒**。
- **icon-dot**：content 盒绘制 100px×100px，`border-radius:50%` 成实心圆，padding 10px 留白，10px 边框作为最外圈。
- **icon-menu**：content 盒高度 10px，与上、下边框宽度相等，实现"**三**"字形状。

#### 任务5-9 使用精灵图（P162–P164）

- **任务背景素材**：某**水果企业为北京奥运会提供新鲜水果产品**，利用美工提供的**精灵图**（图5-35），以单个图标作为背景图片制作 **10 个产品展示框**（每个框显示一种水果）。
- **素材文件**：`image/bdd.png`
- **代码5-19 使用精灵图（关键片段）**

```html
<style>
.box{                       /* #007-#014 */
    width: 172px;
    height: 200px;
    border:1px solid #ccc;
    float: left;
    margin-right: 10px;
    background: url("image/bdd.png") no-repeat;
}
.bdd1{background-position: 0 0;}            /* #015 */
.bdd2{background-position: -172px 0;}       /* #016 */
.bdd3{background-position: -344px 0;}       /* #017 */
.bdd4{background-position: 0px -200px;}     /* #018 */
.bdd5{background-position: -172px -200px;}  /* #019 */
.bdd6{background-position: -344px -200px;}  /* #020 */
.bdd7{background-position: -516px -98px;}   /* #021 */
</style>

<body>
<div class="box bdd1"></div>
<div class="box bdd2"></div>
<div class="box bdd3"></div>
<div class="box bdd4"></div>
<div class="box bdd5"></div>
<div class="box bdd6"></div>
<div class="box bdd7"></div>
</body>
```

**教材问答中的关键知识点（精灵图专题）**
1. **什么是精灵图？**
   > 精灵图取自英文 **Sprite** 的翻译，因为"雪碧"的英文也是 Sprite，所以有些书上也将它称为**雪碧图**。它通常将一组常用的图标、背景图片等按照一定的规律排列，组成一张完整的图片，便于程序员使用。
2. **为什么使用一张大图？**
   > 使用精灵图主要有两个优势：①**加快网页加载速度**。在请求一个具有较多图片的页面时（如 10 张），每张图片都要发送一次请求，会造成大量的性能消耗，而将相关图片组合在一起（合并为 1 张），这样只需请求一次，从而大大加快网页加载速度；②**便于后期维护**。将相关图片有规律地组合在一起，便于程序员开发和使用，同时为后期的修改提供了便利。
3. **如何使用精灵图？**
   > 这里需要根据素材的尺寸和特征，并配合 **background-image、background-repeat、background-position** 属性来实现，**类似于放大镜的使用**。你看到的结果是放大镜中照到的局部信息，通过移动放大镜（也可以理解为移动背景图片），局部信息会发生变化，而移动操作就是通过 background-position 属性进行精准定位的。
4. **如何获取坐标？**
   > 有两种方法：①使用 **Photoshop 等绘图软件**打开原稿，使用测量工具获取西瓜的坐标信息；②直接使用**浏览器开发者工具的调试功能**，通过调试获取坐标信息，并将满意的结果回填到代码中。
5. **技巧（原文）**
   > 通过 Photoshop 等绘图软件和浏览器开发者工具可以有效地帮助用户获取背景图片的坐标信息。

运行效果见图5-36。

---

## 六、5.5 小结（P164）

> 本项目重点介绍了盒子模型的相关知识，以及衍生出来的边框、外边距、背景属性的相关特性。掌握盒子模型是学好 CSS 样式规则应用的重要基石，也为后续的 Web 前端开发奠定了重要基础。

---

## 七、5.6 作业（P164–P165）

### 一、选择题
1. 图5-37 所示为一个**部门通知页面**的局部效果，要实现框选部分中的部门装饰线，可以使用的样式属性是（    ）。
   A．border-top　B．border-right　C．border-bottom　D．border-left
2. 关于边框样式属性，说法正确的是（    ）。
   A．border 有 4 个方向，不能单独对某个特定方向的边框风格进行指定
   B．border-style-right 可以用来对右边框的风格进行指定
   C．在 border 简写样式中，颜色、风格和宽度 3 个值的定义顺序可以颠倒
   D．在使用 border-color 时，只能使用十六进制值
3. 下列属于 background-repeat 的默认值的是（    ）。
   A．no-repeat　B．repeat　C．repeat-x　D．repeat-y
4. 关于 margin 和 padding，说法正确的是（    ）。
   A．inline 元素可以通过 width 和 height 分别指定宽度和高度
   B．当相邻行内元素均设置 padding 时会发生合并
   C．当相邻块级元素均设置 margin 时会发生合并
   D．当相邻行内元素均设置 margin 时会发生合并
5. 关于背景图片，说法正确的是（    ）。
   A．如果一个图标需要提供单击效果，则应该使用 `<img>` 标签而不是背景图片
   B．背景图片一旦被指定，将无法移动
   C．在同一个元素中，如果同时指定背景图片和背景颜色，则谁先定义，将先显示谁
   D．在同一个元素中，只能添加一张背景图片

### 二、操作题
> 实现鼠标指针悬停后高亮的效果是一种常见的功能。请在本书所附的教学项目源文件中，使用 **ch05/images/all_bg.gif** 精灵图，并结合**链接的伪类的特性**，实现鼠标指针悬停后高亮的效果。显示效果如图5-38 所示（默认显示效果 / 鼠标指针悬停后的显示效果）。

### 三、项目讨论
> 精灵图的出现由来已久，在早期的游戏制作中经常使用它。请查找相关资料，列举一个游戏中使用精灵图的案例。结合你的经验，对比精灵图在游戏、网页制作中的使用原理，并讨论使用精灵图的优点。

---

# 项目6 表格和表单

## 一、项目扉页信息（P166）

### 思政课堂（原文要点）
> 2022 年 2 月 4 日至 20 日，北京冬奥会在我国北京市和张家口市联合举行，它是一次全球性的体育盛会。在这次冬奥会上，展现出了**胸怀大局、自信开放、迎难而上、追求卓越、共创未来**的"**北京冬奥精神**"。它激励着我们这代人坚持理想信念，坚定不移地为社会主义伟大事业而奋斗；坚持实事求是，脚踏实地地去创造。我们要把爱国之情、报国之志转化为实际行动，努力拼搏，为祖国争光！

### 学习目标（照抄要点）
- 了解表格的两个作用
- 掌握表格标签及语义
- 掌握表格数据的导入方法
- 了解表单的用途
- 掌握常用表单标签的使用方法
- 掌握 `<input>` 标签及其变体的使用方法

### 技能目标（照抄要点）
- 能正确使用表格标签创建表格
- 能使用表格样式属性美化表格
- 能正确使用表单标签创建表单
- 能使用表单样式属性美化表单

### 素养目标（照抄要点）
- 培养以用户为中心的产品质量意识
- 培养勇于探索、崇尚科学的意志和品德
- 遵守网络规范、网络法规

---

## 二、6.1 表格（P167–P168）

**表格在网页制作历史进程中的两个作用**：
1. **实现网页内容的布局**——图6-1 所示为利用表格实现的复杂界面布局，通过单元格的分割和合并生成具有 **①～⑦ 七个不同板块**的页面效果。
2. **呈现相关的数据**——图6-2 所示为利用表格呈现**汽车详细参数**的页面效果。

**发展脉络**
- 表格初衷是以行列形式将数据罗列出来，结构紧凑、清晰直观，日常生活中大量使用：**财务报表、课程表、问卷调查表**等。
- 由于表格可灵活合并单元格，2008 年以前表格的一个用途是实现网页内容布局。
- 随着前端技术发展，CSS 出现后，使用表格布局网页的方式**已逐渐被抛弃**。
- 目前表格的主要用途回归到它的初衷——**呈现数据**。

> 基于表格具有典型的结构化特征，本项目的主要学习目标是：掌握与表格相关的**结构化标签**；掌握与**美化表格相关的 CSS 样式属性**及其应用。

---

## 三、6.2 表格标签（P168–P173）

- 一个表格通常包括 **行、列和单元格** 3 个部分：**行**是水平分隔、**列**是垂直分隔、**单元格**是行和列相交所产生的区域，用于存放表格数据。
- 也可将表格内容划分为 3 个区域：**表格页眉**（存放表头内容）、**表格主体**（存放数据）、**表格页脚**（存放脚注内容，如汇总数据等）。整个表格还可包含**标题**。

**表6-1 表格标签（完整还原）**

| 标签名 | 描述 |
|---|---|
| table | 定义表格 |
| tr | 定义表格行（table row） |
| th | 定义表格字段的标题（table heading） |
| td | 定义表格的数据（table data） |
| thead | 定义表格页眉 |
| tbody | 定义表格主体 |
| tfoot | 定义表格页脚 |
| caption | 定义表格标题 |

**图示**：图6-3 网页中表格与标签代码的对应关系（`<table>` 代表整个表格；7 行（含标题行）数据 → `<table>` 内 7 组 `<tr>`；每行 4 个单元格 → 16～19 行将 4 组 `<td>` 作为 `<tr>` 的子元素）。

**单元格区别（问答要点）**
> 从样式上来看，它们之间的区别在于**标题单元格是自带加粗样式的，在默认情况下内容是居中的**，而**数字单元格默认是不加粗、居左**的。另外，标题单元格和数字单元格从语义上有很明显的区别，前者用来存放标题信息，后者用来承载数据。这里并没有规定标题单元格的具体位置，因此它既可以出现在第一行，又可以出现在第一列或其他位置上。

**`<caption>` 标签**：用于定义表格标题，**默认在表格中居中显示**。

**表6-2 `<caption>` 标签的两个属性（完整还原）**

| 属性名 | 属性值 | 描述 |
|---|---|---|
| align | left\|center\|right | 设置水平对齐方式，默认值为 center |
| valign | top\|bottom | 设置垂直对齐方式，默认值为 top |

**`<thead>`、`<tbody>`、`<tfoot>`**
- `<thead>`：表格的**表头**分组，组合表格的表头内容。
- `<tbody>`：表格的**主体内容**分组，组合表格中的数据。
- `<tfoot>`：表格的**页脚（表注）**分组，组合表格的页脚（表注）。
- 划分意义：使浏览器有能力支持独立于表格表头和页脚的**表格正文滚动**；长表格打印时表头和页脚可打印在**包含表格数据的每个页面上**；可用 CSS 对这些区域分别设置样式。
- **这 3 个标签不能单独使用，需要配合使用。**

**表6-3 表格的标签属性（完整还原）**

| 属性名 | 属性值 | 描述 |
|---|---|---|
| align | left\|center\|right | 定义表格相对于容器窗口的水平对齐方式，默认靠左对齐 |
| border | pixels | 定义表格边框线的粗细，默认没有边框线 |
| bgcolor | 十六进制值\|RGB 值\|预设颜色值 | 定义表格的背景颜色 |
| cellpadding | pixels | 定义单元格的内边距，即数据与边框线之间的距离 |
| cellspacing | pixels | 定义单元格的间距，即单元格与单元格之间的距离 |
| height | pixels\|% | 定义表格的高度，即百分比相对于父元素的高度 |
| width | pixels\|% | 定义表格的宽度，即百分比相对于父元素的宽度 |

**表6-4 表格行的标签属性（完整还原）**

| 属性名 | 属性值 | 描述 |
|---|---|---|
| align | left\|center\|right | 定义表格行的水平对齐方式 |
| bgcolor | 十六进制值\|RGB 值\|预设颜色值 | 定义表格行的背景颜色 |
| height | pixels | 定义表格行的高度 |
| valign | baseline\|top\|middle\|bottom | 定义单元格的垂直对齐方式，默认垂直居中（middle） |

**表6-5 单元格的标签属性（完整还原）**

| 属性名 | 属性值 | 描述 |
|---|---|---|
| align | left\|center\|right | 定义单元格的水平对齐方式，`<td>` 标签默认靠左，`<th>` 标签默认居中 |
| colspan | number | 定义单元格可跨越列的数目 |
| rowspan | number | 定义单元格可跨越行的数目 |
| height | pixels\|% | 定义单元格的高度，即百分比相对于表格的高度 |
| width | pixels\|% | 定义单元格的宽度，即百分比相对于表格的宽度 |
| valign | baseline\|top\|middle\|bottom | 定义单元格的垂直对齐方式，默认垂直居中（middle） |
| bgcolor | 十六进制值\|RGB 值\|颜色预设值 | 定义单元格的背景颜色 |

**重要结论（教材原文）**
> 这些属性在早期制作表格的过程中对表格的美化起着至关重要的作用。随着 CSS 的出现，绝大多数美化表格的工作已经由 CSS 来完成。**在 HTML5 中，除了 colspan 和 rowspan，其余属性都不建议使用。**

**问答（合并单元格）**
> colspan 和 rowspan 是不是就是合并单元格的意思？——正是如此。由于这两个属性用于**控制表格的结构**，因此其在 HTML5 中被继续保留下来。

---

### 任务6-1 使用 Emmet 语法制作金牌榜表格（P170–P173）

- **任务目标**：将本书所附的教学项目源文件中的图片素材放置在对应项目的 images 文件夹中，然后制作 **2008 年北京奥运会金牌榜表格**，效果如图6-4 所示。
- **核心步骤**：
  1. 观察行列数 → **7 行 4 列**（包含标题行）。
  2. 使用 Emmet 语法快速生成基本结构：**`table>tr*7>td*4`**
  3. 将数据依次填入；**将表格第一行单元格标签由 `<td>` 修改为 `<th>`**。
  4. 给 `<table>` 依次添加 `bgcolor`、`border`、`align`、`width` 属性查看效果。
  5. 对行添加 `align`、`bgcolor` 实现居中和间隔底纹。
- **代码6-1 使用 Emmet 语法制作金牌榜表格（关键片段）**

```html
<table>
    <tr>
        <th>国家/地区</th>
        <th><i class="golden"></i></th>
        <th><i class="silver"></i></th>
        <th><i class="copper"></i></th>
    </tr>
    <tr>
        <td>中国</td>   <td>51</td>  <td>21</td>  <td>28</td>
    </tr>
    <tr>
        <td>美国</td>   <td>36</td>  <td>38</td>  <td>36</td>
    </tr>
    <tr>
        <td>俄罗斯</td> <td>23</td>  <td>21</td>  <td>28</td>
    </tr>
    <tr>
        <td>英国</td>   <td>19</td>  <td>13</td>  <td>15</td>
    </tr>
    <tr>
        <td>德国</td>   <td>16</td>  <td>10</td>  <td>15</td>
    </tr>
    <tr>
        <td>澳大利亚</td> <td>14</td> <td>15</td>  <td>17</td>
    </tr>
</table>
```

**教材问答（为何用 `<i>` 而不是 `<img>`）**
> 因为注意到提供给我们的 **all_bg.gif** 素材文件是一张**精灵图**。我们打算利用项目5 中所讲的精灵图来实现金、银、铜牌图标的显示。011～013 行代码使用 `<i>` 标签作为精灵图的局部显示容器，后面将在该容器中分别显示金、银、铜牌图标。

**属性添加演示**
```html
<table bgcolor="#eee" border="1" align="center" width="600px">
```
→ 图6-6 添加 `<table>` 标签属性的应用效果。

```html
<tr align="center"  bgcolor="#fff">
```
→ 图6-7 具有**间隔底纹**的表格效果（使数据居中、某些行高亮）。

**问答（双线边框与折叠）**
> 为什么表格单元格的边框线看起来像有两条线，如何将它们折叠起来？
> ——cellpadding 表示单元格的内边距，cellspacing 表示单元格之间的距离。每个单元格的 4 条边框线形成了单元格自身的范围，而单元格之间的距离正是由 cellspacing 属性控制的。可以尝试修改 `<table>` 标签的 **cellspacing** 属性。
> - 图6-8：cellspacing 值从 **0 → 5**，双线情况越来越明显，单元格之间距离越来越大。
> - 图6-9：cellpadding 值从 **0 → 10**，单元格文字到边框线之间的内边距不断变大。

---

## 四、6.3 CSS 表格相关样式属性（P174–P179）

**表6-6 CSS 表格相关样式属性（完整还原）**

| 属性名 | 属性值 | 描述 |
|---|---|---|
| border-collapse | separate\|collapse | 默认值为 separate，表格边框线和单元格边框线分开 |
| border-spacing | length | 指定相邻单元格边框线之间的距离，单位为 px、em 等。如果定义两个参数值，则第一个参数值为相邻单元格之间的**水平间隔距离**，第二个参数值为相邻单元格之间的**垂直间隔距离** |
| caption-side | top\|bottom | 默认值为 top，表示表格标题显示在表格上方 |
| table-layout | automatic\|fixed | 默认值为 automatic，使用自动表格布局算法，调整表格及其单元格的宽度以适应内容。如果设置该属性值为 fixed，则使用固定表格布局算法，在使用此关键字时，需要使用 width 属性显式指定表格的宽度。如果设置 width 属性值为 auto 或未指定，则浏览器使用自动表格布局算法，在这种情况下，固定值不起作用 |

**单元格对齐方式（9 种）——教材问答要点**
> 和 Word 中表格的单元格对齐方式一样（见图6-10），主要分成**左上、中上、右上、左中、中中、右中、左底、中底、右底 9 种**。要实现这些对齐方式，只需提供两个样式属性分别控制水平方向和垂直方向。
> - 水平方向：仍使用 **text-align**（left、center、right）
> - 垂直方向：使用针对表格专门提供的 **vertical-align**（top、middle、bottom）
> - 配合使用便有 **3×3=9 种**单元格对齐方式。
> - **单元格的默认对齐方式是左中**，即 `text-align:left；vertical-align:middle`。

**技巧（原文）——valign 与 vertical-align 的区别**
> 对照表6-5，vertical-align 样式属性的功能与对应的单元格的标签属性 valign 的功能相同。注意它们的使用区别：①在写法上，单元格的标签属性用缩写，而样式属性用单词全拼，并用"-"分隔多个单词，有人形象地将这种书写规范称为"**烤肉串**"式写法；②样式属性用在 CSS 样式定义中，而单元格的标签属性用在表格的开始标签中。

### 任务6-2 导入数据创建表格（P174–P179）

- **任务目标**：根据本书所附的教学项目源文件提供的 **GoldenMedalRank.txt** 和素材精灵图，使用 CSS 表格相关样式属性实现 2008 年北京奥运会金牌榜表格的创建，效果如图6-11 所示。
- **核心步骤（Dreamweaver 导入）**：
  1. 将光标放置在代码第 8 行（`<body>` 标签内部），选择 **"File" → "Import" → "Tabular Data"** 命令（图6-12），打开导入数据对话框（图6-13）。
  2. ① 选择 **GoldenMedalRank.txt** 所在的物理磁盘位置。
  3. ② 指定数据分隔符——GoldenMedalRank.txt 中数据使用 **"Tab"** 进行分隔。
  4. ③ 指定生成的表格大小——这里指定为固定的 **"600 Pixels"**。
  5. ④ 指定 Cell padding、Cell spacing、Border 等值。"Cell padding"和"Cell spacing"文本框**留空表示使用默认值**，在"Border"文本框中输入 **"1"**。
  6. 单击"OK"按钮，完成数据导入，自动生成表格的 HTML 代码（图6-14）。
  7. 打开"**CSS Designer**"面板（图6-15），单击 Sources 左侧的"+"按钮，选择"**Create A New CSS File**"命令（图6-16）。
  8. 指定新样式表文件名为 **style**，存放位置在 **css 文件夹**中，并以 **Link** 方式引入当前文件（图6-17）。
- **素材测量**：根据提供的素材精灵图，可测量出**金、银、铜牌图标的尺寸是 18px×17px**（图6-18），并获取它们在背景图片中的坐标位置。
- **代码6-2 导入数据创建表格（关键片段）**

```html
<head>
    <meta charset="UTF-8">
    <title>数据导入金牌榜表格</title>
    <link href="css/style.css" rel="stylesheet" type="text/css">
</head>
<body>
<table width="600px" border="1">
    <caption>2008 年北京奥运会金牌榜</caption>
    <tr>
        <th>国家/地区</th>
        <th><i class="golden"></i></th>
        <th><i class="silver"></i></th>
        <th><i class="copper"></i></th>
    </tr>
    <tr>
        <td>中国 </td>  <td>51 </td>  <td>21 </td>  <td>28</td>
    </tr>
    <tr>
        <td>美国 </td>  <td>36 </td>  <td>38 </td>  <td>36</td>
    </tr>
    <tr>
        <td>俄罗斯 </td><td>23 </td>  <td>21 </td>  <td>28</td>
    </tr>
    <tr>
        <td>英国 </td>  <td>19 </td>  <td>13 </td>  <td>15</td>
    </tr>
    <tr>
        <td>德国 </td>  <td>16 </td>  <td>10 </td>  <td>15</td>
    </tr>
    <tr>
        <td>澳大利亚 </td><td>14 </td><td>15 </td>  <td>17</td>
    </tr>
</table>
</body>
```

- **代码6-3 金牌榜表格的相关 CSS 代码（完整还原）**

```css
@charset "UTF-8";
table{
    border-collapse: collapse;
    color:#666;
    font-size: 12px;
    margin:0 auto;
    border:1px solid #ccc;
}
tr td,tr th{
    text-align: center;
    vertical-align: middle;
}
th:first-child{
    background-color: #ccc;
    color:white;
}
th i{
    background: url("../images/all_bg_01.gif") no-repeat;
    display: inline-block;
    width: 18px;
    height: 17px;
}
caption{
    font-size: 26px;
    font-weight: bold;
}
.golden{
    background-position: 0 -79px;
}
.silver{
    background-position:-18px -79px;
}
.copper{
    background-position: -36px -79px;
}
```

**讲解要点（教材原文）**
> 013 行代码使用 **`:first-child` 伪类**指定第一个标题单元格的样式，017～022 行代码使用 `<i>` 标签将精灵图作为背景图片，并将其指定为 **18px×17px** 大小的**行内块**；027～035 行代码的背景图片定位语句分别用于显示金、银、铜牌图标。

---

## 五、6.4 表单（P179–P180）

> 表单是 Web 应用的重要组成部分，负责**收集、发送和处理用户提供的数据**，为 Web 应用提供更多的功能。
- **图6-19 商品搜索表单**（用于搜集用户浏览的商品）
- **图6-20 登录表单**（用于搜集用户的账号信息）

**表单的基本原理**
1. 用户在表单中输入想要提交的信息，提交的信息会通过 HTTP 的 **POST 方法或 GET 方法**在服务器和客户端之间传递。
2. 服务器接收并处理，检查信息是否符合要求（如检查用户名是否存在、密码是否符合要求等）。
3. 检查通过 → 将数据存入数据库并反馈给用户（成功或失败）；未通过 → 发送错误消息，要求重新输入。
4. 有时使用**验证码**防止机器人或恶意程序通过表单提交大量无效内容——这是表单的一种重要保护措施。
5. 表单提供多种提交形式：**按钮、文本框、复选框、单选按钮**等。
6. 还有一些安全控制（如只允许特定浏览器、cookie 控制）可帮助用户**防范 XSS 攻击**或保护表单提交的数据。

---

## 六、6.5 表单标签（P180–P199）

> 表单是网页中一个用于搜集用户数据的特定区域。它由 `<form>` 标签定义，该标签主要起到两个作用：一是用于**限定表单的范围**（定义一个特定区域容纳表单的相关控件，单击提交按钮时该区域内的所有数据都将被提交给服务器）；二是利用该标签的相关属性可以**定义提交方式、指定后台处理程序**等。

```html
<form name="表单名称" method="提交方式" action="服务端程序">
…
</form>
```

**表6-7 `<form>` 标签的常用属性（完整还原）**

| 属性 | 描述 |
|---|---|
| name | 指定表单名称，该名称同时作为表单的变量 |
| method | 定义表单数据从客户端传送到服务器中的方法，主要包括 GET 方法和 POST 方法，默认使用 GET 方法 |
| action | 指定处理表单的服务端程序 |
| onsubmit | 指定处理表单的脚本函数 |
| enctype | 设置 MIME 类型，默认值为 application/x-wwww-form-urlencoded；当需要上传文件夹到服务器中时，要将该属性值设置为 multipart/form-data |
| target | 与 `<a>` 标签的 target 属性类似，用于规定在何处打开 action URL，包括 _self、_blank、_parent、_top 和 framename |

**GET 与 POST 的区别（教材问答要点）**
> 使用 **GET 方法**可以将表单内容**附加到 URL 后面**，浏览器厂商对 URL 的长度通常会有一定的限制。例如，**IE 浏览器对 URL 的最大限制字符数为 2083 个**，如果超出这个数字，则提交按钮没有任何反应。同时，GET 方法**不具有保密性**，不适合处理密码、银行卡卡号等要求保密的内容，且**不能传送非 ASCII 码的字符**。
> 使用 **POST 方法**可以使用户在表单中填写的数据**包含在表单的主体中**传送给服务器中的处理程序，该方法**没有字符数和字符类型的限制**，包含了 **ISO 10646** 中的所有字符，所传送的数据**不会显示在浏览器的地址栏中**。

**技巧（原文）**
> 在默认情况下，表单使用 GET 方法传送数据，当数据涉及**保密内容**时，**必须**使用 POST 方法；当所传送的数据用于执行**插入或更新数据库操作**时，**建议**使用 POST 方法；而当执行**搜索操作**时，**建议**使用 GET 方法。

---

### 6.5.1 `<input>` 标签（P181–P188）

```html
<input type="类型" name="表单元素名称">
```
- `<input>` 是表单标签中十分复杂，也是十分重要的一个，主要用于设置表单输入元素。
- `type` 用于设置不同类型的输入元素；`name` 用于指定输入元素的名称，**同时作为服务端程序访问表单元素的变量标识**，必须符合标识符定义且**必须唯一**。

**表6-8 type 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| text | 文本框 |
| password | 密码框 |
| file | 文件域 |
| hidden | 隐藏域 |
| radio | 单选按钮 |
| checkbox | 复选框 |
| submit | 提交按钮 |
| button | 普通按钮 |
| reset | 重置按钮 |
| image | 图像按钮 |

**常见编程错误（原文）**
> 对于 name 属性值，错误地使用中文或不符合标识符的定义是初学者容易犯的错误。

#### 1. 文本框
```html
<input type="text" name="文本框名称" >
```
- type 为 text 时创建**单行输入文本框**，输入内容以**明文**形式显示。

**表6-9 `<input>` 标签常用属性（完整还原）**

| 属性 | 描述 |
|---|---|
| maxlength | 设置文本框中可以输入的最大字符数 |
| size | 控制文本框的长度。单位是像素，默认值为 20 像素 |
| value | 设置文本框的默认值 |
| placeholder | 规定可描述输入 `<input>` 字段预期值的简短提示信息 |
| readonly | 默认值，规定该文本框为只读状态 |
| disable | 规定应该禁用的 `<input>` 标签 |

#### 2. 密码框
```html
<input type="password" name="密码框名称">
```
- 密码框会使用 **"*"符号或"●"符号**回显输入的字符，起到保密作用。

#### 3. 文件域
```html
<input type="file" name="avatarPic" >
```
- 用于将本地文件上传到服务器；服务端程序通过 name 变量名获取该域的文件数据。
- **必须**在 `<form>` 标签中添加 **`enctype="multipart/form-data"`**，同时将表单提交方式指定为 **POST** 方法。

#### 4. 隐藏域
```html
<input type="hidden" name="域名称" value="域值">
```
- 用于在不同页面之间**隐式传递页面数据**，必须同时提供 **type、name、value** 三个属性。
- 数据以"**键值对**"形式提供：name 是键，value 是值。
- **常见编程错误**：未提供 name 属性和 value 属性。

#### 5. 单选按钮
```html
<input type="radio" name="单选按钮名称" value="值" checked="checked" >
```
- `value`：被选中后传递到服务端的变量值。
- `checked="checked"`：默认被选中（默认选项）。不指定则无默认选项。
- **排他性**通过相同的 `name` 实现。
- **常见编程错误**：对于单选按钮，必须提供 `<input>` 的 **type、name、value** 属性，缺少相应属性将无法构成完整的单选按钮。

**代码6-4 单选按钮示例（完整还原）**

```html
<body>
<form action="">
    <input type="radio" name="gender" value="male" checked>男
    <input type="radio" name="gender" value="female">女
</form>
</body>
```

**讲解要点（图6-21）**
- 009 行的 `checked` 表示"男"是默认选项。
- `gender` 作为性别组的名称，服务端通过它读取用户当前选中的单选按钮。
- **它的值不是"男"或"女"，而是 `male` 或 `female`**（即 value 属性的对应值）。
- **为什么 `checked="checked"` 变成了 `checked`？**
  > 这是 **HTML5 对布尔属性提供的简化写法**，类似地，`readonly="readonly"` 可以简化为 `readonly`，`disabled="disabled"` 可以简化为 `disabled`。

#### 6. 复选框
```html
<input type="checkbox" name="复选框名称" value="域值" checked="checked">
```
- 用于在一组选项中进行**多项选择**，每个复选框均用一个方框表示。
- 用法与单选按钮非常类似；**区别在于单选按钮具有排他性，而复选框允许用户多选**。
- **常见编程错误**：同一组复选框使用不同的 name 属性值。**同一组复选框必须使用相同的 name 属性值。**

**代码6-5 复选框示例（关键片段）**

```html
<form action="">
<p>继杨利伟之后，2005 年，下列哪两名航天员搭乘神舟六号载人飞船，第一次进入轨道舱，
第一次进行航天医学空间实验研究，完成了中国真正意义上有人参与的空间科学实验？</p>
    <input type="checkbox" name="astr" value="ylw" />杨利伟<br>
    <input type="checkbox" name="astr" value="fjl" checked />费俊龙<br>
    <input type="checkbox" name="astr" value="nhs" checked />聂海胜<br>
    <input type="checkbox" name="astr" value="lbm" />刘伯明<br>
    <input type="checkbox" name="astr" value="jhp" />景海鹏<br>
</form>
```
→ 图6-22。同一组复选框的 name 相同（`astr`），表示传递到服务端可读取的变量名。

#### `<label>` 标签（提升可用性问答）
> 为什么用户必须精确选中文字前面的 ○ 或 □ 才能选中该选项？很多网页/移动应用中只要选择后面的文字选项就能选中。
> ——需要配合使用 **`<label>` 标签**。该标签专门用于 `<input>` 标签，用户只要单击 `<label>` 标签，就可以实现对应 `<input>` 标签的**聚焦**。

**两种用法**：
- **第一种：隐藏式（隐式绑定）**——`<label>` 与 `<input>` 以**父子嵌套**关系形成隐式绑定。
  ```html
  <label>
      <input type="radio" value="male" name="gender">男
  </label>
  ```
- **第二种：指定式（显式绑定）**——为 `<input>` 添加**唯一的 id 属性**，在 `<label>` 中使用 **for 属性**实现显式绑定。
  ```html
  <input type="checkbox" name="astr" id="lbm" value="lbm" /><label for="lbm">刘伯明</label>
  ```

**常见编程错误（原文）**
> 在使用 `<label>` 标签的指定式绑定语法时，for 属性值对应的是 `<input>` 标签的 **id 属性值**，而不是 name 属性值。

#### 7. 提交按钮
```html
<input type="submit" name="按钮名称" value="按钮显示文本" >
```
- name 用于设置按钮变量名，后端程序不需要引用时可忽略；value 用于设置按钮上的显示文本。
- 提交按钮会**触发整个表单**，将其内容提交到 `<form>` 的 action 属性所指定的服务端程序或在客户端脚本中处理。

#### 8. 普通按钮
```html
<input type="button" name="按钮名称" value="按钮显示文本" onclick="JavaScript 函数">
```
- 可添加事件属性处理单击后的响应事件，**onclick 是常见的事件属性之一**。
- 普通按钮会触发按钮事件动作，需配合 **JavaScript 脚本**对表单执行处理操作。

#### 9. 重置按钮
```html
<input type="reset" name="按钮名称" value="按钮显示文本" >
```
- 用于**清除表单中所输入的内容**，将表单内容恢复到加载页面时的最初状态。

#### 10. 图像按钮
```html
<input type="image" name="按钮名称" src="图像路径" alt="替换信息" width="宽度" height="高度" >
```
- `src` 为**必须设置**的属性；`alt` 通常也需要设置（无法访问图像时显示替换信息）；`width`、`height` 指定宽高。
- 教材态度：虽然图像按钮可以改变单调的默认按钮外观，但**利用 CSS 同样可以达到美化按钮的目的，而且推荐使用 CSS 的做法**。

#### 任务6-3 `<input>` 标签的综合示例（P187–P188）

- **任务目标**：根据上述 `<input>` 标签的相关知识，制作一个简单的**登录表单**，要求具有**重置按钮、提交按钮、图像按钮、普通按钮**（图6-23）。单击"删除用户"按钮后执行 onclick 函数（图6-24）。
- **素材**：`image/btn_bg.png`
- **代码6-6 `<input>` 标签的综合示例（完整还原）**

```html
<head>
    <meta charset="utf-8">
    <title>input 按钮</title>
    <script>
        function deluser(){
            if(confirm("确定删除当前用户?"))
                console.log("用户已删除!");
        }
    </script>
</head>
<body>
<form action="">
    用户名:<input type="text" name="username"  size="50" placeholder="输入8 位字母数字组合" /><br>
    密码:<input type="password" name="password" size="50"  placeholder="输入6 位密码" /><br>
    <input type="reset" value="重置"><input type="submit" value="登录"><br>
    <input type="button" value="删除用户" onclick="deluser()">
    <input type="image" src="image/btn_bg.png" alt="图片按钮" name="imageBtn" width="100">
</form>
</body>
```

**讲解要点**
- `size` 指定了文本框的长度；`placeholder` 是 **HTML5 新增的属性**，用来描述文本框的提示文字。
- "删除用户"按钮提供 `onclick` 属性，指定该事件由 `deluser()` 函数执行。我们将 `deluser()` 称为一次**函数的调用**，当 onclick 事件发生时（用户单击按钮），上述定义函数将执行一次。

---

### 6.5.2 `<button>` 标签（P188–P189）

```html
<button type="submit|button| reset" name="按钮名称" value=" 初始值">文本|图片|…</button>
```
- `<input>` 构成的按钮**内容只能是文本**；当需要在按钮中包含图片或其他元素、或在样式/脚本上更灵活时，使用 `<button>`。
- 包裹在 `<button>` 内部的内容即按钮的内容，可以是**文字、图片、动画**等。
- `type` 取值：`submit`（等效提交按钮）、`button`（等效普通按钮）、`reset`（等效重置按钮）。
- 默认值差异：**W3C 浏览器中 type 默认为 submit**；**IE9 以前版本的 IE 浏览器中默认为 button**。

**技巧（原文）**
> 在较低版本的 IE 浏览器中，如 IE9 以前版本的 IE 浏览器，将提交 `<button>` 与 `<button/>` 标签之间的内容；而其他 W3C 浏览器和 IE10 及其以后版本的 IE 浏览器将提交 `<button>` 标签 **value 属性**的内容。

**代码6-7 使用 `<button>` 标签（关键片段）**

```html
<script>
function deluser(){
    if(confirm("确定删除当前用户?"))
        console.log("用户已删除!");
}
</script>

<body>
<form action="">
    用户名:<input type="text" name="username"  size="50" placeholder="输入8 位字母数字组合" /><br>
    密码:<input type="password" name="password" size="50"  placeholder="输入6 位密码" /><br>
    <button type="submit">登录</button><button type="reset">重置</button><br>
    <button type="button" onclick="deluser()">删除用户</button>
    <button><img src="image/btn_bg.png" alt="图片按钮" width="100"></button>
</form>
</body>
```

→ 图6-25。对图片按钮而言，**直接将 `<img>` 标签作为 `<button>` 标签的子元素**来实现，更加方便和直观。

---

### 6.5.3 `<select>` 标签（P190–P193）

- **列表框**（图6-26）允许用户从选项列表中选择一项或几项，等效于单选按钮（单选时）或复选框（多选时）；在选项比较多时使用列表框可以**节省很大的空间**。
- **下拉列表**（图6-27）是一种**一次只能显示和选择一个选项**的特殊的列表框。
- 正因为下拉列表可理解为特殊的列表框，所以 HTML 中**使用同一套标签**实现它们。

#### 1. 列表框
```html
<select name="列表名" size="显示的选项数目" [multiple="multiple"]>
    <option value="选项值1" [selected="selected"]>选项1</option>
    <option value="选项值2" [selected="selected"]>选项2</option>
    …
</select>
```
- `<select>` 用于声明列表框，指定选项是否可多选、一次可显示的选项数目。
- `<option>` 用于设置**选项值（value）** 及选项是否为**默认选项（selected）**。
- 可选属性 **multiple** 实现多选效果：不添加时只能选择一个；添加时可选择多个。

**教材问答要点**
> `<select>` 的 name 属性值就是整个列表的变量名；用户具体选择了哪些选项，提交时会将 **value 属性值**提交给服务端程序，后端程序只需根据 name 提供的变量名即可得到用户的当前选择。——"你理解得非常正确。这些表单常用控件的使用规则对你今后掌握脚本开发和后端程序开发至关重要。"

**代码6-8 列表框示例（关键片段）**

```html
<form action="">
<p>继杨利伟之后，2005 年，下列哪些航天员搭乘神舟六号载人飞船，第一次进入轨道舱，
第一次进行航天医学空间实验研究，完成了中国真正意义上有人参与的空间科学实验？</p>
<select name="astr" size="6" multiple="multiple">
    <option value="ylw">杨利伟</option>
    <option value="fjl" selected="selected">费俊龙</option>
    <option value="nhs">聂海胜</option>
    <option value="lbm">刘伯明</option>
    <option value="jhp">景海鹏</option>
</select>
</form>
```
→ 图6-28。

#### 2. 下拉列表
```html
<select name="下拉列表名" >
    <option value="选项值1" [selected="selected"]>选项1</option>
    <option value="选项值2" [selected="selected"]>选项2</option>
    …
</select>
```
- 同样使用 `<select>` 和 `<option>`；不给 `<select>` 添加 size 和 multiple 属性。
- 因为 **size 属性值默认为 1**，可理解为"当前列表框只显示一个选项的**退化情况**"。

**代码6-9 下拉列表示例（关键片段）**

```html
<form action="">
<p>截至2023 年，下面哪个城市既举办过冬季奥运会，又举办过夏季奥运会？</p>
<select name="city" size="1">
    <option value="shanghai">上海</option>
    <option value="beijing" selected="selected">北京</option>
    <option value="newyork">纽约</option>
    <option value="tokyo">东京</option>
</select>
</form>
```
→ 图6-29（默认选择效果）、图6-30（单击下拉按钮的效果）。

---

### 6.5.4 `<textarea>` 标签（P193–P194）

- 文本框只能以**单行形式**显示文本；当用户输入内容较多时（如填写问卷或回复评论），使用多行**文本域**（图6-31）。

```html
<textarea name="文本域名" rows="行数" cols="列数">
  …(此处输入默认文字)
</textarea>
```

**代码6-10 文本域示例（完整还原）**

```html
<form action="">
    <textarea name="comments" rows="5" cols="20" placeholder="有什么新鲜事想跟大家分享?"></textarea>
</form>
```
→ 图6-32。指定了 5 行 20 列，并使用 HTML5 新属性 `placeholder` 添加提示文字。

**教材问答要点：默认文字 vs placeholder**
> 我们知道 `<textarea>` 中的 name 属性值就是该文本域的变量名，本示例中是 **comments**。
> - 如果**仅添加提示文字**，那么 comments 变量的值**仍为空**；
> - 如果**仅添加默认文字**，那么 comments 变量的值是用户添加的默认文字。
>
> 也可以这么理解，**placeholder 属性仅起到提示的作用，不会影响 `<textarea>` 标签**；而**默认文字会影响 `<textarea>` 标签提交给服务器的值**，相当于对 comments 变量进行初始化。

---

### 6.5.5 表单新属性（P194–P198）

> HTML5 中添加了 **form、formaction、required、autofocus、pattern** 等新属性，这些新属性提供了**数据验证、非空校验、自动聚焦和信息提示**等功能，从而替代早期需要使用脚本实现的功能，极大地简化了表单功能的设计与实现。

#### 1. form 属性
```html
<form id="login_form">
…
</form>
<input type="text" form="login_form" >
```
- HTML5 之前，一个表单的标签**必须放在 `<form>` 标签内**。
- HTML5 为所有表单标签添加了 **form 属性**，可定义表单标签和某个表单之间的**从属关系**。
- 允许将 `<input>` 放在 `<form>` 标签**外**，但需通过 form 属性指定它所属的表单，**其值对应表单标签的 id 属性值**。
- 意义：可以更灵活地实现表单的布局。

#### 2. formaction 属性
```html
<input type="submit" formaction="处理程序" >
```
- 场景：**一个表单中包含两个或两个以上的提交按钮**，如学工系统中的学生管理模块（通常一个表单中包含**增加、修改和删除**按钮），单击不同按钮会将表单数据提交给不同的后台程序处理。
- HTML5 之前只能通过 JavaScript 动态修改 `<form>` 的 action 属性；HTML5 中只需在每个**提交按钮**中使用 formaction 属性指定处理逻辑。
- 适用：`<input type="submit">`、`<input type="image">`、`<button type="submit">`。

**代码6-11 formaction 属性示例（关键片段）**

```html
<form action="">
    <p>姓名:张三</p>
    <p>学号:031102</p>
    <p>
        <input type="submit" value="新增" formaction="add.do">
        <input type="submit" value="修改" formaction="update.do">
        <input type="submit" value="删除" formaction="delete.do">
    </p>
</form>
```
→ 图6-33。

#### 3. required 属性
```html
<input type="text" name="name" required>
```
或者
```html
<input type="text" name="name" required="true">
```
- 用于**取代"判断内容是否为空/字符长度是否为零"的实现脚本**，简化页面开发步骤。
- 适用：表单中需要提交内容的表单标签，如 `<input>`、`<textarea>`、`<select>` 等。

**代码6-12 使用 required 属性进行字段非空校验（关键片段）**

```html
<form action="">
    <p>姓名:<input type="text" id="name" required /></p>
    <p>学号:<input type="text" name="id" id="id" required /></p>
    <p><input type="submit" value="确定提交">
    </p>
</form>
```
→ 图6-34。

#### 4. autofocus 属性
```html
<input type="text" autofocus>
```
或者
```html
<input type="text" autofocus="true">
<textarea rows="" cols="" autofocus>…</textarea>
```
或者
```html
<textarea rows="" cols="" autofocus="true">…</textarea>
```
- HTML5 表单的 **textarea 和所有 `<input>` 标签**都具有 autofocus 属性，属性值是一个**布尔值，默认值是 false**。
- 一旦设置，页面加载完成后该标签将**自动获得焦点**。
- **注意**：在一个页面中，**最多只能对一个表单标签设置该属性**，否则该功能将失效。**建议对第一个 `<input>` 标签设置 autofocus 属性。**

#### 5. pattern 属性
```html
<input type="text" pattern="正则表达式" title="错误提示信息" >
```
- pattern 属性是 `<input>` 标签的**验证属性**，属性值是一个**正则表达式**，通过该表达式验证输入内容的有效性。
- 正则表达式是一种高效的用于匹配字符串中字符组合的模式，被广泛应用在 Word、Excel 等常用文本处理软件和 JavaScript、Python 等程序语言中。

**代码6-13 正则表达式校验示例（关键片段）**

```html
<form action="">
    学号: <input type="text" name="id" id="id" required pattern="\d{8}"
        title="请输入8 位学号"/>
    用户名:<input type="text" name="username" id="username" required
        pattern="^[a-zA-Z]\w{2,7}" title="请输入用户名，必须以字母开始，字母与数字的组合，长度为3~8 位"/>
    <button type="submit">提交</button>
</form>
```

**正则表达式讲解要点（教材原文）**
> 对于 **8 位学号**，正则表达式中的 `\d` 表示所有数字符号，`{8}` 表示多重性，即出现 8 次数字符号，这就意味着用户只有输入 8 位数字才符合要求。
> 对于**用户名**，正则表达式中的 `^ [a-zA-Z]` 表示以大写或小写字母开始，`\w` 表示字母和数字的组合，`{2,7}` 表示最少 2 个、最多 7 个，这也就意味着用户名**最少 3 位、最多 8 位**，但必须是以字母开始的字母与数字的组合。

**关于 title 属性（问答）**
> title 属性是用来显示错误提示的吧？——你说得没错，当用户输入不符合正则表达式的用户名时，将显示 **title 属性值**。

（效果图6-35：8 位学号的验证效果；图6-36：用户名的验证效果）

---

### 6.5.6 表单美化（P198–P199）

**为什么要重置**
> 在默认情况下，表单标签都具有一些**自带样式**。使用不同的浏览器调试可以发现它们渲染默认表单标签的效果也是不一样的。这些默认样式在不同浏览器中的渲染差异会导致显示效果不一致，在严重时还会对网页布局造成影响，从而影响用户的浏览体验。通常，为了避免这些情况的发生，确保不同浏览器的显示效果一致，需要**重置表单标签的默认样式**。

**如何查看默认样式（问答）**
> 在项目5 中，我们介绍了开发者工具，常见浏览器都提供了自身的开发者工具。利用它找到你要查看的表单标签，就可以查看对应的样式及盒子模型的信息了。

**表6-10 常见表单标签的默认样式和样式重置（完整还原）**

| 表单标签 | 默认样式 | 样式重置 |
|---|---|---|
| form | 在 IE6 浏览器中，`<form>` 标签有一个 margin 属性值 | `form{`<br>`margin:0;`<br>`}` |
| input | 文本框：有内填充、边框<br>单选框：有外边距<br>复选框：有外边距<br>各 input 控件默认都有 outline 轮廓线 | `input[type=text]{`<br>`border:none;`<br>`padding:0;`<br>`outline:0;`<br>`}`<br>`input[type=radio]{`<br>`margin:0;`<br>`outline:0;`<br>`}`<br>`input[type=checkbox]{`<br>`margin:0;`<br>`outline:0;`<br>`}` |
| textarea | 不同浏览器略有不同，通常具有上外边距、下外边距、内边距和边框。有些浏览器的右下角有倒三角图标，可以对文本域进行拉伸，需要使用 **resize** 属性。在 IE6 浏览器下，当标签内容没超出时也会有滚动条，需要使用 **overflow** 属性 | `textarea{`<br>`margin:0;`<br>`padding:0;`<br>`outline:0;`<br>`resize:0;`<br>`overflow:auto;`<br>`}` |
| select | 默认有边框，某些浏览器还有内边距 | `select{`<br>`padding:0;`<br>`}` |
| option | 默认有左内边距、右内边距 | `option{`<br>`padding:0px npx;`<br>`}`<br>这里的 n 根据需要设定 |

**outline 说明（教材原文）**
> 这里简要介绍一下 outline，它是描述控件范围的一圈**轮廓线**，通常位于元素的边缘。当按"**Tab**"键切换表单控件时，当前选中的控件将被一圈轮廓线围绕，以突出当前获得焦点的控件。

**outline 与 border 的区别（问答）**
> 首先，**outline 在 border 的外围，不会占据元素空间，也不会影响布局**；其次，**border 应用于几乎所有的 HTML 元素，而 outline 仅针对链接、表单控件等少量元素**。

**技巧（原文）**
> outline 效果在随着焦点 **focus** 到控件上时自动出现，当失去焦点 **blur** 时自动消失。

**属性选择器在表单重置中的应用（原文）**
> 表6-10 中在对表单进行样式重置时，使用了类似 **`input[type=text]`** 的**属性选择器**，利用它可以选择复杂多变的 `<input>` 标签。（呼应项目4 的 4.1.6 节）

### 任务6-4 个性化表单控件美化（P199 起）

- **任务目标**：学会了表单控件的重置，再添加一些自定义样式，就可以个性化地设计出表单元素。使用表单控件美化和重置语法，并利用本书所附的配套素材实现如图 6-37 所示的**表单控件美化效果**。
- **素材/图示**：图6-37 表单控件美化效果。
- **实现代码**：代码6-14 表单控件美化（**内容位于第 200 页之后，超出本次指定读取范围，需另行补充**）。

---

# 附录 A：本范围内教材全部任务清单（便于课件串联）

| 编号 | 任务名 | 页码 | 类型 |
|---|---|---|---|
| 任务3-6 | 使用自定义字体（思源黑体） | 85–86 | 项目3 尾巴 |
| 任务3-7 | 使用伪类（链接按钮三态） | 87–89 | 项目3 尾巴 |
| 任务4-1 | 将内嵌式改为链接式 | 108–109 | 操作演示 |
| 任务4-2 | Emmet 语法练习1：多重性和项目编号 | 117 | 练习 |
| 任务4-3 | Emmet 语法练习2：分组 | 118 | 练习 |
| 任务5-1 | 使用开发者工具查看盒子模型 | 124–125 | 观察验证 |
| 任务5-2 | 设置支付宝小程序中的 padding | 127–129 | 综合制作 |
| 任务5-3 | 编写并查看边框风格 | 131–133 | 验证演示 |
| 任务5-4 | 边框的神秘之旅（气泡对话框） | 134–139 | 综合进阶 |
| 任务5-5 | 相邻元素外边距合并 | 141–142 | 验证演示 |
| 任务5-6 | 父子元素外边距合并 | 143–144 | 验证演示 |
| 任务5-7 | 制作健康打卡功能的渐变背景 | 151–153 | 综合制作 |
| 任务5-8 | 制作图标（icon-dot / icon-menu） | 160–162 | 综合制作 |
| 任务5-9 | 使用精灵图（水果企业/北京奥运会） | 162–164 | 综合制作 |
| 任务6-1 | 使用 Emmet 语法制作金牌榜表格 | 170–173 | 综合制作 |
| 任务6-2 | 导入数据创建表格 | 174–179 | 综合制作 |
| 任务6-3 | `<input>` 标签的综合示例（登录表单） | 187–188 | 综合制作 |
| 任务6-4 | 个性化表单控件美化 | 199 起 | 综合制作（代码在第 200 页后） |

---

# 附录 B：第 83–92 页（项目3 收尾）补充表格

**表3-13 常见的伪类类型描述（完整还原，P87）**

| 伪类类型 | 描述 |
|---|---|
| :active | 选中被激活的元素 |
| :link | 选中未访问的元素 |
| :hover | 选中鼠标指针悬停的元素 |
| :visited | 选中访问过的元素 |
| :focus | 选中当前光标所在位置的元素 |
| :first-child | 选中元素的第一个子元素 |
| :lang | 选中具有 lang 属性的元素 |

**表3-14 常见的伪元素（完整还原，P90）**

| 伪元素 | 描述 |
|---|---|
| ::first-letter | 选中文本的第一个字符 |
| ::first-line | 选中文本的第一行 |
| ::before | 在选择器选择的元素之前添加内容，并可以为其添加样式 |
| ::after | 在选择器选择的元素之后添加内容，并可以为其添加样式 |

**语法补充（P85–P90）**
- 自定义字体：`@font-face{ font-family:自定义字体的名称; src: url('fontfile_url'); }`，引用时 `font-family:qigong;`
- **常见编程错误**：引用的字体名称与自定义的字体名称不一致，往往是造成自定义字体不起作用的常见原因。
- 伪类语法：`选择器:伪类{ 属性1:属性值1; ... }`
- 伪元素语法：`选择器::伪元素{ 属性1:属性值1; ... }`
- 通用选择器：`*{ 属性1:属性值1; ... }`，常见写法 `*{ margin:0px; padding:0px; }`
- **技巧：Normalize.css** 保留有用的默认样式，并通过标准化样式纠正常见错误和浏览器的不一致性。

---

# 附录 C：教材中出现的案例 / 素材 / 企业背景清单

## 项目4
| 案例/素材 | 说明 | 页码 |
|---|---|---|
| 中国航天员（杨利伟 / 费俊龙 / 聂海胜） | 行内式、内嵌式、链接式三段示例的统一素材 | 105–109 |
| 航天素材图 `images/astronaut.png` | 属性选择器示例中的宇航员图片（alt="宇航员"） | 103–104 |
| 神舟五号 2003 年 10 月 15 日至 16 日 / "航天英雄" | 属性选择器 HTML 文案 | 104 |
| 思政素材：航天精神（"两弹一星"、载人航天、月球探测） | 思政课堂 | 93 |
| 思政素材：能否列举完成航天任务的航天员 | 项目讨论 | 121 |

## 项目5
| 案例/素材 | 说明 | 页码 |
|---|---|---|
| 宁波城市职业技术学院支付宝小程序功能项 | "学生优惠指南""学生特价机票""校园兼职指南""更多服务"，图标 + 文字卡片 | 127（图5-4） |
| `images/nbcc-icon1.png`、`images/nbcc-icon2.png` | 支付宝小程序示例图标素材 | 128 |
| 微信聊天气泡对话框 | 边框制三角 + 矩形正文框 | 134–139 |
| 标签页 / 菜单提示 / 气泡对话框 | 边框的三个常见应用场景图 | 134（图5-8/5-9/5-10） |
| `image/hotel-wallpaper.png`（29px×40px） | 背景平铺 / 滚动 / origin 对比素材 | 146、154、158 |
| `image/HTML5-LOGO.png`（2048px×2048px） | 背景定位 + background-size 素材 | 148–149 |
| `image/nbcc-pic.jpg` | contain / cover 对比素材（600×500 容器） | 150–151 |
| 某健康 App 打卡功能渐变背景 | `linear-gradient(45deg,#7ca9f0,#82d695)`，文案">7 天跳绳打卡" | 151–153 |
| icon-dot / icon-menu 移动应用图标 | background-clip + currentColor 绘制 | 160–162 |
| 某水果企业为北京奥运会提供新鲜水果 → 精灵图 `image/bdd.png`（172×200 单元格） | 精灵图任务 | 162–164 |
| 宁波城市职业技术学院简介文案 | background-clip / background-origin 示例文本 | 156–159 |
| 数字化生活应用：支付宝、Keep、京东、淘宝 | 思政课堂 | 122 |
| 部门通知页面装饰线 | 作业选择题素材（图5-37） | 164 |
| `ch05/images/all_bg.gif` 精灵图 + 链接伪类悬停高亮 | 操作题素材（图5-38） | 165 |

## 项目6
| 案例/素材 | 说明 | 页码 |
|---|---|---|
| 表格实现的复杂界面布局（①～⑦ 七个板块） | 说明表格的"布局"作用（图6-1） | 167 |
| 汽车详细参数表格 | 说明表格的"呈现数据"作用（图6-2） | 167 |
| 2008 年北京奥运会金牌榜（7 行 4 列） | 项目主线案例，贯穿任务6-1、6-2 | 170–179 |
| `GoldenMedalRank.txt`（Tab 分隔） | Dreamweaver 导入表格数据的数据源文件 | 174–176 |
| `../images/all_bg_01.gif` / `all_bg.gif` 精灵图 | 金、银、铜牌图标，18px×17px，坐标 `0 / -18 / -36 -79px` | 172、176、178–179 |
| 商品搜索表单 / 登录表单 | 说明表单用途（图6-19、图6-20） | 179 |
| `image/btn_bg.png` | `<input type="image">` 与 `<button><img></button>` 的图片按钮素材 | 188、189 |
| 神舟六号航天员多选题（杨利伟/费俊龙/聂海胜/刘伯明/景海鹏） | 复选框与列表框示例 | 184、191 |
| 既举办过冬季奥运会又举办过夏季奥运会的城市（上海/北京/纽约/东京） | 下拉列表示例 | 192–193 |
| 学工系统学生管理模块（新增/修改/删除，add.do / update.do / delete.do） | formaction 示例 | 195–196 |
| 思政素材：2022 北京冬奥会、"北京冬奥精神"（胸怀大局、自信开放、迎难而上、追求卓越、共创未来） | 思政课堂 | 166 |

---

# 附录 D：启发式对话问答关键知识点汇总

## 项目3 尾巴（供衔接）
| 问题 | 要点 |
|---|---|
| 访问过的链接如何恢复？ | 打开浏览器历史记录删除相应页面的访问记录（图3-20）；开发者工具提供伪类状态查看器，单击":hov"可勾选强制查看元素状态（图3-21）。 |
| 为什么要有伪类和伪元素这两个看起来很古怪的东西？ | HTML 是一个文档树，CSS 引入这两个概念是为了**格式化并处理文档树之外的信息**（如段落首字母下沉、在一组列表中选择第一个元素）。 |
| 伪类和伪元素的主要区别？ | 伪类代表元素的**不同状态**（如链接的未访问/悬停/访问过），随用户行为动态变化，这些状态在普通文档树中无法描述；伪元素是**具有元素性质又不存在于文档树中的"幽灵"元素**。从实现角度：伪元素 `::first-letter` 用来代替用 `<span>` 包裹首字符；`:first-child` 伪类用来代替给 `<li>` 加自定义类（如 `<li class="first-one">`）。 |
| **良好编程习惯** | 建议在写伪元素时使用两个单冒号（如 `::before`），以区别伪类。 |
| 通用选择器的作用 | 类似程序中的初始化，将浏览器默认样式"覆盖"（如把 margin、padding 初始化为 0px）。 |
| **技巧：Normalize.css** | 实际开发中不一定完全重置，可采用 Normalize.css 保留有用的默认样式并纠正常见错误和浏览器不一致性。 |

## 项目4
| 小节 | 问题 | 要点 |
|---|---|---|
| 4.1.1 交集 | 交集选择器有什么具体含义？ | 选择器部分同时具有 `div` 和 `.nav` 类样式（中间无空格），所选 `<div>` 必须具备 `.nav` 类样式属性；只有 `<div class="nav">` 被选中。 |
| 4.1.2 并集 | 为什么叫分组/群组选择器？ | 是基本选择器的一种组合，实现样式代码的有效复用，等价于拆开的多条规则。 |
| 4.1.3 后代 | 直接子元素可视作特殊的后代选择器吗？ | 确实如此，直接父子关系是一种特殊的后代关系，引出子元素选择器。 |
| 4.1.3 后代 | 书写从哪个父元素开始、到哪个子元素结束有要求吗？ | 常困扰初学者的典型问题。后代选择器提供特定上下文的限定，**只要上下文关系足够覆盖要运用规则的元素即可**；自左向右书写，左侧是父元素，随后可以是任何嵌套层次的后代元素。 |
| 4.1.5 相邻兄弟 | 改成 `p+p` 会选中哪些元素？ | 前者是段落元素、与其相邻的段落元素才被选中 → "办文明事"符合；对"办文明事"而言，后续相邻的"讲文明话"也符合 → 后两个段落都应用该样式（图4-7）。 |
| 4.1.5 相邻兄弟 | 与"做文明人"相邻的为什么不起作用？ | 相邻兄弟选择器确切地说是**后续相邻的兄弟元素**，对前序相邻兄弟元素不起作用——初学者容易犯错之处。 |
| 4.2 | 为什么要从行内式到内嵌式？ | 行内式无法很好复用；抽象成 `.highlight` 类样式，对多个段落添加相同类属性，实现同页面样式代码的高效复用。 |
| 4.2 | 多页面如何统一样式？ | 引出**外部样式表（链接式样式表）**。 |
| 4.3 优先级 | 如何计算优先级？ | A/B/C/D 如同十进制的千位、百位、十位、个位；通用选择器全为 0；`p a`=2；`p a.color`=12；`p .color div #news`=112；行内 style=1000。 |
| 4.3 就近 | 优先级相同且存在继承时怎么办？ | 越靠近要格式化的元素优先级越高（本例 a 覆盖 li → 蓝色）。 |
| 4.3 覆盖 | 优先级与继承层级都相同？ | 后面定义的覆盖前面定义的（新增 `a{color:red}` → 红色）。 |
| 4.5 | CSS 与 LESS/SASS/SCSS 的关系？ | 类似程序语言中的机器语言与高级语言；CSS 预处理器分 LESS 和 SASS 两大类。 |
| 4.5 | 能否进行逻辑判断？ | 不仅可以数学运算、函数引用，还可以进行样式分解和组合；详细用法超出本书范围，可查官网。 |

## 项目5
| 小节 | 问题 | 要点 |
|---|---|---|
| 5.1.1 | padding/border/margin 的命名规律？ | 都有上右下左 4 个方向，统一用 `xxx-top/right/bottom/left` 表示。 |
| 5.1.2 | 值复制原则 | 1 值→四边；2 值→上下/左右；3 值→上/左右/下；4 值→上右下左。 |
| 5.2.1 | `border-style:dashed solid` 是什么意思？ | 上、下虚线，左、右实线。 |
| 5.3.2 | margin 取负值时合并效果如何？ | 得出**"正正取大值""正负相加值""负负最负值"**；-10 与 10 相加为 0 → 垂直方向无缝相接。 |
| 5.3.2 | 多个子元素时如何合并？ | 第一个子元素的 margin-top 和最后一个子元素的 margin-bottom 会分别与父元素的 margin-top、margin-bottom 合并。 |
| 5.3.2 | 如何阻止父子 margin 合并？ | 破坏特定条件：设置 border-top/bottom、padding-top/bottom、插入行内元素分隔，或为父元素设置 height/min-height/max-height。 |
| 5.4.2 | 背景图片不够大怎么办？ | 类似计算机桌面，可**平铺或拉伸**，引出 background-repeat 与 background-size。 |
| 5.4.2 | 为什么 no-repeat 时背景图片在左上角？ | 引出 background-position 与背景坐标系（左上角为原点 (0,0)，图5-23）。 |
| 5.4.2 | `x% y%` 的含义？ | 偏移量是**相对于元素宽度和背景图片宽度之差的百分数**，所以水平方向 100% 才是靠右（图5-25）。 |
| 5.4.2 | `background-size:50%` 是什么意思？ | CSS3 新特性，控制背景图片大小；图标 2048×2048 而容器只有 300×300，缩小一半便于观察；实际开发中常用 **2 倍图、3 倍图**配合该属性。 |
| 5.4.2 | contain 与 cover 的区别？ | contain 尽量**包含**（无裁剪，可能留白）；cover 尽量**覆盖**（必要时裁剪，不留空白）。 |
| 5.4.2 | scroll 与 fixed 的区别？ | scroll：前景与背景像整体一起滚动；fixed：背景像**墙纸**固定不动，前景文字像**窗帘**滚动而互不影响。 |
| 5.4.2 | background-clip 与 background-origin 的区别？ | origin 规定**背景图片的定位区域**，需要有背景图片参与；clip 规定**背景的绘制区域**。 |
| 5.4.3 | 背景属性太麻烦，有综合样式吗？ | 有 `background` 综合样式属性。bg-size 只能紧跟 position 并以"/"分隔；bg-origin/bg-clip 可出现 0/1/2 次。 |
| 任务5-9 | 什么是精灵图？为什么用大图？怎么用？坐标怎么获取？ | 见"任务5-9"四条要点。 |

## 项目6
| 小节 | 问题 | 要点 |
|---|---|---|
| 6.2 | `<th>` 与 `<td>` 的区别？ | 标题单元格自带加粗样式、默认内容居中；数字单元格默认不加粗、居左。语义上前者存放标题信息，后者承载数据。标题单元格位置不限。 |
| 6.2 | colspan / rowspan 是不是合并单元格？ | 正是如此。用于控制表格的结构，HTML5 中继续保留。 |
| 任务6-1 | 金、银、铜牌为什么用 `<i>` 而不是 `<img>`？ | 因为 all_bg.gif 是一张**精灵图**，用 `<i>` 作为精灵图的局部显示容器。 |
| 任务6-1 | 单元格边框为什么像有两条线？ | cellspacing 控制单元格之间的距离（0→5 越来越明显）；cellpadding 控制内容与边框线距离（0→10 越来越大）。 |
| 6.3 | 用 CSS 如何实现表格内容在单元格中对齐？ | 同 Word，共 9 种（3×3）；水平用 `text-align`，垂直用 `vertical-align`；默认 `left / middle`。 |
| 6.3 | valign 与 vertical-align 的区别？ | 功能相同；写法上标签属性用缩写、样式属性用全拼并以"-"分隔（"烤肉串"式写法）；样式属性用于 CSS 定义，标签属性用于开始标签。 |
| 任务6-2 | 如何把外部 txt 数据快速导入 HTML 生成表格？ | 除 Emmet 手写外，可用 **Dreamweaver 的 Import → Tabular Data** 功能。 |
| 6.4/6.5 | GET 与 POST 有何区别？ | IE URL 上限 2083 字符；GET 不保密且不能传非 ASCII；POST 含 ISO 10646 全部字符且不显示在地址栏。 |
| 6.5.1 | 单选按钮如何实现互斥？ | 同一组使用相同的 `name`（如 gender），服务端读取到的值是 **value**（male/female）而不是显示文本（男/女）。 |
| 6.5.1 | 为什么 `checked="checked"` 变成了 `checked`？ | HTML5 对布尔属性的简化写法，类似 `readonly`、`disabled`。 |
| 6.5.1 | 为什么必须精确点中 ○/□ 才能选中？ | 需要配合 `<label>`：单击 label 即可聚焦对应 input。**隐藏式（嵌套）** 与 **指定式（for + id）** 两种；for 对应的是 **id** 而非 name。 |
| 6.5.3 | `<select>` 的 name 是变量名吗？ | 是。name 是变量标识，提交时提交的是 option 的 **value**。 |
| 6.5.3 | 下拉列表和列表框语法相近吗？ | 同一套标签；下拉列表可不写 size 和 multiple，size 默认为 1，可理解为"只显示一个选项的退化情况"。 |
| 6.5.4 | `<textarea>` 中的默认文字与 placeholder 有何区别？ | placeholder 仅提示，不影响提交值（变量仍为空）；默认文字会影响提交值，相当于初始化变量。 |
| 6.5.5 | title 属性是错误提示吗？ | 是，输入不符合正则时显示 title 属性值。 |

---

# 附录 E：逐页要点索引（PDF 第 83–199 页）

| 页码 | 一句话要点 |
|---|---|
| 83 | 项目3 尾：代码3-7 文字排版控制（font 简写 + text-indent） |
| 84 | 代码3-7 续：span 红色加粗微软雅黑下划线 letter-spacing 1.05em；div 600px 边框 |
| 85 | 3.3.5 自定义字体 `@font-face` 语法；常见编程错误（字体名不一致） |
| 86 | 代码3-8 使用自定义思源黑体 SourceHanSansCN-Bold.otf（任务3-6） |
| 87 | 3.3.6 伪类选择器 语法3-15；表3-13 常见伪类；任务3-7 |
| 88 | 代码3-9 伪类按钮 `a` / `a:hover` / `a:visited` |
| 89 | 代码说明；清除访问记录与开发者工具":hov"状态查看器；3.3.7 伪元素 |
| 90 | 语法3-16 伪元素；表3-14；伪类与伪元素区别；良好编程习惯（写 `::`） |
| 91 | 3.3.8 通用选择器 `*`；Normalize.css 技巧 |
| 92 | 3.4 小结；3.5 作业（选择题） |
| 93 | 项目4 扉页：思政课堂（航天精神）+ 学习目标/技能目标/素养目标 |
| 94 | 4.1 复合选择器；4.1.1 交集选择器 语法4-1；代码4-1 起始 |
| 95 | 代码4-1 说明与图4-1；4.1.2 并集选择器 语法4-2 |
| 96 | 代码4-2 并集选择器（div/span/p 集体声明） |
| 97 | 4.1.3 后代选择器 语法4-3；代码4-3 结构 |
| 98 | 图4-3；问答（后代 vs 直接子元素、书写起点、良好编程习惯）；4.1.4 起始 |
| 99 | 语法4-4 子元素选择器；代码4-4 起始 |
| 100 | 代码4-4 结构（第二组 ul 内为 `li>span>a`） |
| 101 | 图4-4/4-5；后代与子元素最大区别；4.1.5 相邻兄弟 语法4-5；代码4-5 |
| 102 | 图4-6/4-7；`p+p` 考考你；技巧（后续相邻的兄弟元素） |
| 103 | 4.1.6 属性选择器 语法4-6；表4-1 常见属性选择器；代码4-6 起始 |
| 104 | 代码4-6 综合示例（中国航天员、astronaut.png 图文混排） |
| 105 | 4.2 应用样式的三种方式；4.2.1 行内式 代码4-7 |
| 106 | 4.2.2 内嵌式；常见编程错误；技巧（type 可省略）；代码4-8 起始 |
| 107 | 代码4-8 `.highlight`；图4-10；引出外部样式表；4.2.3 链接式语法 |
| 108 | link 语法与 type 省略技巧；任务4-1 步骤与代码4-9 |
| 109 | 代码4-9；相对路径 `css/style.css`；良好编程习惯；4.3 解决冲突四原则；代码4-10 起始 |
| 110 | 代码4-10 样式冲突；优先级原则与 A/B/C/D；表4-2 优先级权重表 |
| 111 | 优先级计算讲解；表4-3 利用优先级解决冲突；图4-14；就近原则 |
| 112 | 代码4-11 就近原则 → 蓝色；覆盖原则 |
| 113 | 代码4-12 覆盖原则 → 红色；!important 原则 语法4-7 |
| 114 | 代码4-13 !important → 蓝色（高于行内式） |
| 115 | 4.4 Emmet 简介（Zen Coding）；4.4.1 基础语法 语法4-8 |
| 116 | 语法4-8 续（`^` 父级）；4.4.2 多重性和项目编号 语法4-9 |
| 117 | `$`/`$$`/`$$$`/`@`/`-` 说明；任务4-2（倒序、指定起始序号） |
| 118 | 4.4.3 分组 语法4-10；任务4-3；`html:5` / `!` / `link` |
| 119 | 4.5 LESS、SASS 和 SCSS；Sass 与 SCSS 语法区别；图4-18～4-20 |
| 120 | 图4-21；LESS 用 `@`、SCSS 用 `$` 定义变量；4.6 小结 |
| 121 | 4.7 作业：选择题、简述题、项目讨论（航天员与航天精神） |
| 122 | 项目5 扉页：思政课堂（支付宝/Keep/京东/淘宝）+ 目标 |
| 123 | 5.1 盒子模型简介；5.1.1 组成与常见编程错误；方向命名规律 |
| 124 | 任务5-1 开发者工具查看盒子模型 代码5-1 |
| 125 | 开发者工具快捷键；盒子模型观察 → 引出值复制原则 |
| 126 | 5.1.2 值复制原则 表5-1、语法5-1、表5-2、语法5-2 |
| 127 | 值复制简化书写；5.1.3 内边距特性；任务5-2 支付宝小程序 padding（图5-4） |
| 128 | 代码5-2 nbcc-icon1/2.png 功能模块 |
| 129 | 170px 宽度计算；padding 显示背景；5.2 边框；5.2.1 边框风格 表5-3 |
| 130 | 值复制用于边框风格；表5-4 边框风格值（`dashed solid` 解读） |
| 131 | 任务5-3 编写并查看边框风格 代码5-3（8 个盒子） |
| 132 | 代码5-3 结构与 `float` 并排 |
| 133 | 图5-7；5.2.2 边框宽度 表5-5、表5-6；5.2.3 边框颜色 表5-7 |
| 134 | 5.2.4 边框综合样式 表5-8；任务5-4 边框的神秘之旅（图5-8/5-9/5-10） |
| 135 | 代码5-4 加粗边框 → 图5-11 |
| 136 | 代码5-5 宽高归零 + 四色边框 → 图5-12 出现三角形 |
| 137 | 代码5-6 transparent → 图5-13 单个三角；代码5-7 气泡 HTML 结构；图5-14 |
| 138 | 图5-15 位置关系；top 计算公式；代码5-8 气泡对话框 |
| 139 | 图5-16；`top=50/2-12=13px`；5.3 外边距；表5-9 外边距属性 |
| 140 | 表5-10 取值；5.3.2 外边距特性；相邻合并 图5-17 |
| 141 | 任务5-5 相邻元素外边距合并 代码5-9 |
| 142 | 图5-18；"正正取大值/正负相加值/负负最负值"；图5-19 合并为 0 |
| 143 | 常见编程错误（合并前提）；父子元素合并 图5-20；任务5-6 代码5-10 |
| 144 | 图5-21；多个子元素合并规则；父子合并的特定条件 |
| 145 | 阻止合并技巧；5.4 背景；语法5-3 background-color；语法5-4、5-5 |
| 146 | 代码5-11 background-repeat 四取值 → 图5-22 |
| 147 | 图说；引出 background-position；图5-23 坐标系；语法5-6；表5-11 起始 |
| 148 | 表5-11 续（偏移量、x% y%）；代码5-12 background-position |
| 149 | 图5-24；x% y% 原理（图5-25）；引出 background-size（2048px 图标 vs 300px 容器） |
| 150 | 2 倍图/3 倍图；语法5-7 background-size；表5-12；代码5-13 |
| 151 | 图5-26 contain 与 cover 对比；渐变背景引出（健康 App 图5-27）；语法5-8 |
| 152 | 图5-27；任务5-7 制作健康打卡渐变背景 代码5-14 |
| 153 | 图5-28 完成效果；常见编程错误（`>` 实体等）；语法5-9 attachment；代码5-15 |
| 154 | 代码5-15 scroll vs fixed 对比（Lorem 占位文本） |
| 155 | 图5-29/5-30；墙纸与窗帘比喻；CSS3 新增 background-clip / origin；语法5-10 |
| 156 | 代码5-16 背景剪裁属性（bgc-bb / bgc-pb / bgc-cb） |
| 157 | 图5-31 裁剪效果；语法5-11 background-origin；代码5-17 起始 |
| 158 | 代码5-17 续（bgo-bb / bgo-pb / bgo-cb） |
| 159 | 图5-32/5-33 起始定位差异 |
| 160 | 5.4.3 背景综合样式 语法5-12；技巧与常见错误；任务5-8 制作图标（图5-34） |
| 161 | 代码5-18 icon-dot / icon-menu |
| 162 | currentColor 技巧说明；任务5-9 使用精灵图（图5-35） |
| 163 | 代码5-19 精灵图 bdd1～bdd7 坐标 |
| 164 | 图5-36；坐标获取两种方法；5.5 小结；5.6 作业起始 |
| 165 | 作业：选择题、操作题 all_bg.gif 悬停高亮（图5-38）、项目讨论（游戏中的精灵图） |
| 166 | 项目6 扉页：思政课堂（北京冬奥精神）+ 目标 |
| 167 | 6.1 表格：两个作用（图6-1 布局、图6-2 汽车参数） |
| 168 | 表格历史沿革 → 回归数据呈现；6.2 表格标签；表6-1；th vs td |
| 169 | 图6-3 对应关系；表6-2 caption 属性；thead/tbody/tfoot；表6-3 表格属性 |
| 170 | 表6-4 行属性；表6-5 单元格属性；HTML5 仅保留 colspan/rowspan；任务6-1 起始 |
| 171 | Emmet `table>tr*7>td*4`；代码6-1 金牌榜 HTML 结构（7 行 4 列） |
| 172 | 数据填充；`<i>` 而非 `<img>` 的问答；`<table bgcolor border align width>` |
| 173 | `<tr align bgcolor>` 间隔底纹；cellspacing 0→5；cellpadding 0→10 |
| 174 | 6.3 CSS 表格样式属性 表6-6；9 种对齐（图6-10）；vertical-align vs valign；任务6-2 起始 |
| 175 | GoldenMedalRank.txt 问答；Dreamweaver Import Tabular Data（图6-12/6-13） |
| 176 | 导入四步说明；自动生成代码（图6-14）；CSS Designer 新建 style.css；奖牌 18px×17px（图6-18） |
| 177 | 图6-17/6-18；代码6-2 导入后的表格 HTML |
| 178 | 代码6-3 金牌榜 CSS（border-collapse、th:first-child、th i 精灵图） |
| 179 | caption 样式；金银铜坐标 `0 / -18 / -36 -79px`；6.4 表单（图6-19、图6-20） |
| 180 | 表单原理 GET/POST；6.5 表单标签 `<form>` 语法；表6-7 form 属性 |
| 181 | GET vs POST 区别；使用技巧；6.5.1 `<input>` 语法；表6-8 type 属性值 |
| 182 | 文本框 表6-9；密码框；文件域（enctype + POST）；隐藏域 |
| 183 | 单选按钮语法；代码6-4 gender 示例（图6-21） |
| 184 | value 与显示文本的区别；HTML5 布尔简化；复选框；代码6-5 航天员多选（图6-22） |
| 185 | 图6-22；同一组 name 相同；`<label>` 两种绑定；常见编程错误（for→id） |
| 186 | 7 提交按钮 / 8 普通按钮 / 9 重置按钮 / 10 图像按钮 |
| 187 | 图像按钮说明；任务6-3 `<input>` 综合示例（图6-23/6-24） |
| 188 | 代码6-6 登录表单 + deluser() onclick |
| 189 | size/placeholder 说明；6.5.2 `<button>` 标签 语法；代码6-7 |
| 190 | 图6-25；input 与 button 对比；6.5.3 select（图6-26 列表框、图6-27 下拉列表）；列表框语法 |
| 191 | multiple 说明；name/value 问答；代码6-8 列表框（神舟六号题） |
| 192 | 代码6-8 结构；2. 下拉列表 语法；代码6-9（双奥城市题） |
| 193 | 图6-29/6-30；6.5.4 `<textarea>`（图6-31）；语法；代码6-10 |
| 194 | 图6-32；默认文字 vs placeholder 问答；6.5.5 表单新属性：form 属性 |
| 195 | form 属性说明；2. formaction 语法；代码6-11（add/update/delete.do） |
| 196 | 图6-33；3. required 语法；代码6-12 |
| 197 | 图6-34；4. autofocus；5. pattern 正则；代码6-13 |
| 198 | 图6-35/6-36 正则验证；`\d{8}` 与 `^[a-zA-Z]\w{2,7}`；title 提示；6.5.6 表单美化 |
| 199 | 如何查看表单默认样式；表6-10 常见表单标签默认样式与重置；任务6-4 起始（图6-37） |
