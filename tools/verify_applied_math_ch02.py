"""應用數學第 2 章（二階線性齊次方程）所有題目答案的獨立驗算：python tools/verify_applied_math_ch02.py

每一題：把網站寫的答案代回微分方程（checkodesol 或直接代入化簡為 0）、代入初始／邊界條件，
能用 dsolve 的再和 dsolve 的結果比對。全部通過才算完成。
"""
import sys
import sympy as sp

x, t = sp.symbols("x t", real=True)
X = sp.symbols("X", positive=True)          # Cauchy–Euler 用 x>0
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


def residual(ode_lhs_minus_rhs, sol, var=x):
    """把 sol 代入 L[y]-g，回傳化簡後的結果"""
    f = sp.Lambda(var, sol)
    e = ode_lhs_minus_rhs.subs(y(var), sol).doit()
    return sp.simplify(e)


def L(a, b, f, var=x):
    """y''+a y'+b y"""
    return sp.diff(f, var, 2) + a * sp.diff(f, var) + b * f


# ---------------- s01 結構 ----------------
# a2-b1：y''+y=e^{-x}, y(0)=1, y'(0)=0
yp = sp.exp(-x) / 2
ok("a2-b1 yp 滿足原式", zero(L(0, 1, yp) - sp.exp(-x)))
ok("a2-b1 yp(0)=1/2 不滿足 y(0)=1", yp.subs(x, 0) == sp.Rational(1, 2))
sol = sp.cos(x) / 2 + sp.sin(x) / 2 + sp.exp(-x) / 2
ok("a2-b1 答案滿足方程", zero(L(0, 1, sol) - sp.exp(-x)))
ok("a2-b1 y(0)=1", sol.subs(x, 0) == 1)
ok("a2-b1 y'(0)=0", sp.diff(sol, x).subs(x, 0) == 0)
ds = sp.dsolve(sp.Eq(y(x).diff(x, 2) + y(x), sp.exp(-x)), y(x), ics={y(0): 1, y(x).diff(x).subs(x, 0): 0})
ok("a2-b1 與 dsolve 一致", zero(ds.rhs - sol))

# a2-s01-1：y1=x, y2=x^2 → P=-2/x, Q=2/x^2
P, Q = -2 / X, 2 / X**2
for f, nm in ((X, "x"), (X**2, "x^2"), (3 * X - X**2, "3x-x^2")):
    ok(f"a2-s01-1 {nm} 是 y''+Py'+Qy=0 的解", zero(sp.diff(f, X, 2) + P * sp.diff(f, X) + Q * f))
f = X + X**2 + 1
ok("a2-s01-1 x+x^2+1 不是解（殘差 2/x^2）", zero(sp.diff(f, X, 2) + P * sp.diff(f, X) + Q * f - 2 / X**2))
W = sp.simplify(X * sp.diff(X**2, X) - X**2 * 1)
ok("a2-s01-1 Wronskian = x^2", zero(W - X**2))

# a2-s01-2：y_A=x+e^{2x}, y_B=x+e^{-x}, y_C=x+e^{2x}+e^{-x} 都是 y''+ay'+by=g 的解
a, b = -1, -2
g = -1 - 2 * x
for f, nm in ((x + sp.exp(2 * x), "yA"), (x + sp.exp(-x), "yB"), (x + sp.exp(2 * x) + sp.exp(-x), "yC")):
    ok(f"a2-s01-2 {nm} 滿足 y''-y'-2y=-1-2x", zero(L(a, b, f) - g))
c1, c2 = sp.symbols("c1 c2")
gen = c1 * sp.exp(2 * x) + c2 * sp.exp(-x) + x
s = sp.solve([gen.subs(x, 0), sp.diff(gen, x).subs(x, 0)], [c1, c2])
ok("a2-s01-2 IC y(0)=0,y'(0)=0 → c1=-1/3, c2=1/3", s[c1] == sp.Rational(-1, 3) and s[c2] == sp.Rational(1, 3))
sol = gen.subs(s)
ok("a2-s01-2 解滿足方程", zero(L(a, b, sol) - g))
ds = sp.dsolve(sp.Eq(y(x).diff(x, 2) - y(x).diff(x) - 2 * y(x), -1 - 2 * x), y(x), ics={y(0): 0, y(x).diff(x).subs(x, 0): 0})
ok("a2-s01-2 與 dsolve 一致", zero(ds.rhs - sol))
ok("a2-s01-2 yA-yB=e^{2x}-e^{-x}、yC-yA=e^{-x} 是齊次解", zero(L(a, b, sp.exp(2 * x) - sp.exp(-x))) and zero(L(a, b, sp.exp(-x))))

