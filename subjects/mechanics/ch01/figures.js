/* 力學 Lecture 1（p.1–49）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt, rad = A.rad;
  function deg(x) { return F(x, 1) + "^\\circ"; }
  function add(u, v) { return [u[0] + v[0], u[1] + v[1], (u[2] || 0) + (v[2] || 0)]; }
  function mul(k, u) { return [k * u[0], k * u[1], k * (u[2] || 0)]; }
  function dot3(u, v) { return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]; }
  function cross3(u, v) { return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]; }
  function norm3(u) { var L = Math.sqrt(dot3(u, u)); return [u[0] / L, u[1] / L, u[2] / L]; }
  /* Rodrigues：u 繞單位軸 n 逆時針轉 phi（度） */
  function rotate(u, n, phi) {
    var c = Math.cos(rad(phi)), s = Math.sin(rad(phi)), k = dot3(n, u) * (1 - c), nx = cross3(n, u);
    return [u[0] * c + nx[0] * s + n[0] * k, u[1] * c + nx[1] * s + n[1] * k, u[2] * c + nx[2] * s + n[2] * k];
  }
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)";

  /* ---------------- 1. 乘積律（p.7） ---------------- */
  A.define("product-rule", {
    title: "乘積律：長方形面積 $fg$ 多出哪幾塊",
    question: "$f$、$g$ 各增加一點點時，$fg$ 增加多少？",
    view: [420, 290], origin: [52, 262], scale: 50,
    init: { df: 0, dg: 0 },
    steps: [
      { label: "原本的面積", caption: "長 $f=4$、寬 $g=3$，面積 $fg=12$。", dur: 400, hold: 1800 },
      { label: "長增加 $\\mathrm df$", caption: "長增加 $\\mathrm df$：右邊多出一條長條，面積 $g\\,\\mathrm df$。", to: { df: 1.2 } },
      { label: "寬增加 $\\mathrm dg$", caption: "寬增加 $\\mathrm dg$：上面多出一條 $f\\,\\mathrm dg$，右上角還有一小塊 $\\mathrm df\\,\\mathrm dg$。", to: { dg: 0.9 } },
      { label: "改變量變小", caption: "把 $\\mathrm df,\\mathrm dg$ 一起縮小：兩條長條等比例縮小，角落是「小 × 小」，縮得更快，所佔比例趨近 0。所以只留下 $\\mathrm d(fg)=g\\,\\mathrm df+f\\,\\mathrm dg$。", to: { df: 0.25, dg: 0.19 }, dur: 2800, hold: 2400 }
    ],
    draw: function (d, s) {
      var f = 4, g = 3;
      d.rect(0, 0, f, g, { color: MUTED, width: 1.5, fill: "var(--soft)" });
      if (s.df > 0.001) d.rect(f, 0, f + s.df, g, { color: BLUE, width: 1.5, fill: BLUE, fillOpacity: 0.25 });
      if (s.dg > 0.001) d.rect(0, g, f, g + s.dg, { color: RED, width: 1.5, fill: RED, fillOpacity: 0.25 });
      if (s.df > 0.001 && s.dg > 0.001) d.rect(f, g, f + s.df, g + s.dg, { color: PURPLE, width: 1.5, fill: PURPLE, fillOpacity: 0.45 });
      d.label([f / 2, -0.32], "f=4");
      d.label([-0.42, g / 2], "g=3");
      d.label([f / 2, g / 2], "fg");
      if (s.df > 0.15) d.label([f + s.df / 2, -0.32], "\\mathrm df", { color: BLUE });
      if (s.df > 0.5) d.label([f + s.df / 2, g / 2], "g\\,\\mathrm df", { color: BLUE, size: 13 });
      if (s.dg > 0.15) d.label([-0.42, g + s.dg / 2], "\\mathrm dg", { color: RED });
      if (s.dg > 0.4) d.label([f / 2, g + s.dg / 2], "f\\,\\mathrm dg", { color: RED, size: 13 });
    },
    formula: function (s) {
      var gdf = 3 * s.df, fdg = 4 * s.dg, c = s.df * s.dg, tot = gdf + fdg + c;
      if (tot < 1e-6) return "fg=4\\times3=12";
      return "\\begin{aligned}\\Delta(fg)&=g\\,\\mathrm df+f\\,\\mathrm dg+\\mathrm df\\,\\mathrm dg\\\\&=" + F(gdf) + "+" + F(fdg) + "+" + F(c, 3) +
        "\\\\&\\text{角落佔 }" + F(c / tot * 100, 1) + "\\%\\end{aligned}";
    }
  });

  /* ---------------- 2. 純量與向量（p.13） ---------------- */
  var PARTICLES = [[1, 3, 7], [2, 3, 4], [3, 3, 9], [1, 2, 3], [2, 2, 6], [3, 2, 5], [1, 1, 2], [2, 1, 8], [3, 1, 1]];
  A.define("scalar-vector", {
    title: "轉動座標軸：什麼變、什麼不變",
    question: "粒子不動，只換座標軸，第 4 號粒子的質量與位置分量如何？",
    view: [420, 330], origin: [190, 290], scale: 48,
    init: { phi: 0 },
    steps: [
      { label: "原座標", caption: "在 $(x,y)$ 座標中，第 4 號粒子在 $(2,3)$，質量 $M_4$。紅色箭頭是位置向量 $\\vec P_4$。", dur: 400, hold: 2200 },
      { label: "軸轉 $30^\\circ$", caption: "把座標軸逆時針轉 $30^\\circ$。粒子、箭頭都沒動，但量出來的分量 $(x',y')$ 變了。", to: { phi: 30 } },
      { label: "軸轉 $60^\\circ$", caption: "再轉到 $60^\\circ$：分量繼續改變；箭頭長度 $|\\vec P_4|$ 和質量 $M_4$ 始終不變。", to: { phi: 60 } },
      { label: "結論", caption: "質量、長度是<strong>純量</strong>：換座標不變。位置的<strong>分量</strong>會隨座標改變，但向量（箭頭）本身沒變。", dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var c = Math.cos(rad(s.phi)), sn = Math.sin(rad(s.phi));
      var u = [c, sn], w = [-sn, c];
      for (var k = 0; k <= 4; k++) {
        d.line(mul(k, w), add(mul(k, w), mul(4.2, u)), { color: "var(--grid)", width: 1 });
        d.line(mul(k, u), add(mul(k, u), mul(4.2, w)), { color: "var(--grid)", width: 1 });
      }
      if (s.phi > 0.5) {
        d.line([0, 0], [4.2, 0], { color: MUTED, width: 1, dash: "4 4", opacity: 0.6 });
        d.line([0, 0], [0, 4.2], { color: MUTED, width: 1, dash: "4 4", opacity: 0.6 });
      }
      d.arrow([0, 0], mul(4.4, u), { color: GREEN, width: 2 });
      d.arrow([0, 0], mul(4.4, w), { color: GREEN, width: 2 });
      d.label(mul(4.75, u), s.phi > 0.5 ? "x'" : "x", { color: GREEN });
      d.label(mul(4.75, w), s.phi > 0.5 ? "y'" : "y", { color: GREEN });
      PARTICLES.forEach(function (p) {
        d.circle([p[0], p[1]], 11, { color: p[2] === 4 ? RED : MUTED, width: p[2] === 4 ? 2 : 1.2, fill: "var(--paper)" });
        d.label([p[0], p[1]], String(p[2]), { size: 12, color: p[2] === 4 ? RED : INK });
      });
      var P = [2, 3], xp = 2 * c + 3 * sn, yp = -2 * sn + 3 * c;
      d.line(P, mul(xp, u), { color: MUTED, width: 1, dash: "3 4" });
      d.line(P, mul(yp, w), { color: MUTED, width: 1, dash: "3 4" });
      d.arrow([0, 0], [2 - 0.24 * 0.5547, 3 - 0.24 * 0.8321], { color: RED, width: 2.5 });
      d.label([1.0, 1.9], "\\vec P_4", { color: RED });
      d.label([2.55, 3.45], "M_4", { color: RED, size: 13 });
    },
    formula: function (s) {
      var c = Math.cos(rad(s.phi)), sn = Math.sin(rad(s.phi));
      var xp = 2 * c + 3 * sn, yp = -2 * sn + 3 * c;
      var nm = s.phi > 0.5 ? "(x',y')" : "(x,y)";
      return "\\begin{gathered}\\text{軸轉 }" + deg(s.phi) + ":\\ \\ " + nm + "=(" + F(xp) + ",\\ " + F(yp) + ")\\\\ |\\vec P_4|=\\sqrt{" + F(xp) + "^2+" + F(yp) + "^2}=" + F(Math.sqrt(xp * xp + yp * yp)) + "\\\\ M_4=M_4'\\ (\\text{質量不變})\\end{gathered}";
    }
  });

  /* ---------------- 3. 向量加減（p.17–20） ---------------- */
  A.define("vec-add", {
    title: "首尾相接：加法、交換律與減法",
    question: "向量平移後怎麼相加？$\\vec B-\\vec A$ 指向哪裡？",
    view: [420, 300], origin: [60, 262], scale: 55,
    init: { bs: 0, as: 0, sum: 0, sub: 0 },
    steps: [
      { label: "兩個向量", caption: "$\\vec A=(3,1)$（紅）、$\\vec B=(1,2)$（藍），都從原點出發。", dur: 400, hold: 2000 },
      { label: "平移 $\\vec B$", caption: "把 $\\vec B$ 平移，尾端接到 $\\vec A$ 的箭頭。平移不改變向量。", to: { bs: 1 } },
      { label: "$\\vec A+\\vec B$", caption: "從 $\\vec A$ 的尾端連到平移後 $\\vec B$ 的箭頭，就是 $\\vec A+\\vec B$（綠）。", set: { sum: 1 }, dur: 600, hold: 2400 },
      { label: "交換次序", caption: "改成先走 $\\vec B$ 再走 $\\vec A$：兩條路線是平行四邊形的兩組邊，終點相同，所以 $\\vec A+\\vec B=\\vec B+\\vec A$。", to: { as: 1 } },
      { label: "$\\vec B-\\vec A$", caption: "減法：兩個向量都從原點出發，$\\vec B-\\vec A$（紫）從 $\\vec A$ 的箭頭指向 $\\vec B$ 的箭頭（終點減起點）。", set: { sum: 0, sub: 1 }, to: { bs: 0, as: 0 } }
    ],
    draw: function (d, s) {
      d.grid(-0.5, 5.5, -0.3, 4.2);
      var a = [3, 1], b = [1, 2];
      if (s.as > 0.01) d.arrow(mul(s.as, b), add(mul(s.as, b), a), { color: RED, width: 2, opacity: 0.55 });
      if (s.bs > 0.01) d.arrow(mul(s.bs, a), add(mul(s.bs, a), b), { color: BLUE, width: 2.5 });
      d.arrow([0, 0], a, { color: RED, width: 2.5 });
      d.arrow([0, 0], b, { color: BLUE, width: 2.5, opacity: s.bs > 0.01 ? 0.45 : 1 });
      d.label([1.6, 0.35], "\\vec A", { color: RED });
      d.label([0.25, 1.15], "\\vec B", { color: BLUE });
      if (s.sum) { d.arrow([0, 0], [4, 3], { color: GREEN, width: 3 }); d.label([1.75, 1.75], "\\vec A+\\vec B", { color: GREEN }); }
      if (s.sub) { d.arrow(a, b, { color: PURPLE, width: 3 }); d.label([2.2, 1.95], "\\vec B-\\vec A", { color: PURPLE }); }
    },
    formula: function (s) {
      switch (s._step) {
        case 0: return "\\vec A=(3,1),\\qquad \\vec B=(1,2)";
        case 1: case 2: return "\\vec A+\\vec B=(3+1,\\ 1+2)=(4,3)";
        case 3: return "\\vec B+\\vec A=(1+3,\\ 2+1)=(4,3)=\\vec A+\\vec B";
        default: return "\\vec B-\\vec A=(1-3,\\ 2-1)=(-2,\\ 1)";
      }
    }
  });

  /* ---------------- 4. 純量乘法（p.21–22） ---------------- */
  A.define("scalar-mult", {
    title: "純量乘法：伸縮與反向",
    question: "$c$ 由正變負時，$c\\vec A$ 的長度與方向怎麼變？",
    view: [420, 260], origin: [210, 130], scale: 38,
    init: { c: 1 },
    steps: [
      { label: "$c=1$", caption: "$\\vec A=(2,1)$，長度 $\\sqrt5\\approx2.24$。", dur: 300, hold: 1800 },
      { label: "$c=2$", caption: "$c=2$：每個分量都乘 2，方向不變，長度變 2 倍。", to: { c: 2 } },
      { label: "$c=-2$", caption: "$c=-2$：方向反轉，長度是 $|-2|=2$ 倍（不是 $-2$ 倍）。中途經過 $c=0$ 時變成零向量。", to: { c: -2 }, dur: 3000 },
      { label: "$c=0.5$", caption: "$c=0.5$：方向與 $\\vec A$ 相同，長度變一半。", to: { c: 0.5 }, dur: 2600 }
    ],
    draw: function (d, s) {
      d.grid(-5.4, 5.4, -3.2, 3.2);
      d.axes([-5.4, 5.2], [-3.2, 3.0]);
      d.arrow([0, 0], [2, 1], { color: RED, width: 2, opacity: 0.45 });
      d.label([2.2, 1.45], "\\vec A", { color: RED });
      var col = s.c < 0 ? PURPLE : BLUE;
      d.arrow([0, 0], [2 * s.c, s.c], { color: col, width: 3 });
      if (Math.abs(s.c) > 0.3) d.label([2 * s.c + (s.c > 0 ? 0.2 : -0.2), s.c - (s.c > 0 ? 0.55 : -0.55)], "c\\vec A", { color: col });
    },
    formula: function (s) {
      return "\\begin{gathered}c=" + F(s.c) + ":\\quad c\\vec A=(" + F(2 * s.c) + ",\\ " + F(s.c) + ")\\\\ |c\\vec A|=|c|\\,|\\vec A|=" + F(Math.abs(s.c)) + "\\times\\sqrt5=" + F(Math.abs(s.c) * Math.sqrt(5)) + "\\end{gathered}";
    }
  });

  /* ---------------- 5. 內積與投影（p.25–28） ---------------- */
  A.define("dot-proj", {
    title: "內積 $=|\\vec A|\\times$（$\\vec B$ 在 $\\vec A$ 方向的影子）",
    question: "夾角改變時，內積的正負與大小如何變？",
    view: [440, 270], origin: [170, 205], scale: 45,
    init: { th: 20 },
    steps: [
      { label: "銳角", caption: "$\\theta=20^\\circ$：$\\vec B$ 的影子（綠）和 $\\vec A$ 同方向，內積為正且接近最大值 $12$。", dur: 300, hold: 2200 },
      { label: "轉到 $90^\\circ$", caption: "$\\theta$ 增加，影子變短；$\\theta=90^\\circ$ 時影子長度為 0，內積為 0——這就是「正交」。", to: { th: 90 }, dur: 2600 },
      { label: "鈍角", caption: "$\\theta=150^\\circ$：影子落在 $\\vec A$ 的反方向，$\\cos\\theta\\lt0$，內積為負。", to: { th: 150 } },
      { label: "回到 $60^\\circ$", caption: "$\\theta=60^\\circ$：$\\cos60^\\circ=\\tfrac12$，影子長 $3\\times\\tfrac12=1.5$，內積 $4\\times1.5=6$。", to: { th: 60 }, dur: 2600 }
    ],
    draw: function (d, s) {
      var c = Math.cos(rad(s.th)), sn = Math.sin(rad(s.th)), B = [3 * c, 3 * sn];
      d.line([-3.6, 0], [5.2, 0], { color: "var(--grid)", width: 1.5 });
      d.arc([0, 0], 0.7, 0, s.th, { color: MUTED, width: 1.3 });
      d.label([0.95 * Math.cos(rad(s.th / 2)), 0.95 * Math.sin(rad(s.th / 2))], "\\theta", { color: MUTED, size: 13 });
      d.line(B, [B[0], 0], { color: MUTED, width: 1.2, dash: "4 4" });
      if (Math.abs(B[0]) > 0.05) d.line([0, -0.12], [B[0], -0.12], { color: GREEN, width: 5 });
      d.arrow([0, 0], [4, 0], { color: RED, width: 2.5 });
      d.arrow([0, 0], B, { color: BLUE, width: 2.5 });
      d.label([4.25, 0.3], "\\vec A", { color: RED });
      d.label([B[0] * 1.12, B[1] * 1.12 + 0.15], "\\vec B", { color: BLUE });
      if (Math.abs(B[0]) > 0.4) d.label([B[0] / 2, -0.55], "|\\vec B|\\cos\\theta", { color: GREEN, size: 13 });
    },
    formula: function (s) {
      var v = 12 * Math.cos(rad(s.th));
      var sign = Math.abs(v) < 0.05 ? "=0" : (v > 0 ? "\\gt0" : "\\lt0");
      return "\\begin{aligned}\\vec A\\cdot\\vec B&=|\\vec A||\\vec B|\\cos\\theta\\\\&=4\\times3\\times\\cos" + deg(s.th) + "\\\\&=" + F(v) + "\\ " + sign + "\\end{aligned}";
    }
  });

  /* ---------------- 6. 立方體對角線（課本 1-7） ---------------- */
  var CUBE_EDGES = [[[0, 0, 0], [1, 0, 0]], [[0, 0, 0], [0, 1, 0]], [[0, 0, 0], [0, 0, 1]], [[1, 0, 0], [1, 1, 0]], [[1, 0, 0], [1, 0, 1]], [[0, 1, 0], [1, 1, 0]],
    [[0, 1, 0], [0, 1, 1]], [[0, 0, 1], [1, 0, 1]], [[0, 0, 1], [0, 1, 1]], [[1, 1, 0], [1, 1, 1]], [[1, 0, 1], [1, 1, 1]], [[0, 1, 1], [1, 1, 1]]];
  A.define("cube-diag", {
    title: "單位立方體的體對角線",
    question: "兩條體對角線的夾角是多少？",
    view: [420, 330], origin: [200, 245], scale: 150,
    init: { az: 30, s1: 0, s2: 0, ang: 0, s34: 0 },
    steps: [
      { label: "立方體", caption: "邊長 1，一角在原點、三邊沿 $x_1,x_2,x_3$ 軸。8 個頂點的每個座標都是 0 或 1。", dur: 1200, hold: 1400, to: { az: 36 } },
      { label: "第一條 $\\vec d_1$", caption: "從 $(0,0,0)$ 到 $(1,1,1)$：$\\vec d_1=(1,1,1)$。", set: { s1: 1 }, to: { az: 42 } },
      { label: "第二條 $\\vec d_2$", caption: "從 $(1,0,0)$ 到 $(0,1,1)$：$\\vec d_2=(0,1,1)-(1,0,0)=(-1,1,1)$。", set: { s2: 1 }, to: { az: 48 } },
      { label: "夾角", caption: "兩條對角線交於中心 $(\\tfrac12,\\tfrac12,\\tfrac12)$。不用看圖，用內積就能算出夾角。", set: { ang: 1 }, to: { az: 52 } },
      { label: "其餘兩條", caption: "$\\vec d_3=(1,-1,1)$、$\\vec d_4=(1,1,-1)$。任兩條的內積都是 $\\pm1$，所以夾角都是 $70.5^\\circ$ 或其補角 $109.5^\\circ$。", set: { s34: 1 }, to: { az: 58 }, hold: 2600 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 20);
      [[1.45, 0, 0, "x_1"], [0, 1.45, 0, "x_2"], [0, 0, 1.35, "x_3"]].forEach(function (a) {
        d.arrow3([0, 0, 0], [a[0], a[1], a[2]], { color: MUTED, width: 1.2, head: 8 });
        d.label3([a[0] * 1.08, a[1] * 1.08, a[2] * 1.08], a[3], { color: MUTED, size: 13 });
      });
      CUBE_EDGES.forEach(function (e) { d.line3(e[0], e[1], { color: MUTED, width: 1.3, opacity: 0.8 }); });
      if (s.s34) {
        d.line3([0, 1, 0], [1, 0, 1], { color: GREEN, width: 2, opacity: 0.7 });
        d.line3([0, 0, 1], [1, 1, 0], { color: PURPLE, width: 2, opacity: 0.7 });
      }
      if (s.s1) { d.arrow3([0, 0, 0], [1, 1, 1], { color: RED, width: 3 }); d.label3([1.05, 1.05, 1.12], "\\vec d_1", { color: RED }); }
      if (s.s2) { d.arrow3([1, 0, 0], [0, 1, 1], { color: BLUE, width: 3 }); d.label3([-0.05, 1.0, 1.15], "\\vec d_2", { color: BLUE }); }
      if (s.ang) {
        var C = [0.5, 0.5, 0.5], u = norm3([1, 1, 1]), w = norm3([-1, 1, 1]), pts = [];
        for (var i = 0; i <= 20; i++) { var t = i / 20, v = norm3(add(mul(1 - t, u), mul(t, w))); pts.push(add(C, mul(0.2, v))); }
        d.path3(pts, { color: INK, width: 2 });
        d.dot3(C, { r: 3.5 });
        d.label3(add(C, mul(0.3, norm3(add(u, w)))), "\\theta", { size: 13 });
      }
      [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 1, 1]].forEach(function (p) { if ((s.s1 && (p.join() === "0,0,0" || p.join() === "1,1,1")) || (s.s2 && (p.join() === "1,0,0" || p.join() === "0,1,1"))) d.dot3(p, { r: 3.5, color: INK }); });
    },
    formula: function (s) {
      switch (s._step) {
        case 0: return "\\text{頂點：每個座標取 }0\\text{ 或 }1";
        case 1: return "\\begin{gathered}\\vec d_1=(1,1,1)-(0,0,0)=(1,1,1)\\\\ |\\vec d_1|=\\sqrt3\\end{gathered}";
        case 2: return "\\begin{gathered}\\vec d_2=(0,1,1)-(1,0,0)=(-1,1,1)\\\\ |\\vec d_2|=\\sqrt3\\end{gathered}";
        case 3: return "\\begin{aligned}\\cos\\theta&=\\frac{\\vec d_1\\cdot\\vec d_2}{|\\vec d_1||\\vec d_2|}=\\frac{-1+1+1}{\\sqrt3\\cdot\\sqrt3}\\\\&=\\frac13\\ \\Rightarrow\\ \\theta\\approx70.5^\\circ\\end{aligned}";
        default: return "\\begin{gathered}\\vec d_2\\cdot\\vec d_3=-1-1+1=-1\\\\ \\theta\\approx109.5^\\circ=180^\\circ-70.5^\\circ\\end{gathered}";
      }
    }
  });

  /* ---------------- 7. 外積：面積與方向（p.31–32） ---------------- */
  A.define("cross-area", {
    title: "外積的大小 = 平行四邊形面積，方向用右手定則",
    question: "$\\theta$ 改變時，$\\vec A\\times\\vec B$ 的長度與指向如何變？",
    view: [420, 330], origin: [190, 205], scale: 50,
    init: { th: 40 },
    steps: [
      { label: "$\\theta=40^\\circ$", caption: "$\\vec A$（紅）、$\\vec B$（藍）在水平面上，張成淺藍色平行四邊形。$\\vec A\\times\\vec B$（綠）垂直於這個平面。綠箭頭長度按比例縮小顯示。", dur: 300, hold: 2400 },
      { label: "$\\theta\\to90^\\circ$", caption: "$\\theta=90^\\circ$：平行四邊形變成長方形，面積最大 $=|\\vec A||\\vec B|$。", to: { th: 90 } },
      { label: "$\\theta\\to160^\\circ$", caption: "$\\theta$ 接近 $180^\\circ$：平行四邊形被壓扁，面積趨近 0，外積變短。", to: { th: 160 } },
      { label: "$\\theta\\to250^\\circ$", caption: "$\\vec B$ 轉到 $\\vec A$ 的另一側：從 $\\vec A$ 彎向 $\\vec B$ 變成順時針，右手拇指朝下，外積指向 $-\\hat k$。", to: { th: 250 }, dur: 2800 }
    ],
    draw: function (d, s) {
      d.camera(25, 24);
      var c = Math.cos(rad(s.th)), sn = Math.sin(rad(s.th));
      var a = [0, 3, 0], b = [-2.2 * sn, 2.2 * c, 0], ab = add(a, b);
      d.line3([0, 0, -2.4], [0, 0, 2.6], { color: "var(--grid)", width: 1.5 });
      d.poly3([[0, 0, 0], a, ab, b], { color: BLUE, width: 1, fill: BLUE, fillOpacity: 0.16 });
      var pts = [];
      for (var i = 0; i <= 30; i++) { var t = rad(s.th * i / 30); pts.push([-0.8 * Math.sin(t), 0.8 * Math.cos(t), 0]); }
      d.path3(pts, { color: MUTED, width: 1.3 });
      d.arrow3([0, 0, 0], a, { color: RED, width: 2.5 });
      d.arrow3([0, 0, 0], b, { color: BLUE, width: 2.5 });
      d.label3([0, 3.35, 0], "\\vec A", { color: RED });
      d.label3(mul(1.18, b), "\\vec B", { color: BLUE });
      var cz = 6.6 * sn * 0.33;
      if (Math.abs(cz) > 0.05) d.arrow3([0, 0, 0], [0, 0, cz], { color: GREEN, width: 3 });
      d.label3([0, 0.15, cz + (cz >= 0 ? 0.35 : -0.35)], "\\vec A\\times\\vec B", { color: GREEN });
      var mid = mul(0.5, ab);
      d.label3(mid, "\\text{面積}", { color: BLUE, size: 12 });
    },
    formula: function (s) {
      var sn = Math.sin(rad(s.th)), v = 6.6 * sn;
      var dir = Math.abs(v) < 0.05 ? "\\vec 0" : (v > 0 ? "+\\hat k\\ (\\text{朝上})" : "-\\hat k\\ (\\text{朝下})");
      return "\\begin{aligned}|\\vec A\\times\\vec B|&=|\\vec A||\\vec B||\\sin\\theta|\\\\&=3\\times2.2\\times|\\sin" + deg(s.th) + "|=" + F(Math.abs(v)) + "\\\\ \\text{方向}&:\\ " + dir + "\\end{aligned}";
    }
  });

  /* ---------------- 8. 角速度（p.33–34） ---------------- */
  A.define("angular", {
    title: "$\\vec v=\\vec\\omega\\times\\vec r$：大小 $r\\omega\\sin\\alpha=R\\omega$，方向沿切線",
    question: "原點沿轉軸移動時，$r$ 與 $\\alpha$ 都變了，速度會變嗎？",
    view: [420, 340], origin: [205, 300], scale: 55,
    init: { phi: 0, z0: 0, showR: 0, showV: 0 },
    steps: [
      { label: "繞 $z$ 軸轉", caption: "粒子在高度 $3$、半徑 $R=1.6$ 的圓上繞 $z$ 軸轉，$\\omega=2\\ \\text{rad/s}$。$\\vec\\omega$（紫）沿轉軸朝上（從上往下看是逆時針）。", to: { phi: 100 }, dur: 2400 },
      { label: "$\\vec r$ 與 $\\alpha$", caption: "從軸上的原點 $O$ 畫 $\\vec r$（紅）指向粒子，$\\alpha$ 是 $\\vec r$ 與轉軸的夾角；到軸的距離 $R=r\\sin\\alpha$。", set: { showR: 1 }, to: { phi: 170 } },
      { label: "$\\vec v=\\vec\\omega\\times\\vec r$", caption: "$\\vec v=\\vec\\omega\\times\\vec r$（藍）垂直於轉軸與 $\\vec r$，沿圓周切線，大小 $r\\omega\\sin\\alpha=R\\omega$。", set: { showV: 1 }, to: { phi: 260 } },
      { label: "移動原點", caption: "把原點 $O$ 沿軸往上移：$r$ 變短、$\\alpha$ 變大，但 $r\\sin\\alpha=R$ 不變，所以 $\\vec v$ 完全一樣。", to: { z0: 1.8, phi: 330 }, dur: 3000 },
      { label: "移回原點", caption: "原點移回：$\\vec v$ 仍然相同。只要原點在轉軸上，$\\vec v=\\vec\\omega\\times\\vec r$ 都成立。", to: { z0: 0, phi: 400 }, dur: 3000 }
    ],
    draw: function (d, s) {
      d.camera(30, 16);
      var R = 1.6, h = 3, O = [0, 0, s.z0];
      d.line3([0, 0, -0.3], [0, 0, 4.3], { color: MUTED, width: 1.5, dash: "6 4" });
      var circ = [];
      for (var i = 0; i <= 60; i++) { var t = 2 * Math.PI * i / 60; circ.push([R * Math.cos(t), R * Math.sin(t), h]); }
      d.path3(circ, { color: MUTED, width: 1.3 });
      var p = [R * Math.cos(rad(s.phi)), R * Math.sin(rad(s.phi)), h];
      d.arrow3(O, add(O, [0, 0, 1.3]), { color: PURPLE, width: 3 });
      d.label3(add(O, [0.25, 0, 1.45]), "\\vec\\omega", { color: PURPLE });
      d.dot3(O, { r: 3.5 });
      d.label3(add(O, [0.0, -0.35, -0.1]), "O", { size: 13 });
      if (s.showR) {
        d.line3([0, 0, h], p, { color: MUTED, width: 1.3, dash: "4 3" });
        d.label3(mul(0.5, add([0, 0, h], p)), "R", { color: MUTED, size: 13 });
        d.arrow3(O, p, { color: RED, width: 2.5 });
        d.label3(add(mul(0.55, add(O, p)), [0, 0, -0.25]), "\\vec r", { color: RED });
        var rv = norm3([p[0], p[1], p[2] - s.z0]), pts = [];
        for (var k = 0; k <= 16; k++) { var tt = k / 16; pts.push(add(O, mul(0.7, norm3(add(mul(1 - tt, [0, 0, 1]), mul(tt, rv)))))); }
        d.path3(pts, { color: INK, width: 1.5 });
        d.label3(add(O, mul(0.95, norm3(add([0, 0, 1], rv)))), "\\alpha", { size: 13 });
      }
      d.dot3(p, { r: 6, color: RED });
      if (s.showV) {
        var v = [-2 * p[1], 2 * p[0], 0];
        d.arrow3(p, add(p, mul(0.4, v)), { color: BLUE, width: 3 });
        d.label3(add(p, mul(0.5, v)), "\\vec v", { color: BLUE });
      }
    },
    formula: function (s) {
      var R = 1.6, hz = 3 - s.z0, r = Math.sqrt(R * R + hz * hz), al = Math.atan2(R, hz) * 180 / Math.PI;
      if (!s.showR) return "\\omega=2\\ \\text{rad/s},\\quad R=1.6,\\quad v=R\\omega=3.2";
      return "\\begin{aligned}r&=\\sqrt{1.6^2+" + F(hz) + "^2}=" + F(r) + ",\\quad \\alpha=" + deg(al) + "\\\\ v&=r\\omega\\sin\\alpha=" + F(r) + "\\times2\\times\\sin" + deg(al) + "\\\\&=" + F(r * 2 * Math.sin(rad(al))) + "=R\\omega\\end{aligned}";
    }
  });

  /* ---------------- 9. 橢圓軌道（課本 1-10） ---------------- */
  A.define("ellipse", {
    title: "橢圓軌道上的速度 $\\vec v$（藍）與加速度 $\\vec a$（紅）",
    question: "$\\vec v$ 與 $\\vec a$ 在什麼位置互相垂直？",
    view: [440, 300], origin: [220, 150], scale: 62,
    init: { wt: 0, right: 0 },
    steps: [
      { label: "$t=0$", caption: "取 $b=1$、$\\omega=1$。$t=0$ 時粒子在 $(0,b)$，速度沿 $+x$，速率最大 $2b\\omega$。", dur: 300, hold: 2000 },
      { label: "到 $\\omega t=\\pi/2$", caption: "順時針前進到長軸端點 $(2b,0)$。加速度 $\\vec a=-\\omega^2\\vec r$ 一直指向中心。", to: { wt: Math.PI / 2 }, dur: 3000 },
      { label: "$\\vec v\\perp\\vec a$", caption: "此刻 $\\vec v=(0,-b\\omega)$、$\\vec a=(-2b\\omega^2,0)$，內積為 0：夾角 $90^\\circ$。速率在這裡最小 $b\\omega$。", set: { right: 1 }, dur: 300, hold: 3000 },
      { label: "繞一圈", caption: "繼續繞行：只有在四個軸端點 $\\vec v\\perp\\vec a$；其他位置 $\\vec v\\cdot\\vec a=-3b^2\\omega^3\\sin\\omega t\\cos\\omega t\\neq0$。", set: { right: 0 }, to: { wt: 2.5 * Math.PI }, dur: 6000, hold: 2000 }
    ],
    draw: function (d, s) {
      var pts = [];
      for (var i = 0; i <= 90; i++) { var t = 2 * Math.PI * i / 90; pts.push([2 * Math.sin(t), Math.cos(t)]); }
      d.line([-2.6, 0], [2.6, 0], { color: "var(--grid)", width: 1 });
      d.line([0, -1.5], [0, 1.5], { color: "var(--grid)", width: 1 });
      d.path(pts, { color: MUTED, width: 1.5 });
      d.dot([0, 0], { r: 3 });
      var sn = Math.sin(s.wt), c = Math.cos(s.wt), P = [2 * sn, c];
      d.line([0, 0], P, { color: MUTED, width: 1, dash: "3 3" });
      var v = [2 * c, -sn], a = [-2 * sn, -c];
      d.arrow(P, add(P, mul(0.45, a)), { color: RED, width: 2.5 });
      d.arrow(P, add(P, mul(0.45, v)), { color: BLUE, width: 2.5 });
      d.dot(P, { r: 5, color: INK });
      d.label(add(P, add(mul(0.55, a), [0, 0.18])), "\\vec a", { color: RED });
      d.label(add(P, add(mul(0.55, v), [0.2, 0])), "\\vec v", { color: BLUE });
      if (s.right) d.rightAngle(P, [-1, 0], [0, -1], 0.18, { color: INK, width: 1.4 });
      d.label([2.25, -0.2], "2b", { color: MUTED, size: 12 });
      d.label([0.18, 1.2], "b", { color: MUTED, size: 12 });
    },
    formula: function (s) {
      var sn = Math.sin(s.wt), c = Math.cos(s.wt);
      var wtd = ((s.wt * 180 / Math.PI) % 360 + 360) % 360;
      return "\\begin{aligned}\\omega t&=" + deg(wtd) + "\\\\ \\vec v&=(" + F(2 * c) + ",\\ " + F(-sn) + ")\\,b\\omega\\\\ \\vec a&=(" + F(-2 * sn) + ",\\ " + F(-c) + ")\\,b\\omega^2\\\\ v&=b\\omega\\sqrt{1+3\\cos^2\\omega t}=" + F(Math.sqrt(1 + 3 * c * c)) + "\\,b\\omega\\\\ \\vec v\\cdot\\vec a&=" + F(-3 * sn * c) + "\\,b^2\\omega^3\\end{aligned}";
    }
  });

  /* ---------------- 10. 矩陣乘法（p.39 Example 1.2） ---------------- */
  var MA = [[2, 1, 3], [-2, 2, 4], [-1, -3, -4]], MB = [[-1, -2], [1, 2], [3, 4]];
  var CELL = 36;
  function mprod(i, j) { return MA[i][0] * MB[0][j] + MA[i][1] * MB[1][j] + MA[i][2] * MB[2][j]; }
  function bracket(d, x0, x1, y0, y1) {
    d.path([[x0 + 7, -y0], [x0, -y0], [x0, -y1], [x0 + 7, -y1]], { color: INK, width: 1.6 });
    d.path([[x1 - 7, -y0], [x1, -y0], [x1, -y1], [x1 - 7, -y1]], { color: INK, width: 1.6 });
  }
  var MM_STEPS = [];
  [[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [2, 1]].forEach(function (ij) {
    var i = ij[0], j = ij[1];
    MM_STEPS.push({ label: "$(AB)_{" + (i + 1) + (j + 1) + "}$", caption: "$A$ 的第 " + (i + 1) + " 個 row × $B$ 的第 " + (j + 1) + " 個 column，相乘再相加，填進 $(AB)_{" + (i + 1) + (j + 1) + "}$。", dur: 1500, hold: 1500, set: { i: i, j: j } });
  });
  A.define("matmul", {
    title: "矩陣乘法：row 內積 column",
    question: "$AB$ 的每一格怎麼算出來？",
    view: [440, 170], origin: [0, 0], scale: 1,
    init: { i: 0, j: 0 },
    steps: MM_STEPS,
    draw: function (d, s) {
      var ax = 22, bx = 168, rx = 300, y0 = 22;
      function cx(x0, c) { return x0 + 8 + CELL * c + CELL / 2; }
      function cy(r) { return y0 + CELL * r + CELL / 2; }
      d.rect(ax + 4, -(y0 + CELL * s.i), ax + 12 + CELL * 3, -(y0 + CELL * (s.i + 1)), { color: "none", fill: RED, fillOpacity: 0.14 });
      d.rect(bx + 8 + CELL * s.j, -y0, bx + 8 + CELL * (s.j + 1), -(y0 + CELL * 3), { color: "none", fill: BLUE, fillOpacity: 0.14 });
      d.rect(rx + 8 + CELL * s.j, -(y0 + CELL * s.i), rx + 8 + CELL * (s.j + 1), -(y0 + CELL * (s.i + 1)), { color: "none", fill: GREEN, fillOpacity: 0.2 });
      bracket(d, ax, ax + 16 + CELL * 3, y0 - 2, y0 + CELL * 3 + 2);
      bracket(d, bx, bx + 16 + CELL * 2, y0 - 2, y0 + CELL * 3 + 2);
      bracket(d, rx, rx + 16 + CELL * 2, y0 - 2, y0 + CELL * 3 + 2);
      d.label([ax - 12, -cy(1)], "A", {});
      d.label([bx - 12, -cy(1)], "B", {});
      d.label([rx - 32, -cy(1)], "=", {});
      for (var r = 0; r < 3; r++) {
        for (var c = 0; c < 3; c++) d.label([cx(ax, c), -cy(r)], String(MA[r][c]), { color: r === s.i ? RED : INK, size: 14 });
        for (var c2 = 0; c2 < 2; c2++) {
          d.label([cx(bx, c2), -cy(r)], String(MB[r][c2]), { color: c2 === s.j ? BLUE : INK, size: 14 });
          var idx = r * 2 + c2, cur = s.i * 2 + s.j;
          if (idx < cur || (idx === cur && s._p > 0.55)) d.label([cx(rx, c2), -cy(r)], String(mprod(r, c2)), { color: idx === cur ? GREEN : INK, size: 14 });
        }
      }
    },
    formula: function (s) {
      var i = s.i, j = s.j;
      var terms = [0, 1, 2].map(function (k) { return "(" + MA[i][k] + ")(" + MB[k][j] + ")"; }).join("+");
      var vals = [0, 1, 2].map(function (k) { return MA[i][k] * MB[k][j]; });
      var vs = vals.map(function (v, k) { return (k && v >= 0 ? "+" : "") + v; }).join("");
      return "\\begin{aligned}(AB)_{" + (i + 1) + (j + 1) + "}&=" + terms + (s._p > 0.3 ? "\\\\&=" + vs : "") + (s._p > 0.55 ? "=" + mprod(i, j) : "") + "\\end{aligned}";
    }
  });

  /* ---------------- 11. 二維旋轉（p.41–43） ---------------- */
  A.define("rot2d", {
    title: "座標軸轉 $\\theta$，點 $P$ 不動：$x'$、$y'$ 怎麼來",
    question: "$P=(3,2)$。座標軸逆時針轉 $\\theta$ 後，$P$ 的新座標是多少？",
    view: [420, 330], origin: [200, 255], scale: 42,
    init: { th: 0, parts: 0 },
    steps: [
      { label: "原座標", caption: "點 $P$ 在原座標 $(x,y)=(3,2)$。", dur: 300, hold: 1800 },
      { label: "軸轉 $30^\\circ$", caption: "座標軸逆時針轉 $\\theta=30^\\circ$（綠），點 $P$ 不動。虛線是從 $P$ 往新軸作的垂線，垂足的位置就是 $x'$、$y'$。", to: { th: 30 } },
      { label: "拆成兩段", caption: "$x'$ 可拆成兩段：沿 $x$ 走的 $3$ 投影到 $x'$ 軸得 $x\\cos\\theta$（紅），沿 $y$ 走的 $2$ 投影得 $y\\sin\\theta$（藍）。", set: { parts: 1 }, dur: 300, hold: 3600 },
      { label: "轉到 $90^\\circ$", caption: "轉到 $\\theta=90^\\circ$：新 $x'$ 軸指向原本的 $+y$、新 $y'$ 軸指向原本的 $-x$，所以 $(x',y')=(y,-x)=(2,-3)$。", set: { parts: 0 }, to: { th: 90 }, dur: 3200, hold: 2600 }
    ],
    draw: function (d, s) {
      var c = Math.cos(rad(s.th)), sn = Math.sin(rad(s.th)), u = [c, sn], w = [-sn, c];
      var P = [3, 2], xp = 3 * c + 2 * sn, yp = -3 * sn + 2 * c;
      d.arrow([-4.4, 0], [5, 0], { color: MUTED, width: 1.2, head: 8, opacity: 0.7 });
      d.arrow([0, -1.6], [0, 5.4], { color: MUTED, width: 1.2, head: 8, opacity: 0.7 });
      d.label([5.25, -0.15], "x", { color: MUTED });
      d.label([0.25, 5.55], "y", { color: MUTED });
      if (s.th > 0.5) {
        d.arrow(mul(-1.3, u), mul(5, u), { color: GREEN, width: 2 });
        d.arrow(mul(-1.3, w), mul(4.4, w), { color: GREEN, width: 2 });
        d.label(mul(5.35, u), "x'", { color: GREEN });
        d.label(mul(4.75, w), "y'", { color: GREEN });
        d.arc([0, 0], 0.9, 0, s.th, { color: GREEN, width: 1.3 });
        d.label([1.25 * Math.cos(rad(s.th / 2)), 1.25 * Math.sin(rad(s.th / 2))], "\\theta", { color: GREEN, size: 13 });
        d.line(P, mul(xp, u), { color: MUTED, width: 1.2, dash: "4 4" });
        d.line(P, mul(yp, w), { color: MUTED, width: 1.2, dash: "4 4" });
        d.rightAngle(mul(xp, u), mul(-1, u), mul(yp < 0 ? -1 : 1, w), 0.22);
      }
      if (s.parts) {
        d.path([[0, 0], [3, 0], P], { color: MUTED, width: 1.2, dash: "2 3" });
        var f1 = mul(3 * c, u), f2 = mul(xp, u);
        d.line([3, 0], f1, { color: RED, width: 1, dash: "2 3" });
        d.line([0, 0], f1, { color: RED, width: 5, opacity: 0.85 });
        d.line(f1, f2, { color: BLUE, width: 5, opacity: 0.85 });
        d.label(add(mul(0.5, f1), mul(-0.45, w)), "x\\cos\\theta", { color: RED, size: 13 });
        d.label(add(mul(0.5, add(f1, f2)), mul(-0.45, w)), "y\\sin\\theta", { color: BLUE, size: 13 });
      }
      d.dot(P, { r: 5, color: RED });
      d.label([3.3, 2.35], "P", { color: RED });
    },
    formula: function (s) {
      var c = Math.cos(rad(s.th)), sn = Math.sin(rad(s.th));
      return "\\begin{aligned}x'&=x\\cos\\theta+y\\sin\\theta\\\\&=3\\cos" + deg(s.th) + "+2\\sin" + deg(s.th) + "=" + F(3 * c + 2 * sn) +
        "\\\\ y'&=-x\\sin\\theta+y\\cos\\theta\\\\&=-3\\sin" + deg(s.th) + "+2\\cos" + deg(s.th) + "=" + F(-3 * sn + 2 * c) + "\\end{aligned}";
    }
  });

  /* ---------------- 12. Example 1.1：繞 x1 轉 30°（p.49） ---------------- */
  A.define("rot3d", {
    title: "Example 1.1：座標系繞 $x_1$ 轉 $30^\\circ$，$P(2,1,3)$ 的新分量",
    question: "新 $x_2'$、$x_3'$ 軸上的投影各是多少？長度有沒有變？",
    view: [440, 350], origin: [190, 262], scale: 48,
    init: { phi: 0, p2: 0, p3: 0 },
    steps: [
      { label: "原座標中的 $P$", caption: "點 $P(2,1,3)$。虛線標出它在 $x_1x_2$ 平面上的影子和高度 $3$。", dur: 300, hold: 2200 },
      { label: "繞 $x_1$ 轉 $30^\\circ$", caption: "$x_1$ 軸不動；$x_2,x_3$ 兩軸（綠）在它們的平面內轉 $30^\\circ$：$x_2'$ 往上抬，$x_3'$ 往 $-x_2$ 傾倒。", to: { phi: 30 } },
      { label: "投影到 $x_2'$", caption: "從 $P$ 往 $x_2'$ 軸作垂線，垂足到原點的長度就是 $x_2'=\\cos30^\\circ\\cdot1+\\sin30^\\circ\\cdot3$（紅）。", set: { p2: 1 }, dur: 300, hold: 3200 },
      { label: "投影到 $x_3'$", caption: "同理 $x_3'=-\\sin30^\\circ\\cdot1+\\cos30^\\circ\\cdot3$（藍）。$x_1'=x_1=2$ 不變。", set: { p3: 1 }, dur: 300, hold: 3200 },
      { label: "長度不變", caption: "驗算：新舊分量算出的長度平方都是 $14$。旋轉只改變分量，不改變向量。", dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      d.camera(40, 18);
      var c = Math.cos(rad(s.phi)), sn = Math.sin(rad(s.phi));
      var e2 = [0, c, sn], e3 = [0, -sn, c], P = [2, 1, 3];
      [[[4, 0, 0], "x_1"], [[0, 4, 0], "x_2"], [[0, 0, 4], "x_3"]].forEach(function (a) {
        d.arrow3([0, 0, 0], a[0], { color: MUTED, width: 1.3, head: 8, opacity: 0.8 });
        d.label3(mul(1.08, a[0]), a[1], { color: MUTED, size: 13 });
      });
      d.line3(P, [2, 1, 0], { color: MUTED, width: 1, dash: "3 3" });
      d.line3([2, 1, 0], [2, 0, 0], { color: MUTED, width: 1, dash: "3 3" });
      d.line3([2, 1, 0], [0, 1, 0], { color: MUTED, width: 1, dash: "3 3" });
      if (s.phi > 0.5) {
        d.arrow3([0, 0, 0], mul(4, e2), { color: GREEN, width: 2.2 });
        d.arrow3([0, 0, 0], mul(4, e3), { color: GREEN, width: 2.2 });
        d.label3(mul(4.35, e2), "x_2'", { color: GREEN });
        d.label3(mul(4.3, e3), "x_3'", { color: GREEN });
        var arc = [];
        for (var i = 0; i <= 12; i++) { var t = rad(s.phi * i / 12); arc.push([0, 1.4 * Math.cos(t), 1.4 * Math.sin(t)]); }
        d.path3(arc, { color: GREEN, width: 1.3 });
        d.label3([0, 1.75, 0.45], "30^\\circ", { color: GREEN, size: 12 });
      }
      var x2 = dot3(P, e2), x3 = dot3(P, e3);
      if (s.p2) {
        d.line3(P, mul(x2, e2), { color: RED, width: 1.2, dash: "4 3" });
        d.line3([0, 0, 0], mul(x2, e2), { color: RED, width: 5, opacity: 0.8 });
        d.label3(add(mul(x2 * 0.55, e2), [0, 0.1, -0.45]), "x_2'", { color: RED, size: 13 });
      }
      if (s.p3) {
        d.line3(P, mul(x3, e3), { color: BLUE, width: 1.2, dash: "4 3" });
        d.line3([0, 0, 0], mul(x3, e3), { color: BLUE, width: 5, opacity: 0.8 });
        d.label3(add(mul(x3 * 0.55, e3), [0, -0.5, 0]), "x_3'", { color: BLUE, size: 13 });
      }
      d.line3([0, 0, 0], P, { color: RED, width: 1.2, opacity: 0.5 });
      d.dot3(P, { r: 5.5, color: RED });
      d.label3(add(P, [0, 0.3, 0.3]), "P", { color: RED });
    },
    formula: function (s) {
      var c = Math.cos(rad(s.phi)), sn = Math.sin(rad(s.phi)), x2 = c + 3 * sn, x3 = -sn + 3 * c;
      if (s._step === 0) return "\\vec P=(2,1,3),\\qquad |\\vec P|^2=2^2+1^2+3^2=14";
      if (s._step === 4) return "\\begin{aligned}|\\vec P'|^2&=2^2+" + F(x2, 3) + "^2+" + F(x3, 3) + "^2\\\\&=" + F(4 + x2 * x2 + x3 * x3, 3) + "=|\\vec P|^2\\end{aligned}";
      return "\\begin{aligned}x_1'&=2\\\\ x_2'&=\\cos" + deg(s.phi) + "\\cdot1+\\sin" + deg(s.phi) + "\\cdot3\\\\&=" + F(x2, 3) + "\\\\ x_3'&=-\\sin" + deg(s.phi) + "\\cdot1+\\cos" + deg(s.phi) + "\\cdot3\\\\&=" + F(x3, 3) + "\\end{aligned}";
    }
  });

  /* ---------------- 13. 繞 (1,1,1) 轉 120°（課本 1-3） ---------------- */
  var N111 = norm3([1, 1, 1]);
  A.define("rot120", {
    title: "繞體對角線 $\\hat n=(1,1,1)/\\sqrt3$ 旋轉：三軸輪換",
    question: "轉 $120^\\circ$ 時，每個新軸落在哪個舊軸上？",
    view: [420, 340], origin: [205, 225], scale: 125,
    init: { phi: 0, az: 45, el: 26, tri: 1 },
    steps: [
      { label: "轉軸", caption: "紫色虛線是轉軸 $\\hat n=\\tfrac1{\\sqrt3}(1,1,1)$，與三個座標軸夾角都相等。灰色是原座標軸。", dur: 300, hold: 2400 },
      { label: "轉 $60^\\circ$", caption: "彩色的新軸繞 $\\hat n$ 轉動。三個軸尖端構成的三角形也跟著轉。右邊矩陣的每個 row 是新軸在舊座標中的分量。", to: { phi: 60 }, dur: 3000 },
      { label: "轉到 $120^\\circ$", caption: "轉到 $120^\\circ$：$x_1'$ 落在舊 $x_2$ 上、$x_2'$ 落在 $x_3$ 上、$x_3'$ 落在 $x_1$ 上。", to: { phi: 120 }, dur: 3000 },
      { label: "得到 $\\lambda$", caption: "矩陣變成只有 0 和 1 的輪換矩陣：$x_1'=x_2,\\ x_2'=x_3,\\ x_3'=x_1$。", dur: 300, hold: 3200 }
    ],
    draw: function (d, s) {
      d.camera(s.az, s.el);
      var E = [[1, 0, 0], [0, 1, 0], [0, 0, 1]], names = ["x_1", "x_2", "x_3"], cols = [RED, BLUE, GREEN];
      d.line3(mul(-0.35, N111), mul(1.75, N111), { color: PURPLE, width: 2, dash: "6 4" });
      d.label3(mul(1.88, N111), "\\hat n", { color: PURPLE });
      E.forEach(function (e, i) {
        d.arrow3([0, 0, 0], mul(1.25, e), { color: MUTED, width: 1.3, head: 8, opacity: 0.7 });
        d.label3(mul(1.4, e), names[i], { color: MUTED, size: 13 });
      });
      var R = E.map(function (e) { return rotate(e, N111, s.phi); });
      if (s.tri) d.poly3(R, { color: PURPLE, width: 1, fill: PURPLE, fillOpacity: 0.1 });
      R.forEach(function (r, i) {
        d.arrow3([0, 0, 0], r, { color: cols[i], width: 3 });
        d.label3(add(mul(1.12, r), [0, 0, 0.06]), names[i] + "'", { color: cols[i] });
      });
    },
    formula: function (s) {
      var R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]].map(function (e) { return rotate(e, N111, s.phi); });
      var rows = R.map(function (r) { return r.map(function (x) { return F(x, 2); }).join("&"); }).join("\\\\");
      return "\\phi=" + deg(s.phi) + ":\\quad \\lambda=\\begin{bmatrix}" + rows + "\\end{bmatrix}";
    }
  });
})();
