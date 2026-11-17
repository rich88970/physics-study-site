"""應用數學第 6 章（Bessel 方程與 Bessel 函數）：每張題目卡與變化題的答案用 sympy／mpmath 獨立驗算。

做法：
- 級數：由遞迴重新產生 J_m 的係數，代入 Bessel 方程到指定階；降階法的第二解代入方程式，檢查殘差從截斷階才開始。
- 封閉形式：sympy.checkodesol 或直接代入（J_{±1/2}、sin(x^2)/x、J0(λe^x)、√x J_{±1/3}）。
- 恆等式、積分：sympy 的 besselj 數值比對；定積分用 mpmath.quad 與網站的封閉式比較。
- 零點：mpmath.besseljzero／besselyzero，與板書零點表（一位小數）及網站的精確值比對。

用法：python tools/verify_applied_math_ch06.py   全部通過時印出 ALL CHECKS PASSED。
"""
import sys
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
import mpmath as mp

mp.mp.dps = 30
x = sp.symbols("x", positive=True)
t = sp.symbols("t", positive=True)
R = sp.Rational
FAILS = []
COUNT = [0]


def check(name, cond):
    COUNT[0] += 1
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAILS.append(name)


def close(a, b, tol=1e-9):
    return abs(complex(a) - complex(b)) <= tol * max(1.0, abs(complex(b)))


def bessel_L(y, m):
    return sp.expand(x**2 * sp.diff(y, x, 2) + x * sp.diff(y, x) + (x**2 - m**2) * y)


def Jser(m, N):
    return sum((-1)**k / (sp.factorial(k) * sp.factorial(k + m)) * (x / 2)**(2 * k + m) for k in range(N))


J = mp.besselj
Yb = mp.bessely

# ---------------- 第 1 節 ----------------
# am6-ex-1：遞迴產生係數，與 J_m 一般項一致；代入方程到高階
for m in range(4):
    a = {0: R(1, 2**m * sp.factorial(m))}
    a[1] = 0
    for n in range(2, 14):
        a[n] = -a[n - 2] / ((n + 2 * m) * n)
    ok = all(sp.simplify(a[2 * k] - (-1)**k / (sp.factorial(k) * sp.factorial(k + m) * 2**(2 * k + m))) == 0 for k in range(7))
    check(f"ex-1 遞迴係數 = J_{m} 一般項 (m={m})", ok)
    res = bessel_L(Jser(m, 7), m)
    low = min(sp.Poly(res, x).monoms())[0] if res != 0 else 99
    check(f"ex-1 J_{m} 級數代入方程，殘差最低次 >= {14 + m}", low >= 14 + m)
check("ex-1 J0 前三項", sp.expand(Jser(0, 3)) == 1 - x**2 / 4 + x**4 / 64)
check("ex-1 J1 前三項", sp.expand(Jser(1, 3)) == x / 2 - x**3 / 16 + x**5 / 384)
check("ex-1 n=1 係數 (1+γ)^2-m^2 在 γ=m 為 1+2m", sp.expand((1 + sp.Symbol('m'))**2 - sp.Symbol('m')**2) == 1 + 2 * sp.Symbol('m'))

# am6-sf-01a：J0(λe^x) 滿足 y''+λ²e^{2x}y=0；本徵值與零點
lam = sp.symbols("lam", positive=True)
xx = sp.symbols("xx", real=True)
y = sp.besselj(0, lam * sp.exp(xx))
expr = sp.diff(y, xx, 2) + lam**2 * sp.exp(2 * xx) * y
check("sf-01a J0(λe^x) 代入方程（數值）", all(abs(complex(expr.subs({lam: 2.3, xx: v}).evalf())) < 1e-12 for v in (-2, -0.5, 0)))
yb = sp.bessely(0, lam * sp.exp(xx))
expr2 = sp.diff(yb, xx, 2) + lam**2 * sp.exp(2 * xx) * yb
check("sf-01a Y0(λe^x) 也是解", all(abs(complex(expr2.subs({lam: 2.3, xx: v}).evalf())) < 1e-12 for v in (-2, -0.5, 0)))
j01, j02, j03 = (mp.besseljzero(0, k) for k in (1, 2, 3))
check("sf-01a λ = 2.405, 5.520, 8.654", close(j01, 2.4048, 1e-4) and close(j02, 5.5201, 1e-4) and close(j03, 8.6537, 1e-4))
check("sf-01a y2 內部零點 x = ln(j01/j02) = -0.831", close(mp.log(j01 / j02), -0.831, 1e-3))
mm = 1.7
ym = sp.besselj(mm, sp.exp(xx))
check("sf-01a 推廣 J_m(e^x) 滿足 y''+(e^{2x}-m^2)y=0", all(abs(complex((sp.diff(ym, xx, 2) + (sp.exp(2 * xx) - mm**2) * ym).subs(xx, v).evalf())) < 1e-12 for v in (-1, 0.3)))

