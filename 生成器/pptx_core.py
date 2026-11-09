# -*- coding: utf-8 -*-
"""PPTX 渲染引擎：与 HTML 版共用同一份内容源与配色体系"""
import os
import re
import html as _html
import subprocess
import tempfile

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

from deck_core import THEME, CHROME, FONT_PPT

SW, SH = 13.333, 7.5
ML, MR = 0.62, 0.62
CW = SW - ML - MR

C = {k: RGBColor.from_string(v.lstrip("#")) for k, v in THEME.items()}
INK, MUTED, LINE = C["ink"], C["muted"], C["line"]
BRAND, BRAND2, BRAND_DK = C["brand"], C["brand2"], C["brand_dk"]
VIOLET, ACCENT, OK = C["violet"], C["accent"], C["ok"]
SURFACE, CODE_BG, CODE_INK = C["surface"], C["code_bg"], C["code_ink"]
WHITE = RGBColor.from_string("FFFFFF")


# ------------------------------------------------------------------ 基础封装
def set_run(run, text, size, bold=False, color=INK, font=FONT_PPT, italic=False, spacing=None):
    run.text = text
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = font
    f.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = parse_xml(f'<{tag} {nsdecls("a")} typeface="{font}"/>')
            rPr.append(el)
        else:
            el.set("typeface", font)
    if spacing is not None:
        rPr.set("spc", str(int(spacing * 100)))
    return run


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


def para(tf, first=False, space_before=0, space_after=0, align=PP_ALIGN.LEFT, line=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    if line:
        p.line_spacing = line
    return p


def rrect(slide, x, y, w, h, fill=None, line=None, radius=0.07, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Pt(10)
    tf.margin_top = tf.margin_bottom = Pt(6)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return sp


def grad_bg(slide, c1, c2, angle=45):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(SW), Inches(SH))
    sp.line.fill.background()
    sp.shadow.inherit = False
    f = sp.fill
    f.gradient()
    f.gradient_stops[0].color.rgb = c1
    f.gradient_stops[0].position = 0.0
    f.gradient_stops[1].color.rgb = c2
    f.gradient_stops[1].position = 1.0
    try:
        f.gradient_angle = angle
    except Exception:
        pass
    return sp


# ------------------------------------------------------------------ 代码着色
CODE_COLORS = {
    "pn": RGBColor.from_string("7F93AD"), "tg": RGBColor.from_string("6FD6FF"),
    "at": RGBColor.from_string("FFCF7A"), "st": RGBColor.from_string("A5E88A"),
    "com": RGBColor.from_string("6B8099"), "sel": RGBColor.from_string("FFB3C8"),
    "cls": RGBColor.from_string("FFD479"), "id": RGBColor.from_string("9FE8FF"),
    "pc": RGBColor.from_string("C8A2FF"), "prop": RGBColor.from_string("8FD3FF"),
    "num": RGBColor.from_string("F7C774"), "fn": RGBColor.from_string("D0B0FF"),
    "imp": RGBColor.from_string("FF8A8A"),
}
_PAT = {
    "html": re.compile(
        r'(?P<com>&lt;!--[\s\S]*?--&gt;|<!--[\s\S]*?-->)'
        r'|(?P<st>"[^"]*"|\'[^\']*\')'
        r'|(?P<tg>&lt;/?[a-zA-Z][\w:-]*|</?[a-zA-Z][\w:-]*)'
        r'|(?P<at>[a-zA-Z-]+(?==))'
        r'|(?P<pn>&gt;|&lt;|/?>)', re.S),
    "css": re.compile(
        r'(?P<com>/\*[\s\S]*?\*/)'
        r'|(?P<st>"[^"]*"|\'[^\']*\')'
        r'|(?P<at>@[\w-]+)'
        r'|(?P<num>#[0-9a-fA-F]{3,8}\b|-?\d*\.?\d+(?:px|em|rem|%|s|ms|deg|vw|vh|vmin|vmax|fr|pt)?)'
        r'|(?P<prop>[-\w]+(?=\s*:))'
        r'|(?P<pc>::?[a-zA-Z][-\w()]*)'
        r'|(?P<sel>[.#][a-zA-Z][-\w]*)'
        r'|(?P<pn>[{};:,])', re.S),
}


def colorize(code, lang="html"):
    pat = _PAT.get(lang, _PAT["html"])
    segs, pos = [], 0
    for m in pat.finditer(code):
        if m.start() > pos:
            segs.append((code[pos:m.start()], None))
        col = CODE_COLORS.get(m.lastgroup)
        segs.append((m.group(0), col))
        pos = m.end()
    if pos < len(code):
        segs.append((code[pos:], None))
    lines = [[]]
    for text, col in segs:
        parts = text.split("\n")
        for i, pt in enumerate(parts):
            if pt:
                lines[-1].append((pt, col))
            if i < len(parts) - 1:
                lines.append([])
    return lines


# ------------------------------------------------------------------ 截图
def shot(html_str, out_png, w=1180, h=680):
    if not os.path.exists(CHROME):
        return False
    full = ("<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'><style>"
            "html,body{margin:0;height:100%}"
            "body{font-family:'PingFang SC','Microsoft YaHei',system-ui,sans-serif;color:#0E1B2E;"
            "display:grid;place-items:center;background:linear-gradient(140deg,#f4f8ff,#eaf1fb);"
            "padding:26px;box-sizing:border-box}"
            "</style></head><body>" + html_str + "</body></html>")
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "s.html")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(full)
        cmd = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
               "--hide-scrollbars", "--force-device-scale-factor=2", f"--window-size={w},{h}",
               f"--screenshot={out_png}", "file://" + f]
        try:
            subprocess.run(cmd, capture_output=True, timeout=60)
        except Exception:
            return False
    return os.path.exists(out_png)


