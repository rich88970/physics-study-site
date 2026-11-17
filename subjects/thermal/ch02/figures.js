/* 熱學第 2 章（Schroeder, The Second Law）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)", GRID = "var(--grid)";

  /* ln n!：n ≤ 1200 用累加表，精確 */
  var LF = [0];
  for (var i = 1; i <= 1200; i++) LF[i] = LF[i - 1] + Math.log(i);
  function lnC(n, k) { return (k < 0 || k > n) ? -Infinity : LF[n] - LF[k] - LF[n - k]; }
  function lnEin(N, q) { return lnC(q + N - 1, q); }                 // 愛因斯坦固體 Ω(N,q)
  function sci(lnv, d) {                                            // e^lnv 寫成 a×10^b
    var l = lnv / Math.LN10, e = Math.floor(l), m = Math.pow(10, l - e);
    if (m >= 9.995) { m = 1; e += 1; }
    if (e >= -2 && e <= 3) return F(Math.exp(lnv), e < 0 ? 4 : 2);
    return F(m, d == null ? 2 : d) + "\\times10^{" + e + "}";
  }
  function pct(p) { return p >= 0.001 ? F(100 * p, 1) + "\\%" : sci(Math.log(p)); }

  /* ---------------- 1. 硬幣的機率分布（§2.1） ---------------- */
  var COIN_N = [4, 10, 20, 50, 100];
  A.define("t2-coins", {
    title: "$N$ 枚硬幣：$n$ 個正面的機率",
    question: "硬幣越多，正面比例離一半太遠的機率怎麼變？",
    view: [440, 270], origin: [46, 222], scale: 40,
    init: { c: 0 },
    steps: [
      { label: "$N=4$", caption: "習題 2.1：16 個微觀態分給 5 個巨觀態，多重度 $1,4,6,4,1$。高度都除以中間那根，橫軸用正面比例 $n/N$。", dur: 300, hold: 2200 },
      { label: "$N=10$", caption: "考古 115-3：$2^{10}=1024$ 個微觀態、11 個巨觀態。$n=7$ 的機率 $120/1024=11.7\\%$。", set: { c: 1 }, dur: 300, hold: 2200 },
      { label: "$N=20$", caption: "考古 114-6：12 正 8 反的機率 12.0%。分布開始集中在 $n/N=0.5$ 附近。", set: { c: 2 }, dur: 300, hold: 2200 },
      { label: "$N=50$", caption: "習題 2.3：$P(25)=0.112$，但 $P(40)$ 只有 $9\\times10^{-6}$——比例 0.8 的長條已經看不到。", set: { c: 3 }, dur: 300, hold: 2400 },
      { label: "$N=100$", caption: "最可能的巨觀態本身只有 8%，可是比例偏離 0.5 超過 0.2 的機率只剩 $10^{-4}$ 量級：相對寬度 $\\propto1/\\sqrt N$。", set: { c: 4 }, dur: 300, hold: 2800 }
    ],
    draw: function (d, s) {
      var N = COIN_N[s.c], mid = lnC(N, Math.floor(N / 2)), W = 9, H = 4;
      d.line([0, 0], [W + 0.3, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, H + 0.4], { color: MUTED, width: 1.3 });
      [0, 0.25, 0.5, 0.75, 1].forEach(function (f) { d.line([f * W, 0], [f * W, -0.12], { color: MUTED, width: 1 }); d.label([f * W, -0.4], F(f, 2), { color: MUTED, size: 11 }); });
      d.label([W / 2, -0.9], "n/N", { color: MUTED, size: 12 });
      d.label([0.15, H + 0.75], "P(n)/P_{\\max}", { color: MUTED, size: 12, dx: 30 });
      d.line([0, H], [W, H], { color: GRID, width: 1 });
      var w = Math.min(0.8, 0.85 * W / (N + 1));
      for (var n = 0; n <= N; n++) {
        var h = H * Math.exp(lnC(N, n) - mid), x = n / N * W;
        if (h > 0.004) d.rect(x - w / 2, 0, x + w / 2, h, { color: BLUE, fill: BLUE, fillOpacity: 0.55, width: 0.6 });
      }
    },
    formula: function (s) {
      var N = COIN_N[s.c], m = Math.floor(N / 2), tot = N * Math.LN2, tail = 0;
      for (var n = 0; n <= N; n++) if (Math.abs(n / N - 0.5) >= 0.2 - 1e-9) tail += Math.exp(lnC(N, n) - tot);
      return "N=" + N + ":\\quad P(" + m + ")=\\frac{\\binom{" + N + "}{" + m + "}}{2^{" + N + "}}=" + F(Math.exp(lnC(N, m) - tot), 3) +
        "\\\\ P\\left(\\left|\\tfrac nN-\\tfrac12\\right|\\ge0.2\\right)=" + (tail > 0.01 ? F(tail, 3) : sci(Math.log(tail)));
    }
  });

  /* ---------------- 2. 點與線（§2.2，習題 2.7） ---------------- */
  var PAIRS = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]];
  function seq(k) { var p = PAIRS[k], out = []; for (var j = 0; j < 5; j++) out.push(j === p[0] || j === p[1] ? 1 : 0); return out; }
  function occ(sq) { var o = [0], c = 0; sq.forEach(function (v) { if (v) o[c]++; else { c++; o[c] = 0; } }); return o; }
  function drawSeq(d, sq, x0, y, dx, r, bh, col) {
    sq.forEach(function (v, j) {
      var x = x0 + j * dx;
      if (v) d.dot([x, y], { color: col, r: r }); else d.line([x, y - bh], [x, y + bh], { color: INK, width: r > 5 ? 3 : 1.6 });
    });
  }
  A.define("t2-dots", {
    title: "點與線：4 個振子、2 份能量",
    question: "為什麼 $\\Omega(N,q)=\\binom{q+N-1}{q}$？",
    view: [440, 250], origin: [16, 236], scale: 20,
    init: { k: 0 },
    steps: [
      { label: "一串符號", caption: "2 個點（能量）和 3 條隔線（分開 4 個振子）排成 5 個位置。這一串是「第 1、2 位放點」：第一個振子有 2 份，其餘 0 份。", dur: 300, hold: 2600 },
      { label: "逐一列出", caption: "點換位置就是換一個微觀態。5 個位置選 2 個放點，所有排法依序出現在下方。", to: { k: 9.999 }, dur: 9000, hold: 1200 },
      { label: "數完", caption: "共 $\\binom52=10$ 種，和習題 2.5(d) 窮舉的 10 種相同。一般地，$q$ 個點、$N-1$ 條線：$\\binom{q+N-1}{q}$。", dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var k = Math.min(9, Math.floor(s.k)), sq = seq(k), o = occ(sq);
      drawSeq(d, sq, 5.5, 9.4, 2.6, 9, 1.2, RED);
      d.label([11.0, 7.2], "(q_1,q_2,q_3,q_4)=(" + o.join(",") + ")", { color: INK, size: 14 });
      for (var j = 0; j < 10; j++) {
        var col = j % 5, row = Math.floor(j / 5), x0 = 1.2 + col * 4.1, y = row ? 1.4 : 4.2;
        if (j === k) d.rect(x0 - 0.6, y - 1.0, x0 + 3.4, y + 1.0, { color: RED, width: 1.4, fill: RED, fillOpacity: 0.08 });
        drawSeq(d, seq(j), x0, y, 0.7, j <= s.k ? 3.4 : 2.4, 0.5, j <= s.k ? RED : MUTED);
      }
    },
    formula: function (s) {
      var k = Math.min(9, Math.floor(s.k)), p = PAIRS[k];
      return "\\text{點在第 }" + (p[0] + 1) + "," + (p[1] + 1) + "\\text{ 位}\\quad(\\text{第 }" + (k + 1) + "\\text{ 種})\\\\ \\Omega(4,2)=\\binom{2+4-1}{2}=\\binom52=10";
    }
  });

  /* ---------------- 3. 兩個固體分能量（§2.3） ---------------- */
  var SOL = [[3, 3, 6, "Fig. 2.4"], [3, 2, 5, "考古 114-4"], [10, 20, 60, "考古 115-5"], [300, 200, 100, "Fig. 2.5"]];
  function peaks(r) { var mx = Math.max.apply(null, r), out = []; r.forEach(function (v, i) { if (Math.abs(v - mx) < 1e-9) out.push(i); }); return out; }
  function solRows(c) {
    var NA = SOL[c][0], NB = SOL[c][1], q = SOL[c][2], r = [];
    for (var a = 0; a <= q; a++) r.push(lnEin(NA, a) + lnEin(NB, q - a));
    return r;
  }
  A.define("t2-two-solids", {
    title: "兩個愛因斯坦固體：$\\Omega_{\\text{total}}$ 對 $q_A$",
    question: "能量最可能怎麼分？系統變大時峰怎麼變？",
    view: [440, 270], origin: [46, 222], scale: 40,
    init: { c: 0 },
    steps: [
      { label: "$3,3,6$", caption: "Fig. 2.4：$\\Omega_{\\text{total}}=28,63,90,100,90,63,28$，共 462 個微觀態。各 3 份最可能（21.6%）。", dur: 300, hold: 2400 },
      { label: "$3,2,5$", caption: "考古 114-4：$6,15,24,30,30,21$。$q_A=3,4$ 並列最大，能量大致照振子數 $3:2$ 分。", set: { c: 1 }, dur: 300, hold: 2400 },
      { label: "$10,20,60$", caption: "考古 115-5：61 個巨觀態，峰在 $q_A=19$（不是照比例的 20），機率 6.3%；全在 A 只有 $2.5\\times10^{-13}$。", set: { c: 2 }, dur: 300, hold: 2600 },
      { label: "$300,200,100$", caption: "Fig. 2.5：峰在 $q_A=60$，峰是 $q_A=0$ 那一端的 $2.5\\times10^{33}$ 倍（$q_A=100$ 那端是 $4\\times10^{18}$ 倍）。$q_A<30$ 或 $>90$ 的總機率不到百萬分之一。", set: { c: 3 }, dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var c = s.c, q = SOL[c][2], r = solRows(c), mx = Math.max.apply(null, r), W = 9, H = 4, tops = peaks(r);
      d.line([0, 0], [W + 0.3, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, H + 0.4], { color: MUTED, width: 1.3 });
      [0, Math.floor(q / 2), q].forEach(function (a) { d.label([a / q * W, -0.4], String(a), { color: MUTED, size: 11 }); });
      d.label([W / 2, -0.9], "q_A", { color: MUTED, size: 12 });
      d.label([0.15, H + 0.75], "\\Omega_{\\text{total}}/\\Omega_{\\max}", { color: MUTED, size: 12, dx: 40 });
      var w = Math.min(0.9, 0.82 * W / (q + 1));
      for (var a = 0; a <= q; a++) {
        var h = H * Math.exp(r[a] - mx), x = a / q * W, top = tops.indexOf(a) >= 0;
        if (h > 0.004) d.rect(x - w / 2, 0, x + w / 2, h, { color: top ? RED : BLUE, fill: top ? RED : BLUE, fillOpacity: 0.55, width: 0.6 });
      }
      var xm = (tops[0] + tops[tops.length - 1]) / 2 / q * W;
      d.label([xm, H + 0.3], "q_A=" + tops.join(","), { color: RED, size: 12 });
    },
    formula: function (s) {
      var c = s.c, NA = SOL[c][0], NB = SOL[c][1], q = SOL[c][2], r = solRows(c), mx = Math.max.apply(null, r), tops = peaks(r);
      var lt = lnEin(NA + NB, q), mn = Math.min.apply(null, r);
      return "N_A=" + NA + ",\\ N_B=" + NB + ",\\ q=" + q + "\\\\ \\Omega(\\text{all})=\\binom{" + (q + NA + NB - 1) + "}{" + q + "}=" + sci(lt) +
        "\\\\ P(q_A=" + tops.join(") = P(q_A=") + ")=" + pct(Math.exp(mx - lt)) + (tops.length > 1 ? "\\\\ " : ",\\quad") + "\\frac{\\Omega_{\\max}}{\\Omega_{\\min}}=" + sci(mx - mn);
    }
  });

  /* ---------------- 4. Stirling 近似的誤差（§2.4） ---------------- */
  function stirErr(N) { return 1 - Math.exp(N * Math.log(N) - N + 0.5 * Math.log(2 * Math.PI * N) - LF[N]); }
  function lnErr(N) { return 1 - (N * Math.log(N) - N) / LF[N]; }
  A.define("t2-stirling", {
    title: "Stirling 近似有多準",
    question: "$N$ 要多大，$N!\\approx N^Ne^{-N}\\sqrt{2\\pi N}$ 和 $\\ln N!\\approx N\\ln N-N$ 才夠準？",
    view: [440, 270], origin: [52, 226], scale: 40,
    init: { lg: 0 },
    steps: [
      { label: "$N=1$", caption: "$1!=1$，完整式給 0.922（差 7.8%，課本表寫 7.7%）；$\\ln1!=0$ 而 $N\\ln N-N=-1$，對數形式完全不能用。", dur: 300, hold: 2200 },
      { label: "$N=10$", caption: "Table 2.3：完整式差 0.83%；對數形式 15.1 對 13.0，差 13.8%。", to: { lg: 1 }, dur: 2400, hold: 2200 },
      { label: "$N=50$", caption: "習題 2.15：完整式差 0.17%，對數形式差 1.9%。", to: { lg: Math.log(50) / Math.LN10 }, dur: 1800, hold: 2200 },
      { label: "$N=100$", caption: "完整式差 0.083%（約 $1/12N$），對數形式差 0.89%：少掉的正是 $\\tfrac12\\ln(2\\pi N)$。$N\\sim10^{23}$ 時兩者都無誤差可言。", to: { lg: 2 }, dur: 1800, hold: 3000 }
    ],
    draw: function (d, s) {
      var W = 9, H = 4, ymax = 0.16;
      d.line([0, 0], [W + 0.3, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, H + 0.3], { color: MUTED, width: 1.3 });
      [1, 10, 100].forEach(function (N, j) { d.label([j * W / 2, -0.4], String(N), { color: MUTED, size: 11 }); d.line([j * W / 2, 0], [j * W / 2, -0.12], { color: MUTED, width: 1 }); });
      d.label([W / 2 + 1.1, -0.9], "N", { color: MUTED, size: 12 });
      [0.05, 0.1, 0.15].forEach(function (y) { d.line([0, y / ymax * H], [W, y / ymax * H], { color: GRID, width: 1 }); d.label([-0.55, y / ymax * H], F(100 * y, 0) + "\\%", { color: MUTED, size: 10 }); });
      var p1 = [], p2 = [];
      for (var N = 1; N <= 100; N++) {
        var x = Math.log(N) / Math.LN10 * W / 2;
        p1.push([x, Math.min(H, stirErr(N) / ymax * H)]);
        if (N >= 2) { var e2 = lnErr(N); if (e2 <= ymax * 1.02) p2.push([x, e2 / ymax * H]); }
      }
      d.path(p1, { color: BLUE, width: 2.2 }); d.path(p2, { color: RED, width: 2.2 });
      d.label([1.2, 2.55], "N^Ne^{-N}\\sqrt{2\\pi N}", { color: BLUE, size: 12 });
      d.label([6.3, 3.3], "N\\ln N-N", { color: RED, size: 12 });
      var Nc = Math.max(1, Math.round(Math.pow(10, s.lg))), xc = Math.log(Nc) / Math.LN10 * W / 2;
      d.line([xc, 0], [xc, H], { color: MUTED, width: 1, dash: "3 4" });
      d.dot([xc, Math.min(H, stirErr(Nc) / ymax * H)], { color: BLUE });
      if (Nc >= 3) d.dot([xc, lnErr(Nc) / ymax * H], { color: RED });
    },
    formula: function (s) {
      var N = Math.max(1, Math.round(Math.pow(10, s.lg)));
      var st = N * Math.log(N) - N + 0.5 * Math.log(2 * Math.PI * N);
      return "N=" + N + ":\\quad N!=" + sci(LF[N], 4) + "\\\\ N^Ne^{-N}\\sqrt{2\\pi N}=" + sci(st, 4) + "\\ (" + F(100 * stirErr(N), 3) + "\\%)" +
        "\\\\ \\ln N!=" + F(LF[N], 2) + ",\\quad N\\ln N-N=" + F(N * Math.log(N) - N, 2) + (N > 1 ? "\\ (" + F(100 * lnErr(N), 2) + "\\%)" : "");
    }
  });

  /* ---------------- 5. 高溫與低溫極限（§2.4） ---------------- */
  function fEin(x) { return (1 + x) * Math.log(1 + x) - x * Math.log(x); }
  A.define("t2-limits", {
    title: "$\\ln\\Omega/N$ 對 $q/N$：高溫與低溫極限",
    question: "$(eq/N)^N$ 和 $(eN/q)^q$ 各在什麼範圍才準？",
    view: [440, 300], origin: [50, 250], scale: 40,
    init: { lx: 0, hi: 0, lo: 0 },
    steps: [
      { label: "一般式", caption: "大 $N,q$ 時 $\\ln\\Omega/N\\approx(1+x)\\ln(1+x)-x\\ln x$，$x=q/N$（(2.18) 除以 $N$）。橫軸是對數刻度。", dur: 300, hold: 2400 },
      { label: "高溫 $q\\gg N$", caption: "$(eq/N)^N$ 給 $\\ln\\Omega/N=\\ln x+1$（藍虛線）：$x=100$ 時幾乎重合，$x=1$ 時已經低估 28%。", set: { hi: 1 }, to: { lx: 2 }, dur: 2600, hold: 2400 },
      { label: "低溫 $q\\ll N$", caption: "$(eN/q)^q$ 給 $\\ln\\Omega/N=x(1-\\ln x)$（綠虛線）：只在 $x\\ll1$ 時準，大多數振子沒有能量。", set: { lo: 1 }, to: { lx: -2 }, dur: 3200, hold: 2400 },
      { label: "$q=N$", caption: "$x=1$ 兩個極限都不準：要用一般式，$\\ln\\Omega/N=2\\ln2=1.39$（變化題 9）。", to: { lx: 0 }, dur: 2200, hold: 2800 }
    ],
    draw: function (d, s) {
      var W = 9, ys = 0.65;
      function X(lx) { return (lx + 2) / 4 * W; }
      d.line([0, 0], [W + 0.3, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 6 * ys + 0.3], { color: MUTED, width: 1.3 });
      [-2, -1, 0, 1, 2].forEach(function (k) { d.label([X(k), -0.4], k < 0 ? F(Math.pow(10, k), 2) : String(Math.pow(10, k)), { color: MUTED, size: 11 }); d.line([X(k), 0], [X(k), -0.12], { color: MUTED, width: 1 }); });
      d.label([W / 2 + 1.1, -0.9], "q/N", { color: MUTED, size: 12 });
      [2, 4, 6].forEach(function (y) { d.line([0, y * ys], [W, y * ys], { color: GRID, width: 1 }); d.label([-0.45, y * ys], String(y), { color: MUTED, size: 10 }); });
      d.label([0.2, 6 * ys + 0.55], "\\ln\\Omega/N", { color: MUTED, size: 12, dx: 22 });
      var pe = [], ph = [], pl = [];
      for (var j = 0; j <= 160; j++) {
        var lx = -2 + j / 40, x = Math.pow(10, lx);
        pe.push([X(lx), fEin(x) * ys]);
        var h = Math.log(x) + 1; if (h >= 0) ph.push([X(lx), h * ys]);
        var l = x * (1 - Math.log(x)); if (l >= 0 && l <= 6.2) pl.push([X(lx), l * ys]);
      }
      d.path(pe, { color: INK, width: 2.4 });
      if (s.hi) { d.path(ph, { color: BLUE, width: 2, dash: "6 4" }); d.label([X(1.2), 5.2 * ys], "\\ln\\tfrac{eq}N", { color: BLUE, size: 12 }); }
      if (s.lo) { d.path(pl, { color: GREEN, width: 2, dash: "6 4" }); d.label([X(-0.9), 1.6 * ys], "\\tfrac qN\\ln\\tfrac{eN}q", { color: GREEN, size: 12 }); }
      var xc = Math.pow(10, s.lx);
      d.line([X(s.lx), 0], [X(s.lx), 6 * ys], { color: MUTED, width: 1, dash: "3 4" });
      d.dot([X(s.lx), fEin(xc) * ys], { color: RED });
    },
    formula: function (s) {
      var x = Math.pow(10, s.lx), out = "x=\\frac qN=" + F(x, x < 0.1 ? 3 : 2) + "\\\\ (1+x)\\ln(1+x)-x\\ln x=" + F(fEin(x), 3);
      if (s.hi) out += "\\\\ \\ln x+1=" + F(Math.log(x) + 1, 3);
      if (s.lo) out += ",\\quad x(1-\\ln x)=" + F(x * (1 - Math.log(x)), 3);
      return out;
    }
  });

  /* ---------------- 6. 峰變尖（§2.4，習題 2.21） ---------------- */
  var SHARP_N = [1, 10, 100, 1000, 10000];
  A.define("t2-sharp", {
    title: "$[4z(1-z)]^N$：峰隨 $N$ 變尖",
    question: "兩個相同固體的多重度，峰寬怎麼隨 $N$ 縮小？",
    view: [440, 260], origin: [40, 214], scale: 40,
    init: { c: 0 },
    steps: [
      { label: "$N=1$", caption: "$z=q_A/q$。(2.22) 除以峰高後是 $[4z(1-z)]^N$：$N=1$ 是一條平緩的拋物線。", dur: 300, hold: 2000 },
      { label: "$N=10$", caption: "取 10 次方，中間比旁邊大一點點的差距被放大。", set: { c: 1 }, dur: 300, hold: 2000 },
      { label: "$N=100$", caption: "$1/e$ 半寬約 $1/(2\\sqrt N)=0.05$。", set: { c: 2 }, dur: 300, hold: 2000 },
      { label: "$N=1000$", caption: "半寬 0.016。", set: { c: 3 }, dur: 300, hold: 2000 },
      { label: "$N=10^4$", caption: "半寬 0.005。$N=10^{20}$ 時是 $5\\times10^{-11}$——整張圖寬 10 萬公里才畫得出 1 公分寬的峰（Fig. 2.7）。", set: { c: 4 }, dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var W = 9, H = 4;
      d.line([0, 0], [W + 0.3, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, H + 0.3], { color: MUTED, width: 1.3 });
      [0, 0.5, 1].forEach(function (f) { d.label([f * W, -0.4], F(f, 1), { color: MUTED, size: 11 }); });
      d.label([W / 2 + 0.9, -0.9], "z", { color: MUTED, size: 12 });
      d.label([-0.4, H], "1", { color: MUTED, size: 11 });
      var cols = [MUTED, GREEN, BLUE, PURPLE, RED];
      for (var c = 0; c <= s.c; c++) {
        var N = SHARP_N[c], pts = [];
        for (var j = 0; j <= 600; j++) { var z = j / 600, v = Math.pow(4 * z * (1 - z), N); pts.push([z * W, v * H]); }
        d.path(pts, { color: cols[c], width: c === s.c ? 2.6 : 1.4, opacity: c === s.c ? 1 : 0.55 });
      }
      var Nn = SHARP_N[s.c], hw = 0.5 * Math.sqrt(1 - Math.exp(-1 / Nn));
      d.line([(0.5 - hw) * W, H / Math.E], [(0.5 + hw) * W, H / Math.E], { color: INK, width: 1.4 });
      d.label([(0.5 + hw) * W + 0.25, H / Math.E + 0.3], "1/e", { color: INK, size: 11, dx: 8 });
    },
    formula: function (s) {
      var N = SHARP_N[s.c], hw = 0.5 * Math.sqrt(1 - Math.exp(-1 / N));
      return "N=" + N + ":\\quad\\text{半寬 }\\Delta z=" + F(hw, 4) + "\\\\ \\approx\\frac1{2\\sqrt N}=" + F(0.5 / Math.sqrt(N), 4);
    }
  });

  /* ---------------- 7. 相空間的格子（§2.5，Fig. 2.9） ---------------- */
  var CELLS = [2, 3, 4, 6, 12];
  A.define("t2-cells", {
    title: "一維粒子的獨立狀態：$LL_p/h$ 格",
    question: "把位置切細，狀態數會變多嗎？",
    view: [440, 260], origin: [70, 220], scale: 40,
    init: { c: 0 },
    steps: [
      { label: "$\\Delta x=L/2$", caption: "設 $LL_p=12h$。位置只分 2 格，每格 $\\Delta x=L/2$；測不準原理 $\\Delta x\\Delta p_x\\approx h$ 讓動量要分得很粗：$\\Delta p_x=L_p/6$。共 $2\\times6=12$ 格。", dur: 300, hold: 2600 },
      { label: "$\\Delta x=L/3$", caption: "位置 3 格、動量 4 格：仍是 12。", set: { c: 1 }, dur: 300, hold: 2000 },
      { label: "$\\Delta x=L/4$", caption: "位置 4 格、動量 3 格：仍是 12。", set: { c: 2 }, dur: 300, hold: 2000 },
      { label: "$\\Delta x=L/6$", caption: "位置 6 格、動量 2 格。", set: { c: 3 }, dur: 300, hold: 2000 },
      { label: "$\\Delta x=L/12$", caption: "位置切得最細，動量就只剩 1 格。不論怎麼切，獨立狀態數都是 $\\frac{L}{\\Delta x}\\cdot\\frac{L_p}{\\Delta p_x}=\\frac{LL_p}h=12$；三維時 $\\Omega_1=VV_p/h^3$。", set: { c: 4 }, dur: 300, hold: 3200 }
    ],
    draw: function (d, s) {
      var nx = CELLS[s.c], np = 12 / nx, W = 7.2, H = 4.2;
      for (var i = 0; i < nx; i++) for (var j = 0; j < np; j++) {
        var x0 = i * W / nx, y0 = j * H / np;
        d.rect(x0, y0, x0 + W / nx, y0 + H / np, { color: BLUE, width: 1.2, fill: (i + j) % 2 ? BLUE : GREEN, fillOpacity: 0.16 });
      }
      d.rect(0, 0, W, H, { color: INK, width: 2 });
      d.label([W / 2, -0.4], "x\\ (\\text{長度 }L)", { color: MUTED, size: 12 });
      d.label([-0.95, H / 2], "p_x", { color: MUTED, size: 12 });
      d.label([-0.95, H / 2 - 0.5], "(L_p)", { color: MUTED, size: 11 });
      d.label([W / nx / 2, H + 0.35], "\\Delta x", { color: RED, size: 12 });
      d.label([W + 0.55, H - H / np / 2], "\\Delta p_x", { color: RED, size: 12, dx: 6 });
    },
    formula: function (s) {
      var nx = CELLS[s.c], np = 12 / nx;
      return "\\frac L{\\Delta x}\\times\\frac{L_p}{\\Delta p_x}=" + nx + "\\times" + np + "=12=\\frac{LL_p}h\\\\ \\Delta x\\,\\Delta p_x=\\frac L{" + nx + "}\\cdot\\frac{L_p}{" + np + "}=\\frac{LL_p}{12}=h";
    }
  });

  /* ---------------- 8. 取對數把峰抹平（§2.6） ---------------- */
  A.define("t2-logpeak", {
    title: "多重度很尖，熵很平",
    question: "對 $q_A$ 作圖，$\\Omega_{\\text{total}}$ 和 $S/k=\\ln\\Omega_{\\text{total}}$ 長得一樣嗎？",
    view: [440, 270], origin: [46, 222], scale: 40,
    init: { qa: 60, sh: 0 },
    steps: [
      { label: "$\\Omega_{\\text{total}}$", caption: "Fig. 2.5 的系統（$N_A=300,N_B=200,q=100$）：多重度在 $q_A=60$ 有尖峰，離開 30 就小到看不見。", dur: 300, hold: 2400 },
      { label: "$S/k$", caption: "同一個系統畫 $S/k=\\ln\\Omega_{\\text{total}}$：從 187.5 到 264.4，平緩的拱形。取對數把峰抹平了（習題 2.29）。", set: { sh: 1 }, dur: 300, hold: 2600 },
      { label: "同一個最大值", caption: "兩條曲線的最大值都在 $q_A=60$：「多重度最大」和「熵最大」是同一句話。$q_A$ 移到 30，熵只少 6%，多重度卻小了 $4\\times10^{6}$ 倍。", to: { qa: 30 }, dur: 3000, hold: 3000 }
    ],
    draw: function (d, s) {
      var r = solRows(3), mx = r[60], W = 9, H = 4, Smax = mx;
      d.line([0, 0], [W + 0.3, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, H + 0.4], { color: MUTED, width: 1.3 });
      [0, 50, 100].forEach(function (a) { d.label([a / 100 * W, -0.4], String(a), { color: MUTED, size: 11 }); });
      d.label([W / 2 + 1.1, -0.9], "q_A", { color: MUTED, size: 12 });
      var p1 = [], p2 = [];
      for (var a = 0; a <= 100; a++) { p1.push([a / 100 * W, H * Math.exp(r[a] - mx)]); p2.push([a / 100 * W, H * r[a] / Smax]); }
      d.path(p1, { color: BLUE, width: 2.4 });
      d.label([3.6, H + 0.35], "\\Omega_{\\text{total}}/\\Omega_{\\max}", { color: BLUE, size: 12 });
      if (s.sh) { d.path(p2, { color: RED, width: 2.4 }); d.label([8.2, H * r[90] / Smax + 0.35], "S/S_{\\max}", { color: RED, size: 12 }); }
      var a0 = Math.round(s.qa), x0 = a0 / 100 * W;
      d.line([x0, 0], [x0, H], { color: MUTED, width: 1, dash: "3 4" });
      d.dot([x0, H * Math.exp(r[a0] - mx)], { color: BLUE });
      if (s.sh) d.dot([x0, H * r[a0] / Smax], { color: RED });
    },
    formula: function (s) {
      var r = solRows(3), a = Math.round(s.qa);
      return "q_A=" + a + ":\\quad\\Omega_{\\text{total}}=" + sci(r[a]) + "=" + sci(r[a] - r[60]) + "\\,\\Omega_{\\max}\\\\ \\frac Sk=" + F(r[a], 1) + "=" + F(r[a] / r[60], 3) + "\\,\\frac{S_{\\max}}k";
    }
  });

  /* ---------------- 9. 熵對能量：固體與順磁體（§2.6，考古某級-3(d)） ---------------- */
  function sPara(u) { var a = (1 - u) / 2, b = (1 + u) / 2, f = function (p) { return p > 0 ? p * Math.log(p) : 0; }; return -f(a) - f(b); }
  A.define("t2-s-vs-u", {
    title: "$S(U)$：愛因斯坦固體與兩態順磁體",
    question: "加能量一定讓熵增加嗎？斜率代表什麼？",
    view: [440, 240], origin: [36, 196], scale: 50,
    init: { x: 0.2, u: -0.8, st: 0 },
    steps: [
      { label: "固體", caption: "愛因斯坦固體 $S/Nk=(1+x)\\ln(1+x)-x\\ln x$，$x=U/N\\epsilon$：一直上升、越來越平。切線斜率 $\\partial S/\\partial U$ 越來越小。", to: { x: 3 }, dur: 3600, hold: 2000 },
      { label: "順磁體", caption: "順磁體 $U=\\mu B(N-2N_\\uparrow)$ 從 $-N\\mu B$（全部向上）到 $+N\\mu B$：兩端 $S=0$，$U=0$ 時最大 $Nk\\ln2$。", set: { st: 1 }, to: { u: 0 }, dur: 2600, hold: 2000 },
      { label: "負斜率", caption: "$U>0$（多數偶極反平行於外場）時斜率為負。第 3 章定義 $1/T=\\partial S/\\partial U$，這一半就是負溫度。", to: { u: 0.8 }, dur: 2600, hold: 3000 }
    ],
    draw: function (d, s) {
      // 左：固體（x 0..4，y = S/Nk，0..2.6）
      d.line([0, 0], [4.2, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 2.7], { color: MUTED, width: 1.3 });
      d.label([3.7, -0.62], "U/N\\epsilon", { color: MUTED, size: 11 }); d.label([0.55, 2.85], "S/Nk", { color: MUTED, size: 11 });
      [1, 2, 3, 4].forEach(function (k) { d.label([k, -0.3], String(k), { color: MUTED, size: 10 }); });
      [1, 2].forEach(function (k) { d.line([-0.08, k], [0, k], { color: MUTED, width: 1 }); d.label([-0.3, k], String(k), { color: MUTED, size: 10 }); });
      var pts = [];
      for (var j = 1; j <= 200; j++) { var x = j / 50; pts.push([x, fEin(x)]); }
      pts.unshift([0, 0]);
      d.path(pts, { color: BLUE, width: 2.4 });
      var x0 = s.x, m = Math.log((1 + x0) / x0);
      d.line([x0 - 0.5, fEin(x0) - 0.5 * m], [x0 + 0.5, fEin(x0) + 0.5 * m], { color: INK, width: 1.4 });
      d.dot([x0, fEin(x0)], { color: BLUE });
      // 右：順磁體（u -1..1 → 寬 2.4，y = 3 S/Nk）
      var ox = 6.0, sx = 1.2, sy = 3;
      d.line([ox - sx, 0], [ox + sx + 0.15, 0], { color: MUTED, width: 1.3 }); d.line([ox, 0], [ox, 2.4], { color: MUTED, width: 1.3 });
      d.label([ox - sx, -0.3], "-1", { color: MUTED, size: 10 }); d.label([ox + sx, -0.3], "1", { color: MUTED, size: 10 });
      d.label([ox + sx + 0.25, -0.62], "U/N\\mu B", { color: MUTED, size: 11 });
      [0.2, 0.4, 0.6].forEach(function (v) { d.line([ox - 0.08, v * sy], [ox, v * sy], { color: MUTED, width: 1 }); d.label([ox - 0.32, v * sy], F(v, 1), { color: MUTED, size: 10 }); });
      d.line([ox - 0.12, Math.LN2 * sy], [ox + 0.12, Math.LN2 * sy], { color: MUTED, width: 1, dash: "2 3" });
      d.label([ox + 0.45, Math.LN2 * sy + 0.22], "\\ln2", { color: MUTED, size: 10 });
      if (s.st) {
        var pp = [];
        for (var k = 0; k <= 200; k++) { var u = -1 + k / 100; pp.push([ox + u * sx, sPara(u) * sy]); }
        d.path(pp, { color: RED, width: 2.4 });
        var u0 = s.u, a = (1 - u0) / 2, b = (1 + u0) / 2, mu = 0.5 * Math.log(a / b) * sy / sx;
        d.line([ox + u0 * sx - 0.45, sPara(u0) * sy - 0.45 * mu], [ox + u0 * sx + 0.45, sPara(u0) * sy + 0.45 * mu], { color: INK, width: 1.4 });
        d.dot([ox + u0 * sx, sPara(u0) * sy], { color: RED });
        if (u0 > 0.05) d.label([ox + 1.25 * sx, 1.3], "T<0", { color: RED, size: 12 });
      }
    },
    formula: function (s) {
      var x = s.x, out = "\\text{固體 }x=" + F(x, 2) + ":\\ \\ \\text{斜率 }\\ln\\frac{1+x}x=" + F(Math.log((1 + x) / x), 3);
      if (s.st) {
        var u = s.u, sl = 0.5 * Math.log((1 - u) / (1 + u));
        out += "\\\\ \\text{順磁體 }u=\\tfrac U{N\\mu B}=" + F(u, 2) + ":\\ \\ \\text{斜率 }\\tfrac12\\ln\\frac{N_\\uparrow}{N_\\downarrow}=" + F(sl, 3) + (Math.abs(u) < 0.005 ? "\\ (T=\\infty)" : (sl > 0 ? "\\ (T>0)" : "\\ (T<0)"));
      }
      return out;
    }
  });

  /* ---------------- 10. Sackur–Tetrode 在低溫失效（§2.6，習題 2.35） ---------------- */
  var S300 = 15.17;
  function sHe(T) { return S300 + 1.5 * Math.log(T / 300); }
  A.define("t2-sackur", {
    title: "氦的 $S/Nk$：密度固定、溫度下降",
    question: "Sackur–Tetrode 公式在什麼溫度給出不合理的負熵？",
    view: [440, 290], origin: [52, 206], scale: 30,
    init: { lt: Math.log(300) / Math.LN10 },
    steps: [
      { label: "$300\\ \\text{K}$", caption: "室溫、一大氣壓：$S=15.2\\,Nk=126\\ \\text{J/K}$（一莫耳）。", dur: 300, hold: 2200 },
      { label: "$3\\ \\text{K}$", caption: "密度固定時 $S/Nk=15.2+\\tfrac32\\ln(T/300\\ \\text{K})$；溫度降 100 倍，熵只少 $1.5\\ln100=6.9$。", to: { lt: Math.log(3) / Math.LN10 }, dur: 2600, hold: 2200 },
      { label: "$0.012\\ \\text{K}$", caption: "再降到 $0.012\\ \\text{K}$，公式給 $S=0$；更低就變負——不可能。這時分子的量子波長和間距相當，要用第 7 章的量子統計（習題 2.35）。", to: { lt: Math.log(0.0122) / Math.LN10 }, dur: 3000, hold: 3000 }
    ],
    draw: function (d, s) {
      var ys = 1 / 3;
      function X(lt) { return (lt + 3) * 2; }
      d.rect(0, -1.7, 12, 0, { color: "none", fill: RED, fillOpacity: 0.08, width: 0 });
      d.line([0, 0], [12.3, 0], { color: MUTED, width: 1.3 }); d.line([0, -1.7], [0, 6], { color: MUTED, width: 1.3 });
      [-3, -2, -1, 0, 1, 2, 3].forEach(function (k) { d.line([X(k), 0], [X(k), -0.15], { color: MUTED, width: 1 }); d.label([X(k), -0.55], k < 0 ? F(Math.pow(10, k), 3) : String(Math.pow(10, k)), { color: MUTED, size: 10 }); });
      d.label([8.4, -1.15], "T\\ (\\text{K})", { color: MUTED, size: 11 });
      [5, 10, 15].forEach(function (v) { d.line([0, v * ys], [12, v * ys], { color: GRID, width: 1 }); d.label([-0.55, v * ys], String(v), { color: MUTED, size: 10 }); });
      d.label([0.5, 6.35], "S/Nk", { color: MUTED, size: 12, dx: 10 });
      d.label([2.6, -1.2], "S<0\\ \\text{不合理}", { color: RED, size: 11 });
      var pts = [];
      for (var j = 0; j <= 120; j++) { var lt = -3 + j / 20; pts.push([X(lt), sHe(Math.pow(10, lt)) * ys]); }
      d.path(pts.filter(function (p) { return p[1] > -1.7; }), { color: BLUE, width: 2.4 });
      var T = Math.pow(10, s.lt);
      d.dot([X(s.lt), sHe(T) * ys], { color: RED });
      d.line([X(s.lt), 0], [X(s.lt), sHe(T) * ys], { color: MUTED, width: 1, dash: "3 4" });
    },
    formula: function (s) {
      var T = Math.pow(10, s.lt);
      return "T=" + (T < 1 ? F(T, 4) : F(T, 0)) + "\\ \\text{K}\\\\ \\frac S{Nk}=15.17+\\frac32\\ln\\frac T{300\\ \\text{K}}=" + F(sHe(T), 2);
    }
  });

  /* ---------------- 11. 混合熵（§2.6，習題 2.37） ---------------- */
  function sMix(x) { return x <= 0 || x >= 1 ? 0 : -(x * Math.log(x) + (1 - x) * Math.log(1 - x)); }
  A.define("t2-mixing", {
    title: "混合熵 $\\Delta S/Nk$ 對 B 的比例 $x$",
    question: "兩種氣體以什麼比例混合，產生的熵最多？",
    view: [440, 260], origin: [46, 214], scale: 40,
    init: { x: 0.5 },
    steps: [
      { label: "各半", caption: "$x=\\tfrac12$：$\\Delta S=Nk\\ln2$（$N$ 為總數），即課文的 $2Nk\\ln2$（每種 $N$ 個）。一莫耳對一莫耳：$11.5\\ \\text{J/K}$。", dur: 300, hold: 2400 },
      { label: "$x=\\tfrac14$", caption: "$1\\ \\text{mol}$ 氦配 $3\\ \\text{mol}$ 氬（變化題 7）：$\\Delta S/Nk=0.562$，$N=4\\ \\text{mol}$ 時 $18.7\\ \\text{J/K}$。", to: { x: 0.25 }, dur: 2400, hold: 2400 },
      { label: "$x\\to0$", caption: "幾乎全是同一種氣體，混合熵趨近 0；兩種完全相同的氣體 $\\Delta S=0$（沒有混合熵）。", to: { x: 0.02 }, dur: 2400, hold: 3000 }
    ],
    draw: function (d, s) {
      var W = 8, ys = 5;
      d.line([0, 0], [W + 0.3, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 3.9], { color: MUTED, width: 1.3 });
      [0, 0.25, 0.5, 0.75, 1].forEach(function (f) { d.label([f * W, -0.4], F(f, 2), { color: MUTED, size: 11 }); });
      d.label([W / 2 + 0.9, -0.9], "x", { color: MUTED, size: 12 });
      d.line([0, Math.LN2 * ys], [W, Math.LN2 * ys], { color: GRID, width: 1, dash: "4 4" });
      d.label([-0.5, Math.LN2 * ys], "\\ln2", { color: MUTED, size: 11 });
      d.label([0.6, 4.25], "\\Delta S/Nk", { color: MUTED, size: 12, dx: 14 });
      var pts = [];
      for (var j = 0; j <= 200; j++) { var x = j / 200; pts.push([x * W, sMix(x) * ys]); }
      d.path(pts, { color: BLUE, width: 2.4 });
      d.dot([s.x * W, sMix(s.x) * ys], { color: RED });
      // 比例條：A（綠）與 B（紫）
      d.rect(5.2, 4.1, 5.2 + 3 * (1 - s.x), 4.5, { color: GREEN, fill: GREEN, fillOpacity: 0.5, width: 0.6 });
      d.rect(5.2 + 3 * (1 - s.x), 4.1, 8.2, 4.5, { color: PURPLE, fill: PURPLE, fillOpacity: 0.5, width: 0.6 });
      d.label([6.7, 3.75], "A:B=" + F(1 - s.x, 2) + ":" + F(s.x, 2), { color: MUTED, size: 11 });
    },
    formula: function (s) {
      var x = s.x;
      return "x=" + F(x, 2) + "\\\\ \\frac{\\Delta S}{Nk}=-[x\\ln x+(1-x)\\ln(1-x)]\\\\ =" + F(sMix(x), 3);
    }
  });
})();