# am6-sf-01b：√x J_{±1/3}(2/3 x^{3/2}) 滿足 y''+xy=0
for nu in (R(1, 3), R(-1, 3)):
    yy = sp.sqrt(x) * sp.besselj(nu, R(2, 3) * x**R(3, 2))
    e = sp.diff(yy, x, 2) + x * yy
    check(f"sf-01b √x J_{nu}(2/3 x^1.5) 代入 y''+xy", all(abs(complex(e.subs(x, v).evalf(30))) < 1e-12 for v in (0.3, 1.1, 2.7)))
w = sp.symbols("w", cls=sp.Function)
ysub = sp.sqrt(x) * w(x)
lhs = sp.expand(sp.simplify((sp.diff(ysub, x, 2) + x * ysub) * x**R(3, 2)))
check("sf-01b (a) x^2 w''+x w'+(x^3-1/4)w", sp.simplify(lhs - (x**2 * sp.diff(w(x), x, 2) + x * sp.diff(w(x), x) + (x**3 - R(1, 4)) * w(x))) == 0)
# 首項：√x J_{1/3} ∝ x(1 - x^3/12 + ...)
ser = sp.series(sp.sqrt(x) * sp.besselj(R(1, 3), R(2, 3) * x**R(3, 2)), x, 0, 6).removeO()
c1 = sp.nsimplify(sp.simplify(ser.coeff(x, 1)))
check("sf-01b √x J_{1/3} ∝ x - x^4/12", c1 != 0 and sp.simplify(ser.coeff(x, 4) / c1 + R(1, 12)) == 0)
ser2 = sp.series(sp.sqrt(x) * sp.besselj(R(-1, 3), R(2, 3) * x**R(3, 2)), x, 0, 5).removeO()
c0 = sp.simplify(ser2.coeff(x, 0))
check("sf-01b √x J_{-1/3} ∝ 1 - x^3/6", c0 != 0 and sp.simplify(ser2.coeff(x, 3) / c0 + R(1, 6)) == 0)


# am6-sf-01c：小根遞迴成敗
def small_root(m, N=8):
    """回傳 True=成功（存在一組 a_n），False=失敗。"""
    a = {0: sp.Integer(1)}
    c1 = 1 - 2 * m
    a[1] = sp.Integer(0) if c1 != 0 else sp.Integer(0)  # c1=0 時 a1 自由，取 0
    for n in range(2, N):
        coef = n * (n - 2 * m)
        rhs = -a[n - 2]
        if coef == 0:
            if rhs != 0:
                return False
            a[n] = sp.Integer(0)
        else:
            a[n] = rhs / coef
    return True


check("sf-01c m=1/3 成功", small_root(R(1, 3)))
check("sf-01c m=1/2 成功", small_root(R(1, 2)))
check("sf-01c m=3/2 成功", small_root(R(3, 2)))
check("sf-01c m=5/2 成功", small_root(R(5, 2)))
check("sf-01c m=1 失敗", not small_root(1))
check("sf-01c m=2 失敗", not small_root(2))
check("sf-01c m=3 失敗", not small_root(3))

# ---------------- 第 2 節 ----------------
for m in (1, 2, 3):
    check(f"ex-2 J_(-{m}) = (-1)^{m} J_{m}", all(close(J(-m, v), (-1)**m * J(m, v), 1e-20) for v in (0.7, 2.5, 6.1)))
Jm1 = sum((-1)**n / (sp.factorial(n - 1) * sp.factorial(n)) * (x / 2)**(2 * n - 1) for n in range(1, 4))
check("ex-2 J_-1 = -x/2 + x^3/16 - ...", sp.expand(Jm1 + Jser(1, 3)) == 0)

