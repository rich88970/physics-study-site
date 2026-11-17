"""應用數學第 5 章考試書寫版（exam.html 的「背公式＋計算」改寫）：驗算書寫版裡出現的所有數值與中間值。

做法：Frobenius 係數用 sympy 獨立重算（把 x^γ Σ c_k x^k 代入方程式、逐階解），
降階法的展開用 sympy.series 重算，再和書寫版的數字逐一比對。
用法：python tools/verify_writeup_applied-math_ch05.py   全部通過時印出 ALL CHECKS PASSED。
"""
import sys
import sympy as sp

x = sp.symbols("x", positive=True)
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


def frob(L, g, N, free=None):
    """y=x^g Σ c_k x^k（c0=1）代入 L，逐階解出 c1..cN；free={k: 值} 指定任意係數的取值。"""
    c = sp.symbols(f"c0:{N + 1}")
    y = x**g * sum(c[k] * x**k for k in range(N + 1))
    expr = sp.expand(sp.powsimp(sp.expand(L(y) * x**(-g) * x**2)))
    sol = {c[0]: 1}
    free = free or {}
    for k in range(1, N + 1):
        eq = sp.expand(expr.coeff(x, k + 1).subs(sol)) if k + 1 > 0 else 0
        # 找含 c_k 的最低次方程式
        found = False
        for power in range(-2, N + 3):
            e = sp.expand(expr.coeff(x, power).subs(sol))
            if c[k] in e.free_symbols and all(s == c[k] for s in e.free_symbols if s in c):
                sol[c[k]] = sp.solve(e, c[k])[0]
                found = True
                break
        if not found:
            sol[c[k]] = free.get(k, 0)
    return [sp.nsimplify(sol[c[k]]) for k in range(N + 1)]


def residual_ok(L, y, upto):
    """L(y) 的 Laurent／Puiseux 展開在 x^upto 之前都是 0。"""
    s = sp.series(sp.expand(L(y)), x, 0, upto).removeO()
    return sp.simplify(s) == 0


def indicial(p0, q0):
    g = sp.symbols("g")
    return set(sp.solve(g * (g - 1) + p0 * g + q0, g))


# ---------------- am5-ex-1
L = lambda y: 2 * x**2 * D(y, 2) - x * D(y) + (1 + x) * y
check("ex-1 p0,q0", sp.limit(x * (-x) / (2 * x**2), x, 0) == R(-1, 2) and sp.limit(x**2 * (1 + x) / (2 * x**2), x, 0) == R(1, 2))
check("ex-1 指標 1, 1/2", indicial(R(-1, 2), R(1, 2)) == {1, R(1, 2)})
check("ex-1 γ=1 係數", frob(L, 1, 3)[1:] == [R(-1, 3), R(1, 30), R(-1, 630)])
check("ex-1 γ=1/2 係數", frob(L, R(1, 2), 3)[1:] == [-1, R(1, 6), R(-1, 90)])

# ---------------- am5-hw-1
L = lambda y: 2 * x**2 * D(y, 2) + 3 * x * D(y) + (2 * x - 1) * y
check("hw-1 指標 1/2, -1", indicial(R(3, 2), R(-1, 2)) == {R(1, 2), -1})
check("hw-1 γ=-1 係數 2,-2,4/9", frob(L, -1, 3)[1:] == [2, -2, R(4, 9)])
check("hw-1 γ=1/2 係數 -2/5,2/35,-4/945", frob(L, R(1, 2), 3)[1:] == [R(-2, 5), R(2, 35), R(-4, 945)])

