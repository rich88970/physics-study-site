/* 力學 Lecture 2（Thornton & Marion 第 2 章）的連續圖解。每張圖的數值、說明與公式來自同一個狀態 s。 */
(function () {
  "use strict";
  var A = window.Anim, F = A.fmt;
  var RED = "var(--a)", BLUE = "var(--b)", GREEN = "var(--c)", PURPLE = "var(--d)", MUTED = "var(--muted)", INK = "var(--ink)", GRID = "var(--grid)";
  var G = 9.8;
  function rad(d) { return d * Math.PI / 180; }
  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }

  /* ---------------- 1. 伽利略的斜面（講義 p.7） ---------------- */
  A.define("c2-galileo", {
    title: "伽利略的斜面：球總是爬回原來的高度",
    question: "對面的斜面越來越平，球要滾多遠？",
    view: [440, 165], origin: [118, 122], scale: 26,
    init: { phi: 45, p: 0 },
    steps: [
      { label: "對面 $45^\\circ$", caption: "球從左邊高度 $h$ 由靜止滾下。沒有摩擦時，它在右邊的斜面爬回<strong>同一個高度</strong> $h$ 才停下、折返。", set: { phi: 45, p: 0 }, to: { p: 1 }, dur: 2600, hold: 1200 },
      { label: "對面 $25^\\circ$", caption: "右邊比較平：仍然爬到高度 $h$，只是要走更遠，水平距離 $L=h/\\tan\\phi$。", set: { phi: 25, p: 0 }, to: { p: 1 }, dur: 2800, hold: 1200 },
      { label: "對面 $15^\\circ$", caption: "再平一點，水平距離變成 $7.46$（$h=2$）。高度不變，距離越來越長。", set: { phi: 15, p: 0 }, to: { p: 1 }, dur: 3000, hold: 1200 },
      { label: "對面水平", caption: "右邊完全水平：球永遠到不了高度 $h$，也就沒有理由停下——<strong>不受力的物體保持等速直線運動</strong>。這就是慣性。", set: { phi: 0, p: 0 }, to: { p: 1 }, dur: 3000, hold: 2400 }
    ],
    draw: function (d, s) {
      var h = 2, xl = -h, XMAX = 11.6;  // 左邊 45° 斜面，從 (-2, 2) 到原點
      d.line([-4.2, 0], [12.4, 0], { color: GRID, width: 1 });
      d.line([xl, h], [0, 0], { color: INK, width: 2.5 });
      d.line([-4.2, h], [12.2, h], { color: MUTED, width: 1, dash: "4 5" });
      d.label([-3.4, h + 0.45], "h", { color: MUTED, size: 13 });
      var phi = s.phi, L = phi > 0.5 ? h / Math.tan(rad(phi)) : 99;
      var xr = Math.min(L, XMAX);
      d.line([0, 0], [xr, phi > 0.5 ? xr * Math.tan(rad(phi)) : 0], { color: INK, width: 2.5 });
      // 球的位置：前 40% 下坡、其餘上坡（只示意位置，不是等時）
      var ball;
      if (s.p < 0.4) { var u = s.p / 0.4; ball = [xl * (1 - u), h * (1 - u)]; }
      else { var w = (s.p - 0.4) / 0.6; var xx = xr * w; ball = [xx, phi > 0.5 ? xx * Math.tan(rad(phi)) : 0]; }
      d.dot([ball[0], ball[1] + 0.25], { color: RED, r: 6 });
      if (phi > 0.5) {
        d.arc([0, 0], 1.2, 0, phi, { color: MUTED, width: 1.2 });
        d.label([1.75, 0.17], "\\phi", { color: MUTED, size: 12 });
        d.line([0, -0.45], [L, -0.45], { color: BLUE, width: 1.3 });
        d.line([L, -0.25], [L, -0.65], { color: BLUE, width: 1.3 }); d.line([0, -0.25], [0, -0.65], { color: BLUE, width: 1.3 });
        d.label([L / 2, -0.95], "L=" + F(L, 2), { color: BLUE, size: 12 });
      } else {
        d.arrow([8.6, 0.9], [10.8, 0.9], { color: BLUE, width: 1.6, head: 9 });
        d.label([9.7, 1.4], "\\text{一直滾}", { color: BLUE, size: 12 });
      }
    },
    formula: function (s) {
      return s.phi > 0.5 ? "\\phi=" + F(s.phi, 0) + "^\\circ:\\ L=\\frac{h}{\\tan\\phi}=" + F(2 / Math.tan(rad(s.phi)), 2) + "\\ (h=2)" : "\\phi=0:\\ L=\\frac{h}{\\tan\\phi}\\to\\infty";
    }
  });

  /* ---------------- 2. 加速列車上的球（講義 p.16） ---------------- */
  A.define("c2-train", {
    title: "加速的列車上，光滑地板上的球往後跑",
    question: "地面看和車上看，球的運動有什麼不同？",
    view: [440, 190], origin: [120, 110], scale: 26,
    init: { t: 0, frame: 0 },
    steps: [
      { label: "地面（慣性系）", caption: "列車以 $a=1\\ \\text{m/s}^2$ 向右加速。地板光滑，沒有水平力作用在球上：從地面看，球留在原地（藍點），是列車從它下面溜走。", set: { frame: 0, t: 0 }, to: { t: 2.5 }, dur: 3200, hold: 1400 },
      { label: "車上（非慣性系）", caption: "同一件事從車上看：車廂不動，球以 $1\\ \\text{m/s}^2$ <strong>往後</strong>加速，卻找不到施力者。牛頓定律在這個座標系不成立。", set: { frame: 1, t: 0 }, to: { t: 2.5 }, dur: 3200, hold: 1400 },
      { label: "差一項 $-\\vec a$", caption: "兩個座標系的加速度差 $\\ddot{\\vec r}\\,'=\\ddot{\\vec r}-\\vec a$。只有座標系本身不加速（$\\vec a=0$）時，兩者量到的加速度才相同。", dur: 300, hold: 3000 }
    ],
    draw: function (d, s) {
      var a = 1, t = s.t, xt = s.frame === 0 ? 0.5 * a * t * t : 0, xb = s.frame === 0 ? 0 : -0.5 * a * t * t;
      d.line([-4.6, -1.2], [12.2, -1.2], { color: INK, width: 2 });
      for (var k = -4; k <= 12; k += 2) d.line([k, -1.2], [k - 0.5, -1.7], { color: MUTED, width: 1 });
      // 車廂
      var x0 = xt - 3.4, x1 = xt + 3.4;
      d.rect(x0, -1.0, x1, 1.6, { color: INK, width: 2 });
      d.circle([x0 + 1, -1.0], 5, { color: INK, width: 1.5 }); d.circle([x1 - 1, -1.0], 5, { color: INK, width: 1.5 });
      d.arrow([x1 + 0.3, 0.6], [x1 + 1.7, 0.6], { color: RED, width: 2, head: 9 });
      d.label([x1 + 1.0, 1.15], "a", { color: RED, size: 13 });
      // 球（在車廂地板上）
      d.dot([xb, -0.75], { color: BLUE, r: 6 });
      d.line([0, -1.4], [0, 2.3], { color: MUTED, width: 1, dash: "3 4" });
      d.label([0, 2.65], s.frame === 0 ? "\\text{地面的 }x=0" : "\\text{車廂的起點}", { color: MUTED, size: 12 });
      if (s.frame === 1 && t > 0.3) d.arrow([xb - 0.2, 0.2], [xb - 1.4, 0.2], { color: BLUE, width: 1.6, head: 8 });
    },
    formula: function (s) {
      var t = s.t, h = 0.5 * t * t;
      return s.frame === 0 ? "t=" + F(t, 1) + "\\ \\text{s}:\\ x_{\\text{球}}=0,\\quad x_{\\text{車}}=\\tfrac12at^2=" + F(h, 2) + "\\ \\text{m}"
                           : "t=" + F(t, 1) + "\\ \\text{s}:\\ x'_{\\text{球}}=-\\tfrac12at^2=" + F(-h, 2) + "\\ \\text{m},\\quad\\ddot x'=-a";
    }
  });

  /* ---------------- 3. 斜面上的力（例題 2.1–2.3） ---------------- */
  A.define("c2-incline", {
    title: "斜面上的力：重力分量、正向力、摩擦",
    question: "角度和摩擦係數怎麼決定木塊的加速度？",
    view: [440, 230], origin: [318, 208], scale: 33,
    init: { th: 30, mode: 0 },
    steps: [
      { label: "例題 2.1：無摩擦 $30^\\circ$", caption: "重力 $mg$ 拆成沿斜面的 $mg\\sin\\theta$（虛線，往下坡）和垂直斜面的 $mg\\cos\\theta$；後者被正向力 $N$ 抵消。$\\ddot x=g\\sin30^\\circ=4.9\\ \\text{m/s}^2$。", set: { mode: 0 }, to: { th: 30 }, dur: 400, hold: 2600 },
      { label: "靜摩擦，$15^\\circ$", caption: "$\\mu_s=0.4$。$15^\\circ$ 時下滑分量只有 $0.26mg$，靜摩擦（綠）只需要給這麼多，木塊不動；它的上限是 $\\mu_sN=0.39mg$。", set: { mode: 1 }, to: { th: 15 }, dur: 1600, hold: 2400 },
      { label: "臨界角 $21.8^\\circ$", caption: "角度加大，需要的靜摩擦跟著變大，到 $\\tan\\theta=\\mu_s$ 時剛好等於上限 $\\mu_sN$。再大一點就滑了（例題 2.2）。", set: { mode: 1 }, to: { th: 21.8 }, dur: 1800, hold: 2400 },
      { label: "滑動：$\\mu_k=0.3$、$30^\\circ$", caption: "開始滑之後換成動摩擦 $\\mu_kN$，大小固定。$\\ddot x=g(\\sin30^\\circ-0.3\\cos30^\\circ)=0.24g=2.35\\ \\text{m/s}^2$（例題 2.3）。", set: { mode: 2 }, to: { th: 30 }, dur: 1600, hold: 2600 }
    ],
    draw: function (d, s) {
      var th = rad(s.th), c = Math.cos(th), sn = Math.sin(th), L = 8.4;
      var bot = [3, 0], top = [3 - L * c, L * sn];
      d.poly([bot, top, [top[0], 0]], { color: INK, width: 2, fill: "var(--grid)", fillOpacity: 0.35 });
      d.arc(bot, 1.1, 180 - s.th, 180, { color: MUTED, width: 1.2 });
      d.label([bot[0] - 1.7, 0.35], "\\theta", { color: MUTED, size: 12 });
      var dn = [c, -sn], nn = [sn, c];                   // 下坡方向、法線方向
      var mid = [bot[0] - c * 5.6, sn * 5.6];
      var C = [mid[0] + nn[0] * 0.55, mid[1] + nn[1] * 0.55], hw = 0.55;
      d.poly([[C[0] - dn[0] * hw - nn[0] * hw, C[1] - dn[1] * hw - nn[1] * hw], [C[0] + dn[0] * hw - nn[0] * hw, C[1] + dn[1] * hw - nn[1] * hw],
              [C[0] + dn[0] * hw + nn[0] * hw, C[1] + dn[1] * hw + nn[1] * hw], [C[0] - dn[0] * hw + nn[0] * hw, C[1] - dn[1] * hw + nn[1] * hw]], { color: INK, width: 2 });
      var Lg = 2.0, P0 = mid;
      d.arrow(C, [C[0], C[1] - Lg], { color: RED, width: 2.2 });
      d.label([C[0] + 0.42, C[1] - Lg + 0.1], "mg", { color: RED, size: 12 });
      d.arrow(C, [C[0] + dn[0] * Lg * sn, C[1] + dn[1] * Lg * sn], { color: RED, width: 1.4, dash: "4 3" });
      d.arrow(C, [C[0] - nn[0] * Lg * c, C[1] - nn[1] * Lg * c], { color: RED, width: 1.4, dash: "4 3" });
      d.arrow(C, [C[0] + nn[0] * Lg * c, C[1] + nn[1] * Lg * c], { color: BLUE, width: 2.2 });
      d.label([C[0] + nn[0] * (Lg * c + 0.4), C[1] + nn[1] * (Lg * c + 0.4)], "N", { color: BLUE, size: 12 });
      var f = 0;
      if (s.mode === 1) f = Math.min(sn, 0.4 * c); else if (s.mode === 2) f = 0.3 * c;
      if (f > 0.01) {
        var fe = [P0[0] - dn[0] * (Lg * f + 0.55), P0[1] - dn[1] * (Lg * f + 0.55)];
        d.arrow([P0[0] - dn[0] * 0.55, P0[1] - dn[1] * 0.55], fe, { color: GREEN, width: 2.4 });
        d.label([fe[0] - 0.1, fe[1] + 0.42], "f", { color: GREEN, size: 12 });
      }
    },
    formula: function (s) {
      var th = rad(s.th), sn = Math.sin(th), c = Math.cos(th);
      if (s.mode === 0) return "\\theta=" + F(s.th, 1) + "^\\circ:\\ \\ddot x=g\\sin\\theta=" + F(G * sn, 2) + "\\ \\text{m/s}^2";
      if (s.mode === 1) return "\\theta=" + F(s.th, 1) + "^\\circ:\\ f_s=mg\\sin\\theta=" + F(sn, 3) + "\\,mg\\ \\le\\ \\mu_sN=" + F(0.4 * c, 3) + "\\,mg";
      return "\\theta=" + F(s.th, 1) + "^\\circ:\\ \\ddot x=g(\\sin\\theta-\\mu_k\\cos\\theta)=" + F(G * (sn - 0.3 * c), 2) + "\\ \\text{m/s}^2";
    }
  });

  /* ---------------- 4. 水平線性阻力（例題 2.4） ---------------- */
  function plotAxes(d, xmax, ymax, xl, yl, xticks, yticks) {
    d.line([0, 0], [xmax, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, ymax], { color: MUTED, width: 1.3 });
    xticks.forEach(function (tk) { d.line([tk[0], 0], [tk[0], -0.12], { color: MUTED, width: 1 }); d.label([tk[0], -0.42], tk[1], { color: MUTED, size: 11 }); });
    yticks.forEach(function (tk) { d.line([0, tk[0]], [xmax, tk[0]], { color: GRID, width: 1 }); d.label([-0.42, tk[0]], tk[1], { color: MUTED, size: 11 }); });
    d.label([xmax + 0.1, -0.42], xl, { color: MUTED, size: 12 });
    d.label([0.55, ymax + 0.3], yl, { color: MUTED, size: 12 });
  }
  A.define("c2-linear-drag", {
    title: "線性阻力：速度指數衰減，距離趨近 $v_0/k$",
    question: "物體會在有限距離內停下嗎？",
    view: [440, 230], origin: [44, 190], scale: 42,
    init: { t: 0 },
    steps: [
      { label: "$t=1/k$", caption: "藍線是 $v/v_0=e^{-kt}$，紅線是 $x$ 除以 $v_0/k$。過了一個時間常數 $1/k$，速度剩 $37\\%$，已走完最終距離的 $63\\%$。", to: { t: 1 }, dur: 2200, hold: 1600 },
      { label: "$t=3/k$", caption: "$3/k$ 時速度剩 $5\\%$，距離到 $95\\%$。", to: { t: 3 }, dur: 2200, hold: 1600 },
      { label: "$t\\to\\infty$", caption: "速度永遠大於零（線性阻力在低速時也跟著變小），但總距離有上限 $v_0/k$。而且任何時刻 $v=v_0-kx$：兩條線加起來（各自歸一化）恆為 1。", to: { t: 8 }, dur: 2600, hold: 2400 }
    ],
    draw: function (d, s) {
      var sx = 1.1;   // 每 1/k 佔 1.1 單位
      plotAxes(d, 9.2, 3.4, "kt", "", [[sx, "1"], [3 * sx, "3"], [5 * sx, "5"], [8 * sx, "8"]], [[3, "1"], [1.5, "0.5"]]);
      var pv = [], px = [];
      for (var i = 0; i <= 160; i++) { var u = i / 20; if (u > s.t) break; pv.push([u * sx, 3 * Math.exp(-u)]); px.push([u * sx, 3 * (1 - Math.exp(-u))]); }
      if (pv.length > 1) { d.path(pv, { color: BLUE, width: 2.4 }); d.path(px, { color: RED, width: 2.4 }); }
      var e = Math.exp(-s.t);
      d.dot([s.t * sx, 3 * e], { color: BLUE }); d.dot([s.t * sx, 3 * (1 - e)], { color: RED });
      d.line([0, 3], [9.2, 3], { color: RED, width: 1, dash: "5 4", opacity: 0.6 });
      d.label([6.6, 2.62], "x/(v_0/k)", { color: RED, size: 12 });
      d.label([2.6, 0.75], "v/v_0", { color: BLUE, size: 12 });
    },
    formula: function (s) {
      var e = Math.exp(-s.t);
      return "kt=" + F(s.t, 1) + ":\\ \\frac{v}{v_0}=e^{-kt}=" + F(e, 4) + ",\\quad\\frac{kx}{v_0}=1-e^{-kt}=" + F(1 - e, 4);
    }
  });

  /* ---------------- 5. 終端速度（例題 2.5，Fig. 2-6） ---------------- */
  A.define("c2-terminal", {
    title: "不論初速多少，都趨近同一個終端速度 $g/k$",
    question: "初速比終端速度大的物體會加速還是減速？",
    view: [440, 230], origin: [44, 196], scale: 42,
    init: { t: 0 },
    steps: [
      { label: "$t=1/k$", caption: "向下的速率（以 $g/k$ 為單位）。三條線：由靜止落下、初速 $0.5\\,g/k$、初速 $1.6\\,g/k$。過了 $1/k$，三者和 $g/k$ 的差都只剩原來的 $37\\%$。", to: { t: 1 }, dur: 2400, hold: 1600 },
      { label: "$t=3/k$", caption: "初速 $1.6\\,g/k$ 的那條一開始就<strong>減速</strong>：向上的阻力比重力大。", to: { t: 3 }, dur: 2400, hold: 1600 },
      { label: "$t=6/k$", caption: "全部貼近 $v_t=g/k$：差距 $(v_0-v_t)e^{-kt}$ 指數消失，時間尺度 $1/k$。", to: { t: 6 }, dur: 2400, hold: 2400 }
    ],
    draw: function (d, s) {
      var sx = 1.45, sy = 2.1;
      plotAxes(d, 9.2, 3.7, "kt", "", [[sx, "1"], [3 * sx, "3"], [6 * sx, "6"]], [[sy, "g/k"]]);
      d.line([0, sy], [9.2, sy], { color: MUTED, width: 1.2, dash: "5 4" });
      [[0, BLUE], [0.5, GREEN], [1.6, RED]].forEach(function (c) {
        var pts = [];
        for (var i = 0; i <= 120; i++) { var u = i / 20; if (u > s.t) break; pts.push([u * sx, sy * (1 + (c[0] - 1) * Math.exp(-u))]); }
        if (pts.length > 1) d.path(pts, { color: c[1], width: 2.3 });
        d.dot([s.t * sx, sy * (1 + (c[0] - 1) * Math.exp(-s.t))], { color: c[1] });
      });
      d.label([1.9, sy * 1.6 + 0.1], "v_0=1.6\\,g/k", { color: RED, size: 11 });
      d.label([1.0, 0.25], "v_0=0", { color: BLUE, size: 11 });
      d.label([0.8, 1.9], "v_0=0.5\\,g/k", { color: GREEN, size: 10 });
    },
    formula: function (s) {
      var e = Math.exp(-s.t);
      return "kt=" + F(s.t, 1) + ":\\ \\frac{v}{g/k}=1+\\Big(\\frac{v_0}{g/k}-1\\Big)e^{-kt}\\\\ (v_0=0,\\ 0.5,\\ 1.6\\,g/k):\\ " + F(1 - e, 3) + ",\\ " + F(1 - 0.5 * e, 3) + ",\\ " + F(1 + 0.6 * e, 3);
    }
  });

  /* ---------------- 6. 指數阻力的船（習題 2-39） ---------------- */
  A.define("c2-boat", {
    title: "阻力 $\\alpha e^{\\beta v}$：船在有限時間內停下",
    question: "為什麼線性阻力永遠停不下來？",
    view: [440, 230], origin: [44, 196], scale: 42,
    init: { t: 0 },
    steps: [
      { label: "$t=0.43$", caption: "$m=\\alpha=\\beta=1$、$v_0=2$（紅線）。藍虛線是線性阻力 $kmv$（$k=2\\ \\text{s}^{-1}$）作比較。", to: { t: 0.43 }, dur: 2200, hold: 1500 },
      { label: "$t_{\\text{end}}=0.865$", caption: "紅線在 $t_{\\text{end}}=\\frac{m}{\\alpha\\beta}(1-e^{-\\beta v_0})=0.865$ 剛好降到零：低速時阻力趨近 $\\alpha$，不會變小，所以能把船完全停下。", to: { t: 0.8647 }, dur: 2200, hold: 2000 },
      { label: "之後", caption: "藍線在 $v\\to0$ 時阻力也 $\\to0$，只能指數地逼近零，永遠不停。", to: { t: 1.6 }, dur: 2200, hold: 2200 }
    ],
    draw: function (d, s) {
      var sx = 5.4, sy = 1.6;
      plotAxes(d, 9.2, 3.6, "t", "v", [[0.5 * sx, "0.5"], [0.8647 * sx, "t_{\\text{end}}"], [1.5 * sx, "1.5"]], [[2 * sy, "2"], [sy, "1"]]);
      var te = 1 - Math.exp(-2), pr = [], pb = [];
      for (var i = 0; i <= 160; i++) {
        var u = i / 100; if (u > s.t) break;
        pr.push([u * sx, sy * Math.max(0, u < te ? -Math.log(u + Math.exp(-2)) : 0)]);
        pb.push([u * sx, sy * 2 * Math.exp(-2 * u)]);
      }
      if (pr.length > 1) { d.path(pr, { color: RED, width: 2.4 }); d.path(pb, { color: BLUE, width: 2.2, dash: "6 4" }); }
      var vr = s.t < te ? -Math.log(s.t + Math.exp(-2)) : 0;
      d.dot([s.t * sx, sy * vr], { color: RED }); d.dot([s.t * sx, sy * 2 * Math.exp(-2 * s.t)], { color: BLUE });
      d.label([2.3, 0.4], "-\\alpha e^{\\beta v}", { color: RED, size: 12 });
      d.label([2.7, 2.0], "-kmv", { color: BLUE, size: 12 });
    },
    formula: function (s) {
      var te = 1 - Math.exp(-2), vr = s.t < te ? -Math.log(s.t + Math.exp(-2)) : 0;
      return "t=" + F(s.t, 2) + ":\\ v=-\\ln\\!\\big(t+e^{-2}\\big)=" + F(vr, 3) + ",\\quad v_{\\text{線性}}=2e^{-2t}=" + F(2 * Math.exp(-2 * s.t), 3);
    }
  });

  /* ---------------- 7. 拋體與 45°（例題 2.6） ---------------- */
  A.define("c2-projectile", {
    title: "射程 $R=v_0^2\\sin2\\theta/g$：$45^\\circ$ 最遠",
    question: "仰角從 $30^\\circ$ 調到 $75^\\circ$，射程怎麼變？",
    view: [440, 240], origin: [22, 214], scale: 39,
    init: { th: 30, p: 0 },
    steps: [
      { label: "$30^\\circ$", caption: "以 $v_0^2/g=10$ 為單位。$30^\\circ$：$R=10\\sin60^\\circ=8.66$。", set: { th: 30, p: 0 }, to: { p: 1 }, dur: 2200, hold: 1000 },
      { label: "$45^\\circ$", caption: "$45^\\circ$：$\\sin90^\\circ=1$，射程最大 $R=10$。", set: { th: 45, p: 0 }, to: { p: 1 }, dur: 2400, hold: 1200 },
      { label: "$60^\\circ$", caption: "$60^\\circ$：$\\sin120^\\circ=\\sin60^\\circ$，射程和 $30^\\circ$ <strong>一樣</strong>，只是飛得比較高、比較久。互餘的兩個角射程相同。", set: { th: 60, p: 0 }, to: { p: 1 }, dur: 2600, hold: 1400 },
      { label: "$75^\\circ$", caption: "$75^\\circ$ 與 $15^\\circ$ 互餘：$R=10\\sin150^\\circ=5$。最大高度 $\\frac{v_0^2\\sin^2\\theta}{2g}=4.67$。", set: { th: 75, p: 0 }, to: { p: 1 }, dur: 2800, hold: 2000 }
    ],
    draw: function (d, s) {
      d.line([0, 0], [10.7, 0], { color: MUTED, width: 1.3 });
      [2, 4, 6, 8, 10].forEach(function (x) { d.line([x, 0], [x, -0.12], { color: MUTED, width: 1 }); d.label([x, -0.36], String(x), { color: MUTED, size: 11 }); });
      var K = 10;
      [30, 45, 60, 75].forEach(function (a) {
        if (a >= s.th) return;
        var pts = [], tR = 2 * Math.sin(rad(a));
        for (var i = 0; i <= 60; i++) { var u = tR * i / 60; pts.push([K * Math.cos(rad(a)) * u, K * (Math.sin(rad(a)) * u - u * u / 2)]); }
        d.path(pts, { color: MUTED, width: 1.2, dash: "4 4", opacity: 0.8 });
      });
      var a = rad(s.th), T = 2 * Math.sin(a), pts = [];
      for (var i = 0; i <= 80; i++) { var u = T * Math.min(i / 80, s.p); pts.push([K * Math.cos(a) * u, K * (Math.sin(a) * u - u * u / 2)]); }
      d.path(pts, { color: BLUE, width: 2.5 });
      var last = pts[pts.length - 1];
      d.dot(last, { color: RED, r: 5.5 });
      d.arrow([0, 0], [1.4 * Math.cos(a), 1.4 * Math.sin(a)], { color: RED, width: 2, head: 9 });
      if (s.p > 0.98) { d.dot([K * Math.sin(2 * a), 0], { color: BLUE }); d.label([K * Math.sin(2 * a), 0.4], "R", { color: BLUE, size: 13 }); }
    },
    formula: function (s) {
      var a = rad(s.th);
      return "\\theta=" + F(s.th, 0) + "^\\circ:\\ R=\\frac{v_0^2}{g}\\sin2\\theta=" + F(10 * Math.sin(2 * a), 2) + ",\\quad y_{\\max}=" + F(5 * Math.sin(a) * Math.sin(a), 2);
    }
  });

  /* ---------------- 8. 線性阻力的拋體軌跡（例題 2.7，Fig. 2-8） ---------------- */
  var V7 = 600 * Math.sin(rad(60)), U7 = 600 * Math.cos(rad(60));
  function flight(k) {
    if (k === 0) return 2 * V7 / G;
    var f = function (T) { return -G * T / k + (k * V7 + G) / (k * k) * (1 - Math.exp(-k * T)); };
    var lo = 1e-3, hi = 2 * V7 / G + 1;
    for (var i = 0; i < 80; i++) { var mid = (lo + hi) / 2; if (f(mid) > 0) lo = mid; else hi = mid; }
    return (lo + hi) / 2;
  }
  function xy7(k, t) {
    if (k === 0) return [U7 * t, V7 * t - G * t * t / 2];
    return [U7 / k * (1 - Math.exp(-k * t)), -G * t / k + (k * V7 + G) / (k * k) * (1 - Math.exp(-k * t))];
  }
  var K7 = [0, 0.005, 0.01, 0.02, 0.04];
  A.define("c2-drag-traj", {
    title: "線性阻力讓軌跡變矮、變短、變得不對稱",
    question: "阻力常數 $k$ 加大，射程怎麼變？微擾公式什麼時候失準？",
    view: [440, 225], origin: [26, 196], scale: 118,
    init: { ki: 0, p: 0 },
    steps: [
      { label: "$k=0$", caption: "課本 Fig. 2-8 的數據：$v_0=600\\ \\text{m/s}$、$\\theta=60^\\circ$，座標以 $10^4\\ \\text{m}$ 為單位。無阻力的拋物線，$R=3.18\\times10^4\\ \\text{m}$。", set: { ki: 0, p: 0 }, to: { p: 1 }, dur: 2000, hold: 1000 },
      { label: "$k=0.005\\ \\text{s}^{-1}$", caption: "射程 $2.33\\times10^4\\ \\text{m}$；微擾式 $R(1-\\frac{4kV}{3g})$ 給 $2.06$，已低估 $12\\%$。", set: { ki: 1, p: 0 }, to: { p: 1 }, dur: 2000, hold: 1400 },
      { label: "$k=0.01$", caption: "射程 $1.81$；微擾式只給 $0.93$，完全不能用（$k$ 已接近 $g/V=0.019$）。", set: { ki: 2, p: 0 }, to: { p: 1 }, dur: 2000, hold: 1400 },
      { label: "$k=0.02$", caption: "射程 $1.22$。下降段明顯比上升段陡：水平速度 $Ue^{-kt}$ 一直在衰減。", set: { ki: 3, p: 0 }, to: { p: 1 }, dur: 2000, hold: 1400 },
      { label: "$k=0.04$", caption: "阻力成為主角：最後幾乎垂直落下，鉛直速度趨近終端速度 $g/k$。", set: { ki: 4, p: 0 }, to: { p: 1 }, dur: 2000, hold: 2200 }
    ],
    draw: function (d, s) {
      d.line([0, 0], [3.4, 0], { color: MUTED, width: 1.3 }); d.line([0, 0], [0, 1.45], { color: MUTED, width: 1.3 });
      [1, 2, 3].forEach(function (x) { d.line([x, 0], [x, -0.03], { color: MUTED, width: 1 }); d.label([x, -0.1], String(x), { color: MUTED, size: 11 }); });
      [0.5, 1].forEach(function (y) { d.line([0, y], [3.3, y], { color: GRID, width: 1 }); d.label([-0.1, y], String(y), { color: MUTED, size: 11 }); });
      for (var j = 0; j <= s.ki; j++) {
        var k = K7[j], T = flight(k), pts = [], frac = j === s.ki ? s.p : 1;
        for (var i = 0; i <= 90; i++) { var q = xy7(k, T * Math.min(i / 90, frac)); pts.push([q[0] / 1e4, q[1] / 1e4]); }
        d.path(pts, { color: j === s.ki ? BLUE : MUTED, width: j === s.ki ? 2.5 : 1.3, opacity: j === s.ki ? 1 : 0.85 });
        if (j === s.ki) d.dot(pts[pts.length - 1], { color: RED, r: 5 });
      }
      var Rp = 31812 * (1 - 4 * K7[s.ki] * V7 / (3 * G));
      if (s.ki > 0 && Rp > 0) { d.dot([Rp / 1e4, 0], { color: RED, r: 4 }); d.label([Rp / 1e4, 0.12], "\\text{微擾}", { color: RED, size: 11 }); }
    },
    formula: function (s) {
      var k = K7[s.ki], T = flight(k), R = xy7(k, T)[0], Rp = 31812 * (1 - 4 * k * V7 / (3 * G));
      return "k=" + F(k, 3) + ":\\ R'_{\\text{數值}}=" + F(R / 1e4, 2) + "\\times10^4\\ \\text{m},\\quad R\\Big(1-\\frac{4kV}{3g}\\Big)=" + F(Rp / 1e4, 2) + "\\times10^4\\ \\text{m}";
    }
  });

  /* ---------------- 9. v² 阻力的上拋（習題 2-12） ---------------- */
  var K12 = 0.01, V12 = 30, VT12 = Math.sqrt(G / K12), XM12 = Math.log(1 + K12 * V12 * V12 / G) / (2 * K12);
  A.define("c2-updown", {
    title: "$v^2$ 阻力：上升、下降分開算，回來時比較慢",
    question: "回到出發點時的速率是多少？",
    view: [440, 280], origin: [34, 142], scale: 40,
    init: { ph: 0 },
    steps: [
      { label: "上升", caption: "橫軸是高度、縱軸是速度（向上為正）。$v_0=30\\ \\text{m/s}$、$k=0.01\\ \\text{m}^{-1}$（$v_t=31.3\\ \\text{m/s}$）。阻力和重力都向下，到最高點 $x_{\\max}=\\frac1{2k}\\ln\\frac{g+kv_0^2}{g}=32.6\\ \\text{m}$。", set: { ph: 0 }, to: { ph: 1 }, dur: 2600, hold: 1400 },
      { label: "下降", caption: "最高點起換一條方程式：阻力向上、重力向下。$v^2=\\frac gk(1-e^{-2kx})$，下落 $32.6\\ \\text{m}$ 回到原點。", to: { ph: 2 }, dur: 2600, hold: 1400 },
      { label: "和無阻力比較", caption: "虛線是無阻力：上到 $45.9\\ \\text{m}$、以 $30\\ \\text{m/s}$ 回來。有阻力時回來只有 $\\frac{v_0v_t}{\\sqrt{v_0^2+v_t^2}}=21.7\\ \\text{m/s}$。", dur: 300, hold: 3200 }
    ],
    draw: function (d, s) {
      var sx = 0.2, sy = 0.1;   // 每格：5 m、10 m/s
      d.line([0, 0], [9.6, 0], { color: MUTED, width: 1.3 }); d.line([0, -3.3], [0, 3.3], { color: MUTED, width: 1.3 });
      [10, 20, 30, 40].forEach(function (x) { d.line([x * sx, 0], [x * sx, -0.1], { color: MUTED, width: 1 }); d.label([x * sx, -0.35], String(x), { color: MUTED, size: 11 }); });
      [-30, -20, 20, 30].forEach(function (v) { d.line([0, v * sy], [9.4, v * sy], { color: GRID, width: 1 }); d.label([-0.42, v * sy], String(v), { color: MUTED, size: 11 }); });
      d.label([8.3, 0.3], "x\\,(\\text{m})", { color: MUTED, size: 11 });
      d.label([0.75, 3.15], "v\\,(\\text{m/s})", { color: MUTED, size: 11 });
      if (s._step === 2) {
        var nd = [], xm0 = V12 * V12 / (2 * G);
        for (var i = 0; i <= 60; i++) { var x = xm0 * i / 60; nd.push([x * sx, Math.sqrt(Math.max(0, V12 * V12 - 2 * G * x)) * sy]); }
        d.path(nd, { color: MUTED, width: 1.3, dash: "5 4" });
        d.path(nd.map(function (p) { return [p[0], -p[1]]; }), { color: MUTED, width: 1.3, dash: "5 4" });
      }
      var up = [], dn = [], cur;
      var fu = Math.min(1, s.ph), fd = clamp(s.ph - 1, 0, 1);
      for (var j = 0; j <= 80; j++) {
        var xu = XM12 * Math.min(j / 80, fu);
        up.push([xu * sx, Math.sqrt(Math.max(0, G / K12 * ((1 + K12 * V12 * V12 / G) * Math.exp(-2 * K12 * xu) - 1))) * sy]);
      }
      d.path(up, { color: BLUE, width: 2.5 });
      cur = up[up.length - 1];
      if (s.ph > 1) {
        for (var q = 0; q <= 80; q++) {
          var fall = XM12 * Math.min(q / 80, fd);
          dn.push([(XM12 - fall) * sx, -Math.sqrt(G / K12 * (1 - Math.exp(-2 * K12 * fall))) * sy]);
        }
        d.path(dn, { color: RED, width: 2.5 });
        cur = dn[dn.length - 1];
      }
      d.dot(cur, { color: s.ph > 1 ? RED : BLUE, r: 5 });
      d.label([2.2, 1.5], "\\text{上升}", { color: BLUE, size: 12 });
      d.label([2.2, -1.2], "\\text{下降}", { color: RED, size: 12 });
    },
    formula: function (s) {
      if (s.ph <= 1) { var x = XM12 * s.ph, v = Math.sqrt(Math.max(0, G / K12 * ((1 + K12 * V12 * V12 / G) * Math.exp(-2 * K12 * x) - 1))); return "\\text{上升 }x=" + F(x, 1) + "\\ \\text{m}:\\ v=" + F(v, 1) + "\\ \\text{m/s}"; }
      var fall = XM12 * clamp(s.ph - 1, 0, 1), vd = Math.sqrt(G / K12 * (1 - Math.exp(-2 * K12 * fall)));
      return "\\text{下降 }" + F(fall, 1) + "\\ \\text{m}:\\ |v|=" + F(vd, 2) + "\\ \\text{m/s}\\quad(\\tfrac{v_0v_t}{\\sqrt{v_0^2+v_t^2}}=" + F(V12 * VT12 / Math.sqrt(V12 * V12 + VT12 * VT12), 2) + ")";
    }
  });

  /* ---------------- 10. Atwood 機（例題 2.9） ---------------- */
  A.define("c2-atwood", {
    title: "Atwood 機：電梯下降加速時 $g$ 變成 $g-\\alpha$",
    question: "電梯的加速度怎麼改變物體的加速度和張力？",
    view: [440, 250], origin: [150, 222], scale: 26,
    init: { al: 0, p: 0 },
    steps: [
      { label: "(a) 滑輪固定", caption: "$m_1=3\\ \\text{kg}$、$m_2=2\\ \\text{kg}$。$\\ddot x_1=\\frac{(m_1-m_2)g}{m_1+m_2}=\\frac g5=1.96\\ \\text{m/s}^2$，$T=\\frac{2m_1m_2g}{m_1+m_2}=23.5\\ \\text{N}$。", set: { al: 0, p: 0 }, to: { p: 1 }, dur: 2600, hold: 1400 },
      { label: "(b) $\\alpha=g/2$", caption: "電梯以 $\\alpha=4.9\\ \\text{m/s}^2$ 向下加速。從電梯外的慣性系寫 $F=ma$，相對滑輪的加速度和張力都按 $g-\\alpha$ 縮小一半。", set: { al: 0.5, p: 0 }, to: { p: 1 }, dur: 2600, hold: 1400 },
      { label: "$\\alpha=g$", caption: "電梯自由落下：$g-\\alpha=0$，繩子鬆了（$T=0$），兩物體相對滑輪不動——整台機器一起自由落下。", set: { al: 1, p: 0 }, to: { p: 1 }, dur: 2400, hold: 2200 }
    ],
    draw: function (d, s) {
      var m1 = 3, m2 = 2, a = (m1 - m2) * (1 - s.al) / (m1 + m2), disp = 2.2 * a / 0.2 * s.p;   // 位移按比例示意
      var cx = 0, cy = 6.6, r = 0.9;
      d.rect(-3.6, -0.6, 3.6, 7.8, { color: MUTED, width: 1.4, dash: "6 4" });
      d.label([4.9, 7.5], "\\text{電梯}", { color: MUTED, size: 12 });
      if (s.al > 0) { d.arrow([4.6, 5.4], [4.6, 5.4 - 1.6 * s.al - 0.2], { color: PURPLE, width: 2, head: 9 }); d.label([5.6, 4.6], "\\alpha", { color: PURPLE, size: 13 }); }
      d.line([cx, cy], [cx, 7.8], { color: INK, width: 2 });
      d.circle([cx, cy], r * 26, { color: INK, width: 2 }); d.dot([cx, cy], { r: 3 });
      var y1 = 2.6 - disp, y2 = 2.6 + disp;
      d.line([-r, cy], [-r, y1 + 0.55], { color: INK, width: 1.6 }); d.line([r, cy], [r, y2 + 0.45], { color: INK, width: 1.6 });
      d.rect(-r - 0.6, y1 - 0.65, -r + 0.6, y1 + 0.55, { color: BLUE, width: 2 });
      d.rect(r - 0.5, y2 - 0.55, r + 0.5, y2 + 0.45, { color: RED, width: 2 });
      d.label([-r, y1 - 0.05], "m_1", { color: BLUE, size: 12 }); d.label([r, y2 - 0.05], "m_2", { color: RED, size: 12 });
      var T = 2 * m1 * m2 * G * (1 - s.al) / (m1 + m2);
      if (T > 0.5) { d.arrow([-r, y1 + 0.6], [-r, y1 + 0.6 + T / 14], { color: GREEN, width: 2, head: 8 }); d.label([-r - 0.75, y1 + 1.35], "T", { color: GREEN, size: 12 }); }
    },
    formula: function (s) {
      var ge = G * (1 - s.al);
      return "\\alpha=" + F(G * s.al, 1) + ":\\ \\ddot x_1=\\frac{(m_1-m_2)(g-\\alpha)}{m_1+m_2}=" + F(ge / 5, 2) + "\\ \\text{m/s}^2,\\ T=\\frac{2m_1m_2(g-\\alpha)}{m_1+m_2}=" + F(12 * ge / 5, 1) + "\\ \\text{N}";
    }
  });

  /* ---------------- 11. 磁場中的螺旋（例題 2.10） ---------------- */
  A.define("c2-helix", {
    title: "帶電粒子在均勻磁場中：沿 $\\vec B$ 漂移＋垂直平面上的圓",
    question: "沿著磁場方向看，軌跡是什麼形狀？",
    view: [440, 250], origin: [110, 140], scale: 34,
    init: { p: 0, az: 35, el: 18 },
    steps: [
      { label: "螺旋前進", caption: "$\\vec B$ 沿 $y$ 軸。$y$ 方向不受力，$y=\\dot y_0t$ 等速；$x$、$z$ 方向繞圈。三圈的軌跡是一條圓螺旋。", set: { p: 0 }, to: { p: 1 }, dur: 4200, hold: 1400 },
      { label: "順著 $\\vec B$ 看", caption: "轉動視角，沿 $y$ 軸看過去：所有的圈疊成一個半徑 $\\dot z_0m/qB_0$ 的圓。磁力永遠垂直速度，速率不變。", to: { az: 90, el: 0 }, dur: 2400, hold: 2600 }
    ],
    draw: function (d, s) {
      d.camera(s.az, s.el);
      var R = 1.4, pitch = 1.5, turns = 3, pts = [];
      d.arrow3([0, -0.6, 0], [0, 8, 0], { color: MUTED, width: 1.3, head: 9 }); if (s.az < 80) d.label3([0, 8.5, 0], "y", { color: MUTED, size: 12 });
      d.arrow3([0, 0, 0], [2.4, 0, 0], { color: MUTED, width: 1.3, head: 9 }); d.label3([2.8, 0, 0], "x", { color: MUTED, size: 12 });
      d.arrow3([0, 0, 0], [0, 0, 2.4], { color: MUTED, width: 1.3, head: 9 }); d.label3([0, 0, 2.85], "z", { color: MUTED, size: 12 });
      if (s.az < 80) { d.arrow3([0, 4.6, 2.5], [0, 7.4, 2.5], { color: PURPLE, width: 2.2, head: 10 }); d.label3([0, 6.0, 3.05], "\\vec B", { color: PURPLE, size: 13 }); }
      else d.label([0, -2.45], "\\vec B\\ \\text{指向讀者}", { color: PURPLE, size: 12 });
      var n = Math.max(2, Math.round(240 * s.p));
      for (var i = 0; i <= n; i++) { var ph = 2 * Math.PI * turns * i / 240; pts.push([R * Math.cos(ph), pitch * ph / (2 * Math.PI), R * Math.sin(ph)]); }
      d.path3(pts, { color: BLUE, width: 2.2 });
      d.dot3(pts[pts.length - 1], { color: RED, r: 5 });
    },
    formula: function (s) {
      var ph = 2 * Math.PI * 3 * s.p;
      return "\\alpha t=" + F(ph, 2) + ":\\ x-x_0=\\frac{\\dot z_0}{\\alpha}\\cos\\alpha t,\\ z-z_0=\\frac{\\dot z_0}{\\alpha}\\sin\\alpha t,\\ y-y_0=\\dot y_0t";
    }
  });

  /* ---------------- 12. 重力和摩擦沿不同路徑的功（講義 p.128–130） ---------------- */
  var PATHS = (function () {
    var a = [], b = [], c = [];
    for (var i = 0; i <= 40; i++) { var u = i / 40; a.push([6 * u, 3 * u]); }
    for (var j = 0; j <= 40; j++) { var v = j / 40; b.push(v < 0.5 ? [0, 6 * v] : [6 * (v - 0.5) * 2, 3]); }
    for (var k = 0; k <= 80; k++) { var w = k / 80; c.push([6 * w, 3 * w - 1.6 * Math.sin(Math.PI * w)]); }
    function len(p) { var L = 0; for (var q = 1; q < p.length; q++) L += Math.hypot(p[q][0] - p[q - 1][0], p[q][1] - p[q - 1][1]); return L; }
    return [{ pts: a, L: len(a), name: "a" }, { pts: b, L: len(b), name: "b" }, { pts: c, L: len(c), name: "c" }];
  })();
  A.define("c2-work-path", {
    title: "重力的功只看高度差，摩擦的功看路徑長",
    question: "從 A 到 B 走三條不同的路，哪個功會變？",
    view: [440, 230], origin: [60, 175], scale: 28,
    init: { k: 0, p: 0 },
    steps: [
      { label: "路徑 a：直線", caption: "A 到 B 上升 $3$ 個單位。重力的功 $W_g=-mg\\,\\Delta z=-3mg$；摩擦的功 $-F_kS$，直線最短 $S=6.71$。", set: { k: 0, p: 0 }, to: { p: 1 }, dur: 2000, hold: 1400 },
      { label: "路徑 b：先上再右", caption: "先垂直上升 3、再水平走 6：$W_g$ 仍是 $-3mg$（水平段重力不做功），但 $S=9$，摩擦做更多負功。", set: { k: 1, p: 0 }, to: { p: 1 }, dur: 2000, hold: 1400 },
      { label: "路徑 c：先下再上", caption: "先往下再爬上去：下坡時重力做正功、上坡做負功，相加還是 $-3mg$；摩擦的功卻隨路徑長變大。重力保守，摩擦不保守。", set: { k: 2, p: 0 }, to: { p: 1 }, dur: 2200, hold: 2400 }
    ],
    draw: function (d, s) {
      d.line([-0.8, 0], [7.4, 0], { color: GRID, width: 1 }); d.line([-0.8, 3], [7.4, 3], { color: GRID, width: 1 });
      d.arrow([-1.2, -1.4], [-1.2, 4.0], { color: MUTED, width: 1.3, head: 8 }); d.label([-1.55, 3.9], "z", { color: MUTED, size: 12 });
      for (var j = 0; j < PATHS.length; j++) {
        if (j > s.k) break;
        var P = PATHS[j], n = j === s.k ? Math.max(1, Math.round((P.pts.length - 1) * s.p)) : P.pts.length - 1;
        d.path(P.pts.slice(0, n + 1), { color: j === s.k ? BLUE : MUTED, width: j === s.k ? 2.5 : 1.3, opacity: j === s.k ? 1 : 0.8 });
        if (j === s.k) d.dot(P.pts[n], { color: RED, r: 5 });
      }
      d.dot([0, 0], { r: 4 }); d.dot([6, 3], { r: 4 });
      d.label([-0.4, -0.45], "A", { size: 13 }); d.label([6.4, 3.35], "B", { size: 13 });
      d.label([2.7, 2.0], "a", { color: MUTED, size: 12 }); d.label([0.35, 1.6], "b", { color: MUTED, size: 12 }); d.label([3.7, -0.3], "c", { color: MUTED, size: 12 });
    },
    formula: function (s) {
      return "\\text{路徑 }" + PATHS[s.k].name + ":\\ W_g=-mg(z_B-z_A)=-3mg,\\quad W_f=-F_kS=-" + F(PATHS[s.k].L, 2) + "\\,F_k";
    }
  });

  /* ---------------- 13. 迴圈軌道（習題 2-25） ---------------- */
  var H25 = 3.91, R25 = 1.0, XA = 4.0;
  var XB = XA + R25 / Math.SQRT2, YB = R25 - R25 / Math.SQRT2;
  var VB = Math.sqrt(2 * G * (H25 - YB));
  var TL = (VB / Math.SQRT2 + Math.sqrt(VB * VB / 2 + 2 * G * YB)) / G;
  function track(u) {   // u ∈ [0,1]：斜坡；[1,2]：圓弧
    if (u <= 1) return [XA * u, H25 * (1 + Math.cos(Math.PI * u)) / 2];
    var ang = (u - 1) * Math.PI / 4;   // 從最低點轉到 45°
    return [XA + R25 * Math.sin(ang), R25 - R25 * Math.cos(ang)];
  }
  A.define("c2-loop", {
    title: "能量守恆給速率，圓周方程式給正向力",
    question: "木塊在 A、B 兩點的速率與正向力是多少？落在哪裡？",
    view: [440, 212], origin: [20, 168], scale: 31,
    init: { u: 0 },
    steps: [
      { label: "滑到 A", caption: "設 $R=1\\ \\text{m}$ 示意（課本沒給 $R$）。光滑軌道，$v_A=\\sqrt{2gh}=8.75\\ \\text{m/s}$；最低點 $N_A=mg(1+2h/R)=8.82\\,mg$。", to: { u: 1 }, dur: 2400, hold: 1600 },
      { label: "到 B（$45^\\circ$）", caption: "B 比 A 高 $h'=R(1-\\cos45^\\circ)=0.29\\ \\text{m}$：$v_B=\\sqrt{2g(h-h')}=8.42\\ \\text{m/s}$，$N_B=mg[2h/R+3/\\sqrt2-2]=7.94\\,mg$。", to: { u: 2 }, dur: 1600, hold: 1600 },
      { label: "飛出去", caption: "離開時速度沿切線、與水平夾 $45^\\circ$。拋體落地點離 A：$d=\\frac{R}{\\sqrt2}+(h-h')+\\sqrt{h^2-h'^2}=8.22\\ \\text{m}$。", to: { u: 3 }, dur: 2600, hold: 2400 }
    ],
    draw: function (d, s) {
      d.line([-0.4, 0], [13.3, 0], { color: MUTED, width: 1.2 });
      var tp = [];
      for (var i = 0; i <= 80; i++) tp.push(track(2 * i / 80));
      d.path(tp, { color: INK, width: 2.6 });
      d.arc([XA, R25], R25, -90, -45, { color: INK, width: 2.6 });
      d.line([XA, R25], [XB, YB], { color: MUTED, width: 1, dash: "3 3" }); d.line([XA, R25], [XA, 0], { color: MUTED, width: 1, dash: "3 3" });
      d.label([XA - 0.25, -0.38], "A", { size: 12 }); d.label([XB + 0.35, YB - 0.2], "B", { size: 12 });
      d.line([0, 0], [0, H25], { color: MUTED, width: 1, dash: "3 4" }); d.label([-0.0, H25 / 2], "h", { color: MUTED, size: 12, dx: 8 });
      var fl = [];
      for (var q = 0; q <= 60; q++) { var tq = TL * q / 60; fl.push([XB + VB / Math.SQRT2 * tq, YB + VB / Math.SQRT2 * tq - G * tq * tq / 2]); }
      d.path(fl, { color: MUTED, width: 1.2, dash: "5 4" });
      var pos;
      if (s.u <= 2) pos = track(s.u);
      else { var tt = TL * (s.u - 2); pos = [XB + VB / Math.SQRT2 * tt, YB + VB / Math.SQRT2 * tt - G * tt * tt / 2]; }
      d.dot([pos[0], pos[1] + 0.12], { color: RED, r: 6 });
      if (s._step === 0 && s._p > 0.95) { d.arrow([XA, 0.15], [XA, 1.6], { color: BLUE, width: 2.2, head: 9 }); d.label([XA + 0.45, 1.3], "N_A", { color: BLUE, size: 12 }); }
      if (s._step === 1 && s._p > 0.95) { d.arrow([XB, YB], [XB - 0.9, YB + 0.9], { color: BLUE, width: 2.2, head: 9 }); d.label([XB - 1.2, YB + 1.25], "N_B", { color: BLUE, size: 12 }); }
      if (s._step === 2 && s._p > 0.95) {
        var dl = XB + VB / Math.SQRT2 * TL; d.dot([dl, 0], { color: BLUE });
        d.line([XA, -0.6], [dl, -0.6], { color: BLUE, width: 1.3 });
        d.line([XA, -0.4], [XA, -0.8], { color: BLUE, width: 1.3 }); d.line([dl, -0.4], [dl, -0.8], { color: BLUE, width: 1.3 });
        d.label([(XA + dl) / 2, -0.95], "d=" + F(dl - XA, 2) + "\\ \\text{m}", { color: BLUE, size: 12 });
      }
    },
    formula: function (s) {
      var pos, y;
      if (s.u <= 2) { pos = track(s.u); y = pos[1]; }
      else { var tt = TL * (s.u - 2); pos = [XB + VB / Math.SQRT2 * tt, 0]; y = YB + VB / Math.SQRT2 * tt - G * tt * tt / 2; }
      var v = Math.sqrt(Math.max(0, 2 * G * (H25 - y)));
      return "\\frac Um=gy=" + F(G * y, 1) + ",\\ \\frac Tm=\\tfrac12v^2=" + F(v * v / 2, 1) + ",\\ \\frac Em=gh=" + F(G * H25, 1) + "\\ \\text{J/kg}";
    }
  });

  /* ---------------- 14. 雙井位能（例題 2.13） ---------------- */
  function Z13(y) { return -(y * y + 1) / (y * y * y * y + 8); }
  function turning13(E) {   // E/W；解 E y^4 + y^2 + 8E + 1 = 0 的 y^2
    var out = [], disc = 1 - 4 * E * (8 * E + 1);
    if (disc < 0) return out;
    [(-1 + Math.sqrt(disc)) / (2 * E), (-1 - Math.sqrt(disc)) / (2 * E)].forEach(function (y2) { if (y2 >= -1e-12) out.push(Math.sqrt(Math.max(0, y2))); });
    return out.sort(function (a, b) { return a - b; });
  }
  A.define("c2-potential", {
    title: "雙井位能：能量決定能去哪裡",
    question: "$E$ 從谷底往上加，運動範圍怎麼變？",
    view: [440, 200], origin: [220, 48], scale: 34,
    init: { E: -0.22 },
    steps: [
      { label: "$E=-0.22W$", caption: "縱軸是 $U/W$（放大 10 倍畫）。能量低於中間的峰 $-W/8$：質點被困在其中一個谷裡，在兩個轉折點之間來回。", to: { E: -0.22 }, dur: 400, hold: 2600 },
      { label: "$E=-W/8$", caption: "能量剛好等於峰頂 $U(0)=-W/8$：轉折點 $x=\\pm2\\sqrt2\\,d$ 與 $x=0$（不穩定平衡點）。", to: { E: -0.125 }, dur: 2000, hold: 2600 },
      { label: "$E=-0.06W$", caption: "翻過中間的峰，在兩個谷之間來回：仍然有界，因為遠處 $U\\to0>E$。", to: { E: -0.06 }, dur: 2000, hold: 2400 },
      { label: "$E\\ge0$", caption: "$E\\ge0$ 時遠處 $E\\ge U$，質點可以跑到無限遠：無界運動。", to: { E: 0.02 }, dur: 1800, hold: 2400 }
    ],
    draw: function (d, s) {
      var sy = 10;   // U/W 放大 10 倍
      d.line([-6.2, 0], [6.2, 0], { color: MUTED, width: 1.2 }); d.line([0, 0.7], [0, -2.75], { color: MUTED, width: 1 });
      [-6, -3, 3, 6].forEach(function (x) { d.line([x, 0], [x, 0.1], { color: MUTED, width: 1 }); d.label([x, 0.4], String(x), { color: MUTED, size: 11 }); });
      d.label([4.6, 0.4], "x/d", { color: MUTED, size: 11 });
      d.line([-0.1, -1.25], [0.1, -1.25], { color: MUTED, width: 1 }); d.label([0.75, -1.12], "-\\tfrac18", { color: MUTED, size: 11 });
      d.line([-0.1, -2.5], [0.1, -2.5], { color: MUTED, width: 1 }); d.label([0.62, -2.62], "-\\tfrac14", { color: MUTED, size: 11 });
      var pts = [];
      for (var i = 0; i <= 240; i++) { var y = -6.2 + 12.4 * i / 240; pts.push([y, sy * Z13(y)]); }
      d.path(pts, { color: INK, width: 2.3 });
      var E = s.E, ys = turning13(E);
      d.line([-6.2, sy * E], [6.2, sy * E], { color: RED, width: 1.6, dash: "6 4" });
      // 允許區域加粗
      var allowed = [];
      for (var j = 0; j <= 240; j++) { var yy = -6.2 + 12.4 * j / 240; if (Z13(yy) <= E) allowed.push([yy, sy * E]); else if (allowed.length) { d.path(allowed, { color: RED, width: 3.2 }); allowed = []; } }
      if (allowed.length) d.path(allowed, { color: RED, width: 3.2 });
      ys.forEach(function (y) { if (y < 6.2) { d.dot([y, sy * E], { color: BLUE }); d.dot([-y, sy * E], { color: BLUE }); } });
    },
    formula: function (s) {
      var ys = turning13(s.E).filter(function (y) { return y < 50; });
      var t = ys.length ? ys.map(function (y) { return y < 1e-6 ? "0" : "\\pm" + F(y, 3); }).join(",\\ ") : "\\text{無（無界）}";
      return "\\frac{E}{W}=" + F(s.E, 3) + ":\\ \\text{轉折點 }\\frac xd=" + t;
    }
  });
  /* ---------------- 自編難題 c2-self-08b：獵人與猴子（影片也使用） ---------------- */
  // 飛鏢從原點朝 (D,H) 射出；猴子同時從 (D,H) 由靜止落下。k=0 為無阻力，k>0 為兩者都受 -km v 的線性阻力。
  var HM_D = 20, HM_H = 10;
  function hmDart(v0, k, t) {
    var c = HM_D / Math.hypot(HM_D, HM_H), s = HM_H / Math.hypot(HM_D, HM_H);
    if (k < 1e-6) return [v0 * c * t, v0 * s * t - 0.5 * G * t * t];
    var e = 1 - Math.exp(-k * t);
    return [v0 * c / k * e, (v0 * s + G / k) / k * e - G * t / k];
  }
  function hmDrop(k, t) {  // 兩者共同的「比無重力位置多掉的距離」
    if (k < 1e-6) return 0.5 * G * t * t;
    return G * t / k - G / (k * k) * (1 - Math.exp(-k * t));
  }
  function hmStraight(v0, k, t) {  // 無重力時沿瞄準線走的路程
    return k < 1e-6 ? v0 * t : v0 / k * (1 - Math.exp(-k * t));
  }
  function hmHitTime(v0, k) {  // 飛鏢到達 x=D 的時刻（到不了回傳 Infinity）
    var c = HM_D / Math.hypot(HM_D, HM_H);
    if (k < 1e-6) return HM_D / (v0 * c);
    var q = HM_D * k / (v0 * c);
    return q >= 1 ? Infinity : -Math.log(1 - q) / k;
  }
  function hmLandTime(k) {  // 猴子落地的時刻
    var lo = 0, hi = 10;
    for (var i = 0; i < 60; i++) { var m = (lo + hi) / 2; if (hmDrop(k, m) < HM_H) lo = m; else hi = m; }
    return lo;
  }
  A.define("c2-hunter-monkey", {
    title: "獵人與猴子：瞄準猴子，飛鏢和猴子一起往下掉",
    question: "猴子一放手就往下掉，為什麼還是要直接瞄準它？",
    view: [560, 360], origin: [44, 318], scale: 21.5,
    init: { tt: 0, v0: 25, k: 0, aim: 1, ghost: 0, drop: 0, link: 0, trail: 1, theta: 1, dims: 1 },
    steps: [
      { label: "瞄準", caption: "獵人在原點，猴子在 $(D,H)=(20,10)\\ \\text{m}$。槍口直接對準猴子：$\\tan\\theta=H/D$。", dur: 300, hold: 2200 },
      { label: "沒有重力的話", caption: "先想像關掉重力：飛鏢沿瞄準線直走（灰點），猴子停在原地，一定打中。", set: { ghost: 1, trail: 0 }, to: { tt: 0.89 }, dur: 2600, hold: 1600 },
      { label: "打開重力", caption: "重力讓兩者在同一段時間裡都比「無重力位置」多掉 $\\tfrac12gt^2$（紫色箭頭一樣長），所以還是在 $x=D$ 相遇。", set: { tt: 0, drop: 1, trail: 1 }, to: { tt: 0.89 }, dur: 3000, hold: 2400 },
      { label: "加上線性阻力", caption: "兩者都受 $-km\\vec v$：連接飛鏢與猴子的線段（橘）始終平行瞄準線，只是縮短得越來越慢——仍然打中。", set: { tt: 0, k: 0.3, drop: 0, ghost: 0, link: 1 }, to: { tt: 1.05 }, dur: 3200, hold: 2600 }
    ],
    draw: function (d, s) {
      var v0 = s.v0, k = s.k, L = Math.hypot(HM_D, HM_H);
      var th = Math.atan2(HM_H, HM_D), c = Math.cos(th), sn = Math.sin(th);
      var tHit = hmHitTime(v0, k), tLand = hmLandTime(k);
      var t = Math.max(0, Math.min(s.tt, tHit, tLand));
      // 地面、樹、尺寸
      d.line([-1.2, 0], [23.5, 0], { color: MUTED, width: 2 });
      d.line([HM_D + 0.9, 0], [HM_D + 0.9, HM_H + 1.6], { color: "#8a6a3a", width: 6, opacity: 0.55 });
      d.line([HM_D + 0.9, HM_H + 0.3], [HM_D - 0.4, HM_H + 0.3], { color: "#8a6a3a", width: 3.5, opacity: 0.55 });
      if (s.dims) {
        d.line([0, -0.6], [HM_D, -0.6], { color: MUTED, width: 1, dash: "3 4" });
        d.label([HM_D / 2, -1.05], "D=20\\ \\text{m}", { color: MUTED, size: 12 });
        d.label([HM_D + 2.2, HM_H / 2], "H=10\\ \\text{m}", { color: MUTED, size: 12 });
      }
      d.label([-0.2, 1.3], "\\text{獵人}", { color: INK, size: 12 });
      if (s.aim) d.line([0, 0], [HM_D, HM_H], { color: MUTED, width: 1.4, dash: "6 5" });
      if (s.theta) { d.arc([0, 0], 2.4, 0, th * 180 / Math.PI, { color: MUTED, width: 1.4 }); d.label([3.0, 0.75], "\\theta", { color: MUTED, size: 13 }); }
      // 軌跡
      if (s.trail && t > 0) {
        var pts = [];
        for (var i = 0; i <= 60; i++) pts.push(hmDart(v0, k, t * i / 60));
        d.path(pts, { color: RED, width: 2.2, opacity: 0.8 });
      }
      var P = hmDart(v0, k, t), drop = hmDrop(k, t);
      var M = [HM_D, Math.max(0, HM_H - drop)];
      // 無重力位置（灰）與多掉的距離（紫）
      if (s.ghost || s.drop) {
        var g = hmStraight(v0, k, t), Gd = [g * c, g * sn];
        d.dot(Gd, { r: 5, color: MUTED });
        d.dot([HM_D, HM_H], { r: 5, color: MUTED });
        if (s.drop && drop > 0.15) {
          d.arrow(Gd, P, { color: PURPLE, width: 2.4 });
          d.arrow([HM_D, HM_H], M, { color: PURPLE, width: 2.4 });
          d.label([HM_D - 1.6, HM_H - drop / 2], "\\tfrac12gt^2", { color: PURPLE, size: 12 });
        }
      }
      if (s.link) {
        // 每 0.15 s 留下一條淡色的連線：一整排互相平行（都平行瞄準線），越來越短
        for (var tj = 0.15; tj < t - 0.02; tj += 0.15) {
          var Pj = hmDart(v0, k, tj), Mj = [HM_D, Math.max(0, HM_H - hmDrop(k, tj))];
          d.line(Pj, Mj, { color: "var(--orange, #d9822b)", width: 1.6, opacity: 0.35 });
          d.dot(Mj, { r: 3, color: BLUE });
        }
        d.line(P, M, { color: "var(--orange, #d9822b)", width: 3, opacity: 0.9 });
        d.label([20.3, 13.0], k > 0 ? "\\text{阻力 } -km\\vec v" : "", { color: MUTED, size: 12 });
      }
      d.dot(P, { r: 6, color: RED });
      d.dot(M, { r: 7.5, color: BLUE });
      d.label([HM_D - 1.2, M[1] + 1.0], "\\text{猴子}", { color: BLUE, size: 12 });
      var hit = Math.abs(t - tHit) < 1e-3 && tHit <= tLand;
      if (hit) d.label([HM_D - 3.2, M[1] - 1.1], "\\text{命中！}", { color: RED, size: 15 });
      if (tLand < tHit && s.tt >= tLand) d.label([HM_D - 5.5, 1.2], "\\text{猴子先落地}", { color: BLUE, size: 13 });
      d.label([1.5, 12.6], "t=" + F(t, 2) + "\\ \\text{s}", { color: INK, size: 13 });
    },
    formula: function (s) {
      var t = Math.max(0, Math.min(s.tt, hmHitTime(s.v0, s.k), hmLandTime(s.k)));
      var P = hmDart(s.v0, s.k, t), ym = Math.max(0, HM_H - hmDrop(s.k, t));
      return "t=" + F(t, 2) + "\\ \\text{s}:\\ y_{\\text{鏢}}=" + F(P[1], 2) + "\\ \\text{m},\\ y_{\\text{猴}}=" + F(ym, 2) + "\\ \\text{m}";
    }
  });

  /* ---------------- 自編難題 c2-self-11c：球鑽孔後的「餐巾環」轉動慣量＋離合器（影片也使用） ---------------- */
  // 長度單位：公分。mode 0＝剖面（殼層積分、極限）；mode 1＝兩個同高度的環並排比較；mode 2＝離合器接合的 ω–t 圖。
  var NR_I1 = 9.8e-4, NR_I2 = 4.73e-3, NR_N = 0.010, NR_W0 = 30;
  var NR_T = NR_W0 / (NR_N * (1 / NR_I1 + 1 / NR_I2)), NR_WF = NR_I1 * NR_W0 / (NR_I1 + NR_I2);
  function nrHalf(R, a, k, ox) {  // 右半邊剩下的區域：a ≤ x ≤ R、|z| ≤ √(R²−x²)（k＝公分換成圖上單位）
    var top = [], bot = [], n = 48;
    for (var i = 0; i <= n; i++) {
      var x = a + (R - a) * i / n, z = Math.sqrt(Math.max(0, R * R - x * x));
      top.push([ox + k * x, k * z]); bot.unshift([ox + k * x, -k * z]);
    }
    return top.concat(bot);
  }
  function nrRing(d, R, a, k, ox, o) {
    var P = nrHalf(R, a, k, ox);
    d.poly(P, o);
    d.poly(P.map(function (p) { return [2 * ox - p[0], p[1]]; }), o);
  }
  function nrOmegaAt(t) {  // 離合器：小環 ω1、大環 ω2（t* 之後一起轉）
    var u = Math.min(t, NR_T);
    return [NR_W0 - NR_N * u / NR_I1, NR_N * u / NR_I2];
  }
  A.define("c2-napkin-ring", {
    title: "球鑽孔後的環：轉動慣量與離合器",
    question: "同材料、同高度的兩個環質量一樣，轉動慣量也一樣嗎？",
    view: [560, 360], origin: [230, 185], scale: 30,
    init: { mode: 0, a: 3, core: 1, tri: 1, shell: 0, sh: 0, lim: 0, dims: 1, ival: 0, tt: 0, area: 0 },
    steps: [
      { label: "剖面", caption: "沿直徑鑽掉半徑 $a$ 的圓柱，剩下藍色的環（通過轉軸的剖面）。孔壁長 $h=2b$，紫色直角三角形給出 $a^2+b^2=R^2$。", dur: 300, hold: 2600 },
      { label: "圓柱殼", caption: "取半徑 $r$、厚 $\\mathrm dr$ 的圓柱殼（紅）：高 $2\\sqrt{R^2-r^2}$，$\\mathrm dV=2\\pi r\\,\\mathrm dr\\cdot2\\sqrt{R^2-r^2}$；$r$ 從 $a$ 掃到 $R$。", set: { shell: 1, sh: 0, core: 0, tri: 0 }, to: { sh: 0.7 }, dur: 3200, hold: 1800 },
      { label: "$a\\to0$", caption: "孔越來越細：回到實心球，$I/MR^2\\to2/5$。", set: { shell: 0, lim: 1, tri: 0 }, to: { a: 0 }, dur: 2600, hold: 1800 },
      { label: "$a\\to R$", caption: "孔越來越粗：只剩赤道附近一圈，所有質量都離軸 $R$，$I/MR^2\\to1$。", to: { a: 4.97 }, dur: 3200, hold: 1800 },
      { label: "兩個環", caption: "同材料、同高度 $h=6\\ \\text{cm}$：質量相同，但大環的質量全在離軸約 $10\\ \\text{cm}$ 處，$I_2\\approx4.8I_1$。", set: { mode: 1, a: 3, lim: 0, ival: 1 }, dur: 300, hold: 3200 },
      { label: "離合器", caption: "摩擦力矩固定：小環等減速、大環等加速，$t^*=2.44\\ \\text{s}$ 時一起以 $5.15\\ \\text{rad/s}$ 轉；兩線之間的面積是相對轉角。", set: { mode: 2, tt: 0, area: 1 }, to: { tt: 3.2 }, dur: 4000, hold: 2600 }
    ],
    draw: function (d, s) {
      var mode = Math.round(s.mode);
      if (mode === 2) {
        var X = function (t) { return -6 + 5 * t; }, Y = function (w) { return -4.6 + 0.3 * w; };
        d.arrow([X(0), Y(0)], [X(3.3), Y(0)], { color: INK, width: 1.6 });
        d.arrow([X(0), Y(0)], [X(0), Y(34)], { color: INK, width: 1.6 });
        d.label([X(3.3) + 0.2, Y(0) - 0.55], "t\\ (\\text{s})", { color: INK, size: 12 });
        d.label([X(0) + 0.3, Y(34) + 0.35], "\\omega\\ (\\text{rad/s})", { color: INK, size: 12 });
        [1, 2, 3].forEach(function (t) { d.line([X(t), Y(0)], [X(t), Y(0) - 0.15], { color: INK, width: 1 }); d.label([X(t), Y(0) - 0.6], String(t), { color: MUTED, size: 11 }); });
        [10, 20, 30].forEach(function (w) { d.line([X(0), Y(w)], [X(0) - 0.15, Y(w)], { color: INK, width: 1 }); d.label([X(0) - 0.65, Y(w)], String(w), { color: MUTED, size: 11 }); });
        var tt = Math.max(0, Math.min(s.tt, 3.2)), n = 60, p1 = [], p2 = [];
        for (var i = 0; i <= n; i++) { var t = tt * i / n, w = nrOmegaAt(t); p1.push([X(t), Y(w[0])]); p2.push([X(t), Y(w[1])]); }
        if (s.area && tt > 0) {
          var m = Math.min(tt, NR_T), q1 = [], q2 = [];
          for (var j = 0; j <= n; j++) { var u = m * j / n, ww = nrOmegaAt(u); q1.push([X(u), Y(ww[0])]); q2.unshift([X(u), Y(ww[1])]); }
          d.poly(q1.concat(q2), { color: "none", fill: PURPLE, fillOpacity: 0.18, width: 0 });
          if (tt >= NR_T) {
            d.arrow([X(1.55), Y(19.2)], [X(0.95), Y(13)], { color: PURPLE, width: 1.6 });
            d.label([X(2.2), Y(21)], "\\text{面積}=\\Delta\\phi_{\\text{相對}}=\\tfrac12\\omega_0t^*\\approx36.5\\ \\text{rad}", { color: PURPLE, size: 12 });
          }
        }
        d.path(p1, { color: RED, width: 2.6 }); d.path(p2, { color: BLUE, width: 2.6 });
        var wn = nrOmegaAt(tt);
        d.dot([X(tt), Y(wn[0])], { r: 5, color: RED }); d.dot([X(tt), Y(wn[1])], { r: 5, color: BLUE });
        d.label([X(0) + 1.3, Y(30) + 0.1], "\\text{小環 }\\omega_1", { color: RED, size: 12 });
        d.label([X(0.55), Y(0) + 0.75], "\\text{大環 }\\omega_2", { color: BLUE, size: 12 });
        if (tt >= NR_T) {
          d.line([X(NR_T), Y(0)], [X(NR_T), Y(NR_WF)], { color: MUTED, width: 1, dash: "3 4" });
          d.label([X(NR_T), Y(0) - 0.6], "t^*", { color: INK, size: 12 });
          d.label([X(2.95), Y(NR_WF) + 0.65], "\\omega_f\\approx5.15", { color: INK, size: 12 });
        }
        d.label([X(2.3), Y(32)], "t=" + F(tt, 2) + "\\ \\text{s}", { color: INK, size: 13 });
        return;
      }
      if (mode === 1) {
        var k = 13 / 30, b = 3, c1 = -4.6, c2 = 6.4, a1 = 4, a2 = Math.sqrt(91);
        [[c1, 5], [c2, 10]].forEach(function (c) { d.arc([c[0], 0], c[1] * k, 0, 360, { color: MUTED, width: 1, dash: "3 4" }); d.line([c[0], -c[1] * k - 0.4], [c[0], c[1] * k + 0.4], { color: MUTED, width: 1, dash: "5 5" }); });
        nrRing(d, 5, a1, k, c1, { color: RED, width: 1.4, fill: RED, fillOpacity: 0.25 });
        nrRing(d, 10, a2, k, c2, { color: BLUE, width: 1.4, fill: BLUE, fillOpacity: 0.3 });
        // 兩環中間畫一條共用的高度標示，虛線連到兩環的上下緣：高度相同一眼可見
        [-1, 1].forEach(function (sg) { d.line([c1 + a1 * k, sg * b * k], [c2 - a2 * k, sg * b * k], { color: MUTED, width: 1, dash: "2 4" }); });
        d.line([0.2, -b * k], [0.2, b * k], { color: INK, width: 1.4 });
        d.label([0.75, 0], "h", { color: INK, size: 13 });
        d.label([c1, 2.85], "R_1=5\\ \\text{cm}", { color: RED, size: 12 });
        d.label([c2, 4.85], "R_2=10\\ \\text{cm}", { color: BLUE, size: 12 });
        d.label([2.0, 5.7], "\\text{同材料、同高度 }h=6\\ \\text{cm}\\ \\Rightarrow\\ M_1=M_2", { color: INK, size: 13 });
        if (s.ival) {
          d.label([c1, -3.0], "I_1=9.8\\times10^{-4}", { color: RED, size: 12 });
          d.label([c2, -4.9], "I_2=4.73\\times10^{-3}\\ (\\approx4.8I_1)", { color: BLUE, size: 12 });
        }
        return;
      }
      var R = 5, a = Math.max(0, Math.min(s.a, 4.97)), bb = Math.sqrt(R * R - a * a);
      d.arc([0, 0], R, 0, 360, { color: MUTED, width: 1.2, dash: "4 4" });
      d.line([0, -5.7], [0, 5.5], { color: MUTED, width: 1.2, dash: "6 5" });
      d.label([1.35, 5.65], "z", { color: MUTED, size: 12 });
      var rot = [];
      for (var q = 0; q <= 30; q++) { var th = (200 + 300 * q / 30) * Math.PI / 180; rot.push([0.9 * Math.cos(th), 5.15 + 0.28 * Math.sin(th)]); }
      d.path(rot.slice(0, -1), { color: INK, width: 1.4 });
      d.arrow(rot[rot.length - 3], rot[rot.length - 1], { color: INK, width: 1.4 });
      d.label([-1.35, 5.4], "\\omega", { color: INK, size: 13 });
      if (s.core && a > 0.05) {
        d.rect(-a, -bb, a, bb, { color: MUTED, width: 1, dash: "3 3", fill: MUTED, fillOpacity: 0.07 });
        d.label([-1.6, -1.6], "\\text{鑽掉}", { color: MUTED, size: 12 });
      }
      nrRing(d, R, a, 1, 0, { color: BLUE, width: 1.6, fill: BLUE, fillOpacity: 0.22 });
      if (s.shell) {
        var r = a + (R - a) * Math.max(0, Math.min(1, s.sh)), zt = Math.sqrt(Math.max(0, R * R - r * r)), w = 0.17;
        d.rect(r - w / 2, -zt, r + w / 2, zt, { color: RED, width: 1, fill: RED, fillOpacity: 0.55 });
        d.rect(-r - w / 2, -zt, -r + w / 2, zt, { color: RED, width: 1, fill: RED, fillOpacity: 0.55 });
        d.arrow([0, -0.25], [r, -0.25], { color: RED, width: 1.8 });
        d.label([r / 2, -0.8], "r", { color: RED, size: 13 });
        if (zt > 0.8) d.label([r + 1.35, zt * 0.55], "2\\sqrt{R^2-r^2}", { color: RED, size: 11 });
        d.label([7.6, 4.3], "\\mathrm dV=2\\pi r\\,\\mathrm dr\\cdot2\\sqrt{R^2-r^2}", { color: RED, size: 12 });
      }
      if (s.tri && a > 0.05) {
        d.poly([[0, 0], [a, 0], [a, bb]], { color: PURPLE, width: 2 });
        d.label([a / 2, 0.45], "a", { color: PURPLE, size: 13 });
        d.label([a + 0.4, bb / 2], "b", { color: PURPLE, size: 13 });
        d.label([a / 2 - 0.5, bb / 2 + 0.5], "R", { color: PURPLE, size: 13 });
      }
      if (s.dims) {
        d.line([-R - 0.7, -bb], [-R - 0.7, bb], { color: INK, width: 1.2 });
        d.line([-R - 0.9, bb], [-R - 0.5, bb], { color: INK, width: 1.2 });
        d.line([-R - 0.9, -bb], [-R - 0.5, -bb], { color: INK, width: 1.2 });
        d.line([-a, bb], [-R - 0.5, bb], { color: MUTED, width: 1, dash: "2 4" });
        d.line([-a, -bb], [-R - 0.5, -bb], { color: MUTED, width: 1, dash: "2 4" });
        d.label([-R - 1.6, 0], "h=2b", { color: INK, size: 12 });
      }
      if (s.lim) {
        var ratio = (2 + 3 * (a / R) * (a / R)) / 5;
        d.label([7.4, -3.6], "a/R=" + F(a / R, 2), { color: INK, size: 13 });
        d.label([7.4, -4.6], "\\dfrac{I}{MR^2}=\\dfrac{2+3(a/R)^2}{5}=" + F(ratio, 3), { color: INK, size: 13 });
      }
    },
    formula: function (s) {
      var mode = Math.round(s.mode);
      if (mode === 2) { var w = nrOmegaAt(Math.min(s.tt, 3.2)); return "\\omega_1=" + F(w[0], 2) + ",\\ \\omega_2=" + F(w[1], 2) + "\\ \\text{rad/s}"; }
      if (mode === 1) return "I=M\\big(R^2-\\tfrac35b^2\\big):\\ I_1=9.8\\times10^{-4},\\ I_2=4.73\\times10^{-3}\\ \\text{kg·m}^2";
      var R = 5, a = Math.max(0, Math.min(s.a, 4.97));
      return "I=\\tfrac15M(2R^2+3a^2),\\quad a/R=" + F(a / R, 2) + "\\Rightarrow I/MR^2=" + F((2 + 3 * (a / R) * (a / R)) / 5, 3);
    }
  });
})();