# am6-ex-3：m=0 降階法
J0s = Jser(0, 6)
inv = sp.series(1 / (x * J0s**2), x, 0, 5).removeO()
check("ex-3 1/(xJ0^2) = 1/x + x/2 + 5x^3/32", sp.expand(inv - (1 / x + x / 2 + 5 * x**3 / 32)) == 0)
y2 = J0s * sp.log(x) + x**2 / 4 - 3 * x**4 / 128 + 11 * x**6 / 13824
res = sp.expand(bessel_L(y2, 0))
res_nolog = sp.expand(res.subs(sp.log(x), 0))
check("ex-3 J0 ln x + x^2/4 - 3x^4/128 + ... 殘差從 x^8 開始", all(res_nolog.coeff(x, k) == 0 for k in range(0, 8)) and sp.expand(res.coeff(sp.log(x))).subs(x, 0) == 0)
v = x**2 / 4 - 3 * x**4 / 128
Lv = sp.expand(bessel_L(v, 0))
check("ex-3 驗算 L[v] = x^2 - x^4/8 (到 x^4)", Lv.coeff(x, 2) == 1 and Lv.coeff(x, 4) == R(-1, 8))
# Y0 = 2/π [ y2 + (γ - ln 2) J0 ]
xv = 1.3
y2num = J(0, xv) * mp.log(xv) + mp.mpf(xv)**2 / 4 - 3 * mp.mpf(xv)**4 / 128 + 11 * mp.mpf(xv)**6 / 13824 - 25 * mp.mpf(xv)**8 / 1769472
check("ex-3 Y0 = 2/π[y2 + (γ_E - ln2)J0]", close(2 / mp.pi * (y2num + (mp.euler - mp.log(2)) * J(0, xv)), Yb(0, xv), 1e-5))  # 級數截斷到 x^8

# am6-k114-2 / sf-02a：J_{±1/2}
for f in (sp.sin(x) / sp.sqrt(x), sp.cos(x) / sp.sqrt(x)):
    yy = sp.Function("y")
    ode = sp.Eq(x**2 * yy(x).diff(x, 2) + x * yy(x).diff(x) + (x**2 - R(1, 4)) * yy(x), 0)
    check(f"k114-2 checkodesol {f}", sp.checkodesol(ode, sp.Eq(yy(x), f))[0])
s1 = sp.series(sp.sin(x) / x, x, 0, 6).removeO()
s2 = sp.series(sp.cos(x), x, 0, 6).removeO()
check("k114-2 a2=-1/6, a4=1/120", s1.coeff(x, 2) == R(-1, 6) and s1.coeff(x, 4) == R(1, 120))
check("k114-2 a2=-1/2, a4=1/24", s2.coeff(x, 2) == R(-1, 2) and s2.coeff(x, 4) == R(1, 24))
for nv, f in ((0.5, lambda z: mp.sqrt(2 / (mp.pi * z)) * mp.sin(z)), (-0.5, lambda z: mp.sqrt(2 / (mp.pi * z)) * mp.cos(z))):
    check(f"sf-02a J_{nv} 封閉形式", all(close(J(nv, z), f(z), 1e-20) for z in (0.4, 1, 3.3, 9)))
nn = sp.symbols("nn", integer=True, nonnegative=True)
check("sf-02a n!Γ(n+3/2) = √π(2n+1)!/2^(2n+1), n=0..6", all(sp.simplify(sp.factorial(k) * sp.gamma(k + R(3, 2)) - sp.sqrt(sp.pi) * sp.factorial(2 * k + 1) / 2**(2 * k + 1)) == 0 for k in range(7)))
check("sf-02a n!Γ(n+1/2) = √π(2n)!/4^n, n=0..6", all(sp.simplify(sp.factorial(k) * sp.gamma(k + R(1, 2)) - sp.sqrt(sp.pi) * sp.factorial(2 * k) / 4**k) == 0 for k in range(7)))
check("sf-02a J_{1/2}(1) = 0.6714", close(J(0.5, 1), 0.6714, 1e-4))
check("sf-02a J_{1/2}^2 + J_{-1/2}^2 = 2/(πx)", all(close(J(0.5, z)**2 + J(-0.5, z)**2, 2 / (mp.pi * z), 1e-20) for z in (0.5, 2, 7)))


# am6-sf-02b：Wronskian
def W(m, z):
    return J(m, z) * mp.diff(lambda s: J(-m, s), z) - mp.diff(lambda s: J(m, s), z) * J(-m, z)


for m in (mp.mpf(1) / 3, mp.mpf(1) / 2, mp.mpf("0.7")):
    check(f"sf-02b W(J_m,J_-m) = -2 sin(mπ)/(πx), m={float(m):.3f}", all(close(W(m, z), -2 * mp.sin(m * mp.pi) / (mp.pi * z), 1e-12) for z in (0.5, 2, 7)))