# ------------------------------------------------------------------ 版式工具
def head_band(slide, unit, s, kind_label):
    kicker = s.get("kicker") or kind_label
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(ML), Inches(0.58), Inches(0.09), Inches(0.42))
    bar.fill.solid(); bar.fill.fore_color.rgb = BRAND; bar.line.fill.background(); bar.shadow.inherit = False
    tf = textbox(slide, ML + 0.22, 0.5, CW - 0.3, 0.32)
    p = para(tf, True)
    set_run(p.add_run(), kicker, 11, True, BRAND, spacing=0.6)
    tf2 = textbox(slide, ML, 0.88, CW, 0.72, anchor=MSO_ANCHOR.TOP)
    p2 = para(tf2, True)
    set_run(p2.add_run(), s.get("title", ""), 25, True, INK)
    y = 1.62
    if s.get("subtitle"):
        tf3 = textbox(slide, ML, 1.58, CW, 0.5)
        p3 = para(tf3, True)
        set_run(p3.add_run(), s["subtitle"], 12.5, False, MUTED)
        y = 1.98
    return y


def footer(slide, unit, idx, total):
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(ML), Inches(SH - 0.46), Inches(CW), Pt(0.75))
    ln.fill.solid(); ln.fill.fore_color.rgb = LINE; ln.line.fill.background(); ln.shadow.inherit = False
    tf = textbox(slide, ML, SH - 0.4, CW * 0.8, 0.3)
    p = para(tf, True)
    set_run(p.add_run(), f"{unit.get('project','')} · {unit.get('unit','')} · {unit['title']}", 9, False, MUTED)
    tf2 = textbox(slide, SW - MR - 1.4, SH - 0.4, 1.4, 0.3)
    p2 = para(tf2, True, align=PP_ALIGN.RIGHT)
    set_run(p2.add_run(), f"{idx} / {total}", 9, True, BRAND)


def strip_md(t):
    t = re.sub(r"<[^>]+>", "", str(t))
    return _html.unescape(t)


def est_lines(text, w_in, size_pt):
    """估算文本在给定宽度内占的行数（中文按全宽、英文按半宽）"""
    import math
    usable = max(1.0, w_in * 72.0 - 26.0)
    total = 0.0
    for ch in text:
        total += size_pt if ord(ch) > 0x2E80 else size_pt * 0.56
    return max(1, math.ceil(total / usable))


def fit_rows(items, width, size, pad, gap, available, line_f=1.42):
    """按可用高度自动缩小字号，返回 (字号, [每行高度])"""
    s = size
    hs = []
    for _ in range(8):
        hs = [max(0.4, est_lines(strip_md(t), width, s) * (s * line_f) / 72.0 + pad) for t in items]
        if sum(hs) + gap * max(0, len(items) - 1) <= available:
            break
        s -= 0.8
    return s, hs


