"""應用數學第 5 章（Frobenius 法、Legendre 方程式）：每張題目卡的答案用 sympy 獨立驗算。

做法：
- Frobenius 級數：y = x^r Σ c_k x^k 代入，逐階解出係數（獨立重算），和網站的數字比對；
  指標方程式由 x^r 的最低次係數求出。
- 含 ln x 的第二解：把 y2 = k·y1·ln x + x^r Σ b_k x^k 代入，ln x 的係數與其餘係數分開要求為 0。
- 有 closed form 的：sympy.checkodesol／直接代入；初始、邊界條件直接代入。
- Legendre：sympy.legendre 比對、遞迴關係與積分直接計算。

用法：python tools/verify_applied_math_ch05.py   全部通過時印出 ALL CHECKS PASSED。
"""
import sys
import sympy as sp

x = sp.symbols("x", positive=True)
r = sp.symbols("r")
R = sp.Rational
FAILS = []
COUNT = [0]


def check(name, cond):
    COUNT[0] += 1
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAILS.append(name)


def D(y, n=1):
    return sp.diff(y, x, n)


def indicial(L):
    """L(x^r) 的最低次係數（除以 x^r 之後在 x→0 的首項）。"""
    e = sp.expand(sp.simplify(L(x**r) / x**r))
    # e 是 x 的 Laurent 多項式；取最低次項的係數
    e = sp.expand(e)
    terms = sp.Add.make_args(e)
    powers = {}
    for term in terms:
        c, p = term.as_coeff_exponent(x)
        coeff = sp.simplify(term / x**p)
        powers[p] = powers.get(p, 0) + coeff
    lo = min(p for p in powers if sp.simplify(powers[p]) != 0)
    return sp.factor(powers[lo]), lo


def frob_coeffs(L, rr, N, free=None):
    """y = x^rr Σ c_k x^k，c0=1，逐階解出 c1..cN；free={k: value} 指定可自由選的係數。"""
    c = sp.symbols(f"c0:{N + 1}")
    y = x**rr * sum(c[k] * x**k for k in range(N + 1))
    res = sp.expand(sp.simplify(sp.expand(L(y)) / x**rr))
    sol = {c[0]: 1}
    if free:
        sol.update({c[k]: v for k, v in free.items()})
    # 殘差的最低次方
    _, lo = indicial(L)
    for j in range(N):
        eq = sp.expand(res.coeff(x, lo + j + 1).subs(sol)) if True else 0
        unknown = [s for s in eq.free_symbols if s in c and s not in sol]
        if unknown:
            sol[unknown[-1]] = sp.solve(eq, unknown[-1])[0]
        elif sp.simplify(eq) != 0:
            return None  # 矛盾：這個指標根做不出級數解
    return [sp.nsimplify(sol.get(c[k], sp.nan)) for k in range(N + 1)]


def log_second(L, y1, rr, N, b0=1, free_b=None, k_val=None):
    """y2 = k y1 ln x + x^rr Σ b_j x^j（b0 給定），回傳所有解（k 與 b_j）。
    y1 要截斷到夠高次；只取殘差最低的 N 階方程式（更高階會被截斷影響）。"""
    k = sp.symbols("k")
    b = sp.symbols(f"b0:{N + 1}")
    y2 = k * y1 * sp.log(x) + x**rr * sum(b[j] * x**j for j in range(N + 1))
    full = sp.expand(L(y2))
    logpart = sp.expand(full.coeff(sp.log(x)))
    rest = sp.expand((full - logpart * sp.log(x)) * x**(-rr) * x**6)
    poly = sp.Poly(rest, x)
    coeffs = {m[0]: c for m, c in zip(poly.monoms(), poly.coeffs())}
    lo = min(coeffs)
    sol = {b[0]: b0}
    if free_b:
        sol.update({b[j]: v for j, v in free_b.items()})
    eqs = [sp.expand(coeffs.get(lo + j, 0)) for j in range(N)]
    if k_val is not None:
        sol[k] = k_val
    unknowns = ([] if k_val is not None else [k]) + [b[j] for j in range(N + 1) if b[j] not in sol]
    return sp.solve([q.subs(sol) for q in eqs], unknowns, dict=True), logpart


