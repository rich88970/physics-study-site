"""應用數學第 4 章（冪級數解）：每張題目卡的答案用 sympy 獨立驗算。

做法：
- 級數解：把網站寫的截斷級數代回方程式，檢查殘差的低階項全為 0（到網站寫出的那一階）；
  並用「代入未知係數、逐階解線性方程」的方法獨立重算係數，和網站的數字逐一比對。
- 有 closed form 的：用 sympy.checkodesol 驗證，並比對它的泰勒展開。
- 初始／邊界條件：直接代入。

用法：python tools/verify_applied_math_ch04.py   全部通過時印出 ALL CHECKS PASSED。
"""
import sys
import sympy as sp

x, t = sp.symbols("x t")
R = sp.Rational
FAILS = []
COUNT = [0]


def check(name, cond):
    COUNT[0] += 1
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAILS.append(name)


def series_coeffs(L, N, init, rhs=0, var=x):
    """y=Σ c_k var^k 代入 L(y)=rhs，給定 c0、c1，逐階解出 c2..cN（獨立重算，不用網站的遞迴式）。"""
    c = sp.symbols(f"c0:{N + 1}")
    y = sum(c[k] * var**k for k in range(N + 1))
    res = sp.expand(sp.series(sp.expand(L(y)) - rhs, var, 0, N - 1).removeO())
    sol = {c[0]: init[0], c[1]: init[1]}
    for k in range(N - 1):
        eq = sp.expand(res.coeff(var, k).subs(sol))
        unknown = [s for s in eq.free_symbols if s in c]
        if unknown:
            s = sp.solve(eq, unknown[-1])[0]
            sol[unknown[-1]] = s
    return [sp.nsimplify(sol.get(c[k], sp.Symbol(f"free{k}"))) for k in range(N + 1)]


def residual_low_terms_zero(L, y, order, var=x, rhs=0):
    """截斷級數代入後，殘差在 var^0..var^(order-1) 的係數都要是 0。"""
    r = sp.expand(sp.series(sp.expand(L(y)) - rhs, var, 0, order).removeO())
    return all(sp.simplify(r.coeff(var, k)) == 0 for k in range(order))


def D(y, n=1, var=x):
    return sp.diff(y, var, n)


# ---------------------------------------------------------------- §2 板書：y''+ω0²y=0
w = sp.symbols("omega0", positive=True)
L = lambda y: D(y, 2) + w**2 * y
cs0 = series_coeffs(L, 9, (1, 0))
cs1 = series_coeffs(L, 9, (0, 1))
check("am4-ex-1 a2=-w^2/2! a0", sp.simplify(cs0[2] + w**2 / 2) == 0)
check("am4-ex-1 a4=w^4/4! a0", sp.simplify(cs0[4] - w**4 / 24) == 0)
check("am4-ex-1 a3=-w^2/3! a1", sp.simplify(cs1[3] + w**2 / 6) == 0)
check("am4-ex-1 a5=w^4/5! a1", sp.simplify(cs1[5] - w**4 / 120) == 0)
check("am4-ex-1 even series = cos(w x)", all(sp.simplify(cs0[k] - sp.series(sp.cos(w * x), x, 0, 10).removeO().coeff(x, k)) == 0 for k in range(9)))
check("am4-ex-1 odd series = sin(w x)/w", all(sp.simplify(cs1[k] - sp.series(sp.sin(w * x) / w, x, 0, 10).removeO().coeff(x, k)) == 0 for k in range(9)))
check("am4-ex-1 C2=a1/w0 ⇒ y'(0)=a1", sp.simplify(D(sp.sin(w * x) / w).subs(x, 0) - 1) == 0)

# ---------------------------------------------------------------- §3 板書：y''-xy'+y=0
L = lambda y: D(y, 2) - x * D(y) + y
c0 = series_coeffs(L, 10, (1, 0))
c1 = series_coeffs(L, 10, (0, 1))
check("am4-ex-2 a2=-1/2,a4=-1/24,a6=-1/240,a8=-1/2688", c0[2] == R(-1, 2) and c0[4] == R(-1, 24) and c0[6] == R(-1, 240) and c0[8] == R(-1, 2688))
check("am4-ex-2 odd chain: y2 = x exactly", all(c1[k] == (1 if k == 1 else 0) for k in range(10)))
check("am4-ex-2 y=x solves ODE", sp.simplify(L(x)) == 0)
# 遞迴式 a_{n+2}=(n-1)a_n/((n+2)(n+1))
check("am4-ex-2 recurrence matches", all(sp.simplify(c0[n + 2] - R(n - 1, (n + 2) * (n + 1)) * c0[n]) == 0 for n in range(8)))