# ---------------- am5-sf-01a
L = lambda y: 4 * x * D(y, 2) + 2 * D(y) + y
check("sf-01a 指標 0, 1/2", indicial(R(1, 2), 0) == {0, R(1, 2)})
c0 = frob(L, 0, 4)
c1 = frob(L, R(1, 2), 4)
check("sf-01a γ=0 係數 (-1)^n/(2n)!", all(c0[n] == R((-1) ** n, sp.factorial(2 * n)) for n in range(5)))
check("sf-01a γ=1/2 係數 (-1)^n/(2n+1)!", all(c1[n] == R((-1) ** n, sp.factorial(2 * n + 1)) for n in range(5)))
y = 3 * sp.cos(sp.sqrt(x)) - 2 * sp.sin(sp.sqrt(x))
check("sf-01a y=3cos√x-2sin√x 是解", sp.simplify(L(y)) == 0)
check("sf-01a y(0)=3, y(π²/4)=-2", sp.limit(y, x, 0) == 3 and sp.simplify(y.subs(x, sp.pi**2 / 4)) == -2)
check("sf-01a y1'(0)=-1/2、y2' 發散", sp.limit(D(sp.cos(sp.sqrt(x))), x, 0) == R(-1, 2) and sp.limit(D(sp.sin(sp.sqrt(x))), x, 0, "+") == sp.oo)

# ---------------- am5-sf-01b
L = lambda y: 2 * x * D(y, 2) + (1 + x) * D(y) + y
c0 = frob(L, 0, 4)
check("sf-01b γ=0 係數 -1,1/3,-1/15,1/105", c0[1:] == [-1, R(1, 3), R(-1, 15), R(1, 105)])
c1 = frob(L, R(1, 2), 4)
check("sf-01b γ=1/2 係數 (-1/2)^n/n!", c1 == [1, R(-1, 2), R(1, 8), R(-1, 48), R(1, 384)])
check("sf-01b √x e^{-x/2} 是解", sp.simplify(L(sp.sqrt(x) * sp.exp(-x / 2))) == 0)
check("sf-01b y1'(0)=-1", c0[1] == -1)

# ---------------- am5-ex-2
L = lambda y: (x**2 - x) * D(y, 2) + (3 * x - 1) * D(y) + y
P = (3 * x - 1) / (x**2 - x)
check("ex-2 p0=1,q0=0", sp.limit(x * P, x, 0) == 1 and sp.limit(x**2 / (x**2 - x), x, 0) == 0)
check("ex-2 部分分式 P=1/x+2/(x-1)", sp.simplify(P - (1 / x + 2 / (x - 1))) == 0)
check("ex-2 a_{n+1}=a_n（全為 1）", frob(L, 0, 5) == [1] * 6)
check("ex-2 y1=1/(1-x), y2=ln x/(1-x) 是解", sp.simplify(L(1 / (1 - x))) == 0 and sp.simplify(L(sp.log(x) / (1 - x))) == 0)

# ---------------- am5-sf-02a
L = lambda y: x * D(y, 2) + (1 - x) * D(y) - y
check("sf-02a y1=e^x", sp.simplify(L(sp.exp(x))) == 0 and frob(L, 0, 4) == [1, 1, R(1, 2), R(1, 6), R(1, 24)])
up = sp.series(sp.exp(-x) / x, x, 0, 3).removeO()
check("sf-02a u'=1/x-1+x/2-x^2/6", sp.simplify(up - (1 / x - 1 + x / 2 - x**2 / 6)) == 0)
u = sp.log(x) - x + x**2 / 4 - x**3 / 18
check("sf-02a u 逐項積分", sp.simplify(D(u) - up) == 0)
rest = sp.expand(sp.series(sp.exp(x) * (u - sp.log(x)), x, 0, 4).removeO())
check("sf-02a 其餘部分 -x-3/4x^2-11/36x^3", sp.simplify(rest - (-x - R(3, 4) * x**2 - R(11, 36) * x**3)) == 0)
check("sf-02a 中間值 1/4-1=-3/4, -1/18+1/4-1/2=-11/36", R(1, 4) - 1 == R(-3, 4) and R(-1, 18) + R(1, 4) - R(1, 2) == R(-11, 36))
y2 = sp.exp(x) * sp.log(x) + rest
check("sf-02a y2 代回殘差到 x^2 為 0", residual_ok(L, y2, 3))