# ================================================================ §1 板書 10/7：2x²y''-xy'+(1+x)y=0
L = lambda y: 2 * x**2 * D(y, 2) - x * D(y) + (1 + x) * y
ind, _ = indicial(L)
check("am5-ex-1 indicial 2γ²-3γ+1=(2γ-1)(γ-1)", sp.expand(ind - (2 * r**2 - 3 * r + 1)) == 0)
c1 = frob_coeffs(L, 1, 6)
c2 = frob_coeffs(L, R(1, 2), 6)
check("am5-ex-1 γ=1: 1,-1/3,1/30,-1/630", c1[:4] == [1, R(-1, 3), R(1, 30), R(-1, 630)])
check("am5-ex-1 γ=1/2: 1,-1,1/6,-1/90", c2[:4] == [1, -1, R(1, 6), R(-1, 90)])
check("am5-ex-1 γ=1 general term (-1)^n 2^n/(2n+1)!", all(c1[n] == R((-1)**n * 2**n, sp.factorial(2 * n + 1)) for n in range(7)))
check("am5-ex-1 γ=1/2 general term (-1)^n 2^n/(2n)!", all(c2[n] == R((-1)**n * 2**n, sp.factorial(2 * n)) for n in range(7)))
Y1 = sp.sqrt(x / 2) * sp.sin(sp.sqrt(2 * x))
Y2 = sp.sqrt(x) * sp.cos(sp.sqrt(2 * x))
check("am5-ex-1 closed form sqrt(x/2) sin sqrt(2x) solves", sp.simplify(L(Y1)) == 0)
check("am5-ex-1 closed form sqrt(x) cos sqrt(2x) solves", sp.simplify(L(Y2)) == 0)
check("am5-ex-1 recurrence a_n = -a_{n-1}/((2n+2γ-1)(n+γ-1))", all(c1[n] == -c1[n - 1] / ((2 * n + 1) * n) for n in range(1, 6)) and all(c2[n] == -c2[n - 1] / (n * (2 * n - 1)) for n in range(1, 6)))

# ================================================================ §1 作業 1：2x²y''+3xy'+(2x-1)y=0
L = lambda y: 2 * x**2 * D(y, 2) + 3 * x * D(y) + (2 * x - 1) * y
ind, _ = indicial(L)
check("am5-hw-1 indicial (2r-1)(r+1)", sp.expand(ind - (2 * r - 1) * (r + 1)) == 0)
cA = frob_coeffs(L, -1, 5)
cB = frob_coeffs(L, R(1, 2), 5)
check("am5-hw-1 y1 = x^-1(1+2x-2x^2+4/9 x^3)", cA[:4] == [1, 2, -2, R(4, 9)])
check("am5-hw-1 y2 = sqrt x(1-2/5x+2/35x^2-4/945x^3)", cB[:4] == [1, R(-2, 5), R(2, 35), R(-4, 945)])
check("am5-hw-1 next terms: y1 a4=-2/45, y2 a4=2/10395", cA[4] == R(-2, 45) and cB[4] == R(2, 10395))

# ================================================================ §1 自編 a：4xy''+2y'+y=0
L = lambda y: 4 * x * D(y, 2) + 2 * D(y) + y
ind, _ = indicial(L)
check("am5-sf-01a indicial 2r(2r-1)", sp.expand(ind - 2 * r * (2 * r - 1)) == 0)
check("am5-sf-01a cos sqrt x and sin sqrt x solve", sp.simplify(L(sp.cos(sp.sqrt(x)))) == 0 and sp.simplify(L(sp.sin(sp.sqrt(x)))) == 0)
cc = frob_coeffs(L, 0, 5)
cs_ = frob_coeffs(L, R(1, 2), 5)
check("am5-sf-01a r=0 coefficients (-1)^n/(2n)!", all(cc[n] == R((-1)**n, sp.factorial(2 * n)) for n in range(6)))
check("am5-sf-01a r=1/2 coefficients (-1)^n/(2n+1)!", all(cs_[n] == R((-1)**n, sp.factorial(2 * n + 1)) for n in range(6)))
ysol = 3 * sp.cos(sp.sqrt(x)) - 2 * sp.sin(sp.sqrt(x))
check("am5-sf-01a y(0)=3 bounded combination; y(pi^2/4)= -2", ysol.subs(x, 0) == 3 and sp.simplify(ysol.subs(x, sp.pi**2 / 4)) == -2)

