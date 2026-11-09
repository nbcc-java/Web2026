# -*- coding: utf-8 -*-
"""
课件总目录页生成（输出 课件/index.html）

输入 units: [{
    id, unit, project, project_name, title,
    pages, quiz, demo, href
}]
href 为相对「课件/」目录的、已 URL 编码的路径。
"""
import html

PALETTE = ["#2F6BFF", "#0FB5C9", "#7C5CFF", "#FF8A3D", "#12A150",
           "#D9534F", "#3B82F6", "#8B5CF6", "#0E9F6E", "#F59E0B"]


def esc(t):
    return html.escape(str(t), quote=True)


def _cards(units, color):
    out = []
    for i, u in enumerate(units):
        metas = [f'<span class="m">{u["pages"]} 页</span>',
                 f'<span class="m">{u["quiz"]} 题</span>']
        if u.get("demo"):
            metas.append('<span class="m m-demo">含实时演示</span>')
        meta = "".join(metas)
        key = f'{u["id"]} {u["project"]} {u["project_name"]} {u["title"]}'.lower()
        out.append(f"""      <a class="card" href="{esc(u['href'])}" target="_blank" rel="noopener"
         data-k="{esc(key)}" data-label="{esc(u['id'] + ' ' + u['title'])}" style="--pc:{color}">
        <div class="card-top"><span class="uid">{esc(u['id'])}</span>
          <span class="go">打开 <i>→</i></span></div>
        <h3>{esc(u['title'])}</h3>
        <div class="meta">{meta}</div>
      </a>""")
    return "\n".join(out)