# ---------------------------------------------------------------- §3 作業 1：y''+x²y'+xy=0
L = lambda y: D(y, 2) + x**2 * D(y) + x * y
c0 = series_coeffs(L, 10, (1, 0))
c1 = series_coeffs(L, 10, (0, 1))
check("am4-hw-1 y1 = 1 - x^3/6 + x^6/45", c0[3] == R(-1, 6) and c0[6] == R(1, 45) and c0[2] == 0 and c0[4] == 0 and c0[5] == 0)
check("am4-hw-1 y2 = x - x^4/6 + 5x^7/252", c1[4] == R(-1, 6) and c1[7] == R(5, 252) and c1[2] == 0 and c1[3] == 0)
check("am4-hw-1 next terms a9=-7/3240 a0, a10=-1/567 a1", c0[9] == R(-7, 3240) and c1[10 - 1 + 1 - 1] == c1[9] and series_coeffs(L, 11, (0, 1))[10] == R(-1, 567))
check("am4-hw-1 recurrence a_{k+2}=-k a_{k-1}/((k+2)(k+1))", all(sp.simplify(c0[k + 2] + R(k, (k + 2) * (k + 1)) * c0[k - 1]) == 0 for k in range(1, 8)))

# ---------------------------------------------------------------- §3 作業 2：y''+(x³+1)y'-y=0
L = lambda y: D(y, 2) + (x**3 + 1) * D(y) - y
c0 = series_coeffs(L, 8, (1, 0))
c1 = series_coeffs(L, 8, (0, 1))
check("am4-hw-2 y1 = 1 + x^2/2 - x^3/6 + x^4/12", c0[2] == R(1, 2) and c0[3] == R(-1, 6) and c0[4] == R(1, 12))
check("am4-hw-2 y2 = x - x^2/2 + x^3/3 - x^4/8", c1[2] == R(-1, 2) and c1[3] == R(1, 3) and c1[4] == R(-1, 8))
check("am4-hw-2 a5: y1 -1/40, y2 -1/120", c0[5] == R(-1, 40) and c1[5] == R(-1, 120))

# ---------------------------------------------------------------- §3 考古 114上期末 1：y''-x²y'-xy=0
L = lambda y: D(y, 2) - x**2 * D(y) - x * y
c0 = series_coeffs(L, 9, (1, 0))
c1 = series_coeffs(L, 9, (0, 1))
check("am4-k114-1 y1 = 1 + x^3/6 + x^6/45", c0[3] == R(1, 6) and c0[6] == R(1, 45) and c0[2] == 0)
check("am4-k114-1 y2 = x + x^4/6 + 5x^7/252", c1[4] == R(1, 6) and c1[7] == R(5, 252))
check("am4-k114-1 recurrence a_{n+3}=(n+1)a_n/((n+3)(n+2))", all(sp.simplify(c0[n + 3] - R(n + 1, (n + 3) * (n + 2)) * c0[n]) == 0 for n in range(5)))

# ---------------------------------------------------------------- §3 考古 112上期末 3：y''-4xy'+(4x²-2)y=0
L = lambda y: D(y, 2) - 4 * x * D(y) + (4 * x**2 - 2) * y
c0 = series_coeffs(L, 10, (1, 0))
c1 = series_coeffs(L, 10, (0, 1))
check("am4-k112-3 y1 coefficients 1,0,1,0,1/2,0,1/6", c0[:7] == [1, 0, 1, 0, R(1, 2), 0, R(1, 6)])
check("am4-k112-3 y2 coefficients 0,1,0,1,0,1/2,0,1/6", c1[:8] == [0, 1, 0, 1, 0, R(1, 2), 0, R(1, 6)])
check("am4-k112-3 e^{x^2} solves", sp.simplify(L(sp.exp(x**2))) == 0)
check("am4-k112-3 x e^{x^2} solves", sp.simplify(L(x * sp.exp(x**2))) == 0)
check("am4-k112-3 series of e^{x^2} matches y1", all(sp.series(sp.exp(x**2), x, 0, 10).removeO().coeff(x, k) == c0[k] for k in range(10)))
check("am4-k112-3 Wronskian nonzero", sp.simplify(sp.exp(x**2) * D(x * sp.exp(x**2)) - x * sp.exp(x**2) * D(sp.exp(x**2))) == sp.exp(2 * x**2))

