/* 熱學第 1 章（Schroeder, Energy in Thermal Physics）的連續圖解。由 tools/merge_parts_thermal_ch01.py 從片段合併產生，請改 tools/parts/thermal-ch01/figures-*.js。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)", GRID = "var(--grid)";
  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }

  /* ===== 片段 A ===== */
  /* ---------- 代理 A：§1.1 熱平衡與溫度、§1.2 理想氣體 ---------- */

  /* 線性最小平方：回傳 [斜率, 截距] */
  function t1Fit(pts) {
    var n = pts.length, sx = 0, sy = 0, sxx = 0, sxy = 0;
    pts.forEach(function (p) { sx += p[0]; sy += p[1]; sxx += p[0] * p[0]; sxy += p[0] * p[1]; });
    var s = (n * sxy - sx * sy) / (n * sxx - sx * sx);
    return [s, (sy - s * sx) / n];
  }

  /* ---------------- 1. 定容氣體溫度計（§1.1 Fig. 1.3） ---------------- */
  /* 資料點由課本 Fig. 1.3 的向量座標換算（°C, atm） */
  var GT_DATA = [
    [[-78, 0.856], [-38, 1.026], [0, 1.187], [45, 1.377], [97, 1.598]],
    [[-76, 0.661], [-38, 0.775], [0, 0.918], [47, 1.058], [95, 1.212]],
    [[-82, 0.446], [-38, 0.545], [0, 0.637], [48, 0.742], [95, 0.847]]
  ];
  var GT_COL = [RED, BLUE, GREEN];
  function gtX(T) { return (T + 300) / 40; }   // °C → 圖座標
  function gtY(P) { return P * 2.4; }
  A.define("t1-gas-thermo", {
    title: "定容氣體溫度計：壓力對溫度",
    question: "三種氣體量的直線往低溫外插，會交在哪裡？",
    view: [440, 270], origin: [30, 222], scale: 38,
    init: { e: 0, k: 0 },
    steps: [
      { label: "實驗數據", caption: "Fig. 1.3：固定體積的空氣，三種不同的氣體量。每組都排成直線，氣體越多斜率越大。", dur: 300, hold: 2400 },
      { label: "往低溫外插", caption: "把三條直線往左延伸到 $P=0$。實際上氣體會先液化，但直線的趨勢很清楚。", to: { e: 1 }, dur: 2600, hold: 1600 },
      { label: "共同的零點", caption: "三條線都在約 $-280^\\circ\\text{C}$ 碰到 $P=0$：氣體量只改斜率、不改零點。密度趨近零的極限是 $-273.15^\\circ\\text{C}$——絕對零度。", dur: 300, hold: 2600 },
      { label: "改用 kelvin", caption: "溫度改從絕對零度量起：$T(\\text{K})=T(^\\circ\\text{C})+273.15$。每條線都變成過原點的正比 $P\\propto T$，這就是理想氣體定律裡的 $T$。", set: { k: 1 }, dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var x0 = gtX(-300), x1 = gtX(120);
      d.line([x0, 0], [x1, 0], { color: MUTED, width: 1.3 });
      d.line([x0, 0], [x0, gtY(1.75)], { color: MUTED, width: 1.3 });
      (s.k ? [0, 100, 200, 300, 400] : [-300, -200, -100, 0, 100]).forEach(function (v) {
        var T = s.k ? v - 273.15 : v;
        d.line([gtX(T), 0], [gtX(T), -0.12], { color: MUTED, width: 1 });
        d.label([gtX(T), -0.42], String(v), { color: MUTED, size: 11 });
      });
      d.label([gtX(-60), -0.95], s.k ? "T\\ (\\text{K})" : "T\\ (^\\circ\\text{C})", { color: MUTED, size: 12 });
      [0.4, 0.8, 1.2, 1.6].forEach(function (P) {
        d.line([x0, gtY(P)], [x1, gtY(P)], { color: GRID, width: 1 });
        d.label([x0 + 0.35, gtY(P) + 0.18], F(P, 1), { color: MUTED, size: 10 });
      });
      d.label([x0 + 1.25, gtY(1.75) + 0.2], "P\\ (\\text{atm})", { color: MUTED, size: 12 });
      GT_DATA.forEach(function (pts, i) {
        var f = t1Fit(pts), T0 = -f[1] / f[0], Tl = -82 + s.e * (T0 + 82);
        d.line([gtX(Tl), gtY(f[0] * Tl + f[1])], [gtX(100), gtY(f[0] * 100 + f[1])], { color: GT_COL[i], width: 1.6, dash: s.e > 0 ? "5 4" : null, opacity: 0.85 });
        pts.forEach(function (p) { d.dot([gtX(p[0]), gtY(p[1])], { color: GT_COL[i], r: 3.6 }); });
      });
      if (s._step >= 2) {
        d.dot([gtX(-273.15), 0], { color: PURPLE, r: 5 });
        d.label([gtX(-273.15) + 0.25, 0.7], s.k ? "0\\ \\text{K}" : "-273.15^\\circ\\text{C}", { color: PURPLE, size: 12 });
      }
    },
    formula: function (s) {
      var f = t1Fit(GT_DATA[1]), T0 = -f[1] / f[0];
      if (s.k) return "P=s\\,T\\ (T\\text{ 以 K 計})\\\\ \\text{中間線：}s=" + F(f[0] * 1000, 2) + "\\times10^{-3}\\ \\text{atm/K}";
      return "\\text{中間線：}P=s\\,(T-T_0),\\ s=" + F(f[0] * 1000, 2) + "\\times10^{-3}\\ \\tfrac{\\text{atm}}{^\\circ\\text{C}}\\\\ T_0=" + F(T0, 0) + "^\\circ\\text{C}";
    }
  });

  /* ---------------- 2. β = αx + αy + αz（§1.1 習題 1.8(c)） ---------------- */
  function t1Box(d, b, col, op) {
    var x0 = b[0], x1 = b[1], y0 = b[2], y1 = b[3], z0 = b[4], z1 = b[5];
    var st = { color: col, width: 1.3, fill: col, fillOpacity: op };
    d.poly3([[x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1]], st);
    d.poly3([[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]], st);
    d.poly3([[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], st);
  }
  A.define("t1-expansion", {
    title: "長方體受熱膨脹：$\\Delta V$ 是三塊薄板",
    question: "為什麼體膨脹係數是三個線膨脹係數相加？",
    view: [440, 280], origin: [215, 190], scale: 34,
    init: { ex: 0, ey: 0, ez: 0, eps: 0.12 },
    steps: [
      { label: "原來的長方體", caption: "邊長 $L_x,L_y,L_z$，$V=L_xL_yL_z$。升溫 $\\Delta T$ 後每邊變成 $L_i(1+\\alpha_i\\Delta T)$。圖中把 $\\alpha\\Delta T$ 誇大成 0.12。", dur: 300, hold: 2200 },
      { label: "$x$ 方向伸長", caption: "多出一塊薄板：厚 $\\Delta L_x=\\alpha_xL_x\\Delta T$，面積 $L_yL_z$，體積 $\\alpha_x\\Delta T\\cdot V$。", to: { ex: 1 }, dur: 1200, hold: 1400 },
      { label: "$y$ 方向伸長", caption: "第二塊：$\\alpha_y\\Delta T\\cdot V$。", to: { ey: 1 }, dur: 1200, hold: 1200 },
      { label: "$z$ 方向伸長", caption: "第三塊：$\\alpha_z\\Delta T\\cdot V$。三塊合計 $(\\alpha_x+\\alpha_y+\\alpha_z)\\Delta T\\cdot V$；邊上與角上還缺幾條細條（正比於 $(\\Delta T)^2$）。", to: { ez: 1 }, dur: 1200, hold: 2200 },
      { label: "$\\Delta T\\to0$", caption: "真實的 $\\alpha\\Delta T\\sim10^{-4}$：細條比薄板小一萬倍，可以略去。所以 $\\Delta V/V=(\\alpha_x+\\alpha_y+\\alpha_z)\\Delta T$，$\\beta=\\alpha_x+\\alpha_y+\\alpha_z$。", to: { eps: 0.02 }, dur: 2200, hold: 2600 }
    ],
    draw: function (d, s) {
      var a = 3.2, e = s.eps * a;
      d.camera(35, 22);
      t1Box(d, [0, a, 0, a, 0, a], MUTED, 0.12);
      if (s.ex > 0) t1Box(d, [a, a + e * s.ex, 0, a, 0, a], RED, 0.35);
      if (s.ey > 0) t1Box(d, [0, a, a, a + e * s.ey, 0, a], BLUE, 0.35);
      if (s.ez > 0) t1Box(d, [0, a, 0, a, a, a + e * s.ez], GREEN, 0.35);
      if (s.ez >= 1) {
        var dash = { color: PURPLE, width: 1.2, dash: "3 3" };
        d.line3([a + e, a, 0], [a + e, a + e, 0], dash); d.line3([a + e, a + e, 0], [a, a + e, 0], dash);
        d.line3([a + e, a + e, 0], [a + e, a + e, a + e], dash); d.line3([a + e, 0, a + e], [a + e, a + e, a + e], dash);
        d.line3([0, a + e, a + e], [a + e, a + e, a + e], dash);
      }
      d.label3([a / 2, -0.45, a + 0.25], "L_x", { color: MUTED, size: 12 });
      d.label3([a + 0.5, a / 2, -0.35], "L_y", { color: MUTED, size: 12 });
      d.label3([a + 0.4, -0.35, a / 2], "L_z", { color: MUTED, size: 12 });
    },
    formula: function (s) {
      var e = s.eps, exact = Math.pow(1 + e, 3) - 1, lin = 3 * e;
      return "\\alpha\\Delta T=" + F(e, 3) + "\\ (\\text{各向同性})\\\\ \\tfrac{\\Delta V}{V}=(1+" + F(e, 3) + ")^3-1=" + F(exact, 4) + "\\ \\approx\\ 3\\alpha\\Delta T=" + F(lin, 4);
    }
  });

  /* ---------------- 3. 指數大氣（§1.2 習題 1.16） ---------------- */
  var ATM_PL = [["Ogden", 1.43], ["Leadville", 3.09], ["Whitney", 4.42], ["Everest", 8.85]];
  var ATM_H = 8.31 * 280 / (0.029 * 9.8) / 1000;   // km
  A.define("t1-atmosphere", {
    title: "等溫大氣：$P(z)=P_0e^{-z/H}$",
    question: "爬到聖母峰頂，氣壓剩多少？溫度不同時標高怎麼變？",
    view: [440, 270], origin: [52, 228], scale: 1,
    init: { z: 0, T: 280 },
    steps: [
      { label: "海平面", caption: "$z=0$，$P=1\\ \\text{atm}$。取 $T=280\\ \\text{K}$、空氣 $M=0.029\\ \\text{kg/mol}$：標高 $H=RT/Mg=8.19\\ \\text{km}$。", dur: 300, hold: 2000 },
      { label: "往上爬", caption: "每升高一個 $H$，壓力乘 $1/e=0.37$。依序經過 Ogden、Leadville、Whitney，到聖母峰 8850 m：$0.34\\ \\text{atm}$。", to: { z: 8.85 }, dur: 5200, hold: 1800 },
      { label: "溫度較高", caption: "若大氣是 $320\\ \\text{K}$，$H\\propto T$ 變成 $9.4\\ \\text{km}$，曲線變平：同一高度的氣壓較高（虛線是 280 K）。", to: { T: 320 }, dur: 1600, hold: 2400 }
    ],
    draw: function (d, s) {
      var W = 360, Hh = 190, zmax = 12, H = 8.31 * s.T / (0.029 * 9.8) / 1000;
      function X(z) { return z / zmax * W; } function Y(p) { return p * Hh; }
      d.line([0, 0], [W, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, Hh + 8], { color: MUTED, width: 1.3 });
      [0, 2, 4, 6, 8, 10, 12].forEach(function (z) { d.line([X(z), 0], [X(z), -4], { color: MUTED, width: 1 }); d.label([X(z), -14], String(z), { color: MUTED, size: 11 }); });
      d.label([W / 2, -30], "z\\ (\\text{km})", { color: MUTED, size: 12 });
      [0.25, 0.5, 0.75, 1].forEach(function (p) { d.line([0, Y(p)], [W, Y(p)], { color: GRID, width: 1 }); d.label([-18, Y(p)], F(p, 2), { color: MUTED, size: 10 }); });
      d.label([40, Hh + 14], "P/P_0", { color: MUTED, size: 12 });
      var pts = [], ref = [];
      for (var i = 0; i <= 60; i++) { var z = zmax * i / 60; pts.push([X(z), Y(Math.exp(-z / H))]); ref.push([X(z), Y(Math.exp(-z / ATM_H))]); }
      if (s.T > 280.5) d.path(ref, { color: MUTED, width: 1.4, dash: "5 4" });
      d.path(pts, { color: BLUE, width: 2.2 });
      ATM_PL.forEach(function (pl) {
        if (s.z + 1e-6 >= pl[1] || s._step === 2) {
          var p = Math.exp(-pl[1] / H);
          d.dot([X(pl[1]), Y(p)], { color: GREEN, r: 4 });
          d.label([X(pl[1]) + 4, Y(p) + 14], "\\text{" + pl[0] + "}", { color: GREEN, size: 10 });
        }
      });
      var zc = s._step === 2 ? 8.85 : s.z;
      d.dot([X(zc), Y(Math.exp(-zc / H))], { color: RED, r: 5.5 });
    },
    formula: function (s) {
      var H = 8.31 * s.T / (0.029 * 9.8) / 1000, zc = s._step === 2 ? 8.85 : s.z;
      return "H=\\frac{RT}{Mg}=" + F(H, 2) + "\\ \\text{km}\\quad(T=" + F(s.T, 0) + "\\ \\text{K})\\\\ P(" + F(zc, 2) + "\\ \\text{km})=e^{-" + F(zc, 2) + "/" + F(H, 2) + "}=" + F(Math.exp(-zc / H), 3) + "\\ \\text{atm}";
    }
  });

  /* ---------------- 4. 氮的 B(T) 與凡得瓦（§1.2 習題 1.17(d)） ---------------- */
  var VIR = [[100, -160], [200, -35], [300, -4.2], [400, 9.0], [500, 16.9], [600, 21.3]];
  A.define("t1-n2-virial", {
    title: "氮的第二維里係數 $B(T)$ 與凡得瓦預測",
    question: "兩個參數 $a$、$b$ 能把六個數據點對得多好？",
    view: [440, 280], origin: [58, 98], scale: 50,
    init: { a: 0.0748, b: 30, show: 0 },
    steps: [
      { label: "實測數據", caption: "習題 1.17 的表：低溫 $B$ 很負（吸引為主），約 330 K 過零，高溫變正（排斥為主）。", dur: 300, hold: 2200 },
      { label: "粗估 $a$、$b$", caption: "凡得瓦：$B=b-a/RT$。高溫趨於 $b\\approx30\\ \\text{cm}^3/\\text{mol}$、300 K 過零 ⟹ $a=bRT=0.075$。100 K 只有 $-60$，太不夠負。", set: { show: 1 }, dur: 300, hold: 2600 },
      { label: "最小平方擬合", caption: "對六點做最小平方：$b=64\\ \\text{cm}^3/\\text{mol}$、$a=0.182\\ \\text{J}\\cdot\\text{m}^3/\\text{mol}^2$。低溫對上了，但中溫偏負、高溫上升太快。", to: { a: 0.1822, b: 64.2 }, dur: 2400, hold: 2600 },
      { label: "定性對、定量粗", caption: "凡得瓦的 $B$ 單調趨向 $b$（虛線），實測在 20 多就趨緩：兩個參數抓到了變號，抓不到細節。", dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      function X(T) { return T / 100; } function Y(B) { return B / 60; }
      d.line([0, 0], [X(660), 0], { color: MUTED, width: 1.3 });
      d.line([0, Y(-175)], [0, Y(75)], { color: MUTED, width: 1.3 });
      [100, 200, 300, 400, 500, 600].forEach(function (T) { d.line([X(T), 0], [X(T), -0.08], { color: MUTED, width: 1 }); d.line([X(T), Y(-175)], [X(T), Y(-175) - 0.08], { color: MUTED, width: 1 }); d.label([X(T), Y(-175) - 0.3], String(T), { color: MUTED, size: 10 }); });
      d.label([X(700), Y(-175) - 0.3], "T\\ (\\text{K})", { color: MUTED, size: 12 });
      [-150, -100, -50, 50].forEach(function (B) { d.line([0, Y(B)], [X(650), Y(B)], { color: GRID, width: 1 }); d.label([-0.45, Y(B)], String(B), { color: MUTED, size: 10 }); });
      d.label([1.55, Y(98)], "B\\ (\\text{cm}^3/\\text{mol})", { color: MUTED, size: 12 });
      if (s.show) {
        var pts = [];
        for (var T = 70; T <= 650; T += 10) { var B = s.b - s.a / (8.31 * T) * 1e6; if (B > -175) pts.push([X(T), Y(B)]); }
        d.path(pts, { color: BLUE, width: 2.2 });
        if (s._step === 3) d.line([X(60), Y(s.b)], [X(650), Y(s.b)], { color: BLUE, width: 1.2, dash: "5 4" });
      }
      VIR.forEach(function (p) { d.dot([X(p[0]), Y(p[1])], { color: RED, r: 4.2 }); });
    },
    formula: function (s) {
      if (!s.show) return "\\text{數據：}B(100)=-160,\\ B(600)=21.3\\ \\text{cm}^3/\\text{mol}";
      var B1 = s.b - s.a / (8.31 * 100) * 1e6, B6 = s.b - s.a / (8.31 * 600) * 1e6;
      return "B=b-\\frac{a}{RT},\\ b=" + F(s.b, 1) + ",\\ a=" + F(s.a, 3) + "\\\\ B(100)=" + F(B1, 0) + ",\\ B(600)=" + F(B6, 1);
    }
  });

  /* ---------------- 5. 一個分子撞活塞（§1.2 微觀模型） ---------------- */
  var PIS_L = 6, PIS_TW = 24;
  var PIS_MANY = [0.55, 0.8, 1.05, 0.65, 1.3, 0.9, 1.15, 0.7, 1.45, 0.6, 1.0, 1.25];
  function pisX(v, t, ph) { var p = ((v * t + ph) % (2 * PIS_L) + 2 * PIS_L) % (2 * PIS_L); return p < PIS_L ? p : 2 * PIS_L - p; }
  function pisHits(v, t, ph) { var out = [], n = 0, th; while ((th = ((2 * n + 1) * PIS_L - ph) / v) <= t) { if (th >= 0) out.push(th); n++; } return out; }
  A.define("t1-piston", {
    title: "分子撞活塞：一陣一陣的力，平均成壓力",
    question: "為什麼 $\\overline P=mv_x^2/V$ 有兩個 $v_x$？",
    view: [440, 290], origin: [30, 270], scale: 26,
    init: { t: 0, v: 1, many: 0 },
    steps: [
      { label: "一個分子", caption: "長 $L$ 的圓筒裡一個分子，$x$ 方向速率 $v_x$，彈性碰撞。每來回一次（$\\Delta t=2L/v_x$）撞右邊的活塞一次。", to: { t: PIS_TW }, dur: 6000, hold: 800 },
      { label: "平均力", caption: "每次撞擊給活塞 $2mv_x$ 的衝量（下方的尖峰）。平均力＝衝量 ÷ 間隔 $=2mv_x/(2L/v_x)=mv_x^2/L$（綠線）。", dur: 300, hold: 2600 },
      { label: "速率加倍", caption: "$v_x$ 加倍：每次衝量加倍（一個 $v_x$），撞擊頻率也加倍（另一個 $v_x$），平均力變 4 倍。", set: { t: 0, v: 2 }, to: { t: PIS_TW }, dur: 6000, hold: 2200 },
      { label: "很多分子", caption: "$N$ 個分子各撞各的，尖峰密得像連續的壓力：$PV=Nm\\overline{v_x^2}$。再用 $PV=NkT$ 得 $\\tfrac12m\\overline{v_x^2}=\\tfrac12kT$。", set: { t: 0, v: 1, many: 1 }, to: { t: PIS_TW }, dur: 6000, hold: 2600 }
    ],
    draw: function (d, s) {
      var yb = 6.4, h = 2.6, L = PIS_L, x0 = 1.2;
      d.rect(x0, yb, x0 + L, yb + h, { color: INK, width: 1.6 });
      d.rect(x0 + L, yb - 0.2, x0 + L + 0.35, yb + h + 0.2, { color: PURPLE, width: 1.4, fill: PURPLE, fillOpacity: 0.35 });
      d.label([x0 + L + 0.9, yb + h + 0.5], "\\text{活塞 }A", { color: PURPLE, size: 11 });
      d.label([x0 + L / 2, yb + h + 0.5], "L", { color: MUTED, size: 12 });
      var mols = s.many ? PIS_MANY.map(function (v, i) { return [v, i * 1.7]; }) : [[s.v, 0]];
      mols.forEach(function (mv, i) {
        var x = pisX(mv[0], s.t, mv[1]), yy = yb + 0.35 + ((i * 0.53 + 0.5) % 1) * (h - 0.7);
        if (!s.many) yy = yb + h / 2;
        d.dot([x0 + x, yy], { color: RED, r: s.many ? 3.2 : 5 });
        if (!s.many) d.arrow([x0 + x, yy], [x0 + x + 0.9 * (Math.floor((s.v * s.t) / L) % 2 ? -1 : 1), yy], { color: RED, width: 1.6, head: 7 });
      });
      /* 下方：活塞受力對時間 */
      var gx = 1.2, gw = 14.0, gy = 0.6, gh = 4.2, sc = gw / PIS_TW;
      d.line([gx, gy], [gx + gw, gy], { color: MUTED, width: 1.2 }); d.line([gx, gy], [gx, gy + gh], { color: MUTED, width: 1.2 });
      d.label([gx + gw - 0.3, gy - 0.45], "t", { color: MUTED, size: 12 });
      d.label([gx + 1.2, gy + gh + 0.3], "F_{\\text{活塞}}", { color: MUTED, size: 12 });
      var unit = 0.32, tot = 0;
      mols.forEach(function (mv) {
        pisHits(mv[0], s.t, mv[1]).forEach(function (th) {
          var hgt = Math.min(gh - 0.2, unit * 2 * mv[0] * (s.many ? 2.2 : 3));
          d.line([gx + th * sc, gy], [gx + th * sc, gy + hgt], { color: BLUE, width: s.many ? 1.2 : 2.2 });
        });
        tot += mv[0] * mv[0];
      });
      if (s._step >= 1) {
        var avg = s.many ? tot / PIS_MANY.length * 0.35 * 2.2 : s.v * s.v * 0.35;
        d.line([gx, gy + avg], [gx + gw, gy + avg], { color: GREEN, width: 2, dash: "6 4" });
      }
    },
    formula: function (s) {
      if (s.many) return "PV=\\sum_i m v_{ix}^2=Nm\\overline{v_x^2}=NkT\\\\ \\Longrightarrow\\ \\tfrac12m\\overline{v^2}=\\tfrac32kT";
      return "v_x=" + F(s.v, 0) + ":\\ \\Delta t=\\frac{2L}{v_x},\\ \\Delta v_x=-2v_x\\\\ \\overline P=\\frac{m\\,(2v_x)}{A\\,(2L/v_x)}=\\frac{mv_x^2}{V}\\ \\propto\\ " + F(s.v * s.v, 0);
    }
  });

  /* ===== 片段 B ===== */
  /* 代理 B：§1.3 能量均分、§1.4 熱與功、§1.5 壓縮功。包在自己的函式裡，避免和其他片段的變數同名。 */
  (function () {
    var ATM_L = 101.3;   // 1 atm·L = 101.3 J

    /* ---------------- §1.3 數自由度 ---------------- */
    var TR = { n: 3, col: BLUE, lab: ["x", "y", "z"], name: "\\text{平移}" };
    var ROT2 = { n: 2, col: GREEN, lab: ["\\omega_1", "\\omega_2"], name: "\\text{轉動}" };
    var ROT3 = { n: 3, col: GREEN, lab: ["\\omega_1", "\\omega_2", "\\omega_3"], name: "\\text{轉動}" };
    var DOF = [
      { name: "\\text{單原子（He、Ar）}", groups: [TR], from: 0 },
      { name: "\\text{雙原子，室溫}", groups: [TR, ROT2], from: 1 },
      { name: "\\text{雙原子，高溫}", groups: [TR, ROT2, { n: 2, col: RED, lab: ["K", "U"], name: "\\text{振動}" }], from: 2 },
      { name: "\\text{固體（每個原子）}", groups: [{ n: 3, col: BLUE, lab: ["x", "y", "z"], name: "\\text{動能}" }, { n: 3, col: PURPLE, lab: ["x", "y", "z"], name: "\\text{位能}" }], from: 0 },
      { name: "\\text{水蒸氣（全部活化）}", groups: [TR, ROT3, { n: 6, col: RED, lab: ["", "", "", "", "", ""], name: "\\text{3 個振動模式}" }], from: 1 }
    ];
    function dofF(c) { return DOF[c].groups.reduce(function (a, g) { return a + g.n; }, 0); }
    A.define("t1-dof", {
      title: "每個二次自由度分到 $\\tfrac12kT$",
      question: "不同的分子各有幾個自由度？一莫耳在 300 K 有多少熱能？",
      view: [440, 250], origin: [24, 196], scale: 30,
      init: { c: 0, a: 1 },
      steps: [
        { label: "單原子", caption: "氦、氬只有 $x,y,z$ 三個平移動能，每格高度代表 $\\tfrac12kT$：$f=3$，每個原子平均 $\\tfrac32kT$。", set: { c: 0, a: 0 }, to: { a: 1 }, dur: 1200, hold: 2200 },
        { label: "雙原子（室溫）", caption: "N$_2$、O$_2$ 多了繞兩個垂直軸的轉動；繞分子軸的轉動不算（量子力學）。振動在室溫凍結：$f=5$。", set: { c: 1, a: 0 }, to: { a: 1 }, dur: 1200, hold: 2400 },
        { label: "雙原子（高溫）", caption: "溫度夠高時振動「解凍」：一個振動模式有動能 $K$ 與位能 $U$ 兩個平方項，$f=7$。", set: { c: 2, a: 0 }, to: { a: 1 }, dur: 1400, hold: 2400 },
        { label: "固體", caption: "彈簧床模型：每個原子三個方向各有動能、位能，$f=6$；一莫耳 $3RT$，就是 Dulong–Petit 定律的來源。", set: { c: 3, a: 0 }, to: { a: 1 }, dur: 1400, hold: 2400 },
        { label: "水蒸氣", caption: "習題 1.25：平移 3、轉動 3（彎曲形分子）、3 個振動模式各 2，共 12。室溫時兩個伸縮模式凍結。", set: { c: 4, a: 0 }, to: { a: 1 }, dur: 1600, hold: 3000 }
      ],
      draw: function (d, s) {
        var cs = DOF[s.c], H = 1.6, w = 0.78, gap = 1.0, x = 0.4, k = 0;
        d.line([0, 0], [13.6, 0], { color: MUTED, width: 1.3 });
        d.line([0, H], [13.6, H], { color: GRID, width: 1, dash: "4 4" });
        d.label([1.9, 4.4], "\\text{每格}=\\tfrac12kT", { color: MUTED, size: 12 });
        d.label([8.2, 4.4], cs.name, { color: INK, size: 14 });
        cs.groups.forEach(function (g, gi) {
          var x0 = x, grow = gi >= cs.from ? s.a : 1;
          for (var j = 0; j < g.n; j++) {
            d.rect(x, 0, x + w, H * grow, { color: g.col, fill: g.col, fillOpacity: 0.45, width: 1 });
            if (g.lab[j]) d.label([x + w / 2, -0.4], g.lab[j], { color: g.col, size: 11 });
            x += gap; k++;
          }
          d.label([(x0 + x - gap + w) / 2, H + 0.9], g.name, { color: g.col, size: 12 });
          x += 0.35;
        });
      },
      formula: function (s) {
        var f = dofF(s.c);
        return "f=" + f + "\\qquad\\bar E=\\tfrac{" + f + "}{2}kT\\\\ U(1\\ \\text{mol},300\\ \\text{K})=\\tfrac{" + f + "}{2}RT=" + F(f / 2 * 8.315 * 300, 0) + "\\ \\text{J}";
      }
    });

    /* ---------------- §1.4 第一定律 ΔU = Q + W ---------------- */
    A.define("t1-first-law", {
      title: "第一定律：$\\Delta U=Q+W$",
      question: "同樣的 $\\Delta U$，可以由不同的 $Q$、$W$ 組合而成嗎？",
      view: [440, 250], origin: [20, 230], scale: 20,
      init: { q: 0, w: 0 },
      steps: [
        { label: "定容加熱", caption: "活塞固定、下面點火：熱 $Q=+300\\ \\text{J}$ 流進來，$W=0$，內能增加 300 J。", to: { q: 300, w: 0 }, dur: 1600, hold: 2200 },
        { label: "絕熱壓縮", caption: "快速推活塞、來不及傳熱：$Q=0$、$W=+300\\ \\text{J}$。$\\Delta U$ 和上一步一樣——只看末狀態，分不出是加熱還是做功（習題 1.29）。", to: { q: 0, w: 300 }, dur: 1800, hold: 2600 },
        { label: "等溫壓縮", caption: "慢慢推、熱一邊流出：$W=+300\\ \\text{J}$、$Q=-300\\ \\text{J}$，$\\Delta U=0$（理想氣體溫度不變，第 5 節）。", to: { q: -300, w: 300 }, dur: 1800, hold: 2400 },
        { label: "等溫膨脹", caption: "反過來：吸熱 $Q=+300\\ \\text{J}$，全部拿去對外做功 $W=-300\\ \\text{J}$——加了熱卻不升溫（習題 1.27）。", to: { q: 300, w: -300 }, dur: 1800, hold: 2400 },
        { label: "邊吸熱邊膨脹", caption: "自編難題 04b(a)：$Q=+400\\ \\text{J}$、$W=-200\\ \\text{J}$，留下 $\\Delta U=+200\\ \\text{J}$。", to: { q: 400, w: -200 }, dur: 1800, hold: 2800 }
      ],
      draw: function (d, s) {
        var sc = 0.8 / 100, x0 = 7, x1 = 15, y0 = 1.5, y1 = 7.5, base = 4.0, dU = s.q + s.w;
        d.rect(x0, y0, x1, y1, { color: INK, width: 2 });
        d.rect(x0 + 0.15, y1 - 0.5, x1 - 0.15, y1 - 0.1, { color: MUTED, fill: MUTED, fillOpacity: 0.35, width: 1 });
        d.label([x0 + 1.7, y0 + 0.6], "\\text{系統}", { color: MUTED, size: 12 });
        d.line([10, base], [13, base], { color: MUTED, width: 1, dash: "3 3" });
        if (Math.abs(dU) > 1) d.rect(10.3, base, 12.7, base + dU * sc, { color: GREEN, fill: GREEN, fillOpacity: 0.45, width: 1 });
        d.label([11.5, base + dU * sc + (dU >= 0 ? 0.5 : -0.5)], "\\Delta U=" + F(dU, 0), { color: GREEN, size: 12 });
        var L = Math.abs(s.q) * sc, yq = 4.5;
        if (L > 0.05) {
          if (s.q > 0) d.arrow([x0 - 0.2 - L, yq], [x0 - 0.2, yq], { color: RED, width: 3 });
          else d.arrow([x0 - 0.2, yq], [x0 - 0.2 - L, yq], { color: RED, width: 3 });
        }
        d.label([x0 - 2.6, yq + 0.9], "Q=" + F(s.q, 0) + "\\ \\text{J}", { color: RED, size: 12 });
        var Lw = Math.abs(s.w) * sc, xw = 9.0;
        if (Lw > 0.05) {
          if (s.w > 0) d.arrow([xw, y1 + 0.2 + Lw], [xw, y1 + 0.2], { color: BLUE, width: 3 });
          else d.arrow([xw, y1 + 0.2], [xw, y1 + 0.2 + Lw], { color: BLUE, width: 3 });
        }
        d.label([xw + 2.2, y1 + 1.6], "W=" + F(s.w, 0) + "\\ \\text{J}", { color: BLUE, size: 12 });
      },
      formula: function (s) {
        var q = Math.round(s.q), w = Math.round(s.w);
        return "\\Delta U=Q+W=(" + q + ")+(" + w + ")=" + (q + w) + "\\ \\text{J}";
      }
    });

    /* ---------------- §1.5 PV 圖下的面積 ---------------- */
    var GAM = 1.4;
    var PATHS = [
      { name: "\\text{定壓膨脹}", v0: 1, v1: 3, P: function (v) { return 1; }, W: function (v) { return -(v - 1); }, col: BLUE },
      { name: "P\\propto V", v0: 1, v1: 3, P: function (v) { return v; }, W: function (v) { return -(v * v - 1) / 2; }, col: BLUE },
      { name: "\\text{等溫壓縮}", v0: 3, v1: 1, P: function (v) { return 3 / v; }, W: function (v) { return 3 * Math.log(3 / v); }, col: RED },
      { name: "\\text{絕熱壓縮}", v0: 3, v1: 1, P: function (v) { return Math.pow(3 / v, GAM); }, W: function (v) { return 3 / (GAM - 1) * (Math.pow(3 / v, GAM - 1) - 1); }, col: RED }
    ];
    function PX(v) { return v * 2.6; }
    function PY(p) { return p * 0.95; }
    function curve(pth, va, vb, n) { var out = []; for (var j = 0; j <= n; j++) { var v = va + (vb - va) * j / n; out.push([PX(v), PY(pth.P(v))]); } return out; }
    A.define("t1-pv-work", {
      title: "功＝ PV 曲線下面積的負值",
      question: "同樣在 1 L 與 3 L 之間，不同的路徑做的功一樣嗎？",
      view: [440, 280], origin: [46, 236], scale: 40,
      init: { c: 0, t: 0 },
      steps: [
        { label: "定壓膨脹", caption: "壓力固定 1 atm，由 1 L 膨脹到 3 L：面積是矩形 $P\\Delta V=2\\ \\text{atm·L}$。向右走，$W$ 為負。", set: { c: 0, t: 0 }, to: { t: 1 }, dur: 2400, hold: 2000 },
        { label: "$P\\propto V$", caption: "習題 1.31：沿過原點的直線走到 3 atm，面積是梯形，$W=-4\\ \\text{atm·L}=-405\\ \\text{J}$——同樣的 $\\Delta V$，壓力越高功越大。", set: { c: 1, t: 0 }, to: { t: 1 }, dur: 2400, hold: 2400 },
        { label: "等溫壓縮", caption: "反方向：由 3 L 沿等溫線 $PV=$ 常數壓回 1 L。向左走，$W$ 為正：$W=NkT\\ln3=3.30\\ \\text{atm·L}$。", set: { c: 2, t: 0 }, to: { t: 1 }, dur: 2600, hold: 2400 },
        { label: "絕熱壓縮", caption: "同樣由 3 L、1 atm 出發，絕熱線（$\\gamma=1.4$）比等溫線陡，從 $T_i$ 的等溫線爬到更高溫的等溫線，面積較大：$W=4.14\\ \\text{atm·L}$。", set: { c: 3, t: 0 }, to: { t: 1 }, dur: 2600, hold: 3000 }
      ],
      draw: function (d, s) {
        var pth = PATHS[s.c], v = pth.v0 + (pth.v1 - pth.v0) * s.t;
        d.axes([0, 9.4], [0, 5.3], ["V", "P"]);
        [1, 2, 3].forEach(function (x) { d.line([PX(x), 0], [PX(x), -0.12], { color: MUTED, width: 1 }); d.label([PX(x), -0.4], x + "\\ \\text{L}", { color: MUTED, size: 11 }); });
        [1, 2, 3, 4, 5].forEach(function (p) { d.line([0, PY(p)], [-0.12, PY(p)], { color: MUTED, width: 1 }); d.label([-0.55, PY(p)], String(p), { color: MUTED, size: 10 }); });
        d.label([-0.4, 5.55], "\\text{atm}", { color: MUTED, size: 10 });
        if (s.c === 1) d.line([0, 0], [PX(1), PY(1)], { color: MUTED, width: 1.2, dash: "3 4" });
        if (s.c >= 2) d.path(curve(PATHS[2], 0.9, 3.4, 60), { color: MUTED, width: 1.2, dash: "4 4" });
        if (s.c === 3) {
          var Tf = Math.pow(3, GAM - 1);  // 末溫等溫線 PV = 3·3^{0.4}
          d.path(curve({ P: function (x) { return 3 * Tf / x; } }, 2.75, 3.4, 30), { color: MUTED, width: 1.2, dash: "2 4" });
          d.path(curve({ P: function (x) { return 3 * Tf / x; } }, 0.9, 1.55, 30), { color: MUTED, width: 1.2, dash: "2 4" });
          d.label([PX(1.55) + 0.2, PY(3 * Tf / 1.55) + 0.25], "T_f", { color: MUTED, size: 11 });
          d.label([PX(3.3), PY(3 / 3.3) + 0.35], "T_i", { color: MUTED, size: 11 });
        }
        d.path(curve(pth, pth.v0, pth.v1, 60), { color: MUTED, width: 1.2, dash: "4 4" });
        if (Math.abs(v - pth.v0) > 1e-3) {
          var pts = curve(pth, pth.v0, v, 50);
          d.poly([[PX(pth.v0), 0]].concat(pts, [[PX(v), 0]]), { color: pth.col, fill: pth.col, fillOpacity: 0.18, width: 0.5 });
          d.path(pts, { color: pth.col, width: 2.6 });
        }
        d.dot([PX(v), PY(pth.P(v))], { color: pth.col });
        d.label([5.4, 4.9], pth.name, { color: pth.col, size: 13 });
      },
      formula: function (s) {
        var pth = PATHS[s.c], v = pth.v0 + (pth.v1 - pth.v0) * s.t, W = pth.W(v);
        return "V=" + F(v, 2) + "\\ \\text{L},\\ P=" + F(pth.P(v), 2) + "\\ \\text{atm}\\\\ W=-\\!\\int P\\,dV=" + F(W, 2) + "\\ \\text{atm·L}=" + F(W * ATM_L, 0) + "\\ \\text{J}";
      }
    });

    /* ---------------- §1.5 絕熱壓縮的溫度 VT^{f/2} = 常數 ---------------- */
    function TX(r) { return (r - 1) / 19 * 8.4; }
    function TY(T) { return T / 2400 * 5; }
    function Tad(r, f) { return 300 * Math.pow(r, 2 / f); }
    A.define("t1-adiabat", {
      title: "絕熱壓縮：$T=T_i\\,(V_i/V)^{2/f}$",
      question: "把空氣壓縮成幾分之一，溫度會升到多高？",
      view: [440, 270], origin: [52, 226], scale: 40,
      init: { r: 1, he: 0 },
      steps: [
        { label: "出發", caption: "橫軸是壓縮比 $V_i/V$，縱軸是溫度。等溫壓縮停在 300 K（灰線）；絕熱壓縮 $VT^{f/2}=$ 常數，溫度一路上升。", dur: 300, hold: 2200 },
        { label: "打氣到 7 atm", caption: "習題 1.36：壓到 7 atm 時體積剩 0.249 L（壓縮比 4.01），空氣升到 523 K。", to: { r: 4.01 }, dur: 2200, hold: 2400 },
        { label: "柴油引擎 20 倍", caption: "習題 1.37：壓縮比 20，$T=300\\times20^{0.4}\\approx994\\ \\text{K}$，柴油一噴進去就自燃。", to: { r: 20 }, dur: 3200, hold: 2400 },
        { label: "單原子對照", caption: "同樣壓縮 20 倍，單原子氣體 $f=3$ 指數 $2/3$ 比空氣的 $2/5$ 大，升到 2210 K：自由度少，做的功全部擠在平移上，升溫多。", set: { he: 1 }, dur: 600, hold: 3000 }
      ],
      draw: function (d, s) {
        d.axes([0, 8.9], [0, 5.4], ["V_i/V", "T"]);
        [1, 5, 10, 15, 20].forEach(function (r) { d.line([TX(r), 0], [TX(r), -0.12], { color: MUTED, width: 1 }); d.label([TX(r), -0.4], String(r), { color: MUTED, size: 11 }); });
        [500, 1000, 1500, 2000].forEach(function (T) { d.line([0, TY(T)], [8.7, TY(T)], { color: GRID, width: 1 }); d.label([-0.7, TY(T)], String(T), { color: MUTED, size: 10 }); });
        d.label([-0.6, 5.65], "\\text{K}", { color: MUTED, size: 10 });
        d.line([0, TY(300)], [8.7, TY(300)], { color: MUTED, width: 1.6 });
        d.label([7.9, TY(300) + 0.3], "\\text{等溫}", { color: MUTED, size: 11 });
        var air = [], he = [];
        for (var j = 0; j <= 80; j++) { var r = 1 + 19 * j / 80; air.push([TX(r), TY(Tad(r, 5))]); he.push([TX(r), TY(Tad(r, 3))]); }
        d.path(air, { color: BLUE, width: 1.2, dash: "4 4" });
        var done = air.filter(function (p) { return p[0] <= TX(s.r) + 1e-9; });
        done.push([TX(s.r), TY(Tad(s.r, 5))]);
        d.path(done, { color: BLUE, width: 2.6 });
        d.dot([TX(s.r), TY(Tad(s.r, 5))], { color: BLUE });
        d.label([7.0, TY(Tad(20, 5)) + 0.45], "\\text{空氣 }f=5", { color: BLUE, size: 12 });
        if (s.he) {
          d.path(he, { color: RED, width: 2.2 });
          d.dot([TX(20), TY(Tad(20, 3))], { color: RED });
          d.label([5.4, TY(Tad(20, 3)) + 0.1], "\\text{單原子 }f=3", { color: RED, size: 12 });
        }
      },
      formula: function (s) {
        var out = "\\frac{V_i}{V}=" + F(s.r, 2) + ":\\ T=300\\cdot" + F(s.r, 2) + "^{2/5}=" + F(Tad(s.r, 5), 0) + "\\ \\text{K}\\\\ \\frac P{P_i}=" + F(s.r, 2) + "^{1.4}=" + F(Math.pow(s.r, 1.4), 1);
        if (s.he) out = "\\frac{V_i}{V}=20:\\ T_{\\text{air}}=" + F(Tad(20, 5), 0) + "\\ \\text{K}\\\\ T_{\\text{He}}=300\\cdot20^{2/3}=" + F(Tad(20, 3), 0) + "\\ \\text{K}";
        return out;
      }
    });
  })();

  /* ===== 片段 C ===== */
  /* ---------------- §1.6 熱容量（代理 C） ---------------- */

  /* 1. 氫氣 C_V 對 log T：自由度依序解凍（Fig. 1.13 的示意，用 Einstein 函數畫） */
  function einC(x) { if (x > 60) return 0; var ex = Math.exp(x); return x * x * ex / ((ex - 1) * (ex - 1)); }
  function cvH2(T) { return 1.5 + einC(300 / T) + einC(6000 / T); }      // 以 R 為單位
  var H2X = function (lt) { return (lt - 1) / 2.7 * 9; };                   // log10 T：1→3.7 對到 x：0→9
  var H2Y = 1.15;                                                          // 每 1R 的高度
  A.define("t1-cv-h2", {
    title: "一莫耳氫氣的 $C_V$：自由度依序解凍",
    question: "為什麼同一種氣體的熱容量會隨溫度一階一階升高？",
    view: [440, 260], origin: [46, 214], scale: 40,
    init: { lt: 1.0 },
    steps: [
      { label: "平動", caption: "約 100 K 以下只有 3 個平動自由度：$C_V=\\tfrac32R=12.5$ J/K。（氫在 1 atm 下 20 K 液化，曲線從那裡往上才有意義。）", to: { lt: 1.9 }, dur: 3200, hold: 1600 },
      { label: "轉動解凍", caption: "$kT$ 追上轉動能階間隔後，2 個轉動自由度加入；室溫附近 $C_V\\approx\\tfrac52R=20.8$ J/K。", to: { lt: 2.9 }, dur: 3600, hold: 1600 },
      { label: "振動解凍", caption: "1000 K 以上振動（動能＋位能 2 個自由度）開始活化，趨向 $\\tfrac72R=29.1$ J/K；約 2000 K 起氫分子開始解離。", to: { lt: 3.7 }, dur: 3600, hold: 2200 },
      { label: "固體也一樣", caption: "固體所有振動在 $T\\to0$ 時都凍結，$C\\to0$；高溫才達到 Dulong–Petit 的 $3R$（Fig. 1.14：鉛很早、鑽石很晚）。橫軸是對數：每一格是 10 倍。", dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var W = 9, top = 3.6 * H2Y;
      d.line([0, 0], [W + 0.2, 0], { color: MUTED, width: 1.3 });
      d.line([0, 0], [0, top + 0.3], { color: MUTED, width: 1.3 });
      [[1.5, "\\tfrac32R"], [2.5, "\\tfrac52R"], [3.5, "\\tfrac72R"]].forEach(function (g) {
        d.line([0, g[0] * H2Y], [W, g[0] * H2Y], { color: GRID, width: 1, dash: "4 4" });
        d.label([-0.55, g[0] * H2Y], g[1], { color: MUTED, size: 11 });
      });
      [[1, "10"], [2, "100"], [3, "1000"]].forEach(function (t) {
        d.line([H2X(t[0]), 0], [H2X(t[0]), -0.12], { color: MUTED, width: 1 });
        d.label([H2X(t[0]), -0.45], t[1], { color: MUTED, size: 11 });
      });
      d.label([W - 0.3, -0.45], "T\\ (\\text{K})", { color: MUTED, size: 11 });
      d.label([0.9, top + 0.35], "C_V", { color: MUTED, size: 12 });
      var all = [], done = [];
      for (var i = 0; i <= 120; i++) {
        var lt = 1 + 2.7 * i / 120, p = [H2X(lt), cvH2(Math.pow(10, lt)) * H2Y];
        all.push(p); if (lt <= s.lt + 1e-9) done.push(p);
      }
      d.path(all, { color: MUTED, width: 1.2, dash: "3 4" });
      done.push([H2X(s.lt), cvH2(Math.pow(10, s.lt)) * H2Y]);
      if (done.length > 1) d.path(done, { color: RED, width: 2.6 });
      d.dot([H2X(s.lt), cvH2(Math.pow(10, s.lt)) * H2Y], { color: RED, r: 5 });
      d.label([H2X(1.45), 1.5 * H2Y + 0.35], "\\text{平動}", { color: BLUE, size: 12 });
      d.label([H2X(2.5), 2.5 * H2Y + 0.35], "\\text{＋轉動}", { color: BLUE, size: 12 });
      d.label([H2X(3.45), 3.5 * H2Y + 0.35], "\\text{＋振動}", { color: BLUE, size: 12 });
    },
    formula: function (s) {
      var T = Math.pow(10, s.lt), c = cvH2(T);
      return "T=" + F(T, 0) + "\\ \\text{K}\\qquad C_V\\approx" + F(c, 2) + "R=" + F(c * 8.315, 1) + "\\ \\text{J/K}\\\\ f_{\\text{有效}}=\\dfrac{2C_V}{R}\\approx" + F(2 * c, 1);
    }
  });

  /* 2. 1 g 水的加熱曲線（1 atm）：溫度對加入的熱 */
  var HC = [   // [Q 起點, Q 終點, T 起點, T 終點, 名稱]
    [0, 41.86, -20, 0, "冰升溫"],
    [41.86, 374.86, 0, 0, "熔化"],
    [374.86, 793.46, 0, 100, "水升溫"],
    [793.46, 3053.46, 100, 100, "沸騰"],
    [3053.46, 3093.66, 100, 120, "蒸汽升溫"]
  ];
  function hcT(q) {
    for (var i = 0; i < HC.length; i++) {
      var g = HC[i];
      if (q <= g[1] + 1e-9) return { T: g[2] + (g[3] - g[2]) * (q - g[0]) / (g[1] - g[0]), i: i };
    }
    return { T: 120, i: HC.length - 1 };
  }
  var HCX = function (q) { return q / 3100 * 9.2; };
  var HCY = function (T) { return (T + 20) / 140 * 4.4; };
  A.define("t1-heat-curve", {
    title: "1 g 水從 −20°C 的冰加熱到 120°C 的蒸汽（1 atm）",
    question: "為什麼有兩段加熱時溫度完全不動？哪一段最花熱？",
    view: [440, 270], origin: [40, 226], scale: 42,
    init: { q: 0 },
    steps: [
      { label: "冰升溫", caption: "冰的比熱 2.09 J/(g·K)：升 20 K 只要 42 J，斜線很陡。", to: { q: 41.86 }, dur: 1200, hold: 1200 },
      { label: "熔化", caption: "0°C 冰水共存，溫度不變，熱用來拆晶格：熔化熱 333 J/g（80 cal/g）。這段 $C=Q/0=\\infty$。", to: { q: 374.86 }, dur: 2400, hold: 1400 },
      { label: "水升溫", caption: "水的比熱 4.186 J/(g·K)：0→100°C 共 419 J（100 cal），斜率是冰的一半。", to: { q: 793.46 }, dur: 2400, hold: 1400 },
      { label: "沸騰", caption: "100°C 水與蒸汽共存：汽化熱 2260 J/g（540 cal/g），是整條曲線最長的一段；其中約 8% 是推開大氣的功 $PV$。", to: { q: 3053.46 }, dur: 5000, hold: 1600 },
      { label: "蒸汽升溫", caption: "全部變成蒸汽後才再升溫（定壓比熱約 2.0 J/(g·K)）。加冰降溫有效、被蒸汽燙傷特別嚴重，都是潛熱的緣故。", to: { q: 3093.66 }, dur: 900, hold: 2600 }
    ],
    draw: function (d, s) {
      var W = 9.2;
      d.line([0, 0], [W + 0.2, 0], { color: MUTED, width: 1.3 });
      d.line([0, 0], [0, 4.7], { color: MUTED, width: 1.3 });
      [[0, "0^\\circ"], [100, "100^\\circ"]].forEach(function (t) {
        d.line([0, HCY(t[0])], [W, HCY(t[0])], { color: GRID, width: 1, dash: "4 4" });
        d.label([-0.5, HCY(t[0])], t[1], { color: MUTED, size: 11 });
      });
      d.label([W - 0.45, 0.4], "Q\\ (\\text{J})", { color: MUTED, size: 11 });
      d.label([0.75, 4.95], "T\\ (^\\circ\\text{C})", { color: MUTED, size: 11 });
      [1000, 2000, 3000].forEach(function (q) { d.label([HCX(q), -0.4], String(q), { color: MUTED, size: 10 }); });
      var cur = hcT(s.q);
      HC.forEach(function (g, i) {
        var a = [HCX(g[0]), HCY(g[2])], b = [HCX(g[1]), HCY(g[3])], flat = g[2] === g[3];
        d.line(a, b, { color: MUTED, width: 1.2, dash: "3 4" });
        if (s.q >= g[0]) {
          var qe = Math.min(s.q, g[1]), e = [HCX(qe), HCY(g[2] + (g[3] - g[2]) * (qe - g[0]) / (g[1] - g[0]))];
          d.line(a, e, { color: flat ? BLUE : RED, width: 2.8 });
        }
      });
      d.label([HCX(190), HCY(0) + 0.85], "\\text{熔化 }333", { color: BLUE, size: 11 });
      d.label([HCX(1923), HCY(100) + 0.35], "\\text{沸騰 }2260", { color: BLUE, size: 11 });
      d.dot([HCX(s.q), HCY(cur.T)], { color: RED, r: 5 });
    },
    formula: function (s) {
      var c = hcT(s.q), name = HC[c.i][4];
      return "\\text{" + name + "}\\qquad Q=" + F(s.q, 0) + "\\ \\text{J}\\qquad T=" + F(c.T, 1) + "^\\circ\\text{C}";
    }
  });

  /* 3. 均位定理的能量長條：U_pot = −2K、U = −K */
  A.define("t1-virial", {
    title: "重力束縛系統的能量：$U_{\\text{pot}}=-2U_{\\text{kin}}$",
    question: "恆星失去能量時，為什麼動能（溫度）反而增加？",
    view: [440, 280], origin: [56, 105], scale: 26,
    init: { K: 1 },
    steps: [
      { label: "平衡", caption: "均位定理：位能是動能的 −2 倍，總能量 $U=U_{\\text{kin}}+U_{\\text{pot}}=-U_{\\text{kin}}$，是負的（束縛）。", dur: 300, hold: 2400 },
      { label: "放光", caption: "輻射掉 0.5 份能量：$U$ 從 −1 變 −1.5。位能減少 1 份（收縮）、動能增加 0.5 份——失去能量反而變熱。", to: { K: 1.5 }, dur: 3000, hold: 2200 },
      { label: "加能量", caption: "反過來加入 0.9 份能量：$U$ 變成 −0.6，系統膨脹、動能降到 0.6——加熱反而變冷，熱容量 $C=-\\tfrac32Nk\\lt0$。", to: { K: 0.6 }, dur: 3400, hold: 2600 }
    ],
    draw: function (d, s) {
      var u = 1.7, K = s.K, bars = [[2, K, RED, "U_{\\text{kin}}"], [6.5, -2 * K, BLUE, "U_{\\text{pot}}"], [11, -K, PURPLE, "U"]];
      d.line([0, 0], [13.3, 0], { color: MUTED, width: 1.3 });
      bars.forEach(function (b) {
        var h = b[1] * u;
        d.rect(b[0] - 1.1, 0, b[0] + 1.1, h, { color: b[2], fill: b[2], fillOpacity: 0.45, width: 1 });
        d.label([b[0], h > 0 ? h + 0.45 : h - 0.5], F(b[1], 2), { color: b[2], size: 12 });
        d.label([b[0], h > 0 ? -0.45 : 0.45], b[3], { color: INK, size: 13 });
      });
      d.label([4.3, 1.8], "+", { color: MUTED, size: 16 });
      d.label([8.8, 1.8], "=", { color: MUTED, size: 16 });
    },
    formula: function (s) {
      var K = s.K;
      return "U_{\\text{kin}}=" + F(K, 2) + ",\\quad U_{\\text{pot}}=-2U_{\\text{kin}}=" + F(-2 * K, 2) + "\\\\ U=-U_{\\text{kin}}=" + F(-K, 2) + "\\qquad T\\propto U_{\\text{kin}}:\\ " + (K > 1.01 ? "\\text{變熱}" : K < 0.99 ? "\\text{變冷}" : "\\text{起點}");
    }
  });

  /* ===== 片段 D ===== */
  /* §1.7 過程的速率（代理 D）：窗戶的溫度分布、平均自由徑、三種輸運、熱方程的高斯解 */
  (function () {
    /* ---------- 1. 窗戶：玻璃＋兩層靜止空氣的溫度分布（例題 1.61、習題 1.57） ---------- */
    var RG = 0.0032 / 0.8, KA = 0.026;          // 玻璃 R 值；空氣熱導率
    function winState(a) {                       // a＝每層空氣厚度（mm）
      var Ra = a * 1e-3 / KA, q = 20 / (RG + 2 * Ra);
      return { Ra: Ra, q: q, TL: 20 - q * Ra, TR: q * Ra };
    }
    A.define("t1-window", {
      title: "單層玻璃窗：溫度降在哪裡？",
      question: "為什麼 3.2 mm 的玻璃擋不住熱，加上兩層 1 mm 的靜止空氣就差 20 倍？",
      view: [440, 260], origin: [40, 214], scale: 40,
      init: { a: 0 },
      steps: [
        { label: "只有玻璃", caption: "假設玻璃兩面就是 20°C 和 0°C（課文 1.61）：溫度在 3.2 mm 內線性下降，熱流 5000 W/m²，大得不合理。", dur: 300, hold: 2600 },
        { label: "加上靜止空氣層", caption: "實際上玻璃兩側各黏著一層約 1 mm 的靜止空氣。空氣的熱導率只有玻璃的 $1/30$，R 值卻是玻璃的近 10 倍：串聯後總 R 值變大、熱流變小。", to: { a: 1 }, dur: 3200, hold: 1800 },
        { label: "溫度大多降在空氣裡", caption: "穩態時每一層的熱流相同，所以每層的溫降 ∝ 它的 R 值（習題 1.57(c)）。玻璃只分到約 1°C，19°C 降在兩層空氣上；熱流約 250 W/m²。", dur: 300, hold: 3000 }
      ],
      draw: function (d, s) {
        var a = s.a, w = winState(a);
        function X(mm) { return (mm + 1.4) * 1.15; }
        function Y(T) { return T / 20 * 4.2; }
        // 玻璃與空氣層
        d.rect(X(0), 0, X(3.2), 4.6, { color: BLUE, fill: BLUE, fillOpacity: 0.18, width: 1.2 });
        d.label([X(1.6), 4.95], "\\text{玻璃 }3.2\\text{ mm}", { color: BLUE, size: 12 });
        if (a > 0.02) {
          d.rect(X(-a), 0, X(0), 4.6, { color: MUTED, fill: MUTED, fillOpacity: 0.12, width: 1, dash: "4 3" });
          d.rect(X(3.2), 0, X(3.2 + a), 4.6, { color: MUTED, fill: MUTED, fillOpacity: 0.12, width: 1, dash: "4 3" });
          if (a > 0.6) { d.label([X(-a / 2), 4.95], "\\text{空氣}", { color: MUTED, size: 11 }); d.label([X(3.2 + a / 2), 4.95], "\\text{空氣}", { color: MUTED, size: 11 }); }
        }
        // 座標軸
        d.line([0, 0], [X(4.6), 0], { color: MUTED, width: 1.2 });
        d.line([0, 0], [0, 4.6], { color: MUTED, width: 1.2 });
        [0, 10, 20].forEach(function (T) { d.line([-0.1, Y(T)], [0, Y(T)], { color: MUTED, width: 1 }); d.label([-0.5, Y(T)], T + "", { color: MUTED, size: 11 }); });
        d.label([-0.5, 4.95], "T(^\\circ\\text{C})", { color: MUTED, size: 11 });
        d.label([X(4.5), -0.4], "x", { color: MUTED, size: 12 });
        d.label([0.55, -0.45], "\\text{室內}", { color: INK, size: 12 });
        d.label([X(4.3), -0.45], "\\text{室外}", { color: INK, size: 12 });
        // 溫度分布
        var pts = [[0.05, Y(20)], [X(-a), Y(20)], [X(0), Y(w.TL)], [X(3.2), Y(w.TR)], [X(3.2 + a), Y(0)], [X(4.6), Y(0)]];
        d.path(pts, { color: RED, width: 3 });
        d.dot([X(0), Y(w.TL)], { color: RED, r: 4 }); d.dot([X(3.2), Y(w.TR)], { color: RED, r: 4 });
        if (a > 0.05) {
          d.label([X(0) + 0.6, Y(w.TL) + 0.5], F(w.TL, 1) + "^\\circ", { color: RED, size: 12 });
          d.label([X(3.2) - 0.6, Y(w.TR) + 0.5], F(w.TR, 1) + "^\\circ", { color: RED, size: 12 });
        }
        // 熱流箭頭：粗細 ∝ 熱流
        var thick = 1.2 + 7 * w.q / 5000;
        d.arrow([X(0.2), 1.0], [X(3.0), 1.0], { color: GREEN, width: thick, head: 10 + thick });
        d.label([X(1.6), 0.5], F(w.q, 0) + "\\ \\text{W/m}^2", { color: GREEN, size: 13 });
      },
      formula: function (s) {
        var w = winState(s.a);
        return "\\frac{Q/\\Delta t}{A}=\\frac{\\Delta T}{R_{\\text{玻}}+2R_{\\text{氣}}}\\\\[6pt]=\\frac{20}{" + F(RG, 4) + "+2\\times" + F(w.Ra, 4) + "}=" + F(w.q, 0) + "\\ \\text{W/m}^2";
      }
    });

    /* ---------- 2. 平均自由徑：掃出的圓柱（式 1.62） ---------- */
    var MOL = (function () {                     // 固定的「凍結分子」位置（偽亂數，碰撞點手動放好）
      var seed = 7, out = [];
      function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
      for (var i = 0; i < 26; i++) {
        var x = 0.6 + rnd() * 20.2, y = -4.8 + rnd() * 9.6;
        if (Math.abs(y) < 0.75 && x < 10.5) y = y < 0 ? y - 1.0 : y + 1.0;   // 碰撞點之前的帶子內不放分子
        out.push([x, y]);
      }
      out.push([9.2, 0.35]);
      return out;
    })();
    var R2 = 0.6, HIT = 9.2 - Math.sqrt(R2 * R2 - 0.35 * 0.35);
    A.define("t1-mfp", {
      title: "平均自由徑：分子掃出一根圓柱",
      question: "一個分子平均走多遠才撞到另一個分子？",
      view: [440, 240], origin: [8, 120], scale: 20,
      init: { x: 1, big: 0 },
      steps: [
        { label: "碰撞條件", caption: "假設其他分子都凍結不動。兩個半徑 $r$ 的分子，<b>中心距離</b>小於 $2r$ 就算碰撞。", dur: 300, hold: 2400 },
        { label: "換成大球＋點", caption: "等價的說法：讓移動的分子變成半徑 $2r$ 的大球，其他分子縮成點——碰撞次數完全一樣。", set: { big: 1 }, dur: 300, hold: 2400 },
        { label: "掃出圓柱", caption: "大球直線前進，掃過一根半徑 $2r$ 的圓柱（圖中的帶子）。圓柱裡一出現某個分子的中心，就撞上了。", to: { x: HIT }, dur: 4200, hold: 1400 },
        { label: "圓柱體積＝每個分子的體積", caption: "圓柱體積長到「平均每個分子分到的體積 $V/N$」時，裡面平均有一個分子：$\\pi(2r)^2\\ell\\approx V/N$。空氣：$\\ell\\approx150$ nm，約分子間距的 40 倍。", dur: 300, hold: 3200 }
      ],
      draw: function (d, s) {
        var big = s.big > 0.5, x = s.x, k = 20;
        if (big) d.rect(1, -R2, x, R2, { color: PURPLE, fill: PURPLE, fillOpacity: 0.14, width: 1, dash: "5 3" });
        MOL.forEach(function (p) {
          if (big) d.dot(p, { color: INK, r: 2.4 });
          else d.circle(p, 0.3 * k, { color: MUTED, fill: MUTED, fillOpacity: 0.25, width: 1.2 });
        });
        var hit = x >= HIT - 1e-3;
        if (hit) d.dot(MOL[MOL.length - 1], { color: RED, r: big ? 4 : 3 });
        d.circle([x, 0], (big ? R2 : 0.3) * k, { color: RED, fill: RED, fillOpacity: 0.25, width: 2 });
        d.arrow([x, 0], [x + 1.6, 0], { color: RED, width: 2, head: 8 });
        if (!big) {
          var p = MOL[MOL.length - 1];
          d.circle(p, 0.3 * k, { color: BLUE, fill: BLUE, fillOpacity: 0.25, width: 1.6 });
          d.line([p[0] - 1.6, p[1] - 1.9], [p[0] - 1.6 + 1.2, p[1] - 1.9], { color: INK, width: 1.4 });
          d.label([p[0] - 1.0, p[1] - 2.5], "2r", { color: INK, size: 12 });
        } else {
          if (x > 1.6) d.line([1, -R2 - 0.5], [x, -R2 - 0.5], { color: PURPLE, width: 1.4 });
          if (x > 1.6) d.label([(1 + x) / 2, -R2 - 1.1], "\\text{已走 }" + F((x - 1) / (HIT - 1), 2) + "\\,\\ell", { color: PURPLE, size: 12 });
          d.label([x, R2 + 0.9], "2r", { color: RED, size: 12 });
        }
      },
      formula: function (s) {
        if (s._step < 2) return "\\text{碰撞}\\iff|\\vec r_1-\\vec r_2|\\lt 2r";
        if (s._step === 2) return "V_{\\text{柱}}=\\pi(2r)^2\\,x,\\qquad x=" + F((s.x - 1) / (HIT - 1), 2) + "\\,\\ell";
        return "\\pi(2r)^2\\ell\\approx\\frac VN\\ \\Rightarrow\\ \\ell\\approx\\frac{1}{4\\pi r^2}\\frac VN\\\\=\\frac{4.1\\times10^{-26}}{4\\pi(1.5\\times10^{-10})^2}\\approx1.5\\times10^{-7}\\ \\text{m}";
      }
    });

    /* ---------- 3. 三種輸運：兩個盒子交換分子（式 1.64、習題 1.66、1.70） ---------- */
    var BOXL = [[1.0, 0.7], [2.3, 1.9], [3.6, 0.9], [4.9, 2.2], [1.7, 2.5], [4.2, 1.5], [2.9, 0.5], [5.3, 0.6], [1.2, 1.5], [3.4, 2.4]];
    var BOXU = [[1.3, 3.7], [2.6, 4.8], [3.9, 3.6], [5.1, 4.9], [1.9, 5.4], [4.5, 4.3], [3.1, 5.5], [5.4, 3.5], [0.9, 4.6], [3.6, 4.6], [2.2, 4.0], [4.8, 5.6]];
    var MODES = [
      { name: "能量（熱傳導）", law: "\\frac{Q}{A\\Delta t}=-k_t\\frac{dT}{dz}", coef: "k_t\\approx\\tfrac12\\frac{C_V}{V}\\ell\\bar v", val: "0.031\\ \\text{W/(m·K)}" },
      { name: "動量（黏滯）", law: "\\frac{|F_x|}{A}=\\eta\\frac{du_x}{dz}", coef: "\\eta\\approx\\tfrac12\\rho\\ell\\bar v", val: "4.4\\times10^{-5}\\ \\text{Pa·s}" },
      { name: "粒子（擴散）", law: "J_z=-D\\frac{dn}{dz}", coef: "D\\approx\\tfrac12\\ell\\bar v", val: "3.8\\times10^{-5}\\ \\text{m}^2/\\text{s}" }
    ];
    A.define("t1-transport", {
      title: "兩個盒子交換分子：熱導、黏滯、擴散",
      question: "為什麼三個輸運係數都長成 $\\tfrac12\\times(\\text{密度})\\times\\ell\\times\\bar v$？",
      view: [440, 280], origin: [22, 246], scale: 36,
      init: { m: 0, p: 0 },
      steps: [
        { label: "能量", caption: "上盒較熱（分子能量大，紅），下盒較冷（藍）。每個盒子厚一個自由徑 $\\ell$；一個碰撞時間內，各有一半分子穿過中線。帶上去的能量少、帶下來的多：淨熱流向下（向冷處）。", set: { m: 0, p: 0 }, to: { p: 1 }, dur: 3200, hold: 1800 },
        { label: "動量", caption: "上層流體水平速度 $u_x$ 較大（箭頭較長）。交換分子時，上盒失去 $x$ 動量、下盒得到——這就是上下兩層互相拉扯的黏滯力。", set: { m: 1, p: 0 }, to: { p: 1 }, dur: 3200, hold: 1800 },
        { label: "粒子", caption: "上盒的某種分子濃度 $n$ 較高。兩邊都是一半往對面走，但上盒本來就多：淨粒子流向下（向低濃度處）——擴散。", set: { m: 2, p: 0 }, to: { p: 1 }, dur: 3200, hold: 1800 },
        { label: "同一個公式", caption: "淨流量＝$\\tfrac12\\times$（兩盒的差）÷碰撞時間 $\\ell/\\bar v$，差＝$\\ell\\times$梯度。三個係數都是「每單位體積帶的量」$\\times\\tfrac12\\ell\\bar v$；密度和 $\\ell\\propto V/N$ 相消，所以氣體的 $k_t$、$\\eta$ 與壓力無關。", set: { m: 2 }, dur: 300, hold: 3400 }
      ],
      draw: function (d, s) {
        var m = s.m, p = s.p, W = 6;
        d.rect(0.3, 0, W, 3, { color: BLUE, fill: BLUE, fillOpacity: m === 0 ? 0.13 : 0.05, width: 1.4 });
        d.rect(0.3, 3, W, 6, { color: RED, fill: RED, fillOpacity: m === 0 ? 0.13 : 0.05, width: 1.4 });
        d.line([0, 3], [W + 0.3, 3], { color: INK, width: 2, dash: "6 4" });
        d.label([W + 0.75, 4.5], "\\text{盒 2}", { color: RED, size: 12 });
        d.label([W + 0.75, 1.5], "\\text{盒 1}", { color: BLUE, size: 12 });
        d.line([W + 0.4, 3], [W + 0.4, 6], { color: MUTED, width: 1 });
        d.label([W + 0.75, 3.4], "\\ell", { color: MUTED, size: 12 });
        d.arrow([-0.15, 0.3], [-0.15, 5.6], { color: MUTED, width: 1.2, head: 8 });
        d.label([-0.15, 6.15], "z", { color: MUTED, size: 12 });
        var up = m === 2 ? BOXU : BOXU.slice(0, 10);
        function mover(list, dir, col, len) {
          list.forEach(function (q, i) {
            var moving = i % 2 === 0, y = q[1] + (moving ? dir * 3 * p : 0);
            if (m === 1) { d.dot([q[0], y], { color: col, r: 3.5 }); d.arrow([q[0], y], [q[0] + len, y], { color: col, width: 1.6, head: 6 }); }
            else d.dot([q[0], y], { color: col, r: m === 0 ? (dir < 0 ? 5.5 : 3.5) : 4 });
          });
        }
        mover(m === 2 ? BOXL.slice(0, 6) : BOXL, +1, BLUE, 0.35);
        mover(up, -1, RED, 0.95);
        // 右側：交換的箭頭與淨流
        d.arrow([W + 2.3, 2.1], [W + 2.3, 3.9], { color: BLUE, width: 2, head: 8 });
        d.arrow([W + 3.3, 3.9], [W + 3.3, 2.1], { color: RED, width: m === 2 ? 3.6 : 2, head: 9 });
        d.label([W + 2.3, 1.55], "\\tfrac12\\text{盒 1}", { color: BLUE, size: 11 });
        d.label([W + 3.3, 4.45], "\\tfrac12\\text{盒 2}", { color: RED, size: 11 });
        d.label([W + 2.8, 5.6], MODES[m].name.replace(/（.*）/, ""), { color: INK, size: 14 });
      },
      formula: function (s) {
        var md = MODES[s.m];
        if (s._step === 3) return "k_t\\approx\\tfrac12\\frac{C_V}{V}\\ell\\bar v,\\quad\\eta\\approx\\tfrac12\\rho\\,\\ell\\bar v\\\\ D\\approx\\tfrac12\\ell\\bar v";
        return md.law + "\\\\ " + md.coef + "\\approx " + md.val;
      }
    });

    /* ---------- 4. 熱方程（擴散方程）的高斯解（習題 1.62、1.69） ---------- */
    function gauss(x, t) { return Math.exp(-x * x / (4 * t)) / Math.sqrt(t); }
    A.define("t1-spread", {
      title: "熱方程的解：一團熱慢慢攤開",
      question: "$T-T_0=\\dfrac{A}{\\sqrt t}e^{-x^2/4Kt}$ 隨時間怎麼變？",
      view: [440, 250], origin: [220, 214], scale: 40,
      init: { t: 0.25 },
      steps: [
        { label: "剛放進去", caption: "$t$ 很小：多出來的熱集中在 $x=0$ 附近，又高又窄（取 $A=K=1$ 的單位）。", dur: 300, hold: 2200 },
        { label: "攤開", caption: "峰高 $\\propto1/\\sqrt t$ 下降，寬度 $\\propto\\sqrt{Kt}$ 增加；一開始梯度大、攤得快，之後越來越慢。", to: { t: 4 }, dur: 5200, hold: 1400 },
        { label: "面積不變", caption: "曲線下的面積 $\\int(T-T_0)\\,dx=2A\\sqrt{\\pi K}$ 與 $t$ 無關：多出的熱能守恆，只是重新分布。濃度 $n$ 的擴散（Fick 第二定律）長得一模一樣。", dur: 300, hold: 3200 }
      ],
      draw: function (d, s) {
        var t = s.t, Ys = 2;
        d.line([-5.3, 0], [5.3, 0], { color: MUTED, width: 1.2 });
        d.line([0, 0], [0, 4.6], { color: MUTED, width: 1 });
        [-4, -2, 2, 4].forEach(function (x) { d.line([x, 0], [x, -0.12], { color: MUTED, width: 1 }); d.label([x, -0.42], x + "", { color: MUTED, size: 11 }); });
        d.label([5.2, -0.42], "x", { color: MUTED, size: 12 });
        d.label([0.95, 4.75], "T-T_0", { color: MUTED, size: 12 });
        [0.25, 1, 4].forEach(function (tt) {
          if (tt < t - 1e-6) { var g = []; for (var x = -5.2; x <= 5.2001; x += 0.1) g.push([x, Ys * gauss(x, tt)]); d.path(g, { color: MUTED, width: 1.2, dash: "4 3" }); }
        });
        var pts = [[-5.2, 0]];
        for (var x = -5.2; x <= 5.2001; x += 0.08) pts.push([x, Ys * gauss(x, t)]);
        pts.push([5.2, 0]);
        d.poly(pts, { color: RED, width: 2.6, fill: RED, fillOpacity: s._step === 2 ? 0.22 : 0.1 });
        var hw = Math.sqrt(4 * Math.log(2) * t);
        d.line([-hw, Ys * gauss(0, t) / 2], [hw, Ys * gauss(0, t) / 2], { color: BLUE, width: 1.6 });
        d.label([hw + 0.25, Ys * gauss(0, t) / 2 + 0.25], "\\text{半高寬}", { color: BLUE, size: 11 });
        d.label([3.6, 3.9], "t=" + F(t, 2), { color: INK, size: 14 });
      },
      formula: function (s) {
        var t = s.t;
        return "t=" + F(t, 2) + ":\\ \\text{峰高 }\\tfrac{1}{\\sqrt t}=" + F(1 / Math.sqrt(t), 2) + "\\\\ \\text{半寬 }\\sqrt{4\\ln2\\,t}=" + F(Math.sqrt(4 * Math.log(2) * t), 2) + ",\\ \\text{面積 }2\\sqrt\\pi=" + F(2 * Math.sqrt(Math.PI), 2);
      }
    });
  })();
})();
