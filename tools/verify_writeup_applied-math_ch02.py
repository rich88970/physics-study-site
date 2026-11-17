"""驗算應用數學第 2 章「考試書寫版」（exam.html）改寫後出現的所有中間值與答案。

用法：python tools/verify_writeup_applied-math_ch02.py   全部通過時結束碼 0。
"""
import math
import sys

import sympy as sp

x, t, lam, m = sp.symbols("x t lambda m")
fails = []


def check(name, cond):
    ok = bool(cond)
    print(("OK  " if ok else "FAIL") + "  " + name)
    if not ok:
        fails.append(name)


def zero(e):
    return sp.simplify(e) == 0


def ode(y, a, b, c=None):
    """回傳 y''+a y'+b y（c 給定時為 a y''+b y'+c y）"""
    if c is None:
        return sp.diff(y, x, 2) + a * sp.diff(y, x) + b * y
    return a * sp.diff(y, x, 2) + b * sp.diff(y, x) + c * y


def near(a, b, tol=5e-4):
    return abs(float(a) - float(b)) < tol


# a2-b1
yp = sp.Rational(1, 2) * sp.exp(-x)
check("a2-b1 (a) y_p''+y_p=e^{-x}", zero(ode(yp, 0, 1) - sp.exp(-x)))
check("a2-b1 (b) y_p(0)=1/2, y_p'(0)=-1/2", yp.subs(x, 0) == sp.Rational(1, 2) and sp.diff(yp, x).subs(x, 0) == -sp.Rational(1, 2))
y = sp.Rational(1, 2) * (sp.cos(x) + sp.sin(x) + sp.exp(-x))
check("a2-b1 (c) 解與初始條件", zero(ode(y, 0, 1) - sp.exp(-x)) and y.subs(x, 0) == 1 and sp.diff(y, x).subs(x, 0) == 0)

# a2-s01-1
P, Q = -2 / x, 2 / x**2
check("a2-s01-1 (a) P,Q 使 x、x^2 為解", zero(ode(x, P, Q)) and zero(ode(x**2, P, Q)))
check("a2-s01-1 (b) W=x^2", zero(x * 2 * x - x**2 - x**2))
check("a2-s01-1 (c) 3x-x^2 是解、L[1]=2/x^2", zero(ode(3 * x - x**2, P, Q)) and zero(ode(sp.Integer(1), P, Q) - 2 / x**2))
y = 3 * x - x**2
check("a2-s01-1 (d) y(1)=2, y'(1)=1", y.subs(x, 1) == 2 and sp.diff(y, x).subs(x, 1) == 1)

# a2-s01-2
check("a2-s01-2 (a) 特徵式 (λ-2)(λ+1)=λ^2-λ-2", sp.expand((lam - 2) * (lam + 1)) == lam**2 - lam - 2)
check("a2-s01-2 (a) g=-1-2x", zero(ode(x, -1, -2) - (-1 - 2 * x)))
for yy in (x + sp.exp(2 * x), x + sp.exp(-x), x + sp.exp(2 * x) + sp.exp(-x)):
    check(f"a2-s01-2 三個函數都是解：{yy}", zero(ode(yy, -1, -2) - (-1 - 2 * x)))
y = -sp.Rational(1, 3) * sp.exp(2 * x) + sp.Rational(1, 3) * sp.exp(-x) + x
check("a2-s01-2 (c) y(0)=y'(0)=0", y.subs(x, 0) == 0 and zero(sp.diff(y, x).subs(x, 0)))

# a2-b2、a2-110a-m3、a2-109b-3a
y = 2 * sp.exp(x) - sp.exp(2 * x)
check("a2-b2", zero(ode(y, -3, 2)) and y.subs(x, 0) == 1 and sp.diff(y, x).subs(x, 0) == 0)
y = sp.exp(x) + 3 * sp.exp(-2 * x)
check("a2-110a-m3", zero(ode(y, 1, -2)) and y.subs(x, 0) == 4 and sp.diff(y, x).subs(x, 0) == -5)
check("a2-109b-3a 因式 (3λ-4)(λ+2)", sp.expand((3 * lam - 4) * (lam + 2)) == 3 * lam**2 + 2 * lam - 8)
y = -9 * sp.exp(sp.Rational(4, 3) * x) + 3 * sp.exp(-2 * x)
check("a2-109b-3a", zero(ode(y, 3, 2, -8)) and y.subs(x, 0) == -6 and sp.diff(y, x).subs(x, 0) == -18)

