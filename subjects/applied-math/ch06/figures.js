/* 應用數學第 6 章（Bessel 函數）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。
   J_n 用級數、Y_0／Y_1 用含 ln 的級數計算（0 < x ≤ 12 誤差 < 1e-11，已用 mpmath 比對）。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", GRID = "var(--grid)";
  var EG = 0.5772156649015329;

  function fact(n) { var r = 1; for (var i = 2; i <= n; i++) r *= i; return r; }
  function Jn(n, x) {
    var t = Math.pow(x / 2, n) / fact(n), s = 0;
    for (var k = 0; k < 60; k++) { s += t; t *= -(x * x / 4) / ((k + 1) * (k + 1 + n)); }
    return s;
  }
  function Y0(x) {
    var t = 1, H = 0, s = 0;
    for (var k = 1; k < 60; k++) { t *= -(x * x / 4) / (k * k); H += 1 / k; s -= t * H; }
    return 2 / Math.PI * ((Math.log(x / 2) + EG) * Jn(0, x) + s);
  }
  function Y1(x) {
    var t = x / 2, Hk = 0, s = 0;
    for (var k = 0; k < 60; k++) {
      if (k > 0) { t *= -(x * x / 4) / (k * (k + 1)); Hk += 1 / k; }
      s += (2 * (Hk - EG) + 1 / (k + 1)) * t;
    }
    return 2 / Math.PI * Jn(1, x) * Math.log(x / 2) - 2 / (Math.PI * x) - s / Math.PI;
  }
  var J0 = function (x) { return Jn(0, x); }, J1 = function (x) { return Jn(1, x); };

  /* ---------------- 1. J0, J1, Y0, Y1 與零點（§3.1、§3.2） ---------------- */
  var ZJ0 = [2.4048, 5.5201, 8.6537], ZJ1 = [3.8317, 7.0156, 10.1735];
  var ZY0 = [0.8936, 3.9577, 7.0861], ZY1 = [2.1971, 5.4297, 8.5960];
  A.define("am6-graphs", {
    title: "$J_0,J_1$ 與 $Y_0,Y_1$（$0\\lt x\\le12$）",
    question: "Bessel 函數長什麼樣？零點表的數字在圖上是哪裡？",
    view: [440, 260], origin: [30, 140], scale: 100,
    init: { k: 0 },
    steps: [
      { label: "$J_0$、$J_1$", caption: "$J_0(0)=1$、$J_1(0)=0$；兩者都是振幅像 $1/\\sqrt x$ 衰減的振盪，零點間距越來越接近 $\\pi$。圓點是零點：$J_0$ 在 2.40、5.52、8.65，$J_1$ 在 3.83、7.02、10.17（板書 2.4、5.5、8.7；3.8、7.0、10.2）。兩組零點交錯出現。", dur: 300, hold: 3200 },
      { label: "$Y_0$、$Y_1$", caption: "Neumann 函數在 $x\\to0^+$ 往 $-\\infty$（$Y_0\\sim\\frac2\\pi\\ln x$、$Y_1\\sim-\\frac2{\\pi x}$），所以圓心在區域內時一定要丟掉。零點：$Y_0$ 在 0.89、3.96、7.09，$Y_1$ 在 2.20、5.43、8.60（板書 0.9、4.0、7.1；2.2、5.4、8.6）。", set: { k: 1 }, dur: 300, hold: 3200 },
      { label: "全部", caption: "四條曲線放在一起：$x$ 大時 $J_m$ 與 $Y_m$ 像 $\\cos$ 與 $\\sin$，相位差 $\\frac\\pi2$，零點也彼此交錯。", set: { k: 2 }, dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var sx = 33, sy = 1.05;   // 每單位 x 33px、y 105px
      function P(x, y) { return [x * sx / 100, y * sy]; }
      d.line(P(0, 0), P(12.4, 0), { color: MUTED, width: 1.2 });
      d.line(P(0, -1.08), P(0, 1.08), { color: MUTED, width: 1.2 });
      [3, 6, 9, 12].forEach(function (t) { d.line(P(t, -0.03), P(t, 0.03), { color: MUTED, width: 1 }); d.label(P(t, -0.13), String(t), { color: MUTED, size: 11 }); });
      [-1, 1].forEach(function (t) { d.line(P(-0.12, t), P(0.12, t), { color: MUTED, width: 1 }); d.label(P(-0.5, t), String(t), { color: MUTED, size: 11 }); });
      function curve(f, x0, o) {
        var pts = [];
        for (var i = 0; i <= 300; i++) { var x = x0 + (12 - x0) * i / 300, y = f(x); if (y < -1.05) continue; pts.push(P(x, y)); }
        d.path(pts, o);
      }
      var showJ = s.k === 0 || s.k === 2, showY = s.k >= 1;
      if (showJ) {
        curve(J0, 0, { color: BLUE, width: 2.6 });
        curve(J1, 0, { color: RED, width: 2.6 });
        ZJ0.forEach(function (z) { d.dot(P(z, 0), { color: BLUE, r: 3.5 }); });
        ZJ1.forEach(function (z) { d.dot(P(z, 0), { color: RED, r: 3.5 }); });
        d.label(P(0.9, 0.95), "J_0", { color: BLUE, size: 13 });
        d.label(P(2.6, 0.68), "J_1", { color: RED, size: 13 });
      }
      if (showY) {
        curve(Y0, 0.12, { color: GREEN, width: s.k === 1 ? 2.6 : 1.8, dash: s.k === 2 ? "6 4" : null });
        curve(Y1, 0.6, { color: PURPLE, width: s.k === 1 ? 2.6 : 1.8, dash: s.k === 2 ? "6 4" : null });
        ZY0.forEach(function (z) { d.dot(P(z, 0), { color: GREEN, r: 3 }); });
        ZY1.forEach(function (z) { d.dot(P(z, 0), { color: PURPLE, r: 3 }); });
        d.label(P(2.0, 0.62), "Y_0", { color: GREEN, size: 13 });
        d.label(P(4.4, 0.5), "Y_1", { color: PURPLE, size: 13 });
      }
    },
    formula: function (s) {
      if (s.k === 0) return "J_0(x)=1-\\tfrac{x^2}{4}+\\tfrac{x^4}{64}-\\cdots\\\\ j_{0n}\\approx2.405,\\ 5.520,\\ 8.654;\\quad j_{1n}\\approx3.832,\\ 7.016,\\ 10.17";
      if (s.k === 1) return "Y_0(x)\\approx\\tfrac2\\pi\\big(\\ln\\tfrac x2+\\gamma_E\\big)\\to-\\infty\\ (x\\to0^+)\\\\ Y_0(2)=" + F(Y0(2), 4) + ",\\ Y_1(2)=" + F(Y1(2), 4);
      return "J_m\\approx\\sqrt{\\tfrac{2}{\\pi x}}\\cos\\!\\big(x-\\tfrac{m\\pi}{2}-\\tfrac\\pi4\\big),\\quad Y_m\\approx\\sqrt{\\tfrac{2}{\\pi x}}\\sin\\!\\big(x-\\tfrac{m\\pi}{2}-\\tfrac\\pi4\\big)";
    }
  });

  /* ---------------- 2. 圓形鼓膜 (0,n) 模態的徑向剖面（自編 3-a） ---------------- */
  A.define("am6-drum", {
    title: "圓形鼓膜的軸對稱模態 $J_0(j_{0n}r/R)$",
    question: "$J_0$ 的零點怎麼變成鼓膜上的節線圓？",
    view: [440, 250], origin: [220, 125], scale: 95,
    init: { n: 1 },
    steps: [
      { label: "$(0,1)$", caption: "基頻模態 $J_0(2.405\\,r/R)$：整片鼓膜同向振動，只有邊緣 $r=R$ 不動（$J_0(2.405)=0$）。左右是通過圓心的剖面 $-R\\le r\\le R$。", dur: 300, hold: 2800 },
      { label: "$(0,2)$", caption: "$J_0(5.520\\,r/R)$：在 $r=\\frac{2.405}{5.520}R=0.436R$ 多了一個節線圓（圓點），內外反向振動。頻率是基頻的 $5.520/2.405=2.295$ 倍——不是整數倍。", set: { n: 2 }, dur: 300, hold: 3000 },
      { label: "$(0,3)$", caption: "$J_0(8.654\\,r/R)$：節線圓在 $r=0.278R$、$0.638R$，頻率 $3.598$ 倍。第 $n$ 個模態有 $n-1$ 個內部節線圓。", set: { n: 3 }, dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var Z = [2.4048, 5.5201, 8.6537], j = Z[s.n - 1];
      d.line([-1.15, 0], [1.15, 0], { color: MUTED, width: 1.2 });
      d.line([-1, -0.08], [-1, 0.08], { color: MUTED, width: 1.2 });
      d.line([1, -0.08], [1, 0.08], { color: MUTED, width: 1.2 });
      d.label([-1, -0.2], "-R", { color: MUTED, size: 11 });
      d.label([1, -0.2], "R", { color: MUTED, size: 11 });
      var pts = [];
      for (var i = 0; i <= 240; i++) { var r = -1 + 2 * i / 240; pts.push([r, J0(j * Math.abs(r))]); }
      d.path(pts, { color: BLUE, width: 2.8 });
      for (var k = 0; k < s.n - 1; k++) {
        var rn = Z[k] / j;
        d.dot([rn, 0], { color: RED, r: 4 }); d.dot([-rn, 0], { color: RED, r: 4 });
        d.label([rn, 0.18], F(rn, 3) + "R", { color: RED, size: 11 });
      }
      d.dot([1, 0], { color: "var(--ink)", r: 3.5 }); d.dot([-1, 0], { color: "var(--ink)", r: 3.5 });
    },
    formula: function (s) {
      var Z = [2.4048, 5.5201, 8.6537], j = Z[s.n - 1];
      return "u_{0" + s.n + "}\\propto J_0\\!\\Big(\\tfrac{" + F(j, 3) + "\\,r}{R}\\Big)\\cos\\omega_{0" + s.n + "}t,\\qquad\\frac{\\omega_{0" + s.n + "}}{\\omega_{01}}=" + F(j / Z[0], 3);
    }
  });
})();
