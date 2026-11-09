# -*- coding: utf-8 -*-
"""
课件生成入口
用法:
  python build.py            # 生成 content/ 下全部单元 + 总目录页
  python build.py U01 U02    # 只生成指定单元的课件（总目录页始终全量重建）
"""
import os
import re
import sys
import json
import glob
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "content")
OUT = os.path.join(ROOT, "课件")

sys.path.insert(0, HERE)
from deck_core import render_html          # noqa: E402
from pptx_core import render_pptx          # noqa: E402
from index_core import render_index        # noqa: E402


def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "-", name)


def collect(all_files):
    """扫描全部内容文件，按单元号排序，返回元信息列表（供总目录与「下一讲」使用）"""
    units = []
    for f in all_files:
        with open(f, encoding="utf-8") as fp:
            u = json.load(fp)
        slides = u.get("slides", [])
        units.append({
            "id": u["id"],
            "unit": u.get("unit", ""),
            "project": u.get("project", ""),
            "project_name": u.get("project_name", ""),
            "title": u["title"],
            "folder": safe(f"{u.get('project','')}-{u.get('project_name','')}"),
            "base": safe(f"{u['id']} {u['title']}"),
            "pages": len(slides) + 1,
            "quiz": sum(len(s.get("items", [])) for s in slides if s.get("type") == "quiz"),
            "demo": sum(1 for s in slides if s.get("type") == "demo"),
        })
    units.sort(key=lambda x: x["id"])
    return units


def nav_for(i, units):
    """当前单元的导航信息：下一讲 + 总目录"""
    cur = units[i]
    nav = {"index": "../index.html"}
    if i + 1 < len(units):
        n = units[i + 1]
        rel = os.path.relpath(os.path.join(n["folder"], n["base"] + ".html"), cur["folder"])
        nav["next"] = {
            "href": quote(rel.replace(os.sep, "/"), safe="/"),
            "label": f'{n["id"]} {n["title"]}',
        }
    return nav


def build_one(path, units, idx_of):
    with open(path, encoding="utf-8") as f:
        unit = json.load(f)
    folder = safe(f"{unit['project']}-{unit.get('project_name','')}")
    outdir = os.path.join(OUT, folder)
    os.makedirs(outdir, exist_ok=True)
    base = safe(f"{unit['id']} {unit['title']}")
    html_path = os.path.join(outdir, base + ".html")
    pptx_path = os.path.join(outdir, base + ".pptx")

    i = idx_of.get(unit["id"])
    nav = nav_for(i, units) if i is not None else None

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html(unit, nav=nav))
    render_pptx(unit, pptx_path)
    print(f"  ✓ {unit['id']} {unit['title']}  →  {folder}/")
    nxt = (nav or {}).get("next")
    print(f"      下一讲: {nxt['label']}" if nxt else "      下一讲: （课程结束）")
    return html_path, pptx_path


def build_index(units):
    items = [{
        "id": u["id"],
        "project": u["project"],
        "project_name": u["project_name"],
        "title": u["title"],
        "pages": u["pages"],
        "quiz": u["quiz"],
        "demo": u["demo"],
        "href": quote(f'{u["folder"]}/{u["base"]}.html', safe="/"),
    } for u in units]
    path = os.path.join(OUT, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_index(items))
    print(f"\n  ✓ 总目录页  →  index.html（{len(items)} 个单元）")
    return path


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    all_files = sorted(glob.glob(os.path.join(CONTENT, "*.json")))
    if not all_files:
        print("没有找到内容文件")
        return
    units = collect(all_files)
    idx_of = {u["id"]: i for i, u in enumerate(units)}

    files = all_files
    if args:
        files = [f for f in all_files if any(a in os.path.basename(f) for a in args)]
        if not files:
            print("没有匹配的内容文件")
            return

    print(f"共 {len(files)} 个教学单元，开始生成…")
    for f in files:
        build_one(f, units, idx_of)
    build_index(units)
    print(f"\n完成，输出目录：{OUT}")


if __name__ == "__main__":
    main()