check("sf-02b m=1 時 W=0", all(abs(W(1, z)) < 1e-15 for z in (0.5, 2)))

# am6-sf-02c
check("sf-02c m=1/2：1/(x y1^2) = csc^2 x", sp.simplify(1 / (x * (sp.sin(x) / sp.sqrt(x))**2) - 1 / sp.sin(x)**2) == 0)
check("sf-02c m=1/2：y2 = -cos x/√x", sp.simplify(sp.sin(x) / sp.sqrt(x) * (-sp.cot(x)) + sp.cos(x) / sp.sqrt(x)) == 0)
J1s = Jser(1, 6)
inv1 = sp.series(1 / (x * J1s**2), x, 0, 2).removeO()
check("sf-02c 1/(xJ1^2) = 4/x^3 + 1/x + 7x/48", sp.expand(inv1 - (4 / x**3 + 1 / x + 7 * x / 48)) == 0)
y2m1 = J1s * sp.log(x) - 1 / x + x / 8 + x**3 / 32
r1 = sp.expand(bessel_L(y2m1, 1))
r1n = sp.expand(r1.subs(sp.log(x), 0))
check("sf-02c m=1：J1 ln x - 1/x + x/8 + x^3/32 殘差從 x^5 開始", all(r1n.coeff(x, k) == 0 for k in range(-1, 5)) and all(sp.expand(r1.coeff(sp.log(x))).coeff(x, k) == 0 for k in range(0, 12)))
check("sf-02c J1^2 x^4 係數 5/192", sp.expand(sp.series((J1s / (x / 2))**2, x, 0, 5).removeO()).coeff(x, 4) == R(5, 192))

# ---------------- 第 3 節 ----------------
board = {(0, 1): 2.4, (0, 2): 5.5, (0, 3): 8.7, (1, 1): 3.8, (1, 2): 7.0, (1, 3): 10.2}
for (m, n), b in board.items():
    check(f"板書零點表 J_{m} 第 {n} 個 ≈ {b}", abs(float(mp.besseljzero(m, n)) - b) <= 0.051)
boardY = {(0, 1): 0.9, (0, 2): 4.0, (0, 3): 7.1, (1, 1): 2.2, (1, 2): 5.4, (1, 3): 8.6}
for (m, n), b in boardY.items():
    check(f"板書零點表 Y_{m} 第 {n} 個 ≈ {b}", abs(float(mp.besselyzero(m, n)) - b) <= 0.051)
site = {(0, 1): 2.4048, (0, 2): 5.5201, (0, 3): 8.6537, (1, 1): 3.8317, (1, 2): 7.0156, (1, 3): 10.1735, (2, 1): 5.1356, (2, 2): 8.4172, (2, 3): 11.6198}
check("3.2 節精確值表 J", all(abs(float(mp.besseljzero(m, n)) - v) < 6e-5 for (m, n), v in site.items()))
siteY = {(0, 1): 0.8936, (0, 2): 3.9577, (0, 3): 7.0861, (1, 1): 2.1971, (1, 2): 5.4297, (1, 3): 8.5960}
check("3.2 節精確值表 Y", all(abs(float(mp.besselyzero(m, n)) - v) < 6e-5 for (m, n), v in siteY.items()))

# am6-k113-3
lv = [mp.besseljzero(0, k) / 3 for k in (1, 2, 3)]
check("k113-3 λ = 0.8016, 1.8400, 2.8846", all(close(a, b, 1e-4) for a, b in zip(lv, (0.8016, 1.8400, 2.8846))))
check("k113-3 J0(3λ1)=0", abs(J(0, 3 * lv[0])) < 1e-25)
y = sp.besselj(0, lam * x)
check("k113-3 J0(λx) 代入方程", all(abs(complex((x**2 * sp.diff(y, x, 2) + x * sp.diff(y, x) + lam**2 * x**2 * y).subs({lam: 0.8016, x: v}).evalf())) < 1e-12 for v in (0.5, 2)))
check("k113-3 板書值 2.4/3, 5.5/3, 8.7/3 = 0.80, 1.83, 2.90", abs(2.4 / 3 - 0.80) < 1e-9 and abs(5.5 / 3 - 1.83) < 0.005 and abs(8.7 / 3 - 2.90) < 1e-9)

