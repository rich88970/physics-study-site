"""力學 Lecture 2（Thornton & Marion 第 2 章）：獨立重算網站中出現的數值答案，並用 sympy 檢查符號解。

用法：python -X utf8 tools/verify_mechanics_ch02.py（需要 numpy、scipy、sympy）
"""
import math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ok = True
g = 9.8


def check(name, got, want, tol=1e-3, rel=False):
    global ok
    got_a, want_a = np.array(got, dtype=float), np.array(want, dtype=float)
    good = np.allclose(got_a, want_a, rtol=tol if rel else 0, atol=0 if rel else tol)
    ok &= bool(good)
    print(("OK  " if good else "FAIL"), name, np.round(got_a, 5).tolist(), "expected", want)


def zero(name, expr):
    """sympy 化簡後應該是 0"""
    global ok
    z = sp.simplify(expr)
    good = z == 0
    ok &= bool(good)
    print(("OK  " if good else "FAIL"), name, "" if good else z)


t, x, k, m, v0, h, th, a_, b_, c_, al, be, n = sp.symbols("t x k m v0 h theta a b c alpha beta n", positive=True)

# ---------- 第 2 節：地球是不是慣性座標系（講義 p.19–21） ----------
v_rev = 2 * math.pi * 1.496e11 / 3.156e7
check("p19 公轉速率 v", v_rev, 29780, tol=20)
check("p19 公轉加速度", v_rev**2 / 1.496e11, 5.93e-3, tol=0.02e-3)
check("p19 汽車 0→100 km/h 5 s", (100 / 3.6) / 5, 5.56, tol=0.01)
v_rot = 2 * math.pi * 6378137 / 86400
check("p20 自轉速率 v（一天 86400 s）", v_rot, 464, tol=0.5)
check("p20 自轉加速度（86400 s）", v_rot**2 / 6378137, 3.37e-2, tol=0.01e-2)
v_sid = 2 * math.pi * 6378137 / 86164
check("p20 用恆星日 86164 s：v≈465", v_sid, 465, tol=0.5)
check("p20 用恆星日：a≈3.39e-2", v_sid**2 / 6378137, 3.39e-2, tol=0.01e-2)
check("p20 自轉/公轉 ≈ 6", (v_rot**2 / 6378137) / (v_rev**2 / 1.496e11), 5.7, tol=0.05)
check("p21 赤道讀數少的比例 v^2/(Rg)", (v_rot**2 / 6378137) / g, 0.00346, tol=0.00002)

# ---------- 第 3 節：雙星（2-49） ----------
G, m1, m2, d = sp.symbols("G m1 m2 d", positive=True)
w2 = G * (m1 + m2) / d**3
r1 = m2 * d / (m1 + m2)
zero("2-49 m1 的向心力 = 萬有引力", m1 * w2 * r1 - G * m1 * m2 / d**2)

# ---------- 第 4 節：2-1 (c) 用 v dv/dx 也能積 ----------
# 舉例 f(x)=-x, g(xdot)=xdot^2+1：m v dv/dx = -x (v^2+1) → (m/2) ln(v^2+1) = -x^2/2 + C
vv = sp.Function("v")(x)
sol = sp.dsolve(sp.Eq(m * vv * vv.diff(x), -x * (vv**2 + 1)))
print("     2-1(c) 例子 dsolve:", sol)

# ---------- 第 5 節：斜面 ----------
check("Ex2.1 a=g sin30", g * math.sin(math.radians(30)), 4.9)
check("Ex2.2 θc=atan 0.4", math.degrees(math.atan(0.4)), 21.8, tol=0.05)
check("Ex2.3 a/g", math.sin(math.radians(30)) - 0.3 * math.cos(math.radians(30)), 0.240, tol=0.001)
check("Ex2.3 a", g * (math.sin(math.radians(30)) - 0.3 * math.cos(math.radians(30))), 2.35, tol=0.01)
check("Ex2.3 減速角 atan 0.3", math.degrees(math.atan(0.3)), 16.7, tol=0.05)
check("2-16 t=2v0/(g sinα)", 2 * 2.4 / (g * math.sin(math.radians(26))), 1.12, tol=0.005)
for mu in (0.0, 0.1, 0.3):  # 2-32：2 sinθ + 2μ cosθ = 1
    s = (1 - mu * math.sqrt(3 + 4 * mu**2)) / (2 * (1 + mu**2))
    th0 = math.asin(s)
    check(f"2-32 μ={mu} 代回 2sinθ+2μcosθ", 2 * math.sin(th0) + 2 * mu * math.cos(th0), 1)
