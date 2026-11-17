"""驗算應用數學第 3 章「考試書寫版」（exam.html）改寫後出現的所有中間值與答案。

用法：python tools/verify_writeup_applied-math_ch03.py   全部通過時結束碼 0。
"""
import math
import sys

import sympy as sp

x, t, lam = sp.symbols("x t lambda")
fails = []


def check(name, cond):
    ok = bool(cond)
    print(("OK  " if ok else "FAIL") + "  " + name)
    if not ok:
        fails.append(name)


def zero(e):
    return sp.simplify(e) == 0


def L(y, a, b, var=x):
    return sp.diff(y, var, 2) + a * sp.diff(y, var) + b * y


def ic(y, y0, dy0, at=0, var=x):
    return zero(y.subs(var, at) - y0) and zero(sp.diff(y, var).subs(var, at) - dy0)


def near(a, b, tol=5e-4):
    return abs(float(a) - float(b)) < tol


R = sp.Rational
K0, K1, K2, A, B, C, D, c1, c2 = sp.symbols("K0 K1 K2 A B C D c1 c2")

# a3-b1、a3-s01-1（同一個 y_p）
yp = -3 + 2 * x - 2 * x**2
check("a3-b1 比較係數方程組", sp.solve([-2 * K2 - 4, -2 * K2 - 2 * K1, 2 * K2 - K1 - 2 * K0], [K0, K1, K2]) == {K2: -2, K1: 2, K0: -3})
check("a3-b1 y_p 滿足方程", zero(L(yp, -1, -2) - 4 * x**2))
check("a3-b1 c1+c2=4、-c1+2c2=-1 → c2=1、c1=3", sp.solve([c1 + c2 - 4, -c1 + 2 * c2 + 1], [c1, c2]) == {c1: 3, c2: 1})
y = 3 * sp.exp(-x) + sp.exp(2 * x) + yp
check("a3-b1 解", zero(L(y, -1, -2) - 4 * x**2) and ic(y, 1, 1))
be = sp.symbols("beta")
cc1, cc2 = -(be - 2) / 3, (be - 2) / 3
y = cc1 * sp.exp(-x) + cc2 * sp.exp(2 * x) + yp
check("a3-s01-1 (a) c1,c2 滿足 y(0)=-3、y'(0)=β", zero(L(y, -1, -2) - 4 * x**2) and ic(y, -3, be))
check("a3-s01-1 (b) β=2 → y=-2x^2+2x-3", zero(y.subs(be, 2) - (-2 * x**2 + 2 * x - 3)))

# a3-111a-m3
check("a3-111a-m3 y_p=x", zero(L(x, -2, 2) - 2 * (x - 1)))
yg = sp.exp(x) * (c1 * sp.cos(x) + c2 * sp.sin(x)) + x
check("a3-111a-m3 y' 展開式", zero(sp.diff(yg, x) - (sp.exp(x) * ((c1 + c2) * sp.cos(x) + (c2 - c1) * sp.sin(x)) + 1)))
check("a3-111a-m3 解 y=x", ic(x, 0, 1))

# a3-114a-m3
check("a3-114a-m3 A=1、B=0", sp.solve([-9 * A + 2 * B + 9, -2 * A - 9 * B + 2], [A, B]) == {A: 1, B: 0})
y = sp.exp(2 * x) + 2 * sp.exp(-4 * x) + sp.cos(x)
check("a3-114a-m3 解", zero(L(y, 2, -8) - (-9 * sp.cos(x) - 2 * sp.sin(x))) and ic(y, 4, -6))

# a3-s01-2
a_, b_ = sp.symbols("a b")
ypp = sp.cos(x) + 3 * sp.sin(x)
lhs = sp.expand(L(ypp, a_, b_))
check("a3-s01-2 (a) cos 係數 -1+3a+b、sin 係數 -3-a+3b", zero(lhs.coeff(sp.cos(x)) - (-1 + 3 * a_ + b_)) and zero(lhs.coeff(sp.sin(x)) - (-3 - a_ + 3 * b_)))
check("a3-s01-2 (a) a=3、b=2", sp.solve([-1 + 3 * a_ + b_ - 10, -3 - a_ + 3 * b_], [a_, b_]) == {a_: 3, b_: 2})
y = -5 * sp.exp(-x) + 4 * sp.exp(-2 * x) + ypp
check("a3-s01-2 (b) 解", zero(L(y, 3, 2) - 10 * sp.cos(x)) and ic(y, 0, 0))

