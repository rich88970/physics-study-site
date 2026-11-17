"""力學 Lecture 2 第 9–15 節：詳解改寫（代號 M2b）新寫進去的中間數值與代數步驟，逐一獨立重算。

用法：python -X utf8 tools/verify_mechanics_ch02_detail_M2b.py（需要 numpy、scipy、sympy）
空氣阻力題一律取 ρ = 1.3 kg/m³、g = 9.8 m/s²（與網站內文相同）。
"""
import math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, minimize_scalar

ok = True
g = 9.8
RHO = 1.3


def check(name, got, want, tol=1e-3, rel=False):
    global ok
    got_a, want_a = np.array(got, dtype=float), np.array(want, dtype=float)
    good = np.allclose(got_a, want_a, rtol=tol if rel else 0, atol=0 if rel else tol)
    ok &= bool(good)
    print(("OK  " if good else "FAIL"), name, np.round(got_a, 5).tolist(), "expected", want)


def zero(name, expr):
    global ok
    z = sp.simplify(expr)
    good = z == 0
    ok &= bool(good)
    print(("OK  " if good else "FAIL"), name, "" if good else z)


def truth(name, cond):
    global ok
    ok &= bool(cond)
    print(("OK  " if cond else "FAIL"), name)


def quad_drag(c, x0, y0, vx0, vy0, events, tmax=100.0):
    """v² 阻力 ẍ = -c v ẋ、ÿ = -g - c v ẏ。"""
    def f(t, s):
        x, y, vx, vy = s
        v = math.hypot(vx, vy)
        return [vx, vy, -c * v * vx, -g - c * v * vy]
    return solve_ivp(f, [0, tmax], [x0, y0, vx0, vy0], events=events, rtol=1e-11, atol=1e-11)


t, k, gg, V, U = sp.symbols("t k g V U", positive=True)

# ======================= 第 9 節 =======================
# ---- Ex 2.7：代數步驟 ----
T = sp.Symbol("T", positive=True)
eps_ = sp.Symbol("epsilon")
# (2.47) 由 (2.45) 展開到 k³：1 - kT/2 + k²T²/6 = 1/(1+kV/g) ⇔ T - kT²/3 = (2V/g)/(1+kV/g)
lhs = (1 - k * T / 2 + k**2 * T**2 / 6) - 1 / (1 + k * V / gg)
rhs = (2 / k) * ((k * T / 2 - k**2 * T**2 / 6) - (k * V / gg) / (1 + k * V / gg))
zero("Ex2.7 (2.47) 的移項：兩種寫法相同", sp.simplify(lhs + rhs * k / 2))
zero("Ex2.7 T 一次項：2V/g(1-kV/g)+k/3·4V²/g² = 2V/g(1-kV/3g)",
     sp.expand(2 * V / gg * (1 - k * V / gg) + k / 3 * 4 * V**2 / gg**2 - 2 * V / gg * (1 - k * V / (3 * gg))))
T1 = 2 * V / gg * (1 - k * V / (3 * gg))
Rp = U / k * (1 - sp.exp(-k * T1))
zero("Ex2.7 射程一次項 R(1-4kV/3g)", sp.series(Rp, k, 0, 2).removeO() - 2 * U * V / gg * (1 - 4 * k * V / (3 * gg)))
yt = -gg * t / k + (k * V + gg) / k**2 * (1 - sp.exp(-k * t))
zero("Ex2.7 y(t) 滿足 ÿ = -kẏ - g", sp.diff(yt, t, 2) + k * sp.diff(yt, t) + gg)
zero("Ex2.7 ẏ(0) = V", sp.diff(yt, t).subs(t, 0) - V)

# ---- 2-12：x_max 的 k→0 極限 ----
v0s = sp.Symbol("v0", positive=True)
xmax = sp.log((gg + k * v0s**2) / gg) / (2 * k)
zero("2-12 k→0 時 x_max → v0²/2g", sp.limit(xmax, k, 0) - v0s**2 / (2 * gg))