# ---------------- am5-sf-02b
L = lambda y: x**2 * D(y, 2) + 3 * x * D(y) + (1 + x) * y
check("sf-02b 指標重根 -1", indicial(3, 1) == {-1})
cc = frob(L, -1, 4)
check("sf-02b c_n=(-1)^n/(n!)^2", cc == [1, -1, R(1, 4), R(-1, 36), R(1, 576)])
y1 = sum(cc[n] * x**(n - 1) for n in range(5))
b1, b2, b3 = 2, R(-3, 4), R(11, 108)
check("sf-02b b 遞迴 n^2b_n+b_{n-1}=-2nc_n", b1 == -2 * cc[1] and 4 * b2 + b1 == -4 * cc[2] and 9 * b3 + b2 == -6 * cc[3])
y2 = y1 * sp.log(x) + b1 + b2 * x + b3 * x**2
check("sf-02b y2 代回殘差到 x^2 為 0", residual_ok(L, y2, 3))
check("sf-02b L[y1 ln x] 非對數部分 = 2xy1'+2y1", sp.simplify(sp.expand(L(y1 * sp.log(x)) - sp.log(x) * L(y1)) - (2 * x * D(y1) + 2 * y1)) == 0)

# ---------------- am5-ex-3
L = lambda y: x * D(y, 2) + 3 * D(y) - y
check("ex-3 指標 0,-2", indicial(3, 0) == {0, -2})
cc = frob(L, 0, 4)
check("ex-3 γ=0 係數 1/3,1/24,1/360", cc[1:4] == [R(1, 3), R(1, 24), R(1, 360)])
y1 = sum(cc[n] * x**n for n in range(5))
inv = sp.series(1 / y1**2, x, 0, 4).removeO()
check("ex-3 1/y1^2=1-2/3x+1/4x^2-19/270x^3", sp.simplify(inv - (1 - R(2, 3) * x + R(1, 4) * x**2 - R(19, 270) * x**3)) == 0)
u = -1 / (2 * x**2) + R(2, 3) / x + R(1, 4) * sp.log(x) - R(19, 270) * x
check("ex-3 u 逐項積分", sp.simplify(D(u) - sp.expand(inv / x**3)) == 0)
nonlog = sp.expand(sp.series((u - R(1, 4) * sp.log(x)) * y1, x, 0, 1).removeO())
check("ex-3 y2 非對數部分 x^-2(-1/2+x/2+29/144x^2)", sp.simplify(nonlog - (-R(1, 2) / x**2 + R(1, 2) / x + R(29, 144))) == 0)
cc6 = frob(L, 0, 8)
Y1 = sum(cc6[n] * x**n for n in range(9))
y2 = R(1, 4) * Y1 * sp.log(x) + sp.expand(sp.series((u - R(1, 4) * sp.log(x)) * Y1, x, 0, 1).removeO())
check("ex-3 y2 代回殘差到 x^-1 為 0", residual_ok(L, y2, 0))

# ---------------- am5-hw-2
L = lambda y: x * D(y, 2) - x * D(y) + y
check("hw-2 y1=x", sp.simplify(L(x)) == 0)
ser = sp.series(sp.exp(x) / x**2, x, 0, 3).removeO()
check("hw-2 e^x/x^2 展開", sp.simplify(ser - (1 / x**2 + 1 / x + R(1, 2) + x / 6 + x**2 / 24)) == 0)
u = -1 / x + sp.log(x) + x / 2 + x**2 / 12 + x**3 / 72
check("hw-2 u 逐項積分", sp.simplify(D(u) - ser) == 0)
y2 = sp.expand(x * u)
check("hw-2 y2=x ln x-1+x^2/2+x^3/12+x^4/72", sp.simplify(y2 - (x * sp.log(x) - 1 + x**2 / 2 + x**3 / 12 + x**4 / 72)) == 0)
check("hw-2 y2 代回殘差到 x^2 為 0", residual_ok(L, y2, 3))

