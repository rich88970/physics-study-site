"""力學 Lecture 2：考古題卡的獨立驗算。

用法：python -X utf8 tools/verify_mechanics_ch02_exams.py（需要 numpy、scipy、sympy）
c2-exam4-1：Exam-4（2025/12/18）第 1 題，爆炸成三塊（動量守恆＋動能差）
c2-exam4-3：Exam-4 第 3 題，從光滑桌面滑下的繩子（x(t) 與離開桌面時的速率）
c2-exam5-2：Chapter-05（2025/05/22）第 2 題，kr^n 與 T^2 ∝ r^3 ⟹ n = -2
c2-exam8-1：Chapter-08（2025/06/12）第 1 題，連心力 ⟹ 掃面積速率不變（數值軌道＋反例）
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ok = True


def check(name, got, want, tol=1e-6):
    global ok
    good = np.allclose(np.array(got, dtype=float), np.array(want, dtype=float), rtol=tol, atol=tol)
    ok &= bool(good)
    print(("OK  " if good else "FAIL"), name, np.round(np.array(got, dtype=float), 6).tolist(), "expected", want)


def zero(name, expr):
    global ok
    z = sp.simplify(expr)
    good = z == 0
    ok &= bool(good)
    print(("OK  " if good else "FAIL"), name, "" if good else z)


# ---------- c2-exam4-1：爆炸 ----------
M, v, v2 = sp.symbols('M v v2', real=True)
m1, m2, m3 = M / 2, M / 6, M / 3
zero("exam4-1 質量和 = M", m1 + m2 + m3 - M)
sol = sp.solve(sp.Eq(M * v, m1 * 4 * v + m2 * v2 + m3 * 0), v2)[0]
zero("exam4-1 v2 = -6v", sol + 6 * v)
Ti = sp.Rational(1, 2) * M * v**2
Tf = sp.Rational(1, 2) * m1 * (4 * v)**2 + sp.Rational(1, 2) * m2 * sol**2
zero("exam4-1 T_f = 7Mv^2", Tf - 7 * M * v**2)
Q = sp.simplify(Tf - Ti)
zero("exam4-1 Q = 13/2 Mv^2", Q - sp.Rational(13, 2) * M * v**2)
zero("exam4-1 Q / T_i = 13", Q / Ti - 13)
# 質心速度不變、質心系動能＝釋放的能量
vcm = (m1 * 4 * v + m2 * sol) / M
zero("exam4-1 質心速度仍為 v", vcm - v)
Tcm = sp.Rational(1, 2) * (m1 * (4 * v - v)**2 + m2 * (sol - v)**2 + m3 * (0 - v)**2)
zero("exam4-1 質心系動能 = Q", Tcm - Q)

# ---------- c2-exam4-3：繩子滑下桌 ----------
t, L, g, x0 = sp.symbols('t L g x0', positive=True)
k = sp.sqrt(g / L)
x = x0 * sp.cosh(k * t)
zero("exam4-3 滿足 x'' = (g/L) x", sp.diff(x, t, 2) - g / L * x)
zero("exam4-3 x(0) = x0", x.subs(t, 0) - x0)
zero("exam4-3 x'(0) = 0", sp.diff(x, t).subs(t, 0))
# 離開時 cosh(kt) = L/x0 ⟹ sinh = sqrt(L^2/x0^2 - 1)
sinh_end = sp.sqrt((L / x0)**2 - 1)
vend = x0 * k * sinh_end
zero("exam4-3 由 x(t) 得 v_end^2 = g(L^2-x0^2)/L", sp.simplify(vend**2 - g * (L**2 - x0**2) / L))
# 能量法：重力對垂下部分做功 ∫ (M/L) g x dx = 1/2 M v^2
Ms, xs = sp.symbols('M_s x_s', positive=True)
W = sp.integrate(Ms / L * g * xs, (xs, x0, L))
zero("exam4-3 功能定理給同一個 v^2", sp.solve(sp.Eq(W, Ms * sp.Symbol('V')**2 / 2), sp.Symbol('V'))[0]**2 - g * (L**2 - x0**2) / L)

# 數值：L = 2 m、x0 = 0.5 m、g = 9.8（和自編難題 c2-self-12a 同數據）直接積分 ODE
Ln, x0n, gn = 2.0, 0.5, 9.8
ev = lambda tt, y: y[0] - Ln
ev.terminal = True
r = solve_ivp(lambda tt, y: [y[1], gn / Ln * y[0]], [0, 5], [x0n, 0.0], events=ev, rtol=1e-11, atol=1e-12)
t_end = r.t_events[0][0]
v_end = r.y_events[0][0][1]
check("exam4-3 數值 t_end = sqrt(L/g) arccosh(L/x0)", t_end, np.sqrt(Ln / gn) * np.arccosh(Ln / x0n))
check("exam4-3 數值 v_end = sqrt(g(L^2-x0^2)/L)", v_end, np.sqrt(gn * (Ln**2 - x0n**2) / Ln))
check("exam4-3 數值 v_end ≈ 4.29 m/s、t_end ≈ 0.932 s", [round(v_end, 2), round(t_end, 3)], [4.29, 0.932])

# ---------- c2-exam5-2：kr^n 與 T^2 ∝ r^3 ----------
r, m, kk, n = sp.symbols('r m k n', positive=True)
nn = sp.Symbol('n', real=True)
Tsq = sp.solve(sp.Eq(kk * r**nn, m * (2 * sp.pi * r / sp.Symbol('T', positive=True))**2 / r), sp.Symbol('T', positive=True))[0]**2
zero("exam5-2 T^2 = 4π^2 m/|k| · r^(1-n)", sp.simplify(Tsq - 4 * sp.pi**2 * m / kk * r**(1 - nn)))
check("exam5-2 1-n = 3 ⟹ n = -2", float(sp.solve(sp.Eq(1 - nn, 3), nn)[0]), -2)
G, Me = sp.symbols('G M_e', positive=True)
zero("exam5-2 n=-2、|k|=GMm ⟹ 克卜勒第三定律", sp.simplify(Tsq.subs({nn: -2, kk: G * Me * m}) - 4 * sp.pi**2 * r**3 / (G * Me)))
# 數值：n=-2 時兩個半徑的 T^2/r^3 相同；n=1 時 T 與 r 無關
for nv, name in [(-2, "n=-2 時 T^2/r^3 與 r 無關"), (1, "n=1 時 T 與 r 無關")]:
    Tf = sp.lambdify(r, sp.sqrt(Tsq.subs({nn: nv, kk: 3.0, m: 2.0})))
    if nv == -2:
        check("exam5-2 " + name, Tf(1.0)**2 / 1.0**3, Tf(4.0)**2 / 4.0**3)
    else:
        check("exam5-2 " + name, Tf(1.0), Tf(4.0))

# ---------- c2-exam8-1：連心力 ⟹ dA/dt 為常數 ----------
x_, y_, z_, f_ = sp.symbols('x y z f', real=True)
rv = sp.Matrix([x_, y_, z_])
zero("exam8-1 r × (f r) = 0", (rv.cross(f_ * rv)).norm())
# 數值：任意連心力 F(r) = -1/r^2 - 0.5/r^4 + 0.3 r（非平方反比）積分軌道，dA/dt = |r×v|/2 應不變
def rhs(tt, s, tang=0.0):
    px, py, vx, vy = s
    rr = np.hypot(px, py)
    Fr = -1 / rr**2 - 0.5 / rr**4 + 0.3 * rr
    ax = Fr * px / rr - tang * py / rr
    ay = Fr * py / rr + tang * px / rr
    return [vx, vy, ax, ay]
sol = solve_ivp(rhs, [0, 20], [1.5, 0.0, 0.0, 0.9], rtol=1e-11, atol=1e-12, dense_output=True)
ts = np.linspace(0, 20, 400)
P = sol.sol(ts)
areal = 0.5 * (P[0] * P[3] - P[1] * P[2])
print("    dA/dt0 =", areal[0], "max dev =", float(np.max(np.abs(areal - areal[0]))))
check("exam8-1 連心力：dA/dt 的最大相對偏差 < 1e-6", float(np.max(np.abs(areal - areal[0])) / abs(areal[0])) < 1e-6, 1)
sol2 = solve_ivp(lambda tt, s: rhs(tt, s, tang=0.2), [0, 5], [1.5, 0.0, 0.0, 0.9], rtol=1e-11, atol=1e-12, dense_output=True)
P2 = sol2.sol(np.linspace(0, 5, 100))
areal2 = 0.5 * (P2[0] * P2[3] - P2[1] * P2[2])
changed = float(np.max(np.abs(areal2 - areal2[0])))
ok &= changed > 1e-2
print(("OK  " if changed > 1e-2 else "FAIL"), "exam8-1 反例：加切向力 0.2 θ̂ 時 dA/dt 會變", round(changed, 4))

print("ALL OK" if ok else "SOME FAILED")
raise SystemExit(0 if ok else 1)