# ---- Ex 2.8：初始條件與第一步 ----
c45 = 600 * math.cos(math.radians(45))
check("Ex2.8 初速分量 (m/s)", c45, 424.3, tol=0.05)
check("Ex2.8 無阻力 R (km)、T (s)、ymax (km)", [600**2 / g / 1000, 2 * c45 / g, c45**2 / (2 * g) / 1000], [36.7, 86.6, 9.18], tol=0.05)
vtab = [0, 100, 200, 300, 330, 350, 400, 450, 500, 600, 800, 1000]
Ftab = [0, 15, 40, 95, 135, 210, 300, 385, 460, 620, 930, 1250]   # 依課本 p.60 原圖重讀（審查報告 D）
Fd = lambda s: float(np.interp(s, vtab, Ftab))
check("Ex2.8 讀圖值 F(100,300,400,600) (N)", [Fd(100), Fd(300), Fd(400), Fd(600)], [15, 95, 300, 620], tol=1e-9)
check("Ex2.8 300→400 m/s 阻力倍數", Fd(400) / Fd(300), 3.2, tol=0.05)
a0 = Fd(600) / 30
ax0 = -a0 * math.cos(math.radians(45))
check("Ex2.8 出發時 F/m、ẍ、ÿ (m/s²)", [a0, ax0, ax0 - g], [20.7, -14.6, -24.4], tol=0.05)
check("Ex2.8 F/m 約 2.1 g", a0 / g, 2.1, tol=0.05)
check("Ex2.8 Euler 第一步 ẋ1、ẏ1 (m/s)", [c45 + ax0 * 0.05, c45 + (ax0 - g) * 0.05], [423.5, 423.0], tol=0.05)


def rhs28(tt, y):
    s = math.hypot(y[2], y[3])
    return [y[2], y[3], -Fd(s) / 30 * y[2] / s, -g - Fd(s) / 30 * y[3] / s]


ev330 = lambda tt, y: math.hypot(y[2], y[3]) - 330
ev330.terminal = True
s28 = solve_ivp(rhs28, [0, 100], [0, 0, c45, c45], events=ev330, rtol=1e-8, max_step=0.05)
check("Ex2.8 速率從 600 掉到 330 m/s 的時間約 15 s", s28.t_events[0][0], 15.0, tol=0.5)
ev0 = lambda tt, y: y[1] if tt > 1 else 1
ev0.terminal = True
s28r = solve_ivp(rhs28, [0, 200], [0, 0, c45, c45], events=ev0, rtol=1e-9, max_step=0.05)
check("Ex2.8 讀圖表重算射程 (km)", s28r.y_events[0][0][0] / 1000, 16.5, tol=0.05)
# ---- 審查報告 D：c2-self-15b 的 U''(0) 代入行 ----
kk15, d15, l15 = sp.symbols("k d l_0", positive=True)
zero("s15b k·0 + k(d-l0)/d = k(1-l0/d)", kk15 * 0 + kk15 * (d15 - l15) / d15 - kk15 * (1 - l15 / d15))

# ---- 2-7 ----
c7 = 0.8 * RHO * 0.2 / (2 * 30)
v6 = 160 * 1000 / 3600
check("2-7 c (1/m)", c7, 3.47e-3, tol=0.005e-3)
check("2-7 出發時阻力減速 cv² (m/s²) 與 /g", [c7 * v6**2, c7 * v6**2 / g], [6.85, 0.70], tol=0.01)
e7 = lambda tt, s: s[1]
e7.terminal = True
s7 = quad_drag(c7, 0, 80, v6, 0, e7)
x7 = s7.y_events[0][0][0]
check("2-7 投放距離 209.6、177.5 m，落點差 32.0 m", [v6 * math.sqrt(2 * 80 / g) + 30, x7 + 30, v6 * math.sqrt(2 * 80 / g) - x7], [209.6, 177.5, 32.0], tol=0.06)

# ---- 2-18 ----
A18 = math.pi * 0.05**2
c18 = 0.5 * RHO * A18 / (2 * 0.2)
check("2-18 A (m²)、c (1/m)、v_t (m/s)", [A18, c18, math.sqrt(g / c18)], [7.85e-3, 1.28e-2, 27.7], tol=0.006, rel=True)
check("2-18 25.4 m/s 時的 cv² (m/s²)", c18 * 25.4**2, 8.2, tol=0.05)


def y60(v, th):
    e = lambda tt, s: s[0] - 60
    e.terminal = True
    e2 = lambda tt, s: s[1] + 10
    e2.terminal = True
    r = quad_drag(c18, 0, 0.7, v * math.cos(math.radians(th)), v * math.sin(math.radians(th)), [e, e2])
    return r.y_events[0][0][1] if len(r.t_events[0]) else None


def land18(v, th):
    e = lambda tt, s: s[1]
    e.terminal = True
    e.direction = -1
    r = quad_drag(c18, 0, 0.7, v * math.cos(math.radians(th)), v * math.sin(math.radians(th)), e)
    return r.y_events[0][0][0]