# am6-k113b-2
cands = sorted(float(mp.besseljzero(p, n))**2 + (nz * float(mp.pi) / 2)**2 for p in range(3) for n in (1, 2, 3) for nz in (1, 2, 3))
check("k113b-2 最小 j^2+(nπ/2)^2 = 8.2506", abs(cands[0] - 8.2506) < 1e-4)
check("k113b-2 j01^2=5.783, π^2/4=2.467", abs(float(j01)**2 - 5.783) < 1e-3 and abs(float(mp.pi)**2 / 4 - 2.467) < 1e-3)
check("k113b-2 次低候選 15.65 (n_z=2) 與 17.15 (p=1)", abs(float(j01)**2 + float(mp.pi)**2 - 15.65) < 0.01 and abs(float(mp.besseljzero(1, 1))**2 + float(mp.pi)**2 / 4 - 17.15) < 0.01)

# am6-sf-03a
z = [mp.besseljzero(0, 1), mp.besseljzero(1, 1), mp.besseljzero(2, 1), mp.besseljzero(0, 2)]
check("sf-03a 排序 j01<j11<j21<j02", z[0] < z[1] < z[2] < z[3])
check("sf-03a 比例 1.593, 2.136, 2.295", all(close(z[k] / z[0], v, 3e-4) for k, v in ((1, 1.593), (2, 2.136), (3, 2.295))))
check("sf-03a 節線圓 0.4357R", close(z[0] / z[3], 0.4357, 1e-4))
check("sf-03a 159.3 Hz", close(100 * z[1] / z[0], 159.3, 1e-3))
check("圖解 am6-drum (0,3) 節線 0.278R、0.638R，頻率比 3.598", close(j01 / j03, 0.278, 2e-3) and close(j02 / j03, 0.638, 1e-3) and close(j03 / j01, 3.598, 1e-3))

# am6-sf-03b
orth = mp.quad(lambda s: s * J(0, j01 * s) * J(0, j02 * s), [0, 1])
norm = mp.quad(lambda s: s * J(0, j01 * s)**2, [0, 1])
check("sf-03b 正交 ∫xJ0(j01x)J0(j02x)=0", abs(orth) < 1e-20)
check("sf-03b 歸一化 = J1(j01)^2/2 = 0.1348", close(norm, J(1, j01)**2 / 2, 1e-20) and close(norm, 0.1348, 3e-4))
check("sf-03b J1(j01)=0.5191", close(J(1, j01), 0.5191, 1e-4))

# am6-sf-03c
check("sf-03c J0' = -J1（級數）", sp.expand(sp.diff(Jser(0, 9), x) + Jser(1, 8)) == 0)
check("sf-03c (xJ1)' = xJ0（級數）", sp.expand(sp.diff(x * Jser(1, 8), x) - x * Jser(0, 8)) == 0)
zz0 = [mp.besseljzero(0, k) for k in (1, 2, 3)]
zz1 = [mp.besseljzero(1, k) for k in (1, 2, 3)]
check("sf-03c 交錯 j01<j11<j02<j12<j03<j13", zz0[0] < zz1[0] < zz0[1] < zz1[1] < zz0[2] < zz1[2])
as0 = [(n - 0.25) * mp.pi for n in (1, 2, 3)]
as1 = [(n + 0.25) * mp.pi for n in (1, 2, 3)]
check("sf-03c 漸近 2.356 5.498 8.639 / 3.927 7.069 10.210", all(close(a, b, 1e-3) for a, b in zip(as0 + as1, (2.356, 5.498, 8.639, 3.927, 7.069, 10.210))))
check("sf-03c 誤差 -0.049 -0.022 -0.014 / +0.095 +0.053 +0.037", all(abs(float(a - b) - e) < 1.5e-3 for a, b, e in zip(as0 + as1, zz0 + zz1, (-0.049, -0.022, -0.014, 0.095, 0.053, 0.037))))

# ---------------- 第 4 節 ----------------
# 五條遞迴（含非整數 m）
for m in (2, 3, mp.mpf(1) / 3):
    ok = True
    for z0 in (0.8, 3.1):
        d1 = mp.diff(lambda s: s**m * J(m, s), z0) - z0**m * J(m - 1, z0)
        d3 = mp.diff(lambda s: s**(-m) * J(m, s), z0) + z0**(-m) * J(m + 1, z0)
        dJ = mp.diff(lambda s: J(m, s), z0)
        d2a = dJ - (J(m - 1, z0) - m / z0 * J(m, z0))
        d2b = dJ - (m / z0 * J(m, z0) - J(m + 1, z0))
        d4 = J(m, z0) - z0 * (J(m - 1, z0) + J(m + 1, z0)) / (2 * m)
        d5 = dJ - (J(m - 1, z0) - J(m + 1, z0)) / 2
        ok = ok and all(abs(q) < 1e-12 for q in (d1, d3, d2a, d2b, d4, d5))
    check(f"遞迴關係 1–5 (m={float(m):.3f})", ok)

