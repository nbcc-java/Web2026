# 《网页制作（HTML5+CSS3）》结构化备课笔记（C段：项目7–项目10）

- 源文件：`网页制作教材/book_all.txt`
- 读取范围：第 13051 行 ～ 文件末尾（第 25895 行）
- 对应 PDF 页码：**第 200 页 ～ 第 324 页**
- 覆盖内容：项目7 浮动和定位、项目8 Flex 布局、项目9 过渡和动画、项目10 多媒体应用
- 说明：正文均忠于教材原文摘录；凡属"整理者补充/勘误提示"的内容，一律以【备课提示】标注，便于课件取舍。教材表格中的个别写法（如 `flex-around`、`form5`）为原文/导出文本呈现，已原样保留并加提示。

---

# 项目7 浮动和定位（PDF 第 210–259 页）

## 7.0 项目概览

**项目名**：项目7 浮动和定位

**思政课堂（原文要点）**
> 以 Web 前端技术为代表的网页应用技术可以帮助乡村地区宣传本地特色和文化，吸引游客前来观光旅游，促进经济发展。同时，网页应用技术还可以为乡村地区提供数字化服务，如在线教育、医疗等，提高乡村地区居民的生活质量。未来，随着互联网技术的不断发展，网页应用技术将更加深入地应用于美丽乡村建设中，为乡村地区带来更多发展机遇和可能性。

**学习目标（照抄要点）**
- 了解网页布局排版的概念
- 掌握标准流排版的相关概念
- 掌握浮动排版的相关概念
- 掌握浮动排版的特性
- 使用 BFC 解决高度塌陷的问题
- 掌握 position 属性
- 掌握固对定位、绝定定位、相对定位的特性（原文如此）
- 熟练应用定位技巧实现网页布局特效

**技能目标**
- 能使用浮动和清除浮动
- 能正确使用固定定位
- 能正确使用绝对定位
- 能正确使用相对定位

**素养目标**
- 培养正确的审美观念
- 培养严谨求实的劳动作风
- 培养精益求精的工匠精神

---

## 7.1 网页布局简介

### 7.1.1 标准流

**技术要点**
- 网页布局要解决的问题：一个网页如何排列分布这些盒子，从而达到美观的排版。
- CSS2 提供 3 种盒子排版模型：**标准流排版、浮动排版、定位排版**；CSS3 新增 **Flex 排版、网格排版** 等。
- 标准流亦称**文档流、普通流**，是元素的**默认排版方式**。

**教材关键解释**
> 标准流是指元素在排版布局过程中，会默认按照自左而右、自上而下的方式流式排列。当前面的内容位置发生变化时，后面的内容位置也会随之发生变化。具体而言，多个元素根据定义顺序形成盒子序列，同级块级盒子按照自上而下的方式，同级行内元素按照自左而右的方式进行排列。对于子元素亦是如此，整个页面犹如河流一样不断分支，并向同一个方向流动，故而称其为"标准流"。**浮动排版和定位排版都是通过更改元素的默认排版方式实现的。**

---

### 7.1.2 浮动排版

**技术要点**
- 浮动靠 CSS2 的 `float` 属性实现。
- 当 `float` 值为 `left` 或 `right` 时，元素变成浮动元素，**同时脱离标准流**。
- 浮动框向左/右移动，直到它的外边缘碰到**父容器的边框（包含框）或另一个浮动框的边框**为止。
- 由于浮动框不在标准流中，标准流中的块框表现得就像浮动框不存在一样。

**表7-1 float 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| none | 默认值，不浮动，按照标准流排列元素 |
| left | 向左浮动，元素浮动在父元素的左侧 |
| right | 向右浮动，元素浮动在父元素的右侧 |
| inherit | 继承父元素的 float 属性值 |

---

#### 任务7-1 浮动特性1：脱离标准流（PDF 212–214）

- **任务名**：浮动特性1：脱离标准流
- **任务目标**：使用 `float` 属性，将"框1"盒子向右浮动，比较浮动前、后的效果（图7-2、图7-3）。
- **核心代码（代码7-1，关键片段）**

```css
.outer{ border:1px dashed #969696; }
.box{
    background-color:#FAFAF1;
    border:1px dashed #373734;
    width:50px; height:50px; margin:10px;
}
.box1{ float:right; }
```

```html
<div class="outer">
  <div class="box box1">框1</div>
  <div class="box">框2</div>
  <div class="box">框3</div>
</div>
```

**教材对效果的解释**
- 浮动前，div 作为块级元素占据父容器 `div.outer` 的一整行。
- 浮动后，box1 向指定方向（右侧）移动，直到外边框碰到父容器的边框为止。
- 依次给"框2""框3"加上 `.box1`：3 个框向右排列成一行；由于子元素脱离，**标准流中的父容器最终塌陷成了一条线**（图7-4、图7-5）。

**浮动特性（教材归纳，4 条，务必照讲）**
1. 浮动可以让块级元素显示在同一行中。
2. 当浮动元素向指定方向移动时，直到它碰到父容器的边框或另一个浮动框为止。
3. 浮动元素会脱离原来的标准流，且不占据原来标准流中的位置和空间。
4. 子元素全部浮动后，如果父容器中没有其他内容撑开高度，则会发生**高度塌陷**。

---

#### 任务7-2 浮动特性2：图文环绕（PDF 214–217）

- **任务名**：浮动特性2：图文环绕
- **任务目标**：验证浮动元素浮于标准流之上/之下，并利用浮动实现图文环绕效果（素材：新疆简介）。
- **易错点/原理（重点讲解）**
  - 实验：把 `.box1` 改成 `float:left` 后，"框1"似乎把顶替上来的"框2"遮挡了，"框2""框3"被挤到下一行并重叠（图7-6）。
  - 用开发者工具选中"框2"可见："框2"隐藏在"框1"之下，但**"框2"中的文字仍在原来的位置上（第二行）**，并与"框3"重叠（图7-7）。
  - **元素立体两层模型（核心原理）**：HTML 元素在构造时由两层构成，**底层是元素层，其上方是内容层**（文字、图片、视频等）。普通标准流的元素立体层次如图7-8。设置浮动后，该元素脱离标准流、提升层级，"浮"到内容层；后面的元素上移占据浮动元素原有的元素层位置；此时标准流元素的**内容层被挤出来形成环绕效果**（图7-9）。
  - 这正是有些书把浮动称为 **"提升半个层级"** 的原因。图文环绕是**浮动的本质**。

- **核心代码（代码7-2，关键片段）**

```css
.outer{ width:500px; background-color:#F8F4E7; color:#666; padding:5px 10px; }
.outer>img{ width:250px; float:left; padding:5px; }
.outer>p{ text-indent:2em; }
.outer>p.intro::first-letter{ font-size:2em; }
```

```html
<div class="outer">
  <img src="images/xinjiang2.png" alt="新疆地图">
  <p class="intro">新疆位于中国西北角，……</p>
  <p>新疆兼具美景和人文，……</p>
  <p>此外，独具特色的新疆美食更为旅途锦上添花。……</p>
</div>
```

- 教材结论：通过 015 行 `float:left` 将图片设置为向左浮动，图片与段落文字处于相同层，其余文字被挤到图片周围，形成图文环绕。

---

#### 任务7-3 浮动特性3：浮动对行内元素的影响（PDF 217–218）

- **任务名**：浮动特性3：浮动对行内元素的影响
- **任务目标**：把研究对象从 div 换成 span，观察浮动对行内元素的特性。
- **核心代码（代码7-3）**

```css
.outer{ border:1px dashed #969696; }
.outer span{ border:1px dashed #373734; background-color:#FAFAF1; width:50px; height:50px; }
.fl{ float:left; }
```

```html
<div class="outer"><span>行内1</span><span>行内2</span></div>
```

- **观察结论**
  - 浮动前：`width`、`height` 对行内元素**不起作用**，宽高由文字内容决定（图7-11）。
  - 给"行内2"加 `.fl` 后："行内2"突然变大，`width`/`height` 起作用了；同时排在后面的"行内2"向左浮动后被排到左边，原本前面的"行内1"被挤到右边（图7-12）。

**浮动作用于行内元素的特性（2 条）**
1. 会使行内元素具有块级元素的特征，又称"**块级格式化上下文**"。
2. 行内元素在立体空间中与文字同属内容层，会受到浮动影响被挤出原有位置。

---

### 7.1.3 清除浮动

**技术要点**
- 父容器失去高度的现象形象地称为**高度塌陷**（图7-13）。
- 清除浮动使用 `clear` 属性。

**表7-2 clear 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| left | 元素左侧不允许有浮动元素 |
| right | 元素右侧不允许有浮动元素 |
| both | 元素两侧不允许有浮动元素 |
| none | 默认值，元素两侧允许有浮动元素 |
| inherit | 继承父元素的 clear 属性值 |

**清除浮动示例（代码7-4，修改任务7-1，以右浮动为例）**

```css
.box1{ float:right; }
.clr{ clear:right; }
```

```html
<div class="outer">
  <div class="box box1">框1</div>
  <div class="box clr">框2</div>   <!-- 对浮动元素后的元素使用 clear -->
  <div class="box ">框3</div>
</div>
```

- 对右浮动用 `clear:right`；对左浮动用 `clear:left`；左、右浮动都有时用 `clear:both`。

**技巧（教材原文，清除浮动的前提条件和要点，3 条）**
1. 具有 clear 属性的元素**必须是块级元素**。
2. 具有 clear 属性的元素**必须与浮动元素是同级元素（兄弟关系）**。
3. 设置 clear 属性的目的是**清除标准流元素上方的浮动元素对自身的影响**。

---

#### 任务7-4 使用清除浮动解决父容器高度塌陷的问题（PDF 221–223）

- **任务名**：使用清除浮动解决父容器高度塌陷的问题
- **任务目标**：用清除浮动的样式属性和规则，解决父容器高度塌陷。
- **思路**：在浮动元素之后添加一个空白行，让它承担清除浮动的工作（图7-16）。

**方案一：加空 div（代码7-5）**

```html
<div class="outer">
  <div class="box box1">框1</div>
  <div class="box box1">框2</div>
  <div class="box box1">框3</div>
  <div class="clr"></div>      <!-- .clr{ clear:right; } -->
</div>
```

- 教材评价：能达成目的（图7-17），但**在 HTML 中添加了不具有语义功能的 `<div class="clr"></div>`**；页面中大量用到浮动时，这类无意义代码会相应增加。

**方案二：用 `::after` 伪元素（代码7-6，推荐）**

```css
.clr::after{
    content:"";
    display:block;
    clear:right;
}
```

```html
<div class="outer clr">
  <div class="box box1">框1</div>
  <div class="box box1">框2</div>
  <div class="box box1">框3</div>
</div>
```

- **易错点（教材原话）**：因为 `::after` 伪元素默认是一个**行内元素**，所以根据清除浮动的前提条件，**必须将其 display 设置为 block**；同时需要满足添加的内容为空，可通过 `content:""` 实现。
- 举一反三：清除其他方向或两侧浮动，只需修改 clear 的属性值。

---

### 7.1.4 使用 BFC 解决高度塌陷的问题

**技术要点**
- **BFC（Block Formatting Context，块级格式上下文）**：使用浮动的元素将生成 BFC，它为元素提供了一个**独立的布局环境**，该环境中的内容不会影响外部的布局，外部的布局同样也不会影响该环境中的内容。**"如同围墙，围墙内的东西出不去，围墙外的东西进不来。"**
- 解决高度塌陷的第二个思路：**给父容器加上一个围墙（BFC）**，围墙能包含浮动元素，使之无法脱离父容器区域，从而达到清除浮动的效果。

#### 任务7-5 触发 BFC 的 3 种常用方式（PDF 223–227）

- **任务名**：触发 BFC 的 3 种常用方式
- **任务目标**：用设置 `inline-block`、设置父元素浮动、设置 `overflow` 属性 3 种方式触发 BFC，解决父容器高度塌陷。

**方式1：设置 `display:inline-block` 触发 BFC（代码7-7）**

```css
.outer{ border:1px dashed #969696; display:inline-block; }
.box{ background-color:#FAFAF1; border:1px dashed #373734; width:50px; height:50px; margin:10px; }
.fr{ float:right; }
.fl{ float:left; }
```

```html
<div class="outer">
  <div class="box fr">框1</div>
  <div class="box fr">框2</div>
  <div class="box fl">框3</div>
</div>
```

- 原理解释：触发 BFC 后，每个行内块元素都具有"**包裹性**"，当其中存在浮动元素时，能包裹住内部的浮动元素，起到类似清除浮动的效果（图7-18）。

**方式2：设置父元素浮动触发 BFC（代码7-8）**

```css
.outer{ border:1px dashed #969696; float:left; }
/* .box / .fr / .fl 同上 */
```

- **注意事项（教材原文）**：给父元素设置浮动属性后，父元素具有 BFC，可以包裹住浮动的子元素，**但同样也会影响自身和其他元素**。所以解决高度塌陷的方法很多，每种方法都有其自身的特点和优缺点，需要根据具体情况来选择合适的方法。（图7-19）

**方式3：设置 `overflow` 属性值触发 BFC（代码7-9）**

```css
.outer{ border:1px dashed #969696; overflow:hidden; }
/* .box / .fr / .fl 同上 */
```

- 触发规则：**当把父元素的 overflow 属性值设置为除默认值之外的值时会触发该元素的 BFC**，故可设为 `scroll | hidden | auto`。（图7-20）

**表7-3 overflow 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| visible | 默认值，溢出的内容不会被裁剪，会显示在元素框之外 |
| hidden | 溢出的内容会被隐藏 |
| scroll | 溢出的内容会被隐藏，不管内容是否溢出，浏览器都会显示滚动条 |
| auto | 由浏览器决定是否显示滚动条，如果内容溢出了，则显示滚动条，否则不显示 |
| inherit | 继承父元素的 overflow 属性值 |

- 补充（教材原话）：目前看到 3 种触发 BFC 的方式，其实还可以**通过绝对定位等其他方式触发 BFC**。

---

## 7.2 定位简介

**引入（教材原文要点）**
> 如果说通过浮动可以解决平面空间的排版问题，那么通过定位则可以让元素向纵深方向（z 轴）发展，形成层级叠加的现象。网页应用和移动应用中的各种弹窗、对话框等效果需要定位功能的支持……定位让页面呈现出丰富的交互效果。

### 7.2.1 定位属性

**技术要点**
- 元素需要 `position` 属性，并配合 `left`、`right`、`top`、`bottom` 定位属性达到定位目的。
- 纵向空间的叠加现象，通过 `z-index` 调整层叠顺序。

**表7-4 position 属性值及描述（完整还原）**

| 属性值 | 描述 |
|---|---|
| static | 默认值，静态定位，元素按照标准流进行布局 |
| fixed | 固定定位，依据浏览器视口进行偏移 |
| absolute | 绝对定位，将对象从标准流中脱离出来，相对于其最近的一个已定位元素（相对/绝对的祖先元素）进行绝对定位；如果不存在这样的祖先元素，则相对于最外层的包含框（body）进行定位 |
| relative | 相对定位，相对于自身位置进行偏移 |

**表7-5 定位属性值及描述（完整还原）**

| 属性值 | 描述 |
|---|---|
| left | 元素左边的偏移量，可取负值 |
| right | 元素右边的偏移量，可取负值 |
| bottom | 元素下边的偏移量，可取负值 |
| top | 元素上边的偏移量，可取负值 |

**表7-6 z-index 属性值及描述（完整还原）**

| 属性值 | 描述 |
|---|---|
| auto | 默认值，层级与父元素相等 |
| number | 指定元素的层级高低。数值越大，层级越高 |
| inherit | 继承父元素的 z-index 属性值 |

**必须记住的 3 点（教材原文）**
1. 常用的定位有 **static 静态定位、fixed 固定定位、absolute 绝对定位、relative 相对定位** 4 种；
2. `left`、`right`、`bottom`、`top` 是 4 个 CSS 属性，也被称为定位属性，可以和 relative、absolute、fixed 属性配合使用，实现坐标定位的效果；
3. 如果定位的元素发生空间上的重叠，则可以通过 `z-index` 实现层级的切换，数值越大，层级越高，**如同 PPT"排列"选项中"前移一层"的效果**。

---

### 7.2.2 静态定位

**技术要点**
- `position:static` 或不设置 position 时，元素默认静态定位。
- 元素按标准流布局：块级元素从上往下依次排列，行内元素和行内块元素从左往右依次排列，**各元素没有任何移动效果**。
- 之前示例代码都使用静态定位，教材不再举例。

---

### 7.2.3 固定定位