# a2-s02-1
al = sp.symbols("alpha")
c1, c2 = (2 * al + 2) / 5, (3 * al - 2) / 5
check("a2-s02-1 (a) c1+c2=α、3c1-2c2=2", zero(c1 + c2 - al) and zero(3 * c1 - 2 * c2 - 2))
check("a2-s02-1 (b) α=-1 → c1=0、c2=-1", c1.subs(al, -1) == 0 and c2.subs(al, -1) == -1)
check("a2-s02-1 (c) α=0 → c1=2/5、c2=-2/5", c1.subs(al, 0) == sp.Rational(2, 5) and c2.subs(al, 0) == -sp.Rational(2, 5))

# a2-s02-2
k, L = sp.symbols("k L", positive=True)
y = sp.sinh(k * (L - x)) / sp.sinh(k * L)
check("a2-s02-2 (a) 解與邊界", zero(sp.diff(y, x, 2) - k**2 * y) and zero(y.subs(x, 0) - 1) and y.subs(x, L) == 0)
check("a2-s02-2 (b) sinh1=1.1752、sinh2=3.6269、比 0.3240", near(math.sinh(1), 1.1752, 1e-4) and near(math.sinh(2), 3.6269, 1e-4) and near(math.sinh(1) / math.sinh(2), 0.3240, 1e-4))
check("a2-s02-2 (c) L→∞ 時 → e^{-kx}", near(math.sinh(1 * (40 - 1)) / math.sinh(40), math.exp(-1), 1e-9))

# a2-b3
check("a2-b3 根 -1/2±(√3/2)i", sp.simplify(sp.solve(lam**2 + lam + 1, lam)[0].as_real_imag()[0] + sp.Rational(1, 2)) == 0)
K1, K2, A, ph = sp.symbols("K1 K2 A phi")
u = sp.symbols("u")
check("a2-b3 K1cos u+K2 sin u=A cos(u+φ)，K1=Acosφ、K2=-Asinφ", zero(sp.expand_trig(A * sp.cos(u + ph)) - (A * sp.cos(ph) * sp.cos(u) - A * sp.sin(ph) * sp.sin(u))))

# a2-111a-m2
y = sp.cos(x) + sp.sin(x)
check("a2-111a-m2", zero(ode(y, 0, 1)) and y.subs(x, 0) == 1 and sp.diff(y, x).subs(x, 0) == 1 and zero(y - sp.sqrt(2) * sp.sin(x + sp.pi / 4)))

# a2-113a-m3
check("a2-113a-m3 根 -1/2±2i", set(sp.solve(4 * lam**2 + 4 * lam + 17, lam)) == {-sp.Rational(1, 2) + 2 * sp.I, -sp.Rational(1, 2) - 2 * sp.I})
yg = sp.exp(-x / 2) * (K1 * sp.cos(2 * x) + K2 * sp.sin(2 * x))
dy = sp.exp(-x / 2) * ((-K1 / 2 + 2 * K2) * sp.cos(2 * x) + (-K2 / 2 - 2 * K1) * sp.sin(2 * x))
check("a2-113a-m3 y' 展開式", zero(sp.diff(yg, x) - dy))
y = sp.exp(-x / 2) * (4 * sp.cos(2 * x) - 2 * sp.sin(2 * x))
check("a2-113a-m3 解", zero(ode(y, 4, 4, 17)) and y.subs(x, 0) == 4 and sp.diff(y, x).subs(x, 0) == -6)

