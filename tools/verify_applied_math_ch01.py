"""應用數學 第 1 章（一階常微分方程）：每一題的答案用 sympy 獨立驗算。

用法：python tools/verify_applied_math_ch01.py     全部通過時結束碼為 0。
驗法：
- 顯式解 y(x)：代回方程化簡為 0（必要時再加 checkodesol）＋ 初始條件。
- 隱式解 G(x,y)=C：檢查 dG 與 M dx + N dy 成比例（G_x N - G_y M = 0），並把初始點代入 G 得到 C。
- 數值答案：直接算出來比對。
"""
import sys

import sympy as sp

x, y, t = sp.symbols("x y t", real=True)
K, C0 = sp.symbols("K C0")
results = []


def ok(name, cond):
    results.append((name, bool(cond)))


def zero(expr):
    e = sp.simplify(sp.expand(expr))
    if e == 0:
        return True
    e = sp.simplify(sp.trigsimp(sp.expand_trig(e)))
    if e == 0:
        return True
    # 最後用數值抽查（隨機點）確認
    import random
    syms = sorted(e.free_symbols, key=str)
    for _ in range(6):
        vals = {s: random.uniform(0.3, 1.3) for s in syms}
        if abs(complex(e.evalf(subs=vals))) > 1e-9:
            return False
    return True


def implicit(name, G, M, N, pt, Cval):
    """G(x,y)=Cval 是 M dx + N dy = 0 過 pt 的解。"""
    ok(name + " dG∥(M,N)", zero(sp.diff(G, x) * N - sp.diff(G, y) * M))
    ok(name + " 初始點", zero(G.subs({x: pt[0], y: pt[1]}) - Cval))


def explicit(name, yexpr, ode_lhs, ic=None):
    """ode_lhs(Y, Yp) == 0 是方程；yexpr 是顯式解。"""
    yp = sp.diff(yexpr, x)
    ok(name + " 代回方程", zero(ode_lhs(yexpr, yp)))
    if ic is not None:
        ok(name + " 初始條件", zero(yexpr.subs(x, ic[0]) - ic[1]))


# ===== 板書例題 =====
# 9/16 可分離：dy/dx = (2x-8xy)/(x^2+4), y(0)=1
ys = sp.Rational(1, 4) + 192 / (x**2 + 4) ** 4
explicit("板書 可分離", ys, lambda Y, Yp: Yp - (2 * x - 8 * x * Y) / (x**2 + 4), (0, 1))
ok("板書 可分離 隱式形 C=-768", zero(((x**2 + 4) ** 4 * (1 - 4 * ys)) + 768))
f = sp.Function("f")
sol = sp.dsolve(sp.Eq(f(x).diff(x), (2 * x - 8 * x * f(x)) / (x**2 + 4)), f(x), ics={f(0): 1})
ok("板書 可分離 dsolve 一致", zero(sol.rhs - ys))

# 9/16 線性：y' + y = e^x sin x, y(0)=1
yl = sp.exp(x) / 5 * (2 * sp.sin(x) - sp.cos(x)) + sp.Rational(6, 5) * sp.exp(-x)
explicit("板書 線性", yl, lambda Y, Yp: Yp + Y - sp.exp(x) * sp.sin(x), (0, 1))
ok("板書 線性 積分", zero(sp.integrate(sp.exp(2 * x) * sp.sin(x), x) - sp.exp(2 * x) * (2 * sp.sin(x) - sp.cos(x)) / 5))

# 9/16 正合：(x^2-2xy)dx + (sin y - x^2)dy = 0, y(1)=0
M, N = x**2 - 2 * x * y, sp.sin(y) - x**2
ok("板書 正合 M_y=N_x", zero(sp.diff(M, y) - sp.diff(N, x)))
implicit("板書 正合", x**3 / 3 - x**2 * y - sp.cos(y), M, N, (1, 0), sp.Rational(-2, 3))