# ---------------------------------------------------------------- §2 自編 a：y''-3y'+2y=0, y(0)=0, y'(0)=1
L = lambda y: D(y, 2) - 3 * D(y) + 2 * y
cs = series_coeffs(L, 10, (0, 1))
check("am4-sf-02a a_n=(2^n-1)/n!", all(cs[n] == R(2**n - 1, sp.factorial(n)) for n in range(10)))
check("am4-sf-02a closed form e^{2x}-e^x solves + IC", sp.simplify(L(sp.exp(2 * x) - sp.exp(x))) == 0 and (sp.exp(2 * x) - sp.exp(x)).subs(x, 0) == 0 and D(sp.exp(2 * x) - sp.exp(x)).subs(x, 0) == 1)
n = sp.symbols("n", integer=True, nonnegative=True)
an = (2**n - 1) / sp.factorial(n)
check("am4-sf-02a general term satisfies 3-term recurrence",
      sp.simplify(((n + 2) * (n + 1) * an.subs(n, n + 2) - 3 * (n + 1) * an.subs(n, n + 1) + 2 * an).rewrite(sp.gamma)) == 0)

# ---------------------------------------------------------------- §2 自編 b：(1+x)y'=p y
p = sp.symbols("p")
cb = sp.symbols("b0:6")
yb = sum(cb[k] * x**k for k in range(6))
res = sp.expand((1 + x) * D(yb) - p * yb)
solb = sp.solve([res.coeff(x, k) for k in range(5)], cb[1:], dict=True)[0]
check("am4-sf-02b a_{n+1}=(p-n)/(n+1) a_n → binomial", all(sp.simplify(solb[cb[k]].subs(cb[0], 1) - sp.binomial(p, k)) == 0 for k in range(1, 6)))
half = [sp.binomial(R(1, 2), k) for k in range(5)]
check("am4-sf-02b p=1/2 coefficients 1,1/2,-1/8,1/16,-5/128", half == [1, R(1, 2), R(-1, 8), R(1, 16), R(-5, 128)])
check("am4-sf-02b p=3 terminates: 1+3x+3x^2+x^3", [sp.binomial(3, k) for k in range(6)] == [1, 3, 3, 1, 0, 0])
check("am4-sf-02b sqrt(1.2) by 4 terms ≈ 1.0955 (true 1.09545)", abs(sum(half[k] * R(1, 5)**k for k in range(4)) - sp.sqrt(R(6, 5))) < R(1, 1000))
check("am4-sf-02b ratio test |a_{n+1}/a_n|→1 for p=1/2", sp.limit(sp.Abs((R(1, 2) - n) / (n + 1)), n, sp.oo) == 1)

# ---------------------------------------------------------------- §1 自編：奇點與收斂半徑
roots = sp.solve(x**2 - 2 * x + 5, x)
check("am4-sf-01a singular points 1±2i", set(roots) == {1 + 2 * sp.I, 1 - 2 * sp.I})
check("am4-sf-01a R from x0=0 is sqrt5", all(sp.Abs(r - 0) == sp.sqrt(5) for r in roots))
check("am4-sf-01a R from x0=1 is 2", all(sp.Abs(r - 1) == 2 for r in roots))
check("am4-sf-01a R from x0=3 is 2sqrt2", all(sp.simplify(sp.Abs(r - 3) - 2 * sp.sqrt(2)) == 0 for r in roots))
# (b) x²(x-2)² y'' + 3x y' + (x-2) y = 0
P = 3 * x / (x**2 * (x - 2)**2)
Q = (x - 2) / (x**2 * (x - 2)**2)
check("am4-sf-01b x=0 regular: xP→3/4, x²Q→-1/2", sp.limit(x * P, x, 0) == R(3, 4) and sp.limit(x**2 * Q, x, 0) == R(-1, 2))
check("am4-sf-01b x=2 irregular: (x-2)P→∞", sp.limit((x - 2) * P, x, 2) in (sp.oo, -sp.oo, sp.zoo) or sp.limit(sp.Abs((x - 2) * P), x, 2) == sp.oo)
check("am4-sf-01b (x-2)²Q finite at 2 (=0)", sp.limit((x - 2)**2 * Q, x, 2) == 0)