# am6-ex-4
exact = mp.quad(lambda s: s**-3 * J(4, s), [1, 2])
check("ex-4 數值積分 = J3(1) - J3(2)/8 = 0.0034454", close(exact, J(3, 1) - J(3, 2) / 8, 1e-20) and close(exact, 0.0034454, 1e-4))
check("ex-4 板書數值 0.0196 - 0.1289/8 = 0.0034875", abs(0.0196 - 0.1289 / 8 - 0.0034875) < 1e-12)
check("ex-4 表值 J3(1)=0.0196, J3(2)=0.1289", close(J(3, 1), 0.0196, 3e-3) and close(J(3, 2), 0.1289, 1e-3))

# am6-k111-4
I111 = mp.quad(lambda r: (r - r**3) * J(0, 2 * r), [0, 1])
check("k111-4 = J2(2)/2 = (J1(2)-J0(2))/2 = 0.17642", close(I111, J(2, 2) / 2, 1e-20) and close(I111, (J(1, 2) - J(0, 2)) / 2, 1e-20) and close(I111, 0.176417, 1e-5))
check("k111-4 ∫x^3 J0 = x^3 J1 - 2x^2 J2（微分驗證）", all(abs(mp.diff(lambda s: s**3 * J(1, s) - 2 * s**2 * J(2, s), z0) - z0**3 * J(0, z0)) < 1e-15 for z0 in (0.7, 2.3)))
check("k111-4 表值 J0(2)=0.2239, J1(2)=0.5767, J2(2)=0.3528", close(J(0, 2), 0.2239, 2e-4) and close(J(1, 2), 0.5767, 1e-4) and close(J(2, 2), 0.3528, 1e-4))

# am6-sf-04a
check("sf-04a J_{3/2} 封閉形式", all(close(J(1.5, z0), mp.sqrt(2 / (mp.pi * z0)) * (mp.sin(z0) / z0 - mp.cos(z0)), 1e-20) for z0 in (0.3, 2, 8)))

# am6-sf-04b
check("sf-04b (J0 - 4J1/x)' = J3", all(abs(mp.diff(lambda s: J(0, s) - 4 * J(1, s) / s, z0) - J(3, z0)) < 1e-15 for z0 in (0.9, 4)))
check("sf-04b (-J0 - 2J2)' = J3", all(abs(mp.diff(lambda s: -J(0, s) - 2 * J(2, s), z0) - J(3, z0)) < 1e-15 for z0 in (0.9, 4)))
check("sf-04b (x^4J2 - 2x^3J3)' = x^4 J1", all(abs(mp.diff(lambda s: s**4 * J(2, s) - 2 * s**3 * J(3, s), z0) - z0**4 * J(1, z0)) < 1e-13 for z0 in (0.9, 4)))
check("sf-04b ∫J2 = ∫J0 - 2J1", abs(mp.quad(lambda s: J(2, s), [0, 3]) - (mp.quad(lambda s: J(0, s), [0, 3]) - 2 * J(1, 3))) < 1e-20)
I1 = mp.quad(lambda s: s**4 * J(1, s), [0, 2])
I2 = mp.quad(lambda s: J(3, s), [0, 2])
check("sf-04b ∫0^2 x^4 J1 = 16 J0(2) = 3.582", close(I1, 16 * J(0, 2), 1e-20) and close(I1, 3.582, 2e-4))
check("sf-04b ∫0^2 J3 = 0.0704（表值算 0.0705）", close(I2, 0.07044, 1e-3) and abs((-0.2239 - 2 * 0.3528 + 1) - 0.0705) < 1e-9)

# am6-sf-04c
for k, cexp in ((1, 1.108), (2, -0.1398), (3, 0.0455)):
    jk = mp.besseljzero(0, k)
    num = 2 / J(1, jk)**2 * mp.quad(lambda s: s * (1 - s**2) * J(0, jk * s), [0, 1])
    check(f"sf-04c c_{k} = 8/(j^3 J1(j)) = {cexp}", close(num, 8 / (jk**3 * J(1, jk)), 1e-15) and abs(float(num) - cexp) < 6e-4)