# ------------------------------------------------------------------ 各版式
def s_cover(prs, unit, s):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    grad_bg(sl, RGBColor.from_string("0E1B2E"), RGBColor.from_string("1D3A78"), 45)
    o = sl.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.3), Inches(-1.1), Inches(5.4), Inches(5.4))
    o.fill.solid(); o.fill.fore_color.rgb = RGBColor.from_string("2F6BFF"); o.fill.transparency = 0.72
    o.line.fill.background(); o.shadow.inherit = False
    o2 = sl.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.6), Inches(4.4), Inches(3.0), Inches(3.0))
    o2.fill.solid(); o2.fill.fore_color.rgb = RGBColor.from_string("0FB5C9"); o2.fill.transparency = 0.66
    o2.line.fill.background(); o2.shadow.inherit = False
    tf = textbox(sl, ML, 0.72, 7, 0.4)
    p = para(tf, True)
    set_run(p.add_run(), f"{unit.get('project','')} · {unit.get('unit','')}", 12.5, True, RGBColor.from_string("8FD3FF"), spacing=1.2)
    tf2 = textbox(sl, ML, 1.9, 8.4, 1.9)
    p2 = para(tf2, True, line=1.08)
    set_run(p2.add_run(), unit["title"], 40, True, WHITE)
    tf3 = textbox(sl, ML, 3.86, 8.2, 0.9)
    p3 = para(tf3, True, line=1.3)
    set_run(p3.add_run(), unit.get("subtitle", ""), 15, False, RGBColor.from_string("BBD2F2"))
    x = ML
    for t in unit.get("cover_tags", []):
        w = 0.34 + len(t) * 0.145
        sp = rrect(sl, x, 5.0, w, 0.44, RGBColor.from_string("1B335E"), RGBColor.from_string("3C67B8"), 0.5)
        tfx = sp.text_frame; px = para(tfx, True, align=PP_ALIGN.CENTER)
        set_run(px.add_run(), t, 10.5, True, RGBColor.from_string("A9C8FF"))
        x += w + 0.16
    tf4 = textbox(sl, ML, 5.86, 9, 0.4)
    p4 = para(tf4, True)
    set_run(p4.add_run(), f"{unit.get('duration',40)} 分钟　·　教材《网页制作（HTML5+CSS3）》{unit.get('project','')}　·　{unit.get('ref_book','电子工业出版社')}",
            10.5, False, RGBColor.from_string("8FA6C6"))
    return sl


def s_section(prs, unit, s):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    grad_bg(sl, RGBColor.from_string("F5F8FF"), RGBColor.from_string("E9F1FF"), 45)
    tf = textbox(sl, ML, 2.1, CW, 1.4, anchor=MSO_ANCHOR.MIDDLE)
    p = para(tf, True, align=PP_ALIGN.CENTER)
    set_run(p.add_run(), s.get("no", ""), 66, True, RGBColor.from_string("C7D9FF"))
    tf2 = textbox(sl, ML, 3.3, CW, 0.9, anchor=MSO_ANCHOR.MIDDLE)
    p2 = para(tf2, True, align=PP_ALIGN.CENTER)
    set_run(p2.add_run(), s.get("title", ""), 34, True, INK)
    ln = slide_line = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(SW/2 - 0.7), Inches(4.3), Inches(1.4), Pt(4))
    ln.fill.solid(); ln.fill.fore_color.rgb = BRAND2; ln.line.fill.background(); ln.shadow.inherit = False
    if s.get("text"):
        tf3 = textbox(sl, ML, 4.6, CW, 0.7, anchor=MSO_ANCHOR.TOP)
        p3 = para(tf3, True, align=PP_ALIGN.CENTER)
        set_run(p3.add_run(), s["text"], 13, False, MUTED)
    return sl


def _rows(sl, items, y, size=13, gap=0.15, dot=True, fill=SURFACE, border=LINE):
    available = SH - 0.72 - y
    s, hs = fit_rows(items, CW - 0.55, size, 0.2, gap, available)
    for i, t in enumerate(items):
        box = rrect(sl, ML, y, CW, hs[i], fill, border, 0.14)
        tf = box.text_frame
        tf.margin_left = Pt(16); tf.margin_right = Pt(12)
        p = para(tf, True, line=1.2)
        r0 = p.add_run(); set_run(r0, "● ", s * 0.72, True, BRAND)
        r1 = p.add_run(); set_run(r1, strip_md(t), s, False, INK)
        y += hs[i] + gap
    return y