# ---------------- am5-k110-4
L = lambda y: x * D(y, 2) + (x - 1) * D(y) - y
check("k110-4 指標 2,0", indicial(-1, 0) == {0, 2})
check("k110-4 1-x、e^{-x}-1+x 是解", sp.simplify(L(1 - x)) == 0 and sp.simplify(L(sp.exp(-x) - 1 + x)) == 0)
cc = frob(L, 2, 4)
check("k110-4 γ=2：a_n=-a_{n-1}/(n+2)", all(cc[n] == -cc[n - 1] / (n + 2) for n in range(1, 5)))
check("k110-4 a0=1/2 → (-1)^n/(n+2)!", all(cc[n] / 2 == R((-1) ** n, sp.factorial(n + 2)) for n in range(5)))
c1, c2 = sp.symbols("c1 c2")
yg = c1 * (1 - x) + c2 * (sp.exp(-x) - 1 + x)
check("k110-4 c1=1, c2=0", sp.solve([yg.subs(x, 0) - 1, yg.subs(x, 1)], [c1, c2]) == {c1: 1, c2: 0})

# ---------------- am5-k112-4
L = lambda y: (x**2 + 2 * x) * D(y, 2) - 2 * (x + 1) * D(y) + 2 * y
check("k112-4 p0=-1,q0=0", sp.limit(-2 * (x + 1) / (x + 2), x, 0) == -1 and sp.limit(2 * x / (x + 2), x, 0) == 0)
check("k112-4 1+x、x^2 是解", sp.simplify(L(1 + x)) == 0 and sp.simplify(L(x**2)) == 0)
s = sp.symbols("s")
check("k112-4 兩組係數因式分解", sp.factor(2 * s * (s - 1) - 2 * s) == 2 * s * (s - 2) and sp.factor((s - 1) * (s - 2) - 2 * (s - 1) + 2) == (s - 3) * (s - 2))

# ---------------- am5-k114-2
L = lambda y: x**2 * D(y, 2) + x * D(y) + (x**2 - R(1, 4)) * y
check("k114-2 指標 ±1/2", indicial(1, R(-1, 4)) == {R(1, 2), R(-1, 2)})
c_a = frob(L, R(1, 2), 4)
c_b = frob(L, R(-1, 2), 4)
check("k114-2 γ=1/2：a2=-1/6,a4=1/120", c_a[1] == 0 and c_a[2] == R(-1, 6) and c_a[4] == R(1, 120))
check("k114-2 γ=-1/2：a2=-1/2,a4=1/24", c_b[2] == R(-1, 2) and c_b[4] == R(1, 24))
check("k114-2 sin x/√x、cos x/√x 是解", sp.simplify(L(sp.sin(x) / sp.sqrt(x))) == 0 and sp.simplify(L(sp.cos(x) / sp.sqrt(x))) == 0)

# ---------------- am5-sf-03a
L = lambda y: x * D(y, 2) + 2 * D(y) - x * y
check("sf-03a(a) 指標 0,-1", indicial(2, 0) == {0, -1})
check("sf-03a(a) cosh x/x、sinh x/x 是解", sp.simplify(L(sp.cosh(x) / x)) == 0 and sp.simplify(L(sp.sinh(x) / x)) == 0)
ser = sp.series(sp.cosh(x) / x, x, 0, 5).removeO()
check("sf-03a(a) a2=a0/2,a4=a0/24", sp.expand(ser * x).coeff(x, 2) == R(1, 2) and sp.expand(ser * x).coeff(x, 4) == R(1, 24))
ser = sp.expand(sp.series(sp.sinh(x), x, 0, 6).removeO())
check("sf-03a(a) a3=a1/6,a5=a1/120", ser.coeff(x, 3) == R(1, 6) and ser.coeff(x, 5) == R(1, 120))
L = lambda y: x * D(y, 2) - y
check("sf-03a(b) γ=1 係數 1/2,1/12,1/144", frob(L, 1, 3)[1:] == [R(1, 2), R(1, 12), R(1, 144)])