# ================================================================ §1 自編 b：2xy''+(1+x)y'+y=0
L = lambda y: 2 * x * D(y, 2) + (1 + x) * D(y) + y
ind, _ = indicial(L)
check("am5-sf-01b indicial r(2r-1)", sp.expand(ind - r * (2 * r - 1)) == 0)
c0_ = frob_coeffs(L, 0, 6)
ch = frob_coeffs(L, R(1, 2), 6)
check("am5-sf-01b r=0: 1,-1,1/3,-1/15,1/105", c0_[:5] == [1, -1, R(1, 3), R(-1, 15), R(1, 105)])
check("am5-sf-01b r=1/2: (-1/2)^n/n!", all(ch[n] == R((-1)**n, 2**n * sp.factorial(n)) for n in range(7)))
check("am5-sf-01b closed form sqrt(x) e^{-x/2} solves", sp.simplify(L(sp.sqrt(x) * sp.exp(-x / 2))) == 0)

# ================================================================ §2 板書 10/14：(x²-x)y''+(3x-1)y'+y=0
L = lambda y: (x**2 - x) * D(y, 2) + (3 * x - 1) * D(y) + y
ind, lo = indicial(L)
check("am5-ex-2 indicial -γ² (double root 0)", sp.expand(ind + r**2) == 0 and lo == -1)
cq = frob_coeffs(L, 0, 6)
check("am5-ex-2 a_{n+1}=a_n ⇒ all 1", cq == [1] * 7)
check("am5-ex-2 y1=1/(1-x) solves", sp.simplify(L(1 / (1 - x))) == 0)
check("am5-ex-2 y2=ln x/(1-x) solves", sp.simplify(L(sp.log(x) / (1 - x))) == 0)
P = (3 * x - 1) / (x**2 - x)
check("am5-ex-2 partial fractions P=1/x+2/(x-1)", sp.simplify(P - (1 / x + 2 / (x - 1))) == 0)
check("am5-ex-2 e^{-∫P}/y1^2 = 1/x", sp.simplify(sp.exp(-(sp.log(x) + 2 * sp.log(1 - x))) * (1 - x)**2 - 1 / x) == 0)
# 降階法的公式本身：y=u y1 代入
u = sp.Function("u")
y1f = sp.Function("y1")
pp = sp.Function("p")
qq = sp.Function("q")
expr = sp.expand(D(u(x) * y1f(x), 2) + pp(x) * D(u(x) * y1f(x)) + qq(x) * u(x) * y1f(x))
expr_r = expr.subs(D(y1f(x), 2), -pp(x) * D(y1f(x)) - qq(x) * y1f(x))
check("am5-ex-2 reduction: y1 u''+(2y1'+p y1)u'=0", sp.simplify(sp.expand(expr_r) - (y1f(x) * D(u(x), 2) + (2 * D(y1f(x)) + pp(x) * y1f(x)) * D(u(x)))) == 0)

# ================================================================ §2 自編 a：xy''+(1-x)y'-y=0
L = lambda y: x * D(y, 2) + (1 - x) * D(y) - y
ind, _ = indicial(L)
check("am5-sf-02a indicial r^2", sp.expand(ind - r**2) == 0)
check("am5-sf-02a y1=e^x", sp.simplify(L(sp.exp(x))) == 0)
uprime = sp.exp(-sp.integrate((1 - x) / x, x)) / sp.exp(2 * x)
check("am5-sf-02a u'=e^{-x}/x", sp.simplify(uprime - sp.exp(-x) / x) == 0)
useries = sp.log(x) - x + x**2 / 4 - x**3 / 18 + x**4 / 96
y2 = sp.exp(x) * useries
res = sp.series(sp.expand(L(y2)), x, 0, 4).removeO()
check("am5-sf-02a y2=e^x(ln x - x + x²/4 - x³/18 + x⁴/96) residual O(x^4)", sp.simplify(res) == 0)
y2s = sp.expand(sp.series(sp.exp(x) * (-x + x**2 / 4 - x**3 / 18), x, 0, 4).removeO())
check("am5-sf-02a non-log part -x - 3x²/4 - 11x³/36", sp.expand(y2s - (-x - R(3, 4) * x**2 - R(11, 36) * x**3)) == 0)

