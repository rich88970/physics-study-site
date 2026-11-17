/* 範例動畫：一個點沿 x 軸移動，旁邊公式同步顯示目前位置。複製後改名並修改。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  A.define("example", {
    title: "範例：點從 $x=0$ 走到 $x=3$",
    question: "這張圖要回答的問題",
    view: [420, 160], origin: [40, 100], scale: 100,
    init: { x: 0 },
    steps: [
      { label: "起點", caption: "點在 $x=0$。", dur: 300, hold: 1500 },
      { label: "移動", caption: "點移動到 $x=3$。", to: { x: 3 } }
    ],
    draw: function (d, s) {
      d.arrow([0, 0], [3.5, 0], { color: "var(--muted)", width: 1.5 });
      d.dot([s.x, 0], { r: 6, color: "var(--a)" });
      d.label([s.x, 0.3], "P", { color: "var(--a)" });
    },
    formula: function (s) { return "x=" + F(s.x); }
  });
})();