# ---------------- s02 相異實根 ----------------
# a2-b2：y''-3y'+2y=0, y(0)=1, y'(0)=0 → 2e^x-e^{2x}
sol = 2 * sp.exp(x) - sp.exp(2 * x)
ok("a2-b2 方程", zero(L(-3, 2, sol)))
ok("a2-b2 IC", sol.subs(x, 0) == 1 and sp.diff(sol, x).subs(x, 0) == 0)
# a2-110a-m3：y''+y'-2y=0, y(0)=4, y'(0)=-5 → e^x+3e^{-2x}
sol = sp.exp(x) + 3 * sp.exp(-2 * x)
ok("a2-110a-m3 方程", zero(L(1, -2, sol)))
ok("a2-110a-m3 IC", sol.subs(x, 0) == 4 and sp.diff(sol, x).subs(x, 0) == -5)
ds = sp.dsolve(sp.Eq(y(x).diff(x, 2) + y(x).diff(x) - 2 * y(x), 0), y(x), ics={y(0): 4, y(x).diff(x).subs(x, 0): -5})
ok("a2-110a-m3 與 dsolve 一致", zero(ds.rhs - sol))
# a2-s02-1：y''-y'-6y=0, y(0)=alpha, y'(0)=2，有界 ⇔ alpha=-1，解 -e^{-2x}
al = sp.symbols("alpha")
gen = c1 * sp.exp(3 * x) + c2 * sp.exp(-2 * x)
s = sp.solve([gen.subs(x, 0) - al, sp.diff(gen, x).subs(x, 0) - 2], [c1, c2])
ok("a2-s02-1 c1=(2alpha+2)/5", zero(s[c1] - (2 * al + 2) / 5))
ok("a2-s02-1 c2=(3alpha-2)/5", zero(s[c2] - (3 * al - 2) / 5))
ok("a2-s02-1 alpha=-1", sp.solve(s[c1], al) == [-1])
sol = -sp.exp(-2 * x)
ok("a2-s02-1 解 -e^{-2x}", zero(L(-1, -6, sol)) and sol.subs(x, 0) == -1 and sp.diff(sol, x).subs(x, 0) == 2)
# a2-s02-2：y''-k^2 y=0, y(0)=1, y(L)=0 → sinh(k(L-x))/sinh(kL)
k, Lp = sp.symbols("k L", positive=True)
sol = sp.sinh(k * (Lp - x)) / sp.sinh(k * Lp)
ok("a2-s02-2 方程", zero(sp.diff(sol, x, 2) - k**2 * sol))
ok("a2-s02-2 y(0)=1", zero(sol.subs(x, 0) - 1))
ok("a2-s02-2 y(L)=0", zero(sol.subs(x, Lp)))
ok("a2-s02-2 L→∞ 極限 e^{-kx}", zero(sp.limit(sol.rewrite(sp.exp), Lp, sp.oo) - sp.exp(-k * x)))
ok("a2-s02-2 數值 k=1,L=2,x=1：0.3240（無限長 e^{-1}=0.3679）", abs(float(sp.sinh(1) / sp.sinh(2)) - 0.3240) < 5e-5 and abs(float(sp.exp(-1)) - 0.3679) < 5e-5)