# ================================================================ §2 自編 b：x²y''+3xy'+(1+x)y=0
L = lambda y: x**2 * D(y, 2) + 3 * x * D(y) + (1 + x) * y
ind, _ = indicial(L)
check("am5-sf-02b indicial (r+1)^2", sp.expand(ind - (r + 1)**2) == 0)
cy = frob_coeffs(L, -1, 8)
check("am5-sf-02b y1 coefficients (-1)^n/(n!)^2", all(cy[n] == R((-1)**n, sp.factorial(n)**2) for n in range(9)))
Y1 = sum(cy[n] * x**(n - 1) for n in range(9))
s, logpart = log_second(L, Y1, -1, 4, b0=0, k_val=1)
check("am5-sf-02b y2=y1 ln x + x^-1(2x - 3/4 x^2 + 11/108 x^3 - 25/3456 x^4)", any(d.get(sp.Symbol("b1")) == 2 and d.get(sp.Symbol("b2")) == R(-3, 4) and d.get(sp.Symbol("b3")) == R(11, 108) and d.get(sp.Symbol("b4")) == R(-25, 3456) for d in s))

# ================================================================ §3 板書 10/14：xy''+3y'-y=0
L = lambda y: x * D(y, 2) + 3 * D(y) - y
ind, _ = indicial(L)
check("am5-ex-3 indicial γ(γ+2)", sp.expand(ind - r * (r + 2)) == 0)
cz = frob_coeffs(L, 0, 6)
check("am5-ex-3 γ=0: 1,1/3,1/24,1/360 (= 2/(n!(n+2)!))", cz[:4] == [1, R(1, 3), R(1, 24), R(1, 360)] and all(cz[n] == R(2, sp.factorial(n) * sp.factorial(n + 2)) for n in range(7)))
check("am5-ex-3 γ=-2 fails (contradiction)", frob_coeffs(L, -2, 4) is None)
Y1 = sum(cz[n] * x**n for n in range(7))
up = sp.series(1 / (x**3 * Y1**2), x, 0, 1).removeO()
check("am5-ex-3 u'=x^-3(1-2/3x+1/4x^2-19/270x^3...)", sp.expand(up - (x**-3 - R(2, 3) * x**-2 + R(1, 4) / x - R(19, 270))) == 0)
uu = -1 / (2 * x**2) + 2 / (3 * x) + sp.log(x) / 4
check("am5-ex-3 u=-1/(2x²)+2/(3x)+ln x/4 - ...", sp.simplify(D(uu) - (x**-3 - R(2, 3) * x**-2 + R(1, 4) / x)) == 0)
y2 = sp.expand(Y1 * (uu - R(19, 270) * x))
res = sp.series(sp.expand(L(y2)), x, 0, 0).removeO()
check("am5-ex-3 y2=u y1 residual vanishes through x^-1", sp.simplify(res) == 0)
y2nonlog = sp.series(sp.expand(Y1 * (-1 / (2 * x**2) + 2 / (3 * x) - R(19, 270) * x)), x, 0, 1).removeO()
check("am5-ex-3 y2 = 1/4 y1 ln x + x^-2(-1/2 + x/2 + 29/144 x^2 ...)", sp.expand(y2nonlog - (-1 / (2 * x**2) + 1 / (2 * x) + R(29, 144))) == 0)

# ================================================================ §3 作業 2：xy''-xy'+y=0
L = lambda y: x * D(y, 2) - x * D(y) + y
ind, _ = indicial(L)
check("am5-hw-2 indicial r(r-1)", sp.expand(ind - r * (r - 1)) == 0)
check("am5-hw-2 y1=x", sp.simplify(L(x)) == 0)
check("am5-hw-2 r=0 fails", frob_coeffs(L, 0, 3) is None)
y2 = x * sp.log(x) - 1 + x**2 / 2 + x**3 / 12 + x**4 / 72 + x**5 / 480
res = sp.series(sp.expand(L(y2)), x, 0, 5).removeO()
check("am5-hw-2 teacher y2 = x ln x - 1 + x²/2 + x³/12 + x⁴/72 (residual O(x^5))", sp.simplify(res) == 0)
check("am5-hw-2 reduction: e^{x}/x² integrand", sp.simplify(sp.exp(-sp.integrate(-1, x)) / x**2 - sp.exp(x) / x**2) == 0)

