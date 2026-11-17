"""應用數學第 3 章（非齊次方程：待定係數法）所有題目答案的獨立驗算：python tools/verify_applied_math_ch03.py

每一題：把網站寫的特解／完整解代回微分方程（化簡為 0），代入初始條件，能用 dsolve 的再和 dsolve 比對。
全部通過才算完成。
"""
import sys
import sympy as sp

x, t = sp.symbols("x t", real=True)
y = sp.Function("y")
FAIL = []
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def ok(name, cond):
    cond = bool(cond)
    print(("OK  " if cond else "FAIL"), name)
    if not cond:
        FAIL.append(name)


def zero(e):
    return sp.simplify(sp.expand(e)) == 0


def L(a, b, f, var=x):
    return sp.diff(f, var, 2) + a * sp.diff(f, var) + b * f


def ivp(a, b, g, y0, yp0):
    ds = sp.dsolve(sp.Eq(y(x).diff(x, 2) + a * y(x).diff(x) + b * y(x), g), y(x), ics={y(0): y0, y(x).diff(x).subs(x, 0): yp0})
    return ds.rhs


def tcoeffs(e, arg):
    """把 cos(arg)、sin(arg) 換成符號，回傳對 x、cos、sin 的多項式係數（比較係數用）"""
    Cs, Ss = sp.symbols("Cs Ss")
    e = sp.expand(e)
    e = e.subs({sp.cos(arg): Cs, sp.sin(arg): Ss})
    P = sp.Poly(e, x, Cs, Ss)
    return dict(zip(P.monoms(), P.coeffs())), Cs, Ss


def ic(f, y0, yp0):
    return zero(f.subs(x, 0) - y0) and zero(sp.diff(f, x).subs(x, 0) - yp0)


c1, c2 = sp.symbols("c1 c2")

# ---------------- s01 基本規則 ----------------
# a3-b1：y''-y'-2y=4x^2, y(0)=1, y'(0)=1 → yp=-3+2x-2x^2, y=3e^{-x}+e^{2x}-3+2x-2x^2
yp = -3 + 2 * x - 2 * x**2
ok("a3-b1 yp 滿足方程", zero(L(-1, -2, yp) - 4 * x**2))
K0, K1, K2 = sp.symbols("K0 K1 K2")
s = sp.solve(sp.Poly(sp.expand(L(-1, -2, K0 + K1 * x + K2 * x**2) - 4 * x**2), x).coeffs(), [K0, K1, K2])
ok("a3-b1 比較係數 K2=-2, K1=2, K0=-3", s == {K0: -3, K1: 2, K2: -2})
sol = 3 * sp.exp(-x) + sp.exp(2 * x) + yp
ok("a3-b1 完整解與 IC", zero(L(-1, -2, sol) - 4 * x**2) and ic(sol, 1, 1))
ok("a3-b1 與 dsolve 一致", zero(ivp(-1, -2, 4 * x**2, 1, 1) - sol))
# a3-111a-m3：y''-2y'+2y=2(x-1), y(0)=0, y'(0)=1 → y=x
sol = x
ok("a3-111a-m3 yp=x", zero(L(-2, 2, x) - 2 * (x - 1)))
ok("a3-111a-m3 唯一解 y=x", zero(ivp(-2, 2, 2 * (x - 1), 0, 1) - x))
# a3-114a-m3：y''+2y'-8y=-9cos x-2 sin x, y(0)=4, y'(0)=-6 → e^{2x}+2e^{-4x}+cos x
ok("a3-114a-m3 yp=cos x", zero(L(2, -8, sp.cos(x)) - (-9 * sp.cos(x) - 2 * sp.sin(x))))
sol = sp.exp(2 * x) + 2 * sp.exp(-4 * x) + sp.cos(x)
ok("a3-114a-m3 完整解與 IC", zero(L(2, -8, sol) + 9 * sp.cos(x) + 2 * sp.sin(x)) and ic(sol, 4, -6))
ok("a3-114a-m3 與 dsolve 一致", zero(ivp(2, -8, -9 * sp.cos(x) - 2 * sp.sin(x), 4, -6) - sol))
A, B = sp.symbols("A B")
s = sp.solve([-9 * A + 2 * B + 9, -2 * A - 9 * B + 2], [A, B])
ok("a3-114a-m3 聯立 -9A+2B=-9, -2A-9B=-2 → A=1, B=0", s == {A: 1, B: 0})
# a3-s01-1：y''-y'-2y=4x^2, y(0)=-3, y'(0)=β
be = sp.symbols("beta")
gen = c1 * sp.exp(-x) + c2 * sp.exp(2 * x) + yp
s = sp.solve([gen.subs(x, 0) + 3, sp.diff(gen, x).subs(x, 0) - be], [c1, c2])
ok("a3-s01-1 c2=(β-2)/3, c1=-(β-2)/3", zero(s[c2] - (be - 2) / 3) and zero(s[c1] + (be - 2) / 3))
ok("a3-s01-1 多項式解需要 y(0)=-3, y'(0)=2", yp.subs(x, 0) == -3 and sp.diff(yp, x).subs(x, 0) == 2)
# a3-s01-2：yp=cos x+3 sin x 是 y''+ay'+by=10cos x 的特解 → a=3, b=2
a_, b_ = sp.symbols("a b")
e = sp.expand(L(a_, b_, sp.cos(x) + 3 * sp.sin(x)) - 10 * sp.cos(x))
s = sp.solve([e.coeff(sp.cos(x)), e.coeff(sp.sin(x))], [a_, b_])
ok("a3-s01-2 a=3, b=2", s == {a_: 3, b_: 2})
sol = -5 * sp.exp(-x) + 4 * sp.exp(-2 * x) + sp.cos(x) + 3 * sp.sin(x)
ok("a3-s01-2 完整解與 IC", zero(L(3, 2, sol) - 10 * sp.cos(x)) and ic(sol, 0, 0))
ok("a3-s01-2 與 dsolve 一致", zero(ivp(3, 2, 10 * sp.cos(x), 0, 0) - sol))