# a2-s03-2
yg = sp.exp(-x) * (K1 * sp.cos(2 * x) + K2 * sp.sin(2 * x))
check("a2-s03-2 y' 展開式", zero(sp.diff(yg, x) - sp.exp(-x) * ((-K1 + 2 * K2) * sp.cos(2 * x) + (-K2 - 2 * K1) * sp.sin(2 * x))))
y = sp.exp(-x) * (sp.cos(2 * x) + sp.sin(2 * x))
check("a2-s03-2 (a) 解與振幅相位形式", zero(ode(y, 2, 5)) and y.subs(x, 0) == 1 and sp.diff(y, x).subs(x, 0) == 1 and zero(sp.expand_trig(y - sp.sqrt(2) * sp.exp(-x) * sp.cos(2 * x - sp.pi / 4))))
check("a2-s03-2 (b) 第一個零點 3π/8≈1.178", near(3 * math.pi / 8, 1.178) and abs(float(y.subs(x, 3 * sp.pi / 8))) < 1e-12 and all(float(y.subs(x, v)) > 0 for v in [0.1 * i for i in range(1, 11)]))
xs = [i * 1e-4 for i in range(0, 120000)]
vals = [math.exp(-v) * (math.cos(2 * v) + math.sin(2 * v)) for v in xs]
peaks = [i for i in range(1, len(xs) - 1) if vals[i] > vals[i - 1] and vals[i] > vals[i + 1]]
check("a2-s03-2 (c) 相鄰極大值比 e^{-π}≈0.0432", near(vals[peaks[1]] / vals[peaks[0]], math.exp(-math.pi), 1e-4) and near(math.exp(-math.pi), 0.0432))

# a2-hw1
y = -3 * sp.exp(x) * sp.cos(x)
check("a2-hw1", zero(ode(y, -2, 2)) and y.subs(x, 0) == -3 and y.subs(x, sp.pi / 2) == 0)

# a2-s03-1
check("a2-s03-1 (a) y(π/2)=-1 與 K2 無關", zero((sp.cos(2 * x) + K2 * sp.sin(2 * x)).subs(x, sp.pi / 2) + 1))
check("a2-s03-1 (b) y(π/4)=K2", zero((sp.cos(2 * x) + K2 * sp.sin(2 * x)).subs(x, sp.pi / 4) - K2))
check("a2-s03-1 (c) 行列式 sin2L", zero(sp.Matrix([[1, 0], [sp.cos(2 * L), sp.sin(2 * L)]]).det() - sp.sin(2 * L)))

# a2-109b-3b、a2-108b-1a
yg = sp.exp(4 * x) * (K1 * sp.cos(x) + K2 * sp.sin(x))
check("a2-109b-3b y' 展開式", zero(sp.diff(yg, x) - sp.exp(4 * x) * ((4 * K1 + K2) * sp.cos(x) + (4 * K2 - K1) * sp.sin(x))))
y = sp.exp(4 * x) * (-4 * sp.cos(x) + 15 * sp.sin(x))
check("a2-109b-3b", zero(ode(y, -8, 17)) and y.subs(x, 0) == -4 and sp.diff(y, x).subs(x, 0) == -1)
yg = sp.exp(2 * x) * (K1 * sp.cos(3 * x) + K2 * sp.sin(3 * x))
check("a2-108b-1a y' 展開式", zero(sp.diff(yg, x) - sp.exp(2 * x) * ((2 * K1 + 3 * K2) * sp.cos(3 * x) + (2 * K2 - 3 * K1) * sp.sin(3 * x))))
y = sp.exp(2 * x) * (-sp.cos(3 * x) + sp.Rational(4, 3) * sp.sin(3 * x))
check("a2-108b-1a", zero(ode(y, -4, 13)) and y.subs(x, 0) == -1 and sp.diff(y, x).subs(x, 0) == 2)