# ================================================================ §3 考古 110上期末 4：xy''+(x-1)y'-y=0, y(0)=1, y(1)=0
L = lambda y: x * D(y, 2) + (x - 1) * D(y) - y
ind, _ = indicial(L)
check("am5-k110-4 indicial r(r-2)", sp.expand(ind - r * (r - 2)) == 0)
cbig = frob_coeffs(L, 2, 6)
check("am5-k110-4 r=2: a_n=-a_{n-1}/(n+2) → 2(-1)^n/(n+2)!", all(cbig[n] == R(2 * (-1)**n, sp.factorial(n + 2)) for n in range(7)))
csmall = frob_coeffs(L, 0, 6, free={2: 0})
check("am5-k110-4 r=0 with a2=0: 1-x exactly", csmall == [1, -1, 0, 0, 0, 0, 0])
check("am5-k110-4 1-x and e^{-x} solve", sp.simplify(L(1 - x)) == 0 and sp.simplify(L(sp.exp(-x))) == 0)
check("am5-k110-4 r=2 series = 2(e^{-x}-1+x)", sp.simplify(sp.series(2 * (sp.exp(-x) - 1 + x), x, 0, 9).removeO() - sum(cbig[n] * x**(n + 2) for n in range(7))) == 0)
A, B = sp.symbols("A B")
ygen = A * (1 - x) + B * sp.exp(-x)
sAB = sp.solve([ygen.subs(x, 0) - 1, ygen.subs(x, 1)], [A, B], dict=True)[0]
check("am5-k110-4 BC ⇒ y=1-x", sAB[A] == 1 and sAB[B] == 0)

# ================================================================ §3 考古 112上期末 4：(x²+2x)y''-2(x+1)y'+2y=0
L = lambda y: (x**2 + 2 * x) * D(y, 2) - 2 * (x + 1) * D(y) + 2 * y
ind, _ = indicial(L)
check("am5-k112-4 indicial 2r(r-2)", sp.expand(ind - 2 * r * (r - 2)) == 0)
cbig = frob_coeffs(L, 2, 5)
check("am5-k112-4 r=2: x^2 exactly", cbig == [1, 0, 0, 0, 0, 0])
csmall = frob_coeffs(L, 0, 5, free={2: 0})
check("am5-k112-4 r=0 with a2=0: 1+x exactly", csmall == [1, 1, 0, 0, 0, 0])
check("am5-k112-4 x^2 and 1+x solve", sp.simplify(L(x**2)) == 0 and sp.simplify(L(1 + x)) == 0)
check("am5-k112-4 Wronskian (1+x)·2x - x^2 = x^2+2x ≠ 0", sp.expand((1 + x) * 2 * x - x**2 * 1) == x**2 + 2 * x)

# ================================================================ §3 考古 114上期末 2：x²y''+xy'+(x²-1/4)y=0
L = lambda y: x**2 * D(y, 2) + x * D(y) + (x**2 - R(1, 4)) * y
ind, _ = indicial(L)
check("am5-k114-2 indicial (γ+1/2)(γ-1/2)", sp.expand(ind - (r + R(1, 2)) * (r - R(1, 2))) == 0)
cp = frob_coeffs(L, R(1, 2), 6)
cm = frob_coeffs(L, R(-1, 2), 6, free={1: 0})
check("am5-k114-2 γ=1/2: 1,0,-1/6,0,1/120", cp[:5] == [1, 0, R(-1, 6), 0, R(1, 120)])
check("am5-k114-2 γ=-1/2 (a1=0): 1,0,-1/2,0,1/24", cm[:5] == [1, 0, R(-1, 2), 0, R(1, 24)])
check("am5-k114-2 third nonzero terms: -1/5040 x^6, -1/720 x^6", cp[6] == R(-1, 5040) and cm[6] == R(-1, 720))
check("am5-k114-2 closed forms sin x/sqrt x, cos x/sqrt x", sp.simplify(L(sp.sin(x) / sp.sqrt(x))) == 0 and sp.simplify(L(sp.cos(x) / sp.sqrt(x))) == 0)
cm1 = frob_coeffs(L, R(-1, 2), 6, free={1: 1})
check("am5-k114-2 γ=-1/2 with a1=1 adds the γ=1/2 solution", all(sp.simplify(cm1[k] - cm[k] - (cp[k - 1] if k >= 1 else 0)) == 0 for k in range(1, 7)))

