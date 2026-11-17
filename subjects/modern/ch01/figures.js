/* 近代物理第 1 章（Beiser Relativity）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)";
  function gam(b) { return 1 / Math.sqrt(1 - b * b); }
  function frac(x) { return x - Math.floor(x); }
  function cc(x) { return Math.abs(x - 1) < 1e-9 ? "c" : F(x, 3) + "c"; }      // 速度寫成 0.8c；剛好是光速寫 c
  function P3(x) { return x < 0.1 ? String(Number(x.toPrecision(3))) : F(x, 3); }   // 小數值多留位數

  /* ---------------- 1. 光鐘（§1.2，Fig. 1.4–1.5） ---------------- */
  var L0 = 3;
  A.define("light-clock", {
    title: "光鐘：運動的鐘走一下，靜止的鐘走了 $\\gamma$ 下",
    question: "地面看，太空船裡的光鐘滴答一次要多久？",
    view: [440, 250], origin: [24, 205], scale: 36,
    init: { b: 0, ph: 0 },
    steps: [
      { label: "兩個鐘都靜止", caption: "左邊是地面上的鐘，右邊是太空船裡的鐘，還沒出發。光在相距 $L_0$ 的鏡子間來回一次就是一下：$t_0=2L_0/c$。", to: { ph: 1 }, dur: 2400, hold: 1200 },
      { label: "太空船 $0.6c$", caption: "太空船以 $0.6c$ 前進。地面看，光走斜線，斜邊比 $L_0$ 長；光速仍是 $c$，所以一下要比較久。同一段時間，左邊的鐘走了 $\\gamma=1.25$ 下。", set: { b: 0.6, ph: 0 }, to: { ph: 1 }, dur: 3200, hold: 1500 },
      { label: "太空船 $0.8c$", caption: "$0.8c$：斜邊更長。右邊的鐘走一下，左邊的鐘走了 $\\gamma=1.67$ 下——運動的鐘變慢。", set: { b: 0.8, ph: 0 }, to: { ph: 1 }, dur: 3600, hold: 1500 },
      { label: "畢氏定理", caption: "半個週期的三角形：垂直 $L_0$、水平 $vt/2$、斜邊 $ct/2$。$(ct/2)^2=L_0^2+(vt/2)^2$ 解出 $t=t_0/\\sqrt{1-v^2/c^2}$。", dur: 300, hold: 3200 }
    ],
    draw: function (d, s) {
      var g = gam(s.b), half = s.b * g * L0, x0 = 2.4;
      // 地面的鐘
      d.line([0.1, 0], [1.1, 0], { color: INK, width: 3 }); d.line([0.1, L0], [1.1, L0], { color: INK, width: 3 });
      var cyc = s.ph * g, f = frac(cyc), yr = (f < 0.5 ? f * 2 : 2 - f * 2) * L0;
      if (s.ph >= 1 && Math.abs(g - 1) < 1e-6) yr = 0;
      d.dot([0.6, yr], { color: BLUE, r: 5 });
      d.label([0.6, -0.55], "\\text{地面}", { color: MUTED, size: 12 });
      d.label([-0.0, L0 / 2], "L_0", { color: MUTED, size: 13, dx: -2 });
      // 太空船的鐘
      var xs = x0 + s.ph * 2 * half, hw = 0.5 / g;   // 鏡子沿運動方向，長度收縮成 1/γ
      if (s.b > 0.01) {
        [0, 1, 2].forEach(function (k) {
          var xg = x0 + k * half;
          d.line([xg - hw, 0], [xg + hw, 0], { color: MUTED, width: 1.2, dash: "3 4" });
          d.line([xg - hw, L0], [xg + hw, L0], { color: MUTED, width: 1.2, dash: "3 4" });
        });
        d.path([[x0, 0], [x0 + half, L0], [x0 + 2 * half, 0]], { color: RED, width: 1.4, dash: "5 4", opacity: 0.7 });
      }
      d.line([xs - hw, 0], [xs + hw, 0], { color: INK, width: 3 }); d.line([xs - hw, L0], [xs + hw, L0], { color: INK, width: 3 });
      var yp = (s.ph < 0.5 ? s.ph * 2 : 2 - s.ph * 2) * L0;
      d.dot([xs, yp], { color: RED, r: 5 });
      if (s.b > 0.01) {
        d.arrow([xs - 0.4, L0 + 0.5], [xs + 0.4, L0 + 0.5], { color: MUTED, width: 1.5, head: 8 });
        d.label([xs, L0 + 0.95], "v=" + F(s.b, 1) + "c", { color: MUTED, size: 12 });
        if (s._step === 3) {
          d.line([x0, 0], [x0 + half, 0], { color: GREEN, width: 2 });
          d.line([x0 + half, 0], [x0 + half, L0], { color: GREEN, width: 2 });
          d.label([x0 + half / 2, -0.45], "vt/2", { color: GREEN, size: 13 });
          d.label([x0 + half / 2 - 0.4, L0 / 2 + 0.4], "ct/2", { color: RED, size: 13 });
          d.label([x0 + half + 0.4, L0 / 2], "L_0", { color: GREEN, size: 13 });
        }
      }
      d.label([x0, -0.55], "\\text{太空船}", { color: MUTED, size: 12 });
    },
    formula: function (s) {
      var g = gam(s.b);
      return "\\beta=" + F(s.b, 1) + ",\\quad \\gamma=\\frac1{\\sqrt{1-" + F(s.b * s.b, 2) + "}}=" + F(g, 3) + "\\\\ t=\\gamma t_0=" + F(g, 3) + "\\,t_0";
    }
  });

  /* ---------------- 2. 光的都卜勒（§1.3） ---------------- */
  A.define("doppler-light", {
    title: "$\\nu/\\nu_0$ 和速度的關係：接近、遠離、橫向",
    question: "同樣的相對速率，三種情況的頻率差多少？",
    view: [440, 270], origin: [46, 232], scale: 40,
    init: { b: 0 },
    steps: [
      { label: "$\\beta=0$", caption: "沒有相對運動：三條曲線都從 $\\nu/\\nu_0=1$ 出發。", dur: 300, hold: 1800 },
      { label: "$0.204c$ 遠離", caption: "例題 1.3（考古 107-1）的星系：遠離 $\\nu/\\nu_0=0.813$，波長乘 $1.23$，$500\\to615\\ \\text{nm}$。", to: { b: 0.204 } },
      { label: "$0.6c$", caption: "接近變 2 倍、遠離變 $\\tfrac12$（剛好倒數），橫向只剩時間膨脹的 $0.8$。", to: { b: 0.6 } },
      { label: "$0.8c$", caption: "接近 3 倍、遠離 $\\tfrac13$——雙生子例題 1.4 的收訊間隔 3 年和 $\\tfrac13$ 年就是這兩個數。", to: { b: 0.8 } }
    ],
    draw: function (d, s) {
      d.line([0, 0], [9.2, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 4.6], { color: MUTED, width: 1.3 });
      for (var k = 1; k <= 4; k++) { d.line([0, k], [9, k], { color: "var(--grid)", width: 1 }); d.label([-0.45, k], String(k), { color: MUTED, size: 11 }); }
      [0, 0.2, 0.4, 0.6, 0.8].forEach(function (b) { d.label([b * 10, -0.4], F(b, 1), { color: MUTED, size: 11 }); });
      d.label([9.4, -0.4], "\\beta", { color: MUTED, size: 12 });
      d.label([0.4, 4.85], "\\nu/\\nu_0", { color: MUTED, size: 12 });
      var ap = [], re = [], tr = [];
      for (var i = 0; i <= 88; i++) { var b = i / 100; ap.push([b * 10, Math.sqrt((1 + b) / (1 - b))]); re.push([b * 10, Math.sqrt((1 - b) / (1 + b))]); tr.push([b * 10, Math.sqrt(1 - b * b)]); }
      d.path(ap.filter(function (p) { return p[1] < 4.5; }), { color: BLUE, width: 2.2 });
      d.path(re, { color: RED, width: 2.2 });
      d.path(tr, { color: GREEN, width: 2, dash: "6 4" });
      d.label([6.6, 3.75], "\\text{接近}", { color: BLUE, size: 12 });
      d.label([3.0, 0.42], "\\text{遠離}", { color: RED, size: 12 });
      d.label([5.5, 1.05], "\\text{橫向}", { color: GREEN, size: 12 });
      var b0 = s.b, x = b0 * 10;
      d.line([x, 0], [x, 4.4], { color: MUTED, width: 1, dash: "3 4" });
      d.dot([x, Math.sqrt((1 + b0) / (1 - b0))], { color: BLUE });
      d.dot([x, Math.sqrt((1 - b0) / (1 + b0))], { color: RED });
      d.dot([x, Math.sqrt(1 - b0 * b0)], { color: GREEN });
    },
    formula: function (s) {
      var b = s.b;
      return "\\beta=" + F(b, 3) + ":\\ \\sqrt{\\tfrac{1+\\beta}{1-\\beta}}=" + F(Math.sqrt((1 + b) / (1 - b)), 3) + ",\\ \\sqrt{\\tfrac{1-\\beta}{1+\\beta}}=" + F(Math.sqrt((1 - b) / (1 + b)), 3) + ",\\ \\sqrt{1-\\beta^2}=" + F(Math.sqrt(1 - b * b), 3);
    }
  });

  /* ---------------- 3. 緲子（§1.4，Fig. 1.9） ---------------- */
  A.define("muon", {
    title: "緲子：地面看壽命變長，緲子看距離變短",
    question: "壽命只有 $2.2\\ \\mu\\text{s}$ 的緲子為什麼飛得到 10 km 外的地面？",
    view: [440, 300], origin: [40, 272], scale: 24,
    init: { cl: 0, gr: 0, mu: 0, showR: 0 },
    steps: [
      { label: "不考慮相對論", caption: "$v=0.998c$、壽命 $2.2\\ \\mu\\text{s}$：只能飛 $vt_0=0.66\\ \\text{km}$，遠到不了地面。", to: { cl: 1 } },
      { label: "地面：時間膨脹", caption: "地面看緲子在動，壽命 $\\gamma t_0=34.8\\ \\mu\\text{s}$（$\\gamma=15.8$），可以飛 $10.4\\ \\text{km}$，到得了地面。", to: { gr: 1 }, dur: 2800 },
      { label: "緲子：長度收縮", caption: "跟著緲子看，壽命仍是 $2.2\\ \\mu\\text{s}$，但地面以 $0.998c$ 迎面而來，$10.4\\ \\text{km}$ 縮成 $10.4/15.8=0.66\\ \\text{km}$——剛好飛得到。", set: { showR: 1 }, to: { mu: 1 }, dur: 2800, hold: 2600 }
    ],
    draw: function (d, s) {
      var H = 10.4;
      // 左：地面座標系
      d.line([0.5, 0], [6.5, 0], { color: GREEN, width: 3 });
      d.line([1, 0], [1, H], { color: MUTED, width: 1.2 });
      d.line([0.8, H], [1.2, H], { color: MUTED, width: 1.2 });
      d.label([1.0, H + 0.6], "10.4\\ \\text{km}", { color: MUTED, size: 11 });
      d.label([3.5, -0.6], "\\text{地面座標系}", { color: MUTED, size: 12 });
      var yc = H - 0.66 * s.cl;
      if (s.cl > 0) { d.circle([3, yc], 6, { color: MUTED, width: 1.5, dash: "3 3" }); if (s.cl > 0.95 && s.gr < 0.05) d.label([4.6, yc], "\\times\\ \\text{衰變}", { color: MUTED, size: 12 }); }
      var yg = H - H * s.gr;
      if (s.gr > 0) { d.dot([4.5, yg], { color: RED, r: 6 }); d.line([4.5, H], [4.5, yg], { color: RED, width: 1.2, dash: "4 4", opacity: 0.6 }); }
      // 右：緲子座標系
      if (s.showR) {
        var top = H, h = 0.66, xr = 11.5;
        d.dot([xr, top], { color: RED, r: 6 });
        var yy = top - h * (1 - s.mu);   // 地面從 h=0.66 km 外迎面而來，緲子壽命結束時剛好到
        d.line([xr - 2.6, yy], [xr + 3, yy], { color: GREEN, width: 3 });
        d.arrow([xr + 2.4, yy - 1.4], [xr + 2.4, yy - 0.2], { color: GREEN, width: 1.5, head: 8 });
        d.label([xr + 3.2, yy - 0.8], "0.998c", { color: GREEN, size: 11 });
        d.line([xr - 2.2, top], [xr - 2.2, top - h], { color: MUTED, width: 1.2 });
        d.label([xr - 3.8, top - h / 2], "h=0.66\\ \\text{km}", { color: MUTED, size: 11 });
        if (s.mu > 0.95) d.label([xr + 1.8, top + 0.7], "\\text{到地面時衰變}", { color: MUTED, size: 11 });
        d.label([xr, H - 4], "\\text{緲子座標系}", { color: MUTED, size: 12 });
        d.label([xr, H - 5], "\\text{高度 }h=h_0/\\gamma", { color: MUTED, size: 12 });
      }
    },
    formula: function (s) {
      if (s.showR) return "h=\\frac{h_0}{\\gamma}=\\frac{10.4\\ \\text{km}}{15.8}=0.66\\ \\text{km}=vt_0";
      if (s.gr > 0) return "t=\\gamma t_0=\\frac{2.2\\ \\mu\\text{s}}{\\sqrt{1-0.998^2}}=34.8\\ \\mu\\text{s}\\\\ vt=10.4\\ \\text{km}";
      return "vt_0=(2.994\\times10^8)(2.2\\times10^{-6})=0.66\\ \\text{km}";
    }
  });

  /* ---------------- 4. 雙生子時空圖（§1.5，例題 1.4） ---------------- */
  A.define("twin", {
    title: "雙生子的時空圖：Dick 每年發一次訊號",
    question: "Jane 什麼時候收到 Dick 的訊號？",
    view: [400, 320], origin: [70, 292], scale: 5.2,
    init: { tau: 0 },
    steps: [
      { label: "世界線", caption: "橫軸是距離（光年）、縱軸是 Jane 的時間（年）。Jane 停在 $x=0$；Dick 以 $0.8c$ 在第 25 年到達 20 光年處，第 50 年回來。", dur: 300, hold: 2200 },
      { label: "去程訊號", caption: "Dick 每過自己的 1 年發一次（圖上每 3 年畫一條）。訊號以光速（$45^\\circ$ 斜線）傳回，Jane 每 3 年收到一個，直到第 45 年。", to: { tau: 15 }, dur: 3200 },
      { label: "回程訊號", caption: "回程的訊號擠在最後 5 年，每 $\\tfrac13$ 年收到一個。總共 $15+15=30$ 個：Dick 只老了 30 歲。", to: { tau: 30 }, dur: 3200, hold: 2600 }
    ],
    draw: function (d, s) {
      d.line([0, 0], [24, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 54], { color: MUTED, width: 1.3 });
      [10, 20].forEach(function (x) { d.label([x, -3], String(x), { color: MUTED, size: 11 }); });
      [10, 20, 25, 30, 40, 45, 50].forEach(function (t) { d.line([-0.8, t], [0, t], { color: MUTED, width: 1 }); d.label([-5, t], String(t), { color: MUTED, size: 10 }); });
      d.label([26, -3], "x\\,(\\text{ly})", { color: MUTED, size: 11 });
      d.label([4, 54], "t\\,(\\text{y})", { color: MUTED, size: 11 });
      d.line([0, 0], [0, 50], { color: BLUE, width: 3 });
      d.path([[0, 0], [20, 25], [0, 50]], { color: RED, width: 2.5 });
      d.label([21.5, 25], "\\text{恆星}", { color: RED, size: 11, dx: 8 });
      d.label([-6, 35], "\\text{Jane}", { color: BLUE, size: 11 });
      d.label([12, 11], "\\text{Dick}", { color: RED, size: 11 });
      for (var tau = 0; tau <= s.tau + 1e-6; tau += 3) {
        var t, x;
        if (tau <= 15) { t = tau * 5 / 3; x = tau * 4 / 3; } else { var u = tau - 15; t = 25 + u * 5 / 3; x = 20 - u * 4 / 3; }
        if (tau > 0) d.line([x, t], [0, t + x], { color: PURPLE, width: 1.2, dash: "4 3" });
        d.dot([x, t], { color: RED, r: 3 });
        d.dot([0, t + x], { color: PURPLE, r: 3 });
      }
    },
    formula: function (s) {
      var tau = s.tau, arr = tau <= 15 ? 3 * tau : 45 + (tau - 15) / 3;
      return "\\tau_{\\text{Dick}}=" + F(tau, 1) + "\\ \\text{y}\\ \\Rightarrow\\ t_{\\text{Jane 收到}}=" + F(arr, 1) + "\\ \\text{y}" + (tau <= 15 ? "=3\\tau" : "\\\\ =45+\\tfrac{\\tau-15}{3}");
    }
  });

  /* ---------------- 5. 平行電流（§1.6，Fig. 1.12） ---------------- */
  A.define("wires", {
    title: "平行電流：換到電荷的座標系，磁力變成電力",
    question: "兩條電中性的導線為什麼會互相吸引？",
    view: [440, 230], origin: [20, 200], scale: 40,
    init: { mode: 0, ph: 0 },
    steps: [
      { label: "實驗室", caption: "正電荷以 $v$ 向右、負電荷以 $v$ 向左。兩者間距收縮相同，導線 II 仍是中性，但兩導線互相吸引（實驗室把它叫作「磁力」）。$\\lambda_\\pm$ 是 II 中正、負電荷的線電荷密度大小。", set: { mode: 0, ph: 0 }, to: { ph: 1 }, dur: 2800, hold: 1600 },
      { label: "導線 I 的負電荷看", caption: "II 的負電荷和我同速、靜止，間距不縮；II 的正電荷以 $2v$ 運動，縮得更密。II 帶淨正電，吸引我。", set: { mode: 1, ph: 0 }, to: { ph: 1 }, dur: 2800, hold: 1800 },
      { label: "導線 I 的正電荷看", caption: "這次 II 的負電荷較密，II 帶淨負電，同樣吸引正電荷。所有電荷都被另一條導線吸引。", set: { mode: 2, ph: 0 }, to: { ph: 1 }, dur: 2800, hold: 2200 }
    ],
    draw: function (d, s) {
      var yI = 3.4, yII = 1.0;
      [yI, yII].forEach(function (y) { d.rect(0, y - 0.45, 10.4, y + 0.45, { color: MUTED, width: 1.2, fill: "var(--soft)" }); });
      d.label([10.4, yI + 0.75], "\\text{I}", { color: MUTED, size: 12 });
      d.label([10.4, yII + 0.75], "\\text{II}", { color: MUTED, size: 12 });
      // 間距：0 實驗室；1 負電荷系；2 正電荷系
      var sp = [[1.0, 1.0], [0.7, 1.25], [1.25, 0.7]][s.mode];   // [正, 負] 在 II 中的間距（誇大）
      var vel = [[1, -1], [2, 0], [0, -2]][s.mode];
      function row(y, spacing, v, sign, col) {
        var off = frac(s.ph * v * 0.35 / spacing) * spacing;
        for (var x = off + 0.2; x < 10.3; x += spacing) {
          d.circle([x, y + (sign > 0 ? 0.17 : -0.17)], 6.5, { color: col, width: 1.3, fill: "var(--paper)" });
          d.label([x, y + (sign > 0 ? 0.17 : -0.17)], sign > 0 ? "+" : "-", { color: col, size: 12 });
        }
      }
      row(yII, sp[0], vel[0], 1, RED);
      row(yII, sp[1], vel[1], -1, BLUE);
      row(yI, sp[0], vel[0], 1, RED);
      row(yI, sp[1], vel[1], -1, BLUE);
      if (s.mode === 1) d.circle([5.2, yI - 0.17], 10, { color: BLUE, width: 2.5 });
      if (s.mode === 2) d.circle([5.2, yI + 0.17], 10, { color: RED, width: 2.5 });
      var net = ["\\text{II 中性}", "\\text{II 帶淨正電}", "\\text{II 帶淨負電}"][s.mode];
      d.label([5.2, -0.15], net, { color: [MUTED, RED, BLUE][s.mode], size: 13 });
      if (s.mode > 0) d.arrow([5.2, yI - 0.6], [5.2, yII + 0.9], { color: PURPLE, width: 2, head: 9 });
      else { d.arrow([3.0, yI - 0.6], [3.0, yI - 1.0], { color: PURPLE, width: 2, head: 8 }); d.arrow([3.0, yII + 0.6], [3.0, yII + 1.0], { color: PURPLE, width: 2, head: 8 }); d.label([4.1, (yI + yII) / 2], "\\text{「磁力」}", { color: PURPLE, size: 12 }); }
    },
    formula: function (s) {
      return ["\\text{實驗室：}\\ \\lambda_+=\\lambda_-\\ \\Rightarrow\\ \\text{中性，但有「磁力」}", "\\text{負電荷系：}\\ \\lambda_+>\\lambda_-\\ \\Rightarrow\\ \\text{電力吸引}", "\\text{正電荷系：}\\ \\lambda_->\\lambda_+\\ \\Rightarrow\\ \\text{電力吸引}"][s.mode];
    }
  });

  /* ---------------- 6. 動量曲線（§1.7，Fig. 1.14） ---------------- */
  A.define("momentum-curve", {
    title: "$\\gamma mv$ 和 $mv$：低速相同，接近 $c$ 時發散",
    question: "速度越接近 $c$，動量怎麼變？",
    view: [440, 260], origin: [50, 222], scale: 45,
    init: { b: 0.1 },
    steps: [
      { label: "$0.1c$", caption: "低速時兩條曲線幾乎重合，只差 0.5%。", dur: 300, hold: 1800 },
      { label: "$0.6c$", caption: "$\\gamma=1.25$：相對論動量大了 25%。", to: { b: 0.6 } },
      { label: "$0.9c$", caption: "$\\gamma=2.29$。", to: { b: 0.9 } },
      { label: "$\\to c$", caption: "$v\\to c$ 時 $\\gamma mv\\to\\infty$：給有限的動量（有限的衝量）永遠到不了光速。", to: { b: 0.97 }, hold: 2400 }
    ],
    draw: function (d, s) {
      d.line([0, 0], [8.4, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 4.3], { color: MUTED, width: 1.3 });
      for (var k = 1; k <= 4; k++) { d.line([0, k], [8, k], { color: "var(--grid)", width: 1 }); d.label([-0.55, k], (k === 1 ? "" : k) + "mc", { color: MUTED, size: 10 }); }
      [0.2, 0.4, 0.6, 0.8, 1.0].forEach(function (b) { d.label([b * 8, -0.4], F(b, 1), { color: MUTED, size: 11 }); });
      d.line([8, 0], [8, 4.2], { color: MUTED, width: 1, dash: "2 4" });
      d.label([8.5, -0.4], "v/c", { color: MUTED, size: 11 });
      var r = [], c = [];
      for (var i = 0; i <= 97; i++) { var b = i / 100; r.push([b * 8, gam(b) * b]); c.push([b * 8, b]); }
      d.path(r.filter(function (p) { return p[1] < 4.2; }), { color: RED, width: 2.3 });
      d.path(c, { color: BLUE, width: 2, dash: "6 4" });
      d.label([5.7, 3.2], "\\gamma mv", { color: RED, size: 13 });
      d.label([6.6, 0.45], "mv", { color: BLUE, size: 13 });
      d.dot([s.b * 8, gam(s.b) * s.b], { color: RED });
      d.dot([s.b * 8, s.b], { color: BLUE });
    },
    formula: function (s) {
      return "\\beta=" + F(s.b, 2) + ":\\ \\frac{p}{mc}=\\gamma\\beta=" + F(gam(s.b) * s.b, 3) + "\\\\ \\frac{\\gamma mv}{mv}=\\gamma=" + F(gam(s.b), 3);
    }
  });

  /* ---------------- 7. 動能曲線（§1.8，Fig. 1.16） ---------------- */
  A.define("ke-curve", {
    title: "$KE/mc^2$：相對論 $(\\gamma-1)$ 與古典 $\\tfrac12\\beta^2$",
    question: "古典公式在多快的時候開始不準？",
    view: [440, 260], origin: [52, 222], scale: 45,
    init: { b: 0.1 },
    steps: [
      { label: "$0.1c$", caption: "低速兩條曲線重合（古典只低估 0.8%）：$(\\gamma-1)\\approx\\tfrac12\\beta^2$ 就是二項式近似。", dur: 300, hold: 1800 },
      { label: "$0.5c$", caption: "古典低估 19%。", to: { b: 0.5 } },
      { label: "$0.866c$", caption: "$\\gamma=2$，動能等於靜能（習題 1-29）。古典只給 $0.375mc^2$。", to: { b: 0.866 } },
      { label: "$\\to c$", caption: "古典說 $KE=\\tfrac12mc^2$ 就到光速（藍線終點）；相對論需要無限大的動能。", to: { b: 0.92 }, hold: 2400 }
    ],
    draw: function (d, s) {
      var Y = 2.5;   // 縱軸 1 單位 = 0.4 mc²
      d.line([0, 0], [8.4, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 4.3], { color: MUTED, width: 1.3 });
      [0.4, 0.8, 1.2, 1.6].forEach(function (k) { d.line([0, k * Y], [8, k * Y], { color: "var(--grid)", width: 1 }); d.label([-0.55, k * Y], F(k, 1), { color: MUTED, size: 10 }); });
      [0.2, 0.4, 0.6, 0.8, 1.0].forEach(function (b) { d.label([b * 8, -0.4], F(b, 1), { color: MUTED, size: 11 }); });
      d.label([8.5, -0.4], "v/c", { color: MUTED, size: 11 });
      d.label([0.7, 4.55], "KE/mc^2", { color: MUTED, size: 11 });
      var r = [], c = [];
      for (var i = 0; i <= 100; i++) { var b = i / 100; if (b < 0.97) r.push([b * 8, (gam(b) - 1) * Y]); c.push([b * 8, 0.5 * b * b * Y]); }
      d.path(r.filter(function (p) { return p[1] < 4.2; }), { color: RED, width: 2.3 });
      d.path(c, { color: BLUE, width: 2, dash: "6 4" });
      d.label([5.2, 2.6], "(\\gamma-1)", { color: RED, size: 13 });
      d.label([7.3, 0.6], "\\tfrac12\\beta^2", { color: BLUE, size: 13 });
      d.dot([s.b * 8, (gam(s.b) - 1) * Y], { color: RED });
      d.dot([s.b * 8, 0.5 * s.b * s.b * Y], { color: BLUE });
    },
    formula: function (s) {
      var r = gam(s.b) - 1, c = 0.5 * s.b * s.b;
      return "\\beta=" + F(s.b, 3) + ":\\ \\gamma-1=" + P3(r) + ",\\ \\tfrac12\\beta^2=" + P3(c) + "\\ (\\text{低估 }" + F((1 - c / r) * 100, 1) + "\\%)";
    }
  });

  /* ---------------- 8. 能量–動量三角形（§1.9） ---------------- */
  A.define("ep-triangle", {
    title: "$E^2=(mc^2)^2+(pc)^2$：一個直角三角形",
    question: "動量增加時 $E$ 怎麼變？光子對應什麼三角形？",
    view: [440, 250], origin: [90, 215], scale: 60,
    init: { pc: 0, mm: 1 },
    steps: [
      { label: "靜止", caption: "$p=0$：三角形壓成一條線，$E=mc^2$（靜能）。", dur: 300, hold: 1800 },
      { label: "$0.6c$", caption: "$pc=\\gamma\\beta\\,mc^2=0.75\\,mc^2$，斜邊 $E=1.25\\,mc^2$。底邊 $mc^2$ 永遠不變——它是不變量。", to: { pc: 1.5 } },
      { label: "$0.8c$", caption: "$pc=1.33\\,mc^2$，$E=1.67\\,mc^2$。速度 $v/c=pc/E=0.8$，就是高（$pc$）與斜邊（$E$）的比。", to: { pc: 2.667 } },
      { label: "$m\\to0$", caption: "把質量縮到 0（固定 $pc$）：三角形變成一條直立的線，$E=pc$，$v/c=pc/E=1$——無質量粒子一定以光速運動。", to: { mm: 0 }, hold: 2600 }
    ],
    draw: function (d, s) {
      var mc = 2 * s.mm, pc = s.pc, E = Math.sqrt(mc * mc + pc * pc);
      d.line([0, 0], [mc, 0], { color: BLUE, width: 3 });
      d.line([mc, 0], [mc, pc], { color: GREEN, width: 3 });
      d.line([0, 0], [mc, pc], { color: RED, width: 3 });
      if (pc > 0.2 && mc > 0.3) d.rightAngle([mc, 0], [-1, 0], [0, 1], 0.22);
      if (mc > 0.3) d.label([mc / 2, -0.4], "mc^2", { color: BLUE, size: 13 });
      if (pc > 0.3) d.label([mc + 0.55, pc / 2], "pc", { color: GREEN, size: 13 });
      if (E > 0.3) d.label([mc / 2 - 0.45, pc / 2 + 0.25], "E", { color: RED, size: 14 });
    },
    formula: function (s) {
      var mc = s.mm, pc = s.pc / 2, E = Math.sqrt(mc * mc + pc * pc);
      return "(\\text{單位：原本的 }mc^2)\\quad mc^2=" + F(mc, 2) + ",\\ pc=" + F(pc, 2) + "\\\\ E=\\sqrt{" + F(mc, 2) + "^2+" + F(pc, 2) + "^2}=" + F(E, 3) + ",\\quad \\frac vc=\\frac{pc}{E}=" + F(E > 0 ? pc / E : 0, 3);
    }
  });

  /* ---------------- 9. 速度相加（附錄 I） ---------------- */
  A.define("velocity-add", {
    title: "速度相加：伽利略 vs 勞倫茲",
    question: "兩個小於 $c$ 的速度相加，會不會超過 $c$？",
    view: [440, 230], origin: [20, 196], scale: 260,
    init: { v: 0.9, vp: 0.5 },
    steps: [
      { label: "例題 1.11", caption: "Alpha 對地 $0.90c$，Beta 對 Alpha $0.50c$。伽利略相加 $1.40c$，相對論只有 $0.97c$。", dur: 300, hold: 2400 },
      { label: "砲彈", caption: "太空船 $0.5c$ 發射對它 $0.5c$ 的砲彈：$0.8c$，不是 $c$。", to: { v: 0.5, vp: 0.5 } },
      { label: "車燈", caption: "車速 $0.5c$，車燈的光對車是 $c$：對地仍是 $c$。", to: { vp: 1 }, hold: 2600 }
    ],
    draw: function (d, s) {
      var rel = (s.v + s.vp) / (1 + s.v * s.vp), gal = s.v + s.vp;
      d.line([1, -0.05], [1, 0.62], { color: MUTED, width: 1.2, dash: "3 4" });
      d.label([1, 0.67], "c", { color: MUTED, size: 12 });
      d.arrow([0, 0.5], [s.v, 0.5], { color: BLUE, width: 4, head: 10 }); d.label([0, 0.5], "v", { color: BLUE, size: 12, dx: -10 });
      d.arrow([s.v, 0.38], [s.v + s.vp, 0.38], { color: GREEN, width: 4, head: 10 }); d.label([s.v + s.vp * 0.3, 0.44], "V'_x", { color: GREEN, size: 12 });
      d.arrow([0, 0.2], [gal, 0.2], { color: MUTED, width: 3, head: 10, dash: "6 4" }); d.label([gal / 2, 0.27], "\\text{伽利略 }" + F(gal, 2) + "c", { color: MUTED, size: 11 });
      d.arrow([0, 0.05], [rel, 0.05], { color: RED, width: 4, head: 10 }); d.label([rel / 2, 0.12], cc(rel), { color: RED, size: 12 });
    },
    formula: function (s) {
      var rel = (s.v + s.vp) / (1 + s.v * s.vp);
      return "V_x=\\frac{V'_x+v}{1+vV'_x/c^2}=\\frac{" + F(s.vp, 2) + "+" + F(s.v, 2) + "}{1+(" + F(s.v, 2) + ")(" + F(s.vp, 2) + ")}c=" + cc(rel);
    }
  });

  /* ---------------- 10. 同時的相對性（附錄 I，考古 107-4） ---------------- */
  A.define("simultaneity", {
    title: "同時的相對性：Anna 的兩支閃光燈",
    question: "Anna 看同時的兩個閃光，Bob 看誰先？",
    view: [440, 300], origin: [220, 150], scale: 80,
    init: { b: 0 },
    steps: [
      { label: "平板車靜止", caption: "$v=0$：兩座標系一樣。兩手相距 $2\\ \\text{m}$，閃光事件 W、E 在同一條水平線上（同時）。", dur: 300, hold: 2000 },
      { label: "$v=0.6c$ 往東", caption: "Anna 的 $x'$ 軸（她的「同時線」）傾斜，斜率 $\\beta$；W、E 仍在這條線上。投影到 Bob 的時間軸：W 在下、E 在上——西邊先閃。（Bob 量到兩事件相距 $\\gamma\\Delta x'=2.5\\ \\text{m}$：兩事件在 Bob 系不同時，所以這不是長度收縮。）", to: { b: 0.6 }, dur: 2600, hold: 2600 },
      { label: "時間差", caption: "$c\\Delta t=\\gamma\\beta\\,\\Delta x'=(1.25)(0.6)(2\\ \\text{m})=1.5\\ \\text{m}$，所以 $\\Delta t=(1.5\\ \\text{m})/(3\\times10^8\\ \\text{m/s})=5.0\\ \\text{ns}$。", dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var b = s.b, g = gam(b);
      d.line([-2.4, 0], [2.4, 0], { color: MUTED, width: 1.3 }); d.line([0, -1.7], [0, 1.7], { color: MUTED, width: 1.3 });
      d.label([2.55, -0.12], "x\\,(\\text{東})", { color: MUTED, size: 12, dx: 8 }); d.label([0.18, 1.8], "ct", { color: MUTED, size: 12 });
      d.line([-1.7, -1.7], [1.7, 1.7], { color: "var(--grid)", width: 1.2 }); d.line([-1.7, 1.7], [1.7, -1.7], { color: "var(--grid)", width: 1.2 });
      if (b > 0.01) {
        d.line([-2.3, -2.3 * b], [2.3, 2.3 * b], { color: GREEN, width: 1.6 }); d.label([2.45, 2.3 * b + 0.1], "x'", { color: GREEN, size: 12 });
        d.line([-1.7 * b, -1.7], [1.7 * b, 1.7], { color: GREEN, width: 1.6 }); d.label([1.7 * b + 0.18, 1.8], "ct'", { color: GREEN, size: 12 });
      }
      var W = [-g, -g * b], E = [g, g * b];
      d.line(W, [0, W[1]], { color: BLUE, width: 1, dash: "3 4" });
      d.line(E, [0, E[1]], { color: RED, width: 1, dash: "3 4" });
      d.dot(W, { color: BLUE, r: 6 }); d.dot(E, { color: RED, r: 6 });
      d.label([W[0] - 0.2, W[1] + 0.22], "W", { color: BLUE, size: 13 });
      d.label([E[0] + 0.2, E[1] + 0.22], "E", { color: RED, size: 13 });
    },
    formula: function (s) {
      var b = s.b, g = gam(b);
      return "\\beta=" + F(b, 2) + ",\\ \\gamma=" + F(g, 3) + ":\\quad c(t_E-t_W)=\\gamma\\beta\\,\\Delta x'=" + F(g * b * 2, 2) + "\\ \\text{m}\\ \\Rightarrow\\ \\Delta t=" + F(g * b * 2 / 3e8 * 1e9, 2) + "\\ \\text{ns}";
    }
  });

  /* ---------------- 11. 光錐（附錄 II，Fig. 1.25） ---------------- */
  A.define("light-cone", {
    title: "光錐：類時、類光、類空",
    question: "事件 2 在哪裡時，能和事件 1 有因果關係？",
    view: [440, 300], origin: [220, 150], scale: 55,
    init: { x: 0.5, t: 1.8 },
    steps: [
      { label: "類時", caption: "事件 2 在未來光錐內：$c\\Delta t>|\\Delta x|$，$(\\Delta s)^2>0$。比光慢的訊號就能從 1 到 2，可能有因果。", dur: 300, hold: 2200 },
      { label: "類光", caption: "事件 2 在光錐面上：只有光能連起兩事件，$\\Delta s=0$。", to: { x: 1.6, t: 1.6 } },
      { label: "類空", caption: "事件 2 在光錐外：任何訊號都來不及，$(\\Delta s)^2<0$，兩事件完全無關；總能找到一個座標系看它們同時。", to: { x: 2.4, t: 0.9 } },
      { label: "過去", caption: "事件 2 在過去光錐內：它可能影響了事件 1。對所有觀察者它都在「過去」。", to: { x: -0.6, t: -1.6 }, hold: 2400 }
    ],
    draw: function (d, s) {
      d.line([-3.6, 0], [3.6, 0], { color: MUTED, width: 1.3 }); d.line([0, -2.5], [0, 2.5], { color: MUTED, width: 1.3 });
      d.label([3.75, -0.15], "x", { color: MUTED, size: 12 }); d.label([0.25, 2.6], "ct", { color: MUTED, size: 12 });
      d.poly([[0, 0], [2.5, 2.5], [-2.5, 2.5]], { color: "none", fill: BLUE, fillOpacity: 0.12, width: 0 });
      d.poly([[0, 0], [2.5, -2.5], [-2.5, -2.5]], { color: "none", fill: PURPLE, fillOpacity: 0.12, width: 0 });
      d.line([-2.5, -2.5], [2.5, 2.5], { color: INK, width: 1.4 }); d.line([-2.5, 2.5], [2.5, -2.5], { color: INK, width: 1.4 });
      d.label([-1.6, 2.2], "\\text{未來光錐}", { color: BLUE, size: 11 });
      d.label([-1.6, -2.2], "\\text{過去光錐}", { color: PURPLE, size: 11 });
      d.label([3.0, -0.8], "\\text{無關}", { color: MUTED, size: 11 }); d.label([-3.0, -0.8], "\\text{無關}", { color: MUTED, size: 11 });
      d.dot([0, 0], { color: INK, r: 5 }); d.label([-0.35, 0.25], "1", { color: INK, size: 12 });
      d.line([0, 0], [s.x, s.t], { color: RED, width: 1.4, dash: "4 4" });
      d.dot([s.x, s.t], { color: RED, r: 6 }); d.label([s.x + 0.3, s.t + 0.15], "2", { color: RED, size: 12 });
    },
    formula: function (s) {
      var ds2 = s.t * s.t - s.x * s.x, kind = Math.abs(ds2) < 0.02 ? "\\text{類光}" : (ds2 > 0 ? "\\text{類時}" : "\\text{類空}");
      return "(\\Delta s)^2=(c\\Delta t)^2-(\\Delta x)^2=" + F(Math.abs(s.t), 2) + "^2-" + F(Math.abs(s.x), 2) + "^2=" + F(ds2, 2) + "\\ \\Rightarrow\\ " + kind;
    }
  });
})();