# a2-108a-c4、c5、c6
Aa, Bb, kk, w = sp.symbols("A B k omega")
xt = Aa * sp.cos(kk * t) + Bb * sp.sin(kk * t)
check("a2-108a-c4 ẍ=-k^2 x", zero(sp.diff(xt, t, 2) + kk**2 * xt))
y = sp.exp(x) * (sp.cos(x) + sp.sin(x))
check("a2-108a-c5 y'=2e^x cos x、y''=2e^x cos x-2e^x sin x、代回 0", zero(sp.diff(y, x) - 2 * sp.exp(x) * sp.cos(x)) and zero(sp.diff(y, x, 2) - 2 * sp.exp(x) * (sp.cos(x) - sp.sin(x))) and zero(ode(y, -2, 2)))
xt = sp.exp(t) * sp.cos(w * t)
check("a2-108a-c6 導數", zero(sp.diff(xt, t) - sp.exp(t) * (sp.cos(w * t) - w * sp.sin(w * t))) and zero(sp.diff(xt, t, 2) - sp.exp(t) * ((1 - w**2) * sp.cos(w * t) - 2 * w * sp.sin(w * t))))
check("a2-108a-c6 代回 = e^t(9-ω^2)cos ωt", zero(sp.diff(xt, t, 2) - 2 * sp.diff(xt, t) + 10 * xt - sp.exp(t) * (9 - w**2) * sp.cos(w * t)))

# a2-b4
uf = sp.Function("u")(x)
y2 = sp.exp(3 * x) * uf
check("a2-b4 降階代入得 e^{3x}u''", zero(ode(y2, -6, 9) - sp.exp(3 * x) * sp.diff(uf, x, 2)))
y = (1 - 3 * x) * sp.exp(3 * x)
check("a2-b4 解", zero(ode(y, -6, 9)) and y.subs(x, 0) == 1 and sp.diff(y, x).subs(x, 0) == 0)

# a2-hw2、a2-109b-3c
y = -2 * sp.exp(-x / 2)
check("a2-hw2", zero(ode(y, 4, 4, 1)) and y.subs(x, 0) == -2 and sp.diff(y, x).subs(x, 0) == 1)
y = (1 + 7 * x) * sp.exp(-7 * x)
check("a2-109b-3c", zero(ode(y, 14, 49)) and y.subs(x, 0) == 1 and sp.diff(y, x).subs(x, 0) == 0)

# a2-s04-2
eps = sp.symbols("epsilon", positive=True)
y = sp.exp(x) * sp.sinh(eps * x) / eps
check("a2-s04-2 (a) 根 1±ε 與解", set(sp.solve(lam**2 - 2 * lam + 1 - eps**2, lam)) == {1 + eps, 1 - eps} and zero(ode(y, -2, 1 - eps**2)) and y.subs(x, 0) == 0 and zero(sp.diff(y, x).subs(x, 0) - 1))
check("a2-s04-2 (a) c1=1/(2ε)", zero((1 + eps) / (2 * eps) - (1 - eps) / (2 * eps) - 1))
check("a2-s04-2 (b) 極限 xe^x", zero(sp.limit(y, eps, 0) - x * sp.exp(x)))
y = x * sp.exp(x)
check("a2-s04-2 (c) xe^x 滿足重根方程與初始條件", zero(ode(y, -2, 1)) and y.subs(x, 0) == 0 and sp.diff(y, x).subs(x, 0) == 1)

# a2-114a-m2（一般證明；用 y1=x、P=-2x/(1-x^2) 的例子驗公式）
P = -2 * x / (1 - x**2)
Q = 2 / (1 - x**2)
y1 = x
w_ = sp.exp(-sp.integrate(P, x)) / y1**2
y2 = sp.simplify(y1 * sp.integrate(sp.apart(w_, x), x))
check("a2-114a-m2 公式給出的 y2 是解", zero(ode(y2, P, Q)))