# ================================================================ §3 自編 a：xy''+2y'-xy=0 與 xy''-y=0
L = lambda y: x * D(y, 2) + 2 * D(y) - x * y
ind, _ = indicial(L)
check("am5-sf-03a (a) indicial r(r+1)", sp.expand(ind - r * (r + 1)) == 0)
check("am5-sf-03a (a) r=-1 works (a1 free)", frob_coeffs(L, -1, 4, free={1: 0}) == [1, 0, R(1, 2), 0, R(1, 24)])
check("am5-sf-03a (a) cosh x/x, sinh x/x solve", sp.simplify(L(sp.cosh(x) / x)) == 0 and sp.simplify(L(sp.sinh(x) / x)) == 0)
L2 = lambda y: x * D(y, 2) - y
ind2, _ = indicial(L2)
check("am5-sf-03a (b) indicial r(r-1)", sp.expand(ind2 - r * (r - 1)) == 0)
check("am5-sf-03a (b) r=0 fails", frob_coeffs(L2, 0, 3) is None)
cb1 = frob_coeffs(L2, 1, 4)
check("am5-sf-03a (b) r=1: 1,1/2,1/12,1/144", cb1[:4] == [1, R(1, 2), R(1, 12), R(1, 144)])

# ================================================================ §3 自編 b：xy''+y=0
L = lambda y: x * D(y, 2) + y
c1 = frob_coeffs(L, 1, 6)
check("am5-sf-03b y1 = x - x²/2 + x³/12 - x⁴/144", c1[:4] == [1, R(-1, 2), R(1, 12), R(-1, 144)])
check("am5-sf-03b r=0 fails", frob_coeffs(L, 0, 3) is None)
Y1 = sum(c1[n] * x**(n + 1) for n in range(7))
s, _ = log_second(L, Y1, 0, 4, b0=1, free_b={1: 0})
check("am5-sf-03b k=-1, b2=-3/4, b3=7/36", any(d.get(sp.Symbol("k")) == -1 and d.get(sp.Symbol("b2")) == R(-3, 4) and d.get(sp.Symbol("b3")) == R(7, 36) for d in s))

# ================================================================ §4 Legendre
l = sp.symbols("l", integer=True, nonnegative=True)
L = lambda y, ll: (1 - x**2) * D(y, 2) - 2 * x * D(y) + ll * (ll + 1) * y
cvar = sp.symbols("a0:8")
yl = sum(cvar[k] * x**k for k in range(8))
res = sp.expand(L(yl, l))
check("am5-ex-4 recurrence (n+2)(n+1)a_{n+2}=(n+l+1)(n-l)a_n",
      all(sp.simplify(res.coeff(x, n) - ((n + 2) * (n + 1) * cvar[n + 2] - (n - l) * (n + l + 1) * cvar[n])) == 0 for n in range(6)))
a2 = -l * (l + 1) / 2
a4 = (2 - l) * (l + 3) / 12 * a2
check("am5-ex-4 a4 = (l+3)(l-2)(l+1)l/4!", sp.simplify(a4 - (l + 3) * (l - 2) * (l + 1) * l / 24) == 0)
a3 = (1 - l) * (l + 2) / 6
a5 = (3 - l) * (l + 4) / 20 * a3
check("am5-ex-4 a5 = (l+4)(l-3)(l+2)(l-1)/5!", sp.simplify(a5 - (l + 4) * (l - 3) * (l + 2) * (l - 1) / 120) == 0)
# l=0 的奇數級數：x + x³/3 + x⁵/5 + …（板書寫成交錯號是誤植）
odd0 = [sp.Integer(1)]
for n in range(1, 12, 2):
    odd0.append(odd0[-1] * sp.Rational((n - 0) * (n + 1), (n + 2) * (n + 1)))
check("am5-ex-4 l=0 odd series coefficients 1,1/3,1/5,1/7 (all +)", odd0[:4] == [1, R(1, 3), R(1, 5), R(1, 7)])
check("am5-ex-4 l=0 odd series = artanh x", all(sp.series(sp.atanh(x), x, 0, 12).removeO().coeff(x, 2 * k + 1) == odd0[k] for k in range(6)))
even1 = [sp.Integer(1)]
for n in range(0, 10, 2):
    even1.append(even1[-1] * sp.Rational((n - 1) * (n + 2), (n + 2) * (n + 1)))