# ---------------- s03 共軛複根 ----------------
# a2-b3：y''+y'+y=0 → e^{-x/2}(K1 cos(√3x/2)+K2 sin(√3x/2))
K1, K2 = sp.symbols("K1 K2")
sol = sp.exp(-x / 2) * (K1 * sp.cos(sp.sqrt(3) * x / 2) + K2 * sp.sin(sp.sqrt(3) * x / 2))
ok("a2-b3 實數形式滿足方程", zero(L(1, 1, sol)))
lam = sp.solve(sp.Symbol("l")**2 + sp.Symbol("l") + 1, sp.Symbol("l"))
ok("a2-b3 根 (-1±√3 i)/2", set(sp.simplify(r) for r in lam) == {sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2, sp.Rational(-1, 2) - sp.sqrt(3) * sp.I / 2})
# 振幅相位形式：K1 cos θ + K2 sin θ = A cos(θ-δ) 和板書 A cos(θ+φ)（φ=-δ）
A_, th = sp.symbols("A theta")
ok("a2-b3 K1=A cos φ, K2=-A sin φ 對應 A cos(θ+φ)", zero(sp.expand_trig(A_ * sp.cos(th + sp.Symbol("phi"))) - (A_ * sp.cos(sp.Symbol("phi")) * sp.cos(th) - A_ * sp.sin(sp.Symbol("phi")) * sp.sin(th))))
# a2-hw1：y''-2y'+2y=0, y(0)=-3, y(π/2)=0 → -3e^x cos x（老師答案）
sol = -3 * sp.exp(x) * sp.cos(x)
ok("a2-hw1 方程", zero(L(-2, 2, sol)))
ok("a2-hw1 y(0)=-3", sol.subs(x, 0) == -3)
ok("a2-hw1 y(π/2)=0", zero(sol.subs(x, sp.pi / 2)))
# a2-111a-m2：y''+y=0, y(0)=1, y'(0)=1 → cos x+sin x
sol = sp.cos(x) + sp.sin(x)
ok("a2-111a-m2 方程與 IC", zero(L(0, 1, sol)) and sol.subs(x, 0) == 1 and sp.diff(sol, x).subs(x, 0) == 1)
ok("a2-111a-m2 = √2 sin(x+π/4)", zero(sp.expand_trig(sp.sqrt(2) * sp.sin(x + sp.pi / 4)) - sol))
# a2-113a-m3：4y''+4y'+17y=0, y(0)=4, y'(0)=-6 → e^{-x/2}(4cos2x-2sin2x)
sol = sp.exp(-x / 2) * (4 * sp.cos(2 * x) - 2 * sp.sin(2 * x))
ok("a2-113a-m3 方程", zero(4 * sp.diff(sol, x, 2) + 4 * sp.diff(sol, x) + 17 * sol))
ok("a2-113a-m3 IC", sol.subs(x, 0) == 4 and sp.diff(sol, x).subs(x, 0) == -6)
ds = sp.dsolve(sp.Eq(4 * y(x).diff(x, 2) + 4 * y(x).diff(x) + 17 * y(x), 0), y(x), ics={y(0): 4, y(x).diff(x).subs(x, 0): -6})
ok("a2-113a-m3 與 dsolve 一致", zero(ds.rhs - sol))
# a2-s03-1：y''+4y=0, y(0)=1, y(π/2)=B：只有 B=-1 有解（且無限多個）
gen = sp.cos(2 * x) + c2 * sp.sin(2 * x)
ok("a2-s03-1 y(π/2) 與 c2 無關、恆為 -1", zero(gen.subs(x, sp.pi / 2) + 1))
ok("a2-s03-1 (b) y(π/4)=B 時唯一解 c2=B", zero(gen.subs(x, sp.pi / 4) - c2))
# a2-s03-2：y''+2y'+5y=0, y(0)=1, y'(0)=1 → e^{-x}(cos2x+sin2x)=√2 e^{-x} cos(2x-π/4)
sol = sp.exp(-x) * (sp.cos(2 * x) + sp.sin(2 * x))
ok("a2-s03-2 方程與 IC", zero(L(2, 5, sol)) and sol.subs(x, 0) == 1 and sp.diff(sol, x).subs(x, 0) == 1)
ok("a2-s03-2 振幅相位形式", zero(sp.expand_trig(sp.sqrt(2) * sp.exp(-x) * sp.cos(2 * x - sp.pi / 4)) - sol))
ok("a2-s03-2 第一個零點 3π/8", zero(sol.subs(x, 3 * sp.pi / 8)) and float(3 * sp.pi / 8) > 0)
xs = sp.nsolve(sp.diff(sol, x), x, 0.3)
xs2 = sp.nsolve(sp.diff(sol, x), x, 0.3 + float(sp.pi))
ok("a2-s03-2 相鄰極大值比 e^{-π}", abs(float(sol.subs(x, xs2) / sol.subs(x, xs)) - float(sp.exp(-sp.pi))) < 1e-9)
ok("a2-s03-2 極大值位置 x=atan(1/3)/2... 即 tan(2x-π/4)=-1/2", abs(float(sp.tan(2 * xs - sp.pi / 4)) + 0.5) < 1e-9)
ok("a2-s03-2 e^{-π}=0.0432", abs(float(sp.exp(-sp.pi)) - 0.0432) < 5e-5)