# ---------------- s02 加總規則 ----------------
# a3-b2：y''+4y'+4y=4x^2+6e^x → yp1=3/2-2x+x^2, yp2=2/3 e^x
yp1 = sp.Rational(3, 2) - 2 * x + x**2
yp2 = sp.Rational(2, 3) * sp.exp(x)
ok("a3-b2 yp1 滿足 ①", zero(L(4, 4, yp1) - 4 * x**2))
ok("a3-b2 yp2 滿足 ②", zero(L(4, 4, yp2) - 6 * sp.exp(x)))
gen = (c1 + c2 * x) * sp.exp(-2 * x) + yp1 + yp2
ok("a3-b2 一般解滿足原式", zero(L(4, 4, gen) - 4 * x**2 - 6 * sp.exp(x)))
# a3-hw1：y''+2y'+y=sin x+3cos 2x, y(0)=y'(0)=0 → 老師答案
sol = sp.Rational(43, 50) * sp.exp(-x) - sp.Rational(1, 10) * x * sp.exp(-x) - sp.cos(x) / 2 - sp.Rational(9, 25) * sp.cos(2 * x) + sp.Rational(12, 25) * sp.sin(2 * x)
ok("a3-hw1 老師答案滿足方程", zero(L(2, 1, sol) - sp.sin(x) - 3 * sp.cos(2 * x)))
ok("a3-hw1 老師答案滿足 IC", ic(sol, 0, 0))
ok("a3-hw1 yp1=-½cos x", zero(L(2, 1, -sp.cos(x) / 2) - sp.sin(x)))
ok("a3-hw1 yp2=-9/25cos2x+12/25 sin2x", zero(L(2, 1, -sp.Rational(9, 25) * sp.cos(2 * x) + sp.Rational(12, 25) * sp.sin(2 * x)) - 3 * sp.cos(2 * x)))
ok("a3-hw1 與 dsolve 一致", zero(ivp(2, 1, sp.sin(x) + 3 * sp.cos(2 * x), 0, 0) - sol))
# a3-113a-m4：y''+2y'-8y=(x-1)^2+e^{-2x}-9cos x-2 sin x
yp = -x**2 / 8 + sp.Rational(3, 16) * x - sp.Rational(7, 64) - sp.exp(-2 * x) / 8 + sp.cos(x)
ok("a3-113a-m4 yp 滿足方程", zero(L(2, -8, yp) - ((x - 1)**2 + sp.exp(-2 * x) - 9 * sp.cos(x) - 2 * sp.sin(x))))
ok("a3-113a-m4 多項式部分", zero(L(2, -8, -x**2 / 8 + sp.Rational(3, 16) * x - sp.Rational(7, 64)) - (x - 1)**2))
ok("a3-113a-m4 指數部分 -8A=1", zero(L(2, -8, sp.exp(-2 * x)) + 8 * sp.exp(-2 * x)))
# a3-s02-1：y''+y=sin^2 x → yp=1/2+cos2x/6；IC 0,0 → 1/2-2/3cos x+1/6cos2x
yp = sp.Rational(1, 2) + sp.cos(2 * x) / 6
ok("a3-s02-1 yp", zero(L(0, 1, yp) - sp.sin(x)**2))
sol = sp.Rational(1, 2) - sp.Rational(2, 3) * sp.cos(x) + sp.cos(2 * x) / 6
ok("a3-s02-1 完整解與 IC", zero(L(0, 1, sol) - sp.sin(x)**2) and ic(sol, 0, 0))
# a3-s02-2：y''+2y'+5y=cosh x, IC 0,0
yp = sp.exp(x) / 16 + sp.exp(-x) / 8
ok("a3-s02-2 yp", zero(L(2, 5, yp) - sp.cosh(x).rewrite(sp.exp)))
sol = sp.exp(-x) * (-sp.Rational(3, 16) * sp.cos(2 * x) - sp.Rational(1, 16) * sp.sin(2 * x)) + yp
ok("a3-s02-2 完整解與 IC", zero(L(2, 5, sol) - sp.cosh(x).rewrite(sp.exp)) and ic(sol, 0, 0))