check("am5-ex-4 l=1 even series 1 - x² - x⁴/3 - x⁶/5 (板書 +1/3、-1/5 誤植)", even1[:4] == [1, -1, R(-1, 3), R(-1, 5)])
check("am5-ex-4 l=1 even series = 1 - x artanh x", all(sp.series(1 - x * sp.atanh(x), x, 0, 12).removeO().coeff(x, 2 * k) == even1[k] for k in range(5)))
check("am5-ex-4 alternating 1-1/3+1/5-... converges to pi/4 (so 板書寫法自相矛盾)", sp.Sum((-1)**l / (2 * l + 1), (l, 0, sp.oo)).doit() == sp.pi / 4)
check("am5-ex-4 1+1/3+1/5+... diverges (>= 1/2 harmonic)", sp.Sum(1 / (2 * l + 1), (l, 0, sp.oo)).is_convergent() == False)
P = {k: sp.legendre(k, x) for k in range(7)}
check("am5-ex-5 P0..P3 table", [sp.expand(P[k]) for k in range(4)] == [1, x, sp.expand((3 * x**2 - 1) / 2), sp.expand((5 * x**3 - 3 * x) / 2)])
check("am5-ex-5 l=2 terminating 1-3x², l=3 x-5x³/3", sp.simplify(L(1 - 3 * x**2, 2)) == 0 and sp.simplify(L(3 * x - 5 * x**3, 3)) == 0)
check("am5-ex-5 normalization P_l(1)=1", all(P[k].subs(x, 1) == 1 for k in range(7)))
check("am5-ex-5 parity P_l(-x)=(-1)^l P_l(x)", all(sp.expand(P[k].subs(x, -x) - (-1)**k * P[k]) == 0 for k in range(7)))
# 遞迴關係 ①–⑤
ok = True
for k in range(2, 6):
    ok &= sp.expand(k * P[k] - ((2 * k - 1) * x * P[k - 1] - (k - 1) * P[k - 2])) == 0
    ok &= sp.expand(x * D(P[k]) - D(P[k - 1]) - k * P[k]) == 0
    ok &= sp.expand(D(P[k]) - x * D(P[k - 1]) - k * P[k - 1]) == 0
    ok &= sp.expand((1 - x**2) * D(P[k]) - (k * P[k - 1] - k * x * P[k])) == 0
    ok &= sp.expand((2 * k + 1) * P[k] - (D(P[k + 1]) - D(P[k - 1]))) == 0
check("am5-ex-5 recurrence relations ①–⑤ hold for l=2..5", ok)

# 考古 114上期末 3：圖形特徵
P2, P3 = P[2], P[3]
check("am5-k114-3 P2 zeros ±1/sqrt3 ≈ ±0.577, P2(0)=-1/2", set(sp.solve(P2, x)) | set(sp.solve(P2.subs(x, -x), x)) >= {1 / sp.sqrt(3)} and P2.subs(x, 0) == R(-1, 2))
z = sp.symbols("z")
check("am5-k114-3 P3 zeros 0, ±sqrt(3/5)≈0.775", set(sp.solve(sp.legendre(3, z), z)) == {0, sp.sqrt(15) / 5, -sp.sqrt(15) / 5} and abs(float(sp.sqrt(R(3, 5))) - 0.7746) < 1e-4)
check("am5-k114-3 P2 zeros ±0.577", set(sp.solve(sp.legendre(2, z), z)) == {sp.sqrt(3) / 3, -sp.sqrt(3) / 3})
check("am5-k114-3 P3 extrema at ±1/sqrt5 with value ∓1/sqrt5 ≈ 0.447", sp.expand(D(P3).subs(x, 1 / sp.sqrt(5))) == 0 and sp.simplify(P3.subs(x, 1 / sp.sqrt(5)) + 1 / sp.sqrt(5)) == 0)
check("am5-k114-3 values at -1: P_l(-1)=(-1)^l", [P[k].subs(x, -1) for k in range(4)] == [1, -1, 1, -1])

# ================================================================ §4 自編
check("am5-sf-04a P4 = (35x^4-30x^2+3)/8 via ①", sp.expand((7 * x * P3 - 3 * P2) / 4 - (35 * x**4 - 30 * x**2 + 3) / 8) == 0)
check("am5-sf-04a P5 = (63x^5-70x^3+15x)/8 via ①", sp.expand((9 * x * P[4] - 4 * P3) / 5 - (63 * x**5 - 70 * x**3 + 15 * x) / 8) == 0)
check("am5-sf-04a P4 solves Legendre l=4", sp.simplify(L(P[4], 4)) == 0)
# 截斷：l=4 的偶數級數 a2=-10 a0, a4=35/3 a0
check("am5-sf-04a l=4 series 1-10x²+35/3 x⁴ ∝ P4", sp.expand((1 - 10 * x**2 + R(35, 3) * x**4) * R(3, 8) - P[4]) == 0)
check("am5-sf-04a P4(0)=3/8, P5(0)=0", P[4].subs(x, 0) == R(3, 8) and P[5].subs(x, 0) == 0)
I = {k: sp.integrate(P[k], (x, 0, 1)) for k in range(1, 6)}
check("am5-sf-04b ∫0^1 P2 = 0, ∫0^1 P3 = -1/8, ∫0^1 P4 = 0, ∫0^1 P5 = 1/16", I[2] == 0 and I[3] == R(-1, 8) and I[4] == 0 and I[5] == R(1, 16))
check("am5-sf-04b via ⑤: ∫0^1 P_l = -(P_{l+1}(0)-P_{l-1}(0))/(2l+1)", all(I[k] == -(P[k + 1].subs(x, 0) - P[k - 1].subs(x, 0)) / (2 * k + 1) for k in range(1, 6)))