def render_index(units, course="网页制作（HTML5+CSS3）"):
    groups = {}
    order = []
    for u in units:
        p = u["project"]
        if p not in groups:
            groups[p] = []
            order.append(p)
        groups[p].append(u)

    total_pages = sum(u["pages"] for u in units)
    total_quiz = sum(u["quiz"] for u in units)
    total_demo = sum(u.get("demo", 0) for u in units)

    sections, chips = [], []
    for gi, p in enumerate(order):
        color = PALETTE[gi % len(PALETTE)]
        pname = groups[p][0]["project_name"]
        pno = p.replace("项目", "").strip()
        pno = f"{int(pno):02d}" if pno.isdigit() else pno
        sections.append(f"""  <section class="proj" data-p="{esc(p)}" style="--pc:{color}">
    <div class="proj-h">
      <span class="pno">{esc(pno)}</span>
      <h2>{esc(pname)}</h2>
      <span class="pline"></span>
      <span class="pcnt">{len(groups[p])} 个单元</span>
    </div>
    <div class="cards">
{_cards(groups[p], color)}
    </div>
  </section>""")
        chips.append(f'<button type="button" class="chip" data-p="{esc(p)}">'
                     f'<i style="background:{color}"></i>{esc(p)} · {esc(pname)}</button>')

    html_out = TEMPLATE
    html_out = html_out.replace("__COURSE__", esc(course))
    html_out = html_out.replace("__UNITS__", str(len(units)))
    html_out = html_out.replace("__PAGES__", str(total_pages))
    html_out = html_out.replace("__DEMO__", str(total_demo))
    html_out = html_out.replace("__QUIZ__", str(total_quiz))
    html_out = html_out.replace("__CHIPS__", "\n      ".join(chips))
    html_out = html_out.replace("__SECTIONS__", "\n".join(sections))
    return html_out


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>课堂导航 · 网页制作（HTML5+CSS3）</title>
<style>
:root{
  --brand:#2F6BFF;--brand2:#0FB5C9;--violet:#7C5CFF;--accent:#FF8A3D;
  --ink:#0E1B2E;--muted:#5A6B85;--line:#DCE6F5;--bg:#EEF3FB;--surface:#fff;
  --mono:"JetBrains Mono","SFMono-Regular",Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:"PingFang SC","Microsoft YaHei","Helvetica Neue",Arial,sans-serif;
  color:var(--ink);background:
    radial-gradient(1200px 600px at 12% -8%,#dbe8ff 0%,transparent 60%),
    radial-gradient(900px 500px at 88% 4%,#d8f3f8 0%,transparent 55%),
    var(--bg);
  -webkit-font-smoothing:antialiased;line-height:1.6;min-height:100vh}

/* ---------- Hero ---------- */
.hero{position:relative;overflow:hidden;color:#fff;
  background:linear-gradient(140deg,#12203b,#1d3a78 55%,#0e6f88);
  padding:56px 24px 40px}
.hero::before,.hero::after{content:"";position:absolute;border-radius:50%;filter:blur(60px);opacity:.55}
.hero::before{width:420px;height:420px;left:-90px;top:-160px;
  background:radial-gradient(circle,#2f6bff,transparent 70%)}
.hero::after{width:480px;height:480px;right:-120px;top:-180px;
  background:radial-gradient(circle,#0fb5c9,transparent 70%)}
.hero-in{position:relative;z-index:2;max-width:1240px;margin:0 auto}
.brand{display:inline-flex;align-items:center;gap:10px;font-size:13px;letter-spacing:.16em;
  font-weight:700;color:#a8e7f1;text-transform:uppercase;margin-bottom:16px}
.brand b{color:#fff;letter-spacing:.06em;font-size:14px}
.brand .dot{width:6px;height:6px;border-radius:50%;background:#7fd7e4;box-shadow:0 0 12px #7fd7e4}
.hero h1{font-size:clamp(26px,3.6vw,42px);font-weight:900;letter-spacing:.01em;line-height:1.2}
.hero h1 em{font-style:normal;background:linear-gradient(100deg,#7fd7e4,#9db4ff 60%,#fff);
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.hero .sub{margin-top:12px;font-size:clamp(13px,1.15vw,15px);color:#b9cdea;max-width:760px}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.stat{background:rgba(255,255,255,.09);border:1px solid rgba(160,200,235,.24);
  border-radius:12px;padding:10px 16px;backdrop-filter:blur(8px);min-width:104px}
.stat b{display:block;font-size:22px;font-weight:900;color:#fff;font-family:var(--mono);letter-spacing:-.02em}
.stat span{font-size:11.5px;color:#a6c1e2;letter-spacing:.06em}

/* ---------- Toolbar ---------- */
.tools{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-top:26px}
.search{position:relative;flex:1 1 320px;max-width:460px}
.search input{width:100%;font-family:inherit;font-size:14px;color:var(--ink);
  background:rgba(255,255,255,.96);border:1px solid transparent;border-radius:11px;
  padding:12px 14px 12px 40px;outline:none;transition:.2s}
.search input::placeholder{color:#8fa3bf}
.search input:focus{border-color:#7fd7e4;box-shadow:0 0 0 4px rgba(127,215,228,.22)}
.search svg{position:absolute;left:13px;top:50%;transform:translateY(-50%);opacity:.55}
.kbd{position:absolute;right:10px;top:50%;transform:translateY(-50%);
  font-family:var(--mono);font-size:11px;color:#7b8ca6;background:#eef2f8;
  border:1px solid #dbe3ef;border-radius:5px;padding:2px 6px;pointer-events:none}
.resume{display:inline-flex;align-items:center;gap:8px;max-width:100%;
  background:linear-gradient(135deg,rgba(127,215,228,.2),rgba(157,180,255,.16));
  border:1px solid rgba(160,200,235,.42);border-radius:11px;padding:10px 14px;
  color:#eaf4ff;text-decoration:none;font-size:13px;transition:.2s}
.resume:hover{background:rgba(255,255,255,.14);border-color:#7fd7e4}
.resume .rl{font-size:11px;color:#9fc4e6;letter-spacing:.08em}
.resume b{font-weight:700;color:#fff}
.resume .ra{color:#7fd7e4;font-weight:800}
.resume[hidden]{display:none}

/* ---------- Chips ---------- */
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.chip{display:inline-flex;align-items:center;gap:7px;cursor:pointer;font-family:inherit;
  font-size:12.5px;color:#cfe0f5;background:rgba(255,255,255,.07);
  border:1px solid rgba(160,200,235,.22);border-radius:999px;padding:7px 13px;transition:.18s}
.chip i{width:7px;height:7px;border-radius:50%;background:#7fd7e4;box-shadow:0 0 8px rgba(255,255,255,.35)}
.chip:hover{background:rgba(255,255,255,.15);color:#fff;border-color:rgba(160,200,235,.5)}
.chip.on{background:#fff;color:#12305e;border-color:#fff;font-weight:700}
.chip.on i{box-shadow:none}

/* ---------- List ---------- */
main{max-width:1240px;margin:0 auto;padding:34px 24px 60px}
.proj{margin-bottom:34px;animation:up .5s both}
.proj[hidden]{display:none}
.proj-h{display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-wrap:wrap}
.pno{font-family:var(--mono);font-size:13px;font-weight:800;color:#fff;background:var(--pc);
  border-radius:8px;padding:4px 9px;letter-spacing:.04em;box-shadow:0 8px 18px -10px var(--pc)}
.proj-h h2{font-size:19px;font-weight:800;letter-spacing:.01em}
.pline{flex:1;height:1px;min-width:24px;
  background:linear-gradient(90deg,color-mix(in srgb,var(--pc) 45%,transparent),transparent)}
.pcnt{font-size:12px;color:var(--muted);font-family:var(--mono);background:#fff;
  border:1px solid var(--line);border-radius:999px;padding:3px 10px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(296px,1fr));gap:14px}
.card{position:relative;display:flex;flex-direction:column;gap:9px;overflow:hidden;
  background:var(--surface);border:1px solid var(--line);border-radius:15px;
  padding:16px 18px 15px 22px;text-decoration:none;color:inherit;
  box-shadow:0 12px 30px -26px rgba(20,40,90,.6);transition:transform .2s,box-shadow .2s,border-color .2s}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--pc);
  opacity:.9;transition:width .2s}
.card:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--pc) 55%,#fff);
  box-shadow:0 22px 44px -28px color-mix(in srgb,var(--pc) 70%,transparent)}
.card:hover::before{width:6px}
.card:focus-visible{outline:3px solid color-mix(in srgb,var(--pc) 45%,#fff);outline-offset:2px}
.card[hidden]{display:none}
.card-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
.uid{font-family:var(--mono);font-size:12px;font-weight:800;letter-spacing:.08em;
  color:var(--pc);background:color-mix(in srgb,var(--pc) 11%,#fff);
  border:1px solid color-mix(in srgb,var(--pc) 26%,#fff);border-radius:7px;padding:2px 8px}
.go{font-size:12px;color:var(--muted);display:inline-flex;align-items:center;gap:4px;
  opacity:0;transform:translateX(-4px);transition:.2s}
.go i{font-style:normal;color:var(--pc);font-weight:800}
.card:hover .go{opacity:1;transform:none}
.card h3{font-size:15.5px;font-weight:700;line-height:1.5;letter-spacing:.01em;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.9em}
.meta{display:flex;flex-wrap:wrap;gap:7px;margin-top:2px}
.m{font-size:11.5px;color:var(--muted);background:#f4f7fc;border:1px solid #e6edf8;
  border-radius:6px;padding:2px 8px;font-family:var(--mono)}
.m-demo{color:#0a7b87;background:rgba(15,181,201,.09);border-color:rgba(15,181,201,.24)}
.card.is-last{border-color:var(--pc);box-shadow:0 18px 38px -26px color-mix(in srgb,var(--pc) 75%,transparent)}
.card.is-last .go{opacity:1;transform:none}

.empty{display:none;text-align:center;padding:60px 20px;color:var(--muted)}
.empty b{display:block;font-size:17px;color:var(--ink);margin-bottom:6px}
.empty.on{display:block}

footer{max-width:1240px;margin:0 auto;padding:0 24px 44px;color:#8aa0bd;font-size:12.5px;
  display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center}
footer code{font-family:var(--mono);background:#fff;border:1px solid var(--line);
  border-radius:5px;padding:1px 6px;color:#5A6B85}

@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

@media (max-width:640px){
  .hero{padding:40px 18px 30px}
  main{padding:24px 18px 44px}
  .cards{grid-template-columns:1fr}
  .stat{flex:1;min-width:calc(50% - 5px)}
  .kbd{display:none}
  .search{max-width:none;flex:1 1 100%}
  .proj-h h2{font-size:17px}
}
</style>
</head>
<body>

<header class="hero">
  <div class="hero-in">
    <div class="brand"><span class="dot"></span>__COURSE__<b>课堂导航</b></div>
    <h1>课堂导航 · <em>总目录</em></h1>
    <p class="sub">2026 学年 · 教材《网页制作（HTML5+CSS3）》（郑哲、傅冬 主编，电子工业出版社）· 每个教学单元 40 分钟 · 点击任一张卡片即可开始上课</p>
    <div class="stats">
      <div class="stat"><b>__UNITS__</b><span>教学单元</span></div>
      <div class="stat"><b>__PAGES__</b><span>课件页数</span></div>
      <div class="stat"><b>__DEMO__</b><span>实时演示</span></div>
      <div class="stat"><b>__QUIZ__</b><span>随堂检测题</span></div>
      <div class="stat"><b>__UNITS__</b><span>PPTX 版本</span></div>
    </div>
    <div class="tools">
      <div class="search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5A6B85" stroke-width="2.2">
          <circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>
        <input id="q" type="search" placeholder="搜索单元号、标题或关键词…" autocomplete="off">
        <span class="kbd">/</span>
      </div>
      <a class="resume" id="resume" hidden><span class="rl">继续上次</span><b></b><span class="ra">→</span></a>
    </div>
    <div class="chips" id="chips">
      <button type="button" class="chip on" data-p="*"><i style="background:#fff"></i>全部单元</button>
      __CHIPS__
    </div>
  </div>
</header>

<main id="list">
__SECTIONS__
  <div class="empty" id="empty">
    <b>没有匹配的单元</b>
    换个关键词试试，或点「全部单元」查看全部 26 讲
  </div>
</main>

<footer>
  <span>由 <code>生成器/build.py</code> 自动生成 · 内容修改请编辑 <code>content/UXX.json</code> 后重跑构建</span>
  <span>快捷键：<code>/</code> 搜索　<code>Esc</code> 清空　<code>Ctrl/⌘ + 点击</code> 保留目录页另开</span>
</footer>

<script>
(function(){
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('.proj'));
  var q = document.getElementById('q');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var empty = document.getElementById('empty');
  var activeProj = '*';

  function apply(){
    var kw = (q.value || '').trim().toLowerCase();
    var any = false;
    groups.forEach(function(g){
      var shown = 0;
      g.querySelectorAll('.card').forEach(function(c){
        var okP = (activeProj === '*' || g.getAttribute('data-p') === activeProj);
        var okK = !kw || c.getAttribute('data-k').indexOf(kw) >= 0;
        var vis = okP && okK;
        c.hidden = !vis;
        if(vis) shown++;
      });
      g.hidden = shown === 0;
      if(shown > 0) any = true;
    });
    empty.classList.toggle('on', !any);
  }
  q.addEventListener('input', apply);
  q.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){ q.value = ''; apply(); q.blur(); }
    if(e.key === 'Enter'){
      var first = cards.filter(function(c){ return !c.hidden; })[0];
      if(first) first.click();
    }
  });
  chips.forEach(function(ch){
    ch.addEventListener('click', function(){
      activeProj = ch.getAttribute('data-p');
      chips.forEach(function(c){ c.classList.toggle('on', c === ch); });
      apply();
    });
  });
  document.addEventListener('keydown', function(e){
    if(e.key === '/' && document.activeElement !== q){ e.preventDefault(); q.focus(); q.select(); }
  });

  /* 继续上次 / 高亮上次打开 */
  var last = null;
  try{ last = JSON.parse(localStorage.getItem('deck_last') || 'null'); }catch(e){}
  var resume = document.getElementById('resume');
  if(last && last.href){
    resume.querySelector('b').textContent = last.label || '上次的课件';
    resume.setAttribute('href', last.href);
    resume.hidden = false;
    cards.forEach(function(c){
      if(c.getAttribute('href') === last.href) c.classList.add('is-last');
    });
  }
  cards.forEach(function(c){
    c.addEventListener('click', function(){
      try{
        localStorage.setItem('deck_last', JSON.stringify({
          href: c.getAttribute('href'),
          label: c.getAttribute('data-label')
        }));
      }catch(e){}
    });
  });
})();
</script>
</body>
</html>
"""