check("2-18 25.4 m/s 落地距離約 41 m", land18(25.4, 35), 41.4, tol=0.1)
check("2-18 34 m/s 在 59.3 m 落地（到不了牆）", land18(34, 35), 59.3, tol=0.05)
check("2-18 36 m/s 時 y60 (m)", y60(36, 35), 3.78, tol=0.01)
v18 = brentq(lambda v: y60(v, 35) - 2, 34.5, 36)
check("2-18 v0 與 /25.4", [v18, v18 / 25.4], [35.2, 1.39], tol=0.005, rel=True)
check("2-18 掃描 y60 (θ=30,35,40,45,50)", [y60(v18, a) for a in (30, 35, 40, 45, 50)], [-0.26, 2.00, 3.08, 2.20, -2.23], tol=0.01)
best = minimize_scalar(lambda a: -y60(v18, a), bounds=(36, 46), method="bounded")
check("2-18 最佳角、y60、高出牆", [best.x, -best.fun, -best.fun - 2], [40.7, 3.10, 1.1], tol=0.05)

# ---- 2-20 ----
A20 = math.pi * 0.05**2
W140 = 0.5 * 0.2 * RHO * A20 * 140**2
c20 = W140 / (10 * 140**2)
check("2-20 Mach、W (N)、mg (N)、c (1/m)", [140 / 330, W140, 10 * g, c20 * 1e4], [0.42, 20.0, 98, 1.02], tol=0.05)
check("2-20 sin2θ", g * 1000 / 140**2, 0.5, tol=1e-12)


def range20(th):
    e = lambda tt, s: s[1] if tt > 0.1 else 1
    e.terminal = True
    r = quad_drag(c20, 0, 0, 140 * math.cos(math.radians(th)), 140 * math.sin(math.radians(th)), e)
    return r.y_events[0][0][0], r.t_events[0][0]


r15, r17 = range20(15)[0], range20(17)[0]
check("2-20 R(15°)、R(17°)、R(75°) (m)", [r15, r17, range20(75)[0]], [936.4, 1039.3, 862], tol=0.6)
check("2-20 割線法第一步 (°)", 17 - (r17 - 1000) * 2 / (r17 - r15), 16.24, tol=0.005)
lo = brentq(lambda a: range20(a)[0] - 1000, 14, 20)
hi = brentq(lambda a: range20(a)[0] - 1000, 65, 76)
check("2-20 低、高仰角與飛行時間", [lo, range20(lo)[1], hi, range20(hi)[1]], [16.2, 7.8, 72.2, 26.0], tol=0.05)

# ---- 2-35：牛頓法 ----
V35 = 600 * math.sin(math.radians(60))
kk = 0.01
a35 = (kk * V35 + g) / (g * kk)
T0 = 2 * V35 / g
f0 = T0 - a35 * (1 - math.exp(-kk * T0))
fp0 = 1 - a35 * kk * math.exp(-kk * T0)
T1n = T0 - f0 / fp0
f1 = T1n - a35 * (1 - math.exp(-kk * T1n))
T2n = T1n - f1 / (1 - a35 * kk * math.exp(-kk * T1n))
check("2-35 U、V (m/s)", [600 * 0.5, V35], [300, 519.6], tol=0.05)
check("2-35 a (s)、T0 (s)、f、f'", [a35, T0, f0, fp0], [153.0, 106.0, 6.01, 0.470], tol=0.002, rel=True)
check("2-35 牛頓法 T1、T2 (s)", [T1n, T2n], [93.25, 92.11], tol=0.01)
Tk = brentq(lambda T_: T_ - a35 * (1 - math.exp(-kk * T_)), 50, 105)
check("2-35 收斂 T、1-e^{-kT}、R' (km)", [Tk, 1 - math.exp(-kk * Tk), 300 / kk * (1 - math.exp(-kk * Tk)) / 1000], [92.10, 0.602, 18.06], tol=0.005)
check("2-35 微擾 4kV/3g、R(1-…) (km)", [4 * kk * V35 / (3 * g), 600**2 * math.sin(math.radians(120)) / g * (1 - 4 * kk * V35 / (3 * g)) / 1000], [0.707, 9.32], tol=0.005)

# ---- 2-55 ----
U55 = 54 * math.cos(math.radians(45))


def R55(kq):
    a = (kq * U55 + g) / (g * kq)
    T_ = brentq(lambda x: x - a * (1 - math.exp(-kq * x)), 1e-3, 2 * U55 / g)
    return U55 / kq * (1 - math.exp(-kq * T_)), T_


check("2-55 R0 (m)、142/R0", [54**2 / g, 142 / (54**2 / g)], [297.6, 0.477], tol=0.05)
check("2-55 k=0.1: T、R；k=0.3: T、R", [*R55(0.1)[::-1], *R55(0.3)[::-1]], [6.99, 192, 6.05, 107], tol=0.6)
check("2-55 二分法中點 k=0.2、0.15 的 R (m)", [R55(0.2)[0], R55(0.15)[0]], [138.3, 161.3], tol=0.05)
k55 = brentq(lambda kq: R55(kq)[0] - 142, 0.05, 0.5)
check("2-55 k、T、kV/g", [k55, R55(k55)[1], k55 * U55 / g], [0.191, 6.49, 0.74], tol=0.005)
check("2-55 微擾 1-142/R0、4V/3g、k", [1 - 142 / (54**2 / g), 4 * U55 / (3 * g), (1 - 142 / (54**2 / g)) / (4 * U55 / (3 * g))], [0.523, 5.195, 0.101], tol=0.001)

