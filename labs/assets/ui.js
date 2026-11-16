/* ==========================================================================
   HTML5 + CSS3 互动教程 · 交互内核
   主题切换 / 分段控件 / 滑块 / 开关 / 代码高亮 / 单元自测 / 进度记录
   ========================================================================== */
(function (w) {
  "use strict";
  var WB = {};

  /* ---------- 基础 ---------- */
  WB.$ = function (s, r) { return (r || document).querySelector(s); };
  WB.$$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  WB.on = function (el, ev, fn) { if (el) el.addEventListener(ev, fn); return el; };

  var store = {
    get: function (k, d) {
      try { var v = localStorage.getItem("wbx:" + k); return v === null ? d : JSON.parse(v); }
      catch (e) { return d; }
    },
    set: function (k, v) {
      try { localStorage.setItem("wbx:" + k, JSON.stringify(v)); } catch (e) {}
    }
  };
  WB.store = store;

  /* ---------- 主题 ---------- */
  WB.setTheme = function (t) {
    document.documentElement.setAttribute("data-theme", t);
    store.set("theme", t);
    var b = WB.$("#themeBtn");
    if (b) { b.textContent = t === "dark" ? "☀" : "☾"; b.title = t === "dark" ? "切换到浅色" : "切换到深色"; }
  };
  WB.initTheme = function () {
    var q = /[?&]theme=(dark|light)/.exec(location.search || "");
    var saved = store.get("theme", null);
    var t = (q && q[1]) || saved || (w.matchMedia && w.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
    WB.setTheme(t);
    WB.on(WB.$("#themeBtn"), "click", function () {
      WB.setTheme(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  };

  /* ---------- 提示条 ---------- */
  var toastEl;
  WB.toast = function (msg) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.classList.remove("show"); }, 1600);
  };

  /* ---------- 分段控件 ---------- */
  // WB.seg(el, cb) -> { get, set }
  WB.seg = function (el, cb) {
    if (!el) return { get: function () { return null; }, set: function () {} };
    var btns = WB.$$("button", el);
    var val = null;
    function set(v, silent) {
      val = String(v);
      btns.forEach(function (b) {
        var on = b.dataset.v === val;
        b.classList.toggle("on", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
      if (!silent && cb) cb(val);
    }
    btns.forEach(function (b) {
      b.addEventListener("click", function () { set(b.dataset.v); });
    });
    var cur = btns.filter(function (b) { return b.classList.contains("on"); })[0] || btns[0];
    if (cur) {
      if (!cur.classList.contains("on")) cur.classList.add("on");
      val = cur.dataset.v;
    }
    return {
      get: function () { return val; },
      set: set,
      el: el
    };
  };

  /* ---------- 滑块 ---------- */
  WB.range = function (el, outEl, cb) {
    if (!el) return;
    function paint() {
      var min = +el.min || 0, max = +el.max || 100;
      el.style.setProperty("--p", ((el.value - min) / (max - min) * 100) + "%");
      if (outEl) outEl.textContent = el.dataset.unit ? el.value + el.dataset.unit : el.value;
      if (cb) cb(+el.value, el.value);
    }
    el.addEventListener("input", paint);
    paint();
    return el;
  };

  /* ---------- 开关 ---------- */
  WB.switch = function (el, cb) {
    if (!el) return;
    el.addEventListener("change", function () { if (cb) cb(el.checked); });
    return el;
  };

  /* ---------- 代码高亮 ---------- */
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  var CSS_RE = /(\/\*[\s\S]*?\*\/)|(^[^{\n}]+\{)|("(?:[^"\\]|\\.)*")|(#[0-9a-fA-F]{3,8}\b)|(-?\d*\.?\d+(?:px|em|rem|%|s|ms|deg|turn|vh|vw|vmin|vmax|fr|ch|ex)?)|([a-zA-Z-]{2,})(?=\s*:)/gm;
  var HTML_RE = /(&lt;\/?)([a-zA-Z][\w:-]*)|([a-zA-Z-]+)=("[^"]*"|'[^']*')|(\/?&gt;)/g;

  WB.hl = function (src, lang) {
    var s = esc(src);
    if (lang === "html") {
      return s.replace(HTML_RE, function (m, open, tag, attr, val, close) {
        if (open) return '<span class="t">' + open + tag + "</span>";
        if (attr) return '<span class="a">' + attr + "</span>=<span class=\"s\">" + val + "</span>";
        if (close) return '<span class="t">' + close + "</span>";
        return m;
      });
    }
    if (lang === "css") {
      return s.replace(CSS_RE, function (m, cmt, sel, str, hex, num, prop) {
        if (cmt) return '<span class="c">' + cmt + "</span>";
        if (sel) return '<span class="t">' + sel + "</span>";
        if (str) return '<span class="s">' + str + "</span>";
        if (hex) return '<span class="n">' + hex + "</span>";
        if (num) return '<span class="n">' + num + "</span>";
        if (prop) return '<span class="p">' + prop + "</span>";
        return m;
      });
    }
    return s;
  };

  // WB.code(el, text, lang) 更新代码块（含复制按钮）
  WB.code = function (el, text, lang) {
    if (!el) return;
    el.innerHTML = WB.hl(text, lang || "css");
  };

  // 给所有 .code-wrap 自动加复制按钮
  WB.initCopy = function () {
    WB.$$(".code-wrap").forEach(function (wrap) {
      if (wrap.querySelector(".copy")) return;
      var btn = document.createElement("button");
      btn.className = "copy";
      btn.type = "button";
      btn.textContent = "复制";
      btn.addEventListener("click", function () {
        var pre = wrap.querySelector(".code");
        var text = pre ? pre.textContent : "";
        var done = function () { btn.textContent = "已复制"; WB.toast("代码已复制到剪贴板"); setTimeout(function () { btn.textContent = "复制"; }, 1400); };
        if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { WB.toast("请手动选择复制"); });
        else WB.toast("当前环境不支持自动复制");
      });
      wrap.appendChild(btn);
    });
  };

  /* ---------- 进度 ---------- */
  WB.progress = {
    all: function () { return store.get("progress", {}); },
    done: function (id) { var p = store.get("progress", {}); return !!p[id]; },
    mark: function (id, score) {
      var p = store.get("progress", {});
      p[id] = { score: score, at: Date.now() };
      store.set("progress", p);
    }
  };

  /* ---------- 单元自测 ---------- */
  WB.quiz = function (root, list, projectId) {
    if (!root) return;
    var multi = {};
    var html = "";
    list.forEach(function (q, i) {
      multi[i] = q.type === "multi";
      html += '<div class="qcard" data-i="' + i + '">';
      html += '<div class="qtext"><span>Q' + (i + 1) + "</span>" + q.q + (multi[i] ? ' <em class="muted">（多选）</em>' : "") + "</div>";
      html += '<div class="opts">';
      q.opts.forEach(function (o, j) {
        html += '<label class="opt" data-j="' + j + '"><input type="' + (multi[i] ? "checkbox" : "radio") +
          '" name="q' + i + '" value="' + j + '"><span>' + o + "</span></label>";
      });
      html += "</div><div class=\"why\">" + (q.why || "") + "</div></div>";
    });
    html += '<div class="quiz-foot"><button class="btn primary" data-act="check">提交批改</button>' +
      '<button class="btn" data-act="reset">重做</button><span class="score" data-score>共 ' + list.length + " 题，尚未作答</span></div>";
    root.innerHTML = html;

    function clearMarks() {
      WB.$$(".qcard", root).forEach(function (c) {
        c.querySelectorAll(".opt").forEach(function (o) { o.classList.remove("ok", "bad"); });
        c.querySelector(".why").classList.remove("show");
      });
      WB.$$("input", root).forEach(function (i) { i.checked = false; });
    }

    WB.$$("[data-act]", root).forEach(function (btn) {
      btn.addEventListener("click", function () {
        var act = btn.dataset.act;
        if (act === "reset") {
          clearMarks();
          root.querySelector("[data-score]").textContent = "共 " + list.length + " 题，尚未作答";
          return;
        }
        var right = 0, answered = 0;
        list.forEach(function (q, i) {
          var card = root.querySelector('.qcard[data-i="' + i + '"]');
          var picked = WB.$$("input", card).filter(function (x) { return x.checked; }).map(function (x) { return +x.value; });
          if (picked.length) answered++;
          var ans = Array.isArray(q.a) ? q.a.slice() : [q.a];
          var ok = picked.length === ans.length && picked.every(function (v) { return ans.indexOf(v) > -1; });
          if (ok) right++;
          WB.$$(".opt", card).forEach(function (o) {
            var j = +o.dataset.j;
            o.classList.remove("ok", "bad");
            if (ans.indexOf(j) > -1) o.classList.add("ok");
            else if (picked.indexOf(j) > -1) o.classList.add("bad");
          });
          card.querySelector(".why").classList.add("show");
        });
        var msg = "得分 " + right + "/" + list.length;
        if (answered < list.length) msg += "（还有 " + (list.length - answered) + " 题未作答）";
        else if (right === list.length) msg += " · 全部正确，可以进入下一讲 🎉";
        else if (right >= list.length * 0.6) msg += " · 基本掌握，看看标红的解析";
        else msg += " · 建议回到舞台再动手试一遍";
        root.querySelector("[data-score]").innerHTML = "<b>" + msg.replace("得分 ", "得分 ") + "</b>";
        if (projectId && right >= list.length * 0.6) WB.progress.mark(projectId, right + "/" + list.length);
      });
    });
  };

  /* ---------- 自动初始化 ---------- */
  WB.initTheme();
  document.addEventListener("DOMContentLoaded", function () {
    WB.initCopy();
    WB.$$("input[type=range]").forEach(function (r) {
      if (!r.dataset.auto) return;
      WB.range(r, null, null);
    });
  });

  w.WB = WB;
})(window);
