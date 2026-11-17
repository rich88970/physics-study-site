/* 讀懂物理｜連續圖解引擎。
   每個圖解由多個步驟組成：圖、旁邊的說明和當下公式（含代入數值）在同一個狀態下同步更新。
   進入畫面自動播放、播完停在最後一幕；可暫停、重播、逐步查看，不需要拖曳就能看懂。

   定義方式（放在各章 figures.js）：
   Anim.define("id", {
     title: "圖標題", question: "這張圖要回答的問題",
     view: [寬, 高], origin: [原點x, 原點y], scale: 每單位像素,
     init: { 數值狀態 },
     steps: [{ label, caption, dur, to: {要變到的數值}, set: {步驟開始時切換的旗標} }],
     draw: function (d, s) { 用 d.arrow / d.line / d.label … 畫出狀態 s },
     formula: function (s) { return "此刻的 LaTeX 公式與數值"; }
   });
   正文中放 <div class="anim" data-anim="id"></div> 即可。 */
(function () {
  "use strict";
  var defs = {};
  var NS = "http://www.w3.org/2000/svg";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 給 aria-label、tooltip 用的純文字：去掉 $ 與 LaTeX 指令 */
  function plain(s) {
    return String(s).replace(/\$/g, "").replace(/\\(vec|hat|mathrm|text)\s*/g, "").replace(/\\[a-zA-Z]+/g, function (m) {
      return { "\\theta": "θ", "\\omega": "ω", "\\alpha": "α", "\\lambda": "λ", "\\pi": "π", "\\times": "×", "\\circ": "°", "\\to": "→", "\\perp": "⟂", "\\sqrt": "√" }[m] || "";
    }).replace(/[{}^]/g, "");
  }
  function ease(p) { return p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2; }
  function clone(o) { var r = {}; for (var k in o) r[k] = o[k]; return r; }
  function merge(a, b) { var r = clone(a); for (var k in b) r[k] = b[k]; return r; }

  /* 由各步驟的 to / set 推出每一步開始與結束時的狀態 */
  function keyStates(def) {
    var starts = [], ends = [];
    var cur = clone(def.init || {});
    def.steps.forEach(function (st) {
      var start = merge(cur, st.set || {});
      var end = merge(start, st.to || {});
      starts.push(start); ends.push(end); cur = end;
    });
    return { starts: starts, ends: ends };
  }
  function stateAt(def, ks, i, p) {
    var a = ks.starts[i], b = ks.ends[i], e = ease(Math.max(0, Math.min(1, p)));
    var s = clone(b);
    for (var k in b) if (typeof b[k] === "number" && typeof a[k] === "number") s[k] = a[k] + (b[k] - a[k]) * e;
    s._p = p; s._step = i;
    return s;
  }

  /* ---------- 繪圖工具：數學座標（y 向上）→ SVG ---------- */
  function Drawer(svg, labelLayer, def) {
    this.svg = svg; this.layer = labelLayer; this.def = def;
    this.W = def.view[0]; this.H = def.view[1];
    this.o = def.origin || [this.W / 2, this.H / 2];
    this.k = def.scale || 40;
    this.labels = []; this.li = 0;
    this.az = 35; this.el = 20;
  }
  var D = Drawer.prototype;
  D.begin = function () { while (this.svg.firstChild) this.svg.removeChild(this.svg.firstChild); this.li = 0; };
  D.end = function () { for (var i = this.li; i < this.labels.length; i++) this.labels[i].el.style.display = "none"; };
  D.px = function (p) { return [this.o[0] + p[0] * this.k, this.o[1] - p[1] * this.k]; };
  D.camera = function (az, el) { this.az = az; this.el = el; };
  /* 正交投影：x1 朝左前、x2 朝右、x3 朝上（右手系） */
  D.p3 = function (v) {
    var a = this.az * Math.PI / 180, e = this.el * Math.PI / 180;
    var x = v[0], y = v[1], z = v[2];
    var X = -x * Math.sin(a) + y * Math.cos(a);
    var depth = x * Math.cos(a) + y * Math.sin(a);
    var Y = z * Math.cos(e) - depth * Math.sin(e);
    return [X, Y];
  };
  D.node = function (tag, attrs, style) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (style) n.setAttribute("style", style);
    this.svg.appendChild(n); return n;
  };
  function st(o) {
    o = o || {};
    return "stroke:" + (o.color || "var(--ink)") + ";stroke-width:" + (o.width || 2) + ";fill:" + (o.fill || "none") +
      (o.dash ? ";stroke-dasharray:" + o.dash : "") + (o.opacity != null ? ";opacity:" + o.opacity : "") +
      (o.fillOpacity != null ? ";fill-opacity:" + o.fillOpacity : "") + ";stroke-linecap:round;stroke-linejoin:round";
  }
  D.line = function (a, b, o) { var A = this.px(a), B = this.px(b); return this.node("line", { x1: A[0], y1: A[1], x2: B[0], y2: B[1] }, st(o)); };
  D.poly = function (pts, o) { var self = this; return this.node("polygon", { points: pts.map(function (p) { return self.px(p).join(","); }).join(" ") }, st(o)); };
  D.path = function (pts, o) { var self = this; return this.node("polyline", { points: pts.map(function (p) { return self.px(p).join(","); }).join(" ") }, st(o)); };
  D.rect = function (x0, y0, x1, y1, o) { return this.poly([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], o); };
  D.circle = function (c, r, o) { var C = this.px(c); return this.node("circle", { cx: C[0], cy: C[1], r: r }, st(o)); };
  D.dot = function (c, o) { o = o || {}; return this.circle(c, o.r || 4.5, { color: o.color || "var(--ink)", fill: o.color || "var(--ink)", width: 1 }); };
  D.arrow = function (a, b, o) {
    o = o || {};
    var A = this.px(a), B = this.px(b);
    var dx = B[0] - A[0], dy = B[1] - A[1], L = Math.hypot(dx, dy);
    if (L < 0.5) return;
    var ux = dx / L, uy = dy / L, h = Math.min(o.head || 11, L * 0.45), w = h * 0.45;
    var bx = B[0] - ux * h, by = B[1] - uy * h;
    this.node("line", { x1: A[0], y1: A[1], x2: bx, y2: by }, st(o));
    this.node("polygon", { points: [B[0], B[1], bx - uy * w, by + ux * w, bx + uy * w, by - ux * w].join(",") },
      "fill:" + (o.color || "var(--ink)") + ";stroke:none" + (o.opacity != null ? ";opacity:" + o.opacity : ""));
  };
  D.arc = function (c, r, a0, a1, o) {
    var pts = [], n = 40;
    for (var i = 0; i <= n; i++) { var t = (a0 + (a1 - a0) * i / n) * Math.PI / 180; pts.push([c[0] + r * Math.cos(t), c[1] + r * Math.sin(t)]); }
    return this.path(pts, o);
  };
  D.rightAngle = function (corner, u, v, size, o) {
    var s = size || 0.25;
    var p1 = [corner[0] + u[0] * s, corner[1] + u[1] * s], p3 = [corner[0] + v[0] * s, corner[1] + v[1] * s];
    var p2 = [p1[0] + v[0] * s, p1[1] + v[1] * s];
    return this.path([p1, p2, p3], o || { color: "var(--muted)", width: 1.3 });
  };
  D.grid = function (x0, x1, y0, y1, o) {
    for (var x = Math.ceil(x0); x <= x1; x++) this.line([x, y0], [x, y1], { color: "var(--grid)", width: 1 });
    for (var y = Math.ceil(y0); y <= y1; y++) this.line([x0, y], [x1, y], { color: "var(--grid)", width: 1 });
  };
  D.axes = function (xr, yr, names) {
    names = names || ["x", "y"];
    this.arrow([xr[0], 0], [xr[1], 0], { color: "var(--muted)", width: 1.5, head: 9 });
    this.arrow([0, yr[0]], [0, yr[1]], { color: "var(--muted)", width: 1.5, head: 9 });
    this.label([xr[1] + 0.3, -0.05], names[0], { color: "var(--muted)" });
    this.label([0.05, yr[1] + 0.3], names[1], { color: "var(--muted)" });
  };
  /* 3D 工具 */
  D.line3 = function (a, b, o) { return this.line(this.p3(a), this.p3(b), o); };
  D.arrow3 = function (a, b, o) { return this.arrow(this.p3(a), this.p3(b), o); };
  D.dot3 = function (a, o) { return this.dot(this.p3(a), o); };
  D.poly3 = function (pts, o) { var self = this; return this.poly(pts.map(function (p) { return self.p3(p); }), o); };
  D.path3 = function (pts, o) { var self = this; return this.path(pts.map(function (p) { return self.p3(p); }), o); };
  D.label3 = function (a, t, o) { return this.label(this.p3(a), t, o); };
  /* 標籤以 KaTeX 排版（HTML 疊在 SVG 上），字串未變就不重排 */
  D.label = function (p, t, o) {
    o = o || {};
    var P = this.px(p);
    var slot = this.labels[this.li];
    if (!slot) {
      var el = document.createElement("div"); el.className = "fig-label";
      this.layer.appendChild(el); slot = this.labels[this.li] = { el: el, tex: null };
    }
    this.li++;
    var x = P[0] + (o.dx || 0), y = P[1] + (o.dy || 0);
    slot.el.style.display = "";
    slot.el.style.left = (x / this.W * 100) + "%";
    slot.el.style.top = (y / this.H * 100) + "%";
    slot.el.style.color = o.color || "var(--ink)";
    slot.el.style.fontSize = o.size ? (o.size * (this.labelScale || 1)) + "px" : "";
    if (slot.tex !== t) { slot.tex = t; slot.el.innerHTML = window.Study ? window.Study.tex(t) : t; }
  };

  /* ---------- 播放器 ---------- */
  function Player(host, def) {
    this.def = def; this.host = host;
    this.ks = keyStates(def);
    this.i = 0; this.t = 0; this.playing = false; this.done = false;
    this.speed = 1;
    this.build();
    this.render(stateAt(def, this.ks, 0, 0));
  }
  var P = Player.prototype;
  P.build = function () {
    var def = this.def, host = this.host, self = this;
    host.classList.add("figure");
    host.setAttribute("role", "group");
    host.setAttribute("aria-label", def.title);
    host.innerHTML =
      '<div class="fig-head"><h4></h4><span class="q"></span></div>' +
      '<div class="fig-progress"><i></i></div>' +
      '<div class="fig-body"><div class="fig-stage"><div style="position:relative"><svg viewBox="0 0 ' + def.view[0] + " " + def.view[1] + '" role="img"></svg><div class="fig-labels" style="position:absolute;inset:0"></div></div></div>' +
      '<div class="fig-panel" aria-live="polite"><span class="fig-step-label"></span><div class="fig-caption"></div><div class="fig-formula"></div></div></div>' +
      '<div class="fig-controls"><button type="button" class="play">▶ 播放</button><button type="button" class="prev" aria-label="上一步">‹ 上一步</button><button type="button" class="next" aria-label="下一步">下一步 ›</button><button type="button" class="replay">↺ 重播</button><span class="steps"></span></div>';
    host.querySelector("h4").innerHTML = def.title;
    host.querySelector(".q").innerHTML = def.question || "";
    if (window.Study) window.Study.renderMath(host.querySelector(".fig-head"));
    host.querySelector(".fig-stage svg").setAttribute("aria-label", plain(def.title));
    this.drawer = new Drawer(host.querySelector(".fig-stage svg"), host.querySelector(".fig-labels"), def);
    this.bar = host.querySelector(".fig-progress>i");
    this.cap = host.querySelector(".fig-caption");
    this.form = host.querySelector(".fig-formula");
    this.stepLabel = host.querySelector(".fig-step-label");
    this.btnPlay = host.querySelector(".play");
    var steps = host.querySelector(".steps");
    def.steps.forEach(function (s, i) {
      var b = document.createElement("button"); b.type = "button"; b.textContent = i + 1;
      b.setAttribute("aria-label", "第 " + (i + 1) + " 步：" + plain(s.label));
      b.title = plain(s.label);
      b.addEventListener("click", function () { self.jump(i); });
      steps.appendChild(b);
    });
    this.stepBtns = steps.querySelectorAll("button");
    this.btnPlay.addEventListener("click", function () { self.playing ? self.pause() : self.play(); });
    host.querySelector(".replay").addEventListener("click", function () { self.i = 0; self.t = 0; self.done = false; self.play(); });
    host.querySelector(".prev").addEventListener("click", function () { self.jump(Math.max(0, self.i - (self.t > 0.05 && !self.done ? 0 : 1))); });
    host.querySelector(".next").addEventListener("click", function () { self.jump(Math.min(def.steps.length - 1, self.i + 1)); });
    document.addEventListener("themechange", function () { self.render(self.current); });
  };
  P.setStepText = function (i) {
    if (this.shownStep === i) return;
    this.shownStep = i;
    var s = this.def.steps[i];
    this.stepLabel.innerHTML = "第 " + (i + 1) + " / " + this.def.steps.length + " 步｜" + s.label;
    this.cap.innerHTML = s.caption || "";
    if (window.Study) { window.Study.renderMath(this.stepLabel); window.Study.renderMath(this.cap); }
    this.stepBtns.forEach(function (b, k) { b.setAttribute("aria-current", k === i ? "true" : "false"); });
  };
  P.render = function (s) {
    this.current = s;
    var d = this.drawer;
    d.begin(); this.def.draw(d, s); d.end();
    this.setStepText(s._step);
    var f = this.def.formula ? this.def.formula(s) : "";
    if (f !== this.lastFormula) {
      this.lastFormula = f;
      this.form.innerHTML = f ? (window.Study ? window.Study.tex(f, true) : f) : "";
    }
    var total = this.def.steps.length;
    this.bar.style.width = ((s._step + Math.min(1, s._p)) / total * 100) + "%";
  };
  P.durOf = function (i) { var s = this.def.steps[i]; return (s.dur != null ? s.dur : 2200) + (s.hold != null ? s.hold : 1600); };
  P.moveOf = function (i) { var s = this.def.steps[i]; return s.dur != null ? s.dur : 2200; };
  P.play = function () {
    if (this.done) { this.i = 0; this.t = 0; this.done = false; }
    this.playing = true; this.btnPlay.textContent = "❚❚ 暫停";
    var self = this, last = null;
    cancelAnimationFrame(this.raf);
    function tick(ts) {
      if (!self.playing) return;
      if (last == null) last = ts;
      var dt = (ts - last) * self.speed; last = ts;
      var elapsed = self.t * self.durOf(self.i) + dt;
      if (elapsed >= self.durOf(self.i)) {
        if (self.i < self.def.steps.length - 1) { self.i++; self.t = 0; }
        else { self.t = 1; self.render(stateAt(self.def, self.ks, self.i, 1)); self.finish(); return; }
      } else self.t = elapsed / self.durOf(self.i);
      var p = Math.min(1, self.t * self.durOf(self.i) / Math.max(1, self.moveOf(self.i)));
      self.render(stateAt(self.def, self.ks, self.i, p));
      self.raf = requestAnimationFrame(tick);
    }
    this.raf = requestAnimationFrame(tick);
  };
  P.pause = function () { this.playing = false; cancelAnimationFrame(this.raf); this.btnPlay.textContent = "▶ 播放"; };
  P.finish = function () { this.playing = false; this.done = true; this.btnPlay.textContent = "▶ 再播一次"; };
  P.jump = function (i) {
    this.pause(); this.i = i; this.t = 1; this.done = i === this.def.steps.length - 1;
    this.render(stateAt(this.def, this.ks, i, 1));
    if (this.done) this.btnPlay.textContent = "▶ 再播一次";
  };

  var Anim = {
    Drawer: Drawer,
    get: function (id) { return defs[id]; },
    list: function () { return Object.keys(defs); },
    define: function (id, def) { defs[id] = def; },
    mountAll: function (root) {
      var players = [];
      (root || document).querySelectorAll(".anim[data-anim]").forEach(function (host) {
        var def = defs[host.getAttribute("data-anim")];
        if (!def || host._player) return;
        host._player = new Player(host, def);
        players.push(host._player);
      });
      if (reduce || !("IntersectionObserver" in window)) {
        players.forEach(function (p) { p.jump(0); });
        return;
      }
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          var p = en.target._player; if (!p) return;
          if (en.isIntersecting && en.intersectionRatio >= 0.45) {
            if (!p.started) { p.started = true; p.play(); }
            else if (p.autoPaused) { p.autoPaused = false; p.play(); }
          } else if (!en.isIntersecting && p.playing) { p.autoPaused = true; p.pause(); }
        });
      }, { threshold: [0, 0.45] });
      players.forEach(function (p) { io.observe(p.host); });
    },
    fmt: function (x, n) {
      n = n == null ? 2 : n;
      var v = Math.abs(x) < Math.pow(10, -n) / 2 ? 0 : x;
      var s = v.toFixed(n);
      if (s.indexOf(".") >= 0) s = s.replace(/0+$/, "").replace(/\.$/, "");
      return s === "-0" ? "0" : s;
    },
    rad: function (deg) { return deg * Math.PI / 180; }
  };
  window.Anim = Anim;
})();