# ---- s09a ----
q, w = sp.symbols("q w", positive=True)
ttop = -sp.log(q) / k
Vq = (gg / q - gg) / k   # kV+g = g/q
y2 = (-gg * t / k + (k * Vq + gg) / k**2 * (1 - sp.exp(-k * t))).subs(t, 2 * ttop)
zero("s09a y(2t_top) = g/k² [2 ln q + (1-q²)/q]", sp.simplify(y2 - gg / k**2 * (2 * sp.log(q) + (1 - q**2) / q)))
fw = w - 1 / w - 2 * sp.log(w)
zero("s09a f'(w) = (1-1/w)²", sp.diff(fw, w) - (1 - 1 / w)**2)
e9 = 0.005 * V35 / g
check("s09a kV/g、t_top、一次近似 t_top、T/2", [e9, math.log(1 + e9) / 0.005, V35 / g * (1 - e9 / 2), V35 / g * (1 - e9 / 3)], [0.2651, 47.0, 46.0, 48.3], tol=0.05)

# ---- s09b ----
eps9 = 0.01 * 50 / g
d9 = -eps9 / (3 * math.sqrt(2))
check("s09b ε、3√2、δ (rad)、δ (°)、θ*", [eps9, 3 * math.sqrt(2), d9, math.degrees(d9), 45 + math.degrees(d9)], [0.0510, 4.243, -0.0120, -0.69, 44.31], tol=0.005)
th = sp.Symbol("theta")
dR = sp.diff(sp.sin(2 * th) - sp.Rational(4, 3) * eps_ * sp.sin(2 * th) * sp.sin(th), th)
dl = sp.Symbol("delta")
lin = sp.series(sp.series(dR.subs(th, sp.pi / 4 + dl), dl, 0, 2).removeO(), eps_, 0, 2).removeO()
lin = sp.expand(lin).subs(eps_ * dl, 0)
zero("s09b 一次展開 -4δ - 4ε/(3√2)", sp.simplify(lin - (-4 * dl - 4 * eps_ / (3 * sp.sqrt(2)))))

# ======================= 第 10 節 =======================
m1, m2 = sp.symbols("m1 m2", positive=True)
Fspring = 4 * m1 * m2 * gg / (m1 + m2)
zero("s10a (m1+m2)g - F = (m1-m2)²g/(m1+m2)", (m1 + m2) * gg - Fspring - (m1 - m2)**2 * gg / (m1 + m2))
acc = (m1 - m2) * gg / (m1 + m2)
acm = (m1 * acc - m2 * acc) / (m1 + m2)
zero("s10a (m1+m2) a_cm = 總重 - F", (m1 + m2) * acm - ((m1 + m2) * gg - Fspring))
check("s10a F、總重 (N)、a_cm (m/s²)", [4 * 3 * 1 * g / 4, 4 * g, (2 / 4)**2 * g], [29.4, 39.2, 2.45], tol=0.005)
Ae, Be, Om = sp.symbols("A_e B_e Omega", positive=True)
xa = Ae * sp.cos(Om * t) + Be * sp.sin(Om * t)
za = -Be * sp.cos(Om * t) + Ae * sp.sin(Om * t)
zero("2-31 (x-x0)²+(z-z0)² = A²+B²", xa**2 + za**2 - Ae**2 - Be**2)
zero("2-31 ẍ = -α ż", sp.diff(xa, t, 2) + Om * sp.diff(za, t))
# s10b
E_, B_, w_ = sp.symbols("E B omega", positive=True)
xb = E_ / B_ * (t - sp.sin(w_ * t) / w_)
yb = E_ / (B_ * w_) * (1 - sp.cos(w_ * t))
zero("s10b ẍ = ω ẏ", sp.diff(xb, t, 2) - w_ * sp.diff(yb, t))
zero("s10b ÿ = ω(E/B - ẋ)", sp.diff(yb, t, 2) - w_ * (E_ / B_ - sp.diff(xb, t)))
zero("s10b 靜止於原點", sp.Abs(xb.subs(t, 0)) + sp.Abs(yb.subs(t, 0)) + sp.Abs(sp.diff(xb, t).subs(t, 0)) + sp.Abs(sp.diff(yb, t).subs(t, 0)))
v2b = sp.diff(xb, t)**2 + sp.diff(yb, t)**2
zero("s10b v² = (E/B)²(2-2cos ωt)", v2b - (E_ / B_)**2 * (2 - 2 * sp.cos(w_ * t)))
qs = sp.Symbol("q", positive=True)
zero("s10b ½mv² = qEy（m = qB/ω）", sp.Rational(1, 2) * (qs * B_ / w_) * v2b - qs * E_ * yb)
wp = 1.602e-19 * 0.01 / 1.673e-27
check("s10b ω (1/s)、E/B、y_max (m)、v_max、v/c", [wp / 1e5, 1000 / 0.01 / 1e5, 2 * 1e5 / wp, 2e5 / 1e5, 2e5 / 2.998e8 * 1e4], [9.58, 1, 0.209, 2, 6.7], tol=0.05)

