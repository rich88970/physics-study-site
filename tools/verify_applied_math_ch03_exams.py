"""應用數學 第 3 章：考古題盤點後新增的題目卡（108級考古題）用 sympy 獨立驗算。

用法：python tools/verify_applied_math_ch03_exams.py     全部通過時結束碼為 0。
"""
import sys

import sympy as sp

x, t = sp.symbols("x t", real=True)
results = []


def ok(name, cond):
    results.append((name, bool(cond)))


def z(e):
    e = sp.simplify(sp.expand(e))
    if e == 0:
        return True
    return sp.simplify(sp.trigsimp(sp.expand_trig(e))) == 0


# 108級下 ODE2_FS 1(b)：y''+y'-2y=4 sin 2x，y(0)=-4/5、y'(0)=0
y = -sp.Rational(3, 5) * sp.exp(-2 * x) - sp.Rational(1, 5) * sp.cos(2 * x) - sp.Rational(3, 5) * sp.sin(2 * x)
ok("1(b) 代回", z(y.diff(x, 2) + y.diff(x) - 2 * y - 4 * sp.sin(2 * x)))
ok("1(b) y(0)=-4/5", y.subs(x, 0) == -sp.Rational(4, 5))
ok("1(b) y'(0)=0", y.diff(x).subs(x, 0) == 0)
K1, K2 = sp.symbols("K1 K2")
yp = K1 * sp.cos(2 * x) + K2 * sp.sin(2 * x)
r = sp.expand(yp.diff(x, 2) + yp.diff(x) - 2 * yp - 4 * sp.sin(2 * x))
s = sp.solve([r.coeff(sp.cos(2 * x)), r.coeff(sp.sin(2 * x))], [K1, K2])
ok("1(b) K1=-1/5、K2=-3/5", s == {K1: -sp.Rational(1, 5), K2: -sp.Rational(3, 5)})

# 108級下 ODE2_FS 1(c)：y''-2y'+5y=8e^x sin 2x，y(0)=0、y(π/4)=1
y = sp.exp(-sp.pi / 4) * sp.exp(x) * sp.sin(2 * x) - 2 * x * sp.exp(x) * sp.cos(2 * x)
ok("1(c) 代回", z(y.diff(x, 2) - 2 * y.diff(x) + 5 * y - 8 * sp.exp(x) * sp.sin(2 * x)))
ok("1(c) y(0)=0", sp.simplify(y.subs(x, 0)) == 0)
ok("1(c) y(π/4)=1", sp.simplify(y.subs(x, sp.pi / 4)) == 1)
yp = x * sp.exp(x) * (K1 * sp.cos(2 * x) + K2 * sp.sin(2 * x))
r = sp.expand(sp.simplify((yp.diff(x, 2) - 2 * yp.diff(x) + 5 * yp - 8 * sp.exp(x) * sp.sin(2 * x)) / sp.exp(x)))
s = sp.solve([r.coeff(sp.cos(2 * x)), r.coeff(sp.sin(2 * x))], [K1, K2])
ok("1(c) 修正後 K1=-2、K2=0", s == {K1: -2, K2: 0})

# 108級下 ODE2_FS 2：L q'' + R q' + q/C = V0 sin ωt 的穩態
L, R, C, V0, w = sp.symbols("L R C V_0 omega", positive=True)
X = w * L - 1 / (w * C)
Z2 = X**2 + R**2
q = -R * V0 / (w * Z2) * sp.cos(w * t) - X * V0 / (w * Z2) * sp.sin(w * t)
ok("2 穩態 q 代回", z(L * q.diff(t, 2) + R * q.diff(t) + q / C - V0 * sp.sin(w * t)))
i = q.diff(t)
ok("2 電流 i = V0/Z^2 (R sin ωt − X cos ωt)", z(i - V0 / Z2 * (R * sp.sin(w * t) - X * sp.cos(w * t))))

# 108級上 ExpCmplx 5：x'' + γ x' + ω0^2 x = Fd sin ωd t
g, w0, Fd, wd = sp.symbols("gamma omega_0 F_d omega_d", positive=True)
D = (w0**2 - wd**2)**2 + g**2 * wd**2
Kc = -g * wd * Fd / D
Ks = (w0**2 - wd**2) * Fd / D
xp = Kc * sp.cos(wd * t) + Ks * sp.sin(wd * t)
ok("E5 K1、K2 代回", z(xp.diff(t, 2) + g * xp.diff(t) + w0**2 * xp - Fd * sp.sin(wd * t)))
Aamp = Fd / sp.sqrt(D)
ok("E5 A^2 = K1^2 + K2^2", z(Kc**2 + Ks**2 - Aamp**2))
# 峰值位置 ωr^2 = ω0^2 − γ^2/2
u = sp.symbols("u", positive=True)
Du = (w0**2 - u)**2 + g**2 * u
ok("E5 dD/d(ωd^2)=0 → ωr^2 = ω0^2 − γ^2/2", sp.solve(sp.diff(Du, u), u) == [w0**2 - g**2 / 2])
Amax = sp.simplify(Fd / sp.sqrt(Du.subs(u, w0**2 - g**2 / 2)))
ok("E5 A_max = Fd/(γ sqrt(ω0^2 − γ^2/4))", z(Amax**2 - Fd**2 / (g**2 * (w0**2 - g**2 / 4))))
# 數值例：ω0=1、Fd=1、γ=0.2, 0.5, 1
for gv in (0.2, 0.5, 1.0):
    wr = (1 - gv**2 / 2) ** 0.5
    am = 1 / (gv * (1 - gv**2 / 4) ** 0.5)
    num = float(Aamp.subs({w0: 1, Fd: 1, g: gv, wd: wr}))
    ok(f"E5 數值 γ={gv}: ωr={wr:.4f}, Amax={am:.4f}", abs(num - am) < 1e-9)

bad = [n for n, c in results if not c]
for n, c in results:
    print(("PASS " if c else "FAIL ") + n)
print(f"{len(results) - len(bad)}/{len(results)} passed")
sys.exit(1 if bad else 0)