# a3-108b-1b
check("a3-108b-1b K1=-1/5、K2=-3/5", sp.solve([-6 * K1 + 2 * K2, -2 * K1 - 6 * K2 - 4], [K1, K2]) == {K1: R(-1, 5), K2: R(-3, 5)})
y = -R(3, 5) * sp.exp(-2 * x) - R(1, 5) * sp.cos(2 * x) - R(3, 5) * sp.sin(2 * x)
check("a3-108b-1b 解（c1=0）", zero(L(y, 1, -2) - 4 * sp.sin(2 * x)) and ic(y, R(-4, 5), 0))

# a3-b2
check("a3-b2 K2=1、K1=-2、K0=3/2", sp.solve([4 * K2 - 4, 8 * K2 + 4 * K1, 2 * K2 + 4 * K1 + 4 * K0], [K0, K1, K2]) == {K2: 1, K1: -2, K0: R(3, 2)})
yp = x**2 - 2 * x + R(3, 2) + R(2, 3) * sp.exp(x)
check("a3-b2 y_p", zero(L(yp, 4, 4) - (4 * x**2 + 6 * sp.exp(x))))

# a3-hw1
check("a3-hw1 y_p1=-cos x/2", zero(L(-sp.cos(x) / 2, 2, 1) - sp.sin(x)))
check("a3-hw1 C=-9/25、D=12/25", sp.solve([-3 * C + 4 * D - 3, -3 * D - 4 * C], [C, D]) == {C: R(-9, 25), D: R(12, 25)})
y = R(43, 50) * sp.exp(-x) - R(1, 10) * x * sp.exp(-x) - sp.cos(x) / 2 - R(9, 25) * sp.cos(2 * x) + R(12, 25) * sp.sin(2 * x)
yg = (c1 + c2 * x) * sp.exp(-x) - sp.cos(x) / 2 - R(9, 25) * sp.cos(2 * x) + R(12, 25) * sp.sin(2 * x)
check("a3-hw1 y' 展開式", zero(sp.diff(yg, x) - ((c2 - c1 - c2 * x) * sp.exp(-x) + sp.sin(x) / 2 + R(18, 25) * sp.sin(2 * x) + R(24, 25) * sp.cos(2 * x))))
check("a3-hw1 解", zero(L(y, 2, 1) - (sp.sin(x) + 3 * sp.cos(2 * x))) and ic(y, 0, 0))

# a3-113a-m4
check("a3-113a-m4 多項式塊係數", sp.solve([-8 * K2 - 1, 4 * K2 - 8 * K1 + 2, 2 * K2 + 2 * K1 - 8 * K0 - 1], [K0, K1, K2]) == {K2: R(-1, 8), K1: R(3, 16), K0: R(-7, 64)})
check("a3-113a-m4 2K2+2K1=1/8", 2 * R(-1, 8) + 2 * R(3, 16) == R(1, 8))
yp = -R(1, 8) * x**2 + R(3, 16) * x - R(7, 64) - R(1, 8) * sp.exp(-2 * x) + sp.cos(x)
check("a3-113a-m4 y_p", zero(L(yp, 2, -8) - ((x - 1) ** 2 + sp.exp(-2 * x) - 9 * sp.cos(x) - 2 * sp.sin(x))))

# a3-s02-1、a3-s02-2
y = R(1, 2) - R(2, 3) * sp.cos(x) + R(1, 6) * sp.cos(2 * x)
check("a3-s02-1 解", zero(L(y, 0, 1) - sp.sin(x) ** 2) and ic(y, 0, 0))
check("a3-s02-2 A=1/16、B=1/8", R(1, 2) / 8 == R(1, 16) and R(1, 2) / 4 == R(1, 8))
y = -R(1, 16) * sp.exp(-x) * (3 * sp.cos(2 * x) + sp.sin(2 * x)) + R(1, 16) * sp.exp(x) + R(1, 8) * sp.exp(-x)
check("a3-s02-2 解", zero(L(y, 2, 5) - sp.cosh(x)) and ic(y, 0, 0))