# a2-s04-1
check("a2-s04-1 y1=x 是解", zero((1 - x**2) * 0 - 2 * x + 2 * x))
check("a2-s04-1 ∫P=ln(1-x^2)", zero(sp.diff(sp.log(1 - x**2), x) - P))
check("a2-s04-1 部分分式", zero(1 / (x**2 * (1 - x**2)) - (1 / x**2 + 1 / (1 - x**2))))
F = -1 / x + sp.Rational(1, 2) * sp.log((1 + x) / (1 - x))
check("a2-s04-1 積分", zero(sp.diff(F, x) - 1 / (x**2 * (1 - x**2))))
y2 = x / 2 * sp.log((1 + x) / (1 - x)) - 1
check("a2-s04-1 y2 是解", zero(sp.simplify((1 - x**2) * sp.diff(y2, x, 2) - 2 * x * sp.diff(y2, x) + 2 * y2)))
check("a2-s04-1 y2'", zero(sp.diff(y2, x) - (sp.Rational(1, 2) * sp.log((1 + x) / (1 - x)) + x / (1 - x**2))))
check("a2-s04-1 W=1/(1-x^2)", zero(x * sp.diff(y2, x) - y2 - 1 / (1 - x**2)))

# a2-b5
g, w0, x0, s_ = sp.symbols("gamma omega0 x0 s", positive=True)
om = sp.sqrt(w0**2 - g**2)
xa = x0 * sp.exp(-g * t) * (sp.cos(om * t) + g / om * sp.sin(om * t))
eq = lambda z: sp.diff(z, t, 2) + 2 * g * sp.diff(z, t) + w0**2 * z
check("a2-b5 (a) 欠阻尼", zero(eq(xa)) and zero(xa.subs(t, 0) - x0) and zero(sp.diff(xa, t).subs(t, 0)))
xb = x0 * (1 + g * t) * sp.exp(-g * t)
check("a2-b5 (b) 臨界", zero(eq(xb).subs(w0, g)) and zero(xb.subs(t, 0) - x0) and zero(sp.diff(xb, t).subs(t, 0)))
sv = sp.sqrt(g**2 - w0**2)
xc = x0 / (2 * sv) * ((g + sv) * sp.exp((-g + sv) * t) - (g - sv) * sp.exp((-g - sv) * t))
check("a2-b5 (c) 過阻尼", zero(eq(xc)) and zero(xc.subs(t, 0) - x0) and zero(sp.diff(xc, t).subs(t, 0)))

# a2-s05-1
gg, xx0, v0 = 2.0, 0.1, -0.5
ts = -xx0 / (v0 + gg * xx0)
tm = v0 / (gg * (v0 + gg * xx0))
xm = (xx0 + (v0 + gg * xx0) * tm) * math.exp(-gg * tm)
check("a2-s05-1 v0+γx0=-0.3、t*=1/3", near(v0 + gg * xx0, -0.3, 1e-12) and near(ts, 1 / 3, 1e-12))
check("a2-s05-1 t_m=5/6、x=-0.15e^{-5/3}=-0.0283", near(tm, 5 / 6, 1e-12) and near(xm, -0.15 * math.exp(-5 / 3), 1e-12) and near(xm, -0.0283, 5e-5))
G, X0, V0 = sp.symbols("G X0 V0")
xs_ = (X0 + (V0 + G * X0) * t) * sp.exp(-G * t)
check("a2-s05-1 (a) 解與初始條件", zero(sp.diff(xs_, t, 2) + 2 * G * sp.diff(xs_, t) + G**2 * xs_) and xs_.subs(t, 0) == X0 and zero(sp.diff(xs_, t).subs(t, 0) - V0))
check("a2-s05-1 ẋ=0 的 t_m 公式", zero(sp.diff(xs_, t).subs(t, V0 / (G * (V0 + G * X0)))))

# a2-s05-2
omg = 2 * math.pi / 1.0
gam = math.log(2)
w0v = math.sqrt(omg**2 + gam**2)
check("a2-s05-2 ω=6.283、γ=0.693", near(omg, 6.283) and near(gam, 0.693))
check("a2-s05-2 ω^2=39.48、γ^2=0.480、ω0=6.321", near(omg**2, 39.48, 5e-3) and near(gam**2, 0.480, 5e-4) and near(w0v, 6.321))
check("a2-s05-2 b/m=1.386、k/m=39.96", near(2 * gam, 1.386) and near(w0v**2, 39.96, 5e-3))
check("a2-s05-2 臨界 b/m=12.64、9.1 倍", near(2 * w0v, 12.64, 5e-3) and near(2 * w0v / (2 * gam), 9.1, 0.05))