check("2-32 μ=0.1 角度", math.degrees(math.asin((1 - 0.1 * math.sqrt(3.04)) / (2 * 1.01))), 24.1, tol=0.05)
th24 = math.radians(17)
mu24 = 100 * math.sin(th24) / (100 * math.cos(th24) + 70)
check("2-24 μk", mu24, 0.177, tol=0.001)
check("2-24 坡底速率", math.sqrt(2 * mu24 * g * 70), 15.6, tol=0.05)
th29 = math.atan(0.08)
dec = g * (0.45 * math.cos(th29) - math.sin(th29))
v25 = 25 * 0.44704
check("2-29 θ", math.degrees(th29), 4.57, tol=0.01)
check("2-29 25 mph 的煞車距離", v25**2 / (2 * dec), 17.3, tol=0.1)
check("2-29 滑 30 m 的最小初速 (mph)", math.sqrt(2 * dec * 30) / 0.44704, 32.9, tol=0.1)

# ---------- 第 6 節：阻力 ----------
v = sp.Function("v")
zero("Ex2.4 v=v0 e^{-kt} 滿足 dv/dt=-kv", sp.diff(v0 * sp.exp(-k * t), t) + k * v0 * sp.exp(-k * t))
xs = v0 / k * (1 - sp.exp(-k * t))
zero("Ex2.4 x(t) 的導數", sp.diff(xs, t) - v0 * sp.exp(-k * t))
zero("Ex2.4 v = v0 - kx", (v0 * sp.exp(-k * t)) - (v0 - k * xs))
gg = sp.Symbol("g", positive=True)
V0 = sp.Symbol("V0", real=True)
vz = -gg / k + (k * V0 + gg) / k * sp.exp(-k * t)
zero("Ex2.5 dv/dt = -g - kv", sp.diff(vz, t) + gg + k * vz)
zs = h - gg * t / k + (k * V0 + gg) / k**2 * (1 - sp.exp(-k * t))
zero("Ex2.5 z' = v", sp.diff(zs, t) - vz)
v1s = sp.Symbol("v1", positive=True)
s211 = sp.log((gg - k * v0**2) / (gg - k * v1s**2)) / (2 * k)
# 2-11：dz = v dv /(g - k v^2)，從 v0 積到 v1
zero("2-11 ds/dv1 = v1/(g - k v1²)", sp.diff(s211, v1s) - v1s / (gg - k * v1s**2))
zero("2-11 s(v1=v0)=0", s211.subs(v1s, v0))
# 2-9
check("2-9 例：v0=50, k=0.1 的 tm（有阻力）", math.log(1 + 0.1 * 50 / g) / 0.1, 4.12, tol=0.01)
check("2-9 例：無阻力 tm", 50 / g, 5.10, tol=0.01)
# 2-34
al_, be_, yv = sp.symbols("alpha_ beta_ y", positive=True)
vv = sp.Symbol("vv", positive=True)
ya = -m * vv / al_ - m**2 * gg / al_**2 * sp.log(1 - al_ * vv / (m * gg))
zero("2-34(a) dy/dv = m v/(mg - αv)", sp.diff(ya, vv) - m * vv / (m * gg - al_ * vv))
v2b = m * gg / be_ * (1 - sp.exp(-2 * be_ * yv / m))
zero("2-34(b) m/2 d(v^2)/dy = mg - βv^2", m / 2 * sp.diff(v2b, yv) - (m * gg - be_ * v2b))
# 2-15
dd = sp.Symbol("d", positive=True)
xt = sp.log(sp.cosh(sp.sqrt(k * gg * sp.sin(th)) * t)) / k
vt_ = sp.diff(xt, t)
zero("2-15 x(t) 滿足 v' = g sinθ - k v^2", sp.diff(vt_, t) - (gg * sp.sin(th) - k * vt_**2))
check("2-15 例：k=0.1,d=10,θ=30° t", math.acosh(math.exp(0.1 * 10)) / math.sqrt(0.1 * g * 0.5), 2.37, tol=0.01)
# 2-13：數值檢查 x(∞) < π/(2ka)
for vv0 in (1.0, 10.0, 1000.0):
    kk, aa = 1.0, 1.0
    s13 = solve_ivp(lambda tt, y: [y[1], -kk * (y[1]**3 + aa**2 * y[1])], [0, 200], [0, vv0], rtol=1e-10, atol=1e-12)
    xinf = s13.y[0, -1]
    exact = (math.asin(1) - math.asin((aa**2 - vv0**2) / (aa**2 + vv0**2))) / (2 * aa * kk) if False else None
    xform = (math.pi / 2 + math.asin((vv0**2 - aa**2) / (vv0**2 + aa**2))) / (2 * aa * kk)
    check(f"2-13 v0={vv0} 走的距離（公式 vs 數值）", xinf, xform, tol=1e-4)
    print("     ", "< π/(2ka) =", math.pi / 2, xinf < math.pi / 2)