check("am5-k110-4 reduction: d/dx[e^{-x}/(1-x)] = x e^{-x}/(1-x)^2, y2=e^{-x}", sp.simplify(sp.diff(sp.exp(-x) / (1 - x), x) - x * sp.exp(-x) / (1 - x)**2) == 0 and sp.simplify(sp.exp(-sp.integrate((x - 1) / x, x)) - x * sp.exp(-x)) == 0)

# ================================================================ §5 考前衝刺 變化題
L = lambda y: x**2 * D(y, 2) + x * D(y) + (x**2 - R(9, 4)) * y
ind, _ = indicial(L)
check("am5var-1 indicial (2r-3)(2r+3)/4", sp.expand(4 * ind - (2 * r - 3) * (2 * r + 3)) == 0)
check("am5var-1 γ=3/2: 1,-1/10,1/280", [frob_coeffs(L, R(3, 2), 4)[k] for k in (0, 2, 4)] == [1, R(-1, 10), R(1, 280)])
check("am5var-1 γ=-3/2 (a3=0): 1,1/2,-1/8", [frob_coeffs(L, R(-3, 2), 4, free={3: 0})[k] for k in (0, 2, 4)] == [1, R(1, 2), R(-1, 8)])
L = lambda y: x * D(y, 2) + (x - 2) * D(y) - 2 * y
check("am5var-2 small root gives 1-x+x^2/2", frob_coeffs(L, 0, 6, free={3: 0}) == [1, -1, R(1, 2), 0, 0, 0, 0])
check("am5var-2 e^{-x} and 1-x+x^2/2 solve", sp.simplify(L(sp.exp(-x))) == 0 and sp.simplify(L(1 - x + x**2 / 2)) == 0)
L = lambda y: x * D(y, 2) + (1 + x) * D(y) + y
y2v = sp.exp(-x) * (sp.log(x) + x + x**2 / 4 + x**3 / 18 + x**4 / 96)
check("am5var-3 y1=e^{-x}, y2=e^{-x}(ln x + x + x²/4 + x³/18 + …)", sp.simplify(L(sp.exp(-x))) == 0 and sp.simplify(sp.series(sp.expand(L(y2v)), x, 0, 4).removeO()) == 0)
L = lambda y: (x**2 - x) * D(y, 2) + (4 * x - 2) * D(y) + 2 * y
check("am5var-4 1/x and 1/(1-x) solve; indicial γ(γ+1)", sp.simplify(L(1 / x)) == 0 and sp.simplify(L(1 / (1 - x))) == 0 and sp.expand(indicial(L)[0] + r * (r + 1)) == 0)
odd2 = [sp.Integer(1)]
for n in range(1, 8, 2):
    odd2.append(odd2[-1] * R((n - 2) * (n + 3), (n + 2) * (n + 1)))
check("am5var-5 l=2 odd series x - 2/3 x^3 - 1/5 x^5 - 4/35 x^7", odd2[:4] == [1, R(-2, 3), R(-1, 5), R(-4, 35)])
check("am5 figure: y1(1)=0.698, y2(1)=0.156 (closed forms)", abs(float(sp.sqrt(R(1, 2)) * sp.sin(sp.sqrt(2))) - 0.698) < 5e-4 and abs(float(sp.cos(sp.sqrt(2))) - 0.156) < 5e-4)

print(f"\n{COUNT[0]} checks, {len(FAILS)} failed")
if FAILS:
    print("FAILED:", *FAILS, sep="\n  ")
    sys.exit(1)
print("ALL CHECKS PASSED")