# ---------------- s03 乘法規則 ----------------
# a3-b3：y''+9y=x cos x → yp=(1/32) sin x+(1/8) x cos x
yp = sp.sin(x) / 32 + x * sp.cos(x) / 8
ok("a3-b3 yp", zero(L(0, 9, yp) - x * sp.cos(x)))
Ag, Bg, Cg, Dg = sp.symbols("A B C D")
guess = Ag * sp.cos(x) + Bg * sp.sin(x) + Cg * x * sp.cos(x) + Dg * x * sp.sin(x)
cf, _, _ = tcoeffs(L(0, 9, guess) - x * sp.cos(x), x)
g0 = lambda m: cf.get(m, 0)
eqs = [g0((1, 1, 0)), g0((1, 0, 1)), g0((0, 1, 0)), g0((0, 0, 1))]   # x cos, x sin, cos, sin
s = sp.solve(eqs, [Ag, Bg, Cg, Dg])
ok("a3-b3 A=0, B=1/32, C=1/8, D=0", s == {Ag: 0, Bg: sp.Rational(1, 32), Cg: sp.Rational(1, 8), Dg: 0})
ok("a3-b3 板書四條：cos: 8A+2D=0, sin: 8B-2C=0, xcos: 8C=1, xsin: 8D=0", zero(eqs[2] - (8 * Ag + 2 * Dg)) and zero(eqs[3] - (8 * Bg - 2 * Cg)) and zero(eqs[0] - (8 * Cg - 1)) and zero(eqs[1] - 8 * Dg))
# a3-hw2：y''-4y'-12y=x e^{-4x} → (3/100+x/20)e^{-4x}
yp = (sp.Rational(3, 100) + x / 20) * sp.exp(-4 * x)
ok("a3-hw2 老師答案滿足方程", zero(L(-4, -12, yp) - x * sp.exp(-4 * x)))
u = sp.Function("u")(x)
ok("a3-hw2 代 y=e^{-4x}u 得 u''-12u'+20u", zero(sp.simplify(L(-4, -12, sp.exp(-4 * x) * u) * sp.exp(4 * x)) - (sp.diff(u, x, 2) - 12 * sp.diff(u, x) + 20 * u)))
# a3-112a-m3：y''+2y'+17y=60e^{-4x} sin5x
yp = 2 * sp.exp(-4 * x) * sp.cos(5 * x)
ok("a3-112a-m3 yp=2e^{-4x}cos5x", zero(L(2, 17, yp) - 60 * sp.exp(-4 * x) * sp.sin(5 * x)))
yc_ok = zero(L(2, 17, sp.exp(-x) * sp.cos(4 * x))) and zero(L(2, 17, sp.exp(-x) * sp.sin(4 * x)))
ok("a3-112a-m3 yc=e^{-x}(c1cos4x+c2sin4x)", yc_ok)
sol = sp.exp(-x) * (-2 * sp.cos(4 * x) + 2 * sp.sin(4 * x)) + yp
ok("a3-112a-m3 唯一解與 IC", zero(L(2, 17, sol) - 60 * sp.exp(-4 * x) * sp.sin(5 * x)) and ic(sol, 0, 2))
ok("a3-112a-m3 與 dsolve 一致", zero(ivp(2, 17, 60 * sp.exp(-4 * x) * sp.sin(5 * x), 0, 2) - sol))
ok("a3-112a-m3 代 y=e^{-4x}u 得 u''-6u'+25u", zero(sp.simplify(L(2, 17, sp.exp(-4 * x) * u) * sp.exp(4 * x)) - (sp.diff(u, x, 2) - 6 * sp.diff(u, x) + 25 * u)))
# a3-s03-1：y''+4y=x^2 sin x → (x^2/3-14/27) sin x-(4/9)x cos x
yp = (x**2 / 3 - sp.Rational(14, 27)) * sp.sin(x) - sp.Rational(4, 9) * x * sp.cos(x)
ok("a3-s03-1 yp", zero(L(0, 4, yp) - x**2 * sp.sin(x)))
uu = x**2 / 3 - 4 * sp.I * x / 9 - sp.Rational(14, 27)
ok("a3-s03-1 複數法 u''+2iu'+3u=x^2", zero(sp.diff(uu, x, 2) + 2 * sp.I * sp.diff(uu, x) + 3 * uu - x**2))
ok("a3-s03-1 取虛部", zero(sp.im(sp.expand(uu * (sp.cos(x) + sp.I * sp.sin(x)))) - yp))
# a3-s03-2：y''+2y'+ky=e^{-x}cos3x
ok("a3-s03-2 k=5：yp=-(1/5)e^{-x}cos3x", zero(L(2, 5, -sp.exp(-x) * sp.cos(3 * x) / 5) - sp.exp(-x) * sp.cos(3 * x)))
ok("a3-s03-2 k=10：yp=(x/6)e^{-x}sin3x", zero(L(2, 10, x * sp.exp(-x) * sp.sin(3 * x) / 6) - sp.exp(-x) * sp.cos(3 * x)))
ok("a3-s03-2 k=10 時 e^{-x}cos3x 是齊次解", zero(L(2, 10, sp.exp(-x) * sp.cos(3 * x))))
ok("a3-s03-2 代 y=e^{-x}u 得 u''+(k-1)u", zero(sp.simplify(L(2, sp.Symbol("k"), sp.exp(-x) * u) * sp.exp(x)) - (sp.diff(u, x, 2) + (sp.Symbol("k") - 1) * u)))

