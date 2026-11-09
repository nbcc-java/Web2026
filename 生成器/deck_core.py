# -*- coding: utf-8 -*-
"""
《网页制作（HTML5+CSS3）》课件生成引擎 —— 核心渲染库
一份内容源(JSON) -> (1) 带动画特效的单文件 HTML 课件  (2) 对应的 PPTX 课件
"""
import html
import os
import re
import json
import shutil
import subprocess
import tempfile

# ---------------------------------------------------------------- 设计令牌（配色/字体）
THEME = {
    "bg":       "#EEF3FB",
    "bg2":      "#F7FAFF",
    "surface":  "#FFFFFF",
    "ink":      "#0E1B2E",
    "muted":    "#5A6C85",
    "brand":    "#2F6BFF",
    "brand_dk": "#1D46B8",
    "brand2":   "#0FB5C9",
    "violet":   "#7C5CFF",
    "accent":   "#FF8A3D",
    "ok":       "#12A150",
    "line":     "#E1E8F4",
    "code_bg":  "#0D1A2B",
    "code_ink": "#DCE7F8",
}

FONT_CN = "'PingFang SC','Microsoft YaHei','Hiragino Sans GB','Source Han Sans SC',system-ui,-apple-system,'Segoe UI',sans-serif"
FONT_MONO = "'JetBrains Mono','SF Mono',Menlo,Consolas,'Courier New',monospace"
FONT_PPT = "微软雅黑"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


# ---------------------------------------------------------------- 代码高亮
def _sp(cls, txt):
    return f'<span class="{cls}">{txt}</span>'


def hi_html(code):
    """HTML 语法高亮（输入为原始代码）"""
    code = html.escape(code)
    out = []
    i = 0
    n = len(code)
    while i < n:
        k = code.find("&lt;", i)
        if k < 0:
            out.append(code[i:])
            break
        out.append(code[i:k])
        # 注释
        if code.startswith("&lt;!--", k):
            e = code.find("--&gt;", k)
            e = n if e < 0 else e + 5
            out.append(_sp("c", code[k:e]))
            i = e
            continue
        # 找标签结束
        e = code.find("&gt;", k)
        if e < 0:
            out.append(code[k:])
            break
        e += 4
        tag = code[k:e]
        out.append(_hi_tag(tag))
        i = e
    return "".join(out)


def _hi_tag(tag):
    # tag 形如 &lt;div class="a"&gt;  或 &lt;/div&gt;
    m = re.match(r"^(&lt;/?)([a-zA-Z][\w:-]*)([\s\S]*?)(/?&gt;)$", tag)
    if not m:
        return tag
    open_, name, attrs, close_ = m.groups()
    parts = [_sp("pn", open_), _sp("tg", name)]
    # 属性
    pos = 0
    for am in re.finditer(r'([-a-zA-Z:]+)(\s*=\s*)("[^"]*"|\'[^\']*\')', attrs):
        parts.append(html.escape(attrs[pos:am.start()]) if False else attrs[pos:am.start()])
        parts.append(_sp("at", am.group(1)))
        parts.append(am.group(2))
        parts.append(_sp("st", am.group(3)))
        pos = am.end()
    parts.append(attrs[pos:])
    parts.append(_sp("pn", close_))
    return "".join(parts)


def hi_css(code):
    """CSS 语法高亮（输入为原始代码）"""
    code = html.escape(code)
    # 保护注释与字符串
    store = []

    def _protect(m):
        store.append(m.group(0))
        return f"\x00{len(store)-1}\x01"

    code = re.sub(r"/\*[\s\S]*?\*/|\"[^\"]*\"|'[^']*'", _protect, code)

    res = []
    i, n = 0, len(code)
    while i < n:
        j = i
        while j < n and code[j] not in "{};":
            j += 1
        chunk = code[i:j]
        delim = code[j] if j < n else ""
        if delim == "{":
            res.append(_sp("sel", _hi_sel(chunk)))
            res.append(_sp("pn", "{"))
        elif delim == ";":
            res.append(_hi_decl(chunk))
            res.append(_sp("pn", ";"))
        elif delim == "}":
            if chunk.strip():
                res.append(_hi_decl(chunk))
            res.append(_sp("pn", "}"))
        else:
            if chunk.strip():
                res.append(_hi_decl(chunk))
        i = j + 1

    txt = "".join(res)
    # 还原被保护的注释/字符串
    def _restore(m):
        idx = int(m.group(1))
        return _sp("c", store[idx]) if store[idx].startswith("/*") else _sp("st", store[idx])

    txt = re.sub("\x00(\\d+)\x01", _restore, txt)
    return txt


def _hi_sel(chunk):
    # 选择器中：伪类 / 标签 / 类 / id
    chunk = re.sub(r"(@[\w-]+)", lambda m: _sp("at", m.group(1)), chunk)
    chunk = re.sub(r"(\.[-\w]+)", lambda m: _sp("cls", m.group(1)), chunk)
    chunk = re.sub(r"(#[-\w]+)", lambda m: _sp("id", m.group(1)), chunk)
    chunk = re.sub(r"(:{1,2}[-\w()]+)", lambda m: _sp("pc", m.group(1)), chunk)
    return chunk


def _hi_decl(chunk):
    m = re.match(r"^([\s\S]*?)([-\w]+)(\s*:\s*)([\s\S]*)$", chunk)
    if not m:
        return chunk
    lead, prop, sep, val = m.groups()
    return lead + _sp("prop", prop) + sep + _hi_val(val)


def _hi_val(v):
    v = re.sub(r"(#[0-9a-fA-F]{3,8}\b)", lambda m: _sp("num", m.group(1)), v)
    v = re.sub(r"(\b-?\d*\.?\d+(?:px|em|rem|%|s|ms|deg|vw|vh|vmin|vmax|fr|pt|ch|ex|turn|rad)?\b)",
               lambda m: _sp("num", m.group(1)), v)
    v = re.sub(r"([\w-]+)(\()", lambda m: _sp("fn", m.group(1)) + m.group(2), v)
    v = re.sub(r"(!important)", lambda m: _sp("imp", m.group(1)), v)
    return v


HILITE = {"html": hi_html, "css": hi_css, "js": lambda c: html.escape(c), "text": lambda c: html.escape(c)}


def _code(code, lang):
    fn = HILITE.get(lang, HILITE["text"])
    return fn(code)


# ---------------------------------------------------------------- 幻灯片 HTML 渲染
def esc(t):
    return html.escape(str(t))


def ani(i, extra=""):
    return f'class="an {extra}" style="--i:{i}"'


TYPE_LABEL = {
    "bullets": "知识要点", "cards": "要点分解", "table": "对照表", "compare": "对比辨析",
    "steps": "操作步骤", "code": "代码示例", "codebullets": "代码与要点", "demo": "效果演示",
    "task": "任务驱动", "ai": "AI 前沿", "quiz": "随堂检测", "flow": "原理图解",
}


def r_cover(u):
    tags = "".join(f'<span class="pill" style="--i:{3+i}">{esc(t)}</span>' for i, t in enumerate(u.get("cover_tags", [])))
    return f"""
<section class="slide s-cover is-active" data-kind="cover">
  <div class="cover-left">
    <div class="brandrow an" style="--i:0">
      <span class="brandmark">网页制作</span>
      <span class="brandsub">HTML5 + CSS3</span>
    </div>
    <div class="kicker an" style="--i:1">{esc(u.get('project',''))} · {esc(u.get('unit',''))}</div>
    <h1 class="cover-title an" style="--i:2">{esc(u['title'])}</h1>
    <p class="cover-sub an" style="--i:3">{esc(u.get('subtitle',''))}</p>
    <div class="pills">{tags}</div>
    <div class="cover-meta an" style="--i:{4+len(u.get('cover_tags',[]))}">
      <span class="m-item"><b>{esc(u.get('duration',40))}</b> 分钟</span>
      <span class="dot"></span>
      <span class="m-item">教材《网页制作（HTML5+CSS3）》{esc(u.get('project',''))}</span>
      <span class="dot"></span>
      <span class="m-item">{esc(u.get('ref_book','电子工业出版社 · 2025'))}</span>
    </div>
  </div>
  <div class="cover-art" aria-hidden="true">
    <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
    <div class="codewin">
      <div class="cw-bar"><i></i><i></i><i></i></div>
      <pre class="cw-body"><span class="pn">&lt;!</span><span class="tg">DOCTYPE</span> <span class="at">html</span><span class="pn">&gt;</span>
<span class="pn">&lt;</span><span class="tg">html</span> <span class="at">lang</span>=<span class="st">"zh-CN"</span><span class="pn">&gt;</span>
  <span class="pn">&lt;</span><span class="tg">head</span><span class="pn">&gt;</span> <span class="pn">&lt;</span><span class="tg">meta</span> <span class="at">charset</span>=<span class="st">"UTF-8"</span><span class="pn">&gt;</span> <span class="pn">&lt;/</span><span class="tg">head</span><span class="pn">&gt;</span>
  <span class="pn">&lt;</span><span class="tg">body</span><span class="pn">&gt;</span>
    <span class="pn">&lt;</span><span class="tg">h1</span><span class="pn">&gt;</span>Hello, Web<span class="pn">&lt;/</span><span class="tg">h1</span><span class="pn">&gt;</span>
  <span class="pn">&lt;/</span><span class="tg">body</span><span class="pn">&gt;</span>
<span class="pn">&lt;/</span><span class="tg">html</span><span class="pn">&gt;</span></pre>
    </div>
  </div>
</section>"""


def r_section(s, i0=0):
    return f"""
<section class="slide s-section" data-kind="section">
  <div class="sec-inner">
    <div class="sec-num an" style="--i:0">{esc(s.get('no',''))}</div>
    <h2 class="sec-title an" style="--i:1">{esc(s['title'])}</h2>
    <div class="sec-line an" style="--i:2"></div>
    <p class="sec-sub an" style="--i:3">{esc(s.get('text',''))}</p>
  </div>
</section>"""


def r_outline(s, i0=0):
    cls = "outline" + (" dense" if len(s["items"]) >= 5 else "")
    items = "".join(
        f'<li {ani(i+1)}><span class="oi">{i+1:02d}</span><span class="ot">{t}</span></li>'
        for i, t in enumerate(s["items"]))
    return f"""
<section class="slide" data-kind="outline">
  {head(s)}
  <div class="s-body"><ol class="{cls}">{items}</ol></div>
</section>"""


def head(s, kicker=None):
    k = s.get("kicker") or TYPE_LABEL.get(s.get("type", ""), "")
    sub = s.get("subtitle", "")
    return f"""
  <header class="s-head">
    <div class="s-head-left">
      {f'<div class="kicker an" style="--i:0">{esc(k)}</div>' if k else ''}
      <h2 class="s-title an" style="--i:1">{esc(s.get('title',''))}</h2>
      {f'<p class="s-sub an" style="--i:2">{sub}</p>' if sub else ''}
    </div>
  </header>"""


