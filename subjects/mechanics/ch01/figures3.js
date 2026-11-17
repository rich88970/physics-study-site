/* 力學 Lecture 1 第三批圖解：考前補充的課本題與課本例題（1-18、1-19、1-24、§1.7 連續旋轉）。 */
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
  function angOf(u) { return Math.atan2(u[1], u[0]) * 180 / Math.PI; }
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)", ORANGE = "var(--k-pit)";

  /* 指向紙面內（⊗）或紙面外（⊙）的小符號 */
  function outOfPage(d, p, into, color) {
    d.circle(p, 9, { color: color, width: 1.6 });
    if (into) {
      var k = 6 / d.k;
      d.line([p[0] - k, p[1] - k], [p[0] + k, p[1] + k], { color: color, width: 1.6 });
      d.line([p[0] - k, p[1] + k], [p[0] + k, p[1] - k], { color: color, width: 1.6 });
    } else d.dot(p, { color: color, r: 3 });
  }

  /* ========== 1-18 正弦定律：任兩邊的外積長度都是 2 倍面積 ========== */
  var SA = [4, 0], SB = [1.4, 2.6], SC = sub(SA, SB);
  /* 內角：O 在 A、B 之間；P 在 PO（180°）與 PQ=-C 之間；Q 用三角形內角和 */
  function sineAngles() {
    var tO = angOf(SB), pq = angOf(mul(-1, SC)), tP = Math.abs(180 - pq);
    return { O: tO, P: tP, Q: 180 - tO - tP, pq: pq };
  }
  A.define("sine-law", {
    title: "課本 1-18：三角形任兩邊的外積長度都相等",
    question: "挑哪兩邊做外積，長度為什麼都一樣？",
    view: [440, 300], origin: [165, 150], scale: 50,
    init: { pg: 0 },
    steps: [
      { label: "三角形", caption: "$\\vec A$（紅）、$\\vec B$（藍）從 $O$ 出發，第三邊 $\\vec C=\\vec A-\\vec B$（綠）從 $Q$ 指向 $P$。三個內角 $\\theta_O,\\theta_P,\\theta_Q$ 的對邊分別是 $C,B,A$。", dur: 300, hold: 2600 },
      { label: "$|\\vec A\\times\\vec B|$", caption: "$|\\vec A\\times\\vec B|=AB\\sin\\theta_O$ 是 $\\vec A,\\vec B$ 張成的平行四邊形面積——三角形面積的 2 倍。", set: { pg: 1 } },
      { label: "$|\\vec C\\times\\vec B|$", caption: "在 $Q$ 用邊 $C$ 和 $B$ 張平行四邊形：面積 $CB\\sin\\theta_Q$。它也是同一個三角形拼兩次，所以面積一樣。", set: { pg: 2 } },
      { label: "$|\\vec A\\times\\vec C|$", caption: "在 $P$ 用邊 $A$ 和 $C$：面積 $AC\\sin\\theta_P$。三個面積相等，除以 $ABC$ 就是正弦定律。", set: { pg: 3 }, hold: 3200 }
    ],
    draw: function (d, s) {
      var t = sineAngles(), P = SA, Q = SB, O = [0, 0];
      var par = [null, [O, SA, add(SA, SB), SB], [Q, P, sub(SA, SB), O], [P, O, sub(SB, SA), Q]][s.pg];
      if (par) d.poly(par, { color: ORANGE, width: 1.2, dash: "5 4", fill: ORANGE, fillOpacity: 0.12 });
      d.poly([O, P, Q], { color: "none", fill: GREEN, fillOpacity: 0.08 });
      d.arc(O, 0.55, 0, t.O, { color: MUTED, width: 1.4 });
      d.arc(P, 0.6, t.pq, 180, { color: MUTED, width: 1.4 });
      d.arc(Q, 0.5, 180 + t.O, 360 + angOf(SC), { color: MUTED, width: 1.4 });
      d.label([0.85 * Math.cos(rad(t.O / 2)), 0.85 * Math.sin(rad(t.O / 2))], "\\theta_O", { size: 12, color: MUTED });
      d.label(add(P, [-1.0, 0.25]), "\\theta_P", { size: 12, color: MUTED });
      d.label(add(Q, [0.05, -0.75]), "\\theta_Q", { size: 12, color: MUTED });
      d.arrow(O, SA, { color: RED, width: 3 });
      d.arrow(O, SB, { color: BLUE, width: 3 });
      d.arrow(Q, P, { color: GREEN, width: 3 });
      d.label([2, -0.32], "\\vec A", { color: RED });
      d.label([0.35, 1.55], "\\vec B", { color: BLUE });
      d.label(add(mul(0.5, add(P, Q)), [0.4, 0.3]), "\\vec C", { color: GREEN });
      d.label([-0.25, -0.25], "O", { size: 13 });
      d.label(add(P, [0.3, -0.2]), "P", { size: 13 });
      d.label(add(Q, [-0.1, 0.32]), "Q", { size: 13 });
    },
    formula: function (s) {
      var t = sineAngles(), a = len(SA), b = len(SB), c = len(SC);
      var area2 = Math.abs(SA[0] * SB[1] - SA[1] * SB[0]);
      switch (s.pg) {
        case 0: return "\\theta_O=" + deg(t.O) + ",\\ \\ \\theta_P=" + deg(t.P) + ",\\ \\ \\theta_Q=" + deg(t.Q);
        case 1: return "|\\vec A\\times\\vec B|=AB\\sin\\theta_O=" + F(a) + "\\times" + F(b) + "\\times" + F(Math.sin(rad(t.O))) + "=" + F(area2);
        case 2: return "|\\vec C\\times\\vec B|=CB\\sin\\theta_Q=" + F(c) + "\\times" + F(b) + "\\times" + F(Math.sin(rad(t.Q))) + "=" + F(area2);
        default: return "\\begin{gathered}|\\vec A\\times\\vec C|=AC\\sin\\theta_P=" + F(area2) + "\\\\ \\frac{\\sin\\theta_O}{C}=\\frac{\\sin\\theta_P}{B}=\\frac{\\sin\\theta_Q}{A}=" + F(area2 / (a * b * c), 3) + "\\end{gathered}";
      }
    }
  });

  /* ========== 1-19 和差角：內積給 cos，外積給 sin ========== */
  A.define("angle-diff", {
    title: "課本 1-19：兩個單位向量的夾角是 $\\alpha-\\beta$",
    question: "$\\cos(\\alpha-\\beta)$ 和 $\\sin(\\alpha-\\beta)$ 在圖上各是哪一段？",
    view: [400, 300], origin: [150, 175], scale: 110,
    init: { al: 70, be: 25, proj: 0, perp: 0 },
    steps: [
      { label: "兩個單位向量", caption: "$\\hat a$ 與 $x$ 軸夾 $\\alpha$，$\\hat b$ 夾 $\\beta$，兩者之間的角就是 $\\alpha-\\beta$。", dur: 300, hold: 2400 },
      { label: "內積", caption: "$\\hat a$ 在 $\\hat b$ 方向的投影長 $=\\hat a\\cdot\\hat b=\\cos(\\alpha-\\beta)$；用分量算是 $\\cos\\alpha\\cos\\beta+\\sin\\alpha\\sin\\beta$。", set: { proj: 1 } },
      { label: "外積", caption: "$\\hat a$ 到 $\\hat b$ 直線的垂直距離 $=\\sin(\\alpha-\\beta)$。從 $\\hat b$ 逆時針轉到 $\\hat a$，所以 $\\hat b\\times\\hat a$ 指出紙面（$+\\hat k$）。", set: { perp: 1 } },
      { label: "換角度", caption: "$\\alpha$ 改成 $140^\\circ$，兩個等式仍然成立——公式對任何角度都對。", to: { al: 140 }, hold: 3000 }
    ],
    draw: function (d, s) {
      d.axes([-1.25, 1.25], [-0.6, 1.3]);
      d.arc([0, 0], 1, -10, 190, { color: "var(--grid)", width: 1.2 });
      var a = [Math.cos(rad(s.al)), Math.sin(rad(s.al))], b = [Math.cos(rad(s.be)), Math.sin(rad(s.be))];
      var c = dot(a, b), foot = mul(c, b);
      d.line([0, 0], mul(1.25, b), { color: BLUE, width: 1, dash: "4 4" });
      if (s.proj) { d.line([0, 0], foot, { color: GREEN, width: 5, opacity: 0.6 }); d.line(a, foot, { color: MUTED, width: 1.2, dash: "3 3" }); }
      if (s.perp) {
        d.line(foot, a, { color: PURPLE, width: 4, opacity: 0.75 });
        d.rightAngle(foot, mul(-1, b), [-b[1], b[0]], 0.08);
        outOfPage(d, [0.95, 1.12], false, PURPLE);
        d.label([1.1, 1.12], "\\hat b\\times\\hat a", { size: 12, color: PURPLE, dx: 22 });
      }
      d.arc([0, 0], 0.3, s.be, s.al, { color: INK, width: 1.5 });
      d.label(mul(0.45, [Math.cos(rad((s.al + s.be) / 2)), Math.sin(rad((s.al + s.be) / 2))]), "\\alpha-\\beta", { size: 12 });
      d.arrow([0, 0], a, { color: RED, width: 3 });
      d.arrow([0, 0], b, { color: BLUE, width: 3 });
      d.label(mul(1.13, a), "\\hat a", { color: RED });
      d.label(mul(1.13, b), "\\hat b", { color: BLUE });
    },
    formula: function (s) {
      var dlt = s.al - s.be, ca = Math.cos(rad(s.al)), sa = Math.sin(rad(s.al)), cb = Math.cos(rad(s.be)), sb = Math.sin(rad(s.be));
      var l1 = "\\cos" + deg(dlt) + "=" + F(ca * cb + sa * sb, 3);
      var l2 = "\\sin" + deg(dlt) + "=" + F(sa * cb - ca * sb, 3);
      if (!s.proj) return "\\alpha=" + deg(s.al) + ",\\quad \\beta=" + deg(s.be) + ",\\quad \\alpha-\\beta=" + deg(dlt);
      if (!s.perp) return "\\hat a\\cdot\\hat b:\\ " + l1;
      return "\\begin{gathered}\\hat a\\cdot\\hat b:\\ " + l1 + "\\\\ (\\hat b\\times\\hat a)_3:\\ " + l2 + "\\end{gathered}";
    }
  });

  /* ========== 1-24 把向量拆成平行、垂直 ê 的兩部分 ========== */
  A.define("decompose-e", {
    title: "課本 1-24：$\\vec A=\\hat e(\\vec A\\cdot\\hat e)+\\hat e\\times(\\vec A\\times\\hat e)$",
    question: "兩次外積為什麼會回到紙面上、而且剛好垂直 $\\hat e$？",
    view: [420, 280], origin: [150, 200], scale: 55,
    init: { th: 55, par: 0, ax: 0, perp: 0 },
    steps: [
      { label: "$\\vec A$ 與 $\\hat e$", caption: "$\\hat e$（綠）是固定方向的單位向量，$\\vec A$（紅）任意，兩者夾 $\\theta$。", dur: 300, hold: 2400 },
      { label: "平行部分", caption: "$\\hat e(\\vec A\\cdot\\hat e)$：沿 $\\hat e$、長度 $A\\cos\\theta$（藍）——就是 $\\vec A$ 的投影。", set: { par: 1 } },
      { label: "$\\vec A\\times\\hat e$", caption: "$\\vec A\\times\\hat e$ 同時垂直 $\\vec A$ 和 $\\hat e$，所以垂直紙面（$\\otimes$ 指入紙面），長度 $A\\sin\\theta$。", set: { ax: 1 } },
      { label: "再叉一次 $\\hat e$", caption: "$\\hat e\\times(\\vec A\\times\\hat e)$ 垂直紙面上的那個向量，所以回到紙面；又垂直 $\\hat e$，長度 $A\\sin\\theta$——正好是 $\\vec A$ 的垂直部分（紫）。", set: { perp: 1 } },
      { label: "鈍角也對", caption: "$\\theta\\gt90^\\circ$ 時 $\\vec A\\cdot\\hat e\\lt0$，平行部分反向，兩部分相加仍是 $\\vec A$。", to: { th: 130 }, hold: 3000 }
    ],
    draw: function (d, s) {
      var L = 3, a = [L * Math.cos(rad(s.th)), L * Math.sin(rad(s.th))], par = [a[0], 0];
      d.line([-2.3, 0], [4.3, 0], { color: GREEN, width: 1, dash: "4 4" });
      if (s.par) d.arrow([0, 0], par, { color: BLUE, width: 4, opacity: 0.85 });
      if (s.perp) { d.arrow(par, a, { color: PURPLE, width: 4, opacity: 0.85 }); d.rightAngle(par, [a[0] >= 0 ? -1 : 1, 0], [0, 1], 0.22); }
      else if (s.par) d.line(a, par, { color: MUTED, width: 1.2, dash: "3 3" });
      d.arc([0, 0], 0.6, 0, s.th, { color: MUTED, width: 1.4 });
      d.label([0.9 * Math.cos(rad(s.th / 2)), 0.9 * Math.sin(rad(s.th / 2))], "\\theta", { size: 13, color: MUTED });
      d.arrow([0, 0], [1, 0], { color: GREEN, width: 3.5 });
      d.arrow([0, 0], a, { color: RED, width: 3 });
      d.label([1, -0.32], "\\hat e", { color: GREEN });
      d.label(add(mul(1.08, a), [0, 0.2]), "\\vec A", { color: RED });
      if (s.par) d.label([par[0] / 2, -0.62], "\\hat e(\\vec A\\cdot\\hat e)", { color: BLUE, size: 12 });
      if (s.perp) d.label([par[0] + 0.25, a[1] / 2], "\\hat e\\times(\\vec A\\times\\hat e)", { color: PURPLE, size: 12, dx: 58 });
      if (s.ax) { outOfPage(d, [-1.4, 2.6], true, ORANGE); d.label([-1.4, 3.15], "\\vec A\\times\\hat e", { color: ORANGE, size: 12 }); }
    },
    formula: function (s) {
      var c = 3 * Math.cos(rad(s.th)), sn = 3 * Math.sin(rad(s.th));
      if (!s.par) return "A=3,\\quad \\theta=" + deg(s.th);
      if (!s.ax) return "\\vec A\\cdot\\hat e=A\\cos\\theta=" + F(c);
      if (!s.perp) return "\\vec A\\times\\hat e=-A\\sin\\theta\\,\\hat k=" + F(-sn) + "\\,\\hat k";
      return "\\begin{gathered}\\hat e\\times(\\vec A\\times\\hat e)=\\vec A-\\hat e(\\vec A\\cdot\\hat e)\\\\ =(" + F(c) + "," + F(sn) + ")-(" + F(c) + ",0)=(0," + F(sn) + ")\\end{gathered}";
    }
  });

  /* ========== 課本 §1.7 連續兩次旋轉：次序不同、結果不同 ========== */
  function rotv(v, n, ang) {
    var c = Math.cos(ang), s = Math.sin(ang), k = dot(n, v);
    return add(add(mul(c, v), mul(s, cross(n, v))), mul(k * (1 - c), n));
  }
  var E = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
  function frame(s) {
    var first = s.order ? E[0] : E[2];
    var f = E.map(function (e) { return rotv(e, first, rad(90 * s.p1)); });
    var second = s.order ? f[2] : f[0];
    return f.map(function (e) { return rotv(e, second, rad(90 * s.p2)); });
  }
  function matTex(rows) { return "\\begin{bmatrix}" + rows.map(function (r) { return r.join("&"); }).join("\\\\") + "\\end{bmatrix}"; }
  A.define("rot-seq", {
    title: "課本 §1.7：先轉 $x_3$ 再轉 $x_1'$，和反過來做不一樣",
    question: "兩次 $90^\\circ$ 旋轉對調次序，盒子最後的方向一樣嗎？",
    view: [430, 330], origin: [215, 200], scale: 86,
    init: { order: 0, p1: 0, p2: 0, az: 32 },
    steps: [
      { label: "原來的軸", caption: "灰色是固定的舊軸，彩色是跟著盒子一起轉的座標軸，現在兩組重合。", dur: 300, hold: 2000 },
      { label: "$\\lambda_1$：繞 $x_3$", caption: "繞 $x_3$ 逆時針轉 $90^\\circ$：新的 $x_1'$（紅）轉到舊的 $x_2$，$x_2'$（藍）轉到舊的 $-x_1$。", dur: 1800, to: { p1: 1 } },
      { label: "$\\lambda_2$：繞新 $x_1'$", caption: "再繞「新的」$x_1'$ 轉 $90^\\circ$：最後 $x_1''=x_2$、$x_2''=x_3$、$x_3''=x_1$。這和 1-3 繞 $(1,1,1)$ 轉 $120^\\circ$ 完全相同。", dur: 1800, to: { p2: 1 }, hold: 3200 },
      { label: "對調：先繞 $x_1$", caption: "回到原位，這次先繞 $x_1$ 轉 $90^\\circ$（$\\lambda_2$ 先做）。", set: { order: 1, p1: 0, p2: 0 }, dur: 1800, to: { p1: 1 } },
      { label: "再繞新 $x_3'$", caption: "再繞新的 $x_3'$ 轉 $90^\\circ$：最後 $x_1''=x_3$、$x_2''=-x_1$、$x_3''=-x_2$，和第一種次序不同。", dur: 1800, to: { p2: 1 }, hold: 3600 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 22);
      var names = ["x_1", "x_2", "x_3"];
      E.forEach(function (e, i) {
        d.arrow3([0, 0, 0], mul(1.75, e), { color: MUTED, width: 1.2, head: 8, opacity: 0.6 });
        d.label3(mul(1.95, e), names[i], { color: MUTED, size: 12 });
      });
      var f = frame(s), dims = [1.1, 0.7, 0.35];
      var corner = function (i, j, k) { return add(add(mul(i * dims[0], f[0]), mul(j * dims[1], f[1])), mul(k * dims[2], f[2])); };
      [[0, 0, 0, 1, 0, 0], [0, 1, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1], [0, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1],
       [0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 1], [0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 1, 1]].forEach(function (q) {
        d.line3(corner(q[0], q[1], q[2]), corner(q[3], q[4], q[5]), { color: INK, width: 1, opacity: 0.35 });
      });
      d.poly3([corner(0, 0, 1), corner(1, 0, 1), corner(1, 1, 1), corner(0, 1, 1)], { color: "none", fill: ORANGE, fillOpacity: 0.16 });
      var rotating = s.p2 > 0 ? (s.order ? f[2] : f[0]) : (s.order ? E[0] : E[2]);
      if ((s.p1 > 0 && s.p1 < 1) || (s.p2 > 0 && s.p2 < 1)) d.line3(mul(-1.4, rotating), mul(1.4, rotating), { color: ORANGE, width: 2, dash: "6 4" });
      var mark = s.p2 > 0 ? "''" : s.p1 > 0 ? "'" : "";
      [RED, BLUE, GREEN].forEach(function (col, i) {
        d.arrow3([0, 0, 0], mul(1.35, f[i]), { color: col, width: 3 });
        d.label3(mul(1.55, f[i]), "x_" + (i + 1) + mark, { color: col, size: 13 });
      });
    },
    formula: function (s) {
      var l1 = matTex([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]), l2 = matTex([[1, 0, 0], [0, 0, 1], [0, -1, 0]]);
      switch (s._step) {
        case 0: return "\\lambda_1=" + l1 + ",\\quad \\lambda_2=" + l2;
        case 1: return "\\vec x'=\\lambda_1\\vec x,\\quad \\lambda_1=" + l1;
        case 2: return "\\lambda_3=\\lambda_2\\lambda_1=" + matTex([[0, 1, 0], [0, 0, 1], [1, 0, 0]]);
        case 3: return "\\vec x'=\\lambda_2\\vec x,\\quad \\lambda_2=" + l2;
        default: return "\\lambda_4=\\lambda_1\\lambda_2=" + matTex([[0, 0, 1], [-1, 0, 0], [0, -1, 0]]) + "\\neq\\lambda_3";
      }
    }
  });
})();