# 9/16 非正合：[3x sin2y - 2y]dx + [2x^2 cos2y - x]dy = 0，F = x
M, N = 3 * x * sp.sin(2 * y) - 2 * y, 2 * x**2 * sp.cos(2 * y) - x
D = sp.diff(M, y) - sp.diff(N, x)
ok("板書 非正合 Δ/N=1/x", zero(D / N - 1 / x))
ok("板書 非正合 F=x 後正合", zero(sp.diff(x * M, y) - sp.diff(x * N, x)))
implicit("板書 非正合", x**3 * sp.sin(2 * y) - x**2 * y, M, N, (1, 0), 0)

# 9/16 RC 放電、充電
R, Cc, eps, V0, w = sp.symbols("R C varepsilon V_0 omega", positive=True)
q = Cc * eps * sp.exp(-t / (R * Cc))
ok("板書 RC 放電 方程", zero(R * sp.diff(q, t) + q / Cc))
ok("板書 RC 放電 q(0)", zero(q.subs(t, 0) - Cc * eps))
ok("板書 RC 放電 i", zero(sp.diff(q, t) + eps / R * sp.exp(-t / (R * Cc))))
qc = Cc * eps * (1 - sp.exp(-t / (R * Cc)))
ok("補充 RC 充電 方程", zero(R * sp.diff(qc, t) + qc / Cc - eps))
ok("補充 RC 充電 q(0)=0", zero(qc.subs(t, 0)))

# 9/16 AC 驅動 RC：R q' + q/C = V0 sin wt
qa = Cc * V0 * (sp.sin(w * t) - w * R * Cc * sp.cos(w * t)) / (1 + w**2 * R**2 * Cc**2) + K * sp.exp(-t / (R * Cc))
ok("板書 AC RC 方程", zero(sp.diff(qa, t) + qa / (R * Cc) - V0 / R * sp.sin(w * t)))
ok("板書 AC RC 積分", zero(sp.integrate(V0 / R * sp.sin(w * t) * sp.exp(t / (R * Cc)), t)
                         - Cc * V0 * sp.exp(t / (R * Cc)) * (sp.sin(w * t) - w * R * Cc * sp.cos(w * t)) / (1 + w**2 * R**2 * Cc**2)))
phi = sp.atan(w * R * Cc)
ok("補充 AC 相位形", zero(Cc * V0 / sp.sqrt(1 + w**2 * R**2 * Cc**2) * sp.sin(w * t - phi)
                       - Cc * V0 * (sp.sin(w * t) - w * R * Cc * sp.cos(w * t)) / (1 + w**2 * R**2 * Cc**2)))
K0 = sp.solve(qa.subs(t, 0), K)[0]
ok("補充 AC q(0)=0 的 K", zero(K0 - Cc * V0 * w * R * Cc / (1 + w**2 * R**2 * Cc**2)))

