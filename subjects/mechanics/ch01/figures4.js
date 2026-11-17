/* 力學 Lecture 1 第四批圖解：講義 p.51–114（曲線座標、梯度、散度、旋度、Stokes 定理）。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt, rad = A.rad;
  function deg(x) { return F(x, 0) + "^\\circ"; }
  function add(u, v) { return [u[0] + v[0], u[1] + v[1], (u[2] || 0) + (v[2] || 0)]; }
  function mul(k, u) { return [k * u[0], k * u[1], k * (u[2] || 0)]; }
  function pol(r, t) { return [r * Math.cos(rad(t)), r * Math.sin(rad(t))]; }
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)", ORANGE = "var(--k-pit)", GRID = "var(--grid)";

  function arcPts(r, t0, t1, n) { var p = []; for (var i = 0; i <= (n || 24); i++) p.push(pol(r, t0 + (t1 - t0) * i / (n || 24))); return p; }

  /* ========== 10.2 極座標的面積元 ========== */
  A.define("polar-area", {
    title: "極座標的小面積 $\\mathrm dA=r\\,\\mathrm dr\\,\\mathrm d\\theta$",
    question: "同樣的 $\\mathrm dr$、$\\mathrm d\\theta$，離原點越遠面積為什麼越大？",
    view: [420, 300], origin: [60, 260], scale: 52,
    init: { r0: 2.4, edges: 0 },
    steps: [
      { label: "極座標格子", caption: "圓（$r$ 固定）和射線（$\\theta$ 固定）把平面切成小塊。橘色那一塊從 $r$ 到 $r+\\mathrm dr$、從 $\\theta$ 到 $\\theta+\\mathrm d\\theta$。", dur: 300, hold: 2200 },
      { label: "兩條邊", caption: "徑向的邊長 $\\mathrm dr$；圓弧的邊長是弧長 $r\\,\\mathrm d\\theta$——角度要乘上半徑才是長度。", set: { edges: 1 } },
      { label: "往外移", caption: "同一個 $\\mathrm d\\theta$，在 $r=4$ 處弧長變長，小塊面積跟著變大，所以 $\\mathrm dA$ 裡多一個 $r$。", to: { r0: 4 }, hold: 2800 }
    ],
    draw: function (d, s) {
      for (var r = 1; r <= 5; r++) d.path(arcPts(r, 0, 90), { color: GRID, width: 1 });
      for (var t = 0; t <= 90; t += 15) d.line([0, 0], pol(5.2, t), { color: GRID, width: 1 });
      d.axes([0, 6.6], [0, 4.6], ["x", "y"]);
      var dr = 0.6, t0 = 30, dt = 15, r0 = s.r0;
      var poly = arcPts(r0, t0, t0 + dt, 12).concat(arcPts(r0 + dr, t0 + dt, t0, 12));
      d.poly(poly, { color: ORANGE, width: 1.5, fill: ORANGE, fillOpacity: 0.35 });
      d.line([0, 0], pol(r0, t0), { color: MUTED, width: 1.2, dash: "4 3" });
      d.label(add(pol(r0 * 0.5, t0), [0.15, -0.25]), "r", { size: 13, color: MUTED });
      if (s.edges) {
        d.line(pol(r0, t0), pol(r0 + dr, t0), { color: RED, width: 3.5 });
        d.path(arcPts(r0, t0, t0 + dt, 12), { color: BLUE, width: 3.5 });
        d.label(add(pol(r0 + dr / 2, t0), [0.2, -0.3]), "\\mathrm dr", { size: 13, color: RED });
        d.label(add(pol(r0 - 0.5, t0 + dt / 2), [0, 0]), "r\\,\\mathrm d\\theta", { size: 13, color: BLUE });
      }
      d.arc([0, 0], 0.7, 0, t0, { color: MUTED, width: 1.2 });
      d.label(pol(1.0, t0 / 2), "\\theta", { size: 12, color: MUTED });
    },
    formula: function (s) {
      var dA = s.r0 * 0.6 * rad(15);
      return "\\mathrm dA\\approx r\\,\\mathrm dr\\,\\mathrm d\\theta=" + F(s.r0, 1) + "\\times0.6\\times" + F(rad(15), 3) + "=" + F(dA, 3);
    }
  });

  /* ========== 10.3 單位向量跟著轉 ========== */
  A.define("polar-unit", {
    title: "$\\hat r$、$\\hat\\theta$ 跟著粒子轉：$\\mathrm d\\hat r=\\mathrm d\\theta\\,\\hat\\theta$",
    question: "$\\hat r$ 的長度不變，它的改變量指向哪裡？",
    view: [420, 300], origin: [150, 150], scale: 46,
    init: { th: 30, ghost: 0, show: 0 },
    steps: [
      { label: "$\\hat r$ 與 $\\hat\\theta$", caption: "粒子在角度 $\\theta$。$\\hat r$（紅）向外，$\\hat\\theta$（藍）垂直 $\\hat r$、指向 $\\theta$ 增加的方向。", dur: 300, hold: 2200 },
      { label: "轉一個角度", caption: "粒子轉了 $\\Delta\\theta$（這裡放大成 $25^\\circ$）。虛線是轉之後的 $\\hat r$、$\\hat\\theta$，畫在同一點方便比較。", set: { ghost: 1 } },
      { label: "$\\Delta\\hat r$", caption: "$\\Delta\\hat r$（綠）連接兩個 $\\hat r$ 的尖端：長度約 $1\\cdot\\Delta\\theta$，方向約為 $\\hat\\theta$。所以 $\\dot{\\hat r}=\\dot\\theta\\,\\hat\\theta$。", set: { show: 1 } },
      { label: "$\\Delta\\hat\\theta$", caption: "$\\Delta\\hat\\theta$（紫）指向 $-\\hat r$，長度也約 $\\Delta\\theta$：$\\dot{\\hat\\theta}=-\\dot\\theta\\,\\hat r$。", set: { show: 2 } },
      { label: "粒子繼續走", caption: "粒子繞一圈，兩個單位向量也跟著轉一圈；直角座標的 $\\hat i,\\hat j$ 則永遠不動。", set: { ghost: 0, show: 0 }, to: { th: 150 }, dur: 2400, hold: 2200 }
    ],
    draw: function (d, s) {
      d.axes([-3, 4.6], [-2.8, 3]);
      d.path(arcPts(2.2, -10, 190, 40), { color: GRID, width: 1.2 });
      var P = pol(2.2, s.th), dth = 25;
      d.line([0, 0], P, { color: MUTED, width: 1, dash: "4 3" });
      d.dot(P, { color: INK, r: 4.5 });
      var rh = pol(1.4, s.th), thh = pol(1.4, s.th + 90);
      if (s.ghost) {
        var rh2 = pol(1.4, s.th + dth), th2 = pol(1.4, s.th + dth + 90);
        d.arrow(P, add(P, rh2), { color: RED, width: 2, dash: "5 4", opacity: 0.7 });
        d.arrow(P, add(P, th2), { color: BLUE, width: 2, dash: "5 4", opacity: 0.7 });
        if (s.show === 1) d.arrow(add(P, rh), add(P, rh2), { color: GREEN, width: 3 });
        if (s.show === 2) d.arrow(add(P, thh), add(P, th2), { color: PURPLE, width: 3 });
      }
      d.arrow(P, add(P, rh), { color: RED, width: 3 });
      d.arrow(P, add(P, thh), { color: BLUE, width: 3 });
      d.label(add(P, mul(1.25, rh)), "\\hat r", { color: RED });
      d.label(add(P, mul(1.22, thh)), "\\hat\\theta", { color: BLUE });
      d.arc([0, 0], 0.55, 0, s.th, { color: MUTED, width: 1.2 });
    },
    formula: function (s) {
      if (s._step === 2) return "|\\Delta\\hat r|=2\\sin\\tfrac{\\Delta\\theta}{2}\\approx\\Delta\\theta=" + F(rad(25), 3);
      if (s._step === 3) return "\\Delta\\hat\\theta\\approx-\\Delta\\theta\\,\\hat r";
      return "\\hat r=(\\cos\\theta,\\sin\\theta),\\ \\ \\hat\\theta=(-\\sin\\theta,\\cos\\theta),\\ \\ \\theta=" + deg(s.th);
    }
  });

  /* ========== 10.4 速度的兩個分量 ========== */
  A.define("polar-va", {
    title: "螺線上的速度：$\\vec v=\\dot r\\,\\hat r+r\\dot\\theta\\,\\hat\\theta$",
    question: "粒子越轉越外圈時，兩個速度分量怎麼變？",
    view: [420, 320], origin: [210, 160], scale: 34,
    init: { q: 1.2 },
    steps: [
      { label: "螺線", caption: "粒子沿 $r=1+0.4\\theta$ 走，$\\dot\\theta=1$ rad/s 固定。紅色是徑向分量 $\\dot r\\,\\hat r$，藍色是橫向（$\\hat\\theta$ 方向）分量 $r\\dot\\theta\\,\\hat\\theta$，綠色是合速度（沿軌跡的切線）。", dur: 300, hold: 2400 },
      { label: "往外走", caption: "$\\dot r=0.4$ 固定，但 $r$ 越來越大，橫向分量 $r\\dot\\theta$ 跟著變大——這就是加速度裡 $2\\dot r\\dot\\theta$ 那一項的來源之一。", to: { q: 6.4 }, dur: 4200, hold: 2600 }
    ],
    draw: function (d, s) {
      var pts = []; for (var i = 0; i <= 120; i++) { var q = 7 * i / 120; pts.push(pol(1 + 0.4 * q, q * 180 / Math.PI)); }
      d.path(pts, { color: GRID, width: 1.5 });
      d.line([-5.5, 0], [5.5, 0], { color: MUTED, width: 1 }); d.line([0, -4.5], [0, 4.5], { color: MUTED, width: 1 });
      var q = s.q, r = 1 + 0.4 * q, th = q * 180 / Math.PI, P = pol(r, th);
      var sc = 0.5, vr = mul(0.4 * sc, pol(1, th)), vt = mul(r * sc, pol(1, th + 90));
      d.line([0, 0], P, { color: MUTED, width: 1, dash: "4 3" });
      d.arrow(P, add(P, vr), { color: RED, width: 3, head: 9 });
      d.arrow(P, add(P, vt), { color: BLUE, width: 3, head: 9 });
      d.arrow(P, add(P, add(vr, vt)), { color: GREEN, width: 3 });
      d.dot(P, { color: INK, r: 4.5 });
    },
    formula: function (s) {
      var r = 1 + 0.4 * s.q;
      return "\\dot r=0.4,\\quad r\\dot\\theta=" + F(r) + ",\\quad v=\\sqrt{0.4^2+" + F(r) + "^2}=" + F(Math.sqrt(0.16 + r * r));
    }
  });

  /* ========== 11.2 球座標的體積元 ========== */
  function sph(r, t, p) { t = rad(t); p = rad(p); return [r * Math.sin(t) * Math.cos(p), r * Math.sin(t) * Math.sin(p), r * Math.cos(t)]; }
  A.define("sph-element", {
    title: "球座標：$\\mathrm dV=\\mathrm dr\\cdot r\\,\\mathrm d\\theta\\cdot r\\sin\\theta\\,\\mathrm d\\phi$",
    question: "$\\mathrm d\\phi$ 那條邊為什麼要乘 $r\\sin\\theta$？",
    view: [430, 340], origin: [200, 215], scale: 62,
    init: { stage: 0, az: 30 },
    steps: [
      { label: "$(r,\\theta,\\phi)$", caption: "$r$：到原點的距離；$\\theta$：和 $+z$ 軸的夾角；$\\phi$：投影到 $xy$ 平面後和 $+x$ 軸的夾角。", dur: 300, hold: 2400 },
      { label: "緯線圓", caption: "$\\phi$ 改變時，點沿著水平的緯線圓走。這個圓的半徑是點到 $z$ 軸的距離 $r\\sin\\theta$（橘），不是 $r$。", set: { stage: 1 }, to: { az: 36 } },
      { label: "三條邊", caption: "小體積的三條邊：$\\mathrm dr$（紅，沿 $\\hat r$）、$r\\,\\mathrm d\\theta$（藍，沿經線）、$r\\sin\\theta\\,\\mathrm d\\phi$（綠，沿緯線）。三者相乘就是 $\\mathrm dV$。", set: { stage: 2 }, to: { az: 42 }, hold: 3000 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 20);
      [[2.6, 0, 0], [0, 2.6, 0], [0, 0, 2.6]].forEach(function (e, i) {
        d.arrow3([0, 0, 0], e, { color: MUTED, width: 1.2, head: 8, opacity: 0.7 });
        d.label3(mul(1.08, e), ["x", "y", "z"][i], { color: MUTED, size: 12 });
      });
      var R = 2, T = 55, P0 = 110, P = sph(R, T, P0), foot = [P[0], P[1], 0];
      d.line3([0, 0, 0], P, { color: INK, width: 2 });
      d.line3(P, foot, { color: MUTED, width: 1, dash: "3 3" });
      d.line3([0, 0, 0], foot, { color: MUTED, width: 1, dash: "3 3" });
      var arcT = [], arcP = [];
      for (var i = 0; i <= 20; i++) { arcT.push(sph(0.7, T * i / 20, P0)); arcP.push(sph(0.8, 90, P0 * i / 20)); }
      d.path3(arcT, { color: INK, width: 1.4 }); d.path3(arcP, { color: INK, width: 1.4 });
      d.label3(sph(0.95, T / 2, P0), "\\theta", { size: 13 });
      d.label3(sph(1.05, 90, P0 / 2), "\\phi", { size: 13 });
      d.label3(sph(1.1, T, P0 + 12), "r", { size: 13 });
      d.dot3(P, { color: INK, r: 4 });
      if (s.stage >= 1) {
        var circ = []; for (var j = 0; j <= 48; j++) circ.push(sph(R, T, j * 7.5));
        d.path3(circ, { color: ORANGE, width: 1.5, dash: "5 4" });
        d.line3([0, 0, P[2]], P, { color: ORANGE, width: 2.5 });
        d.label3([P[0] / 2, P[1] / 2, P[2]], "r\\sin\\theta", { color: ORANGE, size: 12, dy: -14 });
      }
      if (s.stage >= 2) {
        d.arrow3(P, sph(R + 0.8, T, P0), { color: RED, width: 3, head: 8 });
        var lon = []; for (var k = 0; k <= 10; k++) lon.push(sph(R, T + 25 * k / 10, P0));
        d.path3(lon, { color: BLUE, width: 3.5 });
        var lat = []; for (var m = 0; m <= 10; m++) lat.push(sph(R, T, P0 + 35 * m / 10));
        d.path3(lat, { color: GREEN, width: 3.5 });
        d.label3(sph(R + 1.05, T, P0), "\\mathrm dr", { color: RED, size: 12 });
        d.label3(sph(R, T + 34, P0 - 4), "r\\,\\mathrm d\\theta", { color: BLUE, size: 12 });
        d.label3(sph(R + 0.35, T - 10, P0 + 40), "r\\sin\\theta\\,\\mathrm d\\phi", { color: GREEN, size: 12 });
      }
    },
    formula: function (s) {
      if (s.stage === 0) return "(r,\\theta,\\phi)=(2,\\ 55^\\circ,\\ 110^\\circ)";
      if (s.stage === 1) return "\\text{緯線圓半徑}=r\\sin\\theta=2\\sin55^\\circ=" + F(2 * Math.sin(rad(55)));
      return "\\mathrm dV=\\mathrm dr\\cdot r\\,\\mathrm d\\theta\\cdot r\\sin\\theta\\,\\mathrm d\\phi=r^2\\sin\\theta\\,\\mathrm dr\\,\\mathrm d\\theta\\,\\mathrm d\\phi";
    }
  });

  /* ========== 1-35 兩個垂直圓柱的切片 ========== */
  A.define("two-cylinders", {
    title: "課本 1-35：固定 $x$ 切一刀，截面是正方形",
    question: "切片的位置 $x$ 改變時，正方形的邊長怎麼變？",
    view: [430, 330], origin: [215, 175], scale: 62,
    init: { x0: 0, sq: 0, az: 35 },
    steps: [
      { label: "兩個圓柱", caption: "淺藍：$x^2+y^2=a^2$（軸是 $z$）；淺紅：$x^2+z^2=a^2$（軸是 $y$）。共同部分在兩者裡面。", dur: 300, hold: 2400 },
      { label: "$x=0$ 的切片", caption: "固定 $x$：第一個圓柱限制 $|y|\\le\\sqrt{a^2-x^2}$，第二個限制 $|z|\\le\\sqrt{a^2-x^2}$，截面是正方形。$x=0$ 時邊長 $2a$。", set: { sq: 1 } },
      { label: "移動切片", caption: "$x$ 越靠近 $\\pm a$，正方形越小，到 $x=a$ 縮成一點。把所有正方形面積 $4(a^2-x^2)$ 加起來就是體積。", to: { x0: 0.85 }, dur: 2600, hold: 2600 }
    ],
    draw: function (d, s) {
      d.camera(s.az, 22);
      var a = 1.4, i, pts1 = [], pts2 = [];
      [[2.4, 0, 0], [0, 2.4, 0], [0, 0, 2.2]].forEach(function (e, k) {
        d.arrow3(mul(-1, e), e, { color: MUTED, width: 1, head: 7, opacity: 0.6 });
        d.label3(mul(1.08, e), ["x", "y", "z"][k], { color: MUTED, size: 12 });
      });
      for (i = 0; i <= 40; i++) { var t = 2 * Math.PI * i / 40; pts1.push([a * Math.cos(t), a * Math.sin(t), 0]); pts2.push([a * Math.cos(t), 0, a * Math.sin(t)]); }
      [-1.6, 1.6].forEach(function (h) { d.path3(pts1.map(function (p) { return [p[0], p[1], h]; }), { color: BLUE, width: 1.2, opacity: 0.6 }); });
      [-1.6, 1.6].forEach(function (h) { d.path3(pts2.map(function (p) { return [p[0], h, p[2]]; }), { color: RED, width: 1.2, opacity: 0.6 }); });
      [0, 90, 180, 270].forEach(function (g) { var c = Math.cos(rad(g)), sn = Math.sin(rad(g));
        d.line3([a * c, a * sn, -1.6], [a * c, a * sn, 1.6], { color: BLUE, width: 1, opacity: 0.45 });
        d.line3([a * c, -1.6, a * sn], [a * c, 1.6, a * sn], { color: RED, width: 1, opacity: 0.45 }); });
      if (s.sq) {
        var x = s.x0 * a, h2 = Math.sqrt(Math.max(0, a * a - x * x));
        d.poly3([[x, -h2, -h2], [x, h2, -h2], [x, h2, h2], [x, -h2, h2]], { color: ORANGE, width: 2, fill: ORANGE, fillOpacity: 0.35 });
        d.label3([x, h2 + 0.3, h2 + 0.2], "2\\sqrt{a^2-x^2}", { color: ORANGE, size: 12 });
      }
    },
    formula: function (s) {
      if (!s.sq) return "x^2+y^2\\le a^2,\\qquad x^2+z^2\\le a^2";
      var x = s.x0;
      return "x=" + F(x) + "a:\\quad A(x)=4(a^2-x^2)=" + F(4 * (1 - x * x)) + "\\,a^2";
    }
  });

  /* ========== 12.2 梯度與等高線 ========== */
  function phiHill(x, y) { return -(x - 3) * (x - 3) - (y - 3) * (y - 3); }
  A.define("grad-contour", {
    title: "講義 p.82：$\\phi=-(x-3)^2-(y-3)^2$ 的等高線與梯度",
    question: "梯度箭頭和等高線之間是什麼關係？",
    view: [420, 320], origin: [40, 290], scale: 44,
    init: { pt: 0, field: 0 },
    steps: [
      { label: "等高線", caption: "同心圓是 $\\phi$ 相等的線，中心 $(3,3)$ 是山頂（$\\phi=0$）。", dur: 300, hold: 2200 },
      { label: "$(1,1)$", caption: "$\\nabla\\phi(1,1)=4\\hat i+4\\hat j$：垂直等高線、指向山頂（上坡最陡的方向）。", set: { pt: 1 } },
      { label: "$(1,3)$", caption: "$\\nabla\\phi(1,3)=4\\hat i$，同樣垂直於經過該點的等高線。", set: { pt: 2 } },
      { label: "整個場", caption: "每一點的梯度都指向山頂，離山頂越遠越長；在山頂 $(3,3)$ 梯度是 $\\vec 0$。力 $\\vec F=-\\nabla V$ 則全部反向。", set: { pt: 0, field: 1 }, hold: 3000 }
    ],
    draw: function (d, s) {
      [0.5, 1.5, 2.5].forEach(function (r) { var p = []; for (var i = 0; i <= 60; i++) p.push([3 + r * Math.cos(2 * Math.PI * i / 60), 3 + r * Math.sin(2 * Math.PI * i / 60)]); d.path(p, { color: GREEN, width: 1.3, opacity: 0.7 }); });
      d.axes([0, 6.6], [0, 6.2]);
      if (s.field) {
        for (var x = 0.5; x <= 6; x += 1) for (var y = 0.5; y <= 6; y += 1) {
          var g = [-2 * (x - 3), -2 * (y - 3)];
          d.arrow([x, y], [x + 0.12 * g[0], y + 0.12 * g[1]], { color: BLUE, width: 1.6, head: 6 });
        }
      }
      var P = [null, [1, 1], [1, 3]][s.pt];
      if (P) {
        var gg = [-2 * (P[0] - 3), -2 * (P[1] - 3)];
        d.arrow(P, [P[0] + 0.3 * gg[0], P[1] + 0.3 * gg[1]], { color: RED, width: 3.5 });
        d.dot(P, { color: INK, r: 4.5 });
        d.label([P[0] - 0.2, P[1] - 0.4], "(" + P[0] + "," + P[1] + ")", { size: 12 });
      }
      d.dot([3, 3], { color: INK, r: 3.5 });
    },
    formula: function (s) {
      var P = [null, [1, 1], [1, 3]][s.pt];
      if (!P) return "\\nabla\\phi=-2(x-3)\\,\\hat i-2(y-3)\\,\\hat j";
      return "\\nabla\\phi(" + P[0] + "," + P[1] + ")=" + (-2 * (P[0] - 3)) + "\\hat i+" + (-2 * (P[1] - 3)) + "\\hat j,\\quad \\phi=" + phiHill(P[0], P[1]);
    }
  });

  /* ========== 13.1 散度：方塊的淨通量 ========== */
  var DIVF = [
    { f: function (x, y) { return [0.5 * x, 0.5 * y]; }, tex: "\\vec f=\\tfrac12(x,y)", div: 1, cap: "往外發散：每個面都在流出，淨通量為正，$\\nabla\\cdot\\vec f=\\tfrac12+\\tfrac12=1$。" },
    { f: function (x, y) { return [-0.5 * x, -0.5 * y]; }, tex: "\\vec f=-\\tfrac12(x,y)", div: -1, cap: "往內匯集：每個面都在流入，$\\nabla\\cdot\\vec f=-1$。" },
    { f: function () { return [0.8, 0.4]; }, tex: "\\vec f=(0.8,\\ 0.4)", div: 0, cap: "均勻流動：左、下兩面流進多少，右、上兩面就流出多少，$\\nabla\\cdot\\vec f=0$。" },
    { f: function (x, y) { return [-0.5 * y, 0.5 * x]; }, tex: "\\vec f=\\tfrac12(-y,x)", div: 0, cap: "旋轉流動：沿著方塊繞圈，沒有淨流出，$\\nabla\\cdot\\vec f=0$（但下一節會看到它的旋度不是 0）。" }
  ];
  A.define("div-flux", {
    title: "散度 = 從小方塊淨流出的量 ÷ 體積",
    question: "哪些場會讓方塊有淨流出？",
    view: [400, 300], origin: [200, 150], scale: 40,
    init: { c: 0 },
    steps: DIVF.map(function (k, i) { return { label: ["發散", "匯集", "均勻", "旋轉"][i], caption: k.cap, set: { c: i }, dur: 300, hold: 2600 }; }),
    draw: function (d, s) {
      var k = DIVF[s.c];
      for (var x = -4; x <= 4; x += 1) for (var y = -3; y <= 3; y += 1) {
        if (Math.abs(x) <= 1 && Math.abs(y) <= 1) continue;
        var v = k.f(x, y);
        d.arrow([x, y], [x + 0.7 * v[0], y + 0.7 * v[1]], { color: MUTED, width: 1.3, head: 6, opacity: 0.7 });
      }
      d.rect(-1.2, -1.2, 1.2, 1.2, { color: INK, width: 1.5, fill: ORANGE, fillOpacity: 0.12 });
      [[1.2, 0, 1, 0], [-1.2, 0, -1, 0], [0, 1.2, 0, 1], [0, -1.2, 0, -1]].forEach(function (e) {
        var v = k.f(e[0], e[1]), out = v[0] * e[2] + v[1] * e[3];
        var col = out > 0.01 ? RED : out < -0.01 ? BLUE : MUTED;
        d.arrow([e[0], e[1]], [e[0] + 0.9 * v[0], e[1] + 0.9 * v[1]], { color: col, width: 3, head: 9 });
      });
    },
    formula: function (s) {
      var k = DIVF[s.c];
      return k.tex + ",\\qquad \\nabla\\cdot\\vec f=" + k.div;
    }
  });

  /* ========== 14.2 旋度：小水車轉不轉 ========== */
  var CURLF = [
    { f: function () { return [0, -0.8]; }, tex: "\\vec F=-c\\,\\hat j", w: 0, at: [1.5, 0.5], cap: "均勻向下：水車兩側受力相同，只平移不自轉，$\\nabla\\times\\vec F=0$。" },
    { f: function (x, y) { return [-0.35 * y, 0.35 * x]; }, tex: "\\vec F=-y\\,\\hat i+x\\,\\hat j", w: 1, at: [1.5, 0.5], cap: "旋轉場：放在任何位置（不只是原點）水車都逆時針自轉，$\\nabla\\times\\vec F=2\\hat k$。" },
    { f: function (x) { return [0, -0.15 * (x + 5)]; }, tex: "\\vec F=-(x+5)\\,\\hat j", w: -0.5, at: [1.5, 0.5], cap: "剪切流：箭頭都朝下、彼此平行，但右邊流得比左邊快，水車被扭成順時針轉，$\\nabla\\times\\vec F=-\\hat k$。" },
    { f: function (x, y) { var r2 = x * x + y * y; return [-2.2 * y / r2, 2.2 * x / r2]; }, tex: "\\vec F=\\tfrac{-y\\,\\hat i+x\\,\\hat j}{x^2+y^2}", w: 0, at: [1.5, 0.5], cap: "渦旋場：箭頭繞原點轉，但原點以外的水車不自轉。兩個效應互相抵消：流線繞圈會讓水車逆時針轉，內側快、外側慢的剪切會讓它順時針轉。旋度為 0。" }
  ];
  A.define("curl-paddle", {
    title: "旋度：在場裡放一個小水車",
    question: "箭頭在繞圈，水車就一定會轉嗎？",
    view: [400, 300], origin: [200, 150], scale: 40,
    init: { c: 0, t: 0 },
    steps: CURLF.map(function (k, i) { return { label: ["均勻", "旋轉", "剪切", "渦旋"][i], caption: k.cap, set: { c: i, t: 0 }, to: { t: 6 }, dur: 3600, hold: 1400 }; }),
    draw: function (d, s) {
      var k = CURLF[s.c];
      for (var x = -4; x <= 4; x += 1) for (var y = -3; y <= 3; y += 1) {
        if (x === 0 && y === 0 && s.c === 3) continue;
        var v = k.f(x, y);
        var L = Math.hypot(v[0], v[1]); if (L > 1.8) v = [v[0] * 1.8 / L, v[1] * 1.8 / L];
        d.arrow([x, y], [x + 0.75 * v[0], y + 0.75 * v[1]], { color: MUTED, width: 1.3, head: 6, opacity: 0.7 });
      }
      var C = k.at, ang = rad(40 * k.w * s.t);
      d.circle(C, 26, { color: ORANGE, width: 1.5, fill: ORANGE, fillOpacity: 0.12 });
      for (var j = 0; j < 4; j++) {
        var a2 = ang + j * Math.PI / 2;
        d.line(C, [C[0] + 0.62 * Math.cos(a2), C[1] + 0.62 * Math.sin(a2)], { color: ORANGE, width: 3.5 });
      }
      d.dot(C, { color: INK, r: 3 });
    },
    formula: function (s) {
      var k = CURLF[s.c];
      var c = ["0", "2\\hat k", "-\\hat k", "0\\ (x^2+y^2\\neq0)"][s.c];
      return k.tex + ",\\qquad \\nabla\\times\\vec F=" + c;
    }
  });

  /* ========== 15.1 Stokes 定理：內部的邊互相抵消 ========== */
  A.define("stokes-cells", {
    title: "Stokes 定理：小格子的環流量加起來，只剩邊界",
    question: "相鄰兩格共用的邊為什麼會抵消？",
    view: [400, 290], origin: [55, 250], scale: 48,
    init: { stage: 0 },
    steps: [
      { label: "切成小格", caption: "把曲面切成 $3\\times2$ 個小格，每一格都逆時針繞一圈。每一格的環流量 $=(\\nabla\\times\\vec V)\\cdot\\mathrm d\\vec\\sigma$。", dur: 300, hold: 2600 },
      { label: "內部抵消", caption: "相鄰兩格共用的邊，一格往上走、另一格往下走，兩個線積分正好抵消（變淡的邊）。", set: { stage: 1 } },
      { label: "只剩邊界", caption: "加總後只剩外圈的邊界 $C$，所以 $\\oint_C\\vec V\\cdot\\mathrm d\\vec\\lambda=\\int_S(\\nabla\\times\\vec V)\\cdot\\mathrm d\\vec\\sigma$。", set: { stage: 2 }, hold: 3000 }
    ],
    draw: function (d, s) {
      var W = 2.0, H = 2.0, nx = 3, ny = 2;
      for (var i = 0; i < nx; i++) for (var j = 0; j < ny; j++) {
        var x0 = 0.4 + i * W, y0 = 0.3 + j * H, g = 0.18;
        var c = [[x0 + g, y0 + g], [x0 + W - g, y0 + g], [x0 + W - g, y0 + H - g], [x0 + g, y0 + H - g]];
        for (var e = 0; e < 4; e++) {
          var p = c[e], q = c[(e + 1) % 4];
          var inner = (e === 1 && i < nx - 1) || (e === 3 && i > 0) || (e === 2 && j < ny - 1) || (e === 0 && j > 0);
          var op = s.stage >= 1 && inner ? 0.15 : 1;
          if (s.stage === 2 && inner) continue;
          d.arrow(p, [p[0] + 0.86 * (q[0] - p[0]), p[1] + 0.86 * (q[1] - p[1])], { color: inner ? BLUE : RED, width: 2.2, head: 8, opacity: op });
        }
      }
      if (s.stage === 2) d.rect(0.4, 0.3, 0.4 + nx * W, 0.3 + ny * H, { color: RED, width: 1.2, dash: "5 4" });
      d.label([0.4 + nx * W + 0.35, 0.3 + ny * H], "C", { color: RED });
    },
    formula: function (s) {
      if (s.stage === 0) return "\\sum_{\\text{格子}}\\oint_{\\text{小格}}\\vec V\\cdot\\mathrm d\\vec\\lambda=\\sum(\\nabla\\times\\vec V)\\cdot\\Delta\\vec\\sigma";
      if (s.stage === 1) return "\\text{共用邊}:\\ \\int_{\\uparrow}+\\int_{\\downarrow}=0";
      return "\\oint_C\\vec V\\cdot\\mathrm d\\vec\\lambda=\\int_S(\\nabla\\times\\vec V)\\cdot\\mathrm d\\vec\\sigma";
    }
  });
})();