# ---------------- s04 修正規則 ----------------
# a3-b4：y''-4y'+4y=2e^{2x} → yp=x^2 e^{2x}
yp = x**2 * sp.exp(2 * x)
ok("a3-b4 yp", zero(L(-4, 4, yp) - 2 * sp.exp(2 * x)))
ok("a3-b4 Ae^{2x}、Axe^{2x} 代入都得 0", zero(L(-4, 4, sp.exp(2 * x))) and zero(L(-4, 4, x * sp.exp(2 * x))))
ok("a3-b4 L[x^2e^{2x}]=2e^{2x}（所以 2K=2）", zero(L(-4, 4, x**2 * sp.exp(2 * x)) - 2 * sp.exp(2 * x)))
# 參數變換法重算 a3-b4
y1, y2 = sp.exp(2 * x), x * sp.exp(2 * x)
W = sp.simplify(y1 * sp.diff(y2, x) - y2 * sp.diff(y1, x))
u1 = sp.integrate(sp.simplify(-y2 * 2 * sp.exp(2 * x) / W), x)
u2 = sp.integrate(sp.simplify(y1 * 2 * sp.exp(2 * x) / W), x)
ok("a3-b4 參數變換法也得 x^2 e^{2x}", zero(u1 * y1 + u2 * y2 - x**2 * sp.exp(2 * x)))
# a3-hw3：y''+y=2x sin x → -½x^2 cos x+½x sin x
yp = -x**2 * sp.cos(x) / 2 + x * sp.sin(x) / 2
ok("a3-hw3 老師答案", zero(L(0, 1, yp) - 2 * x * sp.sin(x)))
Ag, Bg, Cg, Dg = sp.symbols("A B C D")
guess = x * ((Ag * x + Bg) * sp.cos(x) + (Cg * x + Dg) * sp.sin(x))
cf, _, _ = tcoeffs(L(0, 1, guess) - 2 * x * sp.sin(x), x)
g0 = lambda m: cf.get(m, 0)
eqs = [g0((0, 1, 0)), g0((0, 0, 1)), g0((1, 1, 0)), g0((1, 0, 1))]   # cos, sin, x cos, x sin
ok("a3-hw3 x^2 項全部抵消", all(v == 0 for m, v in cf.items() if m[0] >= 2))
s = sp.solve(eqs, [Ag, Bg, Cg, Dg])
ok("a3-hw3 A=-1/2, B=0, C=0, D=1/2", s == {Ag: -sp.Rational(1, 2), Bg: 0, Cg: 0, Dg: sp.Rational(1, 2)})
ok("a3-hw3 四條：cos: 2A+2D=0, sin: -2B+2C=0, xcos: 4C=0, xsin: -4A=2", zero(eqs[0] - (2 * Ag + 2 * Dg)) and zero(eqs[1] - (2 * Cg - 2 * Bg)) and zero(eqs[2] - 4 * Cg) and zero(eqs[3] - (-4 * Ag - 2)))
# a3-110a-m4：y''-2y'+2y=2e^x cos x → yp=x e^x sin x
yp = x * sp.exp(x) * sp.sin(x)
ok("a3-110a-m4 yp", zero(L(-2, 2, yp) - 2 * sp.exp(x) * sp.cos(x)))
ok("a3-110a-m4 e^x cos x 是齊次解", zero(L(-2, 2, sp.exp(x) * sp.cos(x))))
ok("a3-110a-m4 代 y=e^x u 得 u''+u", zero(sp.simplify(L(-2, 2, sp.exp(x) * u) * sp.exp(-x)) - (sp.diff(u, x, 2) + u)))
# a3-s04-1：y''-y=cosh x, IC 0,0 → (x/2) sinh x
sol = x * sp.sinh(x) / 2
ok("a3-s04-1 解", zero(sp.simplify((L(0, -1, sol) - sp.cosh(x)).rewrite(sp.exp))) and ic(sol, 0, 0))
# a3-s04-2：y''+3y'=6x+2+9e^{-3x} → yp=x^2-3x e^{-3x}；IC 0,0 → 1-e^{-3x}+x^2-3xe^{-3x}
yp = x**2 - 3 * x * sp.exp(-3 * x)
ok("a3-s04-2 yp", zero(L(3, 0, yp) - (6 * x + 2 + 9 * sp.exp(-3 * x))))
sol = 1 - sp.exp(-3 * x) + yp
ok("a3-s04-2 完整解與 IC", zero(L(3, 0, sol) - (6 * x + 2 + 9 * sp.exp(-3 * x))) and ic(sol, 0, 0))
ok("a3-s04-2 與 dsolve 一致", zero(ivp(3, 0, 6 * x + 2 + 9 * sp.exp(-3 * x), 0, 0) - sol))