# ===== 作業 =====
# 1. xy cos(y^2) y' + 2 sin(y^2) = 0, y(1)=sqrt(pi/2)  →  x^4 sin(y^2) = 1
implicit("作業1", x**4 * sp.sin(y**2), 2 * sp.sin(y**2), x * y * sp.cos(y**2), (1, sp.sqrt(sp.pi / 2)), 1)
# 2. y' = 1/(e^y - x), y(1)=0  →  x e^y = e^{2y}/2 + 1/2（即 x = cosh y）
X = sp.cosh(y)
ok("作業2 dx/dy = e^y - x", zero(sp.diff(X, y) - (sp.exp(y) - X)))
ok("作業2 x(0)=1", zero(X.subs(y, 0) - 1))
ok("作業2 與老師答案同式", zero(X * sp.exp(y) - (sp.exp(2 * y) / 2 + sp.Rational(1, 2))))
# 3. x y' + (1+x) y = e^{-x} sin 2x
y3 = -sp.exp(-x) * sp.cos(2 * x) / (2 * x) + K * sp.exp(-x) / x
explicit("作業3", y3, lambda Y, Yp: x * Yp + (1 + x) * Y - sp.exp(-x) * sp.sin(2 * x))
# 4.（＝110上期中第 1 題）(2y+e^y+6x^2) y' + 4 + 12xy = 0, y(0)=0
M, N = 4 + 12 * x * y, 2 * y + sp.exp(y) + 6 * x**2
ok("作業4/110上期中1 M_y=N_x", zero(sp.diff(M, y) - sp.diff(N, x)))
implicit("作業4/110上期中1", 4 * x + 6 * x**2 * y + y**2 + sp.exp(y), M, N, (0, 0), 1)
# 5. cos y dx - 2(x-y) sin y dy - cos y dy = 0, y(1)=0  →  (x-y)cos^2 y = 1
M, N = sp.cos(y), -2 * (x - y) * sp.sin(y) - sp.cos(y)
D = sp.diff(M, y) - sp.diff(N, x)
ok("作業5 -Δ/M = -tan y", zero(-D / M + sp.tan(y)))
ok("作業5 F=cos y 後正合", zero(sp.diff(sp.cos(y) * M, y) - sp.diff(sp.cos(y) * N, x)))
implicit("作業5", (x - y) * sp.cos(y) ** 2, M, N, (1, 0), 1)

# ===== 考古題 =====
# 110上期中 2：m v' = m g - k v^2, v(0)=0
m, g, k = sp.symbols("m g k", positive=True)
v = sp.sqrt(m * g / k) * sp.tanh(sp.sqrt(g * k / m) * t)
ok("110上期中2 方程", zero(m * sp.diff(v, t) - (m * g - k * v**2)))
ok("110上期中2 v(0)=0", zero(v.subs(t, 0)))
ok("110上期中2 終端速度", zero(sp.limit(v, t, sp.oo) - sp.sqrt(m * g / k)))
# 111上期中 1：(y^2+xy^3)dx + (5y^2-xy+y^3 sin y)dy = 0, y(0)=pi/2
M, N = y**2 + x * y**3, 5 * y**2 - x * y + y**3 * sp.sin(y)
D = sp.diff(M, y) - sp.diff(N, x)
ok("111上期中1 Δ/M = 3/y", zero(D / M - 3 / y))
ok("111上期中1 F=y^-3 後正合", zero(sp.diff(M / y**3, y) - sp.diff(N / y**3, x)))
implicit("111上期中1", x / y + x**2 / 2 + 5 * sp.log(y) - sp.cos(y), M, N, (0, sp.pi / 2), 5 * sp.log(sp.pi / 2))
ok("111上期中1 5ln(pi/2)≈2.258", abs(float(5 * sp.log(sp.pi / 2)) - 2.258) < 5e-4)
# 112上期中 1：dy + (2xy - x e^{-x^2})dx = 0, y(0)=1
explicit("112上期中1", (x**2 / 2 + 1) * sp.exp(-x**2), lambda Y, Yp: Yp + 2 * x * Y - x * sp.exp(-x**2), (0, 1))
# 112上期中 2：(2x e^{3y}+e^x)dx + (3x^2 e^{3y}-y^2)dy = 0, y(0)=1
M, N = 2 * x * sp.exp(3 * y) + sp.exp(x), 3 * x**2 * sp.exp(3 * y) - y**2
ok("112上期中2 M_y=N_x", zero(sp.diff(M, y) - sp.diff(N, x)))
implicit("112上期中2", x**2 * sp.exp(3 * y) + sp.exp(x) - y**3 / 3, M, N, (0, 1), sp.Rational(2, 3))
# 113上期中 1：(e^{2y} - y cos xy)dx + (2x e^{2y} - x cos xy + 2y)dy = 0, (0,2)
M, N = sp.exp(2 * y) - y * sp.cos(x * y), 2 * x * sp.exp(2 * y) - x * sp.cos(x * y) + 2 * y
ok("113上期中1 M_y=N_x", zero(sp.diff(M, y) - sp.diff(N, x)))
implicit("113上期中1", x * sp.exp(2 * y) - sp.sin(x * y) + y**2, M, N, (0, 2), 4)
# 113上期中 2：y' + y^2 = 9, y(0)=0
explicit("113上期中2", 3 * sp.tanh(3 * x), lambda Y, Yp: Yp + Y**2 - 9, (0, 0))
# 114上期中 1：(x^2-x-2) y' + 3xy = x^2-4x+4, y(1)=1
y14 = ((x - 2) ** 4 + 7) / (4 * (x - 2) ** 2 * (x + 1))
explicit("114上期中1", y14, lambda Y, Yp: (x**2 - x - 2) * Yp + 3 * x * Y - (x**2 - 4 * x + 4), (1, 1))
ok("114上期中1 部分分式", zero(3 * x / ((x - 2) * (x + 1)) - (2 / (x - 2) + 1 / (x + 1))))