# ---------------- am5-sf-03b
L = lambda y: x * D(y, 2) + y
cc = frob(L, 1, 5)
check("sf-03b y1 係數 -1/2,1/12,-1/144", cc[1:4] == [R(-1, 2), R(1, 12), R(-1, 144)])
y1 = sum(cc[n] * x**(n + 1) for n in range(6))
nonlog = sp.expand(L(y1 * sp.log(x)) - sp.log(x) * L(y1))
check("sf-03b L[y1 ln x] 非對數 1-3/2x+5/12x^2", sp.expand(nonlog).coeff(x, 0) == 1 and nonlog.coeff(x, 1) == R(-3, 2) and nonlog.coeff(x, 2) == R(5, 12))
y2 = -y1 * sp.log(x) + 1 - R(3, 4) * x**2 + R(7, 36) * x**3
check("sf-03b k=-1,b2=-3/4,b3=7/36 殘差到 x^2 為 0", residual_ok(L, y2, 3))
check("sf-03b 中間值 3/4+5/12=7/6", R(3, 4) + R(5, 12) == R(7, 6))

# ---------------- am5-ex-4 / ex-5（Legendre）
l, nn = sp.symbols("l n")
rec = lambda n_, a: (n_ - l) * (n_ + l + 1) / ((n_ + 2) * (n_ + 1)) * a
A2 = rec(0, 1)
A3 = rec(1, 1)
A4 = rec(2, A2)
A5 = rec(3, A3)
check("ex-4 a2,a3", sp.simplify(A2 + l * (l + 1) / 2) == 0 and sp.simplify(A3 + (l - 1) * (l + 2) / 6) == 0)
check("ex-4 a4,a5", sp.simplify(A4 - (l - 2) * l * (l + 1) * (l + 3) / 24) == 0 and sp.simplify(A5 - (l - 3) * (l - 1) * (l + 2) * (l + 4) / 120) == 0)
check("ex-4 n(n+1)-l(l+1)=(n-l)(n+l+1)", sp.expand(nn * (nn + 1) - l * (l + 1) - (nn - l) * (nn + l + 1)) == 0)
check("ex-4 l=0 奇串比值 n/(n+2)", sp.simplify(rec(nn, 1).subs(l, 0) - nn / (nn + 2)) == 0)
check("ex-4 l=1 偶串比值 (n-1)/(n+1)", sp.simplify(rec(nn, 1).subs(l, 1) - (nn - 1) / (nn + 1)) == 0)
odd = [1]
for n_ in (1, 3):
    odd.append(rec(n_, odd[-1]).subs(l, 0))
even = [1]
for n_ in (0, 2, 4):
    even.append(rec(n_, even[-1]).subs(l, 1))
check("ex-4 l=0 奇串 1,1/3,1/5", odd == [1, R(1, 3), R(1, 5)])
check("ex-4 l=1 偶串 1,-1,-1/3,-1/5", even == [1, -1, R(-1, 3), R(-1, 5)])
P = {0: sp.Integer(1), 1: x}
for k in range(2, 6):
    P[k] = sp.expand(((2 * k - 1) * x * P[k - 1] - (k - 1) * P[k - 2]) / k)
check("ex-5 P2,P3", P[2] == sp.expand(R(1, 2) * (3 * x**2 - 1)) and P[3] == sp.expand(R(1, 2) * (5 * x**3 - 3 * x)))
check("ex-5 l=2:a2=-3a0；l=3:a3=-5/3a1", rec(0, 1).subs(l, 2) == -3 and rec(1, 1).subs(l, 3) == R(-5, 3) and rec(2, 1).subs(l, 2) == 0 and rec(3, 1).subs(l, 3) == 0)
check("ex-5 1-3x^2、3x-5x^3 在 1 為 -2", (1 - 3 * x**2).subs(x, 1) == -2 and (3 * x - 5 * x**3).subs(x, 1) == -2)
check("ex-5 3P3=(15x^3-9x)/2", sp.expand(5 * x * P[2] - 2 * P[1]) == sp.expand((15 * x**3 - 9 * x) / 2))

