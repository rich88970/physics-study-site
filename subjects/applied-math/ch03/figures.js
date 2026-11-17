/* 應用數學第 3 章（非齊次方程：待定係數法）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", MUTED = "var(--muted)", INK = "var(--ink)";

  /* ω0 = 1、F0 = 1 的穩態振幅 A(ω)（第 5 節 a3-b5） */
  function amp(g, w) { var d = 1 - w * w; return 1 / Math.sqrt(d * d + 4 * g * g * w * w); }

  /* ---------------- 共振曲線（照片 10） ---------------- */
  var SX = 150, SY = 30, WMAX = 2.5, AMAX = 5.6;
  A.define("a3-resonance", {
    title: "共振曲線：阻尼越小，峰越高越尖",
    question: "穩態振幅 $A(\\omega)$ 怎麼隨外力頻率變化？（$\\omega_0=1$、$F_0=1$）",
    view: [440, 205], origin: [40, 185], scale: 1,
    init: { g: 0.8 },
    steps: [
      { label: "大阻尼 $\\gamma=0.8$", caption: "$\\gamma\\gt\\omega_0/\\sqrt2$：沒有峰，$A$ 從靜態值 $F_0/\\omega_0^2=1$ 一路遞減。", set: { g: 0.8 }, dur: 400, hold: 2200 },
      { label: "$\\gamma=0.4$", caption: "峰出現在 $\\omega_r=\\sqrt{\\omega_0^2-2\\gamma^2}$，比 $\\omega_0$ 小一點。", to: { g: 0.4 }, dur: 2200, hold: 2200 },
      { label: "$\\gamma=0.2$", caption: "阻尼減半，峰高約加倍：$A_{\\max}\\approx\\dfrac{F_0}{2\\gamma\\omega_0}$。", to: { g: 0.2 }, dur: 2200, hold: 2200 },
      { label: "小阻尼 $\\gamma=0.09$", caption: "峰又高又窄，位置幾乎就在 $\\omega_0$（板書的圖）。$\\gamma\\to0$ 時峰高趨於無限大——無阻尼共振。", to: { g: 0.09 }, dur: 2400, hold: 2600 }
    ],
    draw: function (d, s) {
      var X = function (w) { return w * SX; }, Y = function (a) { return Math.min(a, AMAX) * SY; };
      d.arrow([0, 0], [X(WMAX) + 10, 0], { color: MUTED, width: 1.4, head: 8 });
      d.arrow([0, 0], [0, Y(AMAX) + 8], { color: MUTED, width: 1.4, head: 8 });
      d.label([X(WMAX) + 6, -14], "\\omega", { color: MUTED, size: 13 });
      d.label([-20, Y(AMAX) + 4], "A", { color: MUTED, size: 13 });
      d.line([X(1), 0], [X(1), Y(AMAX)], { color: MUTED, width: 1, dash: "4 5" });
      d.label([X(1), -14], "\\omega_0", { color: MUTED, size: 12 });
      d.line([-4, Y(1)], [4, Y(1)], { color: MUTED, width: 1.2 });
      d.label([-16, Y(1)], "1", { color: MUTED, size: 12 });
      var pts = [];
      for (var i = 0; i <= 300; i++) { var w = WMAX * i / 300; pts.push([X(w), Y(amp(s.g, w))]); }
      var col = s.g > 0.5 ? BLUE : (s.g > 0.15 ? GREEN : RED);
      d.path(pts, { color: col, width: 2.6 });
      if (2 * s.g * s.g < 1) {
        var wr = Math.sqrt(1 - 2 * s.g * s.g), am = amp(s.g, wr);
        if (am <= AMAX) d.dot([X(wr), Y(am)], { color: INK, r: 4 });
      }
    },
    formula: function (s) {
      var g = s.g;
      if (2 * g * g >= 1) return "\\gamma=" + F(g, 2) + ":\\ \\text{沒有峰}";
      var wr = Math.sqrt(1 - 2 * g * g);
      return "\\gamma=" + F(g, 2) + ":\\ \\omega_r=" + F(wr, 3) + ",\\ A_{\\max}=" + F(amp(g, wr), 2);
    }
  });
})();