# ---------------------------------------------------------------- §3 自編 a：Hermite y''-2xy'+2λy=0
lam = sp.symbols("lambda")
L = lambda y: D(y, 2) - 2 * x * D(y) + 2 * lam * y
H3 = 8 * x**3 - 12 * x
check("am4-sf-03a H3 solves with λ=3", sp.simplify(L(H3).subs(lam, 3)) == 0)
check("am4-sf-03a λ=3 odd chain: a3=-2/3 a1, a5=0", series_coeffs(lambda y: L(y).subs(lam, 3), 9, (0, 1))[3] == R(-2, 3) and series_coeffs(lambda y: L(y).subs(lam, 3), 9, (0, 1))[5] == 0)
check("am4-sf-03a λ=3 even chain does not terminate (a2=-3,a4=1/2,a6=1/30)", [series_coeffs(lambda y: L(y).subs(lam, 3), 9, (1, 0))[k] for k in (2, 4, 6)] == [-3, R(1, 2), R(1, 30)])
check("am4-sf-03a λ=2 gives 4x^2-2 (H2)", sp.simplify(L(4 * x**2 - 2).subs(lam, 2)) == 0)
check("am4-sf-03a hermite(3) = 8x^3-12x", sp.expand(sp.hermite(3, x) - H3) == 0)

# ---------------------------------------------------------------- §3 自編 b：Airy y''=xy, y(0)=1, y'(0)=0
L = lambda y: D(y, 2) - x * y
ca = series_coeffs(L, 13, (1, 0))
check("am4-sf-03b a3=1/6, a6=1/180, a9=1/12960, a12=1/1710720", ca[3] == R(1, 6) and ca[6] == R(1, 180) and ca[9] == R(1, 12960) and ca[12] == R(1, 1710720))
check("am4-sf-03b all non-multiples of 3 vanish", all(ca[k] == 0 for k in range(13) if k % 3))
y1val = sum(ca[k] for k in range(13))
check("am4-sf-03b y(1) ≈ 1.17230", abs(float(y1val) - 1.17230) < 5e-6)
check("am4-sf-03b 4 terms give 1.17230 to 5 decimals (5th term 5.8e-7)", abs(float(ca[12]) - 5.85e-7) < 1e-8 and abs(float(sum(ca[k] for k in (0, 3, 6, 9))) - 1.172300) < 1e-6)
check("am4-sf-03b matches Airy combination", abs(float(sum(ca[k] for k in range(13))) - float((sp.airyai(1) * sp.airybiprime(0) - sp.airybi(1) * sp.airyaiprime(0)) / (sp.airyai(0) * sp.airybiprime(0) - sp.airybi(0) * sp.airyaiprime(0)))) < 1e-6)

# ---------------------------------------------------------------- §4 作業 3：(x-1)y''-xy'+y=0, y(0)=-2, y'(0)=6
L = lambda y: (x - 1) * D(y, 2) - x * D(y) + y
cs = series_coeffs(L, 8, (-2, 6))
check("am4-hw-3 series -2,6,-1,-1/3,-1/12", cs[:5] == [-2, 6, -1, R(-1, 3), R(-1, 12)])
ysol = 8 * x - 2 * sp.exp(x)
check("am4-hw-3 closed form 8x-2e^x solves + IC", sp.simplify(L(ysol)) == 0 and ysol.subs(x, 0) == -2 and D(ysol).subs(x, 0) == 6)
check("am4-hw-3 teacher answer -2(1+x^2/2+x^3/6+...)+6x = series", all(sp.series(ysol, x, 0, 8).removeO().coeff(x, k) == cs[k] for k in range(8)))
check("am4-hw-3 recurrence a_{n+2}=((n+1)n a_{n+1}... ) check via a_n = -2/n! (n>=2)", all(cs[k] == R(-2, sp.factorial(k)) for k in range(2, 8)))