def r_bullets(s, i0=0):
    cls = "blist" + (" dense" if len(s["items"]) >= 5 else "")
    items = "".join(
        f'<li {ani(i+1)}><span class="bl-dot"></span><span>{t}</span></li>'
        for i, t in enumerate(s["items"]))
    return f"""
<section class="slide" data-kind="bullets">
  {head(s)}
  <div class="s-body"><ul class="{cls}">{items}</ul></div>
</section>"""


def r_cards(s, i0=0):
    cols = s.get("cols", 3)
    dense = " dense" if len(s["items"]) >= 4 else ""
    cards = ""
    for i, c in enumerate(s["items"]):
        ik = c.get("icon", "")
        cards += f"""<div class="card{dense}" {ani(i+1)}>
          {f'<div class="card-ico">{ik}</div>' if ik else ''}
          <div class="card-t">{c['title']}</div>
          <div class="card-d">{c.get('text','')}</div>
        </div>"""
    return f"""
<section class="slide" data-kind="cards">
  {head(s)}
  <div class="s-body"><div class="grid cols-{cols}{dense}">{cards}</div></div>
</section>"""


def r_table(s, i0=0):
    th = "".join(f"<th>{esc(h)}</th>" for h in s["head"])
    tr = ""
    for i, row in enumerate(s["rows"]):
        tr += f'<tr {ani(i+1)}>' + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
    return f"""
<section class="slide" data-kind="table">
  {head(s)}
  <div class="s-body"><div class="tbl-wrap">
    <table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>
  </div></div>
</section>"""


def r_compare(s, i0=0):
    a, b = s["a"], s["b"]
    def col(c, cls, base):
        rows = "".join(f'<li {ani(base+i)}>{t}</li>' for i, t in enumerate(c.get("items", [])))
        return f"""<div class="cmp {cls}">
          <div class="cmp-h">{esc(c['title'])}</div>
          <ul>{rows}</ul></div>"""
    return f"""
<section class="slide" data-kind="compare">
  {head(s)}
  <div class="s-body"><div class="cmp-wrap">{col(a,'cmp-a',1)}{col(b,'cmp-b',3)}</div></div>
</section>"""


def r_steps(s, i0=0):
    items = ""
    for i, t in enumerate(s["items"]):
        items += f"""<div class="step" {ani(i+1)}>
          <div class="step-n">{i+1}</div>
          <div class="step-b"><div class="step-t">{esc(t['title'])}</div>
          <div class="step-d">{t.get('text','')}</div></div>
        </div>"""
    return f"""
<section class="slide" data-kind="steps">
  {head(s)}
  <div class="s-body"><div class="steps">{items}</div></div>
</section>"""


def r_flow(s, i0=0):
    items = ""
    n = len(s["items"])
    for i, t in enumerate(s["items"]):
        items += f"""<div class="fl" {ani(i+1)}>
          <div class="fl-ico">{t.get('icon','')}</div>
          <div class="fl-t">{t['title']}</div>
          <div class="fl-d">{t.get('text','')}</div>
        </div>"""
        if i < n - 1:
            items += f'<div class="fl-arrow" {ani(i+1, "fl-arrow")}></div>'
    return f"""
<section class="slide" data-kind="flow">
  {head(s)}
  <div class="s-body"><div class="flow">{items}</div>
  {f'<div class="flow-note an" style="--i:{n+1}">{esc(s.get("note",""))}</div>' if s.get('note') else ''}
  </div>
</section>"""


def r_code(s, i0=0):
    return f"""
<section class="slide" data-kind="code">
  {head(s)}
  <div class="s-body col"><div class="codebox" {ani(1)}>
      <div class="cb-bar"><span class="cb-lang">{esc(s.get('lang','html').upper())}</span>
      <span class="cb-file">{esc(s.get('file',''))}</span></div>
      <pre class="cb-code">{_code(s['code'], s.get('lang','html'))}</pre>
    </div>
    {f'<div class="caption an" style="--i:2">{s.get("caption","")}</div>' if s.get('caption') else ''}
  </div>
</section>"""


def r_codebullets(s, i0=0):
    cls = "blist small" + (" dense" if len(s["items"]) >= 4 else "")
    items = "".join(f'<li {ani(i+1)}><span class="bl-dot"></span><span>{t}</span></li>' for i, t in enumerate(s["items"]))
    return f"""
<section class="slide" data-kind="codebullets">
  {head(s)}
  <div class="s-body two">
    <div class="col-l"><ul class="{cls}">{items}</ul></div>
    <div class="col-r"><div class="codebox" {ani(1)}>
      <div class="cb-bar"><span class="cb-lang">{esc(s.get('lang','html').upper())}</span>
      <span class="cb-file">{esc(s.get('file',''))}</span></div>
      <pre class="cb-code">{_code(s['code'], s.get('lang','html'))}</pre></div></div>
  </div>
</section>"""


def r_task(s, i0=0):
    steps = "".join(f'<li {ani(2+i)}>{t}</li>' for i, t in enumerate(s.get("steps", [])))
    code = ""
    if s.get("code"):
        code = f"""<div class="task-code" {ani(2+len(s.get('steps',[])))}>
          <pre class="cb-code">{_code(s['code'], s.get('lang','html'))}</pre></div>"""
    return f"""
<section class="slide" data-kind="task">
  {head(s, kicker='任务驱动')}
  <div class="s-body two">
    <div class="col-l">
      <div class="task-goal an" style="--i:1"><span class="tg-label">任务目标</span>{s.get('goal','')}</div>
      <ol class="task-steps">{steps}</ol>
    </div>
    <div class="col-r">{code}</div>
  </div>
</section>"""


def r_demo(s, i0=0):
    code_html = s.get("code", "")
    srcdoc = html.escape(s["html"], quote=True)
    preview = f'<iframe class="demo-frame" title="效果预览" srcdoc="{srcdoc}"></iframe>'
    right = preview
    if code_html:
        right = f"""<div class="demo-right">
          {preview}
          <details class="demo-code"><summary>查看源码</summary>
          <pre class="cb-code">{_code(code_html, s.get('lang','html'))}</pre></details></div>"""
    return f"""
<section class="slide" data-kind="demo">
  {head(s, kicker='效果演示')}
  <div class="s-body two demo">
    <div class="col-l"><ul class="blist small">{"".join(f'<li {ani(i+1)}><span class="bl-dot"></span><span>{t}</span></li>' for i, t in enumerate(s.get('items', [])))}</ul>
      {f'<div class="hint an" style="--i:{len(s.get("items",[]))+1}"><b>动手试试：</b>{s.get("hint","")}</div>' if s.get('hint') else ''}
    </div>
    <div class="col-r">{right}</div>
  </div>
</section>"""


def r_ai(s, i0=0):
    pts = "".join(f'<li {ani(2+i)}>{t}</li>' for i, t in enumerate(s.get("items", [])))
    return f"""
<section class="slide s-ai" data-kind="ai">
  {head(s, kicker='AI 前沿')}
  <div class="s-body two">
    <div class="col-l"><div class="ai-card an" style="--i:1">
      <div class="ai-badge">AI</div>
      <p>{s.get('text','')}</p></div></div>
    <div class="col-r"><ul class="blist small ai-list">{pts}</ul></div>
  </div>
</section>"""


def _parse_opt(o):
    """'A. HTML' -> ('A', 'HTML')；无前缀则返回 ('', 原文)"""
    m = re.match(r"^\s*([A-Za-z])\s*[.、．:：)）]\s*([\s\S]*)$", str(o))
    if m:
        return m.group(1).upper(), m.group(2)
    return "", str(o)


def r_quiz(s, i0=0):
    items = s["items"]
    n = len(items)
    dense = " dense" if n >= 4 else ""
    qs = ""
    for i, q in enumerate(items):
        ans_raw = re.sub(r"[^A-Za-z]", "", str(q.get("answer", ""))).upper()
        qtype = (q.get("type") or ("multi" if len(ans_raw) > 1 else "single")).lower()
        tag = "多选" if qtype == "multi" else "单选"
        opts = ""
        for j, o in enumerate(q.get("options", [])):
            k, txt = _parse_opt(o)
            k = k or chr(65 + j)
            opts += (f'<button type="button" class="opt" data-k="{k}">'
                     f'<i>{k}</i><span>{txt}</span></button>')
        ans_txt = "、".join(ans_raw) if ans_raw else ""
        tip = f'<span class="ans-tip">{q.get("tip","")}</span>' if q.get("tip") else ""
        qs += f"""<li class="quiz-item {qtype}" {ani(i+1)} data-type="{qtype}" data-answer="{ans_raw}">
          <div class="q"><span class="q-no">{i+1:02d}</span>
            <span class="q-tag {qtype}">{tag}</span><span class="q-txt">{q["q"]}</span></div>
          <div class="opts">{opts}</div>
          <div class="q-foot"><button type="button" class="q-check">查看答案</button>
            <button type="button" class="q-reset" disabled>重做</button>
            <span class="q-verdict"></span></div>
          <div class="q-ans"><b>答案</b><span class="ans-key">{ans_txt}</span>{tip}</div>
        </li>"""
    return f"""
<section class="slide" data-kind="quiz">
  {head(s, kicker='随堂检测')}
  <div class="s-body quiz-body">
    <div class="quiz-top an" style="--i:0">
      <span class="quiz-meta">共 <b>{n}</b> 题　·　先独立作答，再点「查看答案」；误点可「重做」</span>
      <span class="quiz-acts">
        <button type="button" class="q-reset-all" id="quizResetAll">全部重做</button>
        <button type="button" class="q-reveal" id="quizReveal">显示全部答案</button>
      </span>
    </div>
    <ol class="quiz{dense}">{qs}</ol>
  </div>
</section>"""


def r_objectives(s, i0=0):
    def blk(t, arr, cls):
        return f"""<div class="obj {cls}" {ani(int(cls[-1]) if cls[-1].isdigit() else 1)}>
          <div class="obj-h">{esc(t)}</div><ul>{''.join(f'<li>{esc(x)}</li>' for x in arr)}</ul></div>"""
    o = s.get("objectives", {})
    blocks = ""
    if o.get("knowledge"):
        blocks += blk("知识目标", o["knowledge"], "obj-1")
    if o.get("skill"):
        blocks += blk("技能目标", o["skill"], "obj-2")
    if o.get("literacy"):
        blocks += blk("素养目标", o["literacy"], "obj-3")
    return f"""
<section class="slide" data-kind="objectives">
  {head(s, kicker='学习目标')}
  <div class="s-body"><div class="objs">{blocks}</div></div>
</section>"""


def r_ideology(s, i0=0):
    return f"""
<section class="slide s-ideo" data-kind="ideology">
  {head(s, kicker='思政课堂')}
  <div class="s-body"><div class="ideo-wrap">
    <div class="ideo-quote an" style="--i:1">{s.get('text','')}</div>
    {f'<div class="ideo-topic an" style="--i:2"><span class="it-label">课堂讨论</span>{s.get("topic","")}</div>' if s.get('topic') else ''}
  </div></div>
</section>"""


def r_list_simple(s, i0=0, cls="blist", kicker=None):
    items = "".join(f'<li {ani(i+1)}><span class="bl-dot"></span><span>{t}</span></li>' for i, t in enumerate(s["items"]))
    return f"""
<section class="slide" data-kind="{s.get('type','bullets')}">
  {head(s, kicker=kicker)}
  <div class="s-body"><ul class="{cls}">{items}</ul></div>
</section>"""