# a3-b3
yp = A * sp.cos(x) + B * sp.sin(x) + C * x * sp.cos(x) + D * x * sp.sin(x)
check("a3-b3 (x cos x)''、(x sin x)''", zero(sp.diff(x * sp.cos(x), x, 2) - (-2 * sp.sin(x) - x * sp.cos(x))) and zero(sp.diff(x * sp.sin(x), x, 2) - (2 * sp.cos(x) - x * sp.sin(x))))
e = sp.expand(L(yp, 0, 9))
check("a3-b3 四組係數 8A+2D、8B-2C、8C、8D", zero(e - ((8 * A + 2 * D) * sp.cos(x) + (8 * B - 2 * C) * sp.sin(x) + 8 * C * x * sp.cos(x) + 8 * D * x * sp.sin(x))))
check("a3-b3 y_p", zero(L(sp.sin(x) / 32 + x * sp.cos(x) / 8, 0, 9) - x * sp.cos(x)))

# 平移公式 y=e^{γx}u
g_ = sp.symbols("gamma")
uf = sp.Function("u")(x)
yy = sp.exp(g_ * x) * uf
check("平移公式 y''=e^{γx}(u''+2γu'+γ^2u)", zero(sp.diff(yy, x, 2) - sp.exp(g_ * x) * (sp.diff(uf, x, 2) + 2 * g_ * sp.diff(uf, x) + g_**2 * uf)))

# a3-hw2
check("a3-hw2 平移後 u''-12u'+20u", zero(sp.simplify(L(sp.exp(-4 * x) * uf, -4, -12) * sp.exp(4 * x)) - (sp.diff(uf, x, 2) - 12 * sp.diff(uf, x) + 20 * uf)))
yp = (R(3, 100) + x / 20) * sp.exp(-4 * x)
check("a3-hw2 y_p", zero(L(yp, -4, -12) - x * sp.exp(-4 * x)))

# a3-112a-m3
check("a3-112a-m3 (1) 根 -1±4i", set(sp.solve(lam**2 + 2 * lam + 17, lam)) == {-1 + 4 * sp.I, -1 - 4 * sp.I})
check("a3-112a-m3 平移後 u''-6u'+25u", zero(sp.simplify(L(sp.exp(-4 * x) * uf, 2, 17) * sp.exp(4 * x)) - (sp.diff(uf, x, 2) - 6 * sp.diff(uf, x) + 25 * uf)))
u = A * sp.cos(5 * x) + B * sp.sin(5 * x)
check("a3-112a-m3 -6u'=30A sin5x-30B cos5x", zero(-6 * sp.diff(u, x) - (30 * A * sp.sin(5 * x) - 30 * B * sp.cos(5 * x))))
yp = 2 * sp.exp(-4 * x) * sp.cos(5 * x)
check("a3-112a-m3 (2) y_p、y_p'(0)=-8", zero(L(yp, 2, 17) - 60 * sp.exp(-4 * x) * sp.sin(5 * x)) and sp.diff(yp, x).subs(x, 0) == -8)
y = sp.exp(-x) * (2 * sp.sin(4 * x) - 2 * sp.cos(4 * x)) + yp
check("a3-112a-m3 (3) 解", zero(L(y, 2, 17) - 60 * sp.exp(-4 * x) * sp.sin(5 * x)) and ic(y, 0, 2))

# a3-s03-1
a, b, c = R(1, 3), -4 * sp.I / 9, R(-14, 27)
u = a * x**2 + b * x + c
check("a3-s03-1 u''+2iu'+3u=x^2", zero(sp.diff(u, x, 2) + 2 * sp.I * sp.diff(u, x) + 3 * u - x**2))
check("a3-s03-1 常數式 2/3+8/9+3c=0", R(2, 3) + R(8, 9) + 3 * c == 0)
check("a3-s03-1 Y''=e^{ix}(u''+2iu'-u)", zero(sp.diff(sp.exp(sp.I * x) * uf, x, 2) - sp.exp(sp.I * x) * (sp.diff(uf, x, 2) + 2 * sp.I * sp.diff(uf, x) - uf)))
yp = (x**2 / 3 - R(14, 27)) * sp.sin(x) - R(4, 9) * x * sp.cos(x)
check("a3-s03-1 y_p=Im(u e^{ix})", zero(sp.im(sp.expand(u * (sp.cos(x) + sp.I * sp.sin(x))).subs(x, sp.Symbol("xr", real=True))).subs(sp.Symbol("xr", real=True), x) - yp))
check("a3-s03-1 y_p 滿足方程", zero(L(yp, 0, 4) - x**2 * sp.sin(x)))