# 2-51
mm, bb, vb0 = 200.0, 0.2, 2.0
t51 = 999 * mm / (bb * vb0)
check("2-51 t（s）", t51, 4.995e5, tol=10)
check("2-51 t（天）", t51 / 86400, 5.78, tol=0.01)
check("2-51 x（m）", mm / bb * math.log(1 + bb * vb0 * t51 / mm), 6908, tol=1)
# 2-54
check("2-54 終端速度 g/k", g / 0.01, 980)
ym = 120 / 0.01 - g / 0.01**2 * math.log(1 + 0.01 * 120 / g)
check("2-54 最大高度（有阻力）", ym, 680, tol=1)
check("2-54 最大高度（無阻力）", 120**2 / (2 * g), 734.7, tol=0.1)
s54 = solve_ivp(lambda tt, y: [y[1], -g - 0.01 * y[1]], [0, 20], [0, 120], events=lambda tt, y: y[1], rtol=1e-10)
check("2-54 數值積分的最大高度", s54.y_events[0][0][0], ym, tol=0.01)

# ---------- 第 7 節：由 v 求力 ----------
F239 = sp.Symbol("Fv")
vs = -1 / be * sp.log(al * be / m * t + sp.exp(-be * v0))
zero("2-39 v(t) 滿足 m dv/dt = -α e^{βv}", m * sp.diff(vs, t) + al * sp.exp(be * vs))
tend = m / (al * be) * (1 - sp.exp(-be * v0))
zero("2-39 t_end 使 v=0", vs.subs(t, tend))
dstop = sp.integrate(vs, (t, 0, tend))
zero("2-39 停止距離", dstop - m / (al * be**2) * (1 - (1 + be * v0) * sp.exp(-be * v0)))
check("2-39 例：m=1,α=1,β=1,v0=1 d", float((1 - 2 * math.exp(-1))), 0.2642, tol=1e-4)
zero("2-37 F = m v dv/dx（v=α/x）", m * (al / x) * sp.diff(al / x, x) + m * al**2 / x**3)
xt238 = ((n + 1) * al * t) ** (1 / (n + 1))
zero("2-38 x(t) 滿足 dx/dt = α x^{-n}", sp.diff(xt238, t) - al * xt238 ** (-n))
F238 = -m * n * al**2 * x ** (-2 * n - 1)
zero("2-38 F(x) = m v dv/dx", m * al * x**(-n) * sp.diff(al * x**(-n), x) - F238)
zero("2-38 F(t)", sp.simplify(m * sp.diff(xt238, t, 2) - (-m * n * al**2 * ((n + 1) * al * t) ** (-(2 * n + 1) / (n + 1)))))
# 2-50
cc = 2.998e8
for frac_, want in ((0.5, 1.73e7), (0.99, 2.10e8)):
    u = frac_ / math.sqrt(1 - frac_**2)   # Ft/(m0 c)
    check(f"2-50 到 {frac_}c 的時間 (s)", u * cc / 10, want, tol=0.01, rel=True)
print("      (年)", 0.5 / math.sqrt(0.75) * cc / 10 / 3.156e7, 0.99 / math.sqrt(1 - 0.99**2) * cc / 10 / 3.156e7)
Fm, cs = sp.symbols("F m_0", positive=True)
cS = sp.Symbol("c", positive=True)
vrel = (Fm * t / cs) / sp.sqrt(1 + (Fm * t / (cs * cS))**2)
zero("2-50 p=γ m0 v = Ft", cs * vrel / sp.sqrt(1 - vrel**2 / cS**2) - Fm * t)
xrel = cs * cS**2 / Fm * (sp.sqrt(1 + (Fm * t / (cs * cS))**2) - 1)
zero("2-50 x' = v", sp.diff(xrel, t) - vrel)