def r_refs(s, i0=0):
    items = ""
    for i, r in enumerate(s["items"]):
        t = r["t"] if isinstance(r, dict) else r
        u = r.get("u", "") if isinstance(r, dict) else ""
        link = f'<span class="ref-u">{esc(u)}</span>' if u else ""
        items += f'<li {ani(i+1)}><span class="ref-idx">{i+1:02d}</span><span class="ref-t">{esc(t)}</span>{link}</li>'
    return f"""
<section class="slide" data-kind="refs">
  {head(s, kicker='出处与参考')}
  <div class="s-body"><ol class="refs">{items}</ol></div>
</section>"""


def r_end(s, i0=0):
    nav = s.get("_nav") or {}
    nxt = nav.get("next")
    if nxt:
        nav_html = (f'<a class="end-next an" style="--i:3" href="{esc(nxt["href"])}">'
                    f'<span class="en-lab">下一讲</span>'
                    f'<span class="en-t">{esc(nxt["label"])}</span>'
                    f'<span class="en-ar">→</span></a>')
    elif nav:
        nav_html = ('<div class="end-next is-final an" style="--i:3">'
                    '<span class="en-lab">课程结束</span>'
                    '<span class="en-t">全部 10 个项目已完成 · 祝期末顺利</span></div>')
    else:
        nav_html = ""
    back = (f'<a class="end-back an" style="--i:4" href="{esc(nav["index"])}">'
            f'<span>←</span> 返回总目录</a>') if nav.get("index") else ""
    return f"""
<section class="slide s-end" data-kind="end">
  <div class="end-inner">
    <div class="end-mark an" style="--i:0">·</div>
    <h2 class="end-t an" style="--i:1">{esc(s.get('title','本单元结束'))}</h2>
    <p class="end-s an" style="--i:2">{esc(s.get('text','下次课见 · 记得完成课后作业'))}</p>
    {nav_html}
    {back}
  </div>
</section>"""


RENDER = {
    "cover": r_cover, "section": r_section, "outline": r_outline, "bullets": r_bullets,
    "cards": r_cards, "table": r_table, "compare": r_compare, "steps": r_steps, "flow": r_flow,
    "code": r_code, "codebullets": r_codebullets, "task": r_task, "demo": r_demo, "ai": r_ai,
    "quiz": r_quiz, "objectives": r_objectives, "ideology": r_ideology, "refs": r_refs, "end": r_end,
    "summary": lambda s, i0=0: r_list_simple(s, i0, "blist", "本课小结"),
    "homework": lambda s, i0=0: r_list_simple(s, i0, "blist hw", "课后作业"),
    "notice": lambda s, i0=0: r_list_simple(s, i0, "blist", "温馨提示"),
}


# ---------------------------------------------------------------- 生成完整 HTML
def render_html(unit, nav=None):
    """nav: {"next": {"href","label"}, "index": "../index.html"}，仅作用于结束页"""
    nav = nav or {}
    slides = [r_cover(unit)]
    outline = [(unit["title"], "cover")]
    for idx, s in enumerate(unit["slides"]):
        fn = RENDER.get(s["type"])
        if not fn:
            raise ValueError(f"未支持的幻灯片类型: {s['type']}")
        if s["type"] == "end" and (nav.get("next") or nav.get("index")):
            s = dict(s, _nav=nav)
        html_s = fn(s)
        slides.append(html_s)
        label = s.get("nav") or s.get("title") or unit["title"]
        outline.append((label, s.get("type")))

    deck = "\n".join(slides)
    nav = "".join(
        f'<li data-go="{i}"><span class="nv-idx">{i+1:02d}</span><span class="nv-t">{esc(t)}</span></li>'
        for i, (t, _) in enumerate(outline))

    meta = {
        "title": unit["title"],
        "project": f"{unit.get('project','')} · {unit.get('unit','')}",
        "count": len(slides),
    }

    return TEMPLATE.replace("/*__DECK__*/", deck) \
                   .replace("<!--__NAV__-->", nav) \
                   .replace("__TITLE__", esc(unit["title"])) \
                   .replace("__PROJECT__", esc(f"{unit.get('project','')} · {unit.get('unit','')}")) \
                   .replace("__COUNT__", str(len(slides)))