# a3-s03-2
kk = sp.symbols("k")
check("a3-s03-2 平移後 u''+(k-1)u", zero(sp.simplify(L(sp.exp(-x) * uf, 2, kk) * sp.exp(x)) - (sp.diff(uf, x, 2) + (kk - 1) * uf)))
check("a3-s03-2 (a) k=10 時根 -1±3i", set(sp.solve(lam**2 + 2 * lam + 10, lam)) == {-1 + 3 * sp.I, -1 - 3 * sp.I})
check("a3-s03-2 (b) k=5", zero(L(-sp.exp(-x) * sp.cos(3 * x) / 5, 2, 5) - sp.exp(-x) * sp.cos(3 * x)))
check("a3-s03-2 (c) k=10", zero(L(x / 6 * sp.exp(-x) * sp.sin(3 * x), 2, 10) - sp.exp(-x) * sp.cos(3 * x)))
f = A * sp.cos(3 * x) + B * sp.sin(3 * x)
check("a3-s03-2 (c) u''+9u=2f'", zero(sp.diff(x * f, x, 2) + 9 * x * f - 2 * sp.diff(f, x)))

# a3-b4
check("a3-b4 e^{2x}、xe^{2x} 代入得 0", zero(L(sp.exp(2 * x), -4, 4)) and zero(L(x * sp.exp(2 * x), -4, 4)))
check("a3-b4 平移後只剩 u''", zero(sp.simplify(L(sp.exp(2 * x) * uf, -4, 4) * sp.exp(-2 * x)) - sp.diff(uf, x, 2)))
check("a3-b4 y_p=x^2e^{2x}", zero(L(x**2 * sp.exp(2 * x), -4, 4) - 2 * sp.exp(2 * x)))

# a3-hw3
Pp, Qq = A * x**2 + B * x, C * x**2 + D * x
yp = Pp * sp.cos(x) + Qq * sp.sin(x)
check("a3-hw3 恆等式 (P''+2Q')cos+(Q''-2P')sin", zero(L(yp, 0, 1) - ((sp.diff(Pp, x, 2) + 2 * sp.diff(Qq, x)) * sp.cos(x) + (sp.diff(Qq, x, 2) - 2 * sp.diff(Pp, x)) * sp.sin(x))))
check("a3-hw3 展開 (2A+2D+4Cx)cos+(2C-2B-4Ax)sin", zero(L(yp, 0, 1) - ((2 * A + 2 * D + 4 * C * x) * sp.cos(x) + (2 * C - 2 * B - 4 * A * x) * sp.sin(x))))
check("a3-hw3 y_p", zero(L(-x**2 * sp.cos(x) / 2 + x * sp.sin(x) / 2, 0, 1) - 2 * x * sp.sin(x)))

# a3-110a-m4
check("a3-110a-m4 平移後 u''+u", zero(sp.simplify(L(sp.exp(x) * uf, -2, 2) * sp.exp(-x)) - (sp.diff(uf, x, 2) + uf)))
check("a3-110a-m4 y_p=xe^x sin x", zero(L(x * sp.exp(x) * sp.sin(x), -2, 2) - 2 * sp.exp(x) * sp.cos(x)))

# a3-s04-1
check("a3-s04-1 L[xe^{±x}]=±2e^{±x}", zero(L(x * sp.exp(x), 0, -1) - 2 * sp.exp(x)) and zero(L(x * sp.exp(-x), 0, -1) + 2 * sp.exp(-x)))
y = x / 2 * sp.sinh(x)
check("a3-s04-1 解", zero((L(y, 0, -1) - sp.cosh(x)).rewrite(sp.exp)) and ic(y, 0, 0) and zero((x / 4 * (sp.exp(x) - sp.exp(-x)) - y).rewrite(sp.exp)))

# a3-s04-2
check("a3-s04-2 平移後 u''-3u'", zero(sp.simplify(L(sp.exp(-3 * x) * uf, 3, 0) * sp.exp(3 * x)) - (sp.diff(uf, x, 2) - 3 * sp.diff(uf, x))))
y = 1 - sp.exp(-3 * x) + x**2 - 3 * x * sp.exp(-3 * x)
check("a3-s04-2 y' 展開式", zero(sp.diff(y, x) - (3 * sp.exp(-3 * x) + 2 * x - 3 * sp.exp(-3 * x) + 9 * x * sp.exp(-3 * x))))
check("a3-s04-2 解", zero(L(y, 3, 0) - (6 * x + 2 + 9 * sp.exp(-3 * x))) and ic(y, 0, 0))