check("sf-04c J1(j02)=-0.3403, J1(j03)=0.2715", close(J(1, j02), -0.3403, 1e-4) and close(J(1, j03), 0.2715, 2e-4))
c = [8 / (mp.besseljzero(0, k)**3 * J(1, mp.besseljzero(0, k))) for k in (1, 2, 3)]
tau = mp.log(2 * c[0]) / j01**2
check("sf-04c τ = 0.1376", close(tau, 0.1376, 1e-3))
check("sf-04c 第二項 -0.0021", close(c[1] * mp.e**(-j02**2 * tau), -0.0021, 3e-2))
check("sf-04c 三項和 0.4979；前三項 c 和 1.014", close(sum(c[k] * mp.e**(-mp.besseljzero(0, k + 1)**2 * tau) for k in range(3)), 0.4979, 1e-4) and close(sum(c), 1.0137, 1e-4))

# am6-sf-04d
for n in (0, 1, 3):
    for z0 in (2.4048, 5):
        rep = mp.quad(lambda th: mp.cos(n * th - z0 * mp.sin(th)), [0, mp.pi]) / mp.pi
        check(f"sf-04d 積分表示 n={n}, x={z0}", close(rep, J(n, z0), 1e-15) or abs(rep - J(n, z0)) < 1e-15)
tt = sp.symbols("tt")
g = sp.series(sp.exp(x / 2 * tt) , x, 0, 9).removeO() * sp.series(sp.exp(-x / (2 * tt)), x, 0, 9).removeO()
g = sp.expand(g)
okg = True
for n in range(0, 4):
    coef = sp.expand(g.coeff(tt, n))
    target = sp.expand(sp.series(Jser(n, 6), x, 0, 9).removeO())
    okg = okg and all(sp.expand(coef).coeff(x, k) == target.coeff(x, k) for k in range(0, 9))
check("sf-04d 生成函數 t^n 係數 = J_n（到 x^8, n=0..3）", okg)

# 審查 E 修正後新增的檢查
fann = lambda k: J(0, k / 2) * Yb(0, k) - J(0, k) * Yb(0, k / 2)
kann = mp.findroot(fann, 6.2)
check("sf-03a(e) 圓環最低 kR = 6.246、f(6.2)>0>f(6.3)", close(kann, 6.246, 1e-4) and fann(6.2) > 0 > fann(6.3) and close(fann(6.2), 0.0033, 2e-2) and close(fann(6.3), -0.0038, 2e-2))
check("sf-03a(e) 線性內插 6.2+0.1*33/71 = 6.246；2π 差 0.6%；2.60 倍", abs(6.2 + 0.1 * 0.0033 / 0.0071 - 6.246) < 1e-3 and abs(2 * float(mp.pi) / float(kann) - 1 - 0.006) < 1e-3 and close(kann / j01, 2.597, 1e-3))
check("sf-03a(e) 沒有比 6.246 更小的根（掃描 0.5–6.2）", all(fann(k0) > 0 for k0 in [0.5 + 0.05 * i for i in range(115)]))
yl = sp.besselj(R(1, 2), lam * x)
check("sf-02a(e) J_{1/2}(λx) 滿足 x^2y''+xy'+(λ^2x^2-1/4)y=0（數值）", all(abs(complex((x**2 * sp.diff(yl, x, 2) + x * sp.diff(yl, x) + (lam**2 * x**2 - R(1, 4)) * yl).subs({lam: 3 * sp.pi, x: v}).evalf())) < 1e-12 for v in (0.2, 0.7)))
check("sf-02a(e) λ=nπ 時 sin(nπx)/√x 在 x=1 為 0、x→0 趨近 0", all(sp.sin(n * sp.pi) == 0 for n in (1, 2, 3)) and sp.limit(sp.sin(sp.pi * x) / sp.sqrt(x), x, 0) == 0)
check("4.3 ∫x^2 J0 = x^2 J1 + x J0 - ∫J0", abs(mp.quad(lambda s: s**2 * J(0, s), [0, 3]) - (9 * J(1, 3) + 3 * J(0, 3) - mp.quad(lambda s: J(0, s), [0, 3]))) < 1e-20)
check("5.1 Y0 ≈ (2/π)(ln(x/2)+γ_E) 在 x=0.01 相對誤差 < 1e-3", close(2 / mp.pi * (mp.log(0.005) + mp.euler), Yb(0, 0.01), 1e-3))
check("sf-03c J1 第 3 個漸近 10.21 ≈ 板書 10.2；J0 第 3 個 8.639 與板書 8.7 不一致", round(float(as1[2]), 1) == 10.2 and round(float(as0[2]), 1) == 8.6 and abs(float(zz0[2] - as0[2]) - 0.0143) < 2e-4)