# ---------------- s05 受迫阻尼振盪 ----------------
g_, w0, w, F0 = sp.symbols("gamma omega_0 omega F_0", positive=True)
D = (w0**2 - w**2)**2 + 4 * g_**2 * w**2
K1 = -2 * g_ * w * F0 / D
K2 = (w0**2 - w**2) * F0 / D
xp = K1 * sp.cos(w * t) + K2 * sp.sin(w * t)
ok("a3-b5 K1、K2 使 xp 滿足 EOM", zero(sp.diff(xp, t, 2) + 2 * g_ * sp.diff(xp, t) + w0**2 * xp - F0 * sp.sin(w * t)))
ok("a3-b5 A^2=K1^2+K2^2=F0^2/D", zero(K1**2 + K2**2 - F0**2 / D))
ok("a3-b5 tanφ=K1/K2=-2γω/(ω0^2-ω^2)", zero(K1 / K2 + 2 * g_ * w / (w0**2 - w**2)))
# a3-s05-1：A(ω) 的極大在 ω_r=√(ω0^2-2γ^2)，A_max=F0/(2γ√(ω0^2-γ^2))
Dw = sp.diff(D, w)
ok("a3-s05-1 dD/dω=0 ⇒ ω^2=ω0^2-2γ^2", zero(Dw.subs(w, sp.sqrt(w0**2 - 2 * g_**2))))
Amax = F0 / sp.sqrt(D.subs(w, sp.sqrt(w0**2 - 2 * g_**2)))
ok("a3-s05-1 A_max 公式", zero(sp.simplify(Amax**2 - (F0 / (2 * g_ * sp.sqrt(w0**2 - g_**2)))**2)))
num = {w0: 10, g_: 1, F0: 5}
ok("a3-s05-1 ω_r=√98=9.899", abs(float(sp.sqrt(98)) - 9.899) < 5e-4)
ok("a3-s05-1 A_max=5/(2√99)=0.2513", abs(float(Amax.subs(num)) - 0.2513) < 5e-5)
ok("a3-s05-1 A(ω0)=F0/(2γω0)=0.25", zero((F0 / sp.sqrt(D)).subs(w, w0).subs(num) - sp.Rational(1, 4)))
ok("a3-s05-1 A(0)=F0/ω0^2=0.05", zero((F0 / sp.sqrt(D)).subs(w, 0).subs(num) - sp.Rational(1, 20)))
ok("a3-s05-1 A_max/A(0)=5.03", abs(float(Amax.subs(num) / sp.Rational(1, 20)) - 5.03) < 5e-3)
# a3-s05-2：無阻尼共振 ẍ+ω0^2x=F0 sin ω0 t, x(0)=ẋ(0)=0
xs = F0 / (2 * w0**2) * sp.sin(w0 * t) - F0 * t / (2 * w0) * sp.cos(w0 * t)
ok("a3-s05-2 EOM", zero(sp.diff(xs, t, 2) + w0**2 * xs - F0 * sp.sin(w0 * t)))
ok("a3-s05-2 IC", zero(xs.subs(t, 0)) and zero(sp.diff(xs, t).subs(t, 0)))
ok("a3-s05-2 包絡 F0 t/(2ω0) = 10 F0/ω0^2 ⇒ t=20/ω0=10 s（ω0=2）", sp.solve(sp.Eq(F0 * t / (2 * w0), 10 * F0 / w0**2), t) == [20 / w0] and (20 / w0).subs(w0, 2) == 10)