# ---------- 第 8 節：拋體 ----------
check("Ex2.6 Big Bertha R (km)", 1450**2 / g * math.sin(math.radians(110)) / 1000, 202, tol=0.5)
T = 2 * 1450 * math.sin(math.radians(55)) / g
check("Ex2.6 T (s)", T, 242, tol=0.5)
check("Ex2.6 ymax (km)", (1450 * math.sin(math.radians(55)))**2 / (2 * g) / 1000, 72, tol=0.5)
al3, be3 = sp.symbols("alpha_3 beta_3", positive=True)
t3 = 2 * v0 * sp.sin(al3 - be3) / (gg * sp.cos(be3))
zero("2-3 交點在直線上", (v0 * sp.sin(al3) * t3 - gg * t3**2 / 2) - v0 * sp.cos(al3) * t3 * sp.tan(be3))
check("2-5 最小半徑 (km)", (3 * 330)**2 / (8 * g) / 1000, 12.5, tol=0.01)
xx = sp.Symbol("X", positive=True)
roots = sp.solve(sp.Eq(xx - gg * xx**2 / v0**2, h), xx)
zero("2-8 d = |x1-x2|", sp.simplify((roots[1] - roots[0])**2 - (v0 / gg * sp.sqrt(v0**2 - 4 * gg * h))**2))
check("2-19 θmax = asin(√(8/9))", math.degrees(math.asin(math.sqrt(8 / 9))), 70.5, tol=0.05)
# 2-14 數值：最佳角與最大距離
b14 = math.radians(20)
dfun = lambda a: 2 * 30**2 * math.cos(a) * math.sin(a - b14) / (g * math.cos(b14)**2)
aa_ = np.linspace(b14, math.pi / 2, 200001)
best = aa_[np.argmax([dfun(a) for a in aa_])]
check("2-14 最佳 α = π/4 + β/2", math.degrees(best), 45 + 10, tol=0.01)
check("2-14 最大距離 v0²/(g(1+sinβ))", max(dfun(a) for a in aa_), 30**2 / (g * (1 + math.sin(b14))), tol=1e-3)

# ---------- 第 9 節：有阻力的拋體 ----------
def drag_range(kk, v=600.0, th_deg=60.0):
    U, V = v * math.cos(math.radians(th_deg)), v * math.sin(math.radians(th_deg))
    yT = lambda T: -g * T / kk + (kk * V + g) / kk**2 * (1 - math.exp(-kk * T))
    T = brentq(yT, 1e-6 + 2 * V / g * 0.01, 2 * V / g * 1.01 + 1)
    return U / kk * (1 - math.exp(-kk * T)), T
R0 = 600**2 * math.sin(math.radians(120)) / g
check("Ex2.7 k=0 射程 (m)", R0, 31812, tol=2)
for kk, want in ((0.005, 23250), (0.01, 18060), (0.02, 12190)):
    Rk, _ = drag_range(kk)
    print(f"      k={kk}: 數值射程 {Rk:.0f} m，微擾 {R0 * (1 - 4 * kk * 600 * math.sin(math.radians(60)) / (3 * g)):.0f} m")
    check(f"Ex2.7 k={kk} 數值射程（約）", Rk, want, tol=0.02, rel=True)
check("Ex2.7 微擾公式變 0 的 k", 3 * g / (4 * 600 * math.sin(math.radians(60))), 0.0141, tol=0.0001)
# 微擾展開檢查：T ≈ 2V/g (1 - kV/(3g))
Vs = sp.Symbol("V", positive=True)
Tser = sp.Symbol("T")
expr = Tser - (k * Vs + gg) / (gg * k) * (1 - sp.exp(-k * Tser))
T1 = 2 * Vs / gg * (1 - k * Vs / (3 * gg))
zero("Ex2.7 T 的一階微擾", sp.series(expr.subs(Tser, T1), k, 0, 2).removeO())
# 2-12
vt, vu = sp.symbols("v_t u", positive=True)
ret = v0 * vt / sp.sqrt(v0**2 + vt**2)
kk_ = gg / vt**2
xmax = sp.log((gg + kk_ * v0**2) / gg) / (2 * kk_)
zero("2-12 v^2 = g/k (1 - e^{-2k xmax})", ret**2 - gg / kk_ * (1 - sp.exp(-2 * kk_ * xmax)))
s12 = solve_ivp(lambda tt, y: [y[1], -g - 0.01 * y[1] * abs(y[1])], [0, 60], [0, 30.0], events=lambda tt, y: y[0] if tt > 0.1 else 1, rtol=1e-11, atol=1e-11)
vtn = math.sqrt(g / 0.01)
check("2-12 數值：回到原點的速率", abs(s12.y_events[0][0][1]), 30 * vtn / math.sqrt(30**2 + vtn**2), tol=1e-4)
# Ex 2.8 粗略重現（讀 Fig. 2-3 的阻力曲線，30 kg，600 m/s，45°）
vtab = [0, 100, 200, 300, 330, 350, 400, 450, 500, 600, 800, 1000]
Ftab = [0, 15, 40, 95, 135, 210, 300, 385, 460, 620, 930, 1250]   # 2026-10-21 依課本 p.60 原圖重讀（400 m/s 在 300 N 格線上）
Fd = lambda s: np.interp(s, vtab, Ftab)
def rhs(tt, y):
    sp_ = math.hypot(y[2], y[3])
    return [y[2], y[3], -Fd(sp_) / 30 * y[2] / sp_, -g - Fd(sp_) / 30 * y[3] / sp_]