# ---------------------------------------------------------------- HTML 模板（CSS + JS）
TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · 网页制作课件</title>
<style>
:root{
  --bg:#EEF3FB; --bg2:#F7FAFF; --surface:#fff; --ink:#0E1B2E; --muted:#5A6C85;
  --brand:#2F6BFF; --brand-dk:#1D46B8; --brand2:#0FB5C9; --violet:#7C5CFF; --accent:#FF8A3D;
  --ok:#12A150; --line:#E1E8F4; --code-bg:#0D1A2B; --code-ink:#DCE7F8;
  --font:'PingFang SC','Microsoft YaHei','Hiragino Sans GB','Source Han Sans SC',system-ui,-apple-system,'Segoe UI',sans-serif;
  --mono:'JetBrains Mono','SF Mono',Menlo,Consolas,'Courier New',monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
.slide{user-select:text;-webkit-user-select:text}
.hud,.legend,.drawer,.kicker,.topbar{user-select:none;-webkit-user-select:none}
::selection{background:rgba(47,107,255,.22)}
html,body{height:100%}
body{background:radial-gradient(1200px 800px at 12% 0%,#e6efff 0%,transparent 55%),
             radial-gradient(1000px 700px at 100% 100%,#e9fbfd 0%,transparent 50%),var(--bg);
     font-family:var(--font);color:var(--ink);overflow:hidden;-webkit-font-smoothing:antialiased}
.wrap{height:100%;display:grid;place-items:center;padding:2.2vh 2.2vh}
.stage{position:relative;width:100%;height:100%;max-width:calc(100vh * 16 / 9);max-height:calc(100vw * 9 / 16);
       aspect-ratio:16/9;background:var(--bg2);border-radius:20px;overflow:hidden;
       box-shadow:0 34px 80px -30px rgba(18,42,92,.42),0 0 0 1px rgba(255,255,255,.7) inset;
       container-type:size}
/* 背景装饰 */
.bgfx{position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:0}
.blob{position:absolute;border-radius:50%;filter:blur(46px);opacity:.5}
.b1{width:38cqw;height:38cqw;left:-10cqw;top:-14cqw;background:linear-gradient(135deg,#bcd4ff,#8fb6ff);animation:float1 18s ease-in-out infinite}
.b2{width:30cqw;height:30cqw;right:-8cqw;top:6cqw;background:linear-gradient(135deg,#b8f0f6,#7fe3ef);animation:float2 22s ease-in-out infinite}
.b3{width:26cqw;height:26cqw;left:22cqw;bottom:-14cqw;background:linear-gradient(135deg,#d9ccff,#b9a6ff);animation:float3 26s ease-in-out infinite}
@keyframes float1{50%{transform:translate(4cqw,3cqw) scale(1.06)}}
@keyframes float2{50%{transform:translate(-4cqw,4cqw) scale(1.08)}}
@keyframes float3{50%{transform:translate(3cqw,-4cqw) scale(1.05)}}
.grid-lines{position:absolute;inset:0;background-image:linear-gradient(rgba(47,107,255,.05) 1px,transparent 1px),
   linear-gradient(90deg,rgba(47,107,255,.05) 1px,transparent 1px);background-size:4cqw 4cqw;opacity:.7}

/* 幻灯片 */
.slide{position:absolute;inset:0;z-index:2;padding:4.4cqw 5cqw 4cqw;display:flex;flex-direction:column;gap:1.9cqw;
  opacity:0;visibility:hidden;transform:translateY(1.4cqw) scale(.99);
  transition:opacity .52s ease,transform .52s cubic-bezier(.2,.7,.2,1),visibility .52s}
.slide.is-active{opacity:1;visibility:visible;transform:none}
.slide.prev{transform:translateY(-1.4cqw) scale(.99)}
.s-head{display:flex;justify-content:space-between;align-items:flex-start;gap:2cqw;flex:0 0 auto}
.kicker{display:inline-block;font-size:1.16cqw;font-weight:700;letter-spacing:.16em;color:var(--brand);
  background:linear-gradient(90deg,rgba(47,107,255,.12),rgba(15,181,201,.12));padding:.42cqw 1cqw;border-radius:999px;margin-bottom:.75cqw}
.s-title{font-size:2.86cqw;font-weight:800;letter-spacing:.01em;line-height:1.2}
.s-sub{margin-top:.6cqw;font-size:1.32cqw;color:var(--muted);line-height:1.55}
.s-body{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:1.5cqw}
.s-body.two{flex-direction:row;align-items:stretch;gap:2.2cqw}
.s-body.two>*{flex:1;min-width:0}
.s-body.col{justify-content:center}
.col-l,.col-r{min-width:0;display:flex;flex-direction:column;justify-content:center;gap:1.2cqw}

/* 入场动画 */
.an{opacity:0}
.is-active .an{animation:rise .66s cubic-bezier(.2,.75,.2,1) both;animation-delay:calc(var(--i,0)*95ms + 120ms)}
@keyframes rise{from{opacity:0;transform:translateY(1.5cqw)}to{opacity:1;transform:none}}

/* 封面 */
.s-cover{flex-direction:row;align-items:center;gap:3cqw;padding:6cqw 6cqw}
.cover-left{flex:1.15;min-width:0;z-index:2}
.brandrow{display:flex;align-items:baseline;gap:.9cqw;margin-bottom:2.1cqw}
.brandmark{font-size:1.7cqw;font-weight:800;color:var(--brand);letter-spacing:.08em}
.brandsub{font-size:1.1cqw;font-weight:700;color:var(--brand2);letter-spacing:.2em}
.cover-title{font-size:4.5cqw;font-weight:900;line-height:1.14;letter-spacing:-.01em;
  background:linear-gradient(120deg,#12306f,#2f6bff 45%,#0fb5c9);-webkit-background-clip:text;background-clip:text;color:transparent}
.cover-sub{margin-top:1.2cqw;font-size:1.55cqw;color:var(--muted);line-height:1.7;max-width:34cqw}
.pills{display:flex;flex-wrap:wrap;gap:.7cqw;margin-top:1.9cqw}
.pill{font-size:1.03cqw;font-weight:700;color:var(--brand-dk);background:rgba(47,107,255,.1);
  border:1px solid rgba(47,107,255,.2);padding:.4cqw 1cqw;border-radius:999px}
.pill{opacity:0}
.is-active .pill{animation:rise .6s both;animation-delay:calc(var(--i)*95ms + 120ms)}
.cover-meta{margin-top:2.3cqw;display:flex;align-items:center;gap:.9cqw;flex-wrap:wrap;font-size:1.02cqw;color:var(--muted)}
.cover-meta b{color:var(--brand);font-size:1.2cqw}
.cover-meta .dot{width:.34cqw;height:.34cqw;border-radius:50%;background:#c3cfe2}
.cover-art{flex:.85;position:relative;min-width:0;display:grid;place-items:center}
.orb{position:absolute;border-radius:50%;filter:blur(10px);opacity:.75}
.o1{width:15cqw;height:15cqw;right:-1cqw;top:2cqw;background:radial-gradient(circle at 30% 30%,#9dc2ff,#4f83ff)}
.o2{width:8cqw;height:8cqw;right:12cqw;bottom:4cqw;background:radial-gradient(circle at 30% 30%,#a9f0f7,#1fc2d6)}
.o3{width:5cqw;height:5cqw;right:3cqw;bottom:12cqw;background:radial-gradient(circle at 30% 30%,#d5c7ff,#8a63ff)}
.orb{animation:orb 9s ease-in-out infinite}
.o2{animation-duration:11s}.o3{animation-duration:13s}
@keyframes orb{50%{transform:translateY(-1.6cqw) scale(1.06)}}
.codewin{position:relative;z-index:2;width:100%;max-width:32cqw;background:var(--code-bg);border-radius:1.2cqw;
  box-shadow:0 30px 60px -22px rgba(13,26,43,.7);overflow:hidden;transform:rotate(-1.5deg);
  animation:rise .8s cubic-bezier(.2,.75,.2,1) .35s both}
.cw-bar{display:flex;gap:.5cqw;padding:.85cqw 1.1cqw;background:rgba(255,255,255,.06)}
.cw-bar i{width:.72cqw;height:.72cqw;border-radius:50%;background:#ff5f57}
.cw-bar i:nth-child(2){background:#febc2e}.cw-bar i:nth-child(3){background:#28c840}
.cw-body{padding:1.3cqw 1.5cqw;font-family:var(--mono);font-size:1.06cqw;line-height:1.85;color:var(--code-ink);white-space:pre;overflow:auto}

/* 章节过渡 */
.s-section{align-items:center;justify-content:center;text-align:center}
.sec-inner{display:flex;flex-direction:column;align-items:center}
.sec-num{font-size:7.6cqw;font-weight:900;line-height:1;
  background:linear-gradient(120deg,#2f6bff,#0fb5c9);-webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:-.03em}
.sec-title{margin-top:1.2cqw;font-size:3.1cqw;font-weight:800}
.sec-line{width:0;height:.4cqw;border-radius:99px;background:linear-gradient(90deg,var(--brand),var(--brand2));margin:1.4cqw 0}
.is-active .sec-line{animation:draw .8s ease .5s both}
@keyframes draw{from{width:0}to{width:11cqw}}
.sec-sub{font-size:1.4cqw;color:var(--muted);max-width:44cqw;line-height:1.7}

/* 要点列表 */
.blist{list-style:none;display:flex;flex-direction:column;gap:1.05cqw}
.blist li{display:flex;gap:.95cqw;align-items:flex-start;font-size:1.42cqw;line-height:1.6;
  background:var(--surface);border:1px solid var(--line);border-radius:.85cqw;padding:1.05cqw 1.3cqw;
  box-shadow:0 8px 22px -16px rgba(20,40,90,.5);transition:transform .25s,box-shadow .25s}
.blist li:hover{transform:translateX(.4cqw);box-shadow:0 12px 26px -16px rgba(47,107,255,.55)}
.blist.small li{font-size:1.24cqw;padding:.85cqw 1.1cqw}
.blist.dense{gap:.68cqw}
.blist.dense li{font-size:1.18cqw;padding:.72cqw 1.1cqw;line-height:1.55}
.outline.dense{gap:.62cqw}
.outline.dense li{padding:.72cqw 1.15cqw}
.outline.dense .ot{font-size:1.16cqw}
.grid.dense{gap:.95cqw}
.card.dense{padding:1.1cqw}
.card.dense .card-t{font-size:1.26cqw;margin-bottom:.4cqw}
.card.dense .card-d{font-size:1.03cqw;line-height:1.55}
.bl-dot{flex:0 0 auto;width:.62cqw;height:.62cqw;border-radius:50%;margin-top:.62cqw;
  background:linear-gradient(135deg,var(--brand),var(--brand2));box-shadow:0 0 0 .28cqw rgba(47,107,255,.12)}
.blist b,.blist strong{color:var(--brand-dk)}
.blist code{font-family:var(--mono);font-size:.92em;background:#eef3ff;color:#1d46b8;padding:.1em .42em;border-radius:.35em}
.hw li{background:linear-gradient(180deg,#fbfcff,#f3f7ff)}

/* 卡片 */
.grid{display:grid;gap:1.3cqw}
.grid.cols-2{grid-template-columns:repeat(2,1fr)}
.grid.cols-3{grid-template-columns:repeat(3,1fr)}
.grid.cols-4{grid-template-columns:repeat(2,1fr)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:1.1cqw;padding:1.5cqw;position:relative;overflow:hidden;
  box-shadow:0 14px 32px -22px rgba(20,40,90,.55);transition:transform .28s,box-shadow .28s,border-color .28s}
.card:hover{transform:translateY(-.5cqw);box-shadow:0 22px 40px -22px rgba(47,107,255,.5);border-color:rgba(47,107,255,.35)}
.card::before{content:"";position:absolute;left:0;top:0;height:100%;width:.3cqw;background:linear-gradient(180deg,var(--brand),var(--brand2))}
.card-ico{font-size:1.75cqw;margin-bottom:.6cqw}
.card-t{font-size:1.42cqw;font-weight:800;margin-bottom:.55cqw}
.card-d{font-size:1.14cqw;color:var(--muted);line-height:1.62}

/* 表格 */
.tbl-wrap{background:var(--surface);border:1px solid var(--line);border-radius:1.1cqw;overflow:hidden;
  box-shadow:0 16px 36px -26px rgba(20,40,90,.6)}
.tbl{width:100%;border-collapse:collapse;font-size:1.16cqw}
.tbl th{background:linear-gradient(180deg,#eef4ff,#e4edff);color:var(--brand-dk);font-weight:800;text-align:left;
  padding:.95cqw 1.2cqw;border-bottom:1px solid #d8e3f7;font-size:1.12cqw;letter-spacing:.02em}
.tbl td{padding:.85cqw 1.2cqw;border-bottom:1px solid var(--line);line-height:1.55}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr:hover{background:#f7faff}
.tbl code{font-family:var(--mono);font-size:.92em;background:#eef3ff;color:#1d46b8;padding:.08em .4em;border-radius:.35em}

/* 对比 */
.cmp-wrap{display:grid;grid-template-columns:1fr 1fr;gap:1.8cqw}
.cmp{border-radius:1.1cqw;padding:1.4cqw;border:1px solid var(--line);background:var(--surface)}
.cmp-h{font-size:1.4cqw;font-weight:800;margin-bottom:.9cqw;display:flex;align-items:center;gap:.6cqw}
.cmp-a .cmp-h{color:var(--brand-dk)}
.cmp-b .cmp-h{color:#b8730f}
.cmp ul{list-style:none;display:flex;flex-direction:column;gap:.7cqw}
.cmp li{font-size:1.16cqw;line-height:1.6;color:var(--muted);padding-left:1.3cqw;position:relative}
.cmp li::before{content:"";position:absolute;left:0;top:.62cqw;width:.5cqw;height:.5cqw;border-radius:2px;background:var(--brand)}
.cmp-b li::before{background:var(--accent)}
.cmp-a{background:linear-gradient(180deg,#f6f9ff,#fff)}

/* 步骤 */
.steps{display:flex;flex-direction:column;gap:1cqw}
.step{display:flex;gap:1.2cqw;align-items:flex-start;background:var(--surface);border:1px solid var(--line);
  border-radius:.9cqw;padding:1cqw 1.25cqw}
.step-n{flex:0 0 auto;width:2.3cqw;height:2.3cqw;border-radius:50%;display:grid;place-items:center;font-weight:800;font-size:1.15cqw;color:#fff;
  background:linear-gradient(135deg,var(--brand),var(--brand2))}
.step-t{font-size:1.3cqw;font-weight:800}
.step-d{font-size:1.12cqw;color:var(--muted);line-height:1.6;margin-top:.25cqw}

/* 流程图 */
.flow{display:flex;align-items:stretch;justify-content:center;gap:0;flex-wrap:nowrap}
.fl{flex:1;min-width:0;background:var(--surface);border:1px solid var(--line);border-radius:1cqw;padding:1.3cqw 1cqw;text-align:center;
  box-shadow:0 12px 28px -22px rgba(20,40,90,.55)}
.fl-ico{font-size:1.9cqw;margin-bottom:.5cqw}
.fl-t{font-size:1.24cqw;font-weight:800;margin-bottom:.35cqw;color:var(--brand-dk)}
.fl-d{font-size:1.02cqw;color:var(--muted);line-height:1.55}
.fl-arrow{flex:0 0 auto;width:2.2cqw;position:relative;display:grid;place-items:center}
.fl-arrow::after{content:"";width:1.4cqw;height:.22cqw;background:linear-gradient(90deg,var(--brand),var(--brand2));border-radius:99px;position:relative}
.fl-arrow::before{content:"";position:absolute;right:.35cqw;width:.6cqw;height:.6cqw;border-top:.2cqw solid var(--brand2);border-right:.2cqw solid var(--brand2);transform:rotate(45deg)}
.flow-note{margin-top:1.3cqw;font-size:1.1cqw;color:var(--muted);text-align:center;background:rgba(47,107,255,.06);border-radius:.8cqw;padding:.8cqw 1.2cqw}

/* 代码 */
.codebox{background:var(--code-bg);border-radius:1.1cqw;overflow:hidden;box-shadow:0 26px 54px -26px rgba(13,26,43,.75)}
.cb-bar{display:flex;align-items:center;gap:.8cqw;padding:.8cqw 1.2cqw;background:rgba(255,255,255,.06);border-bottom:1px solid rgba(255,255,255,.07)}
.cb-lang{font-family:var(--mono);font-size:.92cqw;font-weight:700;color:#7fd7e4;letter-spacing:.12em}
.cb-file{font-family:var(--mono);font-size:.92cqw;color:#7f93ad}
.cb-code{padding:1.25cqw 1.5cqw;font-family:var(--mono);font-size:1.06cqw;line-height:1.78;color:var(--code-ink);white-space:pre;overflow:auto;max-height:100%}
.cb-code .pn{color:#7f93ad}.cb-code .tg{color:#6fd6ff}.cb-code .at{color:#ffcf7a}.cb-code .st{color:#a5e88a}
.cb-code .c{color:#6b8099;font-style:italic}.cb-code .sel{color:#ffb3c8}.cb-code .cls{color:#ffd479}
.cb-code .id{color:#9fe8ff}.cb-code .pc{color:#c8a2ff}.cb-code .prop{color:#8fd3ff}.cb-code .num{color:#f7c774}
.cb-code .fn{color:#d0b0ff}.cb-code .imp{color:#ff8a8a}.cb-code .at-rules{color:#ff9f6b}
.caption{margin-top:1cqw;font-size:1.08cqw;color:var(--muted);line-height:1.6}
.caption b{color:var(--brand-dk)}

/* 任务 */
.task-goal{background:linear-gradient(180deg,#f4f8ff,#eef4ff);border:1px solid #dbe6fb;border-radius:.9cqw;padding:1.05cqw 1.25cqw;
  font-size:1.22cqw;line-height:1.62}
.tg-label{display:inline-block;font-weight:800;color:#fff;background:var(--brand);border-radius:.45cqw;
  font-size:.98cqw;padding:.16cqw .6cqw;margin-right:.6cqw;vertical-align:.08cqw}
.task-steps{list-style:none;counter-reset:ts;display:flex;flex-direction:column;gap:.75cqw}
.task-steps li{counter-increment:ts;position:relative;padding-left:2.3cqw;font-size:1.14cqw;line-height:1.6}
.task-steps li::before{content:counter(ts);position:absolute;left:0;top:.08cqw;width:1.55cqw;height:1.55cqw;border-radius:50%;
  background:rgba(47,107,255,.12);color:var(--brand-dk);font-size:.92cqw;font-weight:800;display:grid;place-items:center}
.task-code{background:var(--code-bg);border-radius:.9cqw;overflow:hidden;box-shadow:0 20px 44px -26px rgba(13,26,43,.7)}

/* 演示 */
.demo-right{display:flex;flex-direction:column;gap:1cqw;height:100%}
.demo-frame{flex:1;width:100%;min-height:0;border:1px solid var(--line);border-radius:1cqw;background:#fff;
  box-shadow:0 22px 46px -26px rgba(20,40,90,.6)}
.demo-code{background:var(--code-bg);border-radius:.9cqw;overflow:hidden}
.demo-code summary{cursor:pointer;color:#9fb6d4;font-size:1.02cqw;padding:.7cqw 1.1cqw;font-family:var(--mono);user-select:none}
.demo-code .cb-code{padding:0 1.2cqw 1.1cqw;font-size:.96cqw}
.hint{margin-top:1cqw;font-size:1.08cqw;color:var(--muted);background:rgba(255,138,61,.1);border-left:.3cqw solid var(--accent);
  border-radius:.6cqw;padding:.8cqw 1.1cqw;line-height:1.6}
.hint b{color:#c2601a}

/* AI */
.ai-card{background:linear-gradient(160deg,#171a3a,#2b2a5e 55%,#3a2a6a);border-radius:1.1cqw;padding:1.7cqw;color:#e8e6ff;
  position:relative;overflow:hidden;box-shadow:0 24px 52px -26px rgba(40,30,90,.8)}
.ai-card::after{content:"";position:absolute;right:-6cqw;top:-6cqw;width:14cqw;height:14cqw;border-radius:50%;
  background:radial-gradient(circle,rgba(124,92,255,.6),transparent 65%);animation:float1 12s ease-in-out infinite}
.ai-badge{display:inline-grid;place-items:center;width:2.6cqw;height:2.6cqw;border-radius:.7cqw;font-weight:900;font-size:1.1cqw;
  background:linear-gradient(135deg,#7c5cff,#0fb5c9);color:#fff;margin-bottom:.9cqw;letter-spacing:.04em}
.ai-card p{font-size:1.22cqw;line-height:1.72;position:relative;z-index:2}
.ai-list li{border-color:rgba(124,92,255,.25);background:linear-gradient(180deg,#fbf9ff,#f5f2ff)}
.ai-list .bl-dot{background:linear-gradient(135deg,#7c5cff,#0fb5c9)}

/* 检测（可交互：点选 → 判分 → 显示解析） */
.quiz-body{justify-content:flex-start;gap:1.1cqw}
.quiz-top{display:flex;align-items:center;justify-content:space-between;gap:1.2cqw;flex:0 0 auto}
.quiz-meta{font-size:1.02cqw;color:var(--muted)}
.quiz-meta b{color:var(--brand);font-size:1.1cqw}
.q-reveal{cursor:pointer;font-family:inherit;font-size:.98cqw;font-weight:700;color:var(--brand-dk);
  background:#eef4ff;border:1px solid #d6e3fb;border-radius:.5cqw;padding:.4cqw .95cqw;transition:.18s}
.q-reveal:hover{background:#e2ecff;border-color:var(--brand)}
.quiz-acts{display:flex;align-items:center;gap:.6cqw;flex:0 0 auto}
.q-reset-all{cursor:pointer;font-family:inherit;font-size:.98cqw;font-weight:700;color:var(--muted);
  background:#fff;border:1px solid var(--line);border-radius:.5cqw;padding:.4cqw .9cqw;transition:.18s}
.q-reset-all:hover{color:var(--accent);border-color:#ffd0a8;background:#fff8f2}
.quiz{list-style:none;display:flex;flex-direction:column;gap:1cqw;overflow:auto;padding-right:.3cqw}
.quiz.dense{gap:.55cqw}
.quiz-body:has(.quiz.dense){gap:.7cqw}
.quiz-item{background:var(--surface);border:1px solid var(--line);border-radius:.9cqw;padding:1cqw 1.2cqw;
  transition:border-color .2s,box-shadow .2s}
.quiz-item.ok{border-color:rgba(18,161,80,.45);box-shadow:0 10px 26px -20px rgba(18,161,80,.7)}
.quiz-item.bad{border-color:rgba(214,83,79,.45);box-shadow:0 10px 26px -20px rgba(214,83,79,.6)}
.quiz.dense .quiz-item{padding:.6cqw .95cqw}
.quiz.dense .q{font-size:1.08cqw}
.quiz.dense .opts{margin-top:.4cqw;gap:.45cqw}
.quiz.dense .opt{font-size:.94cqw;padding:.22cqw .62cqw}
.quiz.dense .q-foot{margin-top:.4cqw;min-height:1.15cqw}
.quiz.dense .q-check{font-size:.88cqw;padding:.16cqw .6cqw}
.quiz.dense .q-verdict{font-size:.9cqw}
.quiz.dense .q-ans{margin-top:.4cqw;font-size:.92cqw;padding:.4cqw .7cqw}
.q{display:flex;gap:.55cqw;align-items:baseline;font-size:1.22cqw;font-weight:700;line-height:1.5}
.quiz.dense .q{font-size:1.12cqw}
.q-no{font-family:var(--mono);font-size:.92cqw;font-weight:800;color:var(--brand);flex:0 0 auto}
.q-tag{flex:0 0 auto;font-size:.8cqw;font-weight:700;color:#fff;background:var(--brand2);
  border-radius:.32cqw;padding:.08cqw .42cqw;letter-spacing:.04em}
.q-tag.multi{background:var(--violet)}
.q-txt{flex:1;min-width:0}
.opts{display:flex;flex-wrap:wrap;gap:.55cqw;margin-top:.62cqw}
.opt{cursor:pointer;display:inline-flex;gap:.42cqw;align-items:center;font-family:inherit;text-align:left;
  font-size:1.02cqw;line-height:1.45;color:#33456b;background:#f5f8ff;border:1px solid #e0e9fb;
  border-radius:.55cqw;padding:.36cqw .8cqw;transition:background .16s,border-color .16s,box-shadow .16s}
.quiz.dense .opt{font-size:.96cqw;padding:.28cqw .7cqw}
.opt:hover{border-color:var(--brand);background:#eef4ff}
.opt i{font-style:normal;font-family:var(--mono);font-weight:800;font-size:.88em;color:var(--brand)}
.opt.sel{background:#e6efff;border-color:var(--brand);box-shadow:0 0 0 .16cqw rgba(47,107,255,.16)}
.opt.right{background:rgba(18,161,80,.1);border-color:#12A150;color:#0b5f2f}
.opt.right i{color:#0b5f2f}
.q-foot{display:flex;align-items:center;gap:.8cqw;margin-top:.6cqw;min-height:1.5cqw}
.q-check{cursor:pointer;font-family:inherit;font-size:.94cqw;font-weight:700;color:var(--brand);
  background:#fff;border:1px solid #c9daff;border-radius:.45cqw;padding:.26cqw .75cqw;transition:.16s}
.q-check:hover{background:#eef4ff}
.q-reset{cursor:pointer;font-family:inherit;font-size:.94cqw;font-weight:700;color:var(--muted);
  background:#fff;border:1px solid var(--line);border-radius:.45cqw;padding:.26cqw .7cqw;transition:.16s}
.q-reset:hover{color:var(--accent);border-color:#ffd0a8;background:#fff8f2}
.q-reset:disabled{opacity:.38;cursor:default}
.q-reset:disabled:hover{color:var(--muted);border-color:var(--line);background:#fff}
.quiz.dense .q-reset{font-size:.88cqw;padding:.16cqw .55cqw}
.q-verdict{font-size:.96cqw;font-weight:700}
.quiz-item.ok .q-verdict{color:var(--ok)}
.quiz-item.bad .q-verdict{color:#d9534f}
.q-ans{display:none;margin-top:.6cqw;font-size:.98cqw;line-height:1.6;color:#0f7a3d;
  background:rgba(18,161,80,.08);border-radius:.5cqw;padding:.5cqw .8cqw}
.quiz-item.revealed .q-ans{display:block;animation:rise .3s both}
.q-ans b{color:#0b5f2f;margin-right:.45cqw}
.ans-key{font-family:var(--mono);font-weight:800;margin-right:.6cqw}
.ans-tip{color:var(--muted)}

/* 目标 */
.objs{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4cqw}
.obj{border-radius:1.1cqw;padding:1.4cqw;border:1px solid var(--line);background:var(--surface)}
.obj-h{font-size:1.3cqw;font-weight:800;margin-bottom:.85cqw;display:flex;align-items:center;gap:.55cqw}
.obj-h::before{content:"";width:.55cqw;height:1.35cqw;border-radius:99px}
.obj ul{list-style:none;display:flex;flex-direction:column;gap:.62cqw}
.obj li{font-size:1.1cqw;line-height:1.58;color:var(--muted);padding-left:1.15cqw;position:relative}
.obj li::before{content:"";position:absolute;left:0;top:.6cqw;width:.42cqw;height:.42cqw;border-radius:50%;background:#9db4d6}
.obj-1 .obj-h::before{background:var(--brand)}.obj-2 .obj-h::before{background:var(--brand2)}.obj-3 .obj-h::before{background:var(--accent)}
.obj-1 .obj-h{color:var(--brand-dk)}.obj-2 .obj-h{color:#0a7b87}.obj-3 .obj-h{color:#b8730f}

/* 思政 */
.s-ideo .s-body{justify-content:center}
.ideo-wrap{display:flex;flex-direction:column;gap:1.3cqw}
.ideo-quote{position:relative;background:linear-gradient(180deg,#fff8f0,#fffbf6);border:1px solid #ffe3c8;border-left:.42cqw solid var(--accent);
  border-radius:.95cqw;padding:1.6cqw 1.8cqw 1.6cqw 2.2cqw;font-size:1.3cqw;line-height:1.85;color:#4a3a28}
.ideo-quote strong{color:#a3510a}
.ideo-topic{font-size:1.16cqw;color:var(--muted);background:rgba(47,107,255,.06);border-radius:.8cqw;padding:.9cqw 1.2cqw;line-height:1.6}
.it-label{display:inline-block;font-weight:800;color:#fff;background:var(--brand);border-radius:.45cqw;font-size:.96cqw;padding:.16cqw .6cqw;margin-right:.6cqw}

/* 大纲 */
.outline{list-style:none;display:flex;flex-direction:column;gap:.95cqw;counter-reset:none}
.outline li{display:flex;align-items:center;gap:1.2cqw;background:var(--surface);border:1px solid var(--line);border-radius:.9cqw;padding:1.05cqw 1.35cqw;
  box-shadow:0 10px 26px -22px rgba(20,40,90,.55)}
.oi{font-family:var(--mono);font-size:1.1cqw;font-weight:800;color:var(--brand);background:rgba(47,107,255,.1);border-radius:.5cqw;padding:.28cqw .7cqw}
.ot{font-size:1.34cqw;font-weight:700}

/* 参考 */
.refs{list-style:none;display:flex;flex-direction:column;gap:.85cqw}
.refs li{display:flex;align-items:baseline;gap:.9cqw;background:var(--surface);border:1px solid var(--line);border-radius:.8cqw;padding:.9cqw 1.15cqw}
.ref-idx{font-family:var(--mono);font-size:1cqw;font-weight:800;color:var(--brand)}
.ref-t{font-size:1.16cqw;font-weight:600}
.ref-u{font-family:var(--mono);font-size:.92cqw;color:var(--muted);word-break:break-all}

/* 结束 */
.s-end{align-items:center;justify-content:center;text-align:center;background:linear-gradient(140deg,#12203b,#1d3a78 55%,#0e6f88);}
.s-end .end-t{color:#fff}
.end-mark{font-size:2.4cqw;color:#7fd7e4;margin-bottom:.6cqw}
.end-t{font-size:3.4cqw;font-weight:900;letter-spacing:.02em}
.end-s{margin-top:1.2cqw;font-size:1.35cqw;color:#a9c4e8}
/* 结束页导航：下一讲 / 返回总目录 */
.end-inner{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.9cqw;max-width:74%}
.end-next{margin-top:2.6cqw;display:inline-flex;align-items:center;gap:1cqw;text-decoration:none;
  background:rgba(255,255,255,.09);border:1px solid rgba(140,200,235,.42);border-radius:.9cqw;
  padding:1cqw 1.5cqw;transition:.22s;backdrop-filter:blur(6px);max-width:100%}
.end-next:hover{background:rgba(255,255,255,.16);border-color:#7fd7e4;transform:translateY(-2px);
  box-shadow:0 18px 40px -26px rgba(0,0,0,.9)}
.en-lab{flex:0 0 auto;font-size:.92cqw;font-weight:800;letter-spacing:.06em;color:#0c2036;
  background:linear-gradient(135deg,#7fd7e4,#4fc3d9);border-radius:.4cqw;padding:.2cqw .62cqw}
.en-t{color:#eaf4ff;font-size:1.18cqw;font-weight:700;line-height:1.5}
.en-ar{color:#7fd7e4;font-size:1.3cqw;font-weight:800}
.end-next.is-final{cursor:default;box-shadow:none}
.end-next.is-final:hover{transform:none;background:rgba(255,255,255,.09);border-color:rgba(140,200,235,.42);box-shadow:none}
.end-back{margin-top:.5cqw;display:inline-flex;align-items:center;gap:.35cqw;text-decoration:none;
  font-size:1.02cqw;color:#9fbde0;border-bottom:1px dashed rgba(159,189,224,.45);padding-bottom:.12cqw;transition:.2s}
.end-back:hover{color:#fff;border-bottom-color:#7fd7e4}

/* 进度 & HUD */
.topbar{position:absolute;left:0;top:0;height:.42cqw;width:100%;background:rgba(47,107,255,.1);z-index:6}
.topbar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--brand),var(--brand2),var(--violet));
  transition:width .45s cubic-bezier(.2,.7,.2,1)}
.hud{position:absolute;right:2.2cqw;bottom:1.5cqw;z-index:6;display:flex;align-items:center;gap:1cqw;
  font-size:1cqw;color:var(--muted);font-family:var(--mono)}
.hud .btn{cursor:pointer;background:rgba(255,255,255,.82);border:1px solid var(--line);border-radius:.55cqw;padding:.32cqw .7cqw;
  transition:.2s}
.hud .btn:hover{border-color:var(--brand);color:var(--brand)}
.hud .btn[data-on="0"]{color:#a8b6cc;background:rgba(255,255,255,.5);border-style:dashed}
.hud .btn[data-on="0"]:hover{color:var(--accent);border-color:#ffd0a8;border-style:solid;background:#fff8f2}
.hud .btn[data-on="1"]{color:#0a7b87;border-color:#bfe6ea;background:rgba(15,181,201,.09)}
.hud .btn[data-on="1"]:hover{border-color:var(--brand2);background:rgba(15,181,201,.16)}
.pageno b{color:var(--ink)}
.legend{position:absolute;left:2.2cqw;bottom:1.5cqw;z-index:6;font-size:.96cqw;color:#9aabc4;font-family:var(--mono)}
.flip-toast{position:absolute;left:50%;bottom:9%;z-index:9;transform:translate(-50%,10px);
  background:rgba(16,29,50,.9);color:#fff;font-family:var(--mono);font-size:1.02cqw;letter-spacing:.02em;
  padding:.62cqw 1.25cqw;border-radius:999px;opacity:0;pointer-events:none;white-space:nowrap;
  transition:opacity .22s,transform .22s;box-shadow:0 18px 40px -22px rgba(0,0,0,.8)}
.flip-toast.show{opacity:1;transform:translate(-50%,0)}
/* 导航抽屉 */
.drawer{position:absolute;inset:0;z-index:8;background:rgba(12,22,40,.55);backdrop-filter:blur(6px);display:none;padding:4cqw}
.drawer.open{display:block}
.drawer-panel{background:var(--surface);border-radius:1.2cqw;height:100%;padding:2cqw;overflow:auto;box-shadow:0 40px 80px -30px rgba(0,0,0,.5)}
.drawer-h{font-size:1.5cqw;font-weight:800;margin-bottom:1.2cqw;display:flex;justify-content:space-between}
.drawer-h span{cursor:pointer;color:var(--muted);font-weight:600;font-size:1.1cqw}
.drawer ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:.55cqw}
.drawer li{display:flex;gap:.7cqw;align-items:center;padding:.6cqw .8cqw;border-radius:.6cqw;cursor:pointer;border:1px solid transparent}
.drawer li:hover{background:#f2f6ff;border-color:#dbe6fb}
.drawer li.cur{background:#eaf1ff;border-color:#c9daff}
.nv-idx{font-family:var(--mono);font-size:.92cqw;color:var(--brand);font-weight:800}
.nv-t{font-size:1.06cqw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
/* ───────── 屏幕自适应 ─────────
   1) 16:9 / 16:10 笔记本与投影：等比缩放（默认）
   2) 4:3 老投影 / 上下更紧：压缩留白与圆角
   3) 超宽屏：仍按高度定宽，不拉伸变形
   4) 竖屏（手机、平板竖握）：改为纵向流式阅读，单列重排
   5) 系统开启「减弱动效」时关闭所有动画
*/
@media (max-aspect-ratio: 4/3) and (orientation: landscape){
  .wrap{padding:1.2vh}
  .stage{border-radius:14px}
  .slide{padding:3.4cqw 4.2cqw 3.2cqw;gap:1.5cqw}
  .s-title{font-size:2.62cqw}
  .blist{gap:.85cqw}
  .blist li{font-size:1.32cqw;padding:.9cqw 1.15cqw}
  .legend{display:none}
}
@media (min-aspect-ratio: 21/9){
  .stage{max-width:calc(100vh * 16 / 9);max-height:calc(100vw * 9 / 16)}
}
@media (prefers-reduced-motion: reduce){
  .an{opacity:1!important;animation:none!important}
  .blob,.orb,.codewin{animation:none!important}
  .slide{transition:none}
}
/* —— 竖屏：纵向流式阅读 —— */
@media (orientation: portrait){
  html,body{height:auto;overflow-x:hidden;overflow-y:auto}
  html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
  body{overflow:visible;background:var(--bg)}
  .wrap{display:block;height:auto;padding:0}
  .stage{width:100%;height:auto;max-width:none;max-height:none;aspect-ratio:auto;border-radius:0;
    overflow:visible;box-shadow:none;container-type:inline-size;background:transparent}
  .bgfx{display:none}
  .slide{position:relative;inset:auto;opacity:1!important;visibility:visible!important;transform:none!important;
    padding:8vw 6vw 9vw;gap:5vw;min-height:auto;background:var(--bg2);border-bottom:1px solid var(--line)}
  .slide.prev{transform:none!important}
  .an{opacity:1!important;animation:none!important;transform:none!important}
  .s-head{flex-direction:column;gap:0}
  .kicker{font-size:2.6vw;padding:1vw 2.6vw;margin-bottom:2.2vw;letter-spacing:.1em}
  .s-title{font-size:6.4vw;line-height:1.3}
  .s-sub{margin-top:2vw;font-size:3.4vw}
  .s-body{gap:4vw;justify-content:flex-start}
  .s-body.two{flex-direction:column;gap:4.4vw}
  .col-l,.col-r{gap:3.4vw}
  /* 封面 */
  .s-cover{flex-direction:column;align-items:flex-start;gap:5vw;padding:12vw 6vw 10vw}
  .cover-art{display:none}
  .brandrow{margin-bottom:4vw;gap:2vw}
  .brandmark{font-size:4.4vw}.brandsub{font-size:3vw}
  .cover-title{font-size:9.6vw;line-height:1.22}
  .cover-sub{font-size:3.8vw;max-width:none;margin-top:2.6vw}
  .pills{gap:2vw;margin-top:4vw}
  .pill{font-size:2.8vw;padding:1.2vw 2.8vw}
  .cover-meta{font-size:2.9vw;gap:2vw;margin-top:4vw}
  .cover-meta b{font-size:3.4vw}
  /* 章节页 */
  .sec-num{font-size:17vw}
  .sec-title{font-size:7.2vw;margin-top:3vw}
  .sec-sub{font-size:3.6vw;max-width:none;margin-top:3vw}
  .is-active .sec-line{animation:none;width:26vw}
  .sec-line{margin:4vw 0}
  /* 列表 / 卡片 */
  .blist{gap:2.6vw}
  .blist li{font-size:3.7vw;padding:2.8vw 3.4vw;border-radius:2.4vw;gap:2.4vw;line-height:1.62}
  .blist.small li{font-size:3.4vw;padding:2.4vw 3vw}
  .blist.dense li{font-size:3.3vw;padding:2.2vw 3vw}
  .bl-dot{width:1.8vw;height:1.8vw;margin-top:1.8vw;box-shadow:0 0 0 .8vw rgba(47,107,255,.12)}
  .outline{gap:2.4vw}
  .outline li{padding:2.8vw 3.4vw;border-radius:2.2vw;gap:3vw}
  .oi{font-size:2.8vw;padding:.8vw 2vw}
  .ot{font-size:3.9vw}
  .grid{gap:3vw}
  .grid.cols-2,.grid.cols-3,.grid.cols-4{grid-template-columns:1fr}
  .card{padding:4.2vw;border-radius:2.6vw}
  .card-t{font-size:4.1vw;margin-bottom:1.6vw}
  .card-d{font-size:3.3vw}
  .card-ico{font-size:5.6vw;margin-bottom:1.6vw}
  .card::before{width:.8vw}
  /* 表格 */
  .tbl-wrap{overflow-x:auto;border-radius:2.4vw;-webkit-overflow-scrolling:touch}
  .tbl{font-size:3.1vw;min-width:110vw}
  .tbl th{font-size:3vw;padding:2.4vw 2.8vw;white-space:nowrap}
  .tbl td{padding:2.2vw 2.8vw}
  /* 对比 */
  .cmp-wrap{grid-template-columns:1fr;gap:3.4vw}
  .cmp{padding:3.6vw;border-radius:2.4vw}
  .cmp-h{font-size:3.8vw;margin-bottom:2.4vw}
  .cmp ul{gap:2vw}
  .cmp li{font-size:3.2vw;padding-left:3.6vw}
  .cmp li::before{width:1.4vw;height:1.4vw;top:1.7vw}
  /* 步骤 / 流程 */
  .steps{gap:2.6vw}
  .step{padding:3vw 3.4vw;border-radius:2.2vw;gap:3vw}
  .step-n{width:7.4vw;height:7.4vw;font-size:3.2vw}
  .step-t{font-size:3.7vw}
  .step-d{font-size:3.2vw;margin-top:.8vw}
  .flow{flex-direction:column;gap:1.6vw}
  .fl{padding:3.6vw;border-radius:2.4vw}
  .fl-ico{font-size:6.4vw}
  .fl-t{font-size:3.9vw}
  .fl-d{font-size:3.1vw}
  .fl-arrow{width:100%;height:6vw;transform:rotate(90deg)}
  .flow-note{font-size:3.1vw;padding:2.4vw 3vw;border-radius:2vw;margin-top:2.6vw}
  /* 代码 */
  .codebox,.task-code{border-radius:2.4vw}
  .cb-bar{padding:2.2vw 3vw;gap:2.4vw}
  .cb-lang,.cb-file{font-size:2.7vw}
  .cb-code{font-size:3.1vw;line-height:1.62;padding:3vw 3.4vw}
  .caption{font-size:3vw;margin-top:2.4vw}
  .demo-code summary{font-size:2.9vw;padding:2.2vw 3vw}
  .demo-code .cb-code{font-size:2.9vw}
  /* 任务 / 演示 */
  .task-goal{font-size:3.4vw;padding:3.2vw;border-radius:2.2vw}
  .tg-label{font-size:2.6vw;padding:.5vw 1.8vw;margin-right:1.6vw;border-radius:1.2vw}
  .task-steps{gap:2.4vw}
  .task-steps li{font-size:3.3vw;padding-left:6.4vw}
  .task-steps li::before{width:4.6vw;height:4.6vw;font-size:2.8vw}
  .demo-right{height:auto;gap:2.6vw}
  .demo-frame{height:66vw;min-height:190px;border-radius:2.4vw}
  .hint{font-size:3.1vw;padding:2.6vw 3vw;border-radius:2vw;margin-top:2.6vw}
  /* AI */
  .ai-card{padding:4.4vw;border-radius:2.6vw}
  .ai-card p{font-size:3.5vw}
  .ai-badge{width:8.4vw;height:8.4vw;font-size:3.2vw;border-radius:2vw;margin-bottom:2.4vw}
  /* 检测（!important：压过横屏 dense 的 cqw 规则，否则竖屏字号塌缩） */
  .quiz-body{gap:3.4vw}
  .quiz-top{flex-direction:column;align-items:flex-start;gap:2.4vw}
  .quiz-meta{font-size:3vw}
  .quiz-meta b{font-size:3.4vw}
  .quiz-acts{gap:2vw}
  .q-reveal,.q-reset-all{font-size:3vw;padding:1.6vw 3.4vw;border-radius:2vw}
  .quiz{gap:3vw;overflow:visible}
  .quiz.dense{gap:2.6vw}
  .quiz-item,.quiz.dense .quiz-item{padding:3.4vw 3.6vw;border-radius:2.4vw}
  .quiz.dense .q{font-size:3.6vw;gap:1.6vw;line-height:1.55}
  .q-no{font-size:2.9vw}
  .q-tag{font-size:2.4vw;padding:.3vw 1.4vw;border-radius:1.2vw}
  .opts,.quiz.dense .opts{gap:1.8vw;margin-top:2.2vw}
  .opt,.quiz.dense .opt{font-size:3.2vw;padding:1.4vw 2.8vw;border-radius:2vw;gap:1.4vw}
  .q-foot,.quiz.dense .q-foot{margin-top:2vw;gap:2.4vw;min-height:0}
  .q-check,.quiz.dense .q-check{font-size:2.9vw;padding:1.2vw 2.8vw;border-radius:1.6vw}
  .q-reset,.quiz.dense .q-reset{font-size:2.9vw;padding:1.2vw 2.6vw;border-radius:1.6vw}
  .q-verdict,.quiz.dense .q-verdict{font-size:2.9vw}
  .q-ans,.quiz.dense .q-ans{font-size:3vw;padding:2.2vw 3vw;border-radius:1.8vw;margin-top:2vw}
  /* 目标 / 思政 */
  .objs{grid-template-columns:1fr;gap:3vw}
  .obj{padding:4vw;border-radius:2.4vw}
  .obj-h{font-size:3.9vw;margin-bottom:2.4vw}
  .obj-h::before{width:1.4vw;height:4vw}
  .obj ul{gap:2vw}
  .obj li{font-size:3.2vw;padding-left:3.4vw}
  .obj li::before{width:1.2vw;height:1.2vw;top:1.6vw}
  .ideo-wrap{gap:3.4vw}
  .ideo-quote{font-size:3.6vw;padding:4vw 4.4vw;border-radius:2.4vw;line-height:1.8}
  .ideo-topic{font-size:3.2vw;padding:2.8vw 3.2vw;border-radius:2.2vw}
  .it-label{font-size:2.6vw;padding:.5vw 1.6vw;border-radius:1.2vw;margin-right:1.4vw}
  /* 参考 / 结束 */
  .refs{gap:2.2vw}
  .refs li{padding:2.8vw 3.2vw;border-radius:2vw;gap:2.4vw}
  .ref-idx{font-size:2.8vw}
  .ref-t{font-size:3.3vw}
  .ref-u{font-size:2.7vw}
  .s-end{align-items:center;justify-content:center;min-height:60vh}
  .end-t{font-size:8.4vw}
  .end-s{font-size:3.6vw;margin-top:3vw}
  .end-mark{font-size:6vw}
  .end-inner{max-width:none;width:100%;gap:2vw}
  .end-next{margin-top:5vw;gap:2.2vw;padding:3vw 3.6vw;border-radius:2.4vw;flex-wrap:wrap;justify-content:center}
  .en-lab{font-size:2.6vw;padding:.8vw 2vw;border-radius:1.2vw}
  .en-t{font-size:3.4vw}
  .en-ar{font-size:3.6vw}
  .end-back{font-size:3vw;margin-top:2.6vw}
  /* HUD / 目录：固定悬浮 */
  .topbar{position:fixed;height:1.2vw;z-index:20}
  .hud{position:fixed;right:3vw;bottom:calc(3vw + env(safe-area-inset-bottom));z-index:20;
    background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:999px;
    padding:2.2vw 3.4vw;gap:3vw;font-size:3vw;box-shadow:0 10px 30px -12px rgba(16,34,74,.35)}
  .hud .btn{font-size:2.9vw;padding:1vw 2.4vw;border-radius:1.6vw}
  .flip-toast{position:fixed;bottom:calc(16vw + env(safe-area-inset-bottom));z-index:21;
    font-size:3vw;padding:2.2vw 4vw;max-width:84vw;white-space:normal;text-align:center;line-height:1.5}
  .legend{display:none}
  .drawer{position:fixed;padding:4vw}
  .drawer-panel{padding:5vw;border-radius:3vw}
  .drawer-h{font-size:4.2vw;margin-bottom:3vw}
  .drawer-h span{font-size:3.2vw}
  .drawer ul{grid-template-columns:1fr;gap:1.6vw}
  .drawer li{padding:2.4vw 3vw;border-radius:2vw;gap:2.4vw}
  .nv-idx{font-size:2.8vw}
  .nv-t{font-size:3.2vw;white-space:normal}
}
/* 打印 */
@media print{
  body{overflow:visible}
  .wrap{padding:0;display:block}
  .stage{width:100%;max-width:none;height:auto;aspect-ratio:auto;border-radius:0;box-shadow:none}
  .slide{position:relative;opacity:1!important;visibility:visible!important;transform:none!important;
    page-break-after:always;height:100vh;width:100%}
  .an{opacity:1!important;animation:none!important}
  .topbar,.hud,.legend,.drawer{display:none!important}
}
</style>
</head>
<body>
<div class="wrap"><div class="stage" id="stage">
  <div class="bgfx"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="grid-lines"></div></div>
  <div class="topbar"><i id="bar"></i></div>
/*__DECK__*/
  <div class="legend">← → 翻页　·　C 点击翻页开关　·　O 目录　·　F 全屏　·　P 打印　·　拖动圈选不翻页</div>
  <div class="hud">
    <span class="btn" id="btnClick" data-on="1" title="开启 / 关闭「点击鼠标切换页面」（快捷键 C）">点击翻页 开</span>
    <span class="btn" id="btnNav">目录</span>
    <span class="btn" id="btnFull">全屏</span>
    <span class="pageno"><b id="cur">1</b> / __COUNT__</span>
  </div>
  <div class="flip-toast" id="flipToast"></div>
  <div class="drawer" id="drawer">
    <div class="drawer-panel">
      <div class="drawer-h">本单元目录 <span id="drawerClose">关闭 ✕</span></div>
      <ul id="drawerList"><!--__NAV__--></ul>
    </div>
  </div>
</div></div>
<script>
(function(){
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var total = slides.length, cur = 0;
  var stage = document.getElementById('stage');
  var bar = document.getElementById('bar'), curEl = document.getElementById('cur');
  var drawer = document.getElementById('drawer');
  var mqPortrait = window.matchMedia('(orientation: portrait)');
  var flow = mqPortrait.matches;

  /* ---- 点击翻页开关（记忆教师偏好，跨课件生效） ---- */
  var clickOn = true;
  try{ clickOn = localStorage.getItem('deck_clickflip') !== '0'; }catch(e){}
  var btnClick = document.getElementById('btnClick');
  var toastEl = document.getElementById('flipToast'), toastTimer = null;
  function tip(msg){
    if(!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function(){ toastEl.classList.remove('show'); }, 1500);
  }
  function syncClickBtn(){
    if(!btnClick) return;
    if(flow){                                   // 竖屏为滚屏阅读，点击翻页天然不生效
      btnClick.textContent = '竖屏阅读';
      btnClick.setAttribute('data-on', '0');
      btnClick.setAttribute('title', '竖屏为纵向阅读模式，上下滚动即可；旋转为横屏后可用点击翻页');
      return;
    }
    btnClick.textContent = '点击翻页 ' + (clickOn ? '开' : '关');
    btnClick.setAttribute('data-on', clickOn ? '1' : '0');
    btnClick.setAttribute('title', clickOn
      ? '当前：点击鼠标可切换页面。点此关闭（快捷键 C）'
      : '当前：点击鼠标不翻页，方便圈选讲解。点此开启（快捷键 C）');
  }
  function toggleClickFlip(silent){
    clickOn = !clickOn;
    try{ localStorage.setItem('deck_clickflip', clickOn ? '1' : '0'); }catch(e){}
    syncClickBtn();
    if(!silent) tip(clickOn ? '点击翻页已开启' : '点击翻页已关闭 · 仍可用 ← → 或滑动翻页');
  }
  syncClickBtn();

  function hasSelection(){
    var s = window.getSelection && window.getSelection();
    return !!(s && String(s.text || s).length > 0);
  }
  function setIndex(n){
    cur = Math.max(0, Math.min(total-1, n));
    slides.forEach(function(s,i){ s.classList.toggle('is-active', i===cur); });
    var act = slides[cur];
    if(act && !flow) act.querySelectorAll('.an').forEach(function(el){ void el.offsetWidth; });
    bar.style.width = (total>1 ? (cur/(total-1)*100) : 100)+'%';
    curEl.textContent = cur+1;
    document.querySelectorAll('#drawerList li').forEach(function(li,i){ li.classList.toggle('cur', i===cur); });
  }
  function go(n, instant){
    n = Math.max(0, Math.min(total-1, n));
    var same = (n===cur && slides[cur] && slides[cur].classList.contains('is-active'));
    slides.forEach(function(s,i){
      s.classList.remove('prev');
      if(i<n) s.classList.add('prev');
      if(i===n) s.classList.add('is-active');
    });
    setIndex(n);
    if(flow){
      var el = slides[n];
      if(el && el.scrollIntoView) el.scrollIntoView({behavior: instant ? 'auto' : 'smooth', block:'start'});
    } else if(same){
      var a = slides[n]; if(a) a.querySelectorAll('.an').forEach(function(el){ void el.offsetWidth; });
    }
    try{ history.replaceState(null,'','#'+(n+1)); }catch(e){}
  }

  /* 键盘 */
  document.addEventListener('keydown', function(e){
    var k = e.key;
    if(k==='ArrowRight'||k==='ArrowDown'||k===' '||k==='PageDown'||k==='Enter'){ e.preventDefault(); go(cur+1); }
    else if(k==='ArrowLeft'||k==='ArrowUp'||k==='PageUp'){ e.preventDefault(); go(cur-1); }
    else if(k==='Home'){ go(0); } else if(k==='End'){ go(total-1); }
    else if(k==='o'||k==='O'){ drawer.classList.toggle('open'); }
    else if(k==='f'||k==='F'){ toggleFull(); }
    else if(k==='c'||k==='C'){ toggleClickFlip(); }
    else if(k==='Escape'){ drawer.classList.remove('open'); }
    else if(k==='p'||k==='P'){ window.print(); }
  });
  function toggleFull(){
    if(!document.fullscreenElement){ (document.documentElement.requestFullscreen||function(){}).call(document.documentElement); }
    else { document.exitFullscreen(); }
  }

  /* 点击翻页：拖动圈选文字、双击选词、点按钮/选项一律不翻页 */
  var down = null, clickTimer = null;
  function isInteractive(el){
    return !!(el.closest('.hud')||el.closest('.drawer')||el.closest('iframe')||el.closest('summary')||
              el.closest('details')||el.closest('.quiz')||el.closest('a')||el.closest('button')||
              el.closest('input')||el.closest('select')||el.closest('textarea')||el.closest('label'));
  }
  stage.addEventListener('mousedown', function(e){ down = {x:e.clientX, y:e.clientY, t:Date.now()}; });
  stage.addEventListener('click', function(e){
    if(flow) return;
    clearTimeout(clickTimer);
    if(!clickOn) return;                           // 开关关闭：点击不翻页
    if(e.detail > 1) return;                       // 双击 / 三击 = 选词，不翻页
    if(isInteractive(e.target)) return;
    if(hasSelection()) return;                     // 已有选中内容，不翻页
    if(down && (Math.abs(e.clientX-down.x)>6 || Math.abs(e.clientY-down.y)>6)) return;  // 拖动圈选
    if(down && (Date.now()-down.t > 800)) return;  // 长按
    var r = stage.getBoundingClientRect();
    var dir = (e.clientX - r.left) > r.width*0.5 ? 1 : -1;
    clickTimer = setTimeout(function(){
      if(hasSelection()) return;                   // 圈选期间保持静止
      go(cur+dir);
    }, 220);
  });
  document.addEventListener('dblclick', function(){ clearTimeout(clickTimer); });
  document.addEventListener('selectionchange', function(){ if(hasSelection()) clearTimeout(clickTimer); });

  /* 触摸：仅在横向滑动时翻页；竖屏交给页面滚动 */
  var sx=null, sy=null, st=0;
  stage.addEventListener('touchstart', function(e){
    if(e.touches.length>1){ sx=null; return; }
    sx=e.touches[0].clientX; sy=e.touches[0].clientY; st=Date.now();
  }, {passive:true});
  stage.addEventListener('touchend', function(e){
    if(sx===null) return;
    var dx=e.changedTouches[0].clientX-sx, dy=e.changedTouches[0].clientY-sy;
    sx=null;
    if(flow) return;
    if(Date.now()-st>900) return;                  // 长按选词
    if(hasSelection()) return;
    if(Math.abs(dx)>55 && Math.abs(dy)<Math.abs(dx)*0.75) go(dx<0?cur+1:cur-1);
  }, {passive:true});

  /* 竖屏：滚动时同步页码与进度 */
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      if(!flow) return;
      var best=null;
      entries.forEach(function(en){
        if(en.isIntersecting && (!best || en.intersectionRatio > best.intersectionRatio)) best = en;
      });
      if(best){
        var i = slides.indexOf(best.target);
        if(i>=0 && i!==cur) setIndex(i);
      }
    }, {threshold:[0.2,0.5,0.8]});
    slides.forEach(function(s){ io.observe(s); });
  }
  function onOrient(){
    flow = mqPortrait.matches;
    syncClickBtn();
    clearTimeout(clickTimer);
  }
  mqPortrait.addEventListener ? mqPortrait.addEventListener('change', onOrient) : mqPortrait.addListener(onOrient);

  /* 目录 / HUD */
  if(btnClick) btnClick.addEventListener('click', function(e){ e.stopPropagation(); toggleClickFlip(); });
  document.getElementById('btnNav').addEventListener('click', function(e){ e.stopPropagation(); drawer.classList.add('open'); });
  document.getElementById('btnFull').addEventListener('click', function(e){ e.stopPropagation(); toggleFull(); });
  document.getElementById('drawerClose').addEventListener('click', function(){ drawer.classList.remove('open'); });
  drawer.addEventListener('click', function(e){ if(e.target===drawer) drawer.classList.remove('open'); });
  document.querySelectorAll('#drawerList li').forEach(function(li){
    li.addEventListener('click', function(){ go(parseInt(li.dataset.go,10)); drawer.classList.remove('open'); });
  });

  /* 随堂检测：点选选项 → 判分 → 显示答案与解析 → 单选/全量重做 */
  function keysOf(item){
    return (item.getAttribute('data-answer')||'').toUpperCase().replace(/[^A-Z]/g,'').split('');
  }
  function reveal(item){
    var ans = keysOf(item);
    item.querySelectorAll('.opt').forEach(function(b){
      if(ans.indexOf(b.getAttribute('data-k'))>=0) b.classList.add('right');
    });
    item.classList.add('revealed');
  }
  function resetItem(item){
    item.classList.remove('revealed','ok','bad');
    item.querySelectorAll('.opt').forEach(function(b){ b.classList.remove('right','sel'); });
    var v = item.querySelector('.q-verdict'); if(v) v.textContent='';
    var rs = item.querySelector('.q-reset'); if(rs) rs.disabled = true;
  }
  document.querySelectorAll('.quiz-item').forEach(function(item){
    var qtype = item.getAttribute('data-type')||'single';
    var btnReset = item.querySelector('.q-reset');
    item.querySelectorAll('.opt').forEach(function(btn){
      btn.addEventListener('click', function(ev){
        ev.stopPropagation();
        /* 已揭示答案后再点选项 = 重新作答，自动收起答案 */
        if(item.classList.contains('revealed')){
          item.classList.remove('revealed','ok','bad');
          item.querySelectorAll('.opt').forEach(function(b){ b.classList.remove('right'); });
          var v0 = item.querySelector('.q-verdict'); if(v0) v0.textContent='';
        }
        if(qtype==='single'){
          item.querySelectorAll('.opt').forEach(function(b){ b.classList.remove('sel'); });
          btn.classList.add('sel');
        } else {
          btn.classList.toggle('sel');
        }
        item.classList.remove('ok','bad');
        var v = item.querySelector('.q-verdict'); if(v) v.textContent='';
        if(btnReset) btnReset.disabled = false;
      });
    });
    var chk = item.querySelector('.q-check');
    if(chk) chk.addEventListener('click', function(ev){
      ev.stopPropagation();
      var ans = keysOf(item);
      var sel = Array.prototype.slice.call(item.querySelectorAll('.opt.sel')).map(function(b){ return b.getAttribute('data-k'); });
      var ok = sel.length>0 && sel.length===ans.length && sel.filter(function(k){ return ans.indexOf(k)>=0; }).length===ans.length;
      reveal(item);
      if(btnReset) btnReset.disabled = false;
      item.classList.remove('ok','bad'); item.classList.add(ok?'ok':'bad');
      var v = item.querySelector('.q-verdict');
      if(v) v.textContent = ok ? '✓ 回答正确' : (sel.length ? '✗ 再想一想，正确项已标绿' : '请先选择答案');
    });
    if(btnReset) btnReset.addEventListener('click', function(ev){
      ev.stopPropagation();
      resetItem(item);
      tip('本题已重置，可重新作答');
    });
  });
  var btnReveal = document.getElementById('quizReveal');
  if(btnReveal) btnReveal.addEventListener('click', function(ev){
    ev.stopPropagation();
    var on = btnReveal.getAttribute('data-on')==='1';
    var next = !on;
    document.querySelectorAll('.quiz-item').forEach(function(item){
      if(next){
        reveal(item);
        var rs = item.querySelector('.q-reset'); if(rs) rs.disabled = false;
      } else {
        resetItem(item);
      }
    });
    btnReveal.setAttribute('data-on', next ? '1':'0');
    btnReveal.textContent = next ? '隐藏答案' : '显示全部答案';
  });
  var btnResetAll = document.getElementById('quizResetAll');
  if(btnResetAll) btnResetAll.addEventListener('click', function(ev){
    ev.stopPropagation();
    document.querySelectorAll('.quiz-item').forEach(resetItem);
    if(btnReveal){ btnReveal.setAttribute('data-on','0'); btnReveal.textContent = '显示全部答案'; }
    tip('已清空本题全部作答，可重新开始');
  });

  var h = parseInt((location.hash||'').replace('#',''),10);
  go(isNaN(h)?0:h-1, true);
})();
</script>
</body>
</html>
"""
