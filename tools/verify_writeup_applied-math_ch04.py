"""應用數學第 4 章考試書寫版（exam.html 的「背公式＋計算」改寫）：驗算書寫版裡出現的所有數值與中間值。

做法：用 sympy 獨立重算（把截斷級數代入方程式逐階解係數，不用網站的遞迴式），
再和書寫版寫出的數字逐一比對。全部通過時印出 ALL CHECKS PASSED。
用法：python tools/verify_writeup_applied-math_ch04.py
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


def D(y, n=1, var=x):
    return sp.diff(y, var, n)


def coeffs(L, N, init, rhs=0, var=x):
    """y=Σ c_k var^k 代入 L(y)=rhs，給定 c0、c1，逐階解出 c2..cN。"""
    c = sp.symbols(f"c0:{N + 1}")
    y = sum(c[k] * var**k for k in range(N + 1))
    res = sp.expand(sp.series(sp.expand(L(y)) - rhs, var, 0, N - 1).removeO())
    sol = {c[0]: init[0], c[1]: init[1]}
    for k in range(N - 1):
        eq = sp.expand(res.coeff(var, k).subs(sol))
        unknown = [s for s in eq.free_symbols if s in c]
        if unknown:
            sol[unknown[-1]] = sp.solve(eq, unknown[-1])[0]
    return [sp.simplify(sol.get(c[k], 0)) for k in range(N + 1)]


a0, a1 = sp.symbols("a0 a1")

# ---------------- am4-sf-01a
P = x**2 - 2 * x + 5
roots = sp.solve(P, x)
check("sf-01a 奇點 1±2i", set(roots) == {1 + 2 * sp.I, 1 - 2 * sp.I})
check("sf-01a 判別式 4-20=-16", (-2) ** 2 - 4 * 5 == -16)
check("sf-01a |0-(1+2i)|=√5", sp.Abs(0 - (1 + 2 * sp.I)) == sp.sqrt(5))
check("sf-01a √5≈2.24", abs(float(sp.sqrt(5)) - 2.24) < 0.005)
check("sf-01a |1-(1+2i)|=2", sp.Abs(1 - (1 + 2 * sp.I)) == 2)
check("sf-01a |3-(1+2i)|=2√2≈2.83", sp.Abs(3 - (1 + 2 * sp.I)) == 2 * sp.sqrt(2) and abs(float(2 * sp.sqrt(2)) - 2.83) < 0.005)
check("sf-01a y=x 是解", sp.simplify(P * D(x, 2) + x * D(x) - x) == 0)

# ---------------- am4-sf-01b
p = sp.cancel(3 * x / (x**2 * (x - 2) ** 2))
q = sp.cancel((x - 2) / (x**2 * (x - 2) ** 2))
check("sf-01b p=3/(x(x-2)^2)", sp.simplify(p - 3 / (x * (x - 2) ** 2)) == 0)
check("sf-01b q=1/(x^2(x-2))", sp.simplify(q - 1 / (x**2 * (x - 2))) == 0)
check("sf-01b lim xp=3/4", sp.limit(x * p, x, 0) == R(3, 4))
check("sf-01b lim x^2q=-1/2", sp.limit(x**2 * q, x, 0) == R(-1, 2))
check("sf-01b (x-2)p 在 2 發散", sp.limit(((x - 2) * p) ** 2, x, 2) == sp.oo)
check("sf-01b (x-2)^2q→0", sp.limit((x - 2) ** 2 * q, x, 2) == 0)
check("sf-01b x0=1,-1 半徑都 1", min(abs(1 - 0), abs(1 - 2)) == 1 and min(abs(-1 - 0), abs(-1 - 2)) == 1)

# ---------------- am4-ex-1
w = sp.symbols("omega0", positive=True)
L = lambda y: D(y, 2) + w**2 * y
c0 = coeffs(L, 7, (a0, 0))
c1 = coeffs(L, 7, (0, a1))
check("ex-1 a2=-w^2/2! a0", sp.simplify(c0[2] + w**2 / 2 * a0) == 0)
check("ex-1 a3=-w^2/3! a1", sp.simplify(c1[3] + w**2 / 6 * a1) == 0)
check("ex-1 a4=w^4/4! a0", sp.simplify(c0[4] - w**4 / 24 * a0) == 0)
check("ex-1 a5=w^4/5! a1", sp.simplify(c1[5] - w**4 / 120 * a1) == 0)
check("ex-1 closed form", sp.simplify(L(a0 * sp.cos(w * x) + a1 / w * sp.sin(w * x))) == 0)

# ---------------- am4-sf-02a
L = lambda y: D(y, 2) - 3 * D(y) + 2 * y
c = coeffs(L, 7, (0, 1))
check("sf-02a a2..a5", c[2:6] == [R(3, 2), R(7, 6), R(5, 8), R(31, 120)])
check("sf-02a 中間值 21/2-3=15/2 → 5/8", (R(21, 2) - 3) / 12 == R(5, 8))
check("sf-02a 中間值 (15/2-7/3)/20=31/120", (R(15, 2) - R(7, 3)) / 20 == R(31, 120))
n = sp.symbols("n", integer=True, nonnegative=True)
an = lambda k: (2**k - 1) / sp.factorial(k)
check("sf-02a 一般項 a_n=(2^n-1)/n! 前 8 項", all(sp.simplify(an(k) - c[k]) == 0 for k in range(8)))
expr = (n + 2) * (n + 1) * an(n + 2) - 3 * (n + 1) * an(n + 1) + 2 * an(n)
check("sf-02a 一般項代回遞迴為 0", sp.simplify(sp.combsimp(expr)) == 0)
check("sf-02a 特徵根 c1=-1,c2=1", sp.solve([sp.Symbol("c1") + sp.Symbol("c2"), sp.Symbol("c1") + 2 * sp.Symbol("c2") - 1]) == {sp.Symbol("c1"): -1, sp.Symbol("c2"): 1})
check("sf-02a closed form", sp.simplify(L(sp.exp(2 * x) - sp.exp(x))) == 0)

# ---------------- am4-sf-02b
for pv, expect in ((3, [1, 3, 3, 1, 0, 0]), (R(1, 2), [1, R(1, 2), R(-1, 8), R(1, 16)])):
    L = lambda y, pv=pv: (1 + x) * D(y) - pv * y
    cc = [sp.Integer(1)]
    for k in range(len(expect) - 1):
        cc.append(sp.Rational(pv - k, k + 1) * cc[-1] if isinstance(pv, int) else (pv - k) / (k + 1) * cc[-1])
    ser = sp.series((1 + x) ** pv, x, 0, len(expect)).removeO()
    check(f"sf-02b p={pv} 係數", [ser.coeff(x, k) for k in range(len(expect))] == expect and cc == expect)
check("sf-02b p=3 截斷 (1+x)^3", sp.expand((1 + x) ** 3) == 1 + 3 * x + 3 * x**2 + x**3)
check("sf-02b √1.2≈1.0955", abs(1 + 0.1 - 0.005 + 0.0005 - 1.0955) < 1e-12 and abs(1.2**0.5 - 1.0955) < 1e-4)

# ---------------- am4-ex-2
L = lambda y: D(y, 2) - x * D(y) + y
c0 = coeffs(L, 8, (1, 0))
c1 = coeffs(L, 8, (0, 1))
check("ex-2 a2,a4,a6", [c0[2], c0[4], c0[6]] == [R(-1, 2), R(-1, 24), R(-1, 240)])
check("ex-2 奇次截斷 y2=x", all(c1[k] == 0 for k in range(2, 9)))

# ---------------- am4-hw-1 / am4-k114-1
for sgn, tag in ((1, "hw-1"), (-1, "k114-1")):
    L = lambda y, s=sgn: D(y, 2) + s * x**2 * D(y) + s * x * y
    c0 = coeffs(L, 8, (1, 0))
    c1 = coeffs(L, 8, (0, 1))
    check(f"{tag} a2=a5=0", c0[2] == 0 and c0[5] == 0 and c1[2] == 0 and c1[5] == 0)
    check(f"{tag} a3,a6", [c0[3], c0[6]] == [-sgn * R(1, 6), R(1, 45)])
    check(f"{tag} a4,a7", [c1[4], c1[7]] == [-sgn * R(1, 6), R(5, 252)])
check("hw-1 中間值 -2/15·(-1/6)=1/45", R(-2, 15) * R(-1, 6) == R(1, 45))
check("hw-1 中間值 -5/42·(-1/6)=5/252", R(-5, 42) * R(-1, 6) == R(5, 252))

# ---------------- am4-hw-2
L = lambda y: D(y, 2) + (x**3 + 1) * D(y) - y
c0 = coeffs(L, 6, (1, 0))
c1 = coeffs(L, 6, (0, 1))
check("hw-2 y1 a2..a4", c0[2:5] == [R(1, 2), R(-1, 6), R(1, 12)])
check("hw-2 y2 a2..a4", c1[2:5] == [R(-1, 2), R(1, 3), R(-1, 8)])

# ---------------- am4-k112-3
L = lambda y: D(y, 2) - 4 * x * D(y) + (4 * x**2 - 2) * y
c0 = coeffs(L, 9, (1, 0))
c1 = coeffs(L, 9, (0, 1))
check("k112-3 a2,a4,a6", [c0[2], c0[4], c0[6]] == [1, R(1, 2), R(1, 6)])
check("k112-3 a3,a5,a7", [c1[3], c1[5], c1[7]] == [1, R(1, 2), R(1, 6)])
k = sp.symbols("k", integer=True, positive=True)
left = (2 * k + 2) * (2 * k + 1) / sp.factorial(k + 1)
right = (8 * k + 2) / sp.factorial(k) - 4 / sp.factorial(k - 1)
check("k112-3 左=右=2(2k+1)/k!", sp.simplify(sp.combsimp(left - 2 * (2 * k + 1) / sp.factorial(k))) == 0 and sp.simplify(sp.combsimp(right - 2 * (2 * k + 1) / sp.factorial(k))) == 0)
check("k112-3 (a0+a1x)e^{x^2}", sp.simplify(L((a0 + a1 * x) * sp.exp(x**2))) == 0)

# ---------------- am4-sf-03a
lam = 3
L = lambda y: D(y, 2) - 2 * x * D(y) + 2 * lam * y
c1 = coeffs(L, 8, (0, 1))
c0 = coeffs(L, 8, (1, 0))
check("sf-03a a3=-2/3 a1, a5=0", c1[3] == R(-2, 3) and c1[5] == 0 and c1[7] == 0)
check("sf-03a a1=-12 → 8x^3-12x", sp.expand(-12 * (x + c1[3] * x**3)) == 8 * x**3 - 12 * x)
check("sf-03a 偶次 a2,a4,a6", [c0[2], c0[4], c0[6]] == [-3, R(1, 2), R(1, 30)])
check("sf-03a 8x^3-12x 是解", sp.simplify(L(8 * x**3 - 12 * x)) == 0)

# ---------------- am4-sf-03b
L = lambda y: D(y, 2) - x * y
c = coeffs(L, 13, (1, 0))
check("sf-03b a3,a6,a9,a12", [c[3], c[6], c[9], c[12]] == [R(1, 6), R(1, 180), R(1, 12960), R(1, 1710720)])
check("sf-03b 其餘為 0", all(c[j] == 0 for j in range(1, 13) if j % 3))
s4 = sum(c[j] for j in (0, 3, 6, 9))
check("sf-03b 4 項和 1.172299", abs(float(s4) - 1.172299) < 5e-7)
check("sf-03b y(1)≈1.17230", round(float(sum(c)), 5) == 1.17230)
check("sf-03b a12≈5.8e-7", abs(float(c[12]) - 5.8e-7) < 0.05e-7)
check("sf-03b 下一項比值 ≥210", 15 * 14 == 210)
check("sf-03b 各項小數", [round(float(c[j]), 7) for j in (3, 6, 9, 12)] == [0.1666667, 0.0055556, 0.0000772, 0.0000006])

# ---------------- am4-hw-3
L = lambda y: (x - 1) * D(y, 2) - x * D(y) + y
cg = coeffs(L, 6, (a0, a1))
check("hw-3 a2,a3,a4=a0/2!,a0/3!,a0/4!", [sp.simplify(cg[j] - a0 / sp.factorial(j)) for j in (2, 3, 4)] == [0, 0, 0])
check("hw-3 8x-2e^x", sp.simplify(L(8 * x - 2 * sp.exp(x))) == 0 and (8 * x - 2 * sp.exp(x)).subs(x, 0) == -2 and D(8 * x - 2 * sp.exp(x)).subs(x, 0) == 6)

# ---------------- am4-k113-2
L = lambda y: D(y, 2) - (1 + x) * y
c = coeffs(L, 7, (1, 0))
check("k113-2 a2..a6", c[2:7] == [R(1, 2), R(1, 6), R(1, 24), R(1, 30), R(1, 144)])

# ---------------- am4-k110-3
L = lambda y: D(y, 2) - x**2 * D(y) + (x + 2) * y
c = coeffs(L, 7, (2, 1), rhs=x)
check("k110-3 a2..a6", c[2:7] == [-2, R(-1, 2), R(1, 3), R(-1, 20), R(-1, 18)])

# ---------------- am4-k111-3
L = lambda y: (x**2 + 1) * D(y, 2) - 2 * x * D(y) + 2 * y
c0 = coeffs(L, 8, (1, 0))
c1 = coeffs(L, 8, (0, 1))
check("k111-3 偶次 1-x^2 截斷", c0[2] == -1 and all(c0[j] == 0 for j in range(3, 9)))
check("k111-3 奇次 x 截斷", all(c1[j] == 0 for j in range(2, 9)))
yy = 1 + x - x**2
check("k111-3 y=1+x-x^2", sp.simplify(L(yy)) == 0 and yy.subs(x, 0) == 1 and yy.subs(x, 1) == 1)

# ---------------- am4-sf-04a
L = lambda y: D(y, 2, t) + t * D(y, 1, t) + y
c = coeffs(L, 7, (2, 0), var=t)
check("sf-04a a2,a4,a6", [c[2], c[4], c[6]] == [-1, R(1, 4), R(-1, 24)])
check("sf-04a 2e^{-t^2/2}", sp.simplify(L(2 * sp.exp(-t**2 / 2))) == 0)
check("sf-04a e^{-0.125}≈0.8825", round(float(sp.exp(-0.125)), 4) == 0.8825)
check("sf-04a y(1.5)≈1.7650", round(2 * float(sp.exp(-0.125)), 4) == 1.7650)

# ---------------- am4-sf-04b
L = lambda y: D(y, 2) - x * D(y) - y
c = coeffs(L, 7, (0, 0), rhs=sp.series(1 / (1 - x), x, 0, 9).removeO())
check("sf-04b a2..a6", c[2:7] == [R(1, 2), R(1, 6), R(5, 24), R(1, 12), R(49, 720)])
check("sf-04b 中間值 1/12+1/8=5/24, 1/20+1/30=1/12, 1/30+5/144=49/720", R(1, 12) + R(1, 8) == R(5, 24) and R(1, 20) + R(1, 30) == R(1, 12) and R(1, 30) + R(5, 144) == R(49, 720))
check("sf-04b e^{x^2/2} 是齊次解", sp.simplify(L(sp.exp(x**2 / 2))) == 0)
check("sf-04b y''=(1+x^2)e^{x^2/2}", sp.simplify(D(sp.exp(x**2 / 2), 2) - (1 + x**2) * sp.exp(x**2 / 2)) == 0)
cbig = [sp.Integer(0), sp.Integer(0)]
for m in range(0, 60):
    cbig.append(R(1, (m + 2) * (m + 1)) + cbig[m] / (m + 2))
check("sf-04b a_{n+1}/a_n → 1", abs(float(cbig[61] / cbig[60]) - 1) < 0.05)

print(f"\n{COUNT[0]} checks, {len(FAILS)} failed")
if FAILS:
    print("FAILED:", FAILS)
    sys.exit(1)
print("ALL CHECKS PASSED")