# ---------------- s04 重根與降階法 ----------------
# 降階公式：y2=y1∫e^{-∫P}/y1^2 dx 對一般 P、Q 成立（用 y1''=-Py1'-Qy1）
Pf, Qf, y1f = sp.Function("P")(x), sp.Function("Q")(x), sp.Function("y1")(x)
u = sp.Function("u")(x)
expr = sp.diff(y1f * u, x, 2) + Pf * sp.diff(y1f * u, x) + Qf * y1f * u
expr = sp.expand(expr.subs(sp.Derivative(y1f, (x, 2)), -Pf * sp.diff(y1f, x) - Qf * y1f))
ok("a2-114a-m2 代入後 u 項消失：y1 u''+(2y1'+P y1)u'", zero(expr - (y1f * sp.diff(u, x, 2) + (2 * sp.diff(y1f, x) + Pf * y1f) * sp.diff(u, x))))
w = sp.exp(-sp.Integral(Pf, x)) / y1f**2
ok("a2-114a-m2 w=e^{-∫P}/y1^2 滿足 y1 w'+(2y1'+P y1)w=0", zero(sp.simplify(y1f * sp.diff(w, x) + (2 * sp.diff(y1f, x) + Pf * y1f) * w)))
# 具體檢查公式：y''-6y'+9y=0, y1=e^{3x}
y2 = sp.exp(3 * x) * sp.integrate(sp.exp(-sp.integrate(-6, x)) / sp.exp(6 * x), x)
ok("降階公式用在 y''-6y'+9y=0 得 x e^{3x}", zero(y2 - x * sp.exp(3 * x)))
# a2-b4：y''-6y'+9y=0, y(0)=1, y'(0)=0 → (1-3x)e^{3x}
sol = (1 - 3 * x) * sp.exp(3 * x)
ok("a2-b4 方程與 IC", zero(L(-6, 9, sol)) and sol.subs(x, 0) == 1 and sp.diff(sol, x).subs(x, 0) == 0)
# 板書：(e^{3x}u)''-6(e^{3x}u)'+9e^{3x}u = e^{3x}u''
uu = sp.Function("u")(x)
ok("a2-b4 代入 y2=e^{3x}u 後只剩 e^{3x}u''", zero(L(-6, 9, sp.exp(3 * x) * uu) - sp.exp(3 * x) * sp.diff(uu, x, 2)))
# a2-hw2：4y''+4y'+y=0, y(0)=-2, y'(0)=1 → -2e^{-x/2}
sol = -2 * sp.exp(-x / 2)
ok("a2-hw2 方程與 IC（老師答案）", zero(4 * sp.diff(sol, x, 2) + 4 * sp.diff(sol, x) + sol) and sol.subs(x, 0) == -2 and sp.diff(sol, x).subs(x, 0) == 1)
# a2-s04-1：(1-x^2)y''-2xy'+2y=0, y1=x → y2=(x/2)ln((1+x)/(1-x))-1
xx = sp.symbols("xx")
y2 = x / 2 * sp.log((1 + x) / (1 - x)) - 1
ok("a2-s04-1 y1=x 是解", zero((1 - x**2) * 0 - 2 * x * 1 + 2 * x))
ok("a2-s04-1 y2 是解", zero(sp.simplify((1 - x**2) * sp.diff(y2, x, 2) - 2 * x * sp.diff(y2, x) + 2 * y2)))
Ppart = -2 * x / (1 - x**2)
ok("a2-s04-1 ∫P dx = ln(1-x^2)（|x|<1）", zero(sp.diff(sp.log(1 - x**2), x) - Ppart))
ok("a2-s04-1 部分分式 1/x^2+1/(1-x^2)", zero(sp.apart(1 / (x**2 * (1 - x**2)), x) - (1 / x**2 - 1 / (2 * (x - 1)) + 1 / (2 * (x + 1)))) and zero(1 / x**2 + 1 / (1 - x**2) - 1 / (x**2 * (1 - x**2))))
Wr = sp.simplify(x * sp.diff(y2, x) - y2 * 1)
ok("a2-s04-1 W(x,y2)=1/(1-x^2)", zero(sp.simplify(Wr - 1 / (1 - x**2))))
# a2-s04-2：y''-2y'+(1-ε^2)y=0, y(0)=0, y'(0)=1 → e^x sinh(εx)/ε → x e^x
eps = sp.symbols("epsilon", positive=True)
sol = sp.exp(x) * sp.sinh(eps * x) / eps
ok("a2-s04-2 方程", zero(sp.diff(sol, x, 2) - 2 * sp.diff(sol, x) + (1 - eps**2) * sol))
ok("a2-s04-2 IC", zero(sol.subs(x, 0)) and zero(sp.diff(sol, x).subs(x, 0) - 1))
lim = sp.limit(sol, eps, 0)
ok("a2-s04-2 ε→0 極限 x e^x", zero(lim - x * sp.exp(x)))
ok("a2-s04-2 極限是 ε=0 方程的解", zero(L(-2, 1, x * sp.exp(x))))

