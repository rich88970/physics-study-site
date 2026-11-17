/* 應用數學第 5 章（Frobenius 法、Legendre 多項式）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", GRID = "var(--grid)";

  /* ---------------- 1. 10/7 板書例題的兩個解：γ 決定 x→0 的行為 ---------------- */
  function Y1(x) { return x <= 0 ? 0 : Math.sqrt(x / 2) * Math.sin(Math.sqrt(2 * x)); }   // = x(1 - x/3 + x²/30 - …)
  function Y2(x) { return x <= 0 ? 0 : Math.sqrt(x) * Math.cos(Math.sqrt(2 * x)); }         // = √x(1 - x + x²/6 - …)
  A.define("am5-two", {
    title: "$2x^2y''-xy'+(1+x)y=0$ 的兩個 Frobenius 解",
    question: "指標 $\\gamma=1$ 與 $\\gamma=\\tfrac12$ 在圖上看起來差在哪裡？",
    view: [440, 260], origin: [34, 130], scale: 38,
    init: { xm: 1 },
    steps: [
      { label: "$x$ 很小", caption: "$x$ 很小時級數只剩第一項：$y_1\\approx x^{1}$（直線，斜率 1）、$y_2\\approx x^{1/2}$（在 0 的切線是鉛直的）。指標 $\\gamma$ 就是解在 $x\\to0^+$ 的次方。虛線是 $x$ 與 $\\sqrt x$。", dur: 300, hold: 2600 },
      { label: "拉遠", caption: "把範圍拉到 $0\\le x\\le12$：兩個解都在振盪，振幅慢慢變大，而且它們的零點交錯出現。網站由一般項認出 closed form：$y_1=\\sqrt{x/2}\\,\\sin\\sqrt{2x}$、$y_2=\\sqrt x\\cos\\sqrt{2x}$。", to: { xm: 12 }, dur: 1600, hold: 2800 }
    ],
    draw: function (d, s) {
      var U = 10.4, sx = U / s.xm, Ym = Math.max(1.1, Math.sqrt(s.xm) * 1.05), sy = 3.0 / Ym;
      d.line([0, 0], [U + 0.2, 0], { color: MUTED, width: 1.2 });
      d.line([0, -3.2], [0, 3.2], { color: MUTED, width: 1.2 });
      var ticks = s.xm < 3 ? [0.25, 0.5, 0.75, 1] : [3, 6, 9, 12];
      ticks.forEach(function (t) { if (t <= s.xm + 1e-9) { d.line([t * sx, -0.1], [t * sx, 0.1], { color: MUTED, width: 1 }); d.label([t * sx, -0.42], F(t, t < 1 ? 2 : 0), { color: MUTED, size: 11 }); } });
      function curve(f, o) {
        var pts = [], n = 240;
        for (var i = 0; i <= n; i++) { var x = s.xm * i / n; pts.push([x * sx, f(x) * sy]); }
        d.path(pts, o);
      }
      if (s.xm < 4) {
        curve(function (x) { return x; }, { color: BLUE, width: 1.4, dash: "5 4", opacity: 0.7 });
        curve(function (x) { return Math.sqrt(x); }, { color: RED, width: 1.4, dash: "5 4", opacity: 0.7 });
      }
      curve(Y1, { color: BLUE, width: 2.6 });
      curve(Y2, { color: RED, width: 2.6 });
      d.label([1.9, 2.9], "y_1\\ (\\gamma=1)", { color: BLUE, size: 12 });
      d.label([1.9, 2.3], "y_2\\ (\\gamma=\\tfrac12)", { color: RED, size: 12 });
    },
    formula: function (s) {
      var x = s.xm;
      return "y_1=x\\big(1-\\tfrac x3+\\tfrac{x^2}{30}-\\cdots\\big)\\\\ y_2=\\sqrt x\\big(1-x+\\tfrac{x^2}6-\\cdots\\big)\\\\ x=" + F(x, x < 3 ? 2 : 1) + ":\\ y_1=" + F(Y1(x), 3) + ",\\ y_2=" + F(Y2(x), 3);
    }
  });

  /* ---------------- 2. Legendre 多項式 P0–P3（§4、114 上期末 3） ---------------- */
  var P = [
    function () { return 1; },
    function (x) { return x; },
    function (x) { return (3 * x * x - 1) / 2; },
    function (x) { return (5 * x * x * x - 3 * x) / 2; }
  ];
  var COL = [MUTED, BLUE, GREEN, RED];
  var TEX = ["P_0=1", "P_1=x", "P_2=\\tfrac12(3x^2-1)", "P_3=\\tfrac12(5x^3-3x)"];
  var NOTE = [
    "P_0(\\pm1)=1",
    "P_1(1)=1,\\ P_1(-1)=-1,\\ \\text{zero }x=0",
    "P_2(0)=-\\tfrac12,\\ \\text{zeros }x=\\pm\\tfrac1{\\sqrt3}\\approx\\pm0.577",
    "\\text{zeros }0,\\ \\pm\\sqrt{\\tfrac35}\\approx\\pm0.775\\\\ P_3(\\pm\\tfrac1{\\sqrt5})=\\mp\\tfrac1{\\sqrt5}\\approx\\mp0.447"
  ];
  A.define("am5-legendre", {
    title: "Legendre 多項式 $P_0$–$P_3$（$-1\\le x\\le1$）",
    question: "怎麼不用描很多點就畫出 $P_0$ 到 $P_3$？",
    view: [440, 300], origin: [220, 150], scale: 115,
    init: { k: 0 },
    steps: [
      { label: "$P_0$", caption: "$P_0=1$：水平線。所有 $P_l$ 都歸一化成 $P_l(1)=1$，所以每條曲線都通過右上角 $(1,1)$。", dur: 300, hold: 2000 },
      { label: "$P_1$", caption: "$P_1=x$：通過原點的直線，奇函數，$P_1(-1)=-1$。", set: { k: 1 }, dur: 300, hold: 2000 },
      { label: "$P_2$", caption: "$P_2=\\tfrac12(3x^2-1)$：偶函數的拋物線，底部在 $x=0$、高度 $-\\tfrac12$，零點 $\\pm\\tfrac1{\\sqrt3}\\approx\\pm0.577$，兩端都是 1。", set: { k: 2 }, dur: 300, hold: 2400 },
      { label: "$P_3$", caption: "$P_3=\\tfrac12(5x^3-3x)$：奇函數，零點 $0$、$\\pm0.775$；在 $x=\\pm0.447$ 有極值 $\\mp0.447$；$P_3(-1)=-1$。$P_l$ 在 $(-1,1)$ 內正好有 $l$ 個零點。", set: { k: 3 }, dur: 300, hold: 2800 }
    ],
    draw: function (d, s) {
      d.rect(-1, -1, 1, 1, { color: GRID, width: 1 });
      d.line([-1.25, 0], [1.25, 0], { color: MUTED, width: 1.2 });
      d.line([0, -1.2], [0, 1.2], { color: MUTED, width: 1.2 });
      [-1, -0.5, 0.5, 1].forEach(function (t) { d.line([t, -0.03], [t, 0.03], { color: MUTED, width: 1 }); d.label([t, -0.12], F(t, t % 1 ? 1 : 0), { color: MUTED, size: 11 }); });
      [-1, 1].forEach(function (t) { d.label([-1.12, t], F(t, 0), { color: MUTED, size: 11 }); });
      for (var l = 0; l <= s.k; l++) {
        var pts = [];
        for (var i = 0; i <= 160; i++) { var x = -1 + 2 * i / 160; pts.push([x, P[l](x)]); }
        d.path(pts, { color: COL[l], width: l === s.k ? 3 : 1.8, opacity: l === s.k ? 1 : 0.75 });
      }
      var lab = [[0.62, 1.1], [0.62, 0.72], [0.18, -0.6], [0.6, -0.6]];
      for (var j = 0; j <= s.k; j++) d.label(lab[j], "P_" + j, { color: COL[j], size: 13 });
      if (s.k === 2) [-1 / Math.sqrt(3), 1 / Math.sqrt(3)].forEach(function (z) { d.dot([z, 0], { color: GREEN, r: 4 }); });
      if (s.k === 3) {
        [-Math.sqrt(0.6), 0, Math.sqrt(0.6)].forEach(function (z) { d.dot([z, 0], { color: RED, r: 4 }); });
        [-1 / Math.sqrt(5), 1 / Math.sqrt(5)].forEach(function (z) { d.dot([z, P[3](z)], { color: RED, r: 3 }); });
      }
      d.dot([1, 1], { color: "var(--ink)", r: 3.5 });
    },
    formula: function (s) { return TEX[s.k] + "\\\\ " + NOTE[s.k]; }
  });
})();