# ======================= 第 11 節 =======================
Mb, mb, vv = sp.symbols("M m v", positive=True)
v3, v4 = sp.symbols("v3 v4")
sol = sp.solve([Mb * vv - mb * vv - (Mb * v3 + mb * v4), v4 - v3 - 2 * vv], [v3, v4])
zero("2-28 (M+m)v3 = (M-3m)v", (Mb + mb) * sol[v3] - (Mb - 3 * mb) * vv)
v1s, v2s, v3s, v4s = sp.symbols("v1 v2 v3 v4")
zero("2-28 動能式÷動量式 = v1+v3 - (v2+v4)（平方差）",
     sp.factor(Mb * (v1s**2 - v3s**2)) / (Mb * (v1s - v3s)) - (v1s + v3s))
# s11a
r0, r_ = sp.symbols("r_0 r", positive=True)
mq = sp.Symbol("m", positive=True)
Fr = mq * v0s**2 * r0**2 / sp.Symbol("rp", positive=True)**3
Wq = sp.integrate(Fr, (sp.Symbol("rp", positive=True), r_, r0))
zero("s11a W = ½mv0²(r0²/r² - 1)", Wq - mq * v0s**2 / 2 * (r0**2 / r_**2 - 1))
check("s11a v、W、T0、T、F(0.5)、F(0.25)", [0.5 / 0.25 * 1.0, 0.5 * 0.2 * 1 * 3, 0.5 * 0.2 * 1, 0.5 * 0.2 * 4,
                                          0.2 * 1 * 0.25 / 0.5**3, 0.2 * 1 * 0.25 / 0.25**3], [2.0, 0.30, 0.10, 0.40, 0.40, 3.2], tol=1e-9)
# s11b
mm_, MM_, vm, vM = sp.symbols("m_l M_h v_m v_M")
vml = ((mm_ - MM_) * vm + 2 * MM_ * vM) / (mm_ + MM_)
vMl = ((MM_ - mm_) * vM + 2 * mm_ * vm) / (mm_ + MM_)
zero("s11b 輕撞重極限 v_m' → 2v_M - v_m", sp.limit(vml, mm_, 0) - (2 * vM - vm))
zero("s11b 重球速度不變", sp.limit(vMl, mm_, 0) - vM)
u_ = [0]
for kk_ in range(1, 6):
    u_.append(2 * u_[-1] + 1)
truth("s11b u_k = 2^k - 1（k=1…5）", all(u_[kk_] == 2**kk_ - 1 for kk_ in range(6)))

# ======================= 第 12 節 =======================
check("2-26 T1 (J)、√(2/6)、x (m)", [0.5 * 2 * 16, math.sqrt(2 / 6), 4 * math.sqrt(2 / 6)], [16, 0.577, 2.31], tol=0.005)
check("2-26 W_摩擦 (J)、8.16、√2.72", [-0.2 * 2 * g * 2, 16 - 7.84, math.sqrt(2 * 8.16 / 6)], [-7.84, 8.16, 1.65], tol=0.005)
check("2-27 μ、μgz0² (J)、W", [0.4 / 4, 0.1 * g * 0.36, 0.1 * g * 0.36 / 2], [0.1, 0.3528, 0.18], tol=0.005)
Ls, a_, lam = sp.symbols("L a lambda", positive=True)
zero("s12a ∫_a^L λgx dx = λg(L²-a²)/2", sp.integrate(lam * gg * sp.Symbol("x"), (sp.Symbol("x"), a_, Ls)) - lam * gg / 2 * (Ls**2 - a_**2))
kap = sp.sqrt(gg / Ls)
xch = a_ / 2 * (sp.exp(kap * t) + sp.exp(-kap * t))
zero("s12a x(t) = a cosh(κt) 滿足 ẍ = (g/L)x", sp.diff(xch, t, 2) - gg / Ls * xch)
check("s12a L²-a²、v²、v、√(L/g)、acosh4、ln(4+√15)", [4 - 0.25, g * 3.75 / 2, math.sqrt(g * 3.75 / 2), math.sqrt(2 / g), math.acosh(4), math.log(4 + math.sqrt(15))],
      [3.75, 18.4, 4.29, 0.452, 2.063, 2.063], tol=0.03)