# ---------------- s05 阻尼振盪 ----------------
g_, w0, x0 = sp.symbols("gamma omega_0 x_0", positive=True)
# 欠阻尼：x=x0 e^{-γt}(cos ωt+(γ/ω) sin ωt), ω=√(ω0^2-γ^2)
om = sp.sqrt(w0**2 - g_**2)
xu = x0 * sp.exp(-g_ * t) * (sp.cos(om * t) + g_ / om * sp.sin(om * t))
ok("a2-b5 欠阻尼滿足 EOM", zero(sp.diff(xu, t, 2) + 2 * g_ * sp.diff(xu, t) + w0**2 * xu))
ok("a2-b5 欠阻尼 IC", zero(xu.subs(t, 0) - x0) and zero(sp.diff(xu, t).subs(t, 0)))
# 臨界：x=x0(1+γt)e^{-γt}
xc = x0 * (1 + g_ * t) * sp.exp(-g_ * t)
ok("a2-b5 臨界滿足 EOM（ω0=γ）", zero(sp.diff(xc, t, 2) + 2 * g_ * sp.diff(xc, t) + g_**2 * xc))
ok("a2-b5 臨界 IC", zero(xc.subs(t, 0) - x0) and zero(sp.diff(xc, t).subs(t, 0)))
# 過阻尼：x = x0/(λ1-λ2) (λ1 e^{λ2 t} - λ2 e^{λ1 t})
s_ = sp.sqrt(g_**2 - w0**2)
l1, l2 = -g_ + s_, -g_ - s_
xo = x0 / (l1 - l2) * (l1 * sp.exp(l2 * t) - l2 * sp.exp(l1 * t))
ok("a2-b5 過阻尼滿足 EOM", zero(sp.diff(xo, t, 2) + 2 * g_ * sp.diff(xo, t) + w0**2 * xo))
ok("a2-b5 過阻尼 IC", zero(xo.subs(t, 0) - x0) and zero(sp.diff(xo, t).subs(t, 0)))
ok("a2-b5 過阻尼係數 c1=-λ2 x0/(λ1-λ2) = x0(γ+s)/(2s)", zero(-l2 * x0 / (l1 - l2) - x0 * (g_ + s_) / (2 * s_)))
# a2-s05-1：臨界阻尼 x(0)=x0>0, v(0)=v0 → x=(x0+(v0+γx0)t)e^{-γt}；越過平衡 ⇔ v0<-γx0
v0 = sp.symbols("v_0", real=True)
xc2 = (x0 + (v0 + g_ * x0) * t) * sp.exp(-g_ * t)
ok("a2-s05-1 EOM", zero(sp.diff(xc2, t, 2) + 2 * g_ * sp.diff(xc2, t) + g_**2 * xc2))
ok("a2-s05-1 IC", zero(xc2.subs(t, 0) - x0) and zero(sp.diff(xc2, t).subs(t, 0) - v0))
tz = sp.solve(x0 + (v0 + g_ * x0) * t, t)[0]
ok("a2-s05-1 零點 t*=-x0/(v0+γx0)", zero(tz + x0 / (v0 + g_ * x0)))
# 數值：γ=2 s^-1, x0=0.1 m, v0=-0.5 m/s → t*=0.5 s, 最大越過量
num = {g_: 2, x0: sp.Rational(1, 10), v0: sp.Rational(-1, 2)}
ok("a2-s05-1 數值 t*=1/3 s", tz.subs(num) == sp.Rational(1, 3))
xn = xc2.subs(num)
tm = sp.solve(sp.diff(xn, t), t)
ok("a2-s05-1 最遠越過時刻 t=5/6 s", tm == [sp.Rational(5, 6)])
ok("a2-s05-1 最遠越過 x=-(3/20)e^{-5/3}=-0.02833 m", zero(xn.subs(t, sp.Rational(5, 6)) + sp.Rational(3, 20) * sp.exp(sp.Rational(-5, 3))) and abs(float(xn.subs(t, sp.Rational(5, 6))) + 0.02833) < 5e-6)
ok("a2-s05-1 越過的門檻 v0<-γx0=-0.2 m/s", -num[g_] * num[x0] == sp.Rational(-1, 5))
ok("a2-s05-1 v0+γx0=-0.3", num[v0] + num[g_] * num[x0] == sp.Rational(-3, 10))
# a2-s05-2：相鄰極大比 1/2、週期 T=1 s → γ=ln2, ω0=√(4π^2+(ln2)^2)
gam = sp.log(2) / 1
omd = 2 * sp.pi / 1
w0v = sp.sqrt(omd**2 + gam**2)
ok("a2-s05-2 γ=0.6931", abs(float(gam) - 0.6931) < 5e-5)
ok("a2-s05-2 ω0=6.321 rad/s", abs(float(w0v) - 6.321) < 5e-4)
ok("a2-s05-2 b/m=2γ=1.386", abs(float(2 * gam) - 1.386) < 5e-4)
ok("a2-s05-2 k/m=ω0^2=39.96", abs(float(w0v**2) - 39.96) < 5e-3)
ok("a2-s05-2 無阻尼週期 2π/ω0=0.9940 s", abs(float(2 * sp.pi / w0v) - 0.9940) < 5e-5)
ok("a2-s05-2 臨界需要 b/m=2ω0=12.64", abs(float(2 * w0v) - 12.64) < 5e-3)