# ---------------- s06 參數變換法 ----------------
# a3-s06-1：x^2y''+xy'-y=x^2 ln x，y1=x、y2=1/x → yp=(1/3)x^2 ln x-(4/9)x^2；y(1)=y'(1)=0
Xp = sp.symbols("X", positive=True)


def CE3(f):
    return Xp**2 * sp.diff(f, Xp, 2) + Xp * sp.diff(f, Xp) - f


y1, y2 = Xp, 1 / Xp
ok("a3-s06-1 y1=x、y2=1/x 是齊次解", zero(CE3(y1)) and zero(CE3(y2)))
W = sp.simplify(y1 * sp.diff(y2, Xp) - y2 * sp.diff(y1, Xp))
ok("a3-s06-1 W=-2/x", zero(W + 2 / Xp))
g = sp.log(Xp)   # 標準式右邊
u1p = sp.simplify(-y2 * g / W)
u2p = sp.simplify(y1 * g / W)
ok("a3-s06-1 u1'=ln x/2, u2'=-x^2 ln x/2", zero(u1p - sp.log(Xp) / 2) and zero(u2p + Xp**2 * sp.log(Xp) / 2))
u1 = sp.integrate(u1p, Xp)
u2 = sp.integrate(u2p, Xp)
ok("a3-s06-1 u1=(x ln x-x)/2, u2=-x^3 ln x/6+x^3/18", zero(u1 - (Xp * sp.log(Xp) - Xp) / 2) and zero(u2 - (-Xp**3 * sp.log(Xp) / 6 + Xp**3 / 18)))
yp = Xp**2 * sp.log(Xp) / 3 - sp.Rational(4, 9) * Xp**2
ok("a3-s06-1 u1y1+u2y2 = yp", zero(u1 * y1 + u2 * y2 - yp))
ok("a3-s06-1 yp 滿足原式", zero(CE3(yp) - Xp**2 * sp.log(Xp)))
wrong = sp.integrate(sp.simplify(-y2 * Xp**2 * sp.log(Xp) / W), Xp) * y1 + sp.integrate(sp.simplify(y1 * Xp**2 * sp.log(Xp) / W), Xp) * y2
ok("a3-s06-1 誤用 g=x^2 ln x 的結果不滿足原式", not zero(CE3(wrong) - Xp**2 * sp.log(Xp)))
sol = Xp / 2 - 1 / (18 * Xp) + yp
ok("a3-s06-1 IVP 解", zero(CE3(sol) - Xp**2 * sp.log(Xp)) and zero(sol.subs(Xp, 1)) and zero(sp.diff(sol, Xp).subs(Xp, 1)))
tt = sp.symbols("tt", real=True)
Yt = sp.exp(2 * tt) * (tt / 3 - sp.Rational(4, 9))
ok("a3-s06-1 x=e^t 驗算：Y''-Y=t e^{2t}", zero(sp.diff(Yt, tt, 2) - Yt - tt * sp.exp(2 * tt)) and zero(Yt.subs(tt, sp.log(Xp)) - yp))
# a3-s06-2：y''+y=sec x，y(0)=1、y'(0)=0 → cos x+cos x ln cos x+x sin x，|x|<π/2
yp = sp.cos(x) * sp.log(sp.cos(x)) + x * sp.sin(x)
ok("a3-s06-2 yp", zero(sp.simplify(L(0, 1, yp) - 1 / sp.cos(x))))
ok("a3-s06-2 u1'=-tan x, u2'=1", zero(-sp.sin(x) / sp.cos(x) + sp.tan(x)) and zero(sp.cos(x) / sp.cos(x) - 1))
sol = sp.cos(x) + yp
ok("a3-s06-2 IVP 解", zero(sp.simplify(L(0, 1, sol) - 1 / sp.cos(x))) and ic(sol, 1, 0))
ok("a3-s06-2 x→π/2⁻：y→π/2", zero(sp.limit(sol, x, sp.pi / 2, "-") - sp.pi / 2))
ok("a3-s06-2 x→π/2⁻：y''→∞", sp.limit(1 / sp.cos(x) - sol, x, sp.pi / 2, "-") == sp.oo)