**技术要点**
- 企业背景：京东商城页面中的**固定侧边栏**（图7-21），不管页面滚动到哪里，侧边栏始终出现在页面相同位置。
- 定义：固定定位是**相对于浏览器视口（可视窗口）**进行定位的，位置固定，**不会随着网页滚动条的滚动而移动**。
- **固定定位的实现步骤**：① 修改定位属性；② 通过 left、right、bottom、top 固定位置。
- **启发问答知识点**：要用定位属性定位，至少需要几个定位属性？→ **由于元素基于盒子模型，在水平方向和垂直方向上至少各需要一个定位属性。**

#### 任务7-6 使用固定定位实现导航悬停（PDF 229–233）

- **任务名**：使用固定定位实现导航悬停
- **任务目标**：根据固定定位语法和链接锚点知识，实现页面导航悬停效果。
- **素材/企业背景**：正文为新华社报道《建设宜居宜业美丽乡村——权威解读〈乡村建设行动实施方案〉》（图7-22），配合 `.outer` 容器 + `.toolbar` 固定工具栏（回到顶部 / 建什么 / 怎么建 / 建成什么样）。

**核心代码（代码7-10，关键片段）**

```css
.outer{ width:512px; border:1px solid #ccc; margin:0 auto; padding:20px; background-color:#fafbfc; }
.outer img{ width:100%; }
.toolbar{
    position:fixed;
    right:10px;
    top:100px;
}
.toolbarItem{ background-color:bisque; border-top:1px dashed #ccc; }
.toolbarItem>a{ text-decoration:none; display:inline-block; padding:5px 10px; color:#F8534D; }
.toolbarItem>a:hover{ text-decoration:underline; }
```

```html
<div class="outer" id="top">
  <h2>建设宜居宜业美丽乡村——权威解读《乡村建设行动实施方案》</h2>
  <img src="./images/meili01.jpeg" alt="">
  …
  <h3 id="sec01">建什么？加强重点领域农村基础设施建设</h3>
  …
  <h3 id="sec02">怎么建？坚持乡村建设是为农民而建</h3>
  …
  <h3 id="sec03">建成什么样？不搞大拆大建，保留乡村风貌</h3>
  …
</div>
<div class="toolbar">
  <div class="toolbarItem"><a href="#top">回到顶部</a></div>
  <div class="toolbarItem"><a href="#sec01">建什么</a></div>
  <div class="toolbarItem"><a href="#sec02">怎么建</a></div>
  <div class="toolbarItem"><a href="#sec03">建成什么样</a></div>
</div>
```

- **实现说明**：对 `.toolbar` 使用 `position:fixed`，配合 `right`、`top` 定位到页面相应位置。这样无论怎么滚动滚动条，该导航都脱离普通标准流，悬停在视口的相应位置上。
- 素材图片：`meili01.jpeg`～`meili06.jpg`。

---

### 7.2.4 绝对定位

**技术要点（定义）**
- 绝对定位是指**相对于距离最近的已定位祖先元素**进行的定位。如果元素没有已定位祖先元素，那么它的位置**相对于浏览器**进行定位。
- 两种情况：① 上下文中存在已定位祖先元素；② 不存在这样的已定位祖先元素。

**核心代码（代码7-11，不存在已定位祖先元素的情况）**

```css
.outer{ background-color:#01FFFF; }
.box{ width:100px; height:50px; background-color:#FFE4C4; border:1px dashed #518F93; }
.box2{ position:absolute; left:20px; top:40px; }
```

```html
<div class="outer">
  <div class="box">div1</div>
  <div class="box box2">div2</div>
  <div class="box">div3</div>
</div>
```

- 效果对比：图7-23（未使用绝对定位）→ 图7-24（使用绝对定位）。
- 本例中 `div.outer` 与 `body` 均未加定位，属于"不存在已定位祖先元素"的情况：div2 脱离标准流，被定位到**距离浏览器左边界 20px、上边界 40px** 的位置。
- 补充实验：如果只设置绝对定位而没有 left、top 配合，元素会在原来的位置上，**但会脱离标准流**；注释掉宽度后，**不设置宽度、绝对定位后，元素宽度由内容撑开**（图7-25）。

**绝对定位的特性（教材归纳，5 条）**
1. 脱离原来的标准流，并提升层级。
2. 如果在其祖先元素中有已定位元素，则就近进行绝对定位；如果不存在这样的祖先元素，则根据浏览器进行绝对定位。
3. 可以使行内元素支持宽度、高度和内边距、外边距等样式效果。
4. 当块级元素不设置宽度时，其宽度由内容撑开。
5. **可以触发 BFC**。

**技巧（fixed vs absolute，教材原文）**
> 固定定位是相对于视口的，这意味着即使滚动页面，元素也会固定保持在同一个位置上；而绝对定位与此不同，如果不存在已定位祖先元素，则它是相对于浏览器窗口进行定位的。选择时可牢记：如果页面垂直方向超过一个屏幕，则使用绝对定位后，拖动滚动条，绝对定位元素会随着文档一起滚动，而固定定位元素则始终显示在原有位置上。

---

### 7.2.5 相对定位

**技术要点**
- 相对定位是指元素**相对于自身原始位置**进行偏移的定位，偏移量由 `top`、`right`、`bottom`、`left` 实现；未指定时默认值为 0。

**核心代码（代码7-12）**

```css
.outer{ background-color:#01FFFF; }
.box{ width:100px; height:50px; display:inline-block; margin:5px;
      background-color:#FFE4C4; border:1px dashed #518F93; }
.box2{
    position:relative;
    /* left:20px;
       top:40px; */
}
```

```html
<div class="outer">
  <div class="box">div1</div>
  <div class="box box2">div2</div>
  <div class="box">div3</div>
</div>
```

- 图7-26：不设置偏移量的相对定位，和静态定位似乎没区别；打开注释后见图7-27。
- 结论：不设置偏移量，元素仍位于标准流中的原位置；设置偏移量后，最终位置相对于原来标准流中的位置偏移；从 div2 与 div3 的遮挡关系可看出**相对定位的层级比标准流的层级高**。

**相对定位的特性（教材归纳，4 条）**
1. 如果只设置相对定位，不设置偏移量，则相对定位元素的位置不会有任何变化。
2. 元素设置相对定位后**仍然占据其原有空间，不会脱离标准流**。
3. 元素设置相对定位后会**提升其层级**，与原有标准流元素形成遮挡关系。
4. 在配合定位属性时，元素的偏移位置**相对于原来元素在标准中的位置**。

**"已定位元素"概念（承上启下，重要）**
- 相对定位不脱离标准流，其他元素不受影响，仍按原位置排列；相对定位元素会提升一个层级，并具有**由自身偏移量计算的参考系**，这就可以使其成为一个**已定位元素**——"就好像拥有一个局部坐标系来定义它的子元素，其所有子元素在定位时将参考这个局部坐标系。"
- 启发问答：除了相对定位，还有哪些元素属于已定位元素？→ **除了默认的静态定位，父元素使用绝对定位、相对定位、固定定位都属于已定位情况。** 此时子元素使用绝对定位，使用的是父元素的局部坐标系。

---

#### 任务7-7 精品课程封面的制作（PDF 238–241）

- **任务名**：精品课程封面的制作（素材文件名 `JavaCourse`）
- **任务目标**：使用"**父元素的相对定位 + 子元素的绝对定位**"技巧，实现快速局部区域定位，完成精品课程封面（图7-28）。
- **案例参数**：`.outer` 宽 300px；`.course .img-wrap` 高 162px；右上角标签 `div.tag` 宽 120px、`#4c98ff`、白字、居中、`rotate(45deg)`、14px；课程名"Java 程序设计"；年份 2021 + "秋"；"正在开课" + 人数 472；教师"郑哲"，学校"宁波城市职业技术学院"。

**核心代码（代码7-13，关键片段）**

```css
.outer{ width:300px; }
.course{ width:100%; position:relative; overflow:hidden; }        /* ① 父相 */
.course:hover{ box-shadow:0 1px 5px 1px rgb(62,62,62,0.3); }
.course .img-wrap{ height:162px; overflow:hidden; }
.course img{ max-width:100%; transition:all 0.6s; }
.course img:hover{ transform:scale(1.3); }

div.tag{
    width:120px; background-color:#4c98ff; color:#fff; text-align:center;
    position:absolute; right:-22px; top:26px;                     /* ② 子绝 */
    transform:rotate(45deg); font-size:14px;
}
.course-term,.course-status,.teacher-school{
    font-size:13px; color:#333; padding:0px 15px;
    display:flex; justify-content:space-between;
}
.title{ font-weight:800; }
.term-year{ background:url("images/autumn.svg") no-repeat left top; width:66px; height:20px; line-height:20px; }
.year{ color:#dc5704; font-size:14px; font-weight:400; padding-left:10px; }
.term{ color:white; padding:3px; font-size:13px; }
.status{ color:blue; }
.course-status img{ max-width:16px; margin-right:5px; }
.teacher{ display:flex; align-content:center; }
.teacher img{ max-width:16px; margin-right:5px; }
```

```html
<div class="outer">
  <div class="course">
    <div class="img-wrap"><img src="./images/cover.png" alt=""></div>
    <div class="tag"><span class="title">省级精品</span></div>
    <p class="course-term">
      <span class="title">Java 程序设计</span>
      <span class="term-year"><span class="year">2021</span><span class="term">秋</span></span>
    </p>
    <p class="course-status">
      <span class="status">正在开课</span>
      <span class="num"><img src="images/people.png" alt="">472</span>
    </p>
    <p class="teacher-school">
      <span class="teacher"><img src="images/teacherHeader.png" alt=""><span class="t-name">郑哲</span></span>
      <span class="school">宁波城市职业技术学院</span>
    </p>
  </div>
</div>
```

- **教材解析**：右上角"省级精品"标注即"父相对 + 子绝对"的局部坐标系快速定位。012 行 `position:relative` 构建已定位祖先元素；035 行子元素指定绝对定位，通过 top、right 置于右上角；038 行用 `transform` 的 `rotate()` 实现 45 度旋转。
- **启发问答**：`scale()`、`transition` 是什么？→ transform 是变形属性，提供 `scale()`、`rotate()`、`translate()` 等函数；transition 用于实现过渡效果。**将在项目9 中讲述，这里先模仿代码，学完项目9 再体会。**

**技巧（教材原文）**
> 利用"父元素的相对定位 + 子元素的绝对定位"的技巧可实现局部坐标系内的快速定位效果。

- 素材清单：`cover.png`、`autumn.svg`、`people.png`、`teacherHeader.png`。

---

## 7.3 综合案例

### 任务7-8 圣杯布局（PDF 241–247）

- **任务名**：圣杯布局
- **任务目标**：三列布局，左列固定 150px、右列固定 200px，中间列宽度自适应（图7-29）。
- **背景（教材原文）**：圣杯布局源于一篇文章"**In Search of the Holy Grail**"。"圣杯"在西方文字中是"渴求之物"的意思。
- **实现思路（4 步）**
  1. **HTML 结构上把 `.main` 放在最前**（优先渲染中间列，往往是页面主要部分）。
  2. 三列全部 `float:left`，`.main` 宽度 100% 自适应填满父容器（图7-30）。
  3. **margin 负值**把左右两列拉上来：`.left{margin-left:-100%;}`、`.right{margin-left:-202px;}`（图7-31）。
     - 易错点：`-202px` 的原因——**除自身宽度 200px 外，还需加上两侧边线宽度各 1px**。
  4. 给 `.outer` 设置 `padding-left:150px; padding-right:200px;` 腾出位置（图7-32），再用**相对定位**把左右列推到位：`.left{position:relative; left:-150px;}`、`.right{position:relative; right:-200px;}`（图7-33）。
  5. 可将 3 列高度都设为 `height:100%`，填满满屏，得到更完整的圣杯布局（图7-34）。

**完整代码（代码7-15）**

```css
html{ height:100%; }
body{ margin:0; /*去除默认外边距*/ height:100%; }
.outer{ margin:0 auto; /*居中*/ height:100%; padding-left:150px; padding-right:200px; }
.main{ float:left; width:100%; /*自适应填满父容器的宽度*/ height:100%; background-color:#FFE4C4; }
.left{ float:left; width:150px; height:100%; background-color:#01FFFF;
       border:1px dashed #518F93; margin-left:-100%; position:relative; left:-150px; }
.right{ float:left; width:200px; height:100%; background-color:#01FFFF;
        border:1px dashed #518F93; margin-left:-202px; position:relative; right:-200px; }
```

```html
<div class="outer">
  <div class="main">main-content</div>
  <div class="left">left-column</div>
  <div class="right">right-column</div>
</div>
```

---

### 任务7-9 双飞翼布局（PDF 247–249）

- **任务名**：双飞翼布局
- **任务目标**：实现图7-35 的三列效果（左 150px、右 200px、中间自适应）。
- **背景（教材原文）**：双飞翼布局源于**淘宝的 UED**，灵感来自页面渲染，将左、右两列的固定列宽比喻成小鸟的两个翅膀，是对页面的形象表示，**通常认为它是圣杯布局的改进版**。
- **关键差异**：在 `main` 元素上**再添加一层 div（`.main-wrap`）并给它设置 margin 值**。由于左右两列的 margin 负值都是相对于 main-wrap 元素的，main 元素的 margin 值变化不会影响它们，因此**省略了对左右两列设置相对定位的步骤**。

**核心代码（代码7-16）**

```css
html,body{ height:100%; margin:0; }
.main-wrap { float:left; width:100%; background-color:#FFE4C4; height:100%; }
.left      { float:left; width:150px; margin-left:-100%; background-color:#01FFFF; height:100%; }
.right     { float:left; width:200px; margin-left:-200px; background-color:#01FFFF; height:100%; }
.main      { margin:0 200px 0 150px; }
```

```html
<div class="main-wrap">
  <div class="main">main-content</div>
</div>
<div class="left">left-column</div>
<div class="right">right-column</div>
```

- **对比总结（教材原文）**：双飞翼布局的精髓和圣杯布局一样，都是通过设置 **margin 负值** 实现元素布局。不同点在 HTML 结构：双飞翼在 main-wrap 内部又设置一层 main 元素并设置它的左右 margin；而圣杯布局是通过 **padding 属性** 消除两边元素的覆盖。**两种布局原理基本一样，关键在于设置 margin 负值的技巧和元素浮动的相对定位技巧。**

---

### 任务7-10 绝对居中布局（PDF 249–253）

- **任务名**：绝对居中布局
- **任务目标**：模拟元素绝对居中效果（案例图：**图7-36 淘宝 App**、**图7-37 美团 App**）；假设对话框宽度和高度分别为 200px、300px（教材此处表述），代码中使用 300px×400px。
- **关键思路**：让元素水平或垂直居中，就要使元素的中心与父元素的中心重合；**父容器尺寸不固定**（如不同手机尺寸），所以不能用相对父容器的具体数值定位，**可以考虑使用百分比**。

**第一步：绝对定位 + 百分比（代码7-17）**

```css
html,body{ margin:0; height:100%; }
.outer{ background-color:#FFE4C4; height:100%; }
div.mask{ position:absolute; left:0; top:0; width:100%; height:100%;
          opacity:0.3; background-color:#000; }      /* 半透明遮罩 */
.dialog{ width:300px; height:400px; position:absolute; top:50%; left:50%; }
.dialog img{ width:100%; }
```

```html
<div class="outer">
  <div class="dialog"><img src="./images/dialog-img.png"></div>
  <div class="mask"></div>
</div>
```

- **易错点（重点）**：此时对话框**没有真正居中**（图7-38）。原因：**对话框是相对于左上角进行偏移定位的**（图7-39）。

**第二步：margin 负值 + z-index（代码7-18，完整代码）**

```css
.dialog{ width:300px; height:400px; position:absolute; top:50%; left:50%;
         margin-top:-200px; margin-left:-150px; z-index:999; }
```

- 教材解释：`margin` 负值取**自身宽高的一半**；对话框也会受遮罩影响，可通过 `z-index` 调整两者顺序（图7-41）。

---

### 任务7-11 京东秒杀模块的制作（PDF 254–258）

