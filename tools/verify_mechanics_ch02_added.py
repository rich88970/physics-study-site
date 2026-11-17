"""力學 Lecture 2：本次新增的 20 題課本習題與 30 題自編難題，逐題獨立重算（數值積分、sympy 符號檢查）。

用法：python -X utf8 tools/verify_mechanics_ch02_added.py（需要 numpy、scipy、sympy）
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


def quad_drag(m, A, cw, x0, y0, vx0, vy0, stop, tmax=200.0):
    """v² 阻力 W = ½ c_W ρ A v² 的二維拋體；stop(s) 為 0 時停止。"""
    c = 0.5 * cw * RHO * A / m

    def f(t, s):
        x, y, vx, vy = s
        sp_ = math.hypot(vx, vy)
        return [vx, vy, -c * sp_ * vx, -g - c * sp_ * vy]

    ev = lambda t, s: stop(s)
    ev.terminal = True
    return solve_ivp(f, [0, tmax], [x0, y0, vx0, vy0], events=ev, rtol=1e-10, atol=1e-10)


t, x, y, z = sp.symbols("t x y z", real=True)
m, k, R, gg, v0 = sp.symbols("m k R g v_0", positive=True)

print("========== 課本習題 ==========")
# ---- 2-2：球面上的質點（r = R）----
th, ph = sp.Function("theta")(t), sp.Function("phi")(t)
pos = R * sp.Matrix([sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)])
acc = pos.diff(t, 2)
e_r = pos / R
e_th = sp.Matrix([sp.cos(th) * sp.cos(ph), sp.cos(th) * sp.sin(ph), -sp.sin(th)])
e_ph = sp.Matrix([-sp.sin(ph), sp.cos(ph), 0])
thd, phd = th.diff(t), ph.diff(t)
zero("2-2 a_r = -R(θ'² + sin²θ φ'²)", acc.dot(e_r) + R * (thd**2 + sp.sin(th) ** 2 * phd**2))
zero("2-2 a_θ = R(θ'' - sinθcosθ φ'²)", acc.dot(e_th) - R * (th.diff(t, 2) - sp.sin(th) * sp.cos(th) * phd**2))
zero("2-2 a_φ = R(sinθ φ'' + 2cosθ θ'φ')", acc.dot(e_ph) - R * (sp.sin(th) * ph.diff(t, 2) + 2 * sp.cos(th) * thd * phd))

# ---- 2-4：雜耍四顆球 ----
check("2-4 每顆球在空中 3×0.9 s，最小上拋速率 (m/s)", g * (3 * 0.9) / 2, 13.2, tol=0.05)
check("2-4 另一讀法：空中 4×0.9 s 的上拋速率 (m/s)", g * (4 * 0.9) / 2, 17.6, tol=0.05)

# ---- 2-6：飛機投乾草 ----
v6 = 160 / 3.6
t6 = math.sqrt(2 * 80 / g)
check("2-6 落地時間 (s)", t6, 4.04, tol=0.01)
check("2-6 水平飛行距離 (m)", v6 * t6, 179.6, tol=0.1)
check("2-6(a) 落點在牛群前 30 m：推出點距牛群 (m)", v6 * t6 + 30, 209.6, tol=0.1)
check("2-6 另一讀法（落在牛群後方）推出點 (m)", v6 * t6 - 30, 149.6, tol=0.1)
check("2-6(b) 最多晚推多久 (s)", 30 / v6, 0.675, tol=0.001)

# ---- 2-7：乾草含 v² 阻力 ----
s7 = quad_drag(30, 0.2, 0.8, 0, 80, v6, 0, lambda s: s[1])
x7, t7 = s7.y_events[0][0][0], s7.t_events[0][0]
check("2-7 有阻力的水平飛行距離 (m)", x7, 147.5, tol=0.1)
check("2-7 有阻力的落地時間 (s)", t7, 4.44, tol=0.01)
check("2-7 c、終端速度", [0.5 * 0.8 * RHO * 0.2 / 30, math.sqrt(g / (0.5 * 0.8 * RHO * 0.2 / 30))], [3.47e-3, 53.2], tol=0.05)
check("2-7 落地水平速度、速率", [s7.y_events[0][0][2], math.hypot(*s7.y_events[0][0][2:])], [24.3, 40.7], tol=0.05)
check("2-7 同時推出時兩落點相距 (m)", v6 * t6 - x7, 32.0, tol=0.1)
check("2-7 有阻力時推出點距牛群 (m)", x7 + 30, 177.5, tol=0.1)
check("2-7 照無阻力在 209.6 m 處推出，有阻力落點 (m)", -(v6 * t6 + 30) + x7, -62.1, tol=0.1)

# ---- 2-10：例題 2.4 的數值解 ----
s10 = solve_ivp(lambda tt, s: [s[1], -0.1 * s[1]], [0, 30], [0, 10], t_eval=[5, 10, 20, 30], rtol=1e-10, atol=1e-12)
check("2-10 數值 x(5,10,20,30)", s10.y[0], [39.35, 63.21, 86.47, 95.02], tol=0.01)
check("2-10 數值 v(5,10,20,30)", s10.y[1], [6.065, 3.679, 1.353, 0.498], tol=0.001)
check("2-10 解析 x=100(1-e^{-0.1t}) 與數值相同", 100 * (1 - np.exp(-0.1 * s10.t)), s10.y[0], tol=1e-6)
check("2-10 Euler Δt=0.5 s 在 t=10 s 的 v", 10 * 0.95**20, 3.585, tol=0.001)
check("2-10 減半時間 ln2/k", math.log(2) / 0.1, 6.93, tol=0.01)
check("2-10 v = v0 - kx", s10.y[1], 10 - 0.1 * s10.y[0], tol=1e-6)

# ---- 2-17：壘球越過全壘打牆 ----
th17 = math.radians(35)
v17 = math.sqrt(g * 60**2 / (2 * math.cos(th17) ** 2 * (0.7 + 60 * math.tan(th17) - 2)))
check("2-17 最小初速 (m/s)", v17, 25.4, tol=0.05)

# ---- 2-18：壘球含 v² 阻力 ----
A18 = math.pi * 0.05**2


def y_at_fence(vv, deg):
    a = math.radians(deg)
    s = quad_drag(0.2, A18, 0.5, 0, 0.7, vv * math.cos(a), vv * math.sin(a), lambda s: s[0] - 60)
    return s.y_events[0][0][1] if len(s.t_events[0]) else -1e9


v18 = brentq(lambda vv: y_at_fence(vv, 35) - 2, 20, 80)
check("2-18(a) 35° 時所需初速 (m/s)", v18, 35.2, tol=0.05)
check("2-18 阻力常數 c、終端速度", [0.5 * 0.5 * RHO * A18 / 0.2, math.sqrt(g / (0.5 * 0.5 * RHO * A18 / 0.2))], [0.01276, 27.7], tol=0.05)
s18 = quad_drag(0.2, A18, 0.5, 0, 0.7, 25.41 * math.cos(math.radians(35)), 25.41 * math.sin(math.radians(35)), lambda s: s[1] if s[3] < 0 else 1.0)
check("2-18 用 25.4 m/s 有阻力時的落地距離 (m)", s18.y_events[0][0][0], 41.4, tol=0.1)
s18b = quad_drag(0.2, A18, 0.5, 0, 0.7, v18 * math.cos(math.radians(35)), v18 * math.sin(math.radians(35)), lambda s: s[0] - 60)
check("2-18 到牆時間、到牆速率", [s18b.t_events[0][0], math.hypot(*s18b.y_events[0][0][2:])], [3.27, 18.5], tol=0.05)
best = minimize_scalar(lambda a: -y_at_fence(v18, a), bounds=(20, 60), method="bounded")
check("2-18(b) 最容易過牆的仰角 (°)", best.x, 40.7, tol=0.1)
check("2-18(b) 過牆高度餘裕 (m)", -best.fun - 2, 1.10, tol=0.01)

# ---- 2-20：Fig. 2-3 的阻力，140 m/s 打 1000 m ----
A20 = math.pi * 0.05**2
check("2-20 140 m/s 的阻力 (N)，c_W=0.2", 0.5 * 0.2 * RHO * A20 * 140**2, 20.0, tol=0.05)


def range20(deg):
    a = math.radians(deg)
    s = quad_drag(10, A20, 0.2, 0, 0, 140 * math.cos(a), 140 * math.sin(a), lambda s: s[1] if s[3] < 0 else 1.0)
    return s.y_events[0][0][0]


lo20 = brentq(lambda a: range20(a) - 1000, 5, 40)
hi20 = brentq(lambda a: range20(a) - 1000, 50, 85)
check("2-20 低仰角 (°)", lo20, 16.2, tol=0.05)
check("2-20 高仰角 (°)", hi20, 72.2, tol=0.1)
check("2-20 15°、75° 有阻力時的射程 (m)", [range20(15), range20(75)], [936, 862], tol=0.6)
check("2-20 有阻力最大射程約 (m)", max(range20(a) for a in np.arange(40, 48, 0.5)), 1732, tol=2)
check("2-20 無阻力仰角 (°)", [math.degrees(0.5 * math.asin(g * 1000 / 140**2)), 90 - 15], [15.0, 75.0], tol=1e-6)

# ---- 2-23：F = k t e^{-αt} ----
kk, aa = sp.Rational(1), sp.Rational(1, 2)
vt23 = sp.integrate(kk * sp.Symbol("s") * sp.exp(-aa * sp.Symbol("s")), (sp.Symbol("s"), 0, t))
xt23 = sp.integrate(vt23.subs(t, sp.Symbol("s")), (sp.Symbol("s"), 0, t))
zero("2-23 v(t) = 4[1-(1+t/2)e^{-t/2}]", vt23 - 4 * (1 - (1 + t / 2) * sp.exp(-t / 2)))
zero("2-23 x(t) = 4[t-4+(t+4)e^{-t/2}]", xt23 - 4 * (t - 4 + (t + 4) * sp.exp(-t / 2)))
check("2-23 t=2 s 的 a, v, x", [float(2 * sp.exp(-1)), float(vt23.subs(t, 2)), float(xt23.subs(t, 2))], [0.736, 1.057, 0.829], tol=0.001)
check("2-23 t=10 s 的 a, v, x", [float(10 * sp.exp(-5)), float(vt23.subs(t, 10)), float(xt23.subs(t, 10))], [0.0674, 3.838, 24.38], tol=0.005)
tab = [[float(f.subs(t, tv)) for tv in (2, 5, 10, 20)] for f in (t * sp.exp(-t / 2), vt23, xt23)]
check("2-23 數值表 a(2,5,10,20)", tab[0], [0.736, 0.410, 0.067, 0.001], tol=0.001)
check("2-23 數值表 v", tab[1], [1.06, 2.85, 3.84, 4.00], tol=0.005)
check("2-23 數值表 x", tab[2], [0.83, 6.96, 24.4, 64.0], tol=0.05)
check("2-23 終端速度 k/(mα²)", float(sp.limit(vt23, t, sp.oo)), 4.0)

# ---- 2-30：水球與聲音 ----
q30 = g / (2 * 331)
tau30 = (-1 + math.sqrt(1 + 4 * q30 * 4.021)) / (2 * q30)
h30 = g * tau30**2 / 2
check("2-30 落下時間 (s)", tau30, 3.807, tol=0.001)
check("2-30 樓高 (m)", h30, 71.0, tol=0.05)
check("2-30 代回總時間 (s)", math.sqrt(2 * h30 / g) + h30 / 331, 4.021, tol=1e-6)

# ---- 2-31：例題 2.10 加上 x 方向初速 ----
al = sp.Symbol("alpha", positive=True)
xd0, zd0, yd0 = sp.symbols("xdot0 zdot0 ydot0", real=True)
X = (zd0 / al) * sp.cos(al * t) + (xd0 / al) * sp.sin(al * t)
Z = -(xd0 / al) * sp.cos(al * t) + (zd0 / al) * sp.sin(al * t)
zero("2-31 ẍ = -α ż", X.diff(t, 2) + al * Z.diff(t))
zero("2-31 z̈ = α ẋ", Z.diff(t, 2) - al * X.diff(t))
zero("2-31 ẋ(0) = ẋ0", X.diff(t).subs(t, 0) - xd0)
zero("2-31 ż(0) = ż0", Z.diff(t).subs(t, 0) - zd0)
zero("2-31 半徑² = (ẋ0²+ż0²)/α²", X**2 + Z**2 - (xd0**2 + zd0**2) / al**2)

# ---- 2-33：各種物體從 100 m 落下 ----
def fall(mm, r):
    A = math.pi * r**2
    vt = math.sqrt(2 * mm * g / (0.5 * RHO * A))
    v100 = vt * math.sqrt(1 - math.exp(-2 * g * 100 / vt**2))
    t100 = vt / g * math.acosh(math.exp(g * 100 / vt**2))
    return vt, v100, t100


rain = lambda r: 1000 * 4 / 3 * math.pi * r**3
bb, pp, r3 = fall(0.145, 0.0366), fall(0.0024, 0.019), fall(rain(0.003), 0.003)
check("2-33(a) 棒球 v_t, v(100 m), t (s)", bb, [32.2, 29.7, 5.25], tol=0.05)
check("2-33(b) 乒乓球 v_t, v(100 m), t", pp, [7.99, 7.99, 13.08], tol=0.01)
check("2-33(e) c_W ρA/2m：棒球、乒乓球 (1/m)", [0.5 * RHO * math.pi * 0.0366**2 / (2 * 0.145), 0.5 * RHO * math.pi * 0.019**2 / (2 * 0.0024)], [9.43e-3, 0.154], tol=0.01, rel=True)
check("2-33 無阻力 100 m 落地時間、速率", [math.sqrt(200 / g), math.sqrt(2 * g * 100)], [4.52, 44.3], tol=0.05)
check("2-33 v_t²/g：棒球、乒乓球、雨滴", [bb[0]**2 / g, pp[0]**2 / g, r3[0]**2 / g], [106, 6.5, 12.3], tol=0.05)
check("2-33(c) 雨滴 3 mm 的質量 (mg)", rain(0.003) * 1e6, 113.1, tol=0.1)
check("2-33(c) 雨滴 v_t, v(100 m), t", r3, [10.98, 10.98, 9.88], tol=0.01)
check("2-33(f) 雨滴 2 mm、4 mm 的 v_t", [fall(rain(0.002), 0.002)[0], fall(rain(0.004), 0.004)[0]], [8.97, 12.68], tol=0.01)
# 數值積分交叉驗算棒球
sb = solve_ivp(lambda tt, s: [s[1], g - 0.5 * 0.5 * RHO * math.pi * 0.0366**2 / 0.145 * s[1] ** 2], [0, 20], [0, 0],
               events=lambda tt, s: s[0] - 100, rtol=1e-10, atol=1e-10)
check("2-33 棒球數值積分 落地時間與速率", [sb.t_events[0][0], sb.y_events[0][0][1]], [5.25, 29.7], tol=0.05)

# ---- 2-35：例題 2.7 數值（v0=600 m/s、θ=60°）----
U35, V35 = 600 * math.cos(math.radians(60)), 600 * math.sin(math.radians(60))
want35 = {0.005: (98.06, 23.25, 11.74), 0.01: (92.10, 18.06, 10.27), 0.02: (83.71, 12.19, 8.27),
          0.04: (73.97, 7.11, 6.02), 0.08: (65.17, 3.73, 3.96)}
for kv, (Tw, Rw, Hw) in want35.items():
    T = brentq(lambda T: T - (kv * V35 + g) / (g * kv) * (1 - math.exp(-kv * T)), 1e-3, 500)
    Rr = U35 / kv * (1 - math.exp(-kv * T)) / 1000
    H = (V35 / kv - g / kv**2 * math.log(1 + kv * V35 / g)) / 1000
    check(f"2-35 k={kv}: T (s), R (km), y_max (km)", [T, Rr, H], [Tw, Rw, Hw], tol=0.01)
check("2-35 k=0: R, y_max, T", [600**2 * math.sin(math.radians(120)) / g / 1000, V35**2 / (2 * g) / 1000, 2 * V35 / g], [31.81, 13.78, 106.04], tol=0.01)
check("2-35 微擾式在 k = 3g/4V 變成零", 3 * g / (4 * V35), 0.0141, tol=0.0001)
check("2-35 k=0.005 微擾射程 (km)", 31.813 * (1 - 4 * 0.005 * V35 / (3 * g)), 20.57, tol=0.01)
# 用數值積分交叉驗算 k=0.02
s35 = solve_ivp(lambda tt, s: [s[2], s[3], -0.02 * s[2], -g - 0.02 * s[3]], [0, 200], [0, 0, U35, V35],
                events=lambda tt, s: s[1] if tt > 1 else 1, rtol=1e-10, atol=1e-8)
check("2-35 k=0.02 數值積分射程 (km)", s35.y_events[0][0][0] / 1000, 12.19, tol=0.01)

# ---- 2-36：懸崖上的砲 ----
th_, h_, v_ = sp.symbols("theta h v", positive=True)
Rb = v_ * sp.cos(th_) / gg * (v_ * sp.sin(th_) + sp.sqrt(v_**2 * sp.sin(th_) ** 2 + 2 * gg * h_))
yb = lambda T: v_ * sp.sin(th_) * T - gg * T**2 / 2
Tb = (v_ * sp.sin(th_) + sp.sqrt(v_**2 * sp.sin(th_) ** 2 + 2 * gg * h_)) / gg
zero("2-36 飛行時間使 y = -h", yb(Tb) + h_)
for vv, hh, deg, rmax in [(100, 100, 42.44, 1115.9), (50, 100, 36.82, 340.7), (30, 200, 23.37, 212.5)]:
    f = lambda a: -float(Rb.subs({v_: vv, h_: hh, gg: g, th_: a}))
    r = minimize_scalar(f, bounds=(0, math.pi / 2), method="bounded", options={"xatol": 1e-10})
    ana = math.degrees(math.asin(1 / math.sqrt(2 + 2 * g * hh / vv**2)))
    check(f"2-36 v0={vv}, h={hh}: 數值最佳角、解析最佳角、最大射程", [math.degrees(r.x), ana, -r.fun], [deg, deg, rmax], tol=0.05)
    check(f"2-36 v0={vv}, h={hh}: R_max = (v0/g)√(v0²+2gh)", vv / g * math.sqrt(vv**2 + 2 * g * hh), rmax, tol=0.05)

# ---- 2-40：擺線形軌道 ----
A, w = sp.symbols("A alpha", positive=True)
X40 = A * (2 * w * t - sp.sin(w * t))
Y40 = A * (1 - sp.cos(w * t))
vx, vy = X40.diff(t), Y40.diff(t)
ax_, ay_ = vx.diff(t), vy.diff(t)
speed = sp.sqrt(vx**2 + vy**2)
zero("2-40 v² = A²α²(5-4cos αt)", vx**2 + vy**2 - A**2 * w**2 * (5 - 4 * sp.cos(w * t)))
zero("2-40 |a| = Aα²", ax_**2 + ay_**2 - A**2 * w**4)
at = sp.simplify(speed.diff(t))
zero("2-40 a_t = 2Aα² sin αt / √(5-4cos αt)", at - 2 * A * w**2 * sp.sin(w * t) / sp.sqrt(5 - 4 * sp.cos(w * t)))
an = (vx * ay_ - vy * ax_) / speed
zero("2-40 a_n = Aα²(2cos αt - 1)/√(5-4cos αt)", an - A * w**2 * (2 * sp.cos(w * t) - 1) / sp.sqrt(5 - 4 * sp.cos(w * t)))
cs = np.linspace(-1, 1, 20001)
fan = np.abs(2 * cs - 1) / np.sqrt(5 - 4 * cs)
check("2-40 |a_n|/(Aα²) 的最大值與發生的 cos αt", [fan.max(), cs[np.argmax(fan)]], [1.0, -1.0], tol=1e-6)
check("2-40 cos αt = 1 時 |a_n| 也等於 Aα²", fan[-1], 1.0, tol=1e-9)

# ---- 2-44：例題 2.12 用力求解 ----
m1, m2, d, b = sp.symbols("m_1 m_2 d b", positive=True)
cosphi = m2 / (2 * m1)
half = d / sp.sqrt(1 - cosphi**2)
x1_force = b - 2 * half
zero("2-44 用力得到的 x1 與能量法相同", x1_force - (b - 4 * m1 * d / sp.sqrt(4 * m1**2 - m2**2)))
x2s = sp.Symbol("x_2", positive=True)
U44 = -m1 * gg * (b - 2 * sp.sqrt(x2s**2 + d**2)) - m2 * gg * x2s
x2e = sp.sqrt(half**2 - d**2)
zero("2-44 dU/dx2 = 0 在平衡點", sp.diff(U44, x2s).subs(x2s, x2e))
zero("2-44 線性化的『恢復係數』2m1 g d²/L³ = d²U/dx2²", sp.diff(U44, x2s, 2) - 2 * m1 * gg * d**2 / (x2s**2 + d**2) ** sp.Rational(3, 2))
# 數值：m1=1, m2=1.2, d=1, b=5：小擾動在力的方程式下振盪（穩定）
M1, M2, D, B = 1.0, 1.2, 1.0, 5.0
x2eq = float(x2e.subs({m1: M1, m2: M2, d: D}))


def eom44(tt, s):
    x2, v2 = s
    L = math.sqrt(x2**2 + D**2)
    c = x2 / L
    # 繩長限制 x1 = b - 2L，張力 T 處處相同；消去 T 與 ẍ1
    dcdx = D**2 / L**3
    # ẍ1 = -2(c ẍ2 + dcdx·... ) ；精確：ẋ1 = -2 c ẋ2，ẍ1 = -2 c ẍ2 - 2 (dc/dx2) ẋ2²
    a2 = (M2 * g - 2 * M1 * g * c - 4 * M1 * c * dcdx * v2**2) / (M2 + 4 * M1 * c**2)
    return [v2, a2]


s44 = solve_ivp(eom44, [0, 20], [x2eq + 0.01, 0], rtol=1e-10, atol=1e-12, max_step=0.01)
truth("2-44 擾動 0.01 後 x2 一直在平衡點附近（穩定）", np.max(np.abs(s44.y[0] - x2eq)) < 0.0101)
cph = M2 / (2 * M1)
Lh = D / math.sqrt(1 - cph**2)
w44 = math.sqrt(2 * M1 * g * D**2 / (Lh**3 * (M2 + 4 * M1 * cph**2)))
ycross = s44.y[0] - x2eq
tc = [s44.t[i] for i in range(1, len(ycross)) if ycross[i - 1] > 0 >= ycross[i]]
check("2-44 線性化角頻率 vs 數值模擬週期", [2 * math.pi / w44, np.mean(np.diff(tc))], [3.223, 3.223], tol=0.01)
check("2-44 m1=1, m2=1.2, d=1：cosφ、L、x2", [cph, Lh, x2eq], [0.6, 1.25, 0.75], tol=1e-9)

# ---- 2-45、2-46：高階導數判穩定 ----
xs = sp.Symbol("x", real=True)


def classify(U):
    for nn in range(1, 12):
        dn = sp.diff(U, xs, nn).subs(xs, 0)
        if dn != 0:
            if nn == 1:
                return "not eq"
            return "stable" if (nn % 2 == 0 and dn > 0) else "unstable"
    return "?"


for U, want in [(xs**3, "unstable"), (xs**4, "stable"), (-xs**4, "unstable"), (xs**5, "unstable"), (xs**6, "stable"), (xs**4 - xs**5, "stable")]:
    got = classify(U)
    # 直接看 ±0.01 兩側的位能是否都比 U(0) 高
    direct = "stable" if (U.subs(xs, 0.01) > 0 and U.subs(xs, -0.01) > 0) else "unstable"
    truth(f"2-45/46 U={U}: 判準 {got}，直接比較 {direct}", got == want == direct)

# ---- 2-48：等質量雙星 ----
G_ = sp.Symbol("G", positive=True)
mm_, dd_ = sp.symbols("m d", positive=True)
om2 = (G_ * mm_**2 / dd_**2) / (mm_ * dd_ / 2)  # Gm²/d² = m ω² (d/2)
zero("2-48 τ = 2π d^{3/2}/√(2Gm)", 2 * sp.pi / sp.sqrt(om2) - 2 * sp.pi * dd_ ** sp.Rational(3, 2) / sp.sqrt(2 * G_ * mm_))

# ---- 2-55：南瓜砲 ----
v55 = 54
U55 = V55 = v55 * math.cos(math.radians(45))


def R55(kv):
    T = brentq(lambda T: T - (kv * V55 + g) / (g * kv) * (1 - math.exp(-kv * T)), 1e-6, 1000)
    return U55 / kv * (1 - math.exp(-kv * T)), T


k55 = brentq(lambda kv: R55(kv)[0] - 142, 1e-4, 5)
check("2-55 k (1/s)", k55, 0.191, tol=0.001)
check("2-55 飛行時間 (s)", R55(k55)[1], 6.49, tol=0.01)
check("2-55 R(k=0.1)、R(k=0.3)", [R55(0.1)[0], R55(0.3)[0]], [192, 107], tol=0.6)
check("2-55 kV/g、U/k、g/k", [k55 * V55 / g, U55 / k55, g / k55], [0.744, 200, 51.3], tol=0.5)
check("2-55 無阻力射程 (m)", v55**2 / g, 297.6, tol=0.1)
check("2-55 錯用微擾式得到的 k", (1 - 142 / (v55**2 / g)) * 3 * g / (4 * V55), 0.101, tol=0.001)

print("========== 自編難題 ==========")
# ---- s01a：伽利略轉換下的動能 ----
check("s01a 例：S 中碰撞後速度", [(2 - 1) / 3 * 3, 2 * 2 / 3 * 3], [1, 4], tol=1e-12)
T_S = [0.5 * 2 * 9, 0.5 * 2 * 1 + 0.5 * 1 * 16]
T_Sp = [0.5 * 2 * 0 + 0.5 * 1 * 9, 0.5 * 2 * 4 + 0.5 * 1 * 1]
check("s01a S 中前後動能、S'(V=3) 中前後動能", T_S + T_Sp, [9, 9, 4.5, 4.5], tol=1e-12)
Vv, Ptot, Mtot, Tk = sp.symbols("V P M T")
vi = sp.symbols("v1:4")
mi = sp.symbols("m1:4", positive=True)
Tp = sum(sp.Rational(1, 2) * mi[i] * (vi[i] - Vv) ** 2 for i in range(3))
zero("s01a T' = T - V·P + ½MV²", Tp - (sum(sp.Rational(1, 2) * mi[i] * vi[i] ** 2 for i in range(3))
                                         - Vv * sum(mi[i] * vi[i] for i in range(3)) + sp.Rational(1, 2) * sum(mi) * Vv**2))

# ---- s01b：有摩擦的伽利略斜面 ----
def hprime(h, a, bdeg, mu):
    return h * (1 - mu / math.tan(math.radians(a))) / (1 + mu / math.tan(math.radians(bdeg)))


check("s01b h'（β=30°, 10°）", [hprime(1, 30, 30, 0.05), hprime(1, 30, 10, 0.05)], [0.841, 0.712], tol=0.001)
check("s01b 水平面上滑行距離 (m)", (1 - 0.05 / math.tan(math.radians(30))) / 0.05, 18.27, tol=0.01)
check("s01b μ→0 時 h' → h", hprime(1, 30, 5, 1e-9), 1.0, tol=1e-6)
# 數值：斜面 30° 下滑、10° 上坡（摩擦 0.05），直接用 F=ma 算
a_dn = g * (math.sin(math.radians(30)) - 0.05 * math.cos(math.radians(30)))
v_bot2 = 2 * a_dn * (1 / math.sin(math.radians(30)))
a_up = g * (math.sin(math.radians(10)) + 0.05 * math.cos(math.radians(10)))
check("s01b 用 F=ma 分段重算 h'(β=10°)", v_bot2 / (2 * a_up) * math.sin(math.radians(10)), 0.712, tol=0.001)

# ---- s02a：鉛垂線偏角 ----
w2R = 465**2 / 6378137


def plumb(lat):
    L = math.radians(lat)
    return math.degrees(math.atan(w2R * math.sin(L) * math.cos(L) / (g - w2R * math.cos(L) ** 2)))


check("s02a ω²R (m/s²)", w2R, 0.0339, tol=0.0001)
check("s02a 偏角：高雄 22.6°、45°、赤道、極 (°)", [plumb(22.6), plumb(45), plumb(0), plumb(90)], [0.0703, 0.0993, 0, 0], tol=0.0005)
lat_best = minimize_scalar(lambda L: -plumb(L), bounds=(1, 89), method="bounded").x
check("s02a 偏角最大的緯度 (°)", lat_best, 45.0, tol=0.1)
check("s02a 高雄體重計讀數比例 1 - ω²R cos²λ/g", math.hypot(g - w2R * math.cos(math.radians(22.6)) ** 2,
                                                       w2R * math.sin(math.radians(22.6)) * math.cos(math.radians(22.6))) / g, 0.99705, tol=1e-5)

# ---- s02b：加速列車裡落下的球 ----
a2b, H2b = 1.5, 1.0
tf = math.sqrt(2 * H2b / g)
check("s02b 落點在正下方後面 aH/g (cm)", 0.5 * a2b * tf**2 * 100, 15.3, tol=0.05)
check("s02b 車上看路徑的傾角 = 鉛垂線傾角 (°)", [math.degrees(math.atan2(0.5 * a2b * tf**2, H2b)), math.degrees(math.atan(a2b / g))], [8.70, 8.70], tol=0.01)

# ---- s03a：落在秤上的繩子 ----
lam, xx = sp.symbols("lambda x", positive=True)
reading = lam * gg * xx + lam * (2 * gg * xx)  # 靜止部分的重量 + 動量流 λv²
zero("s03a 讀數 = 3λgx", reading - 3 * lam * gg * xx)
# 數值：把繩子切成 N 段依序落下，平均動量流
Lr, lr, Nseg = 1.0, 0.5, 200000
xs_ = np.linspace(0, Lr, Nseg + 1)[1:]
v_ = np.sqrt(2 * g * xs_)
check("s03a 落到 x 時 dp/dt / (λgx) → 2", float(np.mean((lr * v_**2)[Nseg // 2:] / (lr * g * xs_[Nseg // 2:]))), 2.0, tol=1e-9)

# ---- s03b：人在船上走 ----
check("s03b 船移動 (m)、人對岸移動 (m)", [60 * 3 / 180, 3 - 60 * 3 / 180], [1.0, 2.0], tol=1e-12)
# 用 (M+m) v̇_b = -m u̇ - b v_b 數值模擬：u(t) 是任意平滑的走法，∫u dt = 3 m
Tw = 4.0
u_t = lambda tt: (3 / Tw) * (1 - math.cos(2 * math.pi * tt / Tw)) if tt < Tw else 0.0
du_t = lambda tt: (3 / Tw) * (2 * math.pi / Tw) * math.sin(2 * math.pi * tt / Tw) if tt < Tw else 0.0
for bdrag, want in ((0.0, -1.0), (30.0, 0.0)):
    s3b = solve_ivp(lambda tt, s: [s[1], (-60 * du_t(tt) - bdrag * s[1]) / 180], [0, 400], [0, 0], rtol=1e-10, atol=1e-12, max_step=0.01)
    check(f"s03b 水阻 b={bdrag}：船最後的位移 (m)", s3b.y[0][-1], want, tol=1e-3)
s3c = solve_ivp(lambda tt, s: [s[1], (-60 * du_t(tt) - 30 * s[1]) / 180], [0, Tw], [0, 0], rtol=1e-10, atol=1e-12, max_step=0.01)
check("s03b 水阻 b=30：人剛停下時船的位移 (m)", s3c.y[0][-1], -0.72, tol=0.01)

# ---- s04a：F = -kx ----
kk_, AA = sp.symbols("k A", positive=True)
om = sp.sqrt(kk_ / m)
zero("s04a x = A cos ωt 滿足 m ẍ = -kx", m * sp.diff(AA * sp.cos(om * t), t, 2) + kk_ * AA * sp.cos(om * t))
xA = sp.Symbol("x", positive=True)
tint = sp.integrate(1 / (om * sp.sqrt(AA**2 - xA**2)), (xA, 0, AA))
zero("s04a 從 0 到 A 的時間 = (π/2)/ω（四分之一週期）", tint - sp.pi / (2 * om))

# ---- s04b：阻力 m b t v ----
bb_, vv0 = sp.symbols("b v_0", positive=True)
vt4 = vv0 * sp.exp(-bb_ * t**2 / 2)
zero("s04b v = v0 e^{-bt²/2} 滿足 dv/dt = -b t v", vt4.diff(t) + bb_ * t * vt4)
zero("s04b 總距離 v0√(π/2b)", sp.integrate(vt4, (t, 0, sp.oo)) - vv0 * sp.sqrt(sp.pi / (2 * bb_)))
check("s04b 同樣半衰時間的線性阻力：k、總距離", [math.log(2) / math.sqrt(2 * math.log(2) / 0.5), 20 / (math.log(2) / math.sqrt(2 * math.log(2) / 0.5))], [0.416, 48.0], tol=0.05)
check("s04b v0=20, b=0.5：總距離 (m)、降到一半的時間 (s)", [20 * math.sqrt(math.pi), math.sqrt(2 * math.log(2) / 0.5)], [35.45, 1.665], tol=0.005)

# ---- s05a：斜面上最省力的拉法 ----
mm5, th5, mu5 = 20, math.radians(20), 0.4
Fphi = lambda p: mm5 * g * (math.sin(th5) + mu5 * math.cos(th5)) / (math.cos(p) + mu5 * math.sin(p))
r5 = minimize_scalar(Fphi, bounds=(0, 1.5), method="bounded")
check("s05a 最佳角 (°)、最小拉力 (N)、平行斜面拉力 (N)", [math.degrees(r5.x), r5.fun, Fphi(0)], [21.8, 130.6, 140.7], tol=0.05)
check("s05a 最佳角時正向力仍為正 (N)", mm5 * g * math.cos(th5) - r5.fun * math.sin(r5.x), 135.7, tol=0.1)

# ---- s05b：加速楔子 ----
th5b, mu5b = math.radians(30), 0.2
lam5 = math.atan(mu5b)
amin = g * (math.sin(th5b) - mu5b * math.cos(th5b)) / (math.cos(th5b) + mu5b * math.sin(th5b))
amax = g * (math.sin(th5b) + mu5b * math.cos(th5b)) / (math.cos(th5b) - mu5b * math.sin(th5b))
check("s05b a_min = g tan(θ-λ)、a_max = g tan(θ+λ)", [amin, amax], [g * math.tan(th5b - lam5), g * math.tan(th5b + lam5)], tol=1e-9)
check("s05b 數值 a_min, a_max, 無摩擦 g tanθ", [amin, amax, g * math.tan(th5b)], [3.315, 8.61, 5.658], tol=0.005)

# ---- s06a：開傘 ----
vt6, v1 = 5.0, 55.0
acoth = lambda q: 0.5 * math.log((q + 1) / (q - 1))
check("s06a 降到 6 m/s 的時間 (s)", vt6 / g * (acoth(6 / vt6) - acoth(v1 / vt6)), 0.565, tol=0.001)
check("s06a 這段落下的距離 (m)", vt6**2 / (2 * g) * math.log((v1**2 - vt6**2) / (6**2 - vt6**2)), 7.15, tol=0.01)
check("s06a 開傘瞬間減速度 / g", (v1**2 / vt6**2 - 1), 120, tol=1e-9)
s6 = solve_ivp(lambda tt, s: [s[1], g * (1 - s[1] ** 2 / vt6**2)], [0, 1], [0, v1], events=lambda tt, s: s[1] - 6, rtol=1e-11, atol=1e-11)
check("s06a 數值積分：時間、距離", [s6.t_events[0][0], s6.y_events[0][0][0]], [0.565, 7.15], tol=0.005)

# ---- s06b：線性阻力上拋 ----
v6b, k6b = 20.0, 0.2
tup = math.log(1 + k6b * v6b / g) / k6b
H6 = v6b / k6b - g / k6b**2 * math.log(1 + k6b * v6b / g)
tdn = brentq(lambda T: g / k6b * T - g / k6b**2 * (1 - math.exp(-k6b * T)) - H6, 0.1, 50)
vret = g / k6b * (1 - math.exp(-k6b * tdn))
check("s06b 動能損失比例", 1 - vret**2 / v6b**2, 0.384, tol=0.002)
check("s06b 上升時間、最高點、下降時間、回到原處速率", [tup, H6, tdn, vret], [1.711, 16.14, 1.932, 15.70], tol=0.005)
truth("s06b 下降時間 > 上升時間", tdn > tup)
for kv in (0.01, 0.1, 0.5, 2.0):
    tu = math.log(1 + kv * v6b / g) / kv
    Hh = v6b / kv - g / kv**2 * math.log(1 + kv * v6b / g)
    td = brentq(lambda T: g / kv * T - g / kv**2 * (1 - math.exp(-kv * T)) - Hh, 1e-6, 500)
    truth(f"s06b k={kv}: t_down > t_up", td > tu)

# ---- s07a：v = v0 e^{-x/L} ----
L7 = sp.Symbol("L", positive=True)
v7 = v0 * sp.exp(-xA / L7)
zero("s07a F = m v dv/dx = -(m/L) v²", m * v7 * sp.diff(v7, xA) + m / L7 * v7**2)
x7t = L7 * sp.log(1 + v0 * t / L7)
zero("s07a x = L ln(1+v0 t/L) 滿足 dx/dt = v0 e^{-x/L}", sp.diff(x7t, t) - v0 * sp.exp(-x7t / L7))

# ---- s07b：相對論定力的雙曲線 ----
F7, m0, c7 = sp.symbols("F m_0 c", positive=True)
Xc = m0 * c7**2 / F7
x7b = Xc * (sp.sqrt(1 + (F7 * t / (m0 * c7)) ** 2) - 1)
zero("s07b (x + X)² - (ct)² = X²", (x7b + Xc) ** 2 - (c7 * t) ** 2 - Xc**2)
zero("s07b ct - x → X", sp.limit(c7 * t - x7b, t, sp.oo) - Xc)
zero("s07b 牛頓極限 x ≈ ½(F/m0)t²", sp.series(x7b, t, 0, 3).removeO() - F7 * t**2 / (2 * m0))
check("s07b X = c²/(F/m0)，F/m0=10 (m)、(光年)", [2.998e8**2 / 10, 2.998e8**2 / 10 / 9.461e15], [8.99e15, 0.950], tol=0.01, rel=True)

# ---- s08a：安全拋物線 ----
uu = sp.Symbol("u", real=True)
X8, Y8, V8 = sp.symbols("X Y V", positive=True)
aq = gg * X8**2 / (2 * V8**2)
disc = sp.expand(X8**2 - 4 * aq * (Y8 + aq))
Yenv = V8**2 / (2 * gg) - gg * X8**2 / (2 * V8**2)
zero("s08a 判別式 = 0 ⟺ y = v0²/2g - g x²/2v0²", sp.solve(disc, Y8)[0] - Yenv)
a8 = g * 30**2 / (2 * 20**2)
disc8 = 30**2 - 4 * a8 * (8 + a8)
angs = [math.degrees(math.atan((30 + s * math.sqrt(disc8)) / (2 * a8))) for s in (1, -1)]
check("s08a 包絡線在 x=30 m 的高度 (m)", 20**2 / (2 * g) - g * 30**2 / (2 * 20**2), 9.38, tol=0.005)
check("s08a 打中 (30, 8) 的兩個仰角 (°)", angs, [59.75, 45.18], tol=0.01)
for A_ in angs:
    a_ = math.radians(A_)
    tt_ = 30 / (20 * math.cos(a_))
    check(f"s08a 仰角 {A_:.2f}° 代回 y(30)", 20 * math.sin(a_) * tt_ - 0.5 * g * tt_**2, 8.0, tol=1e-9)

# ---- s08b：獵人與猴子 ----
check("s08b D=20, H=10 的最小初速 (m/s)", math.sqrt(g * (20**2 + 10**2) / (2 * 10)), 15.65, tol=0.005)
for kv in (0.0, 0.3):  # 兩者都受同樣的線性阻力仍會打中
    D_, H_, vv = 20.0, 10.0, 25.0
    a_ = math.atan2(H_, D_)

    def f8(tt, s):
        return [s[2], s[3], -kv * s[2], -g - kv * s[3], s[6], s[7], -kv * s[6], -g - kv * s[7]]

    s8 = solve_ivp(f8, [0, 5], [0, 0, vv * math.cos(a_), vv * math.sin(a_), D_, H_, 0, 0],
                   events=lambda tt, s: s[0] - s[4], rtol=1e-11, atol=1e-11)
    te = s8.t_events[0][0]
    ye = s8.y_events[0][0]
    check(f"s08b k={kv}：飛鏢追上猴子時兩者高度差", ye[1] - ye[5], 0.0, tol=1e-6)

# ---- s09a：最高點早於一半時間 ----
for kv in (0.005, 0.01, 0.02):
    T = brentq(lambda T: T - (kv * V35 + g) / (g * kv) * (1 - math.exp(-kv * T)), 1e-3, 500)
    ttop = math.log(1 + kv * V35 / g) / kv
    truth(f"s09a k={kv}: t_top={ttop:.2f} s < T/2={T / 2:.2f} s", ttop < T / 2)
check("s09a k=0.005 的 t_top、T/2", [math.log(1 + 0.005 * V35 / g) / 0.005, 98.062 / 2], [47.03, 49.03], tol=0.01)
kq, Vq = sp.symbols("k V", positive=True)
ttop_s = sp.series(sp.log(1 + kq * Vq / gg) / kq, kq, 0, 2).removeO()
zero("s09a t_top ≈ (V/g)(1 - kV/2g)", sp.expand(ttop_s - Vq / gg * (1 - kq * Vq / (2 * gg))))

# ---- s09b：最佳仰角 ----
def range_lin(deg, kv, vv=50.0):
    a_ = math.radians(deg)
    U_, V_ = vv * math.cos(a_), vv * math.sin(a_)
    T = brentq(lambda T: T - (kv * V_ + g) / (g * kv) * (1 - math.exp(-kv * T)), 1e-6, 1000)
    return U_ / kv * (1 - math.exp(-kv * T))


for kv in (0.002, 0.01):
    best9 = minimize_scalar(lambda a: -range_lin(a, kv), bounds=(30, 50), method="bounded", options={"xatol": 1e-8}).x
    pred = 45 - math.degrees(kv * 50 / (3 * math.sqrt(2) * g))
    check(f"s09b k={kv}: 數值最佳角 vs 45° - kv0/(3√2 g)", best9, pred, tol=0.03)
check("s09b k=0.01, v0=50 的預測角 (°)", 45 - math.degrees(0.01 * 50 / (3 * math.sqrt(2) * g)), 44.31, tol=0.005)

# ---- s10a：吊 Atwood 機的秤 ----
M1_, M2_ = sp.symbols("m_1 m_2", positive=True)
Tt = 2 * M1_ * M2_ * gg / (M1_ + M2_)
zero("s10a (m1+m2)g - 2T = (m1+m2)·a_cm", (M1_ + M2_) * gg - 2 * Tt - (M1_ - M2_) ** 2 * gg / (M1_ + M2_))
check("s10a m1=3, m2=1：讀數 (N) 與總重 (N)", [4 * 3 * 1 * g / 4, 4 * g], [29.4, 39.2], tol=1e-9)

# ---- s10b：E×B 中由靜止出發 ----
E_, B_, w_ = sp.symbols("E B omega", positive=True)
X10 = E_ / B_ * (t - sp.sin(w_ * t) / w_)
Y10 = E_ / (B_ * w_) * (1 - sp.cos(w_ * t))
zero("s10b ẍ = ω ẏ", X10.diff(t, 2) - w_ * Y10.diff(t))
zero("s10b ÿ = ω(E/B) - ω ẋ", Y10.diff(t, 2) - w_ * E_ / B_ + w_ * X10.diff(t))
zero("s10b ½mv² = qE y（以 m=qB/ω 代）", sp.Rational(1, 2) * (X10.diff(t) ** 2 + Y10.diff(t) ** 2) - (E_ * w_ / B_) * Y10)
qp, mp = 1.602e-19, 1.673e-27
wp = qp * 0.01 / mp
check("s10b 質子 E=1000 V/m、B=0.01 T：ω, y_max (m), v_max (m/s)", [wp, 2 * 1e5 / wp, 2e5], [9.576e5, 0.2089, 2e5], tol=0.002, rel=True)

# ---- s11a：穿洞拉繩 ----
r_, r0_, vv0_ = sp.symbols("r r_0 v_0", positive=True)
Ften = m * vv0_**2 * r0_**2 / r_**3
W11 = sp.integrate(Ften, (r_, sp.Symbol("r_1", positive=True), r0_))
r1 = sp.Symbol("r_1", positive=True)
zero("s11a 拉力做功 = ΔT", W11 - (sp.Rational(1, 2) * m * (vv0_ * r0_ / r1) ** 2 - sp.Rational(1, 2) * m * vv0_**2))
check("s11a m=0.2, v0=1, 0.5→0.25 m：v、W", [1 * 0.5 / 0.25, 0.5 * 0.2 * (4 - 1)], [2.0, 0.3], tol=1e-12)

# ---- s11b：三球疊落 ----
def elastic(ma, va, mb, vb):
    return ((ma - mb) * va + 2 * mb * vb) / (ma + mb), ((mb - ma) * vb + 2 * ma * va) / (ma + mb)


ms = [1.0, 1e-6, 1e-12]
vb = 1.0  # 最下面的球剛反彈（向上 +1），上面兩顆仍向下 -1
v2_, _ = elastic(ms[1], -1.0, ms[0], vb)
v3_, _ = elastic(ms[2], -1.0, ms[1], v2_)
check("s11b 質量比很懸殊時：中球 3v、上球 7v、高度 49h", [v2_, v3_, v3_**2], [3, 7, 49], tol=0.001, rel=True)

# ---- s12a：從桌面滑下的鏈條 ----
Lc, ac = 2.0, 0.5
vend = math.sqrt(g * (Lc**2 - ac**2) / Lc)
tend = math.sqrt(Lc / g) * math.acosh(Lc / ac)
check("s12a 離開桌面的速率 (m/s)、時間 (s)", [vend, tend], [4.287, 0.932], tol=0.001)
s12 = solve_ivp(lambda tt, s: [s[1], g * s[0] / Lc], [0, 2], [ac, 0], events=lambda tt, s: s[0] - Lc, rtol=1e-11, atol=1e-11)
check("s12a 數值積分 ẍ = gx/L：時間、速率", [s12.t_events[0][0], s12.y_events[0][0][1]], [0.932, 4.287], tol=0.001)

# ---- s12b：輸送帶 ----
mb_, ub, mub = 10, 2.0, 0.5
db = ub**2 / (2 * mub * g)
dbelt = ub * ub / (mub * g)
check("s12b 箱子滑行距離、皮帶移動距離 (m)", [db, dbelt], [0.408, 0.816], tol=0.001)
check("s12b 馬達做功、箱子動能、生熱 (J)", [mub * mb_ * g * dbelt, 0.5 * mb_ * ub**2, mub * mb_ * g * (dbelt - db)], [40, 20, 20], tol=1e-9)
check("s12b 皮帶座標系：箱子動能損失 = 生熱 (J)", 0.5 * mb_ * ub**2, 20, tol=1e-9)

# ---- s13a：旋度為零但環路積分 2π ----
xr, yr = sp.symbols("x y", real=True)
Fx, Fy = -yr / (xr**2 + yr**2), xr / (xr**2 + yr**2)
zero("s13a ∂Fy/∂x - ∂Fx/∂y = 0（原點以外）", sp.diff(Fy, xr) - sp.diff(Fx, yr))
thc = sp.Symbol("theta", real=True)
loop = sp.integrate((Fx * (-sp.sin(thc)) + Fy * sp.cos(thc)).subs({xr: sp.cos(thc), yr: sp.sin(thc)}), (thc, 0, 2 * sp.pi))
zero("s13a 繞單位圓一圈 = 2π", loop - 2 * sp.pi)
loop2 = sp.integrate((Fx * (-sp.sin(thc)) + Fy * sp.cos(thc)).subs({xr: 3 + sp.cos(thc), yr: sp.sin(thc)}), (thc, 0, 2 * sp.pi))
check("s13a 不包含原點的圓（圓心 (3,0)）環路積分", float(loop2), 0.0, tol=1e-9)

# ---- s13b：被拖著走的彈簧 ----
xf = sp.Function("x")(t)
vh = sp.Symbol("v", positive=True)
Uh = sp.Rational(1, 2) * k * (xf - vh * t) ** 2
E13 = sp.Rational(1, 2) * m * xf.diff(t) ** 2 + Uh
eom = {xf.diff(t, 2): -k * (xf - vh * t) / m}
zero("s13b dE/dt = ∂U/∂t = -kv(x-vt)", E13.diff(t).subs(eom) - (-k * vh * (xf - vh * t)))
Ep = sp.Rational(1, 2) * m * (xf.diff(t) - vh) ** 2 + Uh
zero("s13b 跟著手走的座標系中 E' 守恆", Ep.diff(t).subs(eom))

# ---- s14a：從球頂滑下 ----
cth = sp.Symbol("c")
sol = sp.solve(sp.Eq(gg * R * cth, 2 * gg * R * (1 - cth)), cth)
zero("s14a 離開時 cosθ = 2/3", sol[0] - sp.Rational(2, 3))
check("s14a 離開時的角度 (°)", math.degrees(math.acos(2 / 3)), 48.19, tol=0.01)
s14 = solve_ivp(lambda tt, s: [s[1], g / 1.0 * math.sin(s[0])], [0, 10], [1e-6, 0], events=lambda tt, s: g * math.cos(s[0]) - 1.0 * s[1] ** 2, rtol=1e-11, atol=1e-13)
check("s14a 數值積分：N=0 時的 cosθ", math.cos(s14.y_events[0][0][0]), 2 / 3, tol=1e-5)

# ---- s14b：迴圈 6mg ----
vtop = sp.Symbol("v_t", positive=True)
Nt = m * vtop**2 / R - m * gg
Nb = m * (vtop**2 + 4 * gg * R) / R + m * gg
zero("s14b N_bottom - N_top = 6mg", Nb - Nt - 6 * m * gg)
hmin = sp.solve(sp.Eq(2 * gg * (sp.Symbol("h") - 2 * R), gg * R), sp.Symbol("h"))[0]
zero("s14b 完成迴圈的最低高度 5R/2", hmin - sp.Rational(5, 2) * R)

# ---- s15a：Lennard-Jones ----
eps, sig, rr = sp.symbols("epsilon sigma r", positive=True)
ULJ = 4 * eps * ((sig / rr) ** 12 - (sig / rr) ** 6)
r0 = 2 ** sp.Rational(1, 6) * sig
zero("s15a U'(r0) = 0", sp.diff(ULJ, rr).subs(rr, r0))
zero("s15a U(r0) = -ε", ULJ.subs(rr, r0) + eps)
zero("s15a U''(r0) = 72ε/(2^{1/3}σ²)", sp.diff(ULJ, rr, 2).subs(rr, r0) - 72 * eps / (2 ** sp.Rational(1, 3) * sig**2))
kLJ = 72 * 1.65e-21 / (2 ** (1 / 3) * (3.4e-10) ** 2)
mAr = 39.95 * 1.6605e-27
check("s15a 氬 r0 (nm)、m (kg)", [2 ** (1 / 6) * 0.34, mAr], [0.3816, 6.634e-26], tol=0.001, rel=True)
check("s15a 氬：k (N/m)、ω (rad/s)、f (Hz)", [kLJ, math.sqrt(kLJ / mAr), math.sqrt(kLJ / mAr) / (2 * math.pi)], [0.816, 3.51e12, 5.58e11], tol=0.01, rel=True)

# ---- s15b：彈簧拉著的珠子 ----
dd, l0 = sp.symbols("d l_0", positive=True)
U15 = sp.Rational(1, 2) * k * (sp.sqrt(xs**2 + dd**2) - l0) ** 2
zero("s15b U''(0) = k(1 - l0/d)", sp.diff(U15, xs, 2).subs(xs, 0) - k * (1 - l0 / dd))
xstar = sp.sqrt(l0**2 - dd**2)
zero("s15b U'(±√(l0²-d²)) = 0", sp.diff(U15, xs).subs(xs, xstar))
zero("s15b U''(x*) = k(l0²-d²)/l0²", sp.simplify(sp.diff(U15, xs, 2).subs(xs, xstar) - k * (l0**2 - dd**2) / l0**2))
zero("s15b d = l0 時 U 的四階導數 = 3k/d²", sp.diff(U15.subs(l0, dd), xs, 4).subs(xs, 0) - 3 * k / dd**2)
zero("s15b 山丘高度 ½k(l0-d)²、谷底 0", U15.subs(xs, 0) - sp.Rational(1, 2) * k * (dd - l0) ** 2 + U15.subs(xs, xstar))
zero("s15b d = l0 時 U ≈ k x⁴/(8d²)", sp.series(U15.subs(l0, dd), xs, 0, 5).removeO() - k * xs**4 / (8 * dd**2))

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