# ---------------- 第 5 節 變化題 ----------------
yv = sp.Function("y")
ode = sp.Eq(x**2 * yv(x).diff(x, 2) + x * yv(x).diff(x) + (4 * x**4 - 1) * yv(x), 0)
check("var-1 sin(x^2)/x", sp.checkodesol(ode, sp.Eq(yv(x), sp.sin(x**2) / x))[0])
check("var-1 cos(x^2)/x", sp.checkodesol(ode, sp.Eq(yv(x), sp.cos(x**2) / x))[0])
check("var-2 ∫0^a x^3 J0 = a(a^2-4)J1(a) = 2.226", close(mp.quad(lambda s: s**3 * J(0, s), [0, j01]), j01 * (j01**2 - 4) * J(1, j01), 1e-20) and close(j01 * (j01**2 - 4) * J(1, j01), 2.226, 2e-4))
I3 = mp.quad(lambda s: J(4, s) / s, [1, 2])
check("var-3 ∫1^2 J4/x = [-J3/x - 2J2/x^2] = 0.00848", close(I3, (-J(3, 2) / 2 - 2 * J(2, 2) / 4) - (-J(3, 1) - 2 * J(2, 1)), 1e-20) and close(I3, 0.00848, 1e-3))
check("var-3 表值算 0.0086", abs((-0.1289 / 2 - 2 * 0.3528 / 4) - (-0.0196 - 2 * 0.1149) - 0.00855) < 1e-9)
check("var-3 J2(1)=0.1149", close(J(2, 1), 0.1149, 1e-3))
check("var-4 λ = j1n/2 = 1.916, 3.508, 5.087", all(close(mp.besseljzero(1, k) / 2, v, 2e-4) for k, v in ((1, 1.916), (2, 3.508), (3, 5.087))))
check("var-4 J1'(0) = 1/2", close(mp.diff(lambda s: J(1, s), 0), 0.5, 1e-12))
allz = sorted([(float(mp.besseljzero(p, n)), p, n) for p in range(4) for n in (1, 2, 3)])
check("var-5 第三小 = j21 = 5.136", allz[2][1] == 2 and allz[2][2] == 1 and abs(allz[2][0] - 5.136) < 1e-3)
for k, v in ((1, 1.602), (2, -1.065), (3, 0.851)):
    jk = mp.besseljzero(0, k)
    check(f"var-6 c_{k} = 2/(jJ1(j)) = {v}", close(2 / J(1, jk)**2 * mp.quad(lambda s: s * J(0, jk * s), [0, 1]), 2 / (jk * J(1, jk)), 1e-15) and abs(float(2 / (jk * J(1, jk))) - v) < 6e-4)

# 圖解 JS 的 Y0／Y1 級數（與 figures.js 同一公式）
import math
EG = 0.5772156649015329


def jsJ(n, z):
    tt_, s = (z / 2)**n / math.factorial(n), 0.0
    for k in range(60):
        s += tt_
        tt_ *= -(z * z / 4) / ((k + 1) * (k + 1 + n))
    return s


def jsY0(z):
    tt_, H, s = 1.0, 0.0, 0.0
    for k in range(1, 60):
        tt_ *= -(z * z / 4) / (k * k)
        H += 1 / k
        s -= tt_ * H
    return 2 / math.pi * ((math.log(z / 2) + EG) * jsJ(0, z) + s)


def jsY1(z):
    tt_, Hk, s = z / 2, 0.0, 0.0
    for k in range(60):
        if k > 0:
            tt_ *= -(z * z / 4) / (k * (k + 1))
            Hk += 1 / k
        s += (2 * (Hk - EG) + 1 / (k + 1)) * tt_
    return 2 / math.pi * jsJ(1, z) * math.log(z / 2) - 2 / (math.pi * z) - s / math.pi


err = max(max(abs(jsJ(0, q) - float(J(0, q))), abs(jsJ(1, q) - float(J(1, q))), abs(jsY0(q) - float(Yb(0, q))), abs(jsY1(q) - float(Yb(1, q)))) for q in [12 * i / 240 for i in range(1, 241)])
check(f"figures.js 的 J0,J1,Y0,Y1 級數誤差 {err:.1e} < 1e-10", err < 1e-10)

print(f"\n{COUNT[0]} checks, {len(FAILS)} failed")
if FAILS:
    print("FAILED:", FAILS)
    sys.exit(1)
print("ALL CHECKS PASSED")