# a3-108b-1c
check("a3-108b-1c 平移後 u''+4u", zero(sp.simplify(L(sp.exp(x) * uf, -2, 5) * sp.exp(-x)) - (sp.diff(uf, x, 2) + 4 * uf)))
y = sp.exp(-sp.pi / 4) * sp.exp(x) * sp.sin(2 * x) - 2 * x * sp.exp(x) * sp.cos(2 * x)
check("a3-108b-1c 解與邊界", zero(L(y, -2, 5) - 8 * sp.exp(x) * sp.sin(2 * x)) and y.subs(x, 0) == 0 and zero(y.subs(x, sp.pi / 4) - 1))

# a3-b5
g, w0, w, F0 = sp.symbols("gamma omega0 omega F0", positive=True)
Dd = (w0**2 - w**2) ** 2 + 4 * g**2 * w**2
k1, k2 = -2 * g * w * F0 / Dd, (w0**2 - w**2) * F0 / Dd
xp = k1 * sp.cos(w * t) + k2 * sp.sin(w * t)
check("a3-b5 K1,K2", zero(sp.diff(xp, t, 2) + 2 * g * sp.diff(xp, t) + w0**2 * xp - F0 * sp.sin(w * t)))
check("a3-b5 A^2=K1^2+K2^2=F0^2/D", zero(k1**2 + k2**2 - F0**2 / Dd))

# a3-s05-1
s = sp.symbols("s")
Ds = sp.expand((w0**2 - s) ** 2 + 4 * g**2 * s)
check("a3-s05-1 D(s) 展開", zero(Ds - (s**2 - 2 * (w0**2 - 2 * g**2) * s + w0**4)))
check("a3-s05-1 頂點與 D_min", zero(sp.solve(sp.diff(Ds, s), s)[0] - (w0**2 - 2 * g**2)) and zero(Ds.subs(s, w0**2 - 2 * g**2) - 4 * g**2 * (w0**2 - g**2)))
Af = lambda om: 5 / math.sqrt((100 - om**2) ** 2 + 4 * om**2)
check("a3-s05-1 (b) ω_r=9.90、A_max=0.2513、A(ω0)=0.25、A(0)=0.05", near(math.sqrt(98), 9.90, 5e-3) and near(Af(math.sqrt(98)), 0.2513, 5e-5) and near(5 / (2 * math.sqrt(99)), 0.2513, 5e-5) and near(Af(10), 0.25, 1e-12) and near(Af(0), 0.05, 1e-12))
check("a3-s05-1 (b) 約 5 倍、差約 0.5%", near(Af(math.sqrt(98)) / Af(0), 5.03, 0.01) and near(Af(math.sqrt(98)) / Af(10) - 1, 0.005, 0.0005))

# a3-s05-2
xx = F0 / (2 * w0**2) * sp.sin(w0 * t) - F0 * t / (2 * w0) * sp.cos(w0 * t)
check("a3-s05-2 (a) 解", zero(sp.diff(xx, t, 2) + w0**2 * xx - F0 * sp.sin(w0 * t)) and xx.subs(t, 0) == 0 and zero(sp.diff(xx, t).subs(t, 0)))
check("a3-s05-2 (b) t=20/ω0=10 s", near(20 / 2, 10, 1e-12))

# a3-108b-2
Lh, Rr, Cc, V0 = sp.symbols("L R C V0", positive=True)
X = w * Lh - 1 / (w * Cc)
Z2 = X**2 + Rr**2
q = -Rr * V0 / (w * Z2) * sp.cos(w * t) - X * V0 / (w * Z2) * sp.sin(w * t)
check("a3-108b-2 1/C-Lω^2=-ωX", zero(1 / Cc - Lh * w**2 + w * X))
check("a3-108b-2 q 滿足電路方程", zero(Lh * sp.diff(q, t, 2) + Rr * sp.diff(q, t) + q / Cc - V0 * sp.sin(w * t)))

