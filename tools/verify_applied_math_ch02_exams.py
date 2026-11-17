"""應用數學 第 2 章：考古題盤點後新增的題目卡（108級、109級考古題）用 sympy 獨立驗算。

用法：python tools/verify_applied_math_ch02_exams.py     全部通過時結束碼為 0。
"""
import sys

import sympy as sp

x, t = sp.symbols("x t", real=True)
A, B, k, w = sp.symbols("A B k omega", real=True)
results = []


def ok(name, cond):
    results.append((name, bool(cond)))


def z(e):
    return sp.simplify(sp.expand(e)) == 0


# 109級下 第1次期中 3(a)：3y''+2y'-8y=0，y(0)=-6、y'(0)=-18
y = -9 * sp.exp(sp.Rational(4, 3) * t) + 3 * sp.exp(-2 * t)
ok("3(a) 代回", z(3 * y.diff(t, 2) + 2 * y.diff(t) - 8 * y))
ok("3(a) y(0)=-6", y.subs(t, 0) == -6)
ok("3(a) y'(0)=-18", y.diff(t).subs(t, 0) == -18)
lam = sp.symbols("lam")
ok("3(a) 特徵根 4/3、-2", set(sp.solve(3 * lam**2 + 2 * lam - 8, lam)) == {sp.Rational(4, 3), -2})

# 3(b)：y''-8y'+17y=0，y(0)=-4、y'(0)=-1
y = sp.exp(4 * t) * (-4 * sp.cos(t) + 15 * sp.sin(t))
ok("3(b) 代回", z(y.diff(t, 2) - 8 * y.diff(t) + 17 * y))
ok("3(b) y(0)=-4", y.subs(t, 0) == -4)
ok("3(b) y'(0)=-1", y.diff(t).subs(t, 0) == -1)

# 3(c)：y''+14y'+49y=0，y(0)=1、y'(0)=0
y = (1 + 7 * t) * sp.exp(-7 * t)
ok("3(c) 代回", z(y.diff(t, 2) + 14 * y.diff(t) + 49 * y))
ok("3(c) y(0)=1", y.subs(t, 0) == 1)
ok("3(c) y'(0)=0", y.diff(t).subs(t, 0) == 0)

# 108級下 ODE2_FS 1(a)：y''-4y'+13y=0，y(0)=-1、y'(0)=2
y = sp.exp(2 * x) * (-sp.cos(3 * x) + sp.Rational(4, 3) * sp.sin(3 * x))
ok("108 1(a) 代回", z(y.diff(x, 2) - 4 * y.diff(x) + 13 * y))
ok("108 1(a) y(0)=-1", y.subs(x, 0) == -1)
ok("108 1(a) y'(0)=2", y.diff(x).subs(x, 0) == 2)

# 108級上 Calculus 4：x = A cos kt + B sin kt 滿足 x'' + k^2 x = 0
X = A * sp.cos(k * t) + B * sp.sin(k * t)
ok("108 C4 x''+k^2x=0", z(X.diff(t, 2) + k**2 * X))

# 108級上 Calculus 5（＝109級上 第1次期中 4）：y = e^x(cos x + sin x)
y = sp.exp(x) * (sp.cos(x) + sp.sin(x))
ok("108 C5 y''-2y'+2y=0", z(y.diff(x, 2) - 2 * y.diff(x) + 2 * y))
ok("108 C5 y' = 2e^x cos x", z(y.diff(x) - 2 * sp.exp(x) * sp.cos(x)))
ok("108 C5 y'' = 2e^x(cos x - sin x)", z(y.diff(x, 2) - 2 * sp.exp(x) * (sp.cos(x) - sp.sin(x))))

# 108級上 Calculus 6：x = e^t cos ωt 滿足 x''-2x'+10x=0 → ω = ±3
X = sp.exp(t) * sp.cos(w * t)
res = sp.simplify((X.diff(t, 2) - 2 * X.diff(t) + 10 * X) / sp.exp(t))
ok("108 C6 殘差 = (9-ω^2) cos ωt", z(res - (9 - w**2) * sp.cos(w * t)))
ok("108 C6 ω = ±3", set(sp.solve(9 - w**2, w)) == {-3, 3})

bad = [n for n, c in results if not c]
for n, c in results:
    print(("PASS " if c else "FAIL ") + n)
print(f"{len(results) - len(bad)}/{len(results)} passed")
sys.exit(1 if bad else 0)