# ---------------- am5-k114-3
check("k114-3 P2 零點 ±0.577、P2(0)=-1/2", abs(float(1 / sp.sqrt(3)) - 0.577) < 5e-4 and P[2].subs(x, 0) == R(-1, 2))
check("k114-3 P3 零點 ±0.775", abs(float(sp.sqrt(R(3, 5))) - 0.775) < 5e-4)
xe = 1 / sp.sqrt(5)
check("k114-3 P3 極值 x=±0.447 值 ∓0.447", sp.simplify(D(P[3]).subs(x, xe)) == 0 and sp.simplify(P[3].subs(x, xe) + 1 / sp.sqrt(5)) == 0 and abs(float(xe) - 0.447) < 5e-4)

# ---------------- am5-sf-04a
check("sf-04a P4", P[4] == sp.expand((35 * x**4 - 30 * x**2 + 3) / 8))
check("sf-04a P5", P[5] == sp.expand((63 * x**5 - 70 * x**3 + 15 * x) / 8))
check("sf-04a 4P4 中間式", sp.expand(7 * x * R(1, 2) * (5 * x**3 - 3 * x) - 3 * R(1, 2) * (3 * x**2 - 1)) == sp.expand(R(1, 2) * (35 * x**4 - 30 * x**2 + 3)))
check("sf-04a 5P5 中間式", sp.expand(9 * x * P[4] - 4 * P[3]) == sp.expand((315 * x**5 - 350 * x**3 + 75 * x) / 8))
a2 = rec(0, 1).subs(l, 4)
a4 = rec(2, a2).subs(l, 4)
check("sf-04a 截斷 a2=-10,a4=35/3,a6=0", a2 == -10 and a4 == R(35, 3) and rec(4, a4).subs(l, 4) == 0)
check("sf-04a 在 1 的值 8/3、3/8 倍", 1 + a2 + a4 == R(8, 3) and sp.expand(R(3, 8) * (1 + a2 * x**2 + a4 * x**4)) == P[4])
check("sf-04a √(900-420)=21.91", abs((900 - 420) ** 0.5 - 21.91) < 0.005)
us = sorted(float(r) for r in sp.solve(35 * sp.Symbol("u") ** 2 - 30 * sp.Symbol("u") + 3))
check("sf-04a u=0.1156, 0.7416", abs(us[0] - 0.1156) < 5e-5 and abs(us[1] - 0.7416) < 5e-5)
check("sf-04a x=±0.340, ±0.861", abs(us[0] ** 0.5 - 0.340) < 5e-4 and abs(us[1] ** 0.5 - 0.861) < 5e-4)
check("sf-04a P4(0)=3/8", P[4].subs(x, 0) == R(3, 8))

# ---------------- am5-sf-04b
vals = [sp.integrate(P[k], (x, 0, 1)) for k in (1, 2, 3, 4)]
check("sf-04b ∫P_l = 1/2,0,-1/8,0", vals == [R(1, 2), 0, R(-1, 8), 0])
form = [(P[k - 1].subs(x, 0) - P[k + 1].subs(x, 0)) / (2 * k + 1) for k in (1, 2, 3, 4)]
check("sf-04b 公式值相同", form == vals)
check("sf-04b ⑤ (2l+1)P_l=P'_{l+1}-P'_{l-1}", all(sp.expand((2 * k + 1) * P[k] - D(P[k + 1]) + D(P[k - 1])) == 0 for k in (1, 2, 3, 4)))

print(f"\n{COUNT[0]} checks, {len(FAILS)} failed")
if FAILS:
    print("FAILED:", FAILS)
    sys.exit(1)
print("ALL CHECKS PASSED")
