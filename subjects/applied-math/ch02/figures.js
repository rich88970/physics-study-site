/* 應用數學第 2 章（二階線性齊次方程）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", MUTED = "var(--muted)", INK = "var(--ink)", GRID = "var(--grid)";

  /* ω0 = 1、x(0) = 1、v(0) = 0 的阻尼振盪解（第 5 節 a2-b5 的三個公式） */
  function xt(g, t) {
    if (g < 0.995) {
      var w = Math.sqrt(1 - g * g);
      return Math.exp(-g * t) * (Math.cos(w * t) + g / w * Math.sin(w * t));
    }
    if (g <= 1.005) return (1 + t) * Math.exp(-t);
    var s = Math.sqrt(g * g - 1), l1 = -g + s, l2 = -g - s;
    return (l1 * Math.exp(l2 * t) - l2 * Math.exp(l1 * t)) / (l1 - l2);
  }
  function kind(g) { return g < 0.995 ? 0 : (g <= 1.005 ? 1 : 2); }

  /* ---------------- 阻尼振盪的三種情況（照片 7–8） ---------------- */
  var SX = 30, SY = 72, TMAX = 13;   // 每單位 t 30 px、每單位 x 72 px
  A.define("a2-damping", {
    title: "阻尼振盪：$\\gamma$ 和 $\\omega_0$ 比大小",
    question: "從 $x_0$ 由靜止放開，阻尼變大時曲線怎麼變？（$\\omega_0=1$）",
    view: [440, 215], origin: [34, 100], scale: 1,
    init: { g: 0 },
    steps: [
      { label: "沒有阻尼 $\\gamma=0$", caption: "$b=0$：特徵根 $\\pm i$，$x=x_0\\cos\\omega_0t$，永遠以同樣的振幅來回（板書右上角白色那條）。", set: { g: 0 }, dur: 400, hold: 2200 },
      { label: "欠阻尼 $\\gamma\\lt\\omega_0$", caption: "共軛複根 $-\\gamma\\pm i\\omega$：仍然振盪，但振幅被包絡 $\\pm e^{-\\gamma t}$（虛線）壓下來，角頻率 $\\omega=\\sqrt{\\omega_0^2-\\gamma^2}$ 也變小。", to: { g: 0.2 }, dur: 2200, hold: 2400 },
      { label: "臨界阻尼 $\\gamma=\\omega_0$", caption: "重根 $-\\gamma$：$x=x_0(1+\\gamma t)e^{-\\gamma t}$。剛好不振盪，是「不越過平衡點」中回得最快的。", to: { g: 1 }, dur: 2600, hold: 2400 },
      { label: "過阻尼 $\\gamma\\gt\\omega_0$", caption: "兩個負實根：不振盪，但其中一根 $-\\gamma+\\sqrt{\\gamma^2-\\omega_0^2}$ 很接近 0，衰減很慢——阻尼太大反而回得慢。", to: { g: 3 }, dur: 2600, hold: 2600 }
    ],
    draw: function (d, s) {
      var X = function (t) { return t * SX; }, Y = function (x) { return x * SY; };
      d.arrow([0, 0], [X(TMAX) + 8, 0], { color: MUTED, width: 1.4, head: 8 });
      d.arrow([0, Y(-1.25)], [0, Y(1.3)], { color: MUTED, width: 1.4, head: 8 });
      d.label([X(TMAX) + 4, -14], "t", { color: MUTED, size: 13 });
      d.label([-14, Y(1.3)], "x", { color: MUTED, size: 13 });
      d.line([-4, Y(1)], [4, Y(1)], { color: MUTED, width: 1.2 });
      d.label([-20, Y(1)], "x_0", { color: MUTED, size: 12 });
      var ref = [], cur = [], up = [], dn = [];
      for (var i = 0; i <= 260; i++) {
        var t = TMAX * i / 260;
        ref.push([X(t), Y(Math.cos(t))]);
        cur.push([X(t), Y(xt(s.g, t))]);
        if (s.g > 0.01 && s.g < 0.995) { up.push([X(t), Y(Math.exp(-s.g * t))]); dn.push([X(t), Y(-Math.exp(-s.g * t))]); }
      }
      d.path(ref, { color: MUTED, width: 1.2, dash: "4 5", opacity: s.g > 0.01 ? 0.8 : 0 });
      if (up.length) { d.path(up, { color: GREEN, width: 1.1, dash: "2 4" }); d.path(dn, { color: GREEN, width: 1.1, dash: "2 4" }); }
      var col = s.g < 0.01 ? INK : [GREEN, RED, BLUE][kind(s.g)];
      d.path(cur, { color: col, width: 2.6 });
      d.dot([0, Y(1)], { color: col, r: 4 });
    },
    formula: function (s) {
      var g = s.g;
      if (g < 0.01) return "\\gamma=0:\\ \\lambda=\\pm i";
      if (g < 0.995) return "\\gamma=" + F(g, 2) + ":\\ \\lambda=-" + F(g, 2) + "\\pm" + F(Math.sqrt(1 - g * g), 2) + "\\,i";
      if (g <= 1.005) return "\\gamma=\\omega_0=1:\\ \\lambda=-1\\ (\\text{重根})";
      var r = Math.sqrt(g * g - 1);
      return "\\gamma=" + F(g, 2) + ":\\ \\lambda=" + F(-g + r, 2) + ",\\ " + F(-g - r, 2);
    }
  });
})();