# ---------------------------------------------------------------- §4 考古 110上期末 3：y''-x²y'+(x+2)y=x, y(0)=2, y'(0)=1
L = lambda y: D(y, 2) - x**2 * D(y) + (x + 2) * y
cs = series_coeffs(L, 9, (2, 1), rhs=x)
check("am4-k110-3 coefficients 2,1,-2,-1/2,1/3,-1/20", cs[:6] == [2, 1, -2, R(-1, 2), R(1, 3), R(-1, 20)])
check("am4-k110-3 a6=-1/18, a7=11/420", cs[6] == R(-1, 18) and cs[7] == R(11, 420))
ytr = sum(cs[k] * x**k for k in range(9))
check("am4-k110-3 residual zero through x^6", residual_low_terms_zero(L, ytr, 7, rhs=x))

# ---------------------------------------------------------------- §4 考古 113上期末 2：y''-(1+x)y=0, y(0)=1, y'(0)=0
L = lambda y: D(y, 2) - (1 + x) * y
cs = series_coeffs(L, 9, (1, 0))
check("am4-k113-2 coefficients 1,0,1/2,1/6,1/24,1/30,1/144", cs[:7] == [1, 0, R(1, 2), R(1, 6), R(1, 24), R(1, 30), R(1, 144)])
check("am4-k113-2 a7=1/560, a8=29/40320", cs[7] == R(1, 560) and cs[8] == R(29, 40320))
check("am4-k113-2 recurrence a_{n+2}=(a_n+a_{n-1})/((n+2)(n+1))", all(cs[k + 2] == (cs[k] + (cs[k - 1] if k >= 1 else 0)) / ((k + 2) * (k + 1)) for k in range(7)))

# ---------------------------------------------------------------- §4 考古 111上期末 3：(x²+1)y''-2xy'+2y=0, y(0)=1, y(1)=1
L = lambda y: (x**2 + 1) * D(y, 2) - 2 * x * D(y) + 2 * y
c0 = series_coeffs(L, 8, (1, 0))
c1 = series_coeffs(L, 8, (0, 1))
check("am4-k111-3 a0 chain: 1 - x^2 (terminates)", c0 == [1, 0, -1, 0, 0, 0, 0, 0, 0])
check("am4-k111-3 a1 chain: x (terminates)", c1 == [0, 1, 0, 0, 0, 0, 0, 0, 0])
ys = 1 + x - x**2
check("am4-k111-3 y=1+x-x^2 solves + BC", sp.simplify(L(ys)) == 0 and ys.subs(x, 0) == 1 and ys.subs(x, 1) == 1)

# ---------------------------------------------------------------- §4 自編 a：y''+(x-1)y'+y=0, y(1)=2, y'(1)=0
L = lambda y: D(y, 2, t) + t * D(y, 1, t) + y
cs = series_coeffs(L, 9, (2, 0), var=t)
check("am4-sf-04a t-series 2,0,-1,0,1/4,0,-1/24", cs[:7] == [2, 0, -1, 0, R(1, 4), 0, R(-1, 24)])
yc = 2 * sp.exp(-(x - 1)**2 / 2)
check("am4-sf-04a closed form 2e^{-(x-1)^2/2} solves + IC", sp.simplify(D(yc, 2) + (x - 1) * D(yc) + yc) == 0 and yc.subs(x, 1) == 2 and D(yc).subs(x, 1) == 0)
check("am4-sf-04a y(1.5) ≈ 1.7650", abs(float(yc.subs(x, R(3, 2))) - 1.76499) < 1e-4)

# ---------------------------------------------------------------- §4 自編 b：y''-xy'-y=1/(1-x), y(0)=y'(0)=0
L = lambda y: D(y, 2) - x * D(y) - y
cs = series_coeffs(L, 9, (0, 0), rhs=1 / (1 - x))
check("am4-sf-04b coefficients 0,0,1/2,1/6,5/24,1/12", cs[:6] == [0, 0, R(1, 2), R(1, 6), R(5, 24), R(1, 12)])
check("am4-sf-04b recurrence a_{n+2}=(1+(n+1)a_n)/((n+2)(n+1))", all(cs[k + 2] == (1 + (k + 1) * cs[k]) / ((k + 2) * (k + 1)) for k in range(6)))
check("am4-sf-04b a6=49/720, a7=1/28", cs[6] == R(49, 720) and cs[7] == R(1, 28))
# 半徑：右邊 1/(1-x) 在 x=1 奇異 → 解的級數半徑 1（係數 a_n → 不趨近 0 的比值檢查：a_{n+1}/a_n 的趨勢）
cs30 = series_coeffs(L, 30, (0, 0), rhs=1 / (1 - x))
check("am4-sf-04b n²·a_n stays ≈1 (n=20..29) ⇒ ratio→1, radius exactly 1", all(0.8 < float(cs30[k]) * k * k < 1.4 for k in range(20, 30)))
check("am4-sf-04b homogeneous solution e^{x^2/2}", sp.simplify(L(sp.exp(x**2 / 2))) == 0)

