/* 應用數學第 4 章（冪級數解）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", MUTED = "var(--muted)", GRID = "var(--grid)";

  function fact(n) { var f = 1; for (var i = 2; i <= n; i++) f *= i; return f; }
  /* cos x 的部分和：前 m 個非零項 */
  function cosPartial(x, m) { var s = 0; for (var k = 0; k < m; k++) s += Math.pow(-1, k) * Math.pow(x, 2 * k) / fact(2 * k); return s; }
  /* 把曲線切成 |y| ≤ ymax 的幾段（部分和在遠處會衝出畫面） */
  function pieces(f, x0, x1, ymax) {
    var out = [], cur = [], n = 280;
    for (var i = 0; i <= n; i++) {
      var x = x0 + (x1 - x0) * i / n, y = f(x);
      if (Math.abs(y) <= ymax) cur.push([x, y]);
      else { if (cur.length > 1) out.push(cur); cur = []; }
    }
    if (cur.length > 1) out.push(cur);
    return out;
  }
  function termTex(k) {
    if (k === 0) return "1";
    return (k % 2 ? "-" : "+") + "\\tfrac{x^{" + (2 * k) + "}}{" + (2 * k) + "!}";
  }

  /* ---------------- 1. 部分和逼近 cos x（§2 板書例題 ω0=1、a0=1、a1=0） ---------------- */
  var TERMS = [1, 2, 3, 5, 8];
  A.define("am4-partial", {
    title: "偶次串的部分和逼近 $\\cos x$（$\\omega_0=1$、$a_0=1$、$a_1=0$）",
    question: "冪級數解是無窮多項；只取前幾項時，在多大範圍內可以用？",
    view: [440, 230], origin: [220, 120], scale: 29,
    init: { c: 0 },
    steps: [
      { label: "1 項", caption: "只取 $a_0=1$：$S_1=1$，只在 $x=0$ 附近像 $\\cos x$。", dur: 300, hold: 1800 },
      { label: "2 項", caption: "加上 $a_2x^2=-\\tfrac{x^2}{2}$：拋物線在 $|x|\\lesssim1$ 和 $\\cos x$ 幾乎重合。", set: { c: 1 }, dur: 300, hold: 1900 },
      { label: "3 項", caption: "再加 $a_4x^4=\\tfrac{x^4}{24}$：重合的範圍擴大到 $|x|\\lesssim2$。每多一項，重合範圍就往外推。", set: { c: 2 }, dur: 300, hold: 1900 },
      { label: "5 項", caption: "5 項（到 $x^8$）時，$|x|\\lesssim\\pi$ 都對得上：$S_5(\\pi)=-0.9760$，真值 $-1$。", set: { c: 3 }, dur: 300, hold: 2100 },
      { label: "8 項", caption: "8 項（到 $x^{14}$）已經覆蓋整個畫面。遞迴 $a_{n+2}=-\\dfrac{a_n}{(n+2)(n+1)}$ 讓係數越來越快趨近 0：收斂半徑 $R=\\infty$，這個方程式沒有奇點。", set: { c: 4 }, dur: 300, hold: 2600 }
    ],
    draw: function (d, s) {
      var X = 7.2, Y = 3.2, m = TERMS[s.c];
      d.line([-X, 0], [X, 0], { color: MUTED, width: 1.2 });
      d.line([0, -Y], [0, Y], { color: MUTED, width: 1.2 });
      [-2, -1, 1, 2].forEach(function (k) {
        var xx = k * Math.PI;
        d.line([xx, -0.12], [xx, 0.12], { color: MUTED, width: 1 });
        d.label([xx, -0.5], (k === 1 ? "" : k === -1 ? "-" : k) + "\\pi", { color: MUTED, size: 11 });
      });
      [-1, 1].forEach(function (v) {
        d.line([-X, v], [X, v], { color: GRID, width: 1, dash: "3 4" });
        d.label([-X + 0.3, v + (v > 0 ? 0.3 : -0.3)], F(v, 0), { color: MUTED, size: 11 });
      });
      pieces(Math.cos, -X, X, Y).forEach(function (seg) { d.path(seg, { color: MUTED, width: 2, dash: "6 5" }); });
      pieces(function (x) { return cosPartial(x, m); }, -X, X, Y).forEach(function (seg) { d.path(seg, { color: BLUE, width: 2.6 }); });
      d.label([1.6, -2.25], "S_{" + m + "}(x)", { color: BLUE, size: 13 });
      d.label([1.6, -2.85], "\\cos x", { color: MUTED, size: 13 });
    },
    formula: function (s) {
      var m = TERMS[s.c], parts = [], k;
      var shown = m > 4 ? 3 : m;
      for (k = 0; k < shown; k++) parts.push(termTex(k));
      var tail = m > 4 ? "+\\cdots" + termTex(m - 1) : "";
      return "S_{" + m + "}(x)=" + parts.join("") + tail + "\\\\ S_{" + m + "}(\\pi)=" + F(cosPartial(Math.PI, m), 4) + "\\quad(\\cos\\pi=-1)";
    }
  });

  /* ---------------- 2. 收斂半徑：到最近奇點的距離（§1、§4） ---------------- */
  var CASES = [
    { name: "(x^2+1)y''-2xy'+2y=0", x0: 0, sing: [[0, 1, "i"], [0, -1, "-i"]], Rtex: "|0-(\\pm i)|=1" },
    { name: "(x-1)y''-xy'+y=0", x0: 0, sing: [[1, 0, "1"]], Rtex: "|0-1|=1" },
    { name: "(x^2-2x+5)y''+xy'-y=0", x0: 0, sing: [[1, 2, "1+2i"], [1, -2, "1-2i"]], Rtex: "|0-(1\\pm2i)|=\\sqrt5\\approx2.24" },
    { name: "(x^2-2x+5)y''+xy'-y=0", x0: 1, sing: [[1, 2, "1+2i"], [1, -2, "1-2i"]], Rtex: "|1-(1\\pm2i)|=2" },
    { name: "x^2(x-2)^2y''+3xy'+(x-2)y=0", x0: 1, sing: [[0, 0, "0"], [2, 0, "2"]], Rtex: "\\min(|1-0|,|1-2|)=1" }
  ];
  A.define("am4-radius", {
    title: "收斂半徑至少是展開點到最近奇點的距離（複數平面）",
    question: "係數都是實數，為什麼收斂範圍要看複數平面上的奇點？",
    view: [440, 300], origin: [190, 150], scale: 50,
    init: { c: 0, r: 0 },
    steps: [
      { label: "$\\pm i$", caption: "111 上期末 3：$x^2+1=0$ 在實數線上沒有根，奇點在 $\\pm i$。從 $x_0=0$ 畫圓，碰到 $\\pm i$ 就停：保證 $R\\ge1$。", to: { r: 1 }, dur: 900, hold: 2200 },
      { label: "$x=1$", caption: "作業 3：首項係數 $x-1$ 在 $x=1$ 為零，從 $x_0=0$ 出發距離 1，保證 $|x|\\lt1$ 收斂（這題的解 $8x-2e^x$ 其實處處收斂——定理只給下限）。", set: { c: 1, r: 0 }, to: { r: 1 }, dur: 900, hold: 2400 },
      { label: "$1\\pm2i$", caption: "自編 1-a：分母 $x^2-2x+5$ 在實數線上恆正，奇點卻在 $1\\pm2i$。從 $x_0=0$ 到它們的距離是 $\\sqrt{1^2+2^2}=\\sqrt5$。", set: { c: 2, r: 0 }, to: { r: Math.sqrt(5) }, dur: 900, hold: 2400 },
      { label: "$x_0=1$", caption: "同一題改在 $x_0=1$ 展開：正好在兩個奇點的正中間，距離縮成 2——展開點不同，保證的半徑也不同。", set: { c: 3, r: 0 }, to: { r: 2 }, dur: 900, hold: 2400 },
      { label: "實數奇點", caption: "自編 1-b：奇點 $x=0$（正則）與 $x=2$（不正則）。從 $x_0=1$ 出發兩邊都是 1：保證 $R\\ge1$。", set: { c: 4, r: 0 }, to: { r: 1 }, dur: 900, hold: 2600 }
    ],
    draw: function (d, s) {
      var cs = CASES[s.c];
      d.grid(-3.6, 4.6, -2.8, 2.8);
      d.arrow([-3.6, 0], [4.7, 0], { color: MUTED, width: 1.4, head: 9 });
      d.arrow([0, -2.8], [0, 2.85], { color: MUTED, width: 1.4, head: 9 });
      d.label([4.45, -0.32], "\\mathrm{Re}\\,x", { color: MUTED, size: 12 });
      d.label([0.6, 2.62], "\\mathrm{Im}\\,x", { color: MUTED, size: 12 });
      if (s.r > 0.02) d.circle([cs.x0, 0], s.r * 50, { color: BLUE, width: 2, fill: BLUE, fillOpacity: 0.08, dash: "6 4" });
      d.dot([cs.x0, 0], { color: BLUE, r: 5 });
      d.label([cs.x0 + 0.05, -0.4], "x_0=" + cs.x0, { color: BLUE, size: 12 });
      cs.sing.forEach(function (p) {
        d.line([p[0] - 0.13, p[1] - 0.13], [p[0] + 0.13, p[1] + 0.13], { color: RED, width: 2.6 });
        d.line([p[0] - 0.13, p[1] + 0.13], [p[0] + 0.13, p[1] - 0.13], { color: RED, width: 2.6 });
        d.label([p[0] + 0.55, p[1] + (p[1] >= 0 ? 0.3 : -0.3)], p[2], { color: RED, size: 12 });
      });
      if (s.r > 0.02) {
        var p0 = cs.sing[0], dx = p0[0] - cs.x0, dy = p0[1], L = Math.sqrt(dx * dx + dy * dy) || 1;
        d.arrow([cs.x0, 0], [cs.x0 + s.r * dx / L, s.r * dy / L], { color: GREEN, width: 2, head: 9 });
      }
    },
    formula: function (s) {
      var cs = CASES[s.c];
      return cs.name + "\\\\ R\\ \\ge\\ " + cs.Rtex;
    }
  });
})();