# a2-hw3
X = sp.symbols("X", positive=True)
check("a2-hw3 e^{-∫2/x}=x^{-2}、除以 y1^2 得 1/x", zero(sp.exp(-sp.integrate(2 / X, X)) - X**-2) and zero(X**-2 / (1 / sp.sqrt(X))**2 - 1 / X))
y2 = sp.log(X) / sp.sqrt(X)
check("a2-hw3 y2=ln x/√x 是解", zero(4 * X**2 * sp.diff(y2, X, 2) + 8 * X * sp.diff(y2, X) + y2))
check("a2-hw3 指標式 (2m+1)^2", sp.expand(4 * m * (m - 1) + 8 * m + 1 - (2 * m + 1) ** 2) == 0)

# a2-113b-m4
lam1 = (math.pi / math.log(5)) ** 2
check("a2-113b-m4 π^2=9.8696、(ln5)^2=2.5903、λ1=3.810", near(math.pi**2, 9.8696, 1e-4) and near(math.log(5) ** 2, 2.5903, 1e-4) and near(lam1, 3.810))
n = 2
yn = sp.sin(n * sp.pi * sp.log(X) / sp.log(5))
check("a2-113b-m4 y_n 是解且兩端為 0（n=2）", zero(X**2 * sp.diff(yn, X, 2) + X * sp.diff(yn, X) + (n * sp.pi / sp.log(5)) ** 2 * yn) and yn.subs(X, 1) == 0 and zero(yn.subs(X, 5)))
mu = 0.7
check("a2-113b-m4 λ<0 只有零解（5^μ-5^{-μ}≠0）", abs(5**mu - 5**-mu) > 0)

# a2-s06-1
Y = sp.exp(t) * (K1 * sp.cos(2 * t) + K2 * sp.sin(2 * t))
check("a2-s06-1 Ẏ 展開式", zero(sp.diff(Y, t) - sp.exp(t) * ((K1 + 2 * K2) * sp.cos(2 * t) + (K2 - 2 * K1) * sp.sin(2 * t))))
check("a2-s06-1 根 1±2i", set(sp.solve(lam**2 - 2 * lam + 5, lam)) == {1 + 2 * sp.I, 1 - 2 * sp.I})
y = X * (sp.cos(2 * sp.log(X)) - sp.Rational(1, 2) * sp.sin(2 * sp.log(X)))
check("a2-s06-1 (a) 解", zero(X**2 * sp.diff(y, X, 2) - X * sp.diff(y, X) + 5 * y) and zero(y.subs(X, 1) - 1) and zero(sp.diff(y, X).subs(X, 1)))
xz = math.exp(0.5 * math.atan(2))
check("a2-s06-1 (b) tan^{-1}2=1.1071、e^{0.5536}=1.739", near(math.atan(2), 1.1071, 1e-4) and near(0.5 * math.atan(2), 0.5536, 1e-4) and near(xz, 1.739) and abs(float(y.subs(X, xz))) < 1e-12)

# a2-s06-2
check("a2-s06-2 指標式 (m-3)(m+1)", sp.expand(m * (m - 1) - m - 3 - (m - 3) * (m + 1)) == 0)
y = sp.Rational(3, 4) * (2 * x + 1) ** 3 + sp.Rational(5, 4) / (2 * x + 1)
check("a2-s06-2 解", zero((2 * x + 1) ** 2 * sp.diff(y, x, 2) - 2 * (2 * x + 1) * sp.diff(y, x) - 12 * y) and y.subs(x, 0) == 2 and sp.diff(y, x).subs(x, 0) == 2)

print()
print(f"{'全部通過' if not fails else '失敗 ' + str(len(fails)) + ' 項'}")
sys.exit(1 if fails else 0)