- **任务名**：京东秒杀模块的制作
- **任务目标**：使用定位等相关知识完成京东秒杀模块（图7-42）。
- **模块参数（便于还原）**
  - 容器 `.container`：`overflow:hidden`（触发 BFC 并裁切）。
  - `.item`：`float:left; width:190px; height:275px; border:1px solid #eee;`
  - 秒杀块 `.ms`：`background-color:#e83632; color:#fff; text-align:center;`
  - `.ms .title`：`font-size:34px; margin:15px;`（"京东秒杀"）
  - `.ms .subtitle`：`font-size:20px; color:rgba(255,255,255,0.5); margin-bottom:10px;`（"FLASH DEALS"）
  - `.ms .icon`：`width:20px; height:33px; display:block; background-image:url("./images/sprite.seckill.png"); background-position:-35px -25px; margin:0 auto 20px;`（**雪碧图定位**）
  - `.ms .desc`：`font-size:16px; margin:10px;`（"本场距离结束时间"）
  - `.ms .clock span`：`display:inline-block; width:40px; height:40px; background-color:#2f3430; font-size:20px; line-height:40px;`（23 / 59 / 20）
  - `.product-link`：`display:block; height:100%; text-align:center; padding-top:39px;`
  - `.product-desc`：`white-space:nowrap; width:160px; overflow:hidden; text-overflow:ellipsis; margin:0 auto;`（**单行省略号三件套**）
  - `.price`：`width:160px; height:20px; background-color:#e6382f; margin:20px auto; padding:1px;`
  - `.price span`：`width:78px; height:20px; font-size:14px; display:inline-block;`
  - `.price .price-new`：`line-height:20px; color:#fff;`
  - `.price .price-origin`：`color:#b7bcb8; background-color:#fff;`
  - 全局：`*{ margin:0; padding:0; font:12px/1.5 "微软雅黑",Tahoma,Arial,Harrington,"sans-serif" }`；`a{color:#666}`、`a:hover{color:#c81623}`。

**核心代码（代码7-19，关键片段）**

```css
.container{ overflow:hidden; }
.item{ float:left; width:190px; height:275px; border:1px solid #eee; }
.ms{ background-color:#e83632; color:#fff; text-align:center; }
.ms .icon{ width:20px; height:33px; display:block;
           background-image:url("./images/sprite.seckill.png");
           background-position:-35px -25px; margin:0 auto 20px; }
.product-desc{ white-space:nowrap; width:160px; overflow:hidden; text-overflow:ellipsis; margin:0 auto; }
```

```html
<div class="container">
  <div class="item ms">
    <h2 class="title">京东秒杀</h2>
    <h3 class="subtitle">FLASH DEALS</h3>
    <i class="icon"></i>
    <p class="desc">本场距离结束时间</p>
    <div class="clock"><span class="hour">23</span><span class="minute">59</span><span class="second">20</span></div>
  </div>
  <div class="item">
    <a href="#" class="product-link">
      <img src="./images/pic01.jpg">
      <p class="product-desc">合生元(BIOSTIME)儿童婴幼儿益生菌冲剂…</p>
      <div class="price"><span class="price-new">138.00</span><span class="price-origin">208.00</span></div>
    </a>
  </div>
  <!-- 共 4 个商品 item：pic01~pic04，价格 138.00/208.00、1599.00/2899.00、2097.00/4380.00、155.00/176.00 -->
</div>
```

- 商品文案素材：合生元益生菌、索尼 WH-1000XM2 耳机、艾戈勒手表、合生元益生菌粉（26 袋装）。

---

## 7.4 小结（原文要点）

> 浮动和定位常用于网页的个性化布局中，是静态网页制作中非常重要的概念。通过本项目的学习，我们可以掌握与浮动和定位相关的知识，同时需要重点掌握网页的标准流特性、浮动的相关特性及清除浮动的常用方法。7.2 节介绍了静态定位、固定定位、绝对定位、相对定位的特性及应用案例，我们需要熟练掌握它们的特性及常用的应用写法，以为后续复杂页面布局打好基础。

## 7.5 作业（可作课堂练习/题库）

**一、选择题**
1. 京东商城页面侧边栏不随滚动条滚动而变化，使用了（ ）。A．固定定位 B．相对定位 C．绝对定位 D．静态定位
2. 标准流中的默认定位是（ ）。A．固定定位 B．相对定位 C．绝对定位 D．静态定位
3. 浮动最初的用途是（ ）。A．制作导航 B．实现图文混排 C．解决父容器高度坍塌的问题 D．影响行内元素的尺寸
4. 关于浮动，说法错误的是（ ）。
   A．浮动元素会脱离原来的标准流
   B．不论是块级元素还是行内元素，只要是浮动元素都可以指定其宽度、高度
   C．不论是块级元素还是行内元素，只要是非静态元素都可以指定其宽度、高度
   D．通过对浮动元素设置 overflow 属性值可以触发 BFC
5. 将父容器设置为相对定位，下面关于子元素的说法中正确的是（ ）。
   A．如果将子元素设置为绝对定位，则该元素相对于该父容器进行定位
   B．如果将子元素设置为绝对定位，则该元素始终相对于浏览器窗口进行定位
   C．只有绝对定位元素才能配合使用 left、right、bottom、top 定位属性
   D．如果将子元素设置为固定定位，则该元素相对于父容器进行固定

**二、操作题**：根据图7-44 所示效果，制作一个登录框，并使用定位将其居中显示。

**三、项目讨论**：使用所学知识，以**美丽乡村**为主题，帮助你所在的城市设计和规划一个网页。试讨论你的做法、思路及特点！

---

# 项目8 Flex 布局（PDF 第 260–287 页）

## 8.0 项目概览

**项目名**：项目8 Flex 布局

**思政课堂（原文要点）**
> 网页应用技术是当今数字化时代的重要组成部分，它与 ChatGPT、AIGC 等技术的结合，为各行业带来了巨大的变革。ChatGPT 和 AIGC 等技术通过自然语言处理和机器学习算法实现了更加智能化的交互体验，而网页应用技术则为这些技术提供了展示和应用的平台，使得它们能够更好地服务于各领域。随着技术的不断发展，网页应用技术将与 ChatGPT、AIGC 等技术更加紧密地结合，为各行业带来更加智能、高效的应用体验。

**学习目标**
- 了解 Flex 布局的基本概念
- 掌握 Flex 布局的特点
- 掌握 Flex 容器的相关属性
- 掌握常用的 Flex 布局技巧
- 掌握 Flex 子项的使用方法

**技能目标**
- 能正确使用 Flex 布局实现主轴元素布局控制
- 能正确使用 Flex 布局实现交叉轴元素布局控制
- 能应用 Flex 样式属性调整子项样式

**素养目标**
- 培养精益求精的工匠精神
- 培养勇于探索、崇尚科学的学习品质
- 培养高尚的审美情趣

---

## 8.1 Flex 布局简介

**技术要点**
- Flex 是 **flexible box** 的缩写，意为"弹性布局"，是一种对元素进行**按行或按列**布局的常用布局手法，**常被理解为一种一维布局手法**。
- 使用 Flex 布局的元素可以通过相应的 **grow** 样式属性来抓取填充额外的容器空间；也可以通过 **shrink** 样式属性在容器窗口收缩时得到合适的收缩效果。**这正是弹性布局的要义。**
- 图示：容器窗口从 100px 到 300px 横向扩展（图8-1）时，元素1、元素3 大小不变，由元素2 扩展所有额外空间；纵向扩展（图8-2）同理。

---

## 8.2 Flex 布局的相关术语

**技术要点（图8-3，术语务必讲清）**
- **Flex 容器（flex container）**：采用 Flex 布局的元素，简称"容器"；它的所有子元素被称为 **Flex 子项（flex item）**，简称"子项"。
- **主轴（main axis）**：默认情况下子项沿主轴**横向**排列，左侧为**主轴起点（main start）**，右侧为**主轴结束点（main end）**。
- **交叉轴（cross axis）**：与主轴正交的轴，默认**起点（cross start）在上、终点（cross end）在下**。
- **main size**：每个子项占据主轴空间的宽度；**cross size**：占据交叉轴空间的宽度。

---

## 8.3 Flex 容器

**启用方式（语法）**

```css
display:flex;         /* 块级元素 */
display:inline-flex;  /* 行内元素 */
```

**良好的编程习惯（教材原文）**

```css
.box{
    display:-webkit-flex;  /* Safari */
    display:flex;
}
```

- 对于 WebKit 内核的浏览器，可以通过加上 `-webkit` 前缀来实现兼容性。
- **特别注意（易错点）**：当设置了 Flex 布局之后，子元素的 **`float`、`clear`、`vertical-align` 等样式属性将失效**。

### 8.3.1 Flex 容器的相关属性

**表8-1 Flex 容器常见的 6 个属性（完整还原）**

| 属性名 | 描述 |
|---|---|
| flex-direction | 调整布局方向（指定主轴的方向） |
| flex-wrap | 控制是否换行 |
| flex-flow | 综合样式属性，是 flex-direction 属性和 flex-wrap 属性的组合 |
| justify-content | 定义主轴对齐方式 |
| align-items | 定义交叉轴对齐方式 |
| align-content | 定义多根轴线的对齐方式，如果只有一根轴线，则该属性不起作用 |

#### 8.3.1.1 flex-direction 属性

**语法8-1**

```
flex-direction: row | row-reverse | column | column-reverse
```

- `row`：主轴在水平方向上**自左向右**布局；`column`：主轴在垂直方向上**自上而下**布局；加了 `-reverse` 的属性值会产生**逆向**的布局方式（图8-4）。

#### 8.3.1.2 flex-wrap 属性

**表8-2 flex-wrap 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| nowrap | 默认值，不换行 |
| wrap | 换行，当子项在父容器中宽度不足时自动换行 |
| wrap-reverse | 逆向换行，换行方向与轴方向相反 |

- 实验过程（子项为 50px×50px 正方形）：
  - 父容器宽度大于 300px 时，所有子项**排列在一根轴线上**，正常显示（图8-5）。
  - 容器宽度小于 250px（不足以显示 50px×5）时，**子项并不会换行，而是弹性地缩小其水平空间的尺寸**，每个子项实际宽度都不足 50px（图8-5）。
  - 要保持子项原有尺寸，设置 `flex-wrap:wrap`（图8-6）。
  - 默认换行方向为交叉轴正方向（自上而下），`flex-wrap:wrap-reverse` 为逆方向（自下而上）（图8-7）。

#### 8.3.1.3 flex-flow 属性

**语法8-2**

```
定义语法：flex-flow: [flex-direction] || [flex-wrap]
示例：flex-flow: column wrap-reverse;
```

- 默认属性值为 **row nowrap**。

#### 8.3.1.4 justify-content 属性

**语法8-3**

```
定义语法：justify-content: flex-start | flex-end | center | space-between | space-around;
示例：justify-content: space-around;
```

**表8-3 justify-content 属性值（完整还原，含教材原文写法）**

| 属性值 | 描述 |
|---|---|
| flex-start | 子项在主轴上对齐起点（main-start） |
| flex-end | 子项在主轴上对齐结束点（main-end） |
| center | 子项沿主轴朝容器的中心对齐 |
| flex-around | 子项在主轴上平均分布，首、尾两项与父容器两侧也有一定的间隔（记为 A），子项之间有均匀的间隔（记为 B），**B 通常是 A 的两倍** |
| flex-between | 子项在主轴上平均分布，**首、尾两项紧贴父容器** |

> 【备课提示】表8-3 后两项在导出文本中写作 `flex-around`、`flex-between`，而语法8-3 与后文任务（如任务8-3 均分列布局、任务8-4 组合嵌套布局）使用的是 `space-around`、`space-between`。建议课件中按 **`space-around` / `space-between`** 讲解，并提示此处为教材表格排版笔误。

- 效果见图8-8。

#### 8.3.1.5 align-items 属性

**语法8-4**

```
定义语法：align-items: flex-start | flex-end | center | baseline | stretch;
示例：align-items: stretch;
```

**表8-4 align-items 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| flex-start | 与交叉轴的起点对齐 |
| flex-end | 与交叉轴的终点对齐 |
| center | 与交叉轴的中心对齐 |
| baseline | 与子项文字基线对齐 |
| stretch | **默认值**，如果子项未设置高度或设置为 auto，则占满整个父容器的高度 |

- **特别注意**：`align-items` 默认值是 `stretch`，当子项没有设置高度时，默认占满整个父容器高度（图8-9）。

#### 8.3.1.6 align-content 属性

**语法8-5**

```
定义语法：align-content: flex-start | flex-end | center | space-between | space-around | stretch;
示例：align-content: center;
```

**表8-5 align-content 属性值（完整还原）**

| 属性值 | 描述 |
|---|---|
| flex-start | 多轴子项与交叉轴的起点对齐 |
| flex-end | 多轴子项与交叉轴的终点对齐 |
| center | 多轴子项与交叉轴的中点对齐 |
| space-between | 多轴子项与交叉轴的两端对齐，轴线之间的间隔平均分布 |
| space-around | 多轴子项在交叉轴上平均分布，首、尾两项与父容器两侧也有一定的间隔（记为 A），子项之间有均匀的间隔（记为 B），**B 通常是 A 的两倍** |
| space-evenly | 多轴之间的间隔相等（即全部平均分配） |
| stretch | **默认值**，轴线占满整个交叉轴 |

---

### Flex 容器启发式问答（关键知识点）

1. **为什么 align-content 默认值 stretch 在图8-10 中看不到拉伸效果？**
   → 要让默认值 stretch 起作用，**一定要确保 Flex 容器中的子项没有指定高度**（图8-11）。
2. **align-items 与 align-content 有何区别？何时用哪个？**
   → **`align-items` 针对每个交叉轴进行设置，`align-content` 针对多轴的内容进行整体设置。** 例如 5 个子项构成的两行：`align-items:flex-start` 是让**每一行**的元素对齐到**该行交叉轴空间**的起始位置（两行默认平均分配交叉轴空间）；`align-content:flex-start` 是把**多轴整体**对齐到交叉轴空间的起始位置（图8-12）。
3. **只有一根轴线时两者效果是否一样？**
   → 效果一样（4 个子项时 align-items 会把所有交叉轴空间给该子项），但**代码实现上仍有区别**：align-content 用于对多轴内容进行处理，**一定要配合 `flex-wrap` 换行**，这样才有多轴内容，才会起作用。

**常见的编程错误（教材原文）**
> 仅使用 align-content 属性而不配合使用 flex-wrap 属性往往达不到预期的应用效果，这是一种常见的编程错误。

---

### 8.3.2 居中布局

#### 任务8-1 块级元素居中布局（PDF 268–270）

- **任务名**：块级元素居中布局
- **任务背景**：随着人工智能技术不断发展，以 **ChatGPT** 为代表的人工智能产品、AI 绘图应用不断推出。某在线商城发布了一款智能绘图产品，实现图8-13 的块级元素居中效果（素材 `./images/AI_01.png`）。
- **三种实现方案（课堂对比重点）**

**方案1：Flex 布局（代码8-1）**

```css
div{ display:flex; border:1px solid #ccc; background-color:#eee;
     align-items:center; justify-content:center; width:300px; height:300px; }
div>img{ height:90%; }
```

```html
<div><img src="./images/AI_01.png" alt=""></div>
```

**方案2：表格单元格（代码8-2）**

```css
div{ display:table-cell; border:1px solid #ccc; background-color:#eee;
     vertical-align:middle; text-align:center; width:300px; height:300px; }
div>img{ height:90%; }
```

- 类比 Word 中的单元格对齐方式（图8-14）：配合 `text-align` 实现水平居中，配合 `vertical-align` 实现垂直居中。

**方案3：定位 + translate()（代码8-3）**

```css
div{ position:relative; border:1px solid #ccc; background-color:#eee; width:300px; height:300px; }
div>img{ position:absolute; left:50%; top:50%; height:90%; transform:translate(-50%,-50%); }
```

#### 任务8-2 不定项居中布局（PDF 270–271）

- **任务名**：不定项居中布局
- **任务背景**：轮播图底部的导航按钮个数不确定（3 张图 3 个按钮，5 张图 5 个按钮），但始终位于底部居中（图8-15）。
- **思路**：把导航按钮看成一个整体；013 行 `justify-content` 使它们整体居中；014 行 `align-items` 将其置于交叉轴结束位置（底部）。

**核心代码（代码8-4）**

```css
.wrap{ width:500px; height:200px; background-color:antiquewhite; border:1px solid #eee;
       display:flex; justify-content:center; align-items:flex-end; }
.wrap>li{ justify-content:center; background-color:#999; width:20px; height:20px;
          line-height:20px; text-align:center; border-radius:50%; color:white;
          list-style:none; margin:5px 10px; }
```

```html
<ul class="wrap">
  <li class="item">1</li><li class="item">2</li><li class="item">3</li>
</ul>
```

#### 任务8-3 均分列布局（PDF 272–273）