# ===== 自編難題 =====
# 01a：y' = (x+y+1)^2, y(0) = -1
explicit("自編01a", sp.tan(x) - x - 1, lambda Y, Yp: Yp - (x + Y + 1) ** 2, (0, -1))
# 01b：x y' = y^2 - 1
explicit("自編01b(a)", (1 - x**2) / (1 + x**2), lambda Y, Yp: x * Yp - (Y**2 - 1), (1, 0))
ok("自編01b(b) y≡-1", zero((sp.Integer(-1)) ** 2 - 1))
explicit("自編01b(c)", (2 + x**2) / (2 - x**2), lambda Y, Yp: x * Yp - (Y**2 - 1), (1, 3))
ok("自編01b(c) 爆掉在 √2", sp.solve(2 - x**2, x) == [-sp.sqrt(2), sp.sqrt(2)])
# 02a：Bernoulli y' + y/x = x y^2, y(1)=1
explicit("自編02a", 1 / (2 * x - x**2), lambda Y, Yp: Yp + Y / x - x * Y**2, (1, 1))
# 02b：y' + 2y = g(x)（0≤x≤1 為 1，之後為 0），y(0)=0
y1 = (1 - sp.exp(-2 * x)) / 2
y2 = (sp.exp(2) - 1) * sp.exp(-2 * x) / 2
explicit("自編02b 第一段", y1, lambda Y, Yp: Yp + 2 * Y - 1, (0, 0))
explicit("自編02b 第二段", y2, lambda Y, Yp: Yp + 2 * Y)
ok("自編02b x=1 連續", zero(y1.subs(x, 1) - y2.subs(x, 1)))
ok("自編02b y(1)≈0.4323", abs(float(y1.subs(x, 1)) - 0.4323) < 5e-5)
ok("自編02b y(2)≈0.0585", abs(float(y2.subs(x, 2)) - 0.0585) < 5e-5)
# 03a：M = y cos x + 2x e^y，N = sin x + x^2 e^y + y，y(0)=1
M = y * sp.cos(x) + 2 * x * sp.exp(y)
N = sp.sin(x) + x**2 * sp.exp(y) + y
ok("自編03a M_y=N_x", zero(sp.diff(M, y) - sp.diff(N, x)))
implicit("自編03a", y * sp.sin(x) + x**2 * sp.exp(y) + y**2 / 2, M, N, (0, 1), sp.Rational(1, 2))
# 03b：(2xy+3)dx + (x^2-1)dy = 0, y(0)=2
explicit("自編03b", (2 + 3 * x) / (1 - x**2), lambda Y, Yp: (2 * x * Y + 3) + (x**2 - 1) * Yp, (0, 2))
# 04a：(3y+4xy^2)dx + (2x+3x^2y)dy = 0，μ = x^2 y，y(1)=1
M, N = 3 * y + 4 * x * y**2, 2 * x + 3 * x**2 * y
a, b = sp.symbols("a b")
mu = x**a * y**b
cond = sp.expand(sp.powsimp(sp.expand((sp.diff(mu * M, y) - sp.diff(mu * N, x)) * x**(-a) * y**(-b)), force=True))
ab = sp.solve(sp.Poly(cond, x, y).coeffs(), [a, b], dict=True)
ok("自編04a 解出 a=2,b=1", ab == [{a: 2, b: 1}])
ok("自編04a x^2y 後正合", zero(sp.diff(x**2 * y * M, y) - sp.diff(x**2 * y * N, x)))
D = sp.diff(M, y) - sp.diff(N, x)
ok("自編04a Δ/N 含 y（F(x) 不行）", sp.simplify(D / N).has(y))
ok("自編04a Δ/M 含 x（F(y) 不行）", sp.simplify(D / M).has(x))
implicit("自編04a", x**3 * y**2 + x**4 * y**3, M, N, (1, 1), 2)
# 04b：y dx + (2x - y e^y)dy = 0，F = y，y(0)=1（x=0 時 y=1）
M, N = y, 2 * x - y * sp.exp(y)
D = sp.diff(M, y) - sp.diff(N, x)
ok("自編04b -Δ/M = 1/y", zero(-D / M - 1 / y))
implicit("自編04b", x * y**2 - (y**2 - 2 * y + 2) * sp.exp(y), M, N, (0, 1), -sp.E)
xs = ((y**2 - 2 * y + 2) * sp.exp(y) - sp.E) / y**2
ok("自編04b 線性(x 為未知)", zero(sp.diff(xs, y) + 2 * xs / y - sp.exp(y)))
# 05a：混合槽 Q' = 6 - 2Q/(100+t), Q(0)=0
Q = 2 * (100 + t) - 2 * 10**6 / (100 + t) ** 2
ok("自編05a 方程", zero(sp.diff(Q, t) - (6 - 2 * Q / (100 + t))))
ok("自編05a Q(0)=0", zero(Q.subs(t, 0)))
ok("自編05a Q(100)=350", zero(Q.subs(t, 100) - 350))
# 05b：上拋 v^2 阻力：v' = -g(1+v^2/vt^2)
vt_, v0_, gg = sp.symbols("v_t v_0 g", positive=True)
vv = vt_ * sp.tan(sp.atan(v0_ / vt_) - gg * t / vt_)
ok("自編05b v(t) 方程", zero(sp.diff(vv, t) + gg * (1 + vv**2 / vt_**2)))
ok("自編05b v(0)=v0", zero(vv.subs(t, 0) - v0_))
Y = sp.symbols("Y")
hh = vt_**2 / (2 * gg) * sp.log(1 + v0_**2 / vt_**2)
vy = sp.sqrt((vt_**2 + v0_**2) * sp.exp(-2 * gg * Y / vt_**2) - vt_**2)  # v(y) 上升段
ok("自編05b v dv/dy 方程", zero(vy * sp.diff(vy, Y) + gg * (1 + vy**2 / vt_**2)))
ok("自編05b v(h)=0", zero(vy.subs(Y, hh)))
num = {vt_: 30, v0_: 20, gg: 9.8}
ok("自編05b t_top≈1.800 s", abs(float((vt_ / gg * sp.atan(v0_ / vt_)).subs(num)) - 1.800) < 5e-4)
ok("自編05b h≈16.89 m", abs(float(hh.subs(num)) - 16.885) < 5e-3)
ok("自編05b 真空 2.041 s / 20.41 m", abs(20 / 9.8 - 2.041) < 5e-4 and abs(400 / 19.6 - 20.41) < 5e-3)