# ---------------- 考前衝刺變化題 ----------------
ok("a3var-1 yp=x^2", zero(L(-5, 6, x**2) - (6 * x**2 - 10 * x + 2)))
ok("a3var-2 yp=-2x cos2x", zero(L(0, 4, -2 * x * sp.cos(2 * x)) - 8 * sp.sin(2 * x)))
ok("a3var-3 yp=-x e^x+½e^{3x}", zero(L(-3, 2, -x * sp.exp(x) + sp.exp(3 * x) / 2) - sp.exp(x) - sp.exp(3 * x)))
ok("a3var-4 yp=½x^2e^{-x}", zero(L(2, 1, x**2 * sp.exp(-x) / 2) - sp.exp(-x)))
ok("a3var-5 yp=½(x-1)e^x", zero(L(0, 1, (x - 1) * sp.exp(x) / 2) - x * sp.exp(x)))
Ag, Bg, Cg, Dg, Eg = sp.symbols("A B C D E")
form = x * sp.exp(x) * (Ag * sp.cos(2 * x) + Bg * sp.sin(2 * x)) + (Cg * x**2 + Dg * x + Eg) * sp.exp(x)
e = sp.simplify((L(-2, 5, form) - sp.exp(x) * sp.sin(2 * x) - x**2 * sp.exp(x)) * sp.exp(-x))
cf, _, _ = tcoeffs(sp.expand(e), 2 * x)
s = sp.solve(list(cf.values()), [Ag, Bg, Cg, Dg, Eg])
ok("a3var-6 形式可解（A=-1/4, B=0, C=1/4, D=0, E=-1/8）", s == {Ag: -sp.Rational(1, 4), Bg: 0, Cg: sp.Rational(1, 4), Dg: 0, Eg: -sp.Rational(1, 8)})
xp7 = -sp.Rational(1, 4) * sp.cos(2 * t) + sp.Rational(1, 2) * sp.sin(2 * t)
ok("a3var-7 xp", zero(sp.diff(xp7, t, 2) + 4 * sp.diff(xp7, t) + 20 * xp7 - 10 * sp.sin(2 * t)))
ok("a3var-7 A=10/√320=0.559", abs(10 / 320**0.5 - 0.559) < 5e-4 and zero(sp.Rational(1, 16) + sp.Rational(1, 4) - sp.Rational(100, 320)))
yp = -sp.cos(x) * sp.log(1 / sp.cos(x) + sp.tan(x))
ok("a3var-8 y''+y=tan x 的 yp", zero(sp.simplify(L(0, 1, yp) - sp.tan(x))))

print()
print("全部通過" if not FAIL else f"失敗 {len(FAIL)} 項：{FAIL}")
sys.exit(1 if FAIL else 0)