- **任务名**：均分列布局
- **任务背景**：**城市学院网站**的均分列布局（图8-16）：4 列均匀横向分布在主轴空间，每列显示一个图标和一段说明文字。
- **思路**：把"图标 + 说明文字"看成一个整体，即为典型的一维横向布局；用 `justify-content: space-between` 实现均分。
- **参数**：`.wrap` 540px×153px，白底、`padding:0 30px`、`border-radius:6px`、`margin:0 auto`、`align-items:center`；`.wrap>.item` 91px×120px 居中；`.item>img` 宽 35px；`.item>p` 20px。

**核心代码（代码8-5）**

```css
body{ background-color:#dee9fb; }
.wrap{ width:540px; height:153px; background-color:white; border:1px solid #eee;
       margin:0 auto; display:flex; justify-content:space-between; align-items:center;
       padding:0 30px; border-radius:6px; }
.wrap>.item{ width:91px; height:120px; text-align:center; }
.item>img{ width:35px; }
.item>p{ font-size:20px; }
```

```html
<div class="wrap">
  <div class="item"><img src="./images/nbcc-icon01.png" alt=""><p>学校官网</p></div>
  <div class="item"><img src="./images/nbcc-icon02.png" alt=""><p>校务服务</p></div>
  <div class="item"><img src="./images/nbcc-icon03.png" alt=""><p>办公系统</p></div>
  <div class="item"><img src="./images/nbcc-icon04.png" alt=""><p>教务系统</p></div>
</div>
```

#### 任务8-4 组合嵌套布局（PDF 273–276）

- **任务名**：组合嵌套布局
- **任务背景**：**大美新疆首页的导航栏**，包括 logo、导航、分享按钮、登录按钮、注册按钮（图8-17）。
- **思路（教学要点）**：在实际开发页面中，并不是所有容器子项都能以均匀方式布局。**方法很简单，就是把不熟悉的页面布局转换为熟悉的基本页面布局。** 利用**组合思想**：把左侧 logo + 导航看成一个整体，把右侧分享 + 登录 + 注册看成另一个整体（图8-18），整体即 `justify-content:space-between` 的典型特征。

**核心代码（代码8-6）**

```css
.wrap{ width:1024px; height:60px; background-color:white; border:3px solid #eee;
       padding:0 60px; margin:0 auto; display:flex;
       justify-content:space-between; align-items:center; }
.lft{ display:flex; align-items:center; border:2px solid #ccc; }
.lft>img{ width:70px; }
.nav{ margin:0 0 0 30px; padding:0 10px; width:350px; height:60px; line-height:60px;
      list-style:none; display:flex; justify-content:space-between; align-items:center; }
.nav li{ width:70px; height:60px; text-align:center; line-height:60px; }
.nav li:nth-child(1){ background-color:#ff9d00; color:white; }
.rt{ width:210px; display:flex; border:2px solid #ccc; }
.share{ display:flex; margin-right:20px; align-items:center; justify-content:space-between; }
.login{ color:#ff9d00; }
```

```html
<div class="wrap">
  <div class="lft">
    <img src="./images/logo.png" alt="" class="logo">
    <ul class="nav">
      <li class="item">首页</li><li class="item">旅游</li>
      <li class="item">人文</li><li class="item">关于我们</li>
    </ul>
  </div>
  <div class="rt">
    <div class="share">
      <img src="./images/icon5.png" alt="">
      <img src="./images/icon6.png" alt="">
      <img src="./images/icon7.png" alt="">
    </div>
    <div class="login">登录|注册</div>
  </div>
</div>
```

- 素材：`logo.png`、`icon5.png`、`icon6.png`、`icon7.png`；导航项：首页 / 旅游 / 人文 / 关于我们。

---

## 8.4 Flex 子项

**表8-6 Flex 子项样式属性（完整还原）**

| 属性名 | 描述 |
|---|---|
| order | 定义子项的排列顺序。数值越小，顺序越靠前，默认值为 0 |
| flex-grow | 定义子项的放大比例。默认值为 0，表示如果存在剩余空间，则子项不放大 |
| flex-shrink | 定义子项的缩小比例。默认值为 1，表示如果空间不足，则子项将缩小 |
| flex-basis | 定义在分配剩余空间之前子项在主轴中的空间大小。浏览器根据这个属性计算主轴是否有剩余空间。默认值为 auto，即子项的本来大小 |
| flex | 综合样式属性，是 flex-grow、flex-shrink 和 flex-basis 属性的简写，默认值为 `0 1 auto` |
| align-self | 允许单个子项有与其他子项不一样的对齐方式，可覆盖 align-items 属性。默认值为 auto，表示继承父元素的 align-items 属性，如果没有父元素，则等同于 stretch |

**综合示例（代码8-7，关键片段）**

```css
.wrap{ display:flex; border:2px solid #f00; height:50px; margin:50px auto; }
.item{ width:200px; border:1px solid #000; text-align:center; }
.gr1 { flex-grow:1; }
.sk0 { flex-shrink:0; }
.als { align-self:flex-end; flex-grow:0; }
.base{ flex-basis:300px; }
```

```html
<div class="wrap">
  <div class="item gr1">grow=1</div>
  <div class="item sk0">shrink=0</div>
  <div class="item als">align-self=flex-end</div>
</div>
<div class="wrap">
  <div class="item base">flex-base=300px</div>
  <div class="item base">flex-base=300px</div>
</div>
```

**实验观察（课堂演示要点）**
- 宽度 601px 时：3 个子项均有足够横向空间；因 `align-items` 默认 `stretch`，前两个子项占满父容器高度；带 `.als`（`align-self:flex-end`）的子项**底部对齐**（图8-19）。
- 宽度 801px 时：多出来的额外空间**完全被 grow=1 的子项占据**，其余两个子项宽度不变（图8-20）。
- 宽度缩小到 400px 时：grow=1 的子项与设置了 align-self 的子项实际宽度已小于 200px，而 **`flex-shrink:0` 的子项始终保持宽度不变**（图8-21）。

**启发问答：为什么用 flex-basis 而不是 width？**
- `width` 通常用于固定宽度；在 Flex 布局中，**flex-basis 描述的是子项在主轴中的空间大小**。如果父容器超过所有子项的 flex-basis 总和，说明有额外空间，就会根据子项的 grow 属性计算并分配这些额外空间。因此**在 Flex 布局中常使用 flex-basis 而非 width**。
- 同时使用会怎样？→ 代码8-7 中 `.item` 指定 `width:200px`，`.base` 指定 `flex-basis:300px`，最终显示 **300px**（图8-22）。→ **`flex-basis` 的优先级高于 `width`。**
- 补充细节：图8-22 中实际宽度显示为 **302px**，因为子项宽度 300px 加上左、右各 1px 的边框宽度。

---

### 任务8-5 Flex 布局案例：轮播图的制作（PDF 279–285）

- **任务名**：轮播图的制作
- **任务目标**：制作图8-23～图8-25 的轮播图效果，将 `images/pic1.png～pic3.png`（代码中使用 `pic01.jpg～pic03.jpg`）显示在指定区域；轮播图底部放置 **3 个分页指示器**用于指定当前播放的图片；轮播区域**左右各一个控制器按钮**（上一张 / 下一张）。**注意：不要求实现播放的效果和按钮触发事件。**
- **整体思路（教材原文）**：从整体上看由 3 部分构成——**存放 3 张图片的幻灯片容器、分页指示器、控制器按钮**。先构造幻灯片容器结构（图8-26），再构造分页指示器（3 个行内元素，图8-27），最后用 `<a>` 标签实现控制器按钮（图8-28）。

**核心代码（代码8-8）**

```css
.swiper-container{ position:relative; background-color:#FFE4C4; }
.swiper-wrapper{ display:flex; transition:0.5s; transform:translateX(0px);
                 animation: move-slide 10s ease-in-out infinite; }
.swiper-slide{ width:100%; flex-shrink:0; /*不收缩，溢出布局*/ }
.swiper-slide img{ width:100%; }

.swiper-pagination{ position:absolute; height:28px; width:100%; bottom:40px;
                    display:flex; justify-content:center; align-items:center; }
.swiper-pagination-bullet{ width:12px; height:12px; border-radius:50%;
                           background-color:#c6bcaf; margin:0 4px; }
.swiper-pagination-bullet-active{ background-color:#fff; }

.swiper-button-prev,.swiper-button-next{ position:absolute; top:0%; height:100%;
                                         display:flex; align-items:center; }
.swiper-button-prev{ left:10px; }
.swiper-button-next{ right:10px; }
.swiper-button-next span,.swiper-button-prev span{ font-size:22px; color:#fff; }

@keyframes move-slide {
  0%,10%,100%{ transform: translateX(0px); }
  20%,40%   { transform: translateX(-500px); }
  60%,80%   { transform: translateX(-1000px); }
}
```

```html
<div class="swiper-container">
  <div class="swiper-wrapper">
    <div class="swiper-slide"><img src="./images/pic01.jpg" alt=""></div>
    <div class="swiper-slide"><img src="./images/pic02.jpg" alt=""></div>
    <div class="swiper-slide"><img src="./images/pic03.jpg" alt=""></div>
  </div>
  <div class="swiper-pagination">
    <span class="swiper-pagination-bullet swiper-pagination-bullet-active"></span>
    <span class="swiper-pagination-bullet"></span>
    <span class="swiper-pagination-bullet"></span>
  </div>
  <a class="swiper-button-prev" href="#">
    <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span></a>
  <a class="swiper-button-next" href="#">
    <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span></a>
</div>
```

- 头部引入：`<link rel="stylesheet" href="css/reset.css">`、`<link rel="stylesheet" href="css/bootstrap.min.css">`、`<meta name="viewport" content="width=device-width, initial-scale=1">`。

**溢出布局（代码8-9，重要）**

```css
.swiper-container{ position:relative; background-color:#FFE4C4; }
.swiper-wrapper{ display:flex; }
.swiper-slide{ width:100%; flex-shrink:0; /*不收缩，溢出布局*/ }
```

- 教材说明：对 `.swiper-wrapper` 使用 Flex 布局后，子元素 `.swiper-slide` 需要**溢出到父容器外**，这是通过 `width:100%` + `flex-shrink:0` 实现的。**通常，这种布局形式被称为"溢出布局"。**

**其他要点**
- 028～046 行：用 Flex 布局把 3 个分页指示器放在幻灯片底部中间。
- 047～063 行：用**绝对定位**把两个控制器按钮分别放在距左、右两侧 **10px** 的水平位置，并用 `align-items:center` 使其垂直居中。
- **Bootstrap Glyphicons 字体图标**（3 步）：① 导入 Bootstrap 的 CSS 样式（代码8-8 第 009 行）；② 在项目中放入**字体文件夹**和 Bootstrap 样式（图8-30）；③ 对照 Glyphicon Halflings 字体图标，在标签中使用相应样式，如"<"图标对应 `glyphicon glyphicon-chevron-left`，">"对应 `glyphicon glyphicon-chevron-right`。该字体图标包含 **250 多个** Glyphicon Halflings 图标（图8-29）。
- **调试技巧**：开发者工具 → "移动设备查看模式"（图8-31）→ "尺寸"右侧下拉 → "修改"（图8-32）→ "添加自定义设备"，名称"调试"，尺寸 **500 像素 × 700 像素**（图8-33）→ 在设备下拉列表中选择该自定义设备（图8-34）。之所以取 500px 宽，是为了便于计算滑动偏移量（0 / -500px / -1000px）。
- 017～019 行与 065～075 行（transition / transform / animation / @keyframes）用于实现自动滑动动画，**项目9 将详细介绍**。

---

## 8.5 小结（原文要点）

> 本项目介绍了 Flex 布局的原理及 Flex 容器的相关属性，详细介绍了这些属性的使用特性。我们需要熟练掌握 Flex 的常用布局，以及各属性的配套使用方法，从而能够熟练地制作出常见的 Web 前端页面布局效果。

## 8.6 作业

**一、选择题**
1. （ ）不是 flex-direction 属性值。A．row B．row-reverse C．column D．both
2. 要实现 Flex 布局元素自动换行，应该添加（ ）属性。A．flex-direction B．flex C．flex-wrap D．flex-grow
3. 关于下面语句描述正确的是（ ）。
   `div:nth-of-type(1){flex-grow:1;} div:nth-of-type(2){flex-grow:3;} div:nth-of-type(3){flex-grow:1;}`
   A．div3 的尺寸是 div1 的 3 倍
   B．div2 的尺寸是 div1 和 div3 的 3 倍
   C．在扩展布局范围时，div2 获得的空间是 div1 和 div3 的 3 倍
   D．在收缩布局范围时，div2 获得的空间是 div1 和 div3 的 3 倍
4. 关于 Flex 布局，说法错误的是（ ）。
   A．Flex 布局也叫弹性布局，可以在扩展、收缩页面时自动调整布局
   B．使用 flex-direction:row 可以快速实现横向导航布局效果
   C．在默认情况下，flex-direction 属性值是 column
   D．Flex 布局是主要用于单行（列）的布局
5. 在均分列布局中，设置（ ）不是必要操作。
   A．display:flex; B．justify-content:space-between; C．align-items:center; D．flex-shrink:0;

**二、操作题**：以**慕课 App 中"我的课程"界面**为例（图8-35），利用所学布局知识实现该界面的布局效果。

**三、项目讨论**：在移动应用快速发展的今天，通过慕课 App 学习成为一种免费、高效的学习方式。请结合自身经历和感受：① 举例说明信息技术是如何助力教育教学发展的？② 网页制作技术在这些技术发展中有哪些作用和体现？③ 在未来的教育新技术条件下，作为新一代技术的应用开拓者，你有什么新想法？

---

# 项目9 过渡和动画（PDF 第 288–314 页）

## 9.0 项目概览

**项目名**：项目9 过渡和动画

**思政课堂（原文要点）**
> 互联网的**迭代开发思想**是工匠精神的一种体现，这种思想强调在开发过程中不断进行反馈和改进，追求产品的完美和极致。在每一次迭代过程中，开发人员不断优化和改进产品，逐步完善产品的功能和性能，以满足用户的需求和期望。这种不断追求卓越的精神正是工匠精神的体现。在现代社会，工匠精神已经成为许多行业所追求的核心价值。无论是软件工程师、设计师还是其他领域的专业人才，都需要具备这种精益求精的精神，只有这样才能创造出更加优秀的产品。

**学习目标**
- 掌握 CSS3 2D 变换的相关概念
- 掌握 CSS3 3D 变换的相关概念
- 掌握 CSS3 过渡语法及其应用
- 掌握 CSS3 动画语法及其应用
- 掌握循环动画的制作技巧

**技能目标**
- 能使用 CSS3 过渡语法实现过渡效果
- 能使用 CSS3 动画语法实现 2D 动画效果
- 能使用 CSS3 动画语法实现 3D 动画效果
- 能使用 CSS3 动画语法实现循环动画效果

**素养目标**
- 培养精益求精的工匠精神
- 培养勇于探索、崇尚科学的意志和品德
- 培养严谨求实的学习态度

---

## 9.1 变换

**技术要点**
- 变换（transform）是 CSS3 的新样式属性之一，允许对元素进行**旋转（rotate）、扭曲（skew）、缩放（scale）、平移（translate）、矩阵变形（matrix）** 等，从而实现 2D 变换或 3D 变换。
- **基本语法**：`transform: none | transform-functions;`
  - `none` 表示没有变换；`transform-functions` 表示**一个或多个**变换函数。

---

## 9.2 2D 变换

**坐标系（图9-1）**
- CSS3 的 2D 变换基于 2D 图形坐标系：原点 (0,0) 在**元素的左上角**，每个点使用一组 (x, y) 构建的**笛卡儿坐标系**。
- **x 轴向右为正方向，y 轴向下为正方向。**

**表9-1 常用的 2D 变换函数（完整还原）**

| 2D 变换函数 | 描述 |
|---|---|
| `translate(tx,ty)` | 包含两个参数值，分别指定 x 轴和 y 轴的平移量。根据左侧（x 轴）和顶部（y 轴）位置给定的参数，从当前元素位置开始移动 |
| `rotate(ra)` | 包含一个角度参数，用于指定元素**顺时针**旋转的角度。参数值为负表示元素**逆时针**旋转的角度 |
| `scale(sx[,sy])` | 包含两个参数值，第一个表示 x 轴方向的缩放值，第二个表示 y 轴方向的缩放值。如果第二个参数值为空，则 y 轴方向的缩放值等于 x 轴方向的缩放值 |
| `skew(ax[,ay])` | 包含两个参数值，分别表示 x 轴和 y 轴倾斜的角度。如果第二个参数值为空，则默认值为 0。参数值为负表示向相反方向倾斜 |
| `matrix(a,b,c,d,tx,ty)` | 以包含 6 个值的转换矩阵的形式指定 2D 变换。其中，a、b、c、d 用于描述线变换，tx 表示水平偏移，ty 表示垂直偏移 |