check("am4-k111-3 reduction of order from y1=x gives x^2-1", sp.simplify(x * sp.integrate(sp.exp(-sp.integrate(-2 * x / (x**2 + 1), x)) / x**2, x) - (x**2 - 1)) == 0)

# ---------------------------------------------------------------- §5 考前衝刺 變化題
L = lambda y: D(y, 2) + x**2 * D(y) - x * y
v0 = series_coeffs(L, 10, (1, 0))
v1 = series_coeffs(L, 10, (0, 1))
check("am4var-1 y1 = 1 + x^3/6 - x^6/90 + x^9/1296", v0[3] == R(1, 6) and v0[6] == R(-1, 90) and v0[9] == R(1, 1296))
check("am4var-1 y2 = x exactly", all(v1[k] == (1 if k == 1 else 0) for k in range(10)) and sp.simplify(L(x)) == 0)
L = lambda y: D(y, 2) - 2 * x * D(y) + (x**2 - 1) * y
v0 = series_coeffs(L, 8, (1, 0))
v1 = series_coeffs(L, 8, (0, 1))
check("am4var-2 y1 1,1/2,1/8,1/48 ; y2 1,1/2,1/8", [v0[k] for k in (0, 2, 4, 6)] == [1, R(1, 2), R(1, 8), R(1, 48)] and [v1[k] for k in (1, 3, 5)] == [1, R(1, 2), R(1, 8)])
check("am4var-2 (a0+a1x)e^{x^2/2} solves", sp.simplify(L(sp.exp(x**2 / 2))) == 0 and sp.simplify(L(x * sp.exp(x**2 / 2))) == 0)
L = lambda y: D(y, 2) - (1 + x) * y
v = series_coeffs(L, 8, (0, 1))
check("am4var-3 x + x^3/6 + x^4/12 + x^5/120 + x^6/120", v[:7] == [0, 1, 0, R(1, 6), R(1, 12), R(1, 120), R(1, 120)])
L = lambda y: D(y, 2) - x**2 * D(y) + (x + 2) * y
v = series_coeffs(L, 8, (0, 0), rhs=1)
check("am4var-4 x^2/2 - x^4/12 + x^5/40 + x^6/180", v[:7] == [0, 0, R(1, 2), 0, R(-1, 12), R(1, 40), R(1, 180)])
L = lambda y: (x**2 + 1) * D(y, 2) - 2 * x * D(y) + 2 * y
check("am4var-5 y = x^2 - 1 solves, y(1)=0, y(2)=3", sp.simplify(L(x**2 - 1)) == 0 and (x**2 - 1).subs(x, 1) == 0 and (x**2 - 1).subs(x, 2) == 3)
check("am4var-6 radii 3 (x0=0) and 2 (x0=2)", min(abs(complex(r)) for r in [3j, -3j, 4]) == 3 and min(abs(complex(r) - 2) for r in [3j, -3j, 4]) == 2)
Qv = 1 / ((x**2 + 9) * (x - 4))
check("am4var-6 x=4 regular singular: (x-4)^2 Q -> 0", sp.limit((x - 4)**2 * Qv, x, 4) == 0)
check("am4 partial-sum figure: S5(pi) = -0.9760", abs(sum((-1)**k * float(sp.pi)**(2 * k) / float(sp.factorial(2 * k)) for k in range(5)) + 0.97602) < 1e-4)

print(f"\n{COUNT[0]} checks, {len(FAILS)} failed")
if FAILS:
    print("FAILED:", *FAILS, sep="\n  ")
    sys.exit(1)
print("ALL CHECKS PASSED")
