/* 近代物理第 2 章（Beiser Particle Properties of Waves）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)";
  var H = 6.626e-34, KB = 1.381e-23, HEV = 4.136e-15, LC = 2.426, ME = 0.511;
  function rad(d) { return d * Math.PI / 180; }
  function fx(x, n) { return x.toFixed(n); }            // 固定位數（不去掉尾端的 0）
  function sci(x, n) {                                   // 科學記號 a\times10^{b}
    var e = Math.floor(Math.log(Math.abs(x)) / Math.LN10), m = x / Math.pow(10, e);
    if (Math.abs(m) >= 9.995) { m /= 10; e += 1; }
    return m.toFixed(n == null ? 2 : n) + "\\times10^{" + e + "}";
  }
  /* 波浪狀的光子：從 a 到 b，最後一小段畫箭頭 */
  function photon(d, a, b, o) {
    o = o || {};
    var dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy);
    if (L < 0.05) return;
    var ux = dx / L, uy = dy / L, nx = -uy, ny = ux, amp = o.amp || 0.12, k = o.k || 2.6, head = Math.min(0.4, L * 0.35);
    var pts = [], m = Math.max(8, Math.round(L * 14));
    for (var i = 0; i <= m; i++) {
      var t = (L - head) * i / m, w = amp * Math.sin(2 * Math.PI * k * t);
      pts.push([a[0] + ux * t + nx * w, a[1] + uy * t + ny * w]);
    }
    d.path(pts, { color: o.color || RED, width: o.width || 2 });
    d.arrow([a[0] + ux * (L - head - 0.02), a[1] + uy * (L - head - 0.02)], b, { color: o.color || RED, width: o.width || 2, head: 9 });
  }

  /* ---------------- 1. 黑體輻射（§2.2，Fig. 2.6、2.8） ---------------- */
  // 橫軸 ν 以 10^14 Hz 為單位；縱軸 u(ν) 以 1800 K 的峰值 = 2.8 格標準化
  function planck(nu, T) { var x = H * nu * 1e14 / (KB * T); return nu * nu * nu / (Math.exp(x) - 1); }
  function rj(nu, T) { return nu * nu * KB * T / (H * 1e14); }
  var XNU = 2.8214;
  function nuPeak(T) { return XNU * KB * T / H / 1e14; }
  var UNORM = 2.8 / planck(nuPeak(1800), 1800);
  A.define("m2-blackbody", {
    title: "黑體光譜 $u(\\nu)$：Planck 與 Rayleigh–Jeans",
    question: "溫度升高，光譜怎麼變？古典公式錯在哪裡？",
    view: [440, 270], origin: [50, 236], scale: 62,
    init: { T: 1200, rj: 0, mark: 0, nuM: 0.5 },
    steps: [
      { label: "$T=1200\\ \\text{K}$", caption: "Planck 公式的光譜：低頻時隨 $\\nu^2$ 上升，高頻被 $e^{-h\\nu/kT}$ 壓到零。峰值在 $0.71\\times10^{14}\\ \\text{Hz}$，是紅外線，所以 $1200\\ \\text{K}$ 的鐵只發出暗紅光。", dur: 300, hold: 2200 },
      { label: "升溫到 $1800\\ \\text{K}$", caption: "溫度升高：曲線下的面積（總輻射）大增，峰值頻率和 $T$ 成正比地右移（Wien 位移定律）。可見光（右邊淺色區）的部分變多，物體由紅變黃、變白。", to: { T: 1800 }, dur: 2600, hold: 1800 },
      { label: "$1500\\ \\text{K}$ 與 Rayleigh–Jeans", caption: "虛線是古典的 Rayleigh–Jeans 公式 $u\\propto kT\\nu^2$（Fig. 2.8）：低頻和 Planck 公式重合，高頻卻一直上升——紫外災變。", set: { rj: 1 }, to: { T: 1500 }, dur: 1800, hold: 2400 },
      { label: "高頻：$h\\nu\\gg kT$", caption: "沿著頻率往右看兩者的比值 $\\dfrac{u_{RJ}}{u_{\\text{Planck}}}=\\dfrac{e^{x}-1}{x}$（$x=h\\nu/kT$）：低頻接近 1，到 $4\\times10^{14}\\ \\text{Hz}$ 已差兩萬八千倍。高頻駐波要一整份 $h\\nu$ 才激發得起來。", set: { mark: 1, nuM: 0.1 }, to: { nuM: 4 }, dur: 3200, hold: 2600 }
    ],
    draw: function (d, s) {
      d.rect(4.3, 0, 6, 3.4, { color: "none", fill: GREEN, fillOpacity: 0.10, width: 0 });
      d.label([5.15, 3.2], "\\text{可見光}", { color: GREEN, size: 11 });
      d.line([0, 0], [6.1, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 3.45], { color: MUTED, width: 1.3 });
      for (var k = 1; k <= 6; k++) { d.line([k, 0], [k, -0.07], { color: MUTED, width: 1 }); d.label([k, -0.25], String(k), { color: MUTED, size: 10 }); }
      d.label([0, -0.25], "0", { color: MUTED, size: 10 });
      d.label([5.25, 0.32], "\\nu\\ (10^{14}\\ \\text{Hz})", { color: MUTED, size: 11 });
      d.label([0.55, 3.55], "u(\\nu)", { color: MUTED, size: 12 });
      var pts = [], rjp = [];
      for (var i = 1; i <= 240; i++) { var nu = i * 0.025; pts.push([nu, UNORM * planck(nu, s.T)]); var r = UNORM * rj(nu, s.T); if (r < 3.4) rjp.push([nu, r]); }
      d.path(pts, { color: RED, width: 2.4 });
      if (s.rj) d.path(rjp, { color: BLUE, width: 2, dash: "6 4" });
      if (s.rj && s.T < 1600) d.label([1.45, 3.2], "\\text{Rayleigh–Jeans}", { color: BLUE, size: 11 });
      var np = nuPeak(s.T), up = UNORM * planck(np, s.T);
      d.line([np, 0], [np, up], { color: MUTED, width: 1, dash: "3 4" });
      d.dot([np, up], { color: RED });
      d.label([np + 0.55, up + 0.22], "T=" + Math.round(s.T) + "\\ \\text{K}", { color: RED, size: 12 });
      if (s.mark) {
        var x = s.nuM, y = UNORM * planck(x, s.T);
        d.line([x, 0], [x, 3.3], { color: PURPLE, width: 1.2, dash: "2 3" });
        d.dot([x, y], { color: PURPLE, r: 4 });
      }
    },
    formula: function (s) {
      var np = nuPeak(s.T);
      if (s.mark) {
        var x = H * s.nuM * 1e14 / (KB * s.T), ratio = (Math.exp(x) - 1) / x;
        return "\\nu=" + fx(s.nuM, 2) + "\\times10^{14}\\ \\text{Hz}:\\ x=\\frac{h\\nu}{kT}=" + fx(x, 2) + "\\\\ \\frac{u_{RJ}}{u_{\\text{Planck}}}=\\frac{e^{x}-1}{x}=" + (ratio < 100 ? fx(ratio, 2) : sci(ratio, 1));
      }
      return "T=" + Math.round(s.T) + "\\ \\text{K}:\\ \\nu_{\\max}=2.821\\,\\frac{kT}{h}=" + fx(np, 2) + "\\times10^{14}\\ \\text{Hz}";
    }
  });

  /* ---------------- 2. 光電效應 KE_max–ν（§2.3，Fig. 2.12；考古 107-6） ---------------- */
  var HU = 0.4136, KY = 2;    // 橫軸 1 格 = 10^14 Hz，hν = 0.4136 eV/格；縱軸 1 eV = 2 格
  var METALS = [{ n: "Cs", phi: 1.9, c: BLUE }, { n: "Na", phi: 2.28, c: RED }, { n: "Ca", phi: 3.2, c: GREEN }];
  A.define("m2-photoelectric", {
    title: "$KE_{\\max}$ 與頻率：三條平行線，斜率都是 $h$",
    question: "鈉被 $560\\ \\text{nm}$ 和 $410\\ \\text{nm}$ 的光照射，會怎樣？",
    view: [440, 270], origin: [44, 228], scale: 30,
    init: { nu: 3, on: 0, tri: 0 },
    steps: [
      { label: "三種金屬", caption: "$KE_{\\max}=h\\nu-\\phi$：每種金屬一條直線，和橫軸交在截止頻率 $\\nu_0=\\phi/h$。功函數不同只是平移，斜率都相同。", dur: 300, hold: 2600 },
      { label: "鈉，$560\\ \\text{nm}$", caption: "考古 107-6 (b)：$560\\ \\text{nm}$ 的光子只有 $2.21\\ \\text{eV}$，頻率在鈉的 $\\nu_0$ 左邊，不論光多強都沒有光電子。", set: { on: 1 }, to: { nu: 2998 / 560 }, dur: 2200, hold: 2200 },
      { label: "鈉，$410\\ \\text{nm}$", caption: "考古 107-6 (a)：$410\\ \\text{nm}$ 的光子 $3.02\\ \\text{eV}$，超過功函數 $2.28\\ \\text{eV}$，最大動能 $0.74\\ \\text{eV}$（截止電壓 $0.74\\ \\text{V}$）。強度加倍只會讓電子數加倍，點的高度不變。", to: { nu: 2998 / 410 }, dur: 2200, hold: 2400 },
      { label: "斜率 $=h$", caption: "頻率增加 $3\\times10^{14}\\ \\text{Hz}$，$KE_{\\max}$ 增加 $1.24\\ \\text{eV}$：斜率 $4.14\\times10^{-15}\\ \\text{eV·s}$，正是 Planck 常數（Millikan 1916）。", set: { tri: 1 }, dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      d.line([0, 0], [12.4, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 6.7], { color: MUTED, width: 1.3 });
      for (var k = 2; k <= 12; k += 2) { d.line([k, 0], [k, -0.15], { color: MUTED, width: 1 }); d.label([k, -0.55], String(k), { color: MUTED, size: 10 }); }
      for (var e = 1; e <= 3; e++) { d.line([0, e * KY], [12, e * KY], { color: "var(--grid)", width: 1 }); d.label([-0.55, e * KY], String(e), { color: MUTED, size: 10 }); }
      d.label([10.4, -1.05], "\\nu\\ (10^{14}\\ \\text{Hz})", { color: MUTED, size: 11 });
      d.label([1.6, 7.05], "KE_{\\max}\\ (\\text{eV})", { color: MUTED, size: 11 });
      METALS.forEach(function (m, i) {
        var n0 = m.phi / HU, n1 = Math.min(12, (3.25 + m.phi) / HU);
        var fade = s.on && !s.tri && m.n !== "Na";
        d.line([n0, 0], [n1, (HU * n1 - m.phi) * KY], { color: m.c, width: fade ? 1.4 : 2.3, opacity: fade ? 0.45 : 1 });
        d.label([n1 + 0.5, (HU * n1 - m.phi) * KY], "\\text{" + m.n + "}", { color: m.c, size: 11 });
        d.dot([n0, 0], { color: m.c, r: 3.5 });
      });
      d.line([2.28 / HU, 0], [2.28 / HU, -0.75], { color: RED, width: 1, dash: "2 3" });
      d.label([2.28 / HU, -1.05], "\\nu_0", { color: RED, size: 11 });
      if (s.on) {
        var KE = HU * s.nu - 2.28;
        d.line([s.nu, 0], [s.nu, 6.6], { color: PURPLE, width: 1.2, dash: "3 4" });
        if (KE > 0) { d.dot([s.nu, KE * KY], { color: PURPLE, r: 5 }); if (!s.tri) d.label([s.nu + 0.95, KE * KY - 0.15], fx(KE, 2) + "\\ \\text{eV}", { color: PURPLE, size: 12 }); }
        else { d.circle([s.nu, 0], 6, { color: PURPLE, width: 2 }); d.label([s.nu - 0.6, 1.6], "\\text{無光電子}", { color: PURPLE, size: 12 }); }
      }
      if (s.tri) {
        var a = 8, b = 11, ya = (HU * a - 1.9) * KY, yb = (HU * b - 1.9) * KY;   // 畫在 Cs 線上（三條線斜率相同）
        d.line([a, ya], [b, ya], { color: INK, width: 1.4 }); d.line([b, ya], [b, yb], { color: INK, width: 1.4 });
        d.label([9.5, ya - 0.37], "\\Delta\\nu", { color: INK, size: 12 });
        d.label([11.65, (ya + yb) / 2], "\\Delta KE", { color: INK, size: 12 });
      }
    },
    formula: function (s) {
      if (!s.on) return "KE_{\\max}=h\\nu-\\phi,\\quad \\nu_0=\\frac{\\phi}{h}:\\ \\text{Cs } 4.6,\\ \\text{Na } 5.5,\\ \\text{Ca } 7.7\\ (10^{14}\\ \\text{Hz})";
      if (s.tri) return "h=\\frac{\\Delta KE_{\\max}}{\\Delta\\nu}=\\frac{1.24\\ \\text{eV}}{3\\times10^{14}\\ \\text{Hz}}=4.14\\times10^{-15}\\ \\text{eV·s}";
      var E = HU * s.nu, lam = 2998 / s.nu, KE = E - 2.28;
      return "\\lambda=" + Math.round(lam) + "\\ \\text{nm}:\\ h\\nu=\\frac{1240}{\\lambda}=" + fx(E, 2) + "\\ \\text{eV}\\\\ " +
        (KE > 0 ? "KE_{\\max}=" + fx(E, 2) + "-2.28=" + fx(KE, 2) + "\\ \\text{eV}" : "h\\nu<\\phi=2.28\\ \\text{eV}\\ \\Rightarrow\\ \\text{沒有光電子}");
    }
  });

  /* ---------------- 3. X 光連續譜與截止波長（§2.5，Fig. 2.16；例題 2.3） ---------------- */
  // 橫軸 1 格 = 0.01 nm；曲線形狀用 Kramers 近似 I_λ ∝ (λ − λmin)/λ³（示意，峰值在 1.5λmin），50 kV 峰值 = 5 格
  function kram(l, lm) { return l <= lm ? 0 : (l - lm) / (l * l * l); }
  var KNORM = 5 / kram(1.5 * 1.24 / 50 * 100, 1.24 / 50 * 100);
  A.define("m2-xray", {
    title: "X 光連續譜：電壓越高，$\\lambda_{\\min}$ 越短",
    question: "為什麼每條曲線都有一個鋒利的最短波長？",
    view: [440, 270], origin: [50, 232], scale: 36,
    init: { V: 20 },
    steps: [
      { label: "$20\\ \\text{kV}$", caption: "電子經 $V$ 加速、打上靶，產生連續的制動輻射（曲線形狀是示意）。最短波長是一個電子把全部動能 $eV$ 給一個光子：$\\lambda_{\\min}=hc/eV=0.062\\ \\text{nm}$。", dur: 300, hold: 2200 },
      { label: "$30\\ \\text{kV}$", caption: "電壓提高，截止波長變短（$\\lambda_{\\min}\\propto1/V$），強度也增加。", to: { V: 30 } },
      { label: "$40\\ \\text{kV}$", caption: "截止波長只看 $V$，和靶是鎢還是鉬無關（Duane–Hunt）。", to: { V: 40 } },
      { label: "$50\\ \\text{kV}$（例題 2.3）", caption: "$\\lambda_{\\min}=1.24\\times10^{-6}/5.00\\times10^{4}=0.0248\\ \\text{nm}$，對應 $\\nu_{\\max}=1.21\\times10^{19}\\ \\text{Hz}$。古典理論沒有理由出現這個鋒利的截止，量子理論一行就推出來：逆光電效應。", to: { V: 50 }, hold: 2600 }
    ],
    draw: function (d, s) {
      d.line([0, 0], [10.3, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 5.6], { color: MUTED, width: 1.3 });
      [2, 4, 6, 8, 10].forEach(function (k) { d.line([k, 0], [k, -0.12], { color: MUTED, width: 1 }); d.label([k, -0.45], fx(k / 100, 2), { color: MUTED, size: 10 }); });
      d.label([9.3, 0.4], "\\lambda\\ (\\text{nm})", { color: MUTED, size: 11 });
      d.label([1.2, 5.9], "\\text{相對強度}", { color: MUTED, size: 11 });
      [20, 30, 40, 50].forEach(function (V) {
        if (V > s.V + 0.5) return;
        var lm = 1.24 / V * 100, pts = [];
        for (var l = lm; l <= 10; l += 0.05) pts.push([l, KNORM * kram(l, lm)]);
        d.path(pts, { color: MUTED, width: 1.2, opacity: 0.6 });
      });
      var lm = 1.24 / s.V * 100, cur = [];
      for (var l = lm; l <= 10; l += 0.04) cur.push([l, KNORM * kram(l, lm)]);
      d.path(cur, { color: RED, width: 2.4 });
      d.line([lm, 0], [lm, 5.3], { color: BLUE, width: 1.3, dash: "4 4" });
      d.label([lm + 1.45, 5.45], "\\lambda_{\\min},\\ " + Math.round(s.V) + "\\ \\text{kV}", { color: BLUE, size: 12 });
    },
    formula: function (s) {
      return "V=" + fx(s.V, 1) + "\\ \\text{kV}:\\ \\lambda_{\\min}=\\frac{1.24\\times10^{-6}\\ \\text{V·m}}{V}=" + fx(1.24 / s.V, 4) + "\\ \\text{nm}\\\\ h\\nu_{\\max}=eV=" + fx(s.V, 1) + "\\ \\text{keV}";
    }
  });

  /* ---------------- 4. Bragg 繞射（§2.6，Fig. 2.20；習題 2-22 的 KCl） ---------------- */
  var DB = 1.2, DNM = 0.315, LAMB = 0.30;
  A.define("m2-bragg", {
    title: "Bragg 條件：路程差 $2d\\sin\\theta$ 是 $\\lambda$ 的整數倍才加強",
    question: "$0.30\\ \\text{nm}$ 的 X 光射向 $d=0.315\\ \\text{nm}$ 的 KCl，哪些角度會亮？",
    view: [440, 300], origin: [220, 196], scale: 40,
    init: { th: 15 },
    steps: [
      { label: "$\\theta=15^\\circ$", caption: "光線 I 在第一層的原子 A 散射，光線 II 在下一層的 B 散射，散射角等於入射角 $\\theta$。光線 II 多走綠色的兩段，各 $d\\sin\\theta$。這裡路程差只有 $0.54\\lambda$，相鄰兩層幾乎反相，互相抵消。", dur: 300, hold: 2600 },
      { label: "$\\theta=28.4^\\circ$", caption: "路程差 $2d\\sin\\theta=0.300\\ \\text{nm}=\\lambda$：所有層的散射波同相，一階亮紋（$n=1$）。這就是習題 2-22 量到的最小 Bragg 角。", to: { th: 28.4 }, dur: 2400, hold: 2400 },
      { label: "$\\theta=50^\\circ$", caption: "路程差 $1.61\\lambda$，不是整數倍，暗。晶體有成千上萬層，只要稍微偏離整數倍就會抵消，所以亮紋非常尖銳。", to: { th: 50 }, dur: 2400 },
      { label: "$\\theta=72.2^\\circ$", caption: "路程差 $2\\lambda$：二階亮紋（$n=2$）。$n=3$ 需要 $\\sin\\theta=1.43>1$，不存在。", to: { th: 72.2 }, dur: 2400, hold: 2600 }
    ],
    draw: function (d, s) {
      var t = rad(s.th), ui = [Math.cos(t), -Math.sin(t)], uo = [Math.cos(t), Math.sin(t)], L = 4.2;
      for (var r = 0; r < 3; r++) for (var c = -4; c <= 4; c++) d.circle([c * DB, -r * DB], 4, { color: MUTED, width: 1.3 });
      var Aa = [0, 0], B = [0, -DB], ds = DB * Math.sin(t);
      // 光線 I
      d.line([Aa[0] - L * ui[0], Aa[1] - L * ui[1]], Aa, { color: RED, width: 3 });
      d.arrow(Aa, [Aa[0] + L * uo[0], Aa[1] + L * uo[1]], { color: RED, width: 3, head: 10 });
      // 光線 II
      var t2 = L + ds;
      d.line([B[0] - t2 * ui[0], B[1] - t2 * ui[1]], B, { color: BLUE, width: 3 });
      d.arrow(B, [B[0] + t2 * uo[0], B[1] + t2 * uo[1]], { color: BLUE, width: 3, head: 10 });
      // 多走的兩段與波前
      var P = [B[0] - ds * ui[0], B[1] - ds * ui[1]], Q = [B[0] + ds * uo[0], B[1] + ds * uo[1]];
      d.line(P, B, { color: GREEN, width: 5 }); d.line(B, Q, { color: GREEN, width: 5 });
      d.line(Aa, P, { color: MUTED, width: 1.2, dash: "3 3" }); d.line(Aa, Q, { color: MUTED, width: 1.2, dash: "3 3" });
      d.dot(Aa, { color: INK, r: 4 }); d.dot(B, { color: INK, r: 4 });
      var nn = [Math.sin(t), Math.cos(t)];   // 垂直於入射光、朝右上
      d.label([0.3, 0.35], "A", { color: INK, size: 12 });
      d.label([-0.35, -DB - 0.32], "B", { color: INK, size: 12 });
      d.label([Aa[0] - L * ui[0] + 0.45 * nn[0], Aa[1] - L * ui[1] + 0.45 * nn[1]], "\\text{I}", { color: RED, size: 12 });
      d.label([B[0] - t2 * ui[0] - 0.45 * nn[0], B[1] - t2 * ui[1] - 0.45 * nn[1]], "\\text{II}", { color: BLUE, size: 12 });
      d.arc(Aa, 1.8, 180 - s.th, 180, { color: INK, width: 1.3 });
      var tl = rad(180 - s.th / 2); d.label([2.35 * Math.cos(tl), 2.35 * Math.sin(tl)], "\\theta", { color: INK, size: 12 });
      d.label([0.85, -1.72], "d\\sin\\theta", { color: GREEN, size: 11 });
      d.line([-3.0, -DB], [-3.0, -2 * DB], { color: MUTED, width: 1.2 }); d.label([-3.3, -1.5 * DB], "d", { color: MUTED, size: 12 });
      var ratio = 2 * DNM * Math.sin(t) / LAMB, near = Math.abs(ratio - Math.round(ratio)) < 0.03 && Math.round(ratio) >= 1;
      d.label([-3.8, 4.4], near ? "\\text{建設性：}n=" + Math.round(ratio) : "\\text{不加強}", { color: near ? GREEN : MUTED, size: 13 });
    },
    formula: function (s) {
      var t = rad(s.th), pd = 2 * DNM * Math.sin(t), ratio = pd / LAMB, n = Math.round(ratio), near = Math.abs(ratio - n) < 0.03 && n >= 1;
      return "2d\\sin\\theta=2(0.315)\\sin" + fx(s.th, 1) + "^\\circ=" + fx(pd, 3) + "\\ \\text{nm}=" + fx(ratio, 2) + "\\lambda" + (near ? "\\ \\Rightarrow\\ n=" + n : "");
    }
  });

  /* ---------------- 5. 康普頓散射（§2.7，Fig. 2.22、2.24；例題 2.4） ---------------- */
  var LAM0 = 10.0, SP = 26;    // 入射 10.0 pm；動量 1/λ (pm⁻¹) × 26 = 箭頭長度
  A.define("m2-compton", {
    title: "康普頓散射：$\\Delta\\lambda=\\lambda_C(1-\\cos\\phi)$",
    question: "$10.0\\ \\text{pm}$ 的 X 光散射角越大，波長變多少、電子拿到多少能量？",
    view: [440, 340], origin: [24, 318], scale: 34,
    init: { phi: 45 },
    steps: [
      { label: "$\\phi=45^\\circ$", caption: "上：動量向量圖（長度 $\\propto h/\\lambda$）。紅色入射光子、藍色散射光子、綠色反衝電子，三者的動量守恆。例題 2.4 (a)：$\\lambda'=10.7\\ \\text{pm}$。", dur: 300, hold: 2600 },
      { label: "$\\phi=90^\\circ$", caption: "$\\Delta\\lambda=\\lambda_C=2.43\\ \\text{pm}$。散射角越大，光子損失越多，電子越往正前方（$\\theta$ 變小）。", to: { phi: 90 } },
      { label: "$\\phi=135^\\circ$", caption: "下圖的 $\\Delta\\lambda$ 只由角度決定，和入射波長無關——Fig. 2.24 的峰隨角度右移。", to: { phi: 135 } },
      { label: "$\\phi=180^\\circ$", caption: "光子被反彈：$\\Delta\\lambda=2\\lambda_C=4.85\\ \\text{pm}$，$\\lambda'=14.85\\ \\text{pm}$，電子正前方、動能最大 $40.5\\ \\text{keV}$（課本把 $\\lambda'$ 寫成 $14.9$，得 $40.8\\ \\text{keV}$）。", to: { phi: 180 }, hold: 2800 }
    ],
    draw: function (d, s) {
      var p = rad(s.phi), lp = LAM0 + LC * (1 - Math.cos(p)), E0 = [5.6, 7.0];
      var pin = SP / LAM0, pout = SP / lp;
      var ex = pin - pout * Math.cos(p), ey = -pout * Math.sin(p);
      photon(d, [E0[0] - pin, E0[1]], E0, { color: RED });
      var off = 0.32 * Math.max(0, (s.phi - 150) / 30);   // 接近 180° 時散射光子和入射光子重疊，稍微往上錯開
      photon(d, [E0[0], E0[1] + off], [E0[0] + pout * Math.cos(p), E0[1] + pout * Math.sin(p) + off], { color: BLUE });
      d.arrow(E0, [E0[0] + ex, E0[1] + ey], { color: GREEN, width: 2.6, head: 10 });
      d.line(E0, [E0[0] + 3.6, E0[1]], { color: MUTED, width: 1, dash: "3 4" });
      d.dot(E0, { color: INK, r: 5 });
      if (s.phi < 179) {
        d.arc(E0, 0.75, 0, s.phi, { color: BLUE, width: 1.3 });
        var ph = rad(s.phi / 2); d.label([E0[0] + 1.1 * Math.cos(ph), E0[1] + 1.1 * Math.sin(ph)], "\\phi", { color: BLUE, size: 12 });
      } else d.label([E0[0], E0[1] + 1.0], "\\phi=180^\\circ", { color: BLUE, size: 12 });
      d.label([E0[0] - pin + 0.4, E0[1] + 0.45], "h/\\lambda", { color: RED, size: 12 });
      d.label([E0[0] + ex + 0.45, E0[1] + ey - 0.1], "p_e", { color: GREEN, size: 12 });
      // 下：Δλ–φ 曲線
      var X0 = 1.2, Y0 = 0.8, sx = 10 / 180, sy = 0.6;
      d.line([X0, Y0], [X0 + 10.3, Y0], { color: MUTED, width: 1.3 }); d.line([X0, Y0], [X0, Y0 + 3.2], { color: MUTED, width: 1.3 });
      [0, 45, 90, 135, 180].forEach(function (a) { d.line([X0 + a * sx, Y0], [X0 + a * sx, Y0 - 0.12], { color: MUTED, width: 1 }); d.label([X0 + a * sx, Y0 - 0.42], a + "^\\circ", { color: MUTED, size: 10 }); });
      [[LC, "\\lambda_C"], [2 * LC, "2\\lambda_C"]].forEach(function (q) { d.line([X0, Y0 + q[0] * sy], [X0 + 10, Y0 + q[0] * sy], { color: "var(--grid)", width: 1 }); d.label([X0 - 0.55, Y0 + q[0] * sy], q[1], { color: MUTED, size: 10 }); });
      d.label([X0 + 1.3, Y0 + 3.45], "\\Delta\\lambda\\ (\\text{pm})", { color: MUTED, size: 11 });
      var cv = [];
      for (var a = 0; a <= 180; a += 3) cv.push([X0 + a * sx, Y0 + LC * (1 - Math.cos(rad(a))) * sy]);
      d.path(cv, { color: PURPLE, width: 2.2 });
      d.dot([X0 + s.phi * sx, Y0 + (lp - LAM0) * sy], { color: PURPLE, r: 5 });
    },
    formula: function (s) {
      var p = rad(s.phi), dl = LC * (1 - Math.cos(p)), lp = LAM0 + dl, KE = 1239.8 * (1 / LAM0 - 1 / lp);
      var th = Math.atan2(Math.sin(p) / lp, 1 / LAM0 - Math.cos(p) / lp) * 180 / Math.PI;
      return "\\phi=" + Math.round(s.phi) + "^\\circ:\\ \\Delta\\lambda=" + fx(dl, 2) + "\\ \\text{pm},\\ \\lambda'=" + fx(lp, 2) + "\\ \\text{pm}\\\\ KE=hc\\Big(\\frac1\\lambda-\\frac1{\\lambda'}\\Big)=" + fx(KE, 1) + "\\ \\text{keV},\\ \\theta=" + fx(th, 1) + "^\\circ";
    }
  });

  /* ---------------- 6. 正子撞靜止電子的湮滅（§2.8；考古 107-8） ---------------- */
  A.define("m2-annihilation", {
    title: "湮滅：一前一後兩個光子的能量",
    question: "正子越快，兩個光子的能量差多少？",
    view: [440, 230], origin: [20, 214], scale: 40,
    init: { K: 0 },
    steps: [
      { label: "正子幾乎靜止", caption: "總動量為零：兩個光子反向、各 $0.511\\ \\text{MeV}$。（箭頭長度 $\\propto$ 能量或 $pc$，1 格 $=1\\ \\text{MeV}$。）", dur: 300, hold: 2400 },
      { label: "$KE=1.0\\ \\text{MeV}$", caption: "正子帶來動量 $pc$。光子共線時，動量守恆給 $E_1-E_2=pc$，能量守恆給 $E_1+E_2=KE+2mc^2$：往前的光子變大、往後的變小。", to: { K: 1.0 } },
      { label: "$KE=2.0\\ \\text{MeV}$（107-8）", caption: "考古 107-8：$E_1=2.74\\ \\text{MeV}$（往前）、$E_2=0.28\\ \\text{MeV}$（往後）。", to: { K: 2.0 }, hold: 2400 },
      { label: "$KE=3.0\\ \\text{MeV}$", caption: "變化題 5：$3.75$ 和 $0.27\\ \\text{MeV}$。正子越快，往後的光子越接近一個極限（$KE\\to\\infty$ 時 $E_2\\to\\tfrac12mc^2=0.256\\ \\text{MeV}$）。", to: { K: 3.0 }, hold: 2600 }
    ],
    draw: function (d, s) {
      var Et = s.K + 2 * ME, pc = Math.sqrt(s.K * s.K + 2 * s.K * ME), E1 = (Et + pc) / 2, E2 = (Et - pc) / 2;
      d.label([1.1, 4.5], "\\text{碰撞前}", { color: MUTED, size: 12 });
      d.label([1.1, 2.4], "\\text{湮滅後}", { color: MUTED, size: 12 });
      var ye = 3.6, xp = 1.6, xe = 6.0;
      d.dot([xp, ye], { color: RED, r: 6 }); d.label([xp, ye + 0.45], "e^+", { color: RED, size: 12 });
      if (pc > 0.05) { d.arrow([xp + 0.2, ye], [xp + 0.2 + pc, ye], { color: RED, width: 2.4, head: 10 }); d.label([xp + 0.2 + pc / 2, ye - 0.42], "pc=" + fx(pc, 2), { color: RED, size: 11 }); }
      d.dot([xe, ye], { color: BLUE, r: 6 }); d.label([xe + 0.1, ye + 0.45], "e^-\\ (\\text{靜止})", { color: BLUE, size: 12 });
      var yg = 1.2, xc = 5.6;
      d.dot([xc, yg], { color: MUTED, r: 3 });
      photon(d, [xc, yg], [xc + E1, yg], { color: PURPLE });
      photon(d, [xc, yg], [xc - E2, yg], { color: GREEN });
      d.label([xc + E1 / 2 + 0.2, yg + 0.55], "E_1=" + fx(E1, 3), { color: PURPLE, size: 12 });
      d.label([xc - E2 - 1.1, yg + 0.55], "E_2=" + fx(E2, 3), { color: GREEN, size: 12 });
      d.line([xc - 4.6, 0.2], [xc + 4.6, 0.2], { color: "var(--grid)", width: 1 });
      for (var k = -4; k <= 4; k++) d.line([xc + k, 0.2], [xc + k, 0.32], { color: MUTED, width: 1 });
    },
    formula: function (s) {
      var Et = s.K + 2 * ME, pc = Math.sqrt(s.K * s.K + 2 * s.K * ME);
      return "E_{\\text{tot}}=KE+2mc^2=" + fx(Et, 3) + ",\\ pc=" + fx(pc, 3) + "\\ (\\text{MeV})\\\\ E_{1,2}=\\tfrac12(E_{\\text{tot}}\\pm pc)=" + fx((Et + pc) / 2, 3) + ",\\ " + fx((Et - pc) / 2, 3) + "\\ \\text{MeV}";
    }
  });

  /* ---------------- 7. 衰減曲線（§2.8，Eq. 2.25；考古 107-9） ---------------- */
  var MU = 78;   // 1 MeV γ 射線在鉛中，m⁻¹
  A.define("m2-attenuation", {
    title: "$I=I_0e^{-\\mu x}$：每多一個半值厚度，強度再減半",
    question: "$1\\ \\text{MeV}$ $\\gamma$ 射線（鉛 $\\mu=78\\ \\text{m}^{-1}$）要多厚的鉛才擋掉一半、十分之九？",
    view: [440, 260], origin: [50, 222], scale: 34,
    init: { xm: 0 },
    steps: [
      { label: "入射", caption: "$x=0$：$I=I_0$。橫軸是鉛的厚度（mm），縱軸是相對強度 $I/I_0$。", dur: 300, hold: 1800 },
      { label: "半值厚度", caption: "考古 107-9：$x_{1/2}=0.693/\\mu=8.9\\ \\text{mm}$，強度剩一半。", to: { xm: Math.LN2 / MU * 1000 }, hold: 2000 },
      { label: "兩個半值厚度", caption: "再 $8.9\\ \\text{mm}$ 又減一半：剩 $\\tfrac14$。指數衰減是「乘上同一個比例」，不是減掉同一個量。", to: { xm: 2 * Math.LN2 / MU * 1000 } },
      { label: "三個半值厚度", caption: "$26.7\\ \\text{mm}$ 剩 $\\tfrac18$（變化題 7）。", to: { xm: 3 * Math.LN2 / MU * 1000 } },
      { label: "剩十分之一", caption: "$x_{1/10}=2.30/\\mu=29.5\\ \\text{mm}$，約 3.3 個半值厚度（習題 2-43）。強度永遠不會剛好變成零。", to: { xm: Math.LN10 / MU * 1000 }, hold: 2600 }
    ],
    draw: function (d, s) {
      var SX = 0.25, SY = 5;   // 1 mm = 0.25 格；I/I0 = 1 → 5 格
      d.line([0, 0], [10.6, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 5.4], { color: MUTED, width: 1.3 });
      [0, 10, 20, 30, 40].forEach(function (m) { d.line([m * SX, 0], [m * SX, -0.12], { color: MUTED, width: 1 }); d.label([m * SX, -0.45], String(m), { color: MUTED, size: 10 }); });
      [[1, "1"], [0.5, "\\tfrac12"], [0.25, "\\tfrac14"], [0.125, "\\tfrac18"]].forEach(function (q) {
        d.line([0, q[0] * SY], [10.3, q[0] * SY], { color: "var(--grid)", width: 1 }); d.label([-0.5, q[0] * SY], q[1], { color: MUTED, size: 10 });
      });
      d.label([9.6, 0.95], "x\\ (\\text{mm})", { color: MUTED, size: 11 });
      d.label([1.0, 5.65], "I/I_0", { color: MUTED, size: 12 });
      var pts = [];
      for (var m = 0; m <= 41; m += 0.5) pts.push([m * SX, SY * Math.exp(-MU * m / 1000)]);
      d.path(pts, { color: RED, width: 2.4 });
      var I = Math.exp(-MU * s.xm / 1000), X = s.xm * SX, Y = SY * I;
      d.rect(0, 0, X, 5.2, { color: "none", fill: MUTED, fillOpacity: 0.12, width: 0 });
      d.line([X, 0], [X, Y], { color: BLUE, width: 1.3, dash: "3 4" }); d.line([0, Y], [X, Y], { color: BLUE, width: 1.3, dash: "3 4" });
      d.dot([X, Y], { color: BLUE, r: 5 });
      if (s.xm > 1) d.label([X / 2, 4.65], "\\text{鉛}", { color: MUTED, size: 11 });
    },
    formula: function (s) {
      var I = Math.exp(-MU * s.xm / 1000);
      return "x=" + fx(s.xm, 1) + "\\ \\text{mm}:\\ \\frac{I}{I_0}=e^{-\\mu x}=e^{-(78)(" + fx(s.xm / 1000, 4) + ")}=" + fx(I, 3);
    }
  });
})();