（教材原表另有"效果示例"列，为各函数的效果图示。）

**单轴变换函数**
```
translateX()、translateY()、scaleX()、scaleY()、skewX()、skewY()
```

**复合变换（重点、易错点）**
- CSS3 支持对同一元素进行多个变换函数的复合操作，**多个变换函数之间需要使用空格分隔**：

```
transform: transform-functions1 transform-functions2 …
示例：transform: scale(2.0) translate(10px,20px);
```

> **常见的编程错误（教材原文）**：使用逗号，而不使用空格分隔多个变换函数是一种常见的编程错误。

**综合示例（代码9-1，关键片段）**

```css
.outer{ background-color:#FFE4C4; height:100%; }
.box{ background-color:#01FFFF; width:100px; height:100px;
      display:inline-block; margin:50px; text-align:center; }
.box2{ transform: rotate(45deg); }
.box3{ transform: translate(10px,20px); }
.box4{ transform: scale(2,0.5); }
.box5{ transform: skew(30deg,20deg); }
.box6{ transform: matrix(1,0.2,-1.2,1,0,0); }
```

```html
<div class="outer">
  <div class="box1 box">box1</div> … <div class="box6 box">box6</div>
</div>
```

（运行效果见图9-2。）

---

### 变换轴心 transform-origin

**技术要点**
- 缩放、扭曲的变换轴心默认在**盒子的中心**。
- 语法：`transform-origin: x y;` —— **属性值 x 和 y 之间使用空格分隔。**
- 未指定 x y 时，默认变换轴心是元素的中心点 **50% 50%**，也可用 `center center` 等价替换。
- x y 还可以是具体像素或 CSS3 预定义方位值（**top、bottom、left、right、center**）。

```
transform-origin: 50px 50px;
transform-origin: left bottom;
```

**代码9-2（将变换轴心调整至左上角，图9-3）**

```css
.outer{ display:inline-block; background-color:#FFE4C4; height:300px; width:500px; position:relative; }
.box{ background-color:#01FFFF; width:100px; height:100px; display:inline-block;
      margin:50px; text-align:center; position:absolute; }
.box2,.box4{ opacity:0.3; transform:scale(2); }
.box4{ transform-origin: top left; }
```

- 教材解析：023～026 行用 `scale()` 将 box2、box4 放大 2 倍并增加半透明效果；默认轴心在盒子中心（box2），028 行将缩放点定位至左上角，得到 box4 的效果。

---

## 9.3 3D 变换

**3D 立体坐标系（图9-4）**
- **x 轴**：水平向右为正值，反之为负值；
- **y 轴**：垂直向下为正值，反之为负值；
- **z 轴**：**垂直屏幕，向外为正值，向内为负值**。

**表9-2 常用的 3D 变换函数（完整还原）**

| 3D 变换函数 | 描述 |
|---|---|
| `translate3d(tx,ty,tz)` | 定义 3D 平移，相应的参数值为在相应轴方向上的平移量 |
| `rotate3d(rx,ry,rz,angle)` | 定义 3D 旋转，angle 为绕相应轴方向的旋转角度 |
| `scale3d(sx,sy,sz)` | 定义 3D 缩放，相应的参数值为相应轴方向上的缩放值 |
| `matrix3d(a1,b1,c1,d1,a2,b2,c2,d2,a3,b3,c3,d3,a4,b4,c4,d4)` | 以包含 16 个值的 4×4 转换矩阵的形式指定 3D 变换。其中 a1…d3 表示线性变换，a4、b4、c4、d4 表示平移 |
| `perspective(length)` | 指定透视距离，即观察者与 z=0 平面的距离，从而使元素产生透视效果。当 z>0 时，3D 元素比正常的元素大，而当 z<0 时，3D 元素比正常的元素小，其大小程度由该属性值决定 |
| `perspective-origin(x,y)` | 定义透视关系中消失点的坐标，可以使用方向预设值 |
| `transform-style(flat\|preserve-3d)` | flat：所有子元素在 2D 平面中呈现，**默认值**；preserve-3d：所有子元素在 3D 空间中呈现 |
| `backface-visibility(visible\|hidden)` | 设置当元素背面朝向观察者时是否可见 |

**关键说明**
- 3D 变换函数大都以"**\*3d**"的形式命名，与 2D 变换函数相区别；3D 变换函数是在 2D 变换函数基础上增加了一个 z 轴方向。
- 通常为了让元素的子元素在 3D 空间中呈现，**需要先将 `transform-style` 属性值设置为 `preserve-3d`**。
- `perspective()` 函数用于指定在透视关系中，观察者与平面的距离。

**透视原理（启发问答，图9-5、图9-6）**
> perspective 是指观察者与平面的距离，其值越大，就好像距离屏幕越远，物体看起来就越小；其值越小，表示距离越近，就好像凑到屏幕前，物体看起来就越大。
> 通过 `translateZ()` 将矩形向 z 轴方向移动，可以让物体看起来比原本大；在保持 perspective 不变的前提下，减小 translateZ 值，其在绘制平面上的实际大小会缩小。这就实现了透视关系中**近大远小**的效果。

**perspective 的两种写法**
```css
/* （1）指定父元素：设置在 3D 渲染元素的共同父元素上 */
.parent{ perspective:800px; }

/* （2）指定子元素：设置在当前 3D 渲染元素上，与 transform 属性写在一起 */
.parent .sub{ transform: perspective(800px) rotate(45deg); }
```
- 教材预告：**任务9-5 将演示以"指定子元素"的方式实现卡片翻转动画。**

**perspective-origin（消失点，图9-7～图9-9）**
- 用于指定消失点的位置，**默认值为 `center center`**，也可用 `50% 50%` 代替；将透视线延长，所得焦点就是消失点。
- 设为 `left top` 时效果如图9-8；不同取值对比见图9-9。
- **注意：如果用户只给定一个值，则另一个值取默认值 center。**

**backface-visibility**
- 作用是设置元素背面是否可见（图9-10 为 visible / hidden 的效果对比）。

---

### 任务9-1 制作 3D 骰子（PDF 297–299）

- **任务名**：制作 3D 骰子
- **任务目标**：利用 3D 变换知识，制作图9-11 的 3D 骰子效果，**正方体尺寸为 100px×100px**。
- **参数**：`.outer` 400px×200px、`padding:50px`、`#FFE4C4`；`#dice` 100px×100px、`margin:0 auto`、`transform-style:preserve-3d`、`perspective:800px`、`perspective-origin:bottom center`、`transform:rotate3d(1,1,0,332deg)`；`.face` 用 Flex 居中、`position:absolute`、`backface-visibility:inherit`、`font-size:60px`、`color:#fff`。

**核心代码（代码9-3）**

```css
#dice{
    width:100px; height:100px; margin:0 auto;
    transform-style:preserve-3d;
    perspective:800px;
    perspective-origin:bottom center;
    transform:rotate3d(1, 1, 0, 332deg);
}
.face{
    display:flex; align-items:center; justify-content:center;
    width:100%; height:100%; position:absolute;
    backface-visibility:inherit; font-size:60px; color:#fff;
}
.front { background:rgba(90,90,90,0.7);   transform:translateZ(50px); }
.back  { background:rgba(0,210,0,0.7);    transform:rotateY(180deg) translateZ(50px); }
.right { background:rgba(210,0,0,0.7);    transform:rotateY(90deg)  translateZ(50px); }
.left  { background:rgba(0,0,210,0.7);    transform:rotateY(-90deg) translateZ(50px); }
.top   { background:rgba(210,210,0,0.7);  transform:rotateX(90deg)  translateZ(50px); }
.bottom{ background:rgba(210,0,210,0.7);  transform:rotateX(-90deg) translateZ(50px); }
```

```html
<div class="outer">
  <div id="dice">
    <div class="face front">1</div>
    <div class="face back">2</div>
    <div class="face right">3</div>
    <div class="face left">4</div>
    <div class="face top">5</div>
    <div class="face bottom">6</div>
  </div>
  <h3></h3>
</div>
```

**教材解析（实现思路，务必照讲）**
- 018～020 行对 3D 骰子的父容器设置 3D 透视相关样式：透视距离 **800px**，消失点为**底部中间（bottom center）**，并用 `rotate3d()` 沿 x 轴、y 轴旋转 **332 度**。
- 每个面由 `.face` 定义，用 Flex 布局将内容居中。
- 正面（front）用 `translateZ()` 向正方向平移 **50px**（骰子边长 100px 的一半）；背面（back）向负方向平移 50px，为让前面朝外需**沿 y 轴旋转 180 度**；左面（left）平移后旋转 **−90 度**；右面（right）平移后旋转 **90 度**。

---

## 9.4 过渡

**技术要点（定义）**
> 过渡（transition）样式规则能够让你定义元素在**两种状态之间切换**的过渡效果。常用的例子：通过给同一个元素应用 `:hover` 伪类和 `:active` 伪类，并定义不同的样式，从而实现过渡效果。当然，在学了 JavaScript 之后，也可以通过脚本来实现状态的切换。

**表9-3 常用的过渡样式属性（完整还原）**

| 样式属性名 | 描述 |
|---|---|
| transition-property | 指定 CSS 属性的 name、transition 效果 |
| transition-duration | 指定 transition 效果需要多少秒或毫秒才能完成 |
| transition-timing-function | 指定 transition 效果的转速曲线 |
| transition-delay | 定义 transition 效果开始的时间 |

**综合语法**

```
transition: property duration timing-function delay;
```

---

### 任务9-2 制作简单过渡效果（PDF 300–302）

- **任务名**：制作简单过渡效果
- **任务目标**：创建 div，宽度 100px；鼠标悬停时宽度 300px；实现 **2s 的宽度过渡效果（使用默认动画函数）**（图9-12 默认状态、图9-13 悬停状态）。

**核心代码（代码9-4）**

```css
div{
    background-color:#FFE4C4;
    width:100px;
    padding:20px;
    transition: width 2s;
    -webkit-transition: width 2s;  /* Safari */
}
div:hover { width:300px; }
```

- 教材解析：013 行使用 `-webkit` 前缀是**兼容性写法**（为让 Safari 支持）；010 行设初始宽 100px，`:hover` 处设 300px，使两个状态有明显区别；**最重要的是 012 行**，使用 transition 综合样式属性指定 width 属性执行 2s 过渡变化。

**扩展：多属性过渡（代码9-5，图9-14 → 图9-15）**

```css
div{
    background-color:#FFE4C4; width:100px; padding:20px;
    transition: width ease-in-out 2s, background-color ease-in-out 2s;
    -webkit-transition: width ease-in-out 2s, background-color ease-in-out 2s; /* Safari */
}
div:hover{ width:300px; background-color:#f00; }
```

- 简写技巧：多个样式属性都要过渡时，可用 **all** 代替所有属性：

```css
transition: all ease-in-out 2s;
-webkit-transition: all ease-in-out 2s; /* Safari */
```

> **技巧（教材原文）**：使用 all 代替所有要实现过渡变化的样式属性是一种常用的技巧。
> **常见的编程错误（教材原文）**：将 transition 错拼成 transform 是一种常见的编程错误。

**过渡相关样式属性的初始值（教材给出）**

```
transition-delay: 0s
transition-duration: 0s
transition-property: all
transition-timing-function: ease
```

- 小技巧：可以使用**浏览器开发者工具查看所有预设的动画函数效果**（图9-16），甚至可以自定义动画函数。

---

## 9.5 动画

**技术要点**
- CSS3 中一些样式属性除了可用于过渡，还可以用于创建动画，以此取代许多网页中通过动画图像、Flash 动画和 JavaScript 实现的效果。其原理与过渡非常类似，主要通过具备动画功能的属性实现**从一个值变化到另一个值**（尺寸大小、数量、百分比和颜色变化等）。
- **动画与过渡的最大区别：动画支持自定义关键帧规则。** 关键帧规则通过 **@keyframes** 规则语法定义，通过在动画序列中定义关键帧（waypoints）的样式来控制 CSS 动画序列的**中间步骤**。因此，**动画的可控性要比过渡的可控性高**。

**@keyframes 语法**

```
@keyframes animationname { keyframes-selector { css-styles; } }
```

**示例（教材给出的 rotateDice）**

```css
@keyframes rotateDice {
  0%   { transform: rotate3d(0, 1, 0, 0deg); }
  50%  { transform: rotate3d(0, 1, 0, 180deg); }
  100% { transform: rotate3d(0, 1, 0, 359deg); }
}
```

- 教材解释：按顺序列出关键帧百分比——播放开始（0%）沿 y 轴旋转 0 度；播放到中间（50%）沿 y 轴旋转 180 度；播放结束（100%）沿 y 轴旋转 359 度。

> **技巧（教材原文）**：`0%` 也可以使用预设值 **`from`** 来替代，`100%` 也可以使用预设值 **`to`** 来替代。

**animation 综合语法**

```
animation: name duration timing-function delay iteration-count direction fill-mode;
```

**表9-4 常用的 animation 样式属性（完整还原）**

| 样式属性名 | 描述 |
|---|---|
| animation | 所有动画属性的简写样式属性 |
| animation-name | 规定动画的名称 |
| animation-duration | 规定动画完成一个周期所花费的时间，单位为秒或毫秒。默认值是 0 |
| animation-timing-function | 规定动画的速度曲线。默认值是 ease |
| animation-fill-mode | 规定当不播放动画时（当动画完成播放时，或者当动画有延迟未开始播放时），要应用的元素样式 |
| animation-delay | 规定动画何时开始播放。默认值是 0 |
| animation-iteration-count | 规定动画的播放次数。默认值是 1 |
| animation-direction | 规定动画是否在下一个周期逆向播放。默认值是 normal |
| animation-play-state | 规定动画是否正在播放或暂停。默认值是 running |

**注意事项（教材原文）**
- `animation-name` 所规定的动画名称**必须和前面定义的 @keyframes 动画名称保持一致**。
- `animation-duration`、`animation-timing-function`、`animation-delay` 的用法和过渡样式属性的用法非常类似。

---

### 任务9-3 制作旋转骰子（PDF 304–307）

- **任务名**：制作旋转骰子
- **任务目标**：在任务9-1 基础上，创建自定义动画并命名为 **rotateDice**，利用 @keyframes 规则制作**骰子沿 y 轴旋转**的动画，以 **2s 为一个周期循环播放**（图9-17）。

**核心代码（代码9-6，关键片段）**

```css
@keyframes rotateDice {
  0%   { transform: rotate3d(0, 1, 0, 0deg); }
  50%  { transform: rotate3d(0, 1, 0, 180deg); }
  100% { transform: rotate3d(0, 1, 0, 359deg); }
}
#dice{
    width:100px; height:100px; margin:0 auto;
    transform-style:preserve-3d;
    perspective:800px;
    perspective-origin:center center;      /* 与任务9-1 的 bottom center 不同 */
    animation: rotateDice 2s linear infinite;
}
/* .face / .front / .back / .right / .left / .top / .bottom 与代码9-3 相同 */
```

```html
<div class="outer">
  <div id="dice">
    <div class="face front">1</div><div class="face back">2</div>
    <div class="face right">3</div><div class="face left">4</div>
    <div class="face top">5</div><div class="face bottom">6</div>
  </div>
  <h3></h3>
</div>
```

- 教材解析：013～023 行定义动画，由 3 部分构成——**0% 对应传统动画制作中的起始帧，100% 对应结束帧，50% 对应中间帧**；031 行使用 animation 简写样式属性启用该动画，设置周期为 2s 的**无限循环**。

---

## 9.6 综合案例

### 任务9-4 制作呼吸灯动画（PDF 307–311）

- **任务名**：制作呼吸灯动画
- **任务目标**：由交替的**圆圈1、圆圈2** 构成；圆圈尺寸 **50px×50px**；颜色 **rgb(250,0,0,0.5)**（代码中写作 `rgba(250,0,0,0.5)`）；实现图9-18 的动画效果。
- **分析方法（教学要点）**：制作动画时**先从动画的构造开始分析**，建立关于**时间的动画影像**（图9-19 圆圈1、图9-20 圆圈2）。

**关键帧规则**

```css
@keyframes bounce1{ 0%,100%{ transform:scale(1.0); } 50%{ transform:scale(0); } }
@keyframes bounce2{ 0%,100%{ transform:scale(0.0); } 50%{ transform:scale(1.0); } }
```

**代码9-7（初始实现）**