# ---------------- s06 Cauchy–Euler ----------------
def CE(a, b, f):
    return X**2 * sp.diff(f, X, 2) + a * X * sp.diff(f, X) + b * f
# a2-hw3：4x^2y''+8xy'+y=0, y1=x^{-1/2} → y2=ln x/√x
y1 = 1 / sp.sqrt(X)
y2 = sp.log(X) / sp.sqrt(X)
ok("a2-hw3 y1 是解", zero(4 * X**2 * sp.diff(y1, X, 2) + 8 * X * sp.diff(y1, X) + y1))
ok("a2-hw3 y2 是解（老師答案）", zero(4 * X**2 * sp.diff(y2, X, 2) + 8 * X * sp.diff(y2, X) + y2))
y2f = y1 * sp.integrate(sp.exp(-sp.integrate(2 / X, X)) / y1**2, X)
ok("a2-hw3 降階公式 y1∫e^{-∫2/x}/y1^2 = ln x/√x", zero(y2f - y2))
m = sp.symbols("m")
ok("a2-hw3 指標方程 4m^2+4m+1=(2m+1)^2", zero(4 * m * (m - 1) + 8 * m + 1 - (2 * m + 1)**2))
# a2-113b-m4：x^2y''+xy'+λy=0, y(1)=0, y(5)=0 → λn=(nπ/ln5)^2, yn=sin(nπ ln x/ln5)
n = sp.symbols("n", positive=True, integer=True)
lam_n = (n * sp.pi / sp.log(5))**2
yn = sp.sin(n * sp.pi * sp.log(X) / sp.log(5))
ok("a2-113b-m4 yn 滿足方程", zero(CE(1, lam_n, yn)))
ok("a2-113b-m4 y(1)=0", zero(yn.subs(X, 1)))
ok("a2-113b-m4 y(5)=0", zero(sp.simplify(yn.subs(X, 5))))
mu = sp.symbols("mu", positive=True)
Mneg = sp.Matrix([[1, 1], [5**mu, 5**(-mu)]])
ok("a2-113b-m4 λ<0 行列式 5^{-μ}-5^{μ}≠0（只有零解）", zero(Mneg.det() - (5**(-mu) - 5**mu)) and (5**(-1.0) - 5**1.0) != 0)
ok("a2-113b-m4 λ=0：c1+c2 ln x，行列式 ln5≠0", zero(sp.Matrix([[1, 0], [1, sp.log(5)]]).det() - sp.log(5)))
ok("a2-113b-m4 λ1=(π/ln5)^2=3.810", abs(float(lam_n.subs(n, 1)) - 3.810) < 5e-4)
ok("a2-113b-m4 ln5=1.6094", abs(float(sp.log(5)) - 1.6094) < 5e-5)
# a2-s06-1：x^2y''-xy'+5y=0, y(1)=1, y'(1)=0 → x[cos(2ln x)-½ sin(2ln x)]
sol = X * (sp.cos(2 * sp.log(X)) - sp.sin(2 * sp.log(X)) / 2)
ok("a2-s06-1 方程", zero(CE(-1, 5, sol)))
ok("a2-s06-1 IC", zero(sol.subs(X, 1) - 1) and zero(sp.diff(sol, X).subs(X, 1)))
ok("a2-s06-1 指標方程 m^2-2m+5 根 1±2i", set(sp.solve(m * (m - 1) - m + 5, m)) == {1 + 2 * sp.I, 1 - 2 * sp.I})
xz = sp.exp(sp.atan(2) / 2)
ok("a2-s06-1 第一個零點 x=e^{atan(2)/2}=1.739", zero(sp.simplify(sol.subs(X, xz))) and abs(float(xz) - 1.739) < 5e-4)
# 代換 x=e^t：x^2 y'' + a x y' + b y → Y''+(a-1)Y'+bY
Y = sp.Function("Y")
tt = sp.symbols("tt", real=True)
Yx = Y(sp.log(X))
lhs = sp.simplify(CE(-1, 5, Yx))
rhs = (sp.Derivative(Y(tt), (tt, 2)) - 2 * sp.Derivative(Y(tt), tt) + 5 * Y(tt)).subs(tt, sp.log(X))
ok("a2-s06-1 x=e^t 後變成 Y''-2Y'+5Y", zero(sp.simplify(lhs - rhs.doit())))
# a2-s06-2：(2x+1)^2y''-2(2x+1)y'-12y=0 → c1(2x+1)^3+c2(2x+1)^{-1}
for f, nm in (((2 * x + 1)**3, "(2x+1)^3"), (1 / (2 * x + 1), "(2x+1)^{-1}")):
    ok(f"a2-s06-2 {nm} 是解", zero(sp.simplify((2 * x + 1)**2 * sp.diff(f, x, 2) - 2 * (2 * x + 1) * sp.diff(f, x) - 12 * f)))