s28 = solve_ivp(rhs, [0, 200], [0, 0, 600 / math.sqrt(2), 600 / math.sqrt(2)], events=lambda tt, y: y[1] if tt > 1 else 1, rtol=1e-8, max_step=0.05)
print(f"      Ex2.8 粗略重現：有阻力射程 {s28.y_events[0][0][0] / 1000:.1f} km（課本約 16 km），無阻力 {600**2 / g / 1000:.1f} km（課本約 37 km）")
check("Ex2.8 無阻力射程 (km)", 600**2 / g / 1000, 36.7, tol=0.05)
check("Ex2.8 有阻力射程約 16 km", s28.y_events[0][0][0] / 1000, 16, tol=0.15, rel=True)

# ---------- 第 10 節：Atwood、帶電粒子 ----------
x1, x2, T_, al_e = sp.symbols("x1dd x2dd T alpha_e")
solA = sp.solve([m1 * (x1 + al_e) - (m1 * gg - T_), m2 * (-x1 + al_e) - (m2 * gg - T_)], [x1, T_])
zero("Ex2.9 加速度", solA[x1] - (m1 - m2) * (gg - al_e) / (m1 + m2))
zero("Ex2.9 張力", solA[T_] - 2 * m1 * m2 * (gg - al_e) / (m1 + m2))
w, Ey, Bq, A_ = sp.symbols("omega E_y B A", positive=True)
xq = -A_ / w * sp.cos(w * t) + Ey / Bq * t
yq = A_ / w * sp.sin(w * t)
# m x'' = qB y'，m y'' = qE - qB x'；q/m = ω/B
zero("2-22 x 方程", sp.diff(xq, t, 2) - w * sp.diff(yq, t))
zero("2-22 y 方程", sp.diff(yq, t, 2) - (w * Ey / Bq - w * sp.diff(xq, t)))
zero("2-22 <xdot>", sp.integrate(sp.diff(xq, t), (t, 0, 2 * sp.pi / w)) / (2 * sp.pi / w) - Ey / Bq)
z0d, aq = sp.symbols("zdot0 a_q", positive=True)
xh, zh = z0d / aq * sp.cos(aq * t), z0d / aq * sp.sin(aq * t)
zero("Ex2.10 x'' = -α z'", sp.diff(xh, t, 2) + aq * sp.diff(zh, t))
zero("Ex2.10 z'' = α x'", sp.diff(zh, t, 2) - aq * sp.diff(xh, t))

# ---------- 第 11 節：動量、角動量 ----------
Lz = m * (v0 * sp.cos(al3) * t * (v0 * sp.sin(al3) - gg * t) - (v0 * sp.sin(al3) * t - gg * t**2 / 2) * v0 * sp.cos(al3))
zero("2-21 L_z = -½ m g v0 cosα t²", Lz + m * gg * v0 * sp.cos(al3) * t**2 / 2)
zero("2-21 dL/dt = N_z = -mg x", sp.diff(Lz, t) + m * gg * v0 * sp.cos(al3) * t)
Mb, mb, vv_ = sp.symbols("M m_b v", positive=True)
v3, v4 = sp.symbols("v3 v4")
s28b = sp.solve([Mb * vv_ - mb * vv_ - (Mb * v3 + mb * v4), v4 - v3 - 2 * vv_], [v3, v4])
alr = mb / Mb
zero("2-28 彈珠速度", s28b[v4] - (3 - alr) / (1 + alr) * vv_)
zero("2-28 超級球速度", s28b[v3] - (1 - 3 * alr) / (1 + alr) * vv_)
zero("2-28 能量守恆", Mb * vv_**2 + mb * vv_**2 - Mb * s28b[v3]**2 - mb * s28b[v4]**2)

# ---------- 第 12 節：功 ----------
check("2-26 無摩擦壓縮量", 4 * math.sqrt(2 / 6), 2.31, tol=0.005)
check("2-26 粗糙 2 m 後的壓縮量", math.sqrt((0.5 * 2 * 16 - 0.2 * 2 * g * 2) * 2 / 6), 1.65, tol=0.005)
check("2-27 功 (J)", 0.1 * g * 0.6**2 / 2, 0.176, tol=0.001)
uu = sp.Symbol("u_t", positive=True)
zero("2-41 地面動能增加 = ½mv² + muv", (m * (vv_ + uu)**2 / 2 - m * uu**2 / 2) - (m * vv_**2 / 2 + m * vv_ * uu))