```css
.ball{ width:50px; height:50px; border-radius:50%; position:absolute;
       top:0; left:0; background-color:rgba(250,0,0,0.5); }
.ball1{ -webkit-animation:bounce1 2s ease-in-out infinite;
        -o-animation:bounce1 2s ease-in-out infinite;
        animation:bounce1 2s ease-in-out infinite; }
.ball2{ -webkit-animation:bounce2 2s ease-in-out infinite;
        -o-animation:bounce2 2s ease-in-out infinite;
        animation:bounce2 2s ease-in-out infinite; }
.outer{ width:200px; margin:0 auto; position:relative; }
```

```html
<div class="outer">
  <div class="ball ball1"></div>
  <div class="ball ball2"></div>
</div>
```

**代码优化（代码9-8，思政结合点：迭代优化/工匠精神）**
- 观察：把 bounce1 与 bounce2 的时间线放在一起，发现它们**运动规律一样，只是存在一个时间差**（图9-21）。
- 优化：只定义一个动画，用 **`animation-delay`** 让第二个延迟执行。

```css
.ball{ width:50px; height:50px; border-radius:50%; position:absolute; top:0; left:0;
       background-color:rgba(250,0,0,0.5);
       -webkit-animation:bounce 2s ease-in-out infinite;
       -o-animation:bounce 2s ease-in-out infinite;
       animation:bounce 2s ease-in-out infinite; }
@keyframes bounce{ 0%,100%{ transform:scale(1.0); } 50%{ transform:scale(0); } }
.ball2{ animation-delay:1s; }
.outer{ width:200px; margin:0 auto; position:relative; }
```

- 教材解析：019～026 行统一定义 bounce 动画；030 行将圆圈2 **延迟 1s**（整个动画执行时长为 2s，此处教材表述为"整个动画执行时长为 1s"，实为半个周期错开）。这样大大减少了代码重复，优化了整体设计。

> **良好的编程习惯（教材原文）**：不断思考如何优化产品，是互联网迭代思维的体现，也是工匠精神的体现。

---

### 任务9-5 制作卡片翻转动画（PDF 312–313）

- **任务名**：制作卡片翻转动画
- **任务目标**：由一个正方形卡片构成，尺寸 **60px×60px**，颜色 **#67cf22**；实现图9-22 的卡片翻转动画效果。
- **注意（教材原文）**：这个动画效果**首先沿 x 轴翻转，然后沿 y 轴翻转**，是一个**具有透视效果的 3D 动画**。

**核心代码（代码9-9）**

```css
@keyframes animPlane {
  0%   { transform: perspective(120px) rotateX(0deg) rotateY(0); }
  50%  { transform: perspective(120px) rotateX(-180deg) rotateY(0); }
  100% { transform: perspective(120px) rotateX(-180deg) rotateY(-180deg); }
}
.spinner{
    width:60px; height:60px; background-color:#67cf22; margin:100px auto;
    transform-style:preserve-3d;
    animation: animPlane 1.0s infinite ease-in-out;
}
```

```html
<div class="wrap"><div class="spinner"></div></div>
```

- **易错点（教材原文）**：**只有在 008～016 行代码中加上 transform 属性的 `perspective()` 函数才能在补间动画时产生 3D 透视效果。**

---

## 9.7 小结（原文要点）

> 动画在前端页面中，尤其是在呈现特效和游戏开发中具有广泛的应用。同时，它也是页面用于吸引人注意的重要方式。通过本项目的学习，我们可以深入了解 CSS3 的变换、过渡属性，以及常用的变换函数。通过示例和综合案例的学习与制作，我们可以具备一定的动画分析、制作和优化能力。

## 9.8 作业

**一、选择题**
1. CSS3 中的 @keyframes 规则是用于（ ）。A．定义动画名称 B．定义动画关键帧 C．定义动画函数 D．定义动画播放的时长
2. 在 CSS3 中，animation-fill-mode 属性用于设置（ ）。A．动画播放的时长 B．动画运动的函数 C．动画结束后元素的样式 D．动画的延迟
3. 在 CSS3 中，（ ）不是用来控制动画的速度曲线函数。A．ease B．linear C．linear-gradient D．ease-in-out
4. 关于 CSS3 中的 transition 属性，说法正确的是（ ）。
   A．可以应用于所有 CSS3 属性
   B．只能应用于盒子模型的相关属性
   C．可以应用于所有关于动画的 CSS 属性
   D．以上均不对
5. 关于 CSS3 中的 animation 属性，说法不正确的是（ ）。
   A．它是一个简写样式属性，可以定义动画的相关样式
   B．它可以定义动画规则
   C．它可以指定动画播放的时长
   D．它可以指定动画播放的循环次数

**二、简述题**
1. 在判断 3D 旋转时，有左手法则和右手法则。以右手法则为例：伸出右手，大拇指指向旋转轴的正方向，其余四指的环绕方向恰好对应旋转的正方向，符合这样的旋转规则就被称为右手法则（图9-23）。**请结合本项目的示例，验证并说明 CSS3 的 3D 空间旋转符合左手法则还是右手法则？**
2. 任务9-5 使用**指定子元素**的方式实现了卡片翻转动画。请根据 3D 变换的知识，将其实现代码修改成使用**指定父元素**的方式。比较它们在写法上的区别，分析使用哪种方式更加简洁？

**三、项目讨论**：迭代思维作为互联网的重要思想之一，在工程实践中具有非常重要的作用。它是产品思维的过程化体现，请结合你的开发实践示例说明你的迭代过程，并描述你的体会和感悟！

---

# 项目10 多媒体应用（PDF 第 315–323 页）

## 10.0 项目概览

**项目名**：项目10 多媒体应用

**思政课堂（原文要点）**
> 基于 Web 的网络多媒体为**红色文化的传承和发扬**提供了全新的平台。通过互联网，人们可以随时随地访问各种红色文化资源，如图片、视频、音频等，从而能更加深入地了解红色历史。此外，网络多媒体通过其互动性、社交性等特点，让红色文化更加贴近群众，增强群众对红色文化的认同感和归属感。同时，网络多媒体也为红色文化的传播提供了更加广阔的渠道，让红色文化在全球范围内得到更广泛的传播和推广。因此，基于 Web 的网络多媒体在红色文化传承和发扬中发挥着越来越重要的作用。

**学习目标**
- 掌握 `<object>` 标签的语法及使用方法
- 掌握 `<embed>` 标签的语法及使用方法
- 掌握 `<video>` 标签的语法及使用方法
- 掌握 `<audio>` 标签的语法及使用方法

**技能目标**
- 能使用 `<object>` 标签实现在页面中嵌入 PDF 文档
- 能使用 `<video>` 标签实现在页面中播放视频
- 能使用 `<audio>` 标签实现在页面中播放音频

**素养目标**
- 培养民族自信、文化自信，弘扬社会主义文化价值
- 讲好中国故事，传播好中国声音

---

## 10.1 常见的多媒体标签

**引入（教材原文要点）**
- 网页制作从嵌入文字、链接、一些简单的图片，逐渐向嵌入**视频、音频、PDF、Canvas 动画**等多媒体对象发展。
- HTML 提供了 `<object>`、`<embed>`、`<video>`、`<audio>` 等标签，**但这些标签在使用时存在兼容性问题，需要额外注意。**

---

### 10.1.1 `<object>` 标签

**技术要点**
- `<object>` 标签（**HTML 嵌入对象元素**）表示一个外部资源，可将其视为图像、嵌套的浏览上下文或插件要处理的资源，主要包括**音频、视频、Java Applets 小程序、ActiveX 控件、PDF、Flash** 等。
- 设置 `<object>` 标签的初衷是**取代 `<img>` 标签和 `<applet>` 标签**，但由于漏洞及缺乏浏览器的支持，这一初衷并未实现。
- `<object>` 标签可用于 Windows IE 3.0 及以上版本的 IE 浏览器或其他支持 ActiveX 控件的浏览器；主流浏览器使用不同的代码加载相同的对象类型，可针对不同浏览器设置不同语法解决兼容性问题。

**1．针对 IE 6～9 等低版本 IE 浏览器的语法**

```html
<object classid="clsid" codebase="url" width="w-value" height="h-value">
  <param name="movie" value="file_name">
  <param name="quality" value="high">
  <param name="wmode" value="opaque">
  …
</object>
```

- 上述语法**只对 IE 9 及以下低版本 IE 浏览器有效**，对 IE 10/11 浏览器和非 IE 浏览器无效。针对这些浏览器，需要在 `<object>` 标签中**再嵌入一个 `<object>` 标签**。通常的做法是：如果未显示 `<object>` 标签，则会执行位于 `<object>` 和 `</object>` 之间的代码。通过这种方式能够**嵌套多个 `<object>` 标签（每个对应一个浏览器）**，从而实现对浏览器的兼容。

**2．针对 IE 10/11 浏览器和非 IE 浏览器的语法**

```html
<object classid="clsid" codebase="url" width="w_value" height="h_value">
  <param name="movie" value="file_name">
  …
  <!--[if !IE]>
  <object type="media_type" data="media_fileName" width="w_value" height="h_value">
  <![endif]-->
  <param name="quality" value="high">
  <param name="wmode" value="opaque">
  <!--[if !IE]>
  </object>
  <![endif]-->
</object>
```

- 在非 IE 浏览器中执行时，将会执行**条件注释 `[if !IE]` 内部的语句**，从而实现对非 IE 浏览器的兼容。

> **常见的编程错误（教材原文）**：Firefox 浏览器不支持 `<object>` 标签，上述语法应用在 Firefox 浏览器中是常见的编程错误。

**表10-1 `<object>` 标签属性（完整还原）**

| 属性名 | 属性值 | 描述 |
|---|---|---|
| align | top bottom middle left right | HTML5 不支持。根据周围元素指定 `<object>` 标签的对齐方式 |
| archive | URL | HTML5 不支持。以空格分隔的归档 URL 列表。存档包含与对象相关的资源 |
| border | pixels | HTML5 不支持。指定 `<object>` 标签周围边框的宽度 |
| classid | class_ID | HTML5 不支持。在 Windows 注册表或 URL 中定义类 ID 值 |
| codebase | URL | HTML5 不支持。定义在何处查找对象的代码 |
| codetype | media_type | HTML5 不支持。classid 属性引用的代码的媒体类型 |
| data | URL | 指定对象要使用的资源的 URL |
| declare | declare | HTML5 不支持。定义只能声明对象，而不能在需要之前创建或实例化对象 |
| form5 | form_id | 指定对象所属的一个或多个表单 |
| height | pixels | 指定对象的高度 |
| hspace | pixels | HTML5 不支持。指定对象左侧和右侧的空白 |
| name | name | 指定对象的名称 |
| standby | text | HTML5 不支持。定义在加载对象时要显示的文本 |
| type | media_type | 定义 data 属性中指定的数据的媒体类型 |
| usemap | #mapname | 指定与对象一起使用的客户端图像映射的名称 |
| vspace | pixels | HTML5 不支持。指定对象顶部和底部的空白 |
| width | pixels | 指定对象的宽度 |

> 【备课提示】`form5` 应为 `form` 的识别/排版误差；HTML5 中 `<object>` 支持 `form`、`data`、`type`、`width`、`height`、`name`、`usemap`，其余多已废弃。

**Flash 背景（教材原文，可作课程思政/技术史素材）**
> Flash 作为嵌入网页的动画和多媒体应用，在网页发展历史中曾辉煌一时。但由于其对浏览器搜索引擎不友好，无法实现搜索引擎优化，加上它存在安全隐患，因此**自 2021 年起，Adobe 已停止为 Flash 提供支持**。在随后任何版本的 Google Chrome 浏览器中，Flash 内容（包括音频和视频）都无法再正常显示。目前，尚有部分浏览器支持 Flash，如 360 浏览器和 QQ 浏览器，但并不保证以后还支持。

---

### 10.1.2 `<embed>` 标签

**技术要点**
- `<embed>` 与 `<object>` 一样，可用于在网页中嵌入 Flash 动画、音频和视频等多媒体内容。
- **不同之处**：`<embed>` 用于 **Netscape Navigator 2.0** 及其以后版本的浏览器或其他支持 Netscape 插件的浏览器，**包括 IE 浏览器和 Google Chrome 浏览器**，而 **Firefox 浏览器目前尚不支持**。

**语法**

```html
<embed src="file_url"></embed>
```

- `src` 属性用于指定嵌入对象的文件路径；嵌入对象的格式可以是 **MP3、MP4、SWF** 等。

**表10-2 `<embed>` 标签的常用属性（完整还原）**

| 属性名 | 描述 |
|---|---|
| src | 指定嵌入对象的文件路径 |
| width | 以像素为单位定义嵌入对象的宽度 |
| height | 以像素为单位定义嵌入对象的高度 |
| loop | 指定嵌入对象是否循环播放 |
| hidden | 设置多媒体软件的可视性，默认值为 false |
| type | 定义嵌入对象的 MIME 类型 |

#### 任务10-1 嵌入 PDF（PDF 318–319）

- **任务名**：嵌入 PDF
- **任务目标**：根据 `<object>`、`<embed>` 语法，将教学项目源文件中的 **`assets/zhang.pdf`** 显示在页面中（图10-1）。
- **案例背景**：页面标题为"**红色印记-张人亚党章学堂**"（呼应思政课堂的红色文化主题）。

**核心代码（代码10-1）**

```css
.outer{ margin:0 auto; background-color:#CCC; width:800px; text-align:center; }
```

```html
<div class="outer">
  <embed src="assets/zhang.pdf" width="95%" height="600"></embed>
</div>
```

- **注意（教材原文）**：大多数现代浏览器已经弃用并取消了对浏览器插件的支持，所以如果希望制作的网站可以在普通用户的浏览器中运行，则**建议尽量不使用 `<embed>` 标签**。

---

### 10.1.3 `<video>` 标签

**技术要点**
- 在 HTML5 中，通过专用的 `<video>` 和 `<audio>` 标签分别实现视频、音频嵌入，**从而取代 `<object>` 和 `<embed>` 标签**。
- 它们是 HTML5 新增标签，**IE 9 及其以上版本的 IE 浏览器，以及 Firefox、Opera、Google Chrome、Safari 等主流浏览器都支持**。

**语法**

```html
<video src="file_url"></video>
```

- 在 `<video>` 标签中，**必须设置引用的视频存放地址**，可以是相对路径，也可以是网络路径。

**表10-3 `<video>` 标签的常用属性（完整还原）**

| 属性名 | 属性值 | 描述 |
|---|---|---|
| autoplay | autoplay | 如果出现该属性，则视频在就绪后马上播放 |
| controls | controls | 如果出现该属性，则向用户显示控件，如播放按钮 |
| height | pixels | 设置视频播放器的高度 |
| loop | loop | 如果出现该属性，则当多媒体文件完成播放后再次开始播放 |
| preload | preload | 如果出现该属性，则视频在页面加载时进行加载，并预备播放。如果使用 autoplay 属性，则忽略该属性 |
| src | url | 设置要播放的视频的 URL |
| width | pixels | 设置视频播放器的宽度 |
| muted | muted | 如果出现该属性，则视频的音频输出为静音 |
| poster | URL | 规定视频正在下载时显示的图像，直到用户单击播放按钮 |
| type | MIME | 定义嵌入对象的 MIME 类型 |

**表10-4 `<video>` 标签支持的多媒体文件格式（完整还原）**

| 格式 | MIME-type | 扩展名 | 描述 |
|---|---|---|---|
| Mpeg-4 | video/mp4 | .mp4 | MP4 文件使用 H264 视频编解码器和 AAC 音频编解码器 |
| WebM | video/webm | .webm | WebM 文件使用 VP8 视频编解码器和 Vorbis 音频编解码器 |
| OGG | video/ogg | .ogg | OGG 文件使用 Theora 视频编解码器和 Vorbis 音频编解码器 |

#### 任务10-2 嵌入视频（PDF 320–321）

- **任务名**：嵌入视频
- **任务目标**：将教学项目源文件的 **`intro.mp4`** 显示在页面中（图10-2）。

**核心代码（代码10-2）**

```html
<video src="./assets/intro.mp4" controls loop width="80%"></video>
```

（页面标题："课程宣传片-视频播放"）

---

### 10.1.4 `<audio>` 标签

**技术要点**
- `<audio>` 标签用于在页面中嵌入音频。嵌入的音频格式包括 **MP3、WAV、OGG、WebM** 等。

**语法**

```html
<audio src="file_url" control></audio>
```

- `<audio>` 标签中**至少要包含 src 属性**，它指定了音频文件的路径。除该属性外，还可通过设置**表10-3 中的一些属性**来获得所嵌入对象的不同表现效果。
- **与 `<video>` 的差别**：`<audio>` 和 `<video>` 的绝大多数属性相同，**只是 `<audio>` 标签中不包含 poster 属性**，其余属性用法相同。