ok("a2-s06-2 指標方程 4m(m-1)-4m-12=4(m-3)(m+1)", zero(4 * m * (m - 1) - 4 * m - 12 - 4 * (m - 3) * (m + 1)))
gen = c1 * (2 * x + 1)**3 + c2 / (2 * x + 1)
s = sp.solve([gen.subs(x, 0) - 2, sp.diff(gen, x).subs(x, 0) - 2], [c1, c2])
ok("a2-s06-2 IC y(0)=2,y'(0)=2 → c1=3/4, c2=5/4", s[c1] == sp.Rational(3, 4) and s[c2] == sp.Rational(5, 4))

# ---------------- 補充檢查 ----------------
ph = sp.atan2(1, 2)   # cos φ = 2/√5, sin φ = 1/√5
ok("a2-113a-m3 振幅相位 2√5 e^{-x/2}cos(2x+φ)", zero(sp.expand_trig(2 * sp.sqrt(5) * sp.exp(-x / 2) * sp.cos(2 * x + ph)) - sp.exp(-x / 2) * (4 * sp.cos(2 * x) - 2 * sp.sin(2 * x))))
ok("a2-s04-2 數值 e·sinh(0.01)/0.01=2.71833", abs(float(sp.E * sp.sinh(sp.Rational(1, 100)) * 100) - 2.71833) < 5e-6)
ok("a2-s06-1 cos(atan2)=0.447=½sin(atan2)", abs(float(sp.cos(sp.atan(2))) - 0.447) < 5e-4 and zero(sp.cos(sp.atan(2)) - sp.sin(sp.atan(2)) / 2))
ok("a2-113b-m4 λ2=15.24, λ3=34.29", abs(float(lam_n.subs(n, 2)) - 15.24) < 5e-3 and abs(float(lam_n.subs(n, 3)) - 34.29) < 5e-3)
ok("a2-s05-2 臨界/目前 b/m 比 9.12", abs(float(w0v / gam) - 9.12) < 5e-3)