# ---------- 第 13 節：保守力 ----------
X, Y, Z = sp.symbols("X Y Z")
def curl(F):
    return [sp.diff(F[2], Y) - sp.diff(F[1], Z), sp.diff(F[0], Z) - sp.diff(F[2], X), sp.diff(F[1], X) - sp.diff(F[0], Y)]
Ufun = sp.Function("U")(X, Y, Z)
Fgrad = [-sp.diff(Ufun, X), -sp.diff(Ufun, Y), -sp.diff(Ufun, Z)]
cx = sp.diff(Fgrad[2], Y) - sp.diff(Fgrad[1], Z)
zero("p.135 (∇×F)_x 照講義寫成 ∂²U/∂z∂y − ∂²U/∂y∂z（符號正確）", cx - (sp.Derivative(Ufun, Z, Y) - sp.Derivative(Ufun, Y, Z)).doit())
zero("p.135 (∇×F)_x = 0", cx)
Fp = [a_ * X + b_ * Y**2, c_ * X * Y, 0]
print("      p.139 curl:", [sp.factor(cmp) for cmp in curl(Fp)])
zero("p.139 c=2b 時旋度為 0", curl([a_ * X + b_ * Y**2, 2 * b_ * X * Y, 0])[2])
Ua = -(a_ * X * Y * Z + b_ * X**2 / 2 + c_ * X + b_ * Y * Z)
Fa = [a_ * Y * Z + b_ * X + c_, a_ * X * Z + b_ * Z, a_ * X * Y + b_ * Y]
zero("2-53(a) 旋度", sum(cmp**2 for cmp in curl(Fa)))
zero("2-53(a) -∇U = F", sum((-sp.diff(Ua, s_) - f)**2 for s_, f in zip((X, Y, Z), Fa)))
Zp = sp.Symbol("Zp", positive=True)
Fb = [-Zp * sp.exp(-X), sp.log(Zp), sp.exp(-X) + Y / Zp]
Ub = -(Zp * sp.exp(-X) + Y * sp.log(Zp))
zero("2-53(b) -∇U = F", sum((-sp.diff(Ub, s_) - f)**2 for s_, f in zip((X, Y, Zp), Fb)))
cb = [sp.diff(Fb[2], Y) - sp.diff(Fb[1], Zp), sp.diff(Fb[0], Zp) - sp.diff(Fb[2], X), sp.diff(Fb[1], X) - sp.diff(Fb[0], Y)]
zero("2-53(b) 旋度", sum(cmp**2 for cmp in cb))

# ---------- 第 14 節：迴圈軌道 2-25 ----------
Rr = sp.Symbol("R", positive=True)
vB2 = 2 * gg * h - 2 * gg * Rr + sp.sqrt(2) * gg * Rr
zero("2-25 vB² 由能量守恆", m * vB2 / 2 + m * gg * (Rr - Rr / sp.sqrt(2)) - m * gg * h)
NB = m * gg / sp.sqrt(2) + m * vB2 / Rr
zero("2-25 N_B", NB - m * gg * (2 * h / Rr + 3 / sp.sqrt(2) - 2))
hp = Rr * (1 - 1 / sp.sqrt(2))
vB = sp.sqrt(vB2)
tl = (vB / sp.sqrt(2) + sp.sqrt(vB2 / 2 + 2 * gg * hp)) / gg
zero("2-25 落地時間滿足 y=0", hp + vB / sp.sqrt(2) * tl - gg * tl**2 / 2)
# 2-25 數值例（只為檢查公式，題目沒給 R）：h=3.91 m，R=1 m
hh, RR = 3.91, 1.0
vBn = math.sqrt(2 * g * hh - 2 * g * RR + math.sqrt(2) * g * RR)
hpn = RR * (1 - 1 / math.sqrt(2))
tn = (vBn / math.sqrt(2) + math.sqrt(vBn**2 / 2 + 2 * g * hpn)) / g
dn = RR / math.sqrt(2) + vBn / math.sqrt(2) * tn
H25 = hh - RR + RR / math.sqrt(2)
form = RR / math.sqrt(2) + H25 + math.sqrt(H25**2 + 2 * H25 * hpn)
check("2-25 落點距離公式 (h=3.91, R=1)", dn, form, tol=1e-9)
s25 = solve_ivp(lambda tt, y: [y[2], y[3], 0, -g], [0, 5], [RR / math.sqrt(2), hpn, vBn / math.sqrt(2), vBn / math.sqrt(2)], events=lambda tt, y: y[1] if tt > 0.01 else 1, rtol=1e-11)
check("2-25 數值積分落點", s25.y_events[0][0][0], dn, tol=1e-6)
check("2-25 N_A/mg (h=3.91, R=1)", 1 + 2 * hh / RR, 8.82, tol=0.001)
# 講義 p.149–150 的作法（原點在 B）：g t² − √2 v t + (√2R − 2R) = 0，改正後的根號 2v² − 4g(√2R − 2R)
t_h = (math.sqrt(2) * vBn + math.sqrt(2 * vBn**2 - 4 * g * (math.sqrt(2) * RR - 2 * RR))) / (2 * g)
check("2-25 講義原點在 B 的落點（改正後）", RR / math.sqrt(2) + vBn / math.sqrt(2) * t_h, dn, tol=1e-9)
print("      講義 p.149 照印的根號內 R−2R =", RR - 2 * RR, "（負數，式子無意義）")