#### 任务10-3 嵌入音频（PDF 321–322）

- **任务名**：嵌入音频
- **任务目标**：将教学项目源文件的 **`intro.mp3`** 显示在页面中（图10-3）。

**核心代码（代码10-3）**

```css
.outer{ margin:0 auto; background-color:#FFE4C4; width:800px; text-align:center; }
h2{ color:red; text-shadow:3px 4px #c3610863; }
```

```html
<div class="outer">
  <h2>课程宣传音频</h2>
  <audio controls="controls" autoplay="autoplay" loop="loop">
    <source src="./assets/intro.mp3" type="audio/mpeg">
    <source src="./assets/intro.ogg" type="audio/ogg">
    您的浏览器不支持audio 元素。
  </audio>
</div>
```

**启发问答：为什么不用 `<audio src="…">` 简单写法？**
- 教材说明：这里采用了一种与任务10-2 不同的实现方法，即使用 **`<source>` 标签** 而不是标签属性来定义音频文件。
- 023～024 行使用了**两种不同的音频格式（MP3 和 OGG）**，尽可能确保用户浏览器能正常播放所支持文件格式的音频，从而实现更加友好的兼容；同时，在不支持 `<audio>` 标签的浏览器中，还使用了显式文字"您的浏览器不支持audio 元素"。**不仅便于代码的调试和验证，还极大地提升了用户体验，是一种更加推荐的做法。**

> **良好的编程习惯（教材原文）**：使用兼容性写法，尽可能满足不同浏览器的需求，是良好的编程习惯的体现。

---

## 10.2 小结（原文要点）

> 通过本项目的学习，我们深入了解了网页中多媒体对象嵌入的传统做法及发展历史，并了解了基于 HTML5 的新增 `<video>` 标签和 `<audio>` 标签及其用法。通过项目化的任务，我们掌握了在页面中嵌入 PDF、视频、音频的常用实现方法。

## 10.3 作业

**一、选择题**
1. 以下不是视频格式的是（ ）。A．MP4 B．MP3 C．OGG D．WebM
2. 以下不是音频格式的是（ ）。A．MP3 B．MOV C．OGG D．WAV
3. 要嵌入 PDF 应该使用（ ）标签。A．embed B．video C．audio D．以上均不是
4. 在播放视频时，要想实现静音效果应使用（ ）属性。A．poster B．preload C．loop D．muted
5. 使用（ ）属性可以让视频循环播放。A．poster B．preload C．loop D．muted

**二、操作题**
1. 以"**中国传统美德**"为题，讲述一个经典故事，并将其录制成音频，命名为 `ctmd.mp3`。将该音频置于项目资源文件夹 `assets` 中（完整路径 `assets/ctmd.mp3`）。通过代码实现音频的**自动播放**。
2. 为向世人展现物产丰富、风景迷人的新疆，请以"**大美新疆**"为题，将搜集、选取的相应素材制作成视频，并设计一个宣传页面。要求：嵌入视频、图片和文字。

**三、项目讨论**：本项目介绍了 Web 中视频和音频的处理方式，请结合实际网页或手机应用：① 找 1～2 个包含视频、音频的页面，并探讨实现方法；② 谈一谈在通过网络宣传中国文化时，需要注意的问题。

**拓展学习**：某工业互联网 MES 管理平台（教材仅列标题）。

---

# 附录A：教材启发式问答关键知识点汇总（可直接做课堂提问）

| 序号 | 问题（出处） | 关键答案 |
|---|---|---|
| 1 | 什么是标准流，它是如何排版的？（7.1.1） | 自左而右、自上而下流式排列；同级块级盒子自上而下、行内元素自左而右；浮动和定位都是通过更改默认排版方式实现的 |
| 2 | "框1"原来占据父容器一整行，浮动后还占据吗？（任务7-1） | 不占据，原位置被"框2"占据，这就是"脱离标准流" |
| 3 | 3 个框都浮动后父容器怎么了？ | 由于子元素脱离，父容器塌陷成一条线（高度塌陷） |
| 4 | 如何证明浮动元素是衬于标准流之下还是浮于之上？（任务7-2） | 元素分"元素层+内容层"两层；浮动后提升到内容层，后面元素上移占据其元素层位置，文字内容被挤出形成环绕 → "提升半个层级" |
| 5 | 浮动对行内元素有什么影响？（任务7-3） | 使行内元素具有块级元素特征（块级格式化上下文），width/height 生效；与文字同属内容层，会被挤出原位置 |
| 6 | 后续不需要浮动，如何清除？（7.1.3） | 用 `clear`；前提是：① 必须是块级元素 ② 必须与浮动元素同级 ③ 目的是清除上方浮动元素对自身的影响 |
| 7 | 空 div 清除浮动有什么缺点？更好的办法？ | 增加了无语义标签；可用 `::after` 伪元素（须 `display:block` + `content:""`） |
| 8 | BFC 是什么？ | 块级格式上下文，提供独立布局环境，"围墙内的出不去，围墙外的进不来" |
| 9 | 触发 BFC 的 3 种常用方式？ | `display:inline-block`、父元素浮动、`overflow` 取非 visible 值（scroll/hidden/auto）；绝对定位也可触发 |
| 10 | 父元素浮动触发 BFC 有什么副作用？ | 能包裹浮动子元素，但同样会影响自身和其他元素，需按具体情况选择 |
| 11 | 使用定位属性至少需要几个？ | 水平方向和垂直方向**至少各一个** |
| 12 | 什么是绝对定位？ | 相对于距离最近的已定位祖先元素定位；无已定位祖先元素时相对于浏览器定位 |
| 13 | 只设绝对定位不设偏移量会怎样？ | 元素还在原位置，但会脱离标准流 |
| 14 | fixed 与 absolute 如何选择？ | fixed 相对视口，滚动页面不动；absolute（无已定位祖先时）相对浏览器窗口，会随文档一起滚动 |
| 15 | 什么是"已定位元素"？ | 除静态定位外，父元素使用绝对/相对/固定定位都属于已定位情况；其子元素绝对定位时使用父元素的局部坐标系 |
| 16 | 精品课程封面中的 scale()、transition 是什么？ | transform 提供 scale()/rotate()/translate() 等函数；transition 实现过渡效果，详见项目9 |
| 17 | 圣杯布局中为什么是 `margin-left:-202px`？ | 除自身宽度 200px，还需加两侧边线各 1px |
| 18 | 双飞翼与圣杯的区别？ | 双飞翼在 main 外再加一层 main-wrap 并给 main 设 margin；圣杯用 padding + 相对定位；两者都靠 margin 负值 |
| 19 | 绝对居中时百分比定位为何没居中？ | 元素是相对**左上角**偏移的，还需 `margin-top`/`margin-left` 取自身宽高一半的负值；并用 z-index 调整与遮罩的层级 |
| 20 | 设置 Flex 后哪些属性失效？ | 子元素的 `float`、`clear`、`vertical-align` 失效 |
| 21 | align-content 默认 stretch 为何看不到效果？ | 必须确保子项**没有指定高度** |
| 22 | align-items 与 align-content 区别？ | align-items 针对每根交叉轴（每行）设；align-content 针对多轴内容整体设；align-content 必须配合 flex-wrap 使用 |
| 23 | 为什么用 flex-basis 而不是 width？ | flex-basis 描述子项在主轴中的空间大小，用于判断是否有剩余空间并配合 grow 分配；**flex-basis 优先级高于 width** |
| 24 | 为什么 flex-base 示例显示 302px？ | 300px 子项宽度 + 左右各 1px 边框 |
| 25 | 轮播图 017～019、065～075 行是什么？ | 实现自动滑动的动画效果，项目9 详解 |
| 26 | 变换轴心在哪里？如何调整？ | 默认在盒子中心（50% 50% / center center）；用 `transform-origin: x y`（空格分隔），可用像素或 top/bottom/left/right/center |
| 27 | perspective 值大小意味着什么？ | 值越大＝距离屏幕越远，物体看起来越小；值越小＝距离越近，物体越大；配合 translateZ 实现近大远小 |
| 28 | perspective 的两种写法？ | ① 设在共同父元素上 `perspective:800px`；② 设在当前元素上 `transform:perspective(800px) rotate(45deg)` |
| 29 | perspective-origin 只给一个值会怎样？ | 另一个值取默认值 center |
| 30 | 多个变换函数如何分隔？ | 用**空格**；用逗号是常见编程错误 |
| 31 | 过渡和动画的最大区别？ | 动画支持自定义关键帧（@keyframes），可控制动画序列的**中间步骤**，可控性更高 |
| 32 | 0% 和 100% 可以用什么替代？ | `from`、`to` |
| 33 | 呼吸灯如何优化？ | 两个动画运动规律相同、只差一个时间差 → 只定义一个 bounce，用 `animation-delay:1s` 让第二个错开执行 |
| 34 | 卡片翻转为何要写 perspective()？ | 只有加上 transform 的 `perspective()` 函数，才能在补间动画时产生 3D 透视效果 |
| 35 | 嵌入音频为什么用 `<source>` 而不是 src 属性？ | 可提供 MP3 + OGG 多格式兼容，并在不支持时用显示文字降级，更推荐 |

---

# 附录B：教材表格速查（本范围内全部表格）

| 表号 | 名称 | 页码 | 本笔记位置 |
|---|---|---|---|
| 表6-10 | 表单样式重置（提及，使用 `input[type=text]` 属性选择器） | 200 | —（属项目6 范围） |
| 表7-1 | float 属性值 | 211–212 | 7.1.2 |
| 表7-2 | clear 属性值 | 219 | 7.1.3 |
| 表7-3 | overflow 属性值 | 226 | 7.1.4 |
| 表7-4 | position 属性值及描述 | 228 | 7.2.1 |
| 表7-5 | 定位属性值及描述（left/right/bottom/top） | 228 | 7.2.1 |
| 表7-6 | z-index 属性值及描述 | 228 | 7.2.1 |
| 表8-1 | Flex 容器常见的 6 个属性 | 262 | 8.3.1 |
| 表8-2 | flex-wrap 属性值 | 263 | 8.3.1.2 |
| 表8-3 | justify-content 属性值 | 264 | 8.3.1.4 |
| 表8-4 | align-items 属性值 | 265 | 8.3.1.5 |
| 表8-5 | align-content 属性值 | 266 | 8.3.1.6 |
| 表8-6 | Flex 子项样式属性 | 276 | 8.4 |
| 表9-1 | 常用的 2D 变换函数 | 289–290 | 9.2 |
| 表9-2 | 常用的 3D 变换函数 | 294 | 9.3 |
| 表9-3 | 常用的过渡样式属性 | 300 | 9.4 |
| 表9-4 | 常用的 animation 样式属性 | 304 | 9.5 |
| 表10-1 | `<object>` 标签属性 | 317 | 10.1.1 |
| 表10-2 | `<embed>` 标签的常用属性 | 318 | 10.1.2 |
| 表10-3 | `<video>` 标签的常用属性 | 319–320 | 10.1.3 |
| 表10-4 | `<video>` 标签支持的多媒体文件格式 | 320 | 10.1.3 |

**语法框速查**

| 语法号 | 内容 | 页码 |
|---|---|---|
| 语法8-1 | `flex-direction: row\|row-reverse\|column\|column-reverse` | 262 |
| 语法8-2 | `flex-flow: [flex-direction] \|\| [flex-wrap]`（默认 row nowrap） | 264 |
| 语法8-3 | `justify-content: flex-start \| flex-end \| center \| space-between \| space-around` | 264 |
| 语法8-4 | `align-items: flex-start \| flex-end \| center \| baseline \| stretch` | 265 |
| 语法8-5 | `align-content: flex-start \| flex-end \| center \| space-between \| space-around \| stretch` | 266 |
| — | `transform: none \| transform-functions` | 288 |
| — | `transform-origin: x y` | 292 |
| — | `transition: property duration timing-function delay` | 300 |
| — | `@keyframes animationname { keyframes-selector { css-styles; } }` | 303 |
| — | `animation: name duration timing-function delay iteration-count direction fill-mode` | 304 |

---

# 附录C：案例/素材与企业背景清单（便于课件还原）

| 案例/素材 | 出处 | 关键实现思路与参数 |
|---|---|---|
| 新疆简介图文环绕 | 任务7-2（图7-10） | `.outer` 500px；`img` 250px + `float:left` + `padding:5px`；`p{text-indent:2em}`；`.intro::first-letter{font-size:2em}`；素材 `images/xinjiang2.png` |
| 京东商城固定侧边栏 | 图7-21 | `position:fixed` 相对视口，滚动不变 |
| 美丽乡村文章 + 导航悬停 | 任务7-6（代码7-10） | `.outer` 512px 居中；`.toolbar{position:fixed; right:10px; top:100px}`；锚点 `#top/#sec01/#sec02/#sec03`；图片 `meili01.jpeg`～`meili06.jpg` |
| 精品课程封面 | 任务7-7（图7-28） | 父 `.course{position:relative}` + 子 `div.tag{position:absolute; right:-22px; top:26px; transform:rotate(45deg)}`；`img:hover{transform:scale(1.3)}` + `transition:all .6s`；素材 `cover.png`、`autumn.svg`、`people.png`、`teacherHeader.png` |
| 圣杯布局 | 任务7-8 | 三列全浮动 + `margin-left:-100%/-202px` + `.outer` 左右 padding + 相对定位左右推 |
| 双飞翼布局（淘宝 UED） | 任务7-9 | 加 `.main-wrap` 包裹层，`main{margin:0 200px 0 150px}`，省去相对定位 |
| 绝对居中对话框（淘宝 App / 美团 App） | 任务7-10 | `top:50%;left:50%` + `margin-top:-200px;margin-left:-150px` + `z-index:999`；遮罩 `opacity:0.3`；素材 `dialog-img.png` |
| 京东秒杀模块 | 任务7-11（图7-42） | 浮动 item 190px×275px；`.container{overflow:hidden}`；雪碧图 `sprite.seckill.png` 定位 `-35px -25px`；单行省略号；素材 `pic01.jpg`～`pic04.jpg` |
| 智能绘图产品块级居中（ChatGPT/AI 绘图背景） | 任务8-1 | 3 种方案：Flex / `display:table-cell` + `vertical-align:middle` / 定位 + `translate(-50%,-50%)`；素材 `AI_01.png` |
| 不定项导航按钮（轮播图分页） | 任务8-2 | `.wrap{display:flex; justify-content:center; align-items:flex-end}`；按钮 20px 圆形 `border-radius:50%` |
| 城市学院均分列布局 | 任务8-3 | 540px×153px，`justify-content:space-between`，`padding:0 30px`；4 项：学校官网/校务服务/办公系统/教务系统；素材 `nbcc-icon01~04.png` |
| 大美新疆导航栏（组合嵌套） | 任务8-4 | 1024px×60px，左右两个整体 + `space-between`；`.nav` 350px 内嵌 Flex；首个导航项高亮 `#ff9d00`；素材 `logo.png`、`icon5~7.png` |
| 轮播图 | 任务8-5（图8-23～8-25） | Flex 溢出布局（`width:100%` + `flex-shrink:0`）；分页器绝对定位 `bottom:40px` + Flex 居中；左右按钮绝对定位 10px；`@keyframes move-slide` 位移 0 / −500px / −1000px；Bootstrap Glyphicons 字体图标；调试设备 500×700 |
| 2D 变换综合示例 | 代码9-1 | rotate(45deg) / translate(10px,20px) / scale(2,0.5) / skew(30deg,20deg) / matrix(1,0.2,-1.2,1,0,0) |
| 变换轴心 | 代码9-2 | `scale(2)` + `transform-origin:top left` 对比 |
| 3D 骰子 | 任务9-1 | 100px 立方体；`preserve-3d` + `perspective:800px` + `perspective-origin:bottom center` + `rotate3d(1,1,0,332deg)`；6 面各 `rotateY/X(±90/180deg) translateZ(50px)` |
| 简单过渡 | 任务9-2 | `transition: width 2s` + `-webkit-` 前缀；`div:hover{width:300px}` |
| 背景过渡 | 代码9-5 | `transition: width ease-in-out 2s, background-color ease-in-out 2s`；可简写 `all` |
| 旋转骰子 | 任务9-3 | `@keyframes rotateDice` 0/180/359 度绕 y 轴；`animation: rotateDice 2s linear infinite` |
| 呼吸灯 | 任务9-4 | 50px 圆 `rgba(250,0,0,0.5)`；`bounce` 0%,100% `scale(1)` → 50% `scale(0)`；`2s ease-in-out infinite`；第二个 `animation-delay:1s` |
| 卡片翻转 | 任务9-5 | 60px×60px `#67cf22`；`perspective(120px) rotateX(-180deg)` → `rotateY(-180deg)`；`1.0s infinite ease-in-out` |
| 嵌入 PDF（红色印记-张人亚党章学堂） | 任务10-1 | `<embed src="assets/zhang.pdf" width="95%" height="600">`；`.outer` 800px `#CCC` |
| 嵌入视频（课程宣传片） | 任务10-2 | `<video src="./assets/intro.mp4" controls loop width="80%">` |
| 嵌入音频（课程宣传音频） | 任务10-3 | `<audio controls autoplay loop>` + 两个 `<source>`（mp3 / ogg）+ 降级文字；`h2{color:red; text-shadow:3px 4px #c3610863}` |