# ===== 考前衝刺 變化題 =====
# 1：y' = y cos x/(1+2y^2), y(0)=1 → ln y + y^2 = sin x + 1
implicit("變化1", sp.log(y) + y**2 - sp.sin(x), y * sp.cos(x), -(1 + 2 * y**2), (0, 1), 1)
# 2：y' = (1+y^2)/(1+x^2), y(0)=1 → y = (1+x)/(1-x)
explicit("變化2", (1 + x) / (1 - x), lambda Y, Yp: Yp - (1 + Y**2) / (1 + x**2), (0, 1))
# 3：y' - 2y/x = x^2 cos x, y(pi/2)=0 → y = x^2 (sin x - 1)
explicit("變化3", x**2 * (sp.sin(x) - 1), lambda Y, Yp: Yp - 2 * Y / x - x**2 * sp.cos(x), (sp.pi / 2, 0))
# 4：y' = y/(2x + y^3 e^y) → x = y^2 (e^y + C)
Xc = y**2 * (sp.exp(y) + C0)
ok("變化4 dx/dy", zero(sp.diff(Xc, y) - (2 * Xc + y**3 * sp.exp(y)) / y))
# 5：(x+y)^2 dx + (2xy + x^2 - 1) dy = 0, y(1)=1
M, N = (x + y) ** 2, 2 * x * y + x**2 - 1
ok("變化5 M_y=N_x", zero(sp.diff(M, y) - sp.diff(N, x)))
implicit("變化5", x**3 / 3 + x**2 * y + x * y**2 - y, M, N, (1, 1), sp.Rational(4, 3))
# 6：(x^2+y^2+x)dx + xy dy = 0，F = x
M, N = x**2 + y**2 + x, x * y
ok("變化6 Δ/N = 1/x", zero((sp.diff(M, y) - sp.diff(N, x)) / N - 1 / x))
ok("變化6 dG∥", zero(sp.diff(x**4 / 4 + x**2 * y**2 / 2 + x**3 / 3, x) * N - sp.diff(x**4 / 4 + x**2 * y**2 / 2 + x**3 / 3, y) * M))
# 7：2xy dx + (y^2 - 3x^2) dy = 0，F = y^-4 → x^2 - y^2 = C y^3
M, N = 2 * x * y, y**2 - 3 * x**2
ok("變化7 -Δ/M = -4/y", zero(-(sp.diff(M, y) - sp.diff(N, x)) / M + 4 / y))
G7 = (x**2 - y**2) / y**3
ok("變化7 dG∥", zero(sp.diff(G7, x) * N - sp.diff(G7, y) * M))
# 8：冷卻 T(0)=90、T(10)=60、環境 20：何時 30
kk = sp.log(sp.Rational(7, 4)) / 10
ok("變化8 T(10)=60", zero(20 + 70 * sp.exp(-kk * 10) - 60))
ok("變化8 t≈34.8 min", abs(float(sp.log(7) / kk) - 34.77) < 5e-3)
# 9：RC 充電 R=10kΩ、C=100μF、ε=12V：到 90% 的時間
tau = 10e3 * 100e-6
ok("變化9 τ=1 s", abs(tau - 1.0) < 1e-12)
ok("變化9 t=τ ln10≈2.30 s", abs(tau * float(sp.log(10)) - 2.3026) < 5e-4)
ok("變化9 i(0)=1.2 mA", abs(12 / 10e3 - 1.2e-3) < 1e-12)
# 10：Bernoulli y' + y = y^3, y(0)=1/2 → y = 1/sqrt(1+3e^{2x})
explicit("變化10", 1 / sp.sqrt(1 + 3 * sp.exp(2 * x)), lambda Y, Yp: Yp + Y - Y**3, (0, sp.Rational(1, 2)))

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    bad = [n for n, r in results if not r]
    for n, r in results:
        print(("PASS " if r else "FAIL ") + n)
    print(f"共 {len(results)} 項，失敗 {len(bad)} 項")
    sys.exit(1 if bad else 0)