# ---------- 第 15 節：平衡 ----------
U0s = sp.Symbol("U0", positive=True)
U47 = U0s * (a_ / x + x / a_)
zero("2-47 U'(a)=0", sp.diff(U47, x).subs(x, a_))
zero("2-47 U''(a)=2U0/a²", sp.diff(U47, x, 2).subs(x, a_) - 2 * U0s / a_**2)
check("2-47 U0=1 J, a=2 m: U''(2)", 2 * 1 / 2**2, 0.5)
check("2-47 U(2)", 1 * (2 / 2 + 2 / 2), 2)
bq, dq, x1s = sp.symbols("b_q d_q x_1", positive=True)
U212 = -m1 * gg * x1s - m2 * gg * sp.sqrt((bq - x1s)**2 / 4 - dq**2)
x0s = bq - 4 * m1 * dq / sp.sqrt(4 * m1**2 - m2**2)
num = {m1: 3, m2: 2, gg: sp.Rational(98, 10), bq: 10, dq: 2}
check("Ex2.12 數值 U'(x0)=0", float(sp.diff(U212, x1s).subs(x1s, x0s).subs(num)), 0, tol=1e-9)
check("Ex2.12 U''(x0) 公式", float(sp.diff(U212, x1s, 2).subs(x1s, x0s).subs(num)),
      float((gg * (4 * m1**2 - m2**2)**sp.Rational(3, 2) / (4 * m2**2 * dq)).subs(num)), tol=1e-9)
yy = sp.Symbol("y", real=True)
Zy = -(yy**2 + 1) / (yy**4 + 8)
print("      Ex2.13 平衡點:", sp.solve(sp.diff(Zy, yy), yy))
check("Ex2.13 Z(√2) = -1/4", float(Zy.subs(yy, sp.sqrt(2))), -0.25)
check("Ex2.13 Z(0) = -1/8", float(Zy.subs(yy, 0)), -0.125)
check("Ex2.13 Z''(0) = -1/4 < 0（不穩定）", float(sp.diff(Zy, yy, 2).subs(yy, 0)), -0.25, tol=1e-9)
check("Ex2.13 Z''(√2) = 1/3 > 0（穩定）", float(sp.diff(Zy, yy, 2).subs(yy, sp.sqrt(2))), 1 / 3, tol=1e-9)
print("      Ex2.13 E=-W/8 的轉折點:", sp.solve(sp.Eq(Zy, -sp.Rational(1, 8)), yy))
kq, aq2 = sp.symbols("k_q a_2", positive=True)
U43 = kq * x**2 / 2 - kq * x**4 / (4 * aq2**2)
zero("2-43 -U' = F", -sp.diff(U43, x) - (-kq * x + kq * x**3 / aq2**2))
zero("2-43 U(α) = kα²/4", U43.subs(x, aq2) - kq * aq2**2 / 4)
U52 = U0s * (2 * (x / a_)**2 - (x / a_)**4)
zero("2-52 U''(0)", sp.diff(U52, x, 2).subs(x, 0) - 4 * U0s / a_**2)
zero("2-52 U(a) = U0", U52.subs(x, a_) - U0s)
xs52 = a_ * sp.tanh(sp.sqrt(2 * U0s / (m * a_**2)) * t)
zero("2-52(e) x(t) 的能量 = U0", sp.simplify(m * sp.diff(xs52, t)**2 / 2 + U52.subs(x, xs52) - U0s))
# 2-42 立方體在圓柱上：h(θ) = (R + b/2)cosθ + Rθ sinθ
Rc, bc, thc = sp.symbols("R_c b_c theta_c", positive=True)
hc = (Rc + bc / 2) * sp.cos(thc) + Rc * thc * sp.sin(thc)
zero("2-42 h'(0)=0", sp.diff(hc, thc).subs(thc, 0))
zero("2-42 h''(0) = R - b/2", sp.diff(hc, thc, 2).subs(thc, 0) - (Rc - bc / 2))
print("      2-42 R=b/2 時 h 的四階導數:", sp.simplify(sp.diff(hc, thc, 4).subs(thc, 0).subs(Rc, bc / 2)))