check("s12a t_end、κ、√15、ẋ(t_end)", [math.sqrt(2 / g) * math.acosh(4), math.sqrt(g / 2), math.sqrt(15), 0.5 * math.sqrt(g / 2) * math.sqrt(15)], [0.932, 2.214, 3.873, 4.29], tol=0.005)
check("s12b μg、d_箱、d_帶、W_馬達、ΔT、Q", [0.5 * g, 4 / (2 * 0.5 * g), 4 / (0.5 * g), 10 * 4, 0.5 * 10 * 4, 0.5 * 10 * g * (4 / (0.5 * g) - 4 / (2 * 0.5 * g))],
      [4.9, 0.408, 0.816, 40, 20, 20], tol=0.001)

# ======================= 第 13 節 =======================
X, Y = sp.symbols("X Y", real=True)
kq = sp.Symbol("k", positive=True)
Fx13 = -kq * Y / (X**2 + Y**2)
Fy13 = kq * X / (X**2 + Y**2)
zero("s13a ∂Fy/∂x = k(y²-x²)/(x²+y²)²", sp.diff(Fy13, X) - kq * (Y**2 - X**2) / (X**2 + Y**2)**2)
zero("s13a ∂Fx/∂y = k(y²-x²)/(x²+y²)²", sp.diff(Fx13, Y) - kq * (Y**2 - X**2) / (X**2 + Y**2)**2)
thv = sp.atan2(Y, X)
zero("s13a F = k∇θ（x 分量）", sp.diff(kq * thv, X) - Fx13)
zero("s13a F = k∇θ（y 分量）", sp.diff(kq * thv, Y) - Fy13)
ph = sp.Symbol("phi")
zero("s13a 單位圓 ∮ = 2πk", sp.integrate((Fx13 * sp.diff(sp.cos(ph), ph) + Fy13 * sp.diff(sp.sin(ph), ph)).subs({X: sp.cos(ph), Y: sp.sin(ph)}), (ph, 0, 2 * sp.pi)) - 2 * sp.pi * kq)
circ = lambda p: ((-math.sin(p)) / ((3 + math.cos(p))**2 + math.sin(p)**2) * (-math.sin(p)) + (3 + math.cos(p)) / ((3 + math.cos(p))**2 + math.sin(p)**2) * math.cos(p))
check("s13a 圓心 (3,0) 的 ∮/k", quad(circ, 0, 2 * math.pi)[0], 0, tol=1e-10)
# s13b
xf = sp.Function("x")(t)
vq, mq2 = sp.symbols("v m", positive=True)
U13 = kq * (xf - vq * t)**2 / 2
E13 = mq2 * sp.diff(xf, t)**2 / 2 + U13
dE = sp.diff(E13, t).subs(sp.diff(xf, t, 2), -kq * (xf - vq * t) / mq2)
dUdt = sp.diff(kq * (sp.Symbol("xx") - vq * t)**2 / 2, t).subs(sp.Symbol("xx"), xf)
zero("s13b dE/dt = ∂U/∂t（用運動方程式）", dE - dUdt)
zero("s13b ∂U/∂t = 手的功率 k(vt-x)v", dUdt - kq * (vq * t - xf) * vq)
xp = sp.Symbol("xp")
xpd = sp.Symbol("xpd")
zero("s13b E = E' + mvẋ' + ½mv²", (mq2 * (xpd + vq)**2 / 2 + kq * xp**2 / 2) - (mq2 * xpd**2 / 2 + kq * xp**2 / 2 + mq2 * vq * xpd + mq2 * vq**2 / 2))

# ======================= 第 14 節 =======================
mm, hh, RR = 1.62, 3.91, sp.Symbol("R", positive=True)
check("2-25 mg (N)、2h、2gh、(2-√2)g、3/√2-2", [mm * g, 2 * hh, 2 * g * hh, (2 - math.sqrt(2)) * g, 3 / math.sqrt(2) - 2], [15.9, 7.82, 76.6, 5.74, 0.121], tol=0.05)
mS, hS = sp.symbols("m h", positive=True)
vB2 = 2 * gg * hS - 2 * gg * RR + sp.sqrt(2) * gg * RR
zero("2-25 N_B = mg/√2 + m vB²/R = mg[2h/R + 3/√2 - 2]", mS * gg / sp.sqrt(2) + mS * vB2 / RR - mS * gg * (2 * hS / RR + 3 / sp.sqrt(2) - 2))
hp_ = RR * (1 - 1 / sp.sqrt(2))
vB = sp.sqrt(vB2)
tl = (vB / sp.sqrt(2) + sp.sqrt(vB2 / 2 + 2 * gg * hp_)) / gg
d_expr = RR / sp.sqrt(2) + (hS - hp_) + sp.sqrt(hS**2 - hp_**2)
num25 = {gg: 9.8, hS: 3.91, RR: 1.0}
check("2-25 d 公式 = R/√2 + vB t/√2（R=1）", float((RR / sp.sqrt(2) + vB / sp.sqrt(2) * tl).subs(num25)), float(d_expr.subs(num25)), tol=1e-9)
hp1 = 1 - 1 / math.sqrt(2)
check("2-25 R=1：h'、R/√2、h-h'、√(h²-h'²)、d", [hp1, 1 / math.sqrt(2), 3.91 - hp1, math.sqrt(3.91**2 - hp1**2), 1 / math.sqrt(2) + 3.91 - hp1 + math.sqrt(3.91**2 - hp1**2)],
      [0.293, 0.707, 3.617, 3.899, 8.22], tol=0.005)
