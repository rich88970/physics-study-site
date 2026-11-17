/* 力學 Lecture 1（p.1–49）第二批圖解：補足每一節的圖，並供影片使用（plane-abc、solve-x）。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt, rad = A.rad;
  function deg(x) { return F(x, 1) + "^\\circ"; }
  function add(u, v) { return [u[0] + v[0], u[1] + v[1], (u[2] || 0) + (v[2] || 0)]; }
  function sub(u, v) { return [u[0] - v[0], u[1] - v[1], (u[2] || 0) - (v[2] || 0)]; }
  function mul(k, u) { return [k * u[0], k * u[1], k * (u[2] || 0)]; }
  function dot(u, v) { return u[0] * v[0] + u[1] * v[1] + (u[2] || 0) * (v[2] || 0); }
  function cross(u, v) { return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]; }
  function len(u) { return Math.sqrt(dot(u, u)); }
  function unit(u) { var L = len(u); return [u[0] / L, u[1] / L, (u[2] || 0) / L]; }
  function lerp(a, b, t) { return add(mul(1 - t, a), mul(t, b)); }
  function vec(u, n) { return "(" + u.map(function (x) { return F(x, n == null ? 2 : n); }).join(",\\ ") + ")"; }
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)", ORANGE = "var(--k-pit)";

  function axes3(d, L, names, o) {
    o = o || {};
    names = names || ["x_1", "x_2", "x_3"];
    [[L, 0, 0], [0, L, 0], [0, 0, L]].forEach(function (e, i) {
      d.arrow3([0, 0, 0], e, { color: MUTED, width: 1.2, head: 8, opacity: o.opacity == null ? 0.75 : o.opacity });
      d.label3(mul(1.1, e), names[i], { color: MUTED, size: 13 });
    });
  }
  /* 3D 弧：從方向 u 轉到方向 w（以 c 為中心、半徑 r） */
  function arc3(d, c, u, w, r, o) {
    var pts = [], uu = unit(u), ww = unit(w);
    for (var i = 0; i <= 24; i++) { var t = i / 24; pts.push(add(c, mul(r, unit(lerp(uu, ww, t))))); }
    d.path3(pts, o || { color: INK, width: 1.5 });
  }

  /* ========== 1.1 微分：df 與 Δf ========== */
  A.define("differential", {
    title: "$\\mathrm df=f'(x)\\,\\mathrm dx$ 與真正的改變量 $\\Delta f$",
    question: "$\\mathrm dx$ 越來越小時，切線估計 $\\mathrm df$ 和真正的 $\\Delta f$ 差多少？",
    view: [420, 300], origin: [60, 280], scale: 62,
    init: { dx: 1 },
    steps: [
      { label: "$\\mathrm dx=1$", caption: "$f(x)=x^2$，在 $x=1$ 畫切線（綠，斜率 $f'(1)=2$）。$x$ 增加 $\\mathrm dx=1$：沿切線上升 $\\mathrm df=2$，沿曲線實際上升 $\\Delta f=3$，差 $1$。", dur: 300, hold: 3200 },
      { label: "$\\mathrm dx=0.5$", caption: "$\\mathrm dx$ 減半：$\\mathrm df=1$、$\\Delta f=1.25$，差 $0.25$——差距縮成四分之一，因為差距就是 $(\\mathrm dx)^2$。", to: { dx: 0.5 } },
      { label: "$\\mathrm dx=0.1$", caption: "$\\mathrm dx=0.1$：$\\mathrm df=0.2$、$\\Delta f=0.21$，差只剩 $0.01$。$\\mathrm dx$ 越小，切線估計越準，所以微小改變量寫成 $\\mathrm df=f'(x)\\,\\mathrm dx$。", to: { dx: 0.1 }, dur: 2600, hold: 3200 }
    ],
    draw: function (d, s) {
      var pts = [];
      for (var i = 0; i <= 60; i++) { var x = 2.15 * i / 60; pts.push([x, x * x]); }
      d.arrow([-0.3, 0], [5.6, 0], { color: MUTED, width: 1.2, head: 8 });
      d.arrow([0, -0.2], [0, 4.4], { color: MUTED, width: 1.2, head: 8 });
      d.label([5.6, -0.25], "x", { color: MUTED });
      d.path(pts, { color: INK, width: 2 });
      d.line([0.2, -0.6], [2.4, 3.8], { color: GREEN, width: 1.6, opacity: 0.8 });
      var x0 = 1, x1 = 1 + s.dx;
      d.line([x0, 1], [x1, 1], { color: MUTED, width: 1.2, dash: "4 3" });
      d.line([x1, 1], [x1, 1 + 2 * s.dx], { color: GREEN, width: 4 });
      d.line([x1, 1 + 2 * s.dx], [x1, x1 * x1], { color: PURPLE, width: 4 });
      d.line([x1 + 0.12, 1], [x1 + 0.12, x1 * x1], { color: RED, width: 2.2 });
      d.dot([x0, 1], { r: 4 }); d.dot([x1, x1 * x1], { r: 4, color: RED });
      d.label([(x0 + x1) / 2, 0.75], "\\mathrm dx", { size: 13 });
      if (s.dx > 0.3) {
        d.label([x1 - 0.35, 1 + s.dx], "\\mathrm df", { color: GREEN, size: 13 });
        d.label([x1 + 0.55, 1 + s.dx * 1.2], "\\Delta f", { color: RED, size: 13 });
      }
      d.label([1.3, 4.1], "f(x)=x^2", { size: 13 });
    },
    formula: function (s) {
      var dx = s.dx, Df = (1 + dx) * (1 + dx) - 1, df = 2 * dx;
      return "\\begin{aligned}\\mathrm df&=f'(1)\\,\\mathrm dx=2\\times" + F(dx) + "=" + F(df) + "\\\\ \\Delta f&=(1+" + F(dx) + ")^2-1^2=" + F(Df, 4) + "\\\\ \\Delta f-\\mathrm df&=(\\mathrm dx)^2=" + F(Df - df, 4) + "\\end{aligned}";
    }
  });

  /* ========== 2.3–2.5 三維分量與長度 ========== */
  A.define("vec3d", {
    title: "三維向量：分量相加、長度用兩次畢氏定理",
    question: "$\\vec A=(2,1,2)$ 怎麼由單位向量組成？長度怎麼算？",
    view: [420, 320], origin: [190, 250], scale: 62,
    init: { k1: 0, k2: 0, k3: 0, shadow: 0, hyp: 0, uhat: 0, az: 32 },
    steps: [
      { label: "單位向量", caption: "$\\hat i,\\hat j,\\hat k$ 長度都是 $1$，只負責方向。", dur: 300, hold: 2200 },
      { label: "$2\\hat i$", caption: "先沿 $\\hat i$ 方向走 $A_1=2$。", to: { k1: 1 } },
      { label: "$+\\hat j$", caption: "接著沿 $\\hat j$ 走 $A_2=1$。", to: { k2: 1 } },
      { label: "$+2\\hat k$", caption: "最後沿 $\\hat k$ 往上走 $A_3=2$，抵達 $\\vec A$ 的箭頭：$\\vec A=2\\hat i+\\hat j+2\\hat k$。", to: { k3: 1 } },
      { label: "影子", caption: "$\\vec A$ 在地面（$x_1x_2$ 平面）的影子長 $\\sqrt{2^2+1^2}=\\sqrt5$：第一次畢氏定理。", set: { shadow: 1 }, to: { az: 40 } },
      { label: "長度", caption: "影子與高度 $2$ 垂直，再用一次畢氏定理：$|\\vec A|=\\sqrt{(\\sqrt5)^2+2^2}=3$。", set: { hyp: 1 }, to: { az: 46 } },
      { label: "單位向量 $\\hat A$", caption: "除以長度得到同方向的單位向量 $\\hat A=\\vec A/3$（紫，長度 1）。", set: { uhat: 1 }, to: { az: 50 }, hold: 2600 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 22);
      axes3(d, 2.9);
      d.arrow3([0, 0, 0], [1, 0, 0], { color: RED, width: 3, head: 9 });
      d.arrow3([0, 0, 0], [0, 1, 0], { color: BLUE, width: 3, head: 9 });
      d.arrow3([0, 0, 0], [0, 0, 1], { color: GREEN, width: 3, head: 9 });
      d.label3([0.75, -0.25, 0.1], "\\hat i", { color: RED, size: 13 });
      d.label3([0.1, 0.85, -0.25], "\\hat j", { color: BLUE, size: 13 });
      d.label3([-0.2, 0.1, 0.8], "\\hat k", { color: GREEN, size: 13 });
      var p1 = [2 * s.k1, 0, 0], p2 = [2, s.k2, 0], p3 = [2, 1, 2 * s.k3];
      if (s.k1 > 0.01) d.line3([0, 0, 0], p1, { color: RED, width: 5, opacity: 0.6 });
      if (s.k2 > 0.01) d.line3([2, 0, 0], p2, { color: BLUE, width: 5, opacity: 0.6 });
      if (s.k3 > 0.01) d.line3([2, 1, 0], p3, { color: GREEN, width: 5, opacity: 0.6 });
      if (s.k3 > 0.99) { d.arrow3([0, 0, 0], [2, 1, 2], { color: INK, width: 3 }); d.label3([1.1, 0.4, 1.35], "\\vec A", {}); }
      if (s.shadow) { d.line3([0, 0, 0], [2, 1, 0], { color: ORANGE, width: 3, dash: "6 4" }); d.label3([1.1, 0.8, -0.1], "\\sqrt5", { color: ORANGE, size: 13 }); }
      if (s.hyp) d.rightAngle(d.p3([2, 1, 0]), unit(sub(d.p3([0, 0, 0]), d.p3([2, 1, 0]))), unit(sub(d.p3([2, 1, 1]), d.p3([2, 1, 0]))), 0.22);
      if (s.uhat) { d.arrow3([0, 0, 0], mul(1 / 3, [2, 1, 2]), { color: PURPLE, width: 4 }); d.label3([0.2, 0.55, 0.8], "\\hat A", { color: PURPLE, size: 13 }); }
    },
    formula: function (s) {
      switch (s._step) {
        case 0: return "|\\hat i|=|\\hat j|=|\\hat k|=1";
        case 1: return "2\\hat i";
        case 2: return "2\\hat i+1\\hat j";
        case 3: return "\\vec A=2\\hat i+\\hat j+2\\hat k=(2,1,2)";
        case 4: return "\\text{影子長}=\\sqrt{A_1^2+A_2^2}=\\sqrt{4+1}=\\sqrt5";
        case 5: return "|\\vec A|=\\sqrt{(\\sqrt5)^2+A_3^2}=\\sqrt{4+1+4}=3";
        default: return "\\hat A=\\frac{\\vec A}{|\\vec A|}=\\left(\\tfrac23,\\tfrac13,\\tfrac23\\right),\\quad |\\hat A|=1";
      }
    }
  });

  /* ========== 2.4 極座標與象限 ========== */
  A.define("polar", {
    title: "由分量求角度：小心象限",
    question: "$\\vec A=(-1,\\sqrt3)$ 的角度是 $-60^\\circ$ 還是 $120^\\circ$？",
    view: [420, 280], origin: [220, 190], scale: 70,
    init: { calc: 0, fix: 0, r: 0 },
    steps: [
      { label: "畫出向量", caption: "$\\vec A=(-1,\\sqrt3)$：$x$ 分量負、$y$ 分量正，箭頭在<strong>第二象限</strong>。", dur: 300, hold: 2400 },
      { label: "長度", caption: "長度 $r=\\sqrt{(-1)^2+(\\sqrt3)^2}=2$（灰色圓半徑 2）。", set: { r: 1 }, dur: 300, hold: 2400 },
      { label: "計算機的答案", caption: "$\\tan^{-1}\\!\\big(\\tfrac{\\sqrt3}{-1}\\big)$ 計算機給 $-60^\\circ$（橘色虛線）——它指向第四象限，和箭頭方向相反。", set: { calc: 1 }, dur: 300, hold: 3000 },
      { label: "加 180°", caption: "$\\tan$ 每 $180^\\circ$ 重複一次，所以正確角度是 $-60^\\circ+180^\\circ=120^\\circ$。", set: { fix: 1 }, to: {}, dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      d.grid(-2.8, 2.8, -2.3, 2.5);
      d.axes([-2.9, 2.9], [-2.4, 2.5]);
      if (s.r) d.circle([0, 0], 2 * 70, { color: MUTED, width: 1, dash: "3 4" });
      var P = [-1, Math.sqrt(3)];
      d.line(P, [-1, 0], { color: MUTED, width: 1, dash: "3 3" });
      d.label([-0.5, -0.25], "A_1=-1", { size: 12, color: MUTED });
      d.label([-1.55, 0.86], "A_2=\\sqrt3", { size: 12, color: MUTED });
      if (s.calc) { d.line([0, 0], [1, -Math.sqrt(3)], { color: ORANGE, width: 2.2, dash: "6 4" }); d.arc([0, 0], 0.5, -60, 0, { color: ORANGE, width: 1.5 }); d.label([1.25, -1.6], "-60^\\circ\\ \\text{（錯）}", { color: ORANGE, size: 13 }); }
      if (s.fix) { d.arc([0, 0], 0.6, 0, 120, { color: GREEN, width: 2 }); d.label([0.55, 0.75], "120^\\circ", { color: GREEN, size: 13 }); }
      d.arrow([0, 0], P, { color: RED, width: 3 });
      d.label([-1.25, 1.95], "\\vec A", { color: RED });
    },
    formula: function (s) {
      switch (s._step) {
        case 0: return "\\vec A=(A_1,A_2)=(-1,\\ \\sqrt3)";
        case 1: return "r=\\sqrt{A_1^2+A_2^2}=\\sqrt{1+3}=2";
        case 2: return "\\tan\\theta=\\frac{A_2}{A_1}=-\\sqrt3,\\quad \\tan^{-1}(-\\sqrt3)=-60^\\circ\\ (\\text{錯象限})";
        default: return "\\begin{gathered}\\theta=-60^\\circ+180^\\circ=120^\\circ\\\\ r\\cos120^\\circ=-1,\\ \\ r\\sin120^\\circ=\\sqrt3\\ \\checkmark\\end{gathered}";
      }
    }
  });

  /* ========== 4 Example 1.5（3D） ========== */
  var E15A = [1, 2, -2], E15B = [4, 2, -3];
  A.define("ex15", {
    title: "Example 1.5：$B\\to A$ 的向量、夾角、$\\vec B$ 沿 $\\vec A$ 的分量",
    question: "三個要求在圖上各是什麼？",
    view: [430, 330], origin: [175, 150], scale: 42,
    init: { c: 0, ang: 0, proj: 0, az: 28 },
    steps: [
      { label: "兩個位置向量", caption: "$\\vec A=(1,2,-2)$（紅）、$\\vec B=(4,2,-3)$（藍）都從原點出發，指向點 $A$、點 $B$。", dur: 1200, hold: 1800, to: { az: 32 } },
      { label: "(a) 從 B 到 A", caption: "從點 $B$ 指向點 $A$ 的向量是「終點減起點」$\\vec C=\\vec A-\\vec B$（綠），長度 $\\sqrt{10}$。", set: { c: 1 }, to: { az: 38 } },
      { label: "(b) 夾角", caption: "$\\vec A,\\vec B$ 在原點的夾角 $\\theta$：由 $\\cos\\theta=\\frac{\\vec A\\cdot\\vec B}{|\\vec A||\\vec B|}$ 得約 $29.9^\\circ$。", set: { c: 0, ang: 1 }, to: { az: 44 } },
      { label: "(c) 投影", caption: "$\\vec B$ 往 $\\vec A$ 所在直線作垂線，影子長 $B_A=\\frac{14}{3}\\approx4.67$。影子比 $|\\vec A|=3$ 還長，所以要把 $\\vec A$ 的直線延長（虛線）。", set: { proj: 1 }, to: { az: 50 }, hold: 3000 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 22);
      axes3(d, 3, ["x", "y", "z"], { opacity: 0.5 });
      if (s.proj) {
        var ah = unit(E15A), foot = mul(14 / 3, ah);
        d.line3([0, 0, 0], mul(5.2, ah), { color: RED, width: 1.2, dash: "5 4" });
        d.line3(E15B, foot, { color: MUTED, width: 1.2, dash: "4 3" });
        d.line3([0, 0, 0], foot, { color: GREEN, width: 5, opacity: 0.7 });
        d.label3(add(mul(0.75, foot), [0, 0.6, 0]), "B_A=\\tfrac{14}{3}", { color: GREEN, size: 13 });
      }
      d.arrow3([0, 0, 0], E15A, { color: RED, width: 3 });
      d.arrow3([0, 0, 0], E15B, { color: BLUE, width: 3 });
      d.label3(add(E15A, [0, -0.3, -0.4]), "A", { color: RED });
      d.label3(add(E15B, [0.2, 0.3, -0.3]), "B", { color: BLUE });
      if (s.c) { d.arrow3(E15B, E15A, { color: GREEN, width: 3 }); d.label3(add(mul(0.5, add(E15A, E15B)), [0, 0.3, 0.5]), "\\vec C=\\vec A-\\vec B", { color: GREEN, size: 13 }); }
      if (s.ang) { arc3(d, [0, 0, 0], E15A, E15B, 1.3); d.label3(mul(0.62, unit(add(unit(E15A), unit(E15B)))), "\\theta", { size: 14 }); }
    },
    formula: function (s) {
      switch (s._step) {
        case 0: return "\\vec A=(1,2,-2),\\quad \\vec B=(4,2,-3)";
        case 1: return "\\begin{gathered}\\vec C=\\vec A-\\vec B=(-3,0,1)\\\\ |\\vec C|=\\sqrt{9+0+1}=\\sqrt{10}\\end{gathered}";
        case 2: return "\\begin{gathered}\\cos\\theta=\\frac{4+4+6}{3\\sqrt{29}}=\\frac{14}{3\\sqrt{29}}\\approx0.867\\\\ \\theta\\approx29.9^\\circ\\end{gathered}";
        default: return "B_A=\\frac{\\vec B\\cdot\\vec A}{|\\vec A|}=\\frac{14}{3}\\approx4.67\\ \\gt|\\vec A|=3";
      }
    }
  });

  /* ========== 1-17 餘弦定律 ========== */
  A.define("cosine-law", {
    title: "課本 1-17：三角形第三邊 $\\vec C=\\vec A-\\vec B$",
    question: "夾角 $\\theta$ 改變時，$C^2=A^2+B^2-2AB\\cos\\theta$ 如何跟著變？",
    view: [420, 260], origin: [185, 205], scale: 50,
    init: { th: 50 },
    steps: [
      { label: "$\\theta=50^\\circ$", caption: "$|\\vec A|=4$、$|\\vec B|=3$ 從同一點出發，$\\vec C=\\vec A-\\vec B$（綠）從 $\\vec B$ 的箭頭指向 $\\vec A$ 的箭頭。$\\theta$ 是邊 $C$ 的對角。", dur: 300, hold: 2800 },
      { label: "$\\theta=90^\\circ$", caption: "$\\theta=90^\\circ$：$\\cos\\theta=0$，最後一項消失，變回畢氏定理 $C^2=16+9=25$，$C=5$。", to: { th: 90 } },
      { label: "$\\theta=140^\\circ$", caption: "鈍角：$\\cos\\theta\\lt0$，$-2AB\\cos\\theta$ 變成加分，$C$ 比畢氏定理的 5 還長。", to: { th: 140 }, hold: 2600 }
    ],
    draw: function (d, s) {
      var a = [4, 0], b = [3 * Math.cos(rad(s.th)), 3 * Math.sin(rad(s.th))];
      d.poly([[0, 0], a, b], { color: "none", fill: GREEN, fillOpacity: 0.07 });
      d.arc([0, 0], 0.6, 0, s.th, { color: MUTED, width: 1.4 });
      d.label([0.9 * Math.cos(rad(s.th / 2)), 0.9 * Math.sin(rad(s.th / 2))], "\\theta", { size: 13, color: MUTED });
      d.arrow([0, 0], a, { color: RED, width: 3 });
      d.arrow([0, 0], b, { color: BLUE, width: 3 });
      d.arrow(b, a, { color: GREEN, width: 3 });
      d.label([2, -0.3], "A=4", { color: RED, size: 13 });
      d.label([b[0] / 2 - 0.35, b[1] / 2 + 0.15], "B=3", { color: BLUE, size: 13 });
      d.label([(a[0] + b[0]) / 2 + 0.35, (a[1] + b[1]) / 2 + 0.2], "C", { color: GREEN });
    },
    formula: function (s) {
      var c2 = 25 - 24 * Math.cos(rad(s.th));
      return "\\begin{aligned}C^2&=A^2+B^2-2AB\\cos\\theta\\\\&=16+9-24\\cos" + deg(s.th) + "=" + F(c2) + "\\\\ C&=" + F(Math.sqrt(c2)) + "\\end{aligned}";
    }
  });

  /* ========== 1-8 平面 A·r = A² ========== */
  var P18 = [1.2, 0.8, 1.5];
  A.define("plane18", {
    title: "課本 1-8：所有滿足 $\\vec A\\cdot\\vec r=A^2$ 的點排成一個平面",
    question: "$Q$ 在平面上移動時，什麼量保持不變？",
    view: [430, 320], origin: [190, 260], scale: 62,
    init: { t: 0, plane: 0, q: 0, az: 30 },
    steps: [
      { label: "$\\vec A$ 與點 $P$", caption: "$\\vec A$（紅）從原點指向定點 $P$。", dur: 300, hold: 2000 },
      { label: "垂直平面", caption: "通過 $P$、與 $\\vec A$ 垂直的平面（淺紫）。", set: { plane: 1 }, to: { az: 36 } },
      { label: "動點 $Q$", caption: "$Q$ 在平面上繞一圈。$\\vec r$（藍）一直在變，但它在 $\\hat A$ 方向的影子永遠落在 $P$：$\\vec r\\cdot\\hat A=|\\vec A|$。", set: { q: 1 }, to: { t: 360, az: 44 }, dur: 6000, hold: 1500 },
      { label: "$\\overrightarrow{PQ}\\perp\\vec A$", caption: "等價說法：$\\overrightarrow{PQ}=\\vec r-\\vec A$（綠）永遠垂直 $\\vec A$，即 $\\vec A\\cdot(\\vec r-\\vec A)=0$。", to: { t: 420 }, dur: 1500, hold: 3000 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 20);
      axes3(d, 2.6, ["x_1", "x_2", "x_3"], { opacity: 0.5 });
      var ah = unit(P18), u = unit(cross(P18, [0, 0, 1])), w = cross(ah, u);
      if (s.plane) {
        var c = [add(P18, add(mul(1.6, u), mul(1.3, w))), add(P18, add(mul(-1.6, u), mul(1.3, w))), add(P18, add(mul(-1.6, u), mul(-1.3, w))), add(P18, add(mul(1.6, u), mul(-1.3, w)))];
        d.poly3(c, { color: PURPLE, width: 1, fill: PURPLE, fillOpacity: 0.12 });
      }
      d.arrow3([0, 0, 0], P18, { color: RED, width: 3 });
      d.dot3(P18, { r: 4, color: RED });
      d.label3(add(P18, [0.15, -0.35, 0.1]), "P", { color: RED });
      d.label3(mul(0.5, P18), "\\vec A", { color: RED, size: 13 });
      if (s.q) {
        var Q = add(P18, add(mul(1.1 * Math.cos(rad(s.t)), u), mul(0.9 * Math.sin(rad(s.t)), w)));
        d.arrow3([0, 0, 0], Q, { color: BLUE, width: 2.5 });
        d.arrow3(P18, Q, { color: GREEN, width: 2.5 });
        d.dot3(Q, { r: 4, color: BLUE });
        d.label3(add(Q, [0, 0.2, 0.25]), "Q", { color: BLUE });
        d.label3(mul(0.55, Q), "\\vec r", { color: BLUE, size: 13 });
      }
    },
    formula: function (s) {
      var A2 = dot(P18, P18), L = Math.sqrt(A2);
      if (!s.q) return "\\vec A=(1.2,\\ 0.8,\\ 1.5),\\quad A^2=" + F(A2) + ",\\quad |\\vec A|=" + F(L);
      var ah = unit(P18), u = unit(cross(P18, [0, 0, 1])), w = cross(ah, u);
      var Q = add(P18, add(mul(1.1 * Math.cos(rad(s.t)), u), mul(0.9 * Math.sin(rad(s.t)), w)));
      return "\\begin{aligned}\\vec r&=" + vec(Q) + "\\\\ \\vec A\\cdot\\vec r&=" + F(dot(P18, Q)) + "=A^2\\\\ \\vec r\\cdot\\hat A&=" + F(dot(Q, ah)) + "=|\\vec A|\\end{aligned}";
    }
  });

  /* ========== 5.2 基底外積與右手定則 ========== */
  A.define("right-hand", {
    title: "基底的外積：$\\hat i\\to\\hat j\\to\\hat k\\to\\hat i$ 循環",
    question: "哪一個次序得到正號？反過來為什麼是負號？",
    view: [420, 300], origin: [210, 200], scale: 110,
    init: { k: 0, az: 35 },
    steps: [
      { label: "$\\hat i\\times\\hat j$", caption: "右手四指從 $\\hat i$ 彎向 $\\hat j$（紫色弧），拇指朝 $+\\hat k$：$\\hat i\\times\\hat j=\\hat k$。", set: { k: 0 }, dur: 300, hold: 2800 },
      { label: "$\\hat j\\times\\hat k$", caption: "照循環往下一個：從 $\\hat j$ 彎向 $\\hat k$，拇指朝 $+\\hat i$：$\\hat j\\times\\hat k=\\hat i$。", set: { k: 1 }, dur: 300, hold: 2800 },
      { label: "$\\hat k\\times\\hat i$", caption: "再下一個：$\\hat k\\times\\hat i=\\hat j$。三條都是「循環順序」，結果都是正的。", set: { k: 2 }, dur: 300, hold: 2800 },
      { label: "$\\hat j\\times\\hat i$", caption: "逆著循環：從 $\\hat j$ 彎向 $\\hat i$，拇指朝下：$\\hat j\\times\\hat i=-\\hat k$。這就是 $\\vec B\\times\\vec A=-\\vec A\\times\\vec B$。", set: { k: 3 }, dur: 300, hold: 3200 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 22);
      var E = [[1, 0, 0], [0, 1, 0], [0, 0, 1]], nm = ["\\hat i", "\\hat j", "\\hat k"];
      var pairs = [[0, 1, 2, 1], [1, 2, 0, 1], [2, 0, 1, 1], [1, 0, 2, -1]][s.k];
      E.forEach(function (e, i) {
        var hl = i === pairs[0] || i === pairs[1];
        d.arrow3([0, 0, 0], e, { color: hl ? (i === pairs[0] ? RED : BLUE) : MUTED, width: hl ? 3 : 1.5, opacity: hl ? 1 : 0.6 });
        d.label3(mul(1.15, e), nm[i], { color: hl ? (i === pairs[0] ? RED : BLUE) : MUTED });
      });
      arc3(d, [0, 0, 0], E[pairs[0]], E[pairs[1]], 0.45, { color: PURPLE, width: 2.5 });
      var res = mul(pairs[3] * 0.85, E[pairs[2]]);
      d.arrow3([0, 0, 0], res, { color: GREEN, width: 4 });
      d.label3(add(mul(1.15, res), [0.05, 0.05, 0.05]), (pairs[3] < 0 ? "-" : "") + nm[pairs[2]], { color: GREEN });
    },
    formula: function (s) {
      return ["\\hat i\\times\\hat j=\\hat k", "\\hat j\\times\\hat k=\\hat i", "\\hat k\\times\\hat i=\\hat j", "\\hat j\\times\\hat i=-\\hat k"][s.k];
    }
  });

  /* ========== 1-11 平行六面體體積 ========== */
  var T_A = [2, 0, 0], T_B = [0.8, 1.8, 0];
  A.define("triple", {
    title: "課本 1-11：$(\\vec A\\times\\vec B)\\cdot\\vec C$ = 底面積 × 高 = 體積",
    question: "為什麼三重積是體積？把 $\\vec C$ 平行於底面推動，體積會變嗎？",
    view: [430, 320], origin: [215, 245], scale: 56,
    init: { base: 0, n: 0, h: 0, box: 0, sh: 0, az: 35 },
    steps: [
      { label: "三個向量", caption: "$\\vec A$（紅）、$\\vec B$（藍）在地面上，$\\vec C$（綠）斜向上。", dur: 300, hold: 2200 },
      { label: "底面積", caption: "底面是 $\\vec A,\\vec B$ 張成的平行四邊形，面積 $|\\vec A\\times\\vec B|$。", set: { base: 1 }, to: { az: 40 } },
      { label: "法向量", caption: "$\\vec A\\times\\vec B$（紫）垂直底面，指向上方。", set: { n: 1 } },
      { label: "高", caption: "高 $h$ 是 $\\vec C$ 在法向量方向的分量（橘色虛線），不是 $|\\vec C|$。", set: { h: 1 }, to: { az: 46 } },
      { label: "體積", caption: "體積 $=$ 底面積 $\\times h=|\\vec A\\times\\vec B|\\cdot\\dfrac{(\\vec A\\times\\vec B)\\cdot\\vec C}{|\\vec A\\times\\vec B|}=(\\vec A\\times\\vec B)\\cdot\\vec C$。", set: { box: 1 } },
      { label: "推動 $\\vec C$", caption: "把 $\\vec C$ 的頂端平行底面推動：形狀變斜，但高不變，所以三重積（體積）不變。", to: { sh: 1.2, az: 52 }, dur: 3200, hold: 2600 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 20);
      var C = [0.6 + s.sh, 0.5, 1.6], A_ = T_A, B_ = T_B, AB = add(A_, B_);
      if (s.base) d.poly3([[0, 0, 0], A_, AB, B_], { color: BLUE, width: 1, fill: BLUE, fillOpacity: 0.15 });
      if (s.box) {
        var top = [C, add(C, A_), add(C, AB), add(C, B_)];
        d.poly3(top, { color: MUTED, width: 1, fill: GREEN, fillOpacity: 0.08 });
        [[0, 0, 0], A_, AB, B_].forEach(function (p, i) { d.line3(p, top[i], { color: MUTED, width: 1.2 }); });
      }
      d.arrow3([0, 0, 0], A_, { color: RED, width: 3 });
      d.arrow3([0, 0, 0], B_, { color: BLUE, width: 3 });
      d.arrow3([0, 0, 0], C, { color: GREEN, width: 3 });
      d.label3([1.1, -0.35, 0], "\\vec A", { color: RED });
      d.label3([0.2, 1.1, -0.1], "\\vec B", { color: BLUE });
      d.label3(add(mul(0.55, C), [-0.15, -0.2, 0.15]), "\\vec C", { color: GREEN });
      if (s.n) { d.arrow3([0, 0, 0], [0, 0, 1.15], { color: PURPLE, width: 2.5 }); d.label3([-0.1, -0.35, 1.2], "\\vec A\\times\\vec B", { color: PURPLE, size: 12 }); }
      if (s.h) { d.line3(C, [C[0], C[1], 0], { color: ORANGE, width: 2.2, dash: "5 4" }); d.label3([C[0] + 0.2, C[1] + 0.15, 0.8], "h", { color: ORANGE }); }
    },
    formula: function (s) {
      var C = [0.6 + s.sh, 0.5, 1.6], n = cross(T_A, T_B);
      switch (s._step) {
        case 0: return "\\vec A=(2,0,0),\\ \\vec B=(0.8,1.8,0),\\ \\vec C=" + vec(C, 1);
        case 1: case 2: return "\\vec A\\times\\vec B=(0,0,3.6),\\quad |\\vec A\\times\\vec B|=3.6";
        case 3: return "h=\\vec C\\cdot\\hat n=" + F(C[2]);
        default: return "\\begin{gathered}V=(\\vec A\\times\\vec B)\\cdot\\vec C=" + F(dot(n, C)) + "\\\\ =\\begin{vmatrix}2&0&0\\\\0.8&1.8&0\\\\" + F(C[0]) + "&0.5&1.6\\end{vmatrix}\\end{gathered}";
      }
    }
  });

  /* ========== 1-12 平面 ABC：法向量、距離、面積（影片也使用） ========== */
  var PA = [1, 0, 0], PB = [0, 2, 0], PC = [0, 0, 3], PN = cross(sub(PB, PA), sub(PC, PA)); // (6,3,2)
  A.define("plane-abc", {
    title: "課本 1-12：原點到平面 $ABC$ 的距離與三角形面積",
    question: "距離和面積各要用內積還是外積？",
    view: [430, 340], origin: [205, 255], scale: 58,
    init: { vecs: 1, tri: 0, edges: 0, normal: 0, foot: 0, proj: 0, az: 32, el: 20 },
    steps: [
      { label: "三個點", caption: "取 $\\vec a=(1,0,0)$、$\\vec b=(0,2,0)$、$\\vec c=(0,0,3)$ 當具體例子，從原點指向 $A,B,C$。", dur: 300, hold: 2400 },
      { label: "三角形", caption: "三點決定一個平面，三角形 $ABC$（淺藍）就在這個平面上。", set: { tri: 1 }, to: { az: 38 } },
      { label: "兩條邊", caption: "平面內的兩條邊：$\\overrightarrow{AB}=\\vec b-\\vec a$、$\\overrightarrow{AC}=\\vec c-\\vec a$（橘）。", set: { edges: 1 } },
      { label: "法向量", caption: "兩條邊的外積同時垂直它們，就是平面的法向量 $\\vec n=(6,3,2)$（紫）。面積 $=\\tfrac12|\\vec n|=3.5$。", set: { normal: 1 }, to: { az: 46 } },
      { label: "距離", caption: "原點到平面的最短路徑沿法向量方向（虛線），它的長度就是 $\\vec a$ 在 $\\hat n$ 方向的影子：$d=\\frac{\\vec a\\cdot\\vec n}{|\\vec n|}=\\frac67$。", set: { foot: 1, proj: 1 }, to: { az: 54 }, hold: 3000 }
    ],
    draw: function (d, s) {
      d.camera(s.az, s.el);
      axes3(d, 3.3, ["x_1", "x_2", "x_3"], { opacity: 0.45 });
      if (s.tri) d.poly3([PA, PB, PC], { color: BLUE, width: 1.4, fill: BLUE, fillOpacity: 0.14 });
      if (s.vecs) {
        [[PA, "\\vec a", RED], [PB, "\\vec b", RED], [PC, "\\vec c", RED]].forEach(function (v) {
          d.arrow3([0, 0, 0], v[0], { color: v[2], width: 2.2, opacity: 0.85 });
        });
        d.label3([0.55, -0.3, -0.1], "\\vec a", { color: RED, size: 13 });
        d.label3([-0.15, 1.1, -0.25], "\\vec b", { color: RED, size: 13 });
        d.label3([-0.2, -0.15, 1.6], "\\vec c", { color: RED, size: 13 });
      }
      [[PA, "A"], [PB, "B"], [PC, "C"]].forEach(function (p) { d.dot3(p[0], { r: 4 }); d.label3(add(p[0], [0.15, 0.15, 0.15]), p[1], {}); });
      if (s.edges) {
        d.arrow3(PA, PB, { color: ORANGE, width: 2.5 }); d.arrow3(PA, PC, { color: ORANGE, width: 2.5 });
        d.label3(add(mul(0.5, add(PA, PB)), [0.2, 0.1, -0.25]), "\\vec b-\\vec a", { color: ORANGE, size: 12 });
        d.label3(add(mul(0.5, add(PA, PC)), [0.15, -0.2, 0.1]), "\\vec c-\\vec a", { color: ORANGE, size: 12 });
      }
      var nh = unit(PN), G = mul(1 / 3, add(PA, add(PB, PC)));
      if (s.normal) { d.arrow3(G, add(G, mul(1.1, nh)), { color: PURPLE, width: 3 }); d.label3(add(G, mul(1.3, nh)), "\\vec n", { color: PURPLE }); }
      if (s.foot) {
        var dd = dot(PA, PN) / len(PN), Fp = mul(dd, nh);
        d.line3([0, 0, 0], Fp, { color: GREEN, width: 3.5 });
        d.line3(PA, Fp, { color: MUTED, width: 1.2, dash: "4 3" });
        d.dot3(Fp, { r: 4, color: GREEN });
        d.label3(add(mul(0.5, Fp), [0, -0.3, 0.2]), "d", { color: GREEN });
      }
    },
    formula: function (s) {
      switch (s._step) {
        case 0: return "\\vec a=(1,0,0),\\ \\vec b=(0,2,0),\\ \\vec c=(0,0,3)";
        case 1: return "\\text{平面：}\\ x_1+\\tfrac{x_2}{2}+\\tfrac{x_3}{3}=1";
        case 2: return "\\begin{gathered}\\vec b-\\vec a=(-1,2,0)\\\\ \\vec c-\\vec a=(-1,0,3)\\end{gathered}";
        case 3: return "\\begin{gathered}\\vec n=(\\vec b-\\vec a)\\times(\\vec c-\\vec a)=(6,3,2)\\\\ |\\vec n|=7,\\quad S=\\tfrac12|\\vec n|=3.5\\end{gathered}";
        default: return "d=\\frac{\\vec a\\cdot\\vec n}{|\\vec n|}=\\frac{6}{7}\\approx0.857";
      }
    }
  });

  /* ========== 1-13 由 A×X=B、A·X=φ 解 X（影片也使用） ========== */
  var SX_A = [0, 0, 1.6], SX_X = [1.2, 0.6, 1.0];
  A.define("solve-x", {
    title: "課本 1-13：$\\vec X$ 拆成「平行 $\\vec A$」和「垂直 $\\vec A$」兩部分",
    question: "兩個條件各決定 $\\vec X$ 的哪一部分？",
    view: [430, 330], origin: [200, 255], scale: 78,
    init: { x: 1, par: 0, perp: 0, b: 0, aax: 0, rec: 0, az: 30, el: 20 },
    steps: [
      { label: "$\\vec A$ 與未知的 $\\vec X$", caption: "$\\vec A$（紅）已知；$\\vec X$（灰）是要找的向量。", dur: 300, hold: 2200 },
      { label: "拆成兩部分", caption: "任何 $\\vec X$ 都能拆成平行 $\\vec A$ 的 $\\vec X_\\parallel$（綠）和垂直 $\\vec A$ 的 $\\vec X_\\perp$（藍）。", set: { par: 1, perp: 1 }, to: { az: 36 } },
      { label: "$\\vec A\\cdot\\vec X=\\phi$", caption: "內積只看平行部分：$\\vec A\\cdot\\vec X=\\vec A\\cdot\\vec X_\\parallel=\\phi$，所以 $\\vec X_\\parallel=\\dfrac{\\phi}{A^2}\\vec A$。", dur: 300, hold: 3200 },
      { label: "$\\vec A\\times\\vec X=\\vec B$", caption: "外積只看垂直部分：$\\vec B=\\vec A\\times\\vec X_\\perp$（紫），它同時垂直 $\\vec A$ 和 $\\vec X_\\perp$。", set: { b: 1 }, to: { az: 44 } },
      { label: "BAC–CAB", caption: "再叉一次：$\\vec A\\times\\vec B=\\vec A\\times(\\vec A\\times\\vec X)=\\phi\\vec A-A^2\\vec X$。橘色是 $\\vec A\\times(\\vec A\\times\\vec X)=-A^2\\vec X_\\perp$，與 $\\vec X_\\perp$ 反向。", set: { aax: 1 }, to: { az: 50 } },
      { label: "還原 $\\vec X$", caption: "$\\vec X=\\dfrac{\\phi\\vec A-\\vec A\\times\\vec B}{A^2}$：平行部分加垂直部分，剛好回到原本的 $\\vec X$。", set: { rec: 1 }, to: { az: 56 }, hold: 3000 }
    ],
    draw: function (d, s) {
      d.camera(s.az, s.el);
      axes3(d, 2.0, ["x", "y", "z"], { opacity: 0.4 });
      var Xp = [0, 0, SX_X[2]], Xq = [SX_X[0], SX_X[1], 0], B = cross(SX_A, SX_X);
      d.arrow3([0, 0, 0], SX_A, { color: RED, width: 3 });
      d.label3([-0.15, -0.15, 1.75], "\\vec A", { color: RED });
      if (s.x) { d.arrow3([0, 0, 0], SX_X, { color: s.rec ? INK : MUTED, width: s.rec ? 3.2 : 2.5 }); d.label3(add(SX_X, [0.1, 0.1, 0.15]), "\\vec X", { color: s.rec ? INK : MUTED }); }
      if (s.par) { d.arrow3([0.06, 0, 0], add(Xp, [0.06, 0, 0]), { color: GREEN, width: 4 }); d.label3([0.3, -0.25, 0.55], "\\vec X_{\\parallel}", { color: GREEN, size: 13 }); }
      if (s.perp) {
        d.arrow3([0, 0, 0], Xq, { color: BLUE, width: 3 }); d.label3(add(mul(0.6, Xq), [0.1, 0.15, -0.2]), "\\vec X_{\\perp}", { color: BLUE, size: 13 });
        d.line3(Xq, SX_X, { color: MUTED, width: 1, dash: "3 3" }); d.line3(Xp, SX_X, { color: MUTED, width: 1, dash: "3 3" });
      }
      if (s.b) { d.arrow3([0, 0, 0], mul(0.55, B), { color: PURPLE, width: 3 }); d.label3(add(mul(0.62, B), [0, 0, 0.15]), "\\vec B", { color: PURPLE }); }
      if (s.aax) { var V = mul(-2.56 * 0.45, Xq); d.arrow3([0, 0, 0], V, { color: ORANGE, width: 3 }); d.label3(add(V, [-0.1, -0.1, -0.2]), "\\vec A\\times(\\vec A\\times\\vec X)", { color: ORANGE, size: 12 }); }
    },
    formula: function (s) {
      switch (s._step) {
        case 0: return "\\vec A=(0,0,1.6)\\quad(\\text{例子})";
        case 1: return "\\vec X=\\vec X_\\parallel+\\vec X_\\perp=(0,0,1)+(1.2,0.6,0)";
        case 2: return "\\begin{aligned}\\phi&=\\vec A\\cdot\\vec X=1.6\\\\ \\vec X_\\parallel&=\\frac{\\phi}{A^2}\\vec A=\\frac{1.6}{2.56}(0,0,1.6)=(0,0,1)\\end{aligned}";
        case 3: return "\\vec B=\\vec A\\times\\vec X=(-0.96,\\ 1.92,\\ 0)";
        case 4: return "\\begin{gathered}\\vec A\\times\\vec B=\\phi\\vec A-A^2\\vec X\\\\ \\vec A\\times\\vec B=(-3.072,\\,-1.536,\\,0)\\end{gathered}";
        default: return "\\begin{aligned}\\vec X&=\\frac{\\phi\\vec A-\\vec A\\times\\vec B}{A^2}\\\\&=\\tfrac{1}{2.56}(3.072,\\,1.536,\\,2.56)\\\\&=(1.2,\\,0.6,\\,1)\\end{aligned}";
      }
    }
  });

  /* ========== 6.1 弧長 s = Rθ ========== */
  A.define("arc-length", {
    title: "弧長 $s=R\\theta$（$\\theta$ 用弧度）與 $v=R\\omega$",
    question: "1 弧度是多大？為什麼 $v=R\\omega$？",
    view: [420, 290], origin: [200, 150], scale: 55,
    init: { th: 0 },
    steps: [
      { label: "半徑 $R=2$", caption: "半徑 $R=2$ 的圓，粒子從 $+x$ 軸出發逆時針轉。", dur: 300, hold: 1800 },
      { label: "$\\theta=1$ rad", caption: "轉到 $\\theta=1$ 弧度（約 $57.3^\\circ$）時，走過的弧長剛好等於半徑：$s=R\\cdot1=2$。這就是弧度的定義。", to: { th: 1 } },
      { label: "$\\theta=2.5$ rad", caption: "$\\theta=2.5$：$s=R\\theta=5$。弧長和角度成正比，比例常數就是 $R$。", to: { th: 2.5 } },
      { label: "速率", caption: "若每秒轉 $\\omega$ 弧度，每秒走的弧長就是 $R\\omega$：$v=\\frac{\\mathrm ds}{\\mathrm dt}=R\\frac{\\mathrm d\\theta}{\\mathrm dt}=R\\omega$。", to: { th: 4 }, dur: 3000, hold: 2400 }
    ],
    draw: function (d, s) {
      d.circle([0, 0], 2 * 55, { color: MUTED, width: 1.2, dash: "3 4" });
      var pts = [];
      for (var i = 0; i <= 60; i++) { var t = s.th * i / 60; pts.push([2 * Math.cos(t), 2 * Math.sin(t)]); }
      if (s.th > 0.01) d.path(pts, { color: GREEN, width: 5 });
      var P = [2 * Math.cos(s.th), 2 * Math.sin(s.th)];
      d.line([0, 0], [2, 0], { color: MUTED, width: 1.5 });
      d.line([0, 0], P, { color: RED, width: 2 });
      d.label([1, -0.25], "R", { color: MUTED, size: 13 });
      if (s.th > 0.15) { d.arc([0, 0], 0.5, 0, s.th * 180 / Math.PI, { color: INK, width: 1.4 }); d.label([0.8 * Math.cos(s.th / 2), 0.8 * Math.sin(s.th / 2)], "\\theta", { size: 13 }); }
      d.dot(P, { r: 6, color: RED });
      if (s._step === 3) d.arrow(P, add(P, mul(0.6, [-Math.sin(s.th), Math.cos(s.th)])), { color: BLUE, width: 3 });
      if (s.th > 0.3) d.label([2.45 * Math.cos(s.th / 2), 2.45 * Math.sin(s.th / 2)], "s", { color: GREEN });
    },
    formula: function (s) {
      return "\\theta=" + F(s.th) + "\\ \\text{rad}=" + deg(s.th * 180 / Math.PI) + ",\\quad s=R\\theta=2\\times" + F(s.th) + "=" + F(2 * s.th);
    }
  });

  /* ========== 7 長度固定 → 導數垂直 ========== */
  A.define("const-length", {
    title: "長度固定的向量，導數與它垂直",
    question: "$\\vec A$ 長度不變時，$\\dot{\\vec A}$ 指向哪裡？長度在變時呢？",
    view: [420, 300], origin: [210, 150], scale: 45,
    init: { t: 0, grow: 0 },
    steps: [
      { label: "長度固定", caption: "$|\\vec A|=2$ 固定，$\\vec A$ 只轉方向。導數 $\\dot{\\vec A}$（藍）永遠與 $\\vec A$ 垂直：$\\vec A\\cdot\\dot{\\vec A}=0$。", to: { t: 360 }, dur: 5000, hold: 1500 },
      { label: "長度在變", caption: "讓長度也變大（螺線）：$\\dot{\\vec A}$ 多了沿 $\\vec A$ 方向的分量，$\\vec A\\cdot\\dot{\\vec A}=\\tfrac12\\frac{\\mathrm d}{\\mathrm dt}|\\vec A|^2\\neq0$，不再垂直。", set: { grow: 1 }, to: { t: 300 }, dur: 5000, hold: 2400 }
    ],
    draw: function (d, s) {
      var t = rad(s.t), L = s.grow ? 1.2 + 0.4 * t / (2 * Math.PI) * 2 : 2, Ld = s.grow ? 0.4 / Math.PI : 0;
      var a = [L * Math.cos(t), L * Math.sin(t)], ad = [Ld * Math.cos(t) - L * Math.sin(t), Ld * Math.sin(t) + L * Math.cos(t)];
      var pts = [];
      for (var i = 0; i <= 80; i++) {
        var tt = (s.grow ? s.t : 360) * i / 80 * Math.PI / 180, LL = s.grow ? 1.2 + 0.4 * tt / Math.PI : 2;
        pts.push([LL * Math.cos(tt), LL * Math.sin(tt)]);
      }
      d.path(pts, { color: MUTED, width: 1.2, dash: "3 4" });
      d.arrow([0, 0], a, { color: RED, width: 3 });
      d.arrow(a, add(a, mul(0.55, ad)), { color: BLUE, width: 3 });
      if (!s.grow) d.rightAngle(a, mul(-1 / L, a), unit(ad), 0.22);
      d.label(mul(0.5, a), "\\vec A", { color: RED, dy: -12 });
      d.label(add(a, mul(0.7, ad)), "\\dot{\\vec A}", { color: BLUE });
    },
    formula: function (s) {
      var t = rad(s.t), L = s.grow ? 1.2 + 0.4 * t / Math.PI : 2, Ld = s.grow ? 0.4 / Math.PI : 0;
      return "|\\vec A|=" + F(L) + ",\\qquad \\vec A\\cdot\\dot{\\vec A}=|\\vec A|\\frac{\\mathrm d|\\vec A|}{\\mathrm dt}=" + F(L * Ld, 3);
    }
  });

  /* ========== 8 矩陣尺寸 ========== */
  function grid(d, x0, y0, rows, cols, c, o) {
    o = o || {};
    for (var r = 0; r < rows; r++) for (var k = 0; k < cols; k++) d.rect(x0 + k * c, -(y0 + r * c), x0 + (k + 1) * c - 3, -(y0 + (r + 1) * c - 3), { color: o.color || MUTED, width: 1.2, fill: o.fill || "none", fillOpacity: o.fo || 0.15 });
  }
  A.define("matrix-dims", {
    title: "矩陣相乘的尺寸：內側要相等，結果取外側",
    question: "$(3\\times3)(3\\times2)$ 能乘嗎？$(3\\times2)(3\\times3)$ 呢？",
    view: [440, 200], origin: [0, 0], scale: 1,
    init: { which: 0 },
    steps: [
      { label: "$AB$", caption: "$A$ 是 $3\\times3$、$B$ 是 $3\\times2$：$A$ 每個 row 有 3 個數，$B$ 每個 column 也有 3 個數，對得齊，可以乘。", set: { which: 0 }, dur: 300, hold: 3000 },
      { label: "結果尺寸", caption: "結果的 row 數跟 $A$（3）、column 數跟 $B$（2）：$AB$ 是 $3\\times2$。", set: { which: 1 }, dur: 300, hold: 3000 },
      { label: "$BA$", caption: "反過來 $B$ 的 row 只有 2 個數，$A$ 的 column 有 3 個數，對不齊：$BA$ 不能乘。", set: { which: 2 }, dur: 300, hold: 3200 }
    ],
    draw: function (d, s) {
      var c = 30, y0 = 40;
      if (s.which < 2) {
        grid(d, 20, y0, 3, 3, c, { color: RED, fill: RED, fo: s.which === 0 ? 0.12 : 0.05 });
        grid(d, 140, y0, 3, 2, c, { color: BLUE, fill: BLUE, fo: s.which === 0 ? 0.12 : 0.05 });
        d.label([65, -22], "A:\\ 3\\times\\underline{3}", { color: RED, size: 14 });
        d.label([170, -22], "B:\\ \\underline{3}\\times2", { color: BLUE, size: 14 });
        if (s.which === 1) { d.label([238, -(y0 + 45)], "=", {}); grid(d, 262, y0, 3, 2, c, { color: GREEN, fill: GREEN, fo: 0.2 }); d.label([292, -22], "AB:\\ 3\\times2", { color: GREEN, size: 14 }); }
        if (s.which === 0) d.label([320, -(y0 + 45)], "3=3\\ \\checkmark", { color: GREEN, size: 15 });
      } else {
        grid(d, 20, y0, 3, 2, c, { color: BLUE, fill: BLUE, fo: 0.12 });
        grid(d, 110, y0, 3, 3, c, { color: RED, fill: RED, fo: 0.12 });
        d.label([50, -22], "B:\\ 3\\times\\underline{2}", { color: BLUE, size: 14 });
        d.label([155, -22], "A:\\ \\underline{3}\\times3", { color: RED, size: 14 });
        d.label([320, -(y0 + 45)], "2\\neq3\\ \\text{不能乘}", { color: ORANGE, size: 15 });
      }
    },
    formula: function (s) {
      return ["(3\\times\\mathbf 3)(\\mathbf 3\\times2)\\ \\Rightarrow\\ \\text{可乘}", "(\\mathbf 3\\times3)(3\\times\\mathbf 2)=\\mathbf 3\\times\\mathbf 2", "(3\\times\\mathbf 2)(\\mathbf 3\\times3)\\ \\Rightarrow\\ 2\\neq3,\\ \\text{不能乘}"][s.which];
    }
  });

  /* ========== 9.3 繞 y 軸：從 y 軸上方往下看 (z, x) 平面 ========== */
  A.define("rot-y", {
    title: "繞 $\\hat y$ 旋轉：配對是 $(z,x)$，不是 $(x,z)$",
    question: "為什麼繞 $\\hat y$ 的矩陣，負號在右上角？",
    view: [420, 300], origin: [170, 230], scale: 55,
    init: { th: 0, eq: 0 },
    steps: [
      { label: "從 $+y$ 看過去", caption: "從 $+y$ 往原點看（$\\hat y$ 指向你）：$z$ 軸朝右、$x$ 軸朝上。所以 $z$ 是二維的「第一軸」，$x$ 是「第二軸」。", dur: 300, hold: 3600 },
      { label: "轉 $\\theta$", caption: "兩軸一起逆時針轉 $\\theta$，和二維 $(x,y)$ 的旋轉完全一樣。", to: { th: 30 } },
      { label: "照二維公式寫", caption: "把二維公式的 $x\\to z$、$y\\to x$：$z'=z\\cos\\theta+x\\sin\\theta$、$x'=-z\\sin\\theta+x\\cos\\theta$。", set: { eq: 1 }, dur: 300, hold: 3600 },
      { label: "改回 $(x,z)$ 次序", caption: "排進 $3\\times3$ 矩陣時，$x'$ 那個 row 的 $z$ 位置是 $-\\sin\\theta$（右上角）、$z'$ 那個 row 的 $x$ 位置是 $+\\sin\\theta$（左下角）。", set: { eq: 2 }, dur: 300, hold: 3600 }
    ],
    draw: function (d, s) {
      var c = Math.cos(rad(s.th)), sn = Math.sin(rad(s.th));
      d.arrow([-0.5, 0], [3.6, 0], { color: MUTED, width: 1.3, head: 8 });
      d.arrow([0, -0.5], [0, 3.4], { color: MUTED, width: 1.3, head: 8 });
      d.label([3.85, 0], "z", { color: MUTED }); d.label([0, 3.65], "x", { color: MUTED });
      d.circle([0, 0], 9, { color: INK, width: 1.5 }); d.dot([0, 0], { r: 3 });
      d.label([-0.45, -0.4], "\\hat y\\ \\text{朝你}", { size: 12, color: MUTED });
      if (s.th > 0.5) {
        d.arrow([0, 0], [3.3 * c, 3.3 * sn], { color: GREEN, width: 2.2 });
        d.arrow([0, 0], [-3.1 * sn, 3.1 * c], { color: GREEN, width: 2.2 });
        d.label([3.6 * c, 3.6 * sn], "z'", { color: GREEN }); d.label([-3.4 * sn, 3.4 * c], "x'", { color: GREEN });
        d.arc([0, 0], 1, 0, s.th, { color: GREEN, width: 1.3 });
        d.label([1.3 * Math.cos(rad(s.th / 2)), 1.3 * Math.sin(rad(s.th / 2))], "\\theta", { color: GREEN, size: 13 });
      }
    },
    formula: function (s) {
      if (s.eq === 0) return "\\begin{bmatrix}z'\\\\x'\\end{bmatrix}=\\begin{bmatrix}\\cos\\theta&\\sin\\theta\\\\-\\sin\\theta&\\cos\\theta\\end{bmatrix}\\begin{bmatrix}z\\\\x\\end{bmatrix}";
      if (s.eq === 1) return "\\begin{aligned}z'&=z\\cos\\theta+x\\sin\\theta\\\\ x'&=-z\\sin\\theta+x\\cos\\theta\\end{aligned}";
      return "\\begin{bmatrix}x'\\\\y'\\\\z'\\end{bmatrix}=\\begin{bmatrix}\\cos\\theta&0&-\\sin\\theta\\\\0&1&0\\\\\\sin\\theta&0&\\cos\\theta\\end{bmatrix}\\begin{bmatrix}x\\\\y\\\\z\\end{bmatrix}";
    }
  });

  /* ========== 9 被動 vs 主動旋轉 ========== */
  A.define("passive-active", {
    title: "被動旋轉（軸轉）vs. 主動旋轉（點轉）",
    question: "兩種旋轉算出的座標為什麼不同？",
    view: [440, 250], origin: [0, 0], scale: 40,
    init: { th: 0, act: 0 },
    steps: [
      { label: "被動：軸轉、點不動", caption: "左圖：座標軸逆時針轉 $30^\\circ$（綠），點 $P=(3,1)$ 不動。從新軸看，點好像順時針轉了。", to: { th: 30 }, dur: 2400, hold: 2400 },
      { label: "主動：點轉、軸不動", caption: "右圖：軸不動，點逆時針轉 $30^\\circ$ 到 $P'$。", set: { act: 1 }, dur: 300, hold: 3000 },
      { label: "比較", caption: "兩個矩陣只差 $\\sin\\theta$ 的正負號（互為轉置）。講義第九節用的是<strong>被動</strong>：$\\begin{bmatrix}\\cos\\theta&\\sin\\theta\\\\-\\sin\\theta&\\cos\\theta\\end{bmatrix}$。", dur: 300, hold: 3600 }
    ],
    draw: function (d, s) {
      var O1 = [1.6, -5.2], O2 = [6.9, -5.2], c = Math.cos(rad(s.th)), sn = Math.sin(rad(s.th));
      function at(O, p) { return [O[0] + p[0], O[1] + p[1]]; }
      [O1, O2].forEach(function (O) {
        d.arrow(at(O, [-0.6, 0]), at(O, [3.9, 0]), { color: MUTED, width: 1.1, head: 7 });
        d.arrow(at(O, [0, -0.6]), at(O, [0, 2.9]), { color: MUTED, width: 1.1, head: 7 });
      });
      d.label([3.7, -0.6], "\\text{被動（講義）}", { size: 13 });
      d.label([8.9, -0.6], "\\text{主動}", { size: 13 });
      // 被動：軸轉
      d.arrow(O1, at(O1, [3.6 * c, 3.6 * sn]), { color: GREEN, width: 2 });
      d.arrow(O1, at(O1, [-2.8 * sn, 2.8 * c]), { color: GREEN, width: 2 });
      d.label(at(O1, [3.9 * c, 3.9 * sn]), "x'", { color: GREEN, size: 13 });
      d.label(at(O1, [-3.05 * sn, 3.05 * c]), "y'", { color: GREEN, size: 13 });
      d.dot(at(O1, [3, 1]), { r: 5, color: RED }); d.label(at(O1, [3.3, 1.3]), "P", { color: RED, size: 13 });
      // 主動：點轉
      d.dot(at(O2, [3, 1]), { r: 4, color: MUTED });
      if (s.act) {
        var Pp = [3 * Math.cos(rad(30)) - Math.sin(rad(30)), 3 * Math.sin(rad(30)) + Math.cos(rad(30))];
        var pts = []; for (var i = 0; i <= 20; i++) { var t = rad(18.43 + 30 * i / 20); pts.push(at(O2, [Math.sqrt(10) * Math.cos(t), Math.sqrt(10) * Math.sin(t)])); }
        d.path(pts, { color: RED, width: 1.3, dash: "3 3" });
        d.dot(at(O2, Pp), { r: 5, color: RED }); d.label(at(O2, [Pp[0] + 0.3, Pp[1] + 0.3]), "P'", { color: RED, size: 13 });
      }
    },
    formula: function (s) {
      var c = Math.cos(rad(s.th)), sn = Math.sin(rad(s.th));
      var pas = "\\text{被動}&:\\ x'=3\\cos\\theta+\\sin\\theta=" + F(3 * c + sn) + "\\\\ &\\phantom{:}\\ y'=-3\\sin\\theta+\\cos\\theta=" + F(-3 * sn + c);
      if (!s.act) return "\\begin{aligned}" + pas + "\\end{aligned}";
      return "\\begin{aligned}" + pas + "\\\\[4pt] \\text{主動}&:\\ x=3\\cos\\theta-\\sin\\theta=2.1\\\\ &\\phantom{:}\\ y=3\\sin\\theta+\\cos\\theta=2.37\\end{aligned}";
    }
  });

  /* ========== 1-1 x3 繞 x2 朝 x1 轉 45° ========== */
  A.define("rot11", {
    title: "課本 1-1：$x_3$ 軸繞 $x_2$ 軸、朝 $x_1$ 傾斜 $45^\\circ$",
    question: "新的三個軸用舊座標寫出來是什麼？",
    view: [430, 320], origin: [200, 240], scale: 80,
    init: { phi: 0, comp3: 0, comp1: 0, az: 30 },
    steps: [
      { label: "原座標", caption: "灰色是原座標軸。轉軸是 $x_2$（不動）。", dur: 300, hold: 1800 },
      { label: "轉 $45^\\circ$", caption: "$x_3$ 朝 $x_1$ 傾斜 $45^\\circ$；整組軸是剛體一起轉，所以 $x_1$ 同時往 $-x_3$ 方向傾斜。", to: { phi: 45, az: 38 } },
      { label: "$\\hat x_3'$ 的分量", caption: "$\\hat x_3'$ 往舊軸投影：沿 $x_1$ 是 $\\sin45^\\circ$、沿 $x_3$ 是 $\\cos45^\\circ$，所以 $\\hat x_3'=(\\tfrac1{\\sqrt2},0,\\tfrac1{\\sqrt2})$。", set: { comp3: 1 }, to: { az: 44 } },
      { label: "$\\hat x_1'$ 的分量", caption: "$\\hat x_1'=(\\tfrac1{\\sqrt2},0,-\\tfrac1{\\sqrt2})$。三個新軸當作三個 row，就是變換矩陣 $\\lambda$。", set: { comp1: 1 }, to: { az: 50 }, hold: 3000 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 20);
      axes3(d, 1.45, ["x_1", "x_2", "x_3"], { opacity: 0.6 });
      var c = Math.cos(rad(s.phi)), sn = Math.sin(rad(s.phi));
      var e1 = [c, 0, -sn], e3 = [sn, 0, c];
      if (s.phi > 0.5) {
        d.arrow3([0, 0, 0], mul(1.25, e1), { color: RED, width: 3 });
        d.arrow3([0, 0, 0], mul(1.25, e3), { color: GREEN, width: 3 });
        d.label3(mul(1.42, e1), "x_1'", { color: RED });
        d.label3(mul(1.4, e3), "x_3'", { color: GREEN });
        var arc = []; for (var i = 0; i <= 12; i++) { var t = rad(s.phi * i / 12); arc.push([0.55 * Math.sin(t), 0, 0.55 * Math.cos(t)]); }
        d.path3(arc, { color: GREEN, width: 1.4 });
      }
      d.arrow3([0, 0, 0], [0, 1.25, 0], { color: BLUE, width: 3 });
      d.label3([0, 1.45, 0.08], "x_2=x_2'", { color: BLUE, size: 13 });
      if (s.comp3) {
        d.line3(e3, [e3[0], 0, 0], { color: GREEN, width: 1.2, dash: "4 3" });
        d.line3(e3, [0, 0, e3[2]], { color: GREEN, width: 1.2, dash: "4 3" });
        d.label3([e3[0] / 2, 0, -0.12], "\\sin45^\\circ", { color: GREEN, size: 12 });
      }
      if (s.comp1) {
        d.line3(e1, [e1[0], 0, 0], { color: RED, width: 1.2, dash: "4 3" });
        d.line3(e1, [0, 0, e1[2]], { color: RED, width: 1.2, dash: "4 3" });
      }
    },
    formula: function (s) {
      var c = Math.cos(rad(s.phi)), sn = Math.sin(rad(s.phi));
      return "\\lambda=\\begin{bmatrix}" + F(c, 3) + "&0&" + F(-sn, 3) + "\\\\0&1&0\\\\" + F(sn, 3) + "&0&" + F(c, 3) + "\\end{bmatrix}\\quad(\\text{各 row}=\\hat x_1',\\hat x_2',\\hat x_3')";
    }
  });
})();