# ---------- 考前衝刺 變化題 ----------
check("變化題1 θc=atan0.5", math.degrees(math.atan(0.5)), 26.6, tol=0.05)
check("變化題1 a (θ=35°, μk=0.4)", g * (math.sin(math.radians(35)) - 0.4 * math.cos(math.radians(35))), 2.41, tol=0.01)
zero("變化題2 v=v0/(1+kv0 t) 滿足 v'=-kv²", sp.diff(v0 / (1 + k * v0 * t), t) + k * (v0 / (1 + k * v0 * t))**2)
zero("變化題4 t=artanh(v1√(k/g))/√(gk)", sp.diff(sp.sqrt(gg / k) * sp.tanh(sp.sqrt(gg * k) * t), t) - (gg - k * gg / k * sp.tanh(sp.sqrt(gg * k) * t)**2))
cv = sp.Symbol("c_v", positive=True)
# 變化題 5：m dv/dt = -c√v
sq5 = sp.sqrt(v0) - cv * t / (2 * m)   # √v，在停止前為正
vt5 = sq5**2
zero("變化題5 v(t)", m * sp.diff(vt5, t) + cv * sq5)
t5 = 2 * m * sp.sqrt(v0) / cv
zero("變化題5 停止距離", sp.integrate(vt5, (t, 0, t5)) - 2 * m * v0**sp.Rational(3, 2) / (3 * cv))
R11 = 1.0
h11 = 2 * R11 + (g * R11) / (2 * g)   # 頂端 v² = gR
check("變化題11 h_min/R 與 N_A/mg", [h11 / R11, 1 + 2 * h11 / R11], [2.5, 6.0])
check("變化題12 E=-W/5 轉折點", sorted(math.sqrt(r) for r in ((5 - math.sqrt(13)) / 2, (5 + math.sqrt(13)) / 2)), [0.835, 2.074], tol=0.001)
# 變化題 13：繩子滑下桌面（117 級期末第 3 題的解法）：x'' = g x/L
Ls, x0r = sp.symbols("L x_0", positive=True)
xr = x0r * sp.cosh(sp.sqrt(gg / Ls) * t)
zero("變化題13 x(t)", sp.diff(xr, t, 2) - gg / Ls * xr)
zero("變化題13 ẋ² = g/L (x² - x0²)", sp.diff(xr, t)**2 - gg / Ls * (xr**2 - x0r**2))
zero("變化題9 上升電梯", (solA[x1].subs(al_e, -al_e)) - (m1 - m2) * (gg + al_e) / (m1 + m2))
zero("變化題8 最大高度微擾", sp.series(V0**2 / (2 * gg) - (V0 / k - gg / k**2 * sp.log(1 + k * V0 / gg)) - (V0**3 * k / (3 * gg**2)), k, 0, 2).removeO())
check("變化題1 減速角 atan0.4", math.degrees(math.atan(0.4)), 21.8, tol=0.05)
s3 = sp.integrate(gg / k * (1 - sp.exp(-k * t)), (t, 0, sp.log(2) / k))
zero("變化題3 落下距離 g/k²(ln2-1/2)", s3 - gg / k**2 * (sp.log(2) - sp.Rational(1, 2)))
check("變化題3 係數", math.log(2) - 0.5, 0.193, tol=0.001)
bb6 = sp.Symbol("b6", positive=True)
zero("變化題6 x=b²t²/4 滿足 v=b√x", sp.diff(bb6**2 * t**2 / 4, t) - bb6 * sp.sqrt(bb6**2 * t**2 / 4))
b7 = math.radians(20)
d7 = lambda a: 2 * 30**2 * math.cos(a) * math.sin(a + b7) / (g * math.cos(b7)**2)
aa7 = np.linspace(0, math.pi / 2, 200001)
best7 = aa7[np.argmax([d7(a) for a in aa7])]
check("變化題7 下坡最佳仰角 π/4-β/2", math.degrees(best7), 45 - 10, tol=0.01)
check("變化題7 下坡最大距離", max(d7(a) for a in aa7), 30**2 / (g * (1 - math.sin(b7))), tol=1e-3)
check("變化題9 a、T", [(3 - 2) * (g + 2) / 5, 2 * 3 * 2 * (g + 2) / 5], [2.36, 28.32], tol=0.005)
Fv = [Y**2 * Z, 2 * X * Y * Z, X * Y**2]
zero("變化題14 旋度", sum(cmp**2 for cmp in curl(Fv)))
zero("變化題14 -∇U = F", sum((-sp.diff(-X * Y**2 * Z, s_) - f)**2 for s_, f in zip((X, Y, Z), Fv)))

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