def s_bullets(prs, unit, s, kind="知识要点"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    _rows(sl, s["items"], y + 0.1, 13, 0.15)
    return sl


def s_cards(prs, unit, s, kind="要点分解"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    items = s["items"]; n = len(items)
    cols = 3 if n >= 3 else n
    rows = (n + cols - 1) // cols
    gap = 0.24
    cw = (CW - gap * (cols - 1)) / cols
    top = y + 0.12
    avail = SH - 0.75 - top
    rh = min(2.2, (avail - gap * (rows - 1)) / rows)
    for i, c in enumerate(items):
        r, cc = divmod(i, cols)
        x = ML + cc * (cw + gap); yy = top + r * (rh + gap)
        box = rrect(sl, x, yy, cw, rh, SURFACE, LINE, 0.1)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_top = Pt(12)
        acc = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(yy), Pt(4), Inches(rh))
        acc.fill.solid(); acc.fill.fore_color.rgb = BRAND; acc.line.fill.background(); acc.shadow.inherit = False
        p = para(tf, True, space_after=4)
        set_run(p.add_run(), strip_md(c["title"]), 14, True, BRAND_DK)
        p2 = para(tf, line=1.25)
        set_run(p2.add_run(), strip_md(c.get("text", "")), 11.5, False, MUTED)
    return sl


def s_table(prs, unit, s, kind="对照表"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    rows = len(s["rows"]) + 1
    cols = len(s["head"])
    top = y + 0.12
    h = min(SH - 0.8 - top, 0.42 + 0.44 * (rows - 1))
    gf = sl.shapes.add_table(rows, cols, Inches(ML), Inches(top), Inches(CW), Inches(h))
    tbl = gf.table
    tbl.first_row = True
    for j, htxt in enumerate(s["head"]):
        cell = tbl.cell(0, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor.from_string("E4EDFF")
        cell.margin_left = cell.margin_right = Pt(8); cell.margin_top = cell.margin_bottom = Pt(3)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame; tf.word_wrap = True
        p = para(tf, True)
        set_run(p.add_run(), strip_md(htxt), 12, True, BRAND_DK)
    for i, row in enumerate(s["rows"], start=1):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 else RGBColor.from_string("F7FAFF")
            cell.margin_left = cell.margin_right = Pt(8); cell.margin_top = cell.margin_bottom = Pt(3)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame; tf.word_wrap = True
            p = para(tf, True)
            set_run(p.add_run(), strip_md(val), 11.5, False, INK)
    return sl


def s_compare(prs, unit, s, kind="对比辨析"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    gap = 0.3
    cw = (CW - gap) / 2
    top = y + 0.12
    h = SH - 0.8 - top
    for k, (d, ac) in enumerate([(s["a"], BRAND), (s["b"], ACCENT)]):
        x = ML + k * (cw + gap)
        box = rrect(sl, x, top, cw, h, SURFACE, LINE, 0.06)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_top = Pt(14)
        p = para(tf, True, space_after=6)
        set_run(p.add_run(), strip_md(d["title"]), 15, True, ac)
        for it in d.get("items", []):
            pp = para(tf, space_after=5, line=1.25)
            r0 = pp.add_run(); set_run(r0, "▪ ", 11, True, ac)
            r1 = pp.add_run(); set_run(r1, strip_md(it), 11.5, False, MUTED)
    return sl


def s_steps(prs, unit, s, kind="操作步骤"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    items = s["items"]
    top = y + 0.1
    gap = 0.14
    texts = [strip_md(t["title"]) + ("　—　" + strip_md(t.get("text", "")) if t.get("text") else "") for t in items]
    size, hs = fit_rows(texts, CW - 1.05, 12.5, 0.24, gap, SH - 0.75 - top)
    hs = [max(0.62, h) for h in hs]
    for i, t in enumerate(items):
        yy = top + sum(hs[:i]) + gap * i
        h = hs[i]
        rrect(sl, ML, yy, CW, h, SURFACE, LINE, 0.1)
        c = sl.shapes.add_shape(MSO_SHAPE.OVAL, Inches(ML + 0.16), Inches(yy + h/2 - 0.17), Inches(0.34), Inches(0.34))
        c.fill.solid(); c.fill.fore_color.rgb = BRAND; c.line.fill.background(); c.shadow.inherit = False
        ctf = c.text_frame; ctf.margin_left = ctf.margin_right = ctf.margin_top = ctf.margin_bottom = 0
        cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
        set_run(cp.add_run(), str(i + 1), 11, True, WHITE)
        tf = textbox(sl, ML + 0.68, yy + 0.08, CW - 0.9, h - 0.16, anchor=MSO_ANCHOR.MIDDLE)
        p = para(tf, True)
        set_run(p.add_run(), strip_md(t["title"]), size + 0.5, True, INK)
        if t.get("text"):
            p2 = para(tf, space_before=2, line=1.18)
            set_run(p2.add_run(), strip_md(t["text"]), size - 1.5, False, MUTED)
    return sl


def s_flow(prs, unit, s, kind="原理图解"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    items = s["items"]
    n = len(items)
    gap = 0.42
    cw = (CW - gap * (n - 1)) / n
    top = y + 0.5
    h = 2.4
    for i, t in enumerate(items):
        x = ML + i * (cw + gap)
        rrect(sl, x, top, cw, h, SURFACE, LINE, 0.1)
        tf = textbox(sl, x + 0.12, top + 0.3, cw - 0.24, h - 0.5, anchor=MSO_ANCHOR.MIDDLE)
        p = para(tf, True)
        set_run(p.add_run(), strip_md(t.get("title", "")), 13, True, BRAND_DK)
        p.alignment = PP_ALIGN.CENTER
        p2 = para(tf, space_before=6, line=1.2)
        set_run(p2.add_run(), strip_md(t.get("text", "")), 10.5, False, MUTED)
        p2.alignment = PP_ALIGN.CENTER
        if i < n - 1:
            ax = x + cw + 0.06
            ar = sl.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(ax), Inches(top + h/2 - 0.11), Inches(gap - 0.12), Inches(0.22))
            ar.fill.solid(); ar.fill.fore_color.rgb = BRAND2; ar.line.fill.background(); ar.shadow.inherit = False
    if s.get("note"):
        box = rrect(sl, ML, top + h + 0.3, CW, 0.7, RGBColor.from_string("EEF4FF"), None, 0.2)
        tf = box.text_frame
        p = para(tf, True)
        set_run(p.add_run(), strip_md(s["note"]), 11.5, False, RGBColor.from_string("33517F"))
    return sl


def _code_panel(sl, x, y, w, h, code, lang, file=""):
    rrect(sl, x, y, w, h, CODE_BG, None, 0.05)
    bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.34))
    bar.fill.solid(); bar.fill.fore_color.rgb = RGBColor.from_string("16263C")
    bar.line.fill.background(); bar.shadow.inherit = False
    tf = textbox(sl, x + 0.16, y + 0.02, w - 0.3, 0.3, anchor=MSO_ANCHOR.MIDDLE)
    p = para(tf, True)
    set_run(p.add_run(), lang.upper(), 9.5, True, RGBColor.from_string("7FD7E4"), font="Consolas", spacing=0.8)
    if file:
        r = p.add_run(); set_run(r, "   " + file, 9.5, False, RGBColor.from_string("7F93AD"), font="Consolas")
    body = textbox(sl, x + 0.18, y + 0.44, w - 0.36, h - 0.58)
    lines = colorize(code, lang)
    maxlines = max(1, int((h - 0.58) / 0.235))
    for ln in lines[:maxlines]:
        p = para(body, ln is lines[0], line=1.1, space_after=0)
        if not ln:
            p.add_run()
        for text, col in ln:
            set_run(p.add_run(), text, 10.5, False, col or CODE_INK, font="Consolas")
    return lines


def s_code(prs, unit, s, kind="代码示例"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    top = y + 0.1
    cap = 0.62 if s.get("caption") else 0.0
    h = SH - 0.75 - top - cap
    _code_panel(sl, ML, top, CW, h, s["code"], s.get("lang", "html"), s.get("file", ""))
    if s.get("caption"):
        tf = textbox(sl, ML, top + h + 0.1, CW, 0.5)
        p = para(tf, True, line=1.2)
        set_run(p.add_run(), strip_md(s["caption"]), 11, False, MUTED)
    return sl


def s_codebullets(prs, unit, s, kind="代码与要点"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    top = y + 0.1
    h = SH - 0.75 - top
    lw = CW * 0.4
    rw = CW * 0.58
    items = s["items"]
    empty = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(ML), Inches(top), Inches(1), Inches(1))
    empty.line.fill.background(); empty.fill.background(); empty.shadow.inherit = False
    tf = textbox(sl, ML, top, lw, h, anchor=MSO_ANCHOR.TOP)
    for i, t in enumerate(items):
        p = para(tf, i == 0, space_after=8, line=1.28)
        r0 = p.add_run(); set_run(r0, "● ", 10, True, BRAND)
        r1 = p.add_run(); set_run(r1, strip_md(t), 12, False, INK)
    _code_panel(sl, ML + lw + 0.26, top, rw - 0.26, h, s["code"], s.get("lang", "html"), s.get("file", ""))
    return sl


def s_task(prs, unit, s, kind="任务驱动"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    top = y + 0.1
    h = SH - 0.75 - top
    lw = CW * 0.42
    rw = CW * 0.55
    box = rrect(sl, ML, top, lw, 1.1, RGBColor.from_string("EEF4FF"), RGBColor.from_string("D6E3FB"), 0.18)
    tf = box.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = para(tf, True, line=1.2)
    set_run(p.add_run(), "任务目标　", 11, True, BRAND)
    set_run(p.add_run(), strip_md(s.get("goal", "")), 12, False, INK)
    tf2 = textbox(sl, ML, top + 1.26, lw, h - 1.3, anchor=MSO_ANCHOR.TOP)
    for i, t in enumerate(s.get("steps", [])):
        p = para(tf2, i == 0, space_after=7, line=1.26)
        r0 = p.add_run(); set_run(r0, f"{i+1}. ", 11.5, True, BRAND2)
        r1 = p.add_run(); set_run(r1, strip_md(t), 11.5, False, INK)
    if s.get("code"):
        _code_panel(sl, ML + lw + 0.26, top, rw - 0.26, h, s["code"], s.get("lang", "html"))
    return sl


def s_demo(prs, unit, s, kind="效果演示", tmpdir=None):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    top = y + 0.1
    h = SH - 0.75 - top
    lw = CW * 0.4
    rw = CW * 0.58
    tf = textbox(sl, ML, top, lw, h * 0.72, anchor=MSO_ANCHOR.TOP)
    for i, t in enumerate(s.get("items", [])):
        p = para(tf, i == 0, space_after=9, line=1.3)
        r0 = p.add_run(); set_run(r0, "● ", 10, True, BRAND)
        r1 = p.add_run(); set_run(r1, strip_md(t), 12, False, INK)
    if s.get("hint"):
        box = rrect(sl, ML, top + h * 0.74, lw, h * 0.26, RGBColor.from_string("FFF3E7"), None, 0.14)
        tfb = box.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = para(tfb, True, line=1.25)
        set_run(p.add_run(), "动手试试：", 11, True, RGBColor.from_string("C2601A"))
        set_run(p.add_run(), strip_md(s["hint"]), 10.5, False, RGBColor.from_string("7A4A22"))
    # 预览：优先真实截图
    done = False
    if tmpdir and s.get("html"):
        png = os.path.join(tmpdir, f"demo_{unit['id']}_{abs(hash(s.get('title','')))%99999}.png")
        if shot(s["html"], png, 1180, 660):
            frame = rrect(sl, ML + lw + 0.26, top, rw - 0.26, h, WHITE, LINE, 0.04)
            sl.shapes.add_picture(png, Inches(ML + lw + 0.34), Inches(top + 0.08), width=Inches(rw - 0.42))
            done = True
    if not done and s.get("code"):
        _code_panel(sl, ML + lw + 0.26, top, rw - 0.26, h, s["code"], s.get("lang", "html"))
    return sl


def s_ai(prs, unit, s, kind="AI 前沿"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    top = y + 0.1
    h = SH - 0.75 - top
    lw = CW * 0.52
    rw = CW * 0.45
    box = rrect(sl, ML, top, lw, h, RGBColor.from_string("1C1B45"), None, 0.08)
    o = sl.shapes.add_shape(MSO_SHAPE.OVAL, Inches(ML + lw - 1.6), Inches(top - 0.5), Inches(2.1), Inches(2.1))
    o.fill.solid(); o.fill.fore_color.rgb = VIOLET; o.fill.transparency = 0.55; o.line.fill.background(); o.shadow.inherit = False
    tf = box.text_frame; tf.vertical_anchor = MSO_ANCHOR.TOP; tf.margin_top = Pt(18); tf.margin_left = Pt(18)
    p = para(tf, True, space_after=8)
    set_run(p.add_run(), "AI", 20, True, RGBColor.from_string("B9A6FF"))
    p2 = para(tf, line=1.35)
    set_run(p2.add_run(), strip_md(s.get("text", "")), 13, False, RGBColor.from_string("E8E6FF"))
    tf2 = textbox(sl, ML + lw + 0.28, top, rw - 0.28, h, anchor=MSO_ANCHOR.TOP)
    for i, t in enumerate(s.get("items", [])):
        p = para(tf2, i == 0, space_after=9, line=1.28)
        r0 = p.add_run(); set_run(r0, "✦ ", 11, True, VIOLET)
        r1 = p.add_run(); set_run(r1, strip_md(t), 11.5, False, INK)
    return sl


def s_quiz(prs, unit, s, kind="随堂检测"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    items = s["items"]
    top = y + 0.1
    gap = 0.15
    texts = []
    for q in items:
        ans_raw = re.sub(r"[^A-Za-z]", "", str(q.get("answer", ""))).upper()
        qtype = (q.get("type") or ("multi" if len(ans_raw) > 1 else "single")).lower()
        t = ("［多选］" if qtype == "multi" else "［单选］") + strip_md(q["q"])
        if q.get("options"):
            t += " " + "　".join(strip_md(o) for o in q["options"])
        if ans_raw:
            t += "　答案：" + "、".join(ans_raw)
        texts.append(t)
    size, hs = fit_rows(texts, CW - 0.5, 12, 0.3, gap, SH - 0.75 - top)
    hs = [max(1.05, h) for h in hs]
    total_h = sum(hs) + gap * max(0, len(hs) - 1)
    if total_h > SH - 0.75 - top:
        k = (SH - 0.75 - top) / total_h
        hs = [h * k for h in hs]
    notes = []
    for i, q in enumerate(items):
        yy = top + sum(hs[:i]) + gap * i
        h = hs[i]
        ans_raw = re.sub(r"[^A-Za-z]", "", str(q.get("answer", ""))).upper()
        qtype = (q.get("type") or ("multi" if len(ans_raw) > 1 else "single")).lower()
        rrect(sl, ML, yy, CW, h, SURFACE, LINE, 0.08)
        tf = textbox(sl, ML + 0.18, yy + 0.09, CW - 0.36, h - 0.18, anchor=MSO_ANCHOR.MIDDLE)
        p = para(tf, True, line=1.2)
        tg = p.add_run()
        set_run(tg, "多选  " if qtype == "multi" else "单选  ", max(8.5, size - 1.5), True,
                RGBColor.from_string("7C5CFF") if qtype == "multi" else RGBColor.from_string("0FB5C9"))
        set_run(p.add_run(), strip_md(q["q"]), size, True, INK)
        if q.get("options"):
            p2 = para(tf, space_before=3, line=1.18)
            set_run(p2.add_run(), "　".join(strip_md(o) for o in q["options"]), size - 1, False, RGBColor.from_string("33456B"))
        if ans_raw:
            p3 = para(tf, space_before=3, line=1.18)
            set_run(p3.add_run(), "答案 " + "、".join(ans_raw), size - 1, True, RGBColor.from_string("0F7A3D"))
            if q.get("tip"):
                set_run(p3.add_run(), "　" + strip_md(q["tip"]), max(8.5, size - 1.6), False, MUTED)
        notes.append(f"第 {i+1} 题（{'多选' if qtype=='multi' else '单选'}）　答案：{'、'.join(ans_raw)}"
                     + (f"\n　解析：{strip_md(q.get('tip',''))}" if q.get("tip") else ""))
    try:
        sl.notes_slide.notes_text_frame.text = "\n\n".join(notes)
    except Exception:
        pass
    return sl


def s_objectives(prs, unit, s, kind="学习目标"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    o = s.get("objectives", {})
    blocks = [("知识目标", o.get("knowledge", []), BRAND_DK, BRAND),
              ("技能目标", o.get("skill", []), RGBColor.from_string("0A7B87"), BRAND2),
              ("素养目标", o.get("literacy", []), RGBColor.from_string("B8730F"), ACCENT)]
    gap = 0.26
    cw = (CW - gap * 2) / 3
    top = y + 0.12
    h = SH - 0.8 - top
    for i, (t, arr, tc, ac) in enumerate(blocks):
        x = ML + i * (cw + gap)
        rrect(sl, x, top, cw, h, SURFACE, LINE, 0.07)
        acc = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(top), Inches(cw), Pt(5))
        acc.fill.solid(); acc.fill.fore_color.rgb = ac; acc.line.fill.background(); acc.shadow.inherit = False
        tf = textbox(sl, x + 0.2, top + 0.24, cw - 0.4, h - 0.4, anchor=MSO_ANCHOR.TOP)
        p = para(tf, True, space_after=8)
        set_run(p.add_run(), t, 14, True, tc)
        for it in arr:
            pp = para(tf, space_after=6, line=1.25)
            r0 = pp.add_run(); set_run(r0, "• ", 11, True, ac)
            r1 = pp.add_run(); set_run(r1, strip_md(it), 11, False, MUTED)
    return sl


def s_ideology(prs, unit, s, kind="思政课堂"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    top = y + 0.2
    h = 3.4
    rrect(sl, ML, top, CW, h, RGBColor.from_string("FFF9F2"), RGBColor.from_string("FFE3C8"), 0.06)
    acc = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(ML), Inches(top), Pt(6), Inches(h))
    acc.fill.solid(); acc.fill.fore_color.rgb = ACCENT; acc.line.fill.background(); acc.shadow.inherit = False
    tf = textbox(sl, ML + 0.3, top + 0.3, CW - 0.6, h - 0.6, anchor=MSO_ANCHOR.MIDDLE)
    p = para(tf, True, line=1.5)
    set_run(p.add_run(), strip_md(s.get("text", "")), 14, False, RGBColor.from_string("4A3A28"))
    if s.get("topic"):
        box = rrect(sl, ML, top + h + 0.28, CW, 0.86, RGBColor.from_string("EEF4FF"), None, 0.12)
        tfb = box.text_frame; tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = para(tfb, True, line=1.25)
        set_run(p.add_run(), "课堂讨论　", 11, True, BRAND)
        set_run(p.add_run(), strip_md(s["topic"]), 11.5, False, RGBColor.from_string("33517F"))
    return sl


def s_refs(prs, unit, s, kind="出处与参考"):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    y = head_band(sl, unit, s, kind)
    top = y + 0.1
    items = s["items"]
    h = min(0.62, (SH - 0.75 - top - 0.1 * len(items)) / len(items))
    for i, r in enumerate(items):
        t = r["t"] if isinstance(r, dict) else r
        u = r.get("u", "") if isinstance(r, dict) else ""
        yy = top + i * (h + 0.1)
        rrect(sl, ML, yy, CW, h, SURFACE, LINE, 0.14)
        tf = textbox(sl, ML + 0.2, yy + 0.06, CW - 0.4, h - 0.12, anchor=MSO_ANCHOR.MIDDLE)
        p = para(tf, True)
        set_run(p.add_run(), f"{i+1:02d}  ", 11, True, BRAND)
        set_run(p.add_run(), strip_md(t), 11.5, True, INK)
        if u:
            set_run(p.add_run(), "   " + u, 9.5, False, MUTED, font="Consolas")
    return sl


def s_end(prs, unit, s):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    grad_bg(sl, RGBColor.from_string("12203B"), RGBColor.from_string("0E6F88"), 45)
    tf = textbox(sl, ML, 3.0, CW, 1.0, anchor=MSO_ANCHOR.MIDDLE)
    p = para(tf, True, align=PP_ALIGN.CENTER)
    set_run(p.add_run(), s.get("title", "本单元结束"), 34, True, WHITE)
    tf2 = textbox(sl, ML, 4.2, CW, 0.6, anchor=MSO_ANCHOR.MIDDLE)
    p2 = para(tf2, True, align=PP_ALIGN.CENTER)
    set_run(p2.add_run(), s.get("text", "下次课见 · 记得完成课后作业"), 14, False, RGBColor.from_string("A9C4E8"))
    return sl


PPT_RENDER = {
    "cover": s_cover, "section": s_section, "outline": lambda p, u, s, kind="导览": s_bullets(p, u, s, kind),
    "bullets": s_bullets, "cards": s_cards, "table": s_table, "compare": s_compare, "steps": s_steps,
    "flow": s_flow, "code": s_code, "codebullets": s_codebullets, "task": s_task, "demo": s_demo,
    "ai": s_ai, "quiz": s_quiz, "objectives": s_objectives, "ideology": s_ideology, "refs": s_refs,
    "end": s_end, "summary": lambda p, u, s, kind="本课小结": s_bullets(p, u, s, kind),
    "homework": lambda p, u, s, kind="课后作业": s_bullets(p, u, s, kind),
    "notice": lambda p, u, s, kind="温馨提示": s_bullets(p, u, s, kind),
}


def render_pptx(unit, path):
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    total = len(unit["slides"]) + 1
    tmpdir = tempfile.mkdtemp(prefix="ppt_shot_")
    seq = [{"type": "cover"}] + unit["slides"]
    for i, s in enumerate(seq):
        fn = PPT_RENDER.get(s["type"])
        if not fn:
            fn = s_bullets
        if s["type"] in ("cover", "section", "end"):
            fn(prs, unit, s)
        elif s["type"] in ("demo",):
            fn(prs, unit, s, tmpdir=tmpdir)
        else:
            fn(prs, unit, s)
        if s["type"] not in ("cover", "section", "end"):
            footer(prs.slides[-1], unit, i + 1, total)
    prs.save(path)
    try:
        import shutil; shutil.rmtree(tmpdir, ignore_errors=True)
    except Exception:
        pass
    return path