# a3-108a-x5（題目是 γẋ，不是 2γẋ）
gd, wd, Fd = sp.symbols("gamma_d omega_d F_d", positive=True)
At = Fd / ((w0**2 - wd**2) + sp.I * gd * wd)
check("a3-108a-x5 (a) |Ã|", zero(sp.Abs(At) - Fd / sp.sqrt((w0**2 - wd**2) ** 2 + gd**2 * wd**2)))
z = At * sp.exp(sp.I * wd * t)
check("a3-108a-x5 (a) z 滿足複數方程", zero(sp.diff(z, t, 2) + gd * sp.diff(z, t) + w0**2 * z - Fd * sp.exp(sp.I * wd * t)))
Ds = (w0**2 - s) ** 2 + gd**2 * s
check("a3-108a-x5 (b) 頂點 s=ω0^2-γ^2/2、D_min=γ^2(ω0^2-γ^2/4)", zero(sp.solve(sp.diff(Ds, s), s)[0] - (w0**2 - gd**2 / 2)) and zero(sp.expand(Ds.subs(s, w0**2 - gd**2 / 2) - gd**2 * (w0**2 - gd**2 / 4))))
# 數值：相位落在 (-π, 0)
for (W0, G, WD) in [(1.0, 0.3, 0.5), (1.0, 0.3, 1.5), (2.0, 1.0, 2.0)]:
    ph = -math.atan2(G * WD, W0**2 - WD**2)
    check(f"a3-108a-x5 φ∈(-π,0)（ω0={W0}, γ={G}, ωd={WD}）", -math.pi < ph < 0)

# a3-s06-1
X_ = sp.symbols("X", positive=True)
W = X_ * (-X_**-2) - X_**-1
check("a3-s06-1 W=-2/x", zero(W + 2 / X_))
u1 = sp.integrate(-(1 / X_) * sp.log(X_) / W, X_)
u2 = sp.integrate(X_ * sp.log(X_) / W, X_)
check("a3-s06-1 u1、u2", zero(u1 - (X_ * sp.log(X_) - X_) / 2) and zero(u2 - (-X_**3 * sp.log(X_) / 6 + X_**3 / 18)))
yp = X_**2 * sp.log(X_) / 3 - R(4, 9) * X_**2
check("a3-s06-1 (a) y_p=u1 x+u2/x", zero(u1 * X_ + u2 / X_ - yp))
check("a3-s06-1 (a) y_p 滿足原方程", zero(X_**2 * sp.diff(yp, X_, 2) + X_ * sp.diff(yp, X_) - yp - X_**2 * sp.log(X_)))
check("a3-s06-1 (b) y_p(1)=-4/9、y_p'(1)=-5/9", yp.subs(X_, 1) == R(-4, 9) and zero(sp.diff(yp, X_).subs(X_, 1) + R(5, 9)))
y = X_ / 2 - 1 / (18 * X_) + yp
check("a3-s06-1 (b) 解", zero(y.subs(X_, 1)) and zero(sp.diff(y, X_).subs(X_, 1)))
Yp = sp.exp(2 * t) * (t / 3 - R(4, 9))
check("a3-s06-1 (c) Ÿ-Y=te^{2t}", zero(sp.diff(Yp, t, 2) - Yp - t * sp.exp(2 * t)))

# a3-s06-2
y = sp.cos(x) + sp.cos(x) * sp.log(sp.cos(x)) + x * sp.sin(x)
check("a3-s06-2 (b) 解", zero(L(y, 0, 1) - 1 / sp.cos(x)) and ic(y, 1, 0))
check("a3-s06-2 (b) y_p'", zero(sp.diff(sp.cos(x) * sp.log(sp.cos(x)) + x * sp.sin(x), x) - (-sp.sin(x) * sp.log(sp.cos(x)) + x * sp.cos(x))))
check("a3-s06-2 (a) (sec x tan x)'", zero(sp.diff(sp.sec(x) * sp.tan(x), x) - (sp.sec(x) * sp.tan(x) ** 2 + sp.sec(x) ** 3)))
check("a3-s06-2 (c) 端點 y→π/2", near(float(y.subs(x, math.pi / 2 - 1e-9)), math.pi / 2, 1e-6))

print()
print(f"{'全部通過' if not fails else '失敗 ' + str(len(fails)) + ' 項'}")
sys.exit(1 if fails else 0)