cth = sp.Symbol("c")
Nq = mS * gg * cth - (mS * v0s**2 / RR + 2 * mS * gg * (1 - cth))
zero("s14a N = mg(3cosθ-2) - mv0²/R", Nq - (mS * gg * (3 * cth - 2) - mS * v0s**2 / RR))
check("s14a cos⁻¹(2/3) (°)", math.degrees(math.acos(2 / 3)), 48.2, tol=0.05)
zero("s14a N=0 ⇒ cosθ = 2/3 + v0²/3gR", sp.solve(Nq, cth)[0] - (sp.Rational(2, 3) + v0s**2 / (3 * gg * RR)))
vt2, vb2 = sp.symbols("vt2 vb2", positive=True)
zero("s14b N底 - N頂 = 6mg", (mS * gg + mS * (vt2 + 4 * gg * RR) / RR) - (mS * vt2 / RR - mS * gg) - 6 * mS * gg)
zero("s14b h_min：2g(h-2R) = gR ⇒ h = 5R/2", sp.solve(2 * gg * (hS - 2 * RR) - gg * RR, hS)[0] - sp.Rational(5, 2) * RR)

# ======================= 第 15 節 =======================
U0, aS, xS = sp.symbols("U_0 a x", positive=True)
U47 = U0 * (aS / xS + xS / aS)
check("2-47 U''(2) (J/m²)", float(sp.diff(U47, xS, 2).subs({U0: 1, aS: 2, xS: 2})), 0.5, tol=1e-12)
check("2-47 U(0.5,1,2,4,8) (J)", [float(U47.subs({U0: 1, aS: 2, xS: v})) for v in (0.5, 1, 2, 4, 8)], [4.25, 2.5, 2, 2.5, 4.25], tol=1e-12)
zero("2-47 U(x) = U(a²/x)", U47 - U47.subs(xS, aS**2 / xS))
bq, dq = sp.symbols("b d", positive=True)
S0 = 4 * m1**2 * dq**2 / (4 * m1**2 - m2**2) - dq**2
zero("Ex2.12 S0 = m2²d²/(4m1²-m2²)", S0 - m2**2 * dq**2 / (4 * m1**2 - m2**2))
zero("Ex2.12 (b-x0)²/(4S0) = 4m1²/m2²", (16 * m1**2 * dq**2 / (4 * m1**2 - m2**2)) / (4 * S0) - 4 * m1**2 / m2**2)
x1s = sp.Symbol("x_1")
Sx = (bq - x1s)**2 / 4 - dq**2
zero("Ex2.12 U'' 的一般式", sp.diff(-m2 * gg * sp.sqrt(Sx), x1s, 2) - m2 * gg / 4 * (-1 / sp.sqrt(Sx) + (bq - x1s)**2 / (4 * Sx**sp.Rational(3, 2))))
yq = sp.Symbol("y", real=True)
zero("Ex2.13 無因次化", (-gg * dq**2 * ((yq * dq)**2 + dq**2) / ((yq * dq)**4 + 8 * dq**4)) / gg - (-(yq**2 + 1) / (yq**4 + 8)))
zero("Ex2.13 分子展開 2y(y⁴+2y²-8) = 2y(y²+4)(y²-2)", sp.expand(-2 * yq * (yq**4 + 8) + 4 * yq**3 * (yq**2 + 1)) - sp.expand(2 * yq * (yq**2 + 4) * (yq**2 - 2)))
zero("Ex2.13 轉折點方程 y⁴-8y² = 0 ⇒ y=0, ±2√2", sp.Abs(sp.Rational(1, 8) - (8 + 1) / sp.Integer(64 + 8)))
alq = sp.Symbol("alpha", positive=True)
U43 = kq * xS**2 / 2 - kq * xS**4 / (4 * alq**2)
zero("2-43 U''(α) = -2k", sp.diff(U43, xS, 2).subs(xS, alq) + 2 * kq)
zero("2-52 E=U0：U0 - U = U0(1-u²)²", (U0 - U0 * (2 * yq**2 - yq**4)) - U0 * (1 - yq**2)**2)
lamq = sp.Symbol("lambda", positive=True)
zero("2-52 d/dt tanh⁻¹ 驗算：u = tanh(λt) 滿足 u̇ = λ(1-u²)", sp.diff(sp.tanh(lamq * t), t) - lamq * (1 - sp.tanh(lamq * t)**2))
Rc, bc, thc = sp.symbols("R b theta", positive=True)
hc = (Rc + bc / 2) * sp.cos(thc) + Rc * thc * sp.sin(thc)
zero("2-42 h' = Rθcosθ - (b/2)sinθ", sp.diff(hc, thc) - (Rc * thc * sp.cos(thc) - bc / 2 * sp.sin(thc)))
zero("2-42 h'' = (R-b/2)cosθ - Rθ sinθ", sp.diff(hc, thc, 2) - ((Rc - bc / 2) * sp.cos(thc) - Rc * thc * sp.sin(thc)))
zero("2-42 R=b/2 時 h ≈ b - bθ⁴/24", sp.series(hc.subs(Rc, bc / 2), thc, 0, 5).removeO() - (bc - bc * thc**4 / 24))
# 2-44 線性化
x2q, dd = sp.symbols("x_2 d", positive=True)
Lq = sp.sqrt(x2q**2 + dd**2)
zero("2-44 d(cosφ)/dx2 = d²/L³", sp.diff(x2q / Lq, x2q) - dd**2 / Lq**3)
cphi, Leq = 0.6, 1.25
Meff = 1.2 + 4 * 1 * cphi**2
Keff = 2 * 1 * g * 1**2 / Leq**3
check("2-44 數值例的線性化週期 (s)", 2 * math.pi / math.sqrt(Keff / Meff), 3.223, tol=0.001)
# 2-46：F 的係數
nq = sp.Symbol("n", integer=True, positive=True)
zero("2-46 (n+1)/(n+1)! = 1/n!", sp.simplify((nq + 1) / sp.factorial(nq + 1) - 1 / sp.factorial(nq)))
# s15a
eS, sS, rS = sp.symbols("epsilon sigma r", positive=True)
ULJ = 4 * eS * ((sS / rS)**12 - (sS / rS)**6)
r0s = 2**sp.Rational(1, 6) * sS
zero("s15a U'(r0) = 0", sp.diff(ULJ, rS).subs(rS, r0s))
zero("s15a U''(r0) = 72ε/r0²", sp.simplify(sp.diff(ULJ, rS, 2).subs(rS, r0s) - 72 * eS / r0s**2))
k15 = 72 / 2**(1 / 3) * 1.65e-21 / (3.4e-10)**2
m15 = 39.95 * 1.6605e-27
check("s15a 2^(1/6)、2^(1/3)、72/2^(1/3)", [2**(1 / 6), 2**(1 / 3), 72 / 2**(1 / 3)], [1.122, 1.260, 57.1], tol=0.05)
check("s15a r0 (1e-10 m)、k (N/m)、m (1e-26 kg)", [2**(1 / 6) * 3.4, k15, m15 * 1e26], [3.82, 0.816, 6.63], tol=0.005)
check("s15a ω (1e12/s)、f (1e11 Hz)", [math.sqrt(k15 / m15) / 1e12, math.sqrt(k15 / m15) / (2 * math.pi) / 1e11], [3.5, 5.6], tol=0.05)
# s15b
l0, kk2 = sp.symbols("l_0 k", positive=True)
xs_ = sp.Symbol("x", real=True)
U15 = kk2 * (sp.sqrt(xs_**2 + dd**2) - l0)**2 / 2
zero("s15b U''(0) = k(1 - l0/d)", sp.diff(U15, xs_, 2).subs(xs_, 0) - kk2 * (1 - l0 / dd))
zero("s15b U''(√(l0²-d²)) = k(l0²-d²)/l0²", sp.simplify(sp.diff(U15, xs_, 2).subs(xs_, sp.sqrt(l0**2 - dd**2)) - kk2 * (l0**2 - dd**2) / l0**2))
zero("s15b d=l0：U⁽⁴⁾(0) = 3k/d²", sp.diff(U15.subs(l0, dd), xs_, 4).subs(xs_, 0) - 3 * kk2 / dd**2)
zero("s15b d²s/dx² = d²/s³", sp.simplify(sp.diff(sp.sqrt(xs_**2 + dd**2), xs_, 2) - dd**2 / (xs_**2 + dd**2)**sp.Rational(3, 2)))

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