# ---------------- 盤點報告中「不收」題目的附註 ----------------
f = 1 - x
ok("附註 110a-final Q4：y=1-x 滿足 xy''+(x-1)y'-y=0、y(0)=1、y(1)=0", zero(x * sp.diff(f, x, 2) + (x - 1) * sp.diff(f, x) - f) and f.subs(x, 0) == 1 and f.subs(x, 1) == 0)
ok("附註 110a-final Q4：e^{-x} 也是解", zero(x * sp.exp(-x) + (x - 1) * (-sp.exp(-x)) - sp.exp(-x)))
f = 1 + x - x**2
ok("附註 111a-final Q3：y=1+x-x^2 滿足 (x^2+1)y''-2xy'+2y=0、y(0)=1、y(1)=1", zero((x**2 + 1) * sp.diff(f, x, 2) - 2 * x * sp.diff(f, x) + 2 * f) and f.subs(x, 0) == 1 and f.subs(x, 1) == 1)

xs = (1 + 3 * t) * sp.exp(2 * t)
ys = (sp.diff(xs, t) + xs) / 3
ok("附註 110b-mid Q2：消去法 x''-4x'+4x=0，x=(1+3t)e^{2t}，x(0)=1、y(0)=2", zero(sp.diff(xs, t, 2) - 4 * sp.diff(xs, t) + 4 * xs) and xs.subs(t, 0) == 1 and ys.subs(t, 0) == 2 and zero(sp.diff(ys, t) - (-3 * xs + 5 * ys)))

# ---------------- 考前衝刺變化題 ----------------
sol = sp.exp(5 * x) - sp.exp(-x)
ok("a2var-1", zero(L(-4, -5, sol)) and sol.subs(x, 0) == 0 and sp.diff(sol, x).subs(x, 0) == 6)
sol = 2 * sp.exp(-3 * x) * (sp.cos(2 * x) + sp.sin(2 * x))
ok("a2var-2", zero(L(6, 13, sol)) and sol.subs(x, 0) == 2 and sp.diff(sol, x).subs(x, 0) == -2)
sol = (3 - x) * sp.exp(2 * x / 3)
ok("a2var-3", zero(9 * sp.diff(sol, x, 2) - 12 * sp.diff(sol, x) + 4 * sol) and sol.subs(x, 0) == 3 and sp.diff(sol, x).subs(x, 0) == 1)
ok("a2var-4 (a) sin3x 在 π/3 為 0、(b) sin(π/2)=1", zero(sp.sin(3 * sp.pi / 3)) and sp.sin(3 * sp.pi / 6) == 1 and zero(L(0, 9, sp.sin(3 * x))))
y2 = x + 1
ok("a2var-5 y1=e^x 與 y2=x+1 都是解", zero(x * sp.diff(sp.exp(x), x, 2) - (x + 1) * sp.diff(sp.exp(x), x) + sp.exp(x)) and zero(x * 0 - (x + 1) * 1 + y2))
ok("a2var-5 公式積分 e^x∫x e^{-x}dx = -(x+1)", zero(sp.exp(x) * sp.integrate(x * sp.exp(-x), x) + (x + 1)))
sol = X**2 * (1 - 2 * sp.log(X))
ok("a2var-6", zero(CE(-3, 4, sol)) and zero(sol.subs(X, 1) - 1) and zero(sp.diff(sol, X).subs(X, 1)))
sol = sp.Rational(4, 3) * sp.exp(-2 * t) - sp.Rational(1, 3) * sp.exp(-8 * t)
ok("a2var-7", zero(sp.diff(sol, t, 2) + 10 * sp.diff(sol, t) + 16 * sol) and sol.subs(t, 0) == 1 and sp.diff(sol, t).subs(t, 0) == 0)
ok("a2var-7 臨界 b=2√(km)=8", 2 * sp.sqrt(16 * 1) == 8)
sol = sp.exp(-x) * (3 * sp.cos(2 * x) - sp.sin(2 * x))
ok("a2var-8", zero(L(2, 5, sol)) and sol.subs(x, 0) == 3 and sp.diff(sol, x).subs(x, 0) == -5)

print()
print("全部通過" if not FAIL else f"失敗 {len(FAIL)} 項：{FAIL}")
sys.exit(1 if FAIL else 0)