---

# 附录D：逐页要点索引（PDF 页码 → 一句话要点）

| 页码 | 要点 |
|---|---|
| 200 | 项目6 收尾：outline 与 border 的区别（outline 不占空间、仅针对链接/表单等少量元素）；属性选择器 `input[type=text]`；任务6-4 表单控件美化开始 |
| 201 | 代码6-14 CSS 前半：`.frm_txt`、`.frm_radio/.frm_chkbox{display:none}`、兄弟选择器 `+span` |
| 202 | 代码6-14 CSS 后半：`.file{position:relative}`、`.frm_file{position:absolute; opacity:0}` 隐藏上传控件 |
| 203 | 代码6-14 HTML 与解析：`:checked+span` 伪类、`background-size`、用超链接代替上传控件的思路 |
| 204 | 任务6-5 制作登录表单；代码6-15 HTML 结构（`.nav-simple`/`.page-wrap`/`.user-con`/`.user-item`） |
| 205 | 代码6-15 HTML 结束；代码6-16 CSS 开始（`*{}`、`.w` 1080px 居中、`.nav-simple`） |
| 206 | 代码6-16 CSS：`.page-wrap` `#e72955`、`.user-con` 400px、`.user-item{position:relative}` |
| 207 | 代码6-16 CSS：`.user-label{position:absolute}`、`.btn`、`.link-item`；6.6 小结 |
| 208 | 6.7 作业：项目6 选择题（rowspan / tr / border-collapse / form / GET 提交）与操作题（冬奥会奖牌榜、表单效果） |
| 209 | 项目6 项目讨论：北京 2008 夏奥 + 2022 冬奥"双奥之城" |
| 210 | **项目7 扉页**：思政课堂（Web 技术助力美丽乡村）、学习目标/技能目标/素养目标 |
| 211 | 7.1 网页布局简介（CSS2 三种 + CSS3 新增）；7.1.1 标准流；7.1.2 浮动排版 + 表7-1 float（none/left） |
| 212 | 表7-1 续（right/inherit）；浮动脱离标准流原理；任务7-1 代码7-1 开始 |
| 213 | 代码7-1 完整（`.box1{float:right}`）+ 运行效果分析；启发对话"脱离标准流" |
| 214 | 图7-4/7-5；**浮动 4 条特性**；任务7-2 图文环绕引入 |
| 215 | 元素立体两层模型（元素层/内容层，图7-8、7-9）；浮动"提升半个层级" |
| 216 | 代码7-2 CSS（`.outer` 500px、`img` 250px `float:left`、首字放大） |
| 217 | 代码7-2 HTML 正文（新疆简介三段）；任务7-3 代码7-3（span 行内元素） |
| 218 | 图7-11/7-12；浮动对行内元素的 2 条特性；7.1.3 清除浮动 + 表7-2 clear |
| 219 | 图7-13 高度塌陷；代码7-4 CSS（`.clr{clear:right}`） |
| 220 | 代码7-4 HTML；图7-14/7-15；清除浮动技巧要点(1) 必须是块级元素 |
| 221 | 技巧要点(2)(3)（同级元素、清除上方浮动影响）；任务7-4 代码7-5 CSS |
| 222 | 代码7-5 HTML + 图7-17；提出 ::after 优化方案；代码7-6 CSS |
| 223 | 代码7-6 HTML + 解析（`display:block`、`content:""`）；7.1.4 BFC 概念；任务7-5 |
| 224 | 触发 BFC 方式1：代码7-7 `display:inline-block`（"包裹性"） |
| 225 | 图7-18；方式2：代码7-8 父元素 `float:left` |
| 226 | 代码7-8 HTML + 图7-19 + 注意事项；方式3：overflow；**表7-3 overflow**；代码7-9 开始 |
| 227 | 代码7-9 CSS/HTML + 图7-20；绝对定位等其他方式也可触发 BFC |
| 228 | 7.2 定位简介；7.2.1 定位属性；**表7-4 position / 表7-5 定位属性 / 表7-6 z-index** + 记忆 3 点 |
| 229 | 7.2.2 静态定位；7.2.3 固定定位（京东固定侧边栏图7-21）；定位步骤；任务7-6 |
| 230 | 代码7-10 CSS（`.toolbar{position:fixed; right:10px; top:100px}`）+ HTML 开头 |
| 231 | 代码7-10 正文："建什么？加强重点领域农村基础设施建设"（"183"行动） |
| 232 | 正文："怎么建""建成什么样"；`.toolbar` 锚点链接 HTML |
| 233 | 代码7-10 结束（`#top`/`#sec01`/`#sec02`/`#sec03`）；图7-22；固定定位解析 |
| 234 | 7.2.4 绝对定位定义；代码7-11（`.box2{position:absolute; left:20px; top:40px}`） |
| 235 | 图7-23/7-24/7-25；相对浏览器定位；不设宽度时宽度由内容撑开 |
| 236 | **绝对定位 5 条特性**；技巧：fixed 与 absolute 的差别；7.2.5 相对定位；代码7-12 开始 |
| 237 | 代码7-12 CSS/HTML；图7-26/7-27（不设/设偏移量对比） |
| 238 | **相对定位 4 条特性**；"已定位元素"与局部坐标系；任务7-7 精品课程封面开始 |
| 239 | 代码7-13 CSS：`.course{position:relative}`、`div.tag{position:absolute; rotate(45deg)}`、`img:hover{scale(1.3)}` |
| 240 | 代码7-13 CSS 续：`.term-year` 背景图 `autumn.svg`、`.year`、`.term`、`.status`、`.teacher` |
| 241 | 代码7-13 HTML 结束；"父相子绝"解析；7.3 综合案例；任务7-8 圣杯布局 |
| 242 | 图7-29；"In Search of the Holy Grail"；代码7-14（HTML 顺序 main→left→right） |
| 243 | 代码7-14 结束；图7-30；`.left{margin-left:-100%}`、`.right{margin-left:-202px}` |
| 244 | 图7-31；`.outer{padding-left:150px; padding-right:200px}`；图7-32 |
| 245 | 相对定位推位：`left:-150px` / `right:-200px`；图7-33、图7-34 完整圣杯 |
| 246 | 代码7-15 圣杯完整代码（CSS 前半） |
| 247 | 代码7-15 结束（HTML）；任务7-9 双飞翼布局（源于淘宝 UED） |
| 248 | 代码7-16 双飞翼布局（`.main-wrap` + `.main{margin:0 200px 0 150px}`） |
| 249 | 双飞翼与圣杯对比总结；任务7-10 绝对居中布局（淘宝/美团 App） |
| 250 | 代码7-17（`.mask` 半透明遮罩、`.dialog{top:50%;left:50%}`） |
| 251 | 图7-38/7-39；"对话框没有绝对居中"的原因与 `margin` 负值修正 |
| 252 | 图7-40；z-index 调整遮罩与对话框层级；代码7-18 开始 |
| 253 | 代码7-18 结束（`z-index:999`）；图7-41 最终效果 |
| 254 | 任务7-11 京东秒杀模块；代码7-19 CSS 开头（`*{}`、`.container{overflow:hidden}`、`.item`） |
| 255 | 代码7-19 CSS：`.ms` 配色 `#e83632`、`.title` 34px、`.icon` 雪碧图 `-35px -25px`、`.clock span` |
| 256 | CSS 续：`.product-desc` 单行省略号、`.price`/`.price-new`/`.price-origin`；HTML 开头 |
| 257 | 代码7-19 HTML：4 个商品 item（pic01～pic03、商品文案与价格） |
| 258 | HTML 结束（pic04）；7.4 小结；7.5 作业选择题 1～3 |
| 259 | 作业选择题 4～5、操作题（居中登录框）、项目讨论（美丽乡村网页） |
| 260 | **项目8 扉页**：思政课堂（ChatGPT/AIGC + 网页应用技术）、三类目标；8.1 Flex 布局简介 |
| 261 | 弹性布局扩展/收缩示意（图8-1/8-2）；8.2 术语：容器/子项/主轴/交叉轴/main size/cross size |
| 262 | 8.3 Flex 容器：`display:flex`/`inline-flex`、`-webkit` 前缀、float/clear/vertical-align 失效；**表8-1**；语法8-1 flex-direction |
| 263 | 图8-4；8.3.1.2 flex-wrap **表8-2**；不换行时的弹性缩小（图8-5）、wrap/wrap-reverse（图8-6/8-7） |
| 264 | 语法8-2 flex-flow（默认 row nowrap）；语法8-3 + **表8-3 justify-content**；图8-8 |
| 265 | 图8-8 续；8.3.1.5 语法8-4 + **表8-4 align-items**；图8-9 |
| 266 | align-items 默认 stretch 说明；8.3.1.6 语法8-5 + **表8-5 align-content** |
| 267 | 启发问答：stretch 默认不生效的原因；align-items 与 align-content 的区别（图8-12） |
| 268 | 单轴时两者效果一致、但 align-content 需配合 flex-wrap；**常见编程错误**；任务8-1 代码8-1 |
| 269 | 代码8-1 结束；方案2 `display:table-cell`（代码8-2）；Word 单元格对齐类比（图8-14） |
| 270 | 方案3 定位 + `translate(-50%,-50%)`（代码8-3）；任务8-2 不定项居中布局 |
| 271 | 代码8-4 不定项导航按钮（`justify-content:center; align-items:flex-end`） |
| 272 | 任务8-3 均分列布局（城市学院网站，图8-16）；代码8-5 CSS |
| 273 | 代码8-5 HTML（学校官网/校务服务/办公系统/教务系统） |
| 274 | 任务8-4 组合嵌套布局（大美新疆导航栏）；图8-17/8-18 组合思想；代码8-6 开始 |
| 275 | 代码8-6 CSS 续：`.nav`、`.nav li:nth-child(1)` 高亮、`.rt`、`.share` |
| 276 | 代码8-6 HTML；8.4 Flex 子项；**表8-6 六个子项属性**；代码8-7 开始 |
| 277 | 代码8-7 CSS/HTML；601px 时子项显示与 align-self:flex-end 效果 |
| 278 | 图8-19/8-20/8-21（801px、400px 的 grow/shrink 表现）；flex-basis 优先级高于 width（图8-22） |
| 279 | 302px 宽度说明；任务8-5 轮播图（图8-23～8-25） |
| 280 | 图8-25；代码8-8 CSS 开头（`.swiper-container`、`.swiper-wrapper`、`.swiper-slide`） |
| 281 | 代码8-8 CSS：分页指示器、控制器按钮（绝对定位 left/right 10px） |
| 282 | `@keyframes move-slide`（0/-500px/-1000px）；代码8-8 HTML |
| 283 | 轮播图三步实现思路；图8-26/27/28；代码8-9 溢出布局 |
| 284 | 溢出布局说明；Bootstrap Glyphicons 字体图标使用 3 步（图8-29/8-30） |
| 285 | 移动设备查看模式调试：自定义设备"调试"500×700（图8-31～8-34） |
| 286 | 8.5 小结；8.6 作业选择题 1～5 |
| 287 | 项目8 项目讨论：慕课 App 与信息技术助力教育 |
| 288 | **项目9 扉页**：思政课堂（迭代开发 = 工匠精神）、三类目标；9.1 变换（transform 语法） |
| 289 | 9.2 2D 变换：2D 笛卡儿坐标系（图9-1，x 右为正、y 下为正）；**表9-1 2D 变换函数** |
| 290 | 表9-1 续（skew/matrix）；单轴函数；复合变换用**空格**分隔；常见错误：用逗号 |
| 291 | 代码9-1 CSS/HTML（rotate/translate/scale/skew/matrix 6 个盒子）；图9-2 |
| 292 | `transform-origin: x y`（空格分隔，默认 50% 50%）；代码9-2 开始 |
| 293 | 代码9-2 结束 + 图9-3（轴心调整至左上角）；9.3 3D 立体坐标系（图9-4） |
| 294 | **表9-2 3D 变换函数**；perspective 两种写法；perspective-origin |
| 295 | 图9-5 透视原理、图9-6 近大远小；perspective-origin 消失点（图9-7） |
| 296 | 图9-8（`left top`）、图9-9（不同取值透视对比） |
| 297 | backface-visibility（图9-10）；任务9-1 制作 3D 骰子；代码9-3 开始 |
| 298 | 代码9-3 CSS：`#dice`（preserve-3d、perspective 800px、bottom center、rotate3d 332deg）、`.face`、front/back/right |
| 299 | 代码9-3 续（left/top/bottom）+ HTML；6 面构造解析；9.4 过渡；**表9-3 过渡属性** |
| 300 | 表9-3；`transition: property duration timing-function delay`；任务9-2；代码9-4 开始 |
| 301 | 代码9-4 结束 + 解析（`-webkit-` 兼容）；代码9-5 宽度 + 背景色过渡 |
| 302 | 代码9-5 结束；`all` 简写技巧；常见错误：transition 错拼成 transform |
| 303 | 过渡 4 个初始值（delay 0s / duration 0s / property all / timing-function ease）；9.5 动画；@keyframes 语法 + rotateDice 示例 |
| 304 | 关键帧解析；from/to 技巧；animation 简写语法；**表9-4 animation 属性**；任务9-3 旋转骰子 |
| 305 | 图9-17；代码9-6（`@keyframes rotateDice`） |
| 306 | 代码9-6 CSS 续（`#dice{animation: rotateDice 2s linear infinite}`、6 个面） |
| 307 | 代码9-6 HTML 结束 + 解析（起始帧/中间帧/结束帧）；9.6 综合案例；任务9-4 呼吸灯 |
| 308 | 动画时间影像分析法（图9-19/9-20）；`@keyframes bounce1/bounce2`；代码9-7 开始 |
| 309 | 代码9-7 CSS（`.ball` 50px、`rgba(250,0,0,0.5)`、两套动画 + 前缀） |
| 310 | 代码9-7 HTML；优化思路：bounce1 与 bounce2 只差时间差（图9-21）；代码9-8 开始 |
| 311 | 代码9-8 结束（`.ball2{animation-delay:1s}`）+ 解析；工匠精神/迭代思维点评 |
| 312 | 良好编程习惯框；任务9-5 卡片翻转动画；代码9-9 开始 |
| 313 | 代码9-9 结束 + "必须加 perspective()" 提示；9.7 小结；9.8 作业选择题 |
| 314 | 作业简述题（右手法则验证、指定父元素改写卡片翻转）；项目讨论（迭代思维） |
| 315 | **项目10 扉页**：思政课堂（网络多媒体与红色文化传承）、三类目标；10.1 常见多媒体标签 |
| 316 | 10.1.1 `<object>` 标签：IE 6～9 语法、IE 10/11 及非 IE 语法（条件注释 `[if !IE]`） |
| 317 | 常见错误（Firefox 不支持 object）；**表10-1 object 属性**；Flash 停服背景；10.1.2 `<embed>` |
| 318 | 语法 `<embed src="file_url">`；**表10-2 embed 常用属性**；任务10-1 嵌入 PDF；代码10-1 开始 |
| 319 | 代码10-1（`<embed src="assets/zhang.pdf" width="95%" height="600">`）；现代浏览器弃用提示；10.1.3 video；**表10-3** |
| 320 | 表10-3 续（muted/poster/type）；**表10-4 视频格式**（MP4/WebM/OGG）；任务10-2；代码10-2 |
| 321 | 代码10-2（`<video src="./assets/intro.mp4" controls loop width="80%">`）；10.1.4 `<audio>`；任务10-3；代码10-3 开始 |
| 322 | 代码10-3（多 `<source>` + 降级文字）；兼容性写法 = 良好编程习惯；10.2 小结 |
| 323 | 10.3 作业（选择题、中国传统美德音频、大美新疆视频、项目讨论、拓展学习：工业互联网 MES 平台） |
| 324 | 反侵权盗版声明（电子工业出版社） |
