"""應用數學第 6 章考試書寫版（exam.html 的「背公式＋計算」改寫）：驗算書寫版裡出現的所有數值與中間值。

做法：級數展開用 sympy 重算；Bessel 函數值、零點、積分用 mpmath（sympy 內附）獨立計算，
再和書寫版的數字（依書寫版寫出的位數）逐一比對。
用法：python tools/verify_writeup_applied-math_ch06.py   全部通過時印出 ALL CHECKS PASSED。
"""
import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
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


def near(a, b, tol):
    return abs(float(a) - float(b)) <= tol


def D(y, n=1):
    return sp.diff(y, x, n)


J = lambda m, z: mp.besselj(m, z)
Y = lambda m, z: mp.bessely(m, z)
j0 = [mp.besseljzero(0, k) for k in (1, 2, 3)]
j1 = [mp.besseljzero(1, k) for k in (1, 2, 3)]
j21 = mp.besseljzero(2, 1)


def Jser(m, K):
    return sum(R((-1) ** k, sp.factorial(k) * sp.factorial(m + k)) * (x / 2) ** (2 * k + m) for k in range(K + 1))


# ---------------- am6-ex-1
check("ex-1 J0 前三項 1,-x^2/4,x^4/64", sp.expand(Jser(0, 2)) == 1 - x**2 / 4 + x**4 / 64)
check("ex-1 J1 前三項 x/2,-x^3/16,x^5/384", sp.expand(Jser(1, 2)) == x / 2 - x**3 / 16 + x**5 / 384)
m, k = sp.symbols("m k", positive=True, integer=True)
a = lambda kk: R((-1) ** kk) * sp.factorial(m) / (4**kk * sp.factorial(kk) * sp.factorial(m + kk))
check("ex-1 a2=-a0/(4(m+1))", sp.simplify(sp.combsimp(a(1) + 1 / (4 * (m + 1)))) == 0)
check("ex-1 a_{2k} 遞迴 -a_{2k-2}/(4k(k+m))", all(sp.simplify(sp.combsimp(a(kk) + a(kk - 1) / (4 * kk * (kk + m)))) == 0 for kk in (1, 2, 3)))
for mm in (0, 1, 2, 3):
    s = sp.expand(x**2 * D(Jser(mm, 6), 2) + x * D(Jser(mm, 6)) + (x**2 - mm**2) * Jser(mm, 6))
    check(f"ex-1 J_{mm} 級數代回殘差低階為 0", all(s.coeff(x, p) == 0 for p in range(0, 12 + mm)))

# ---------------- am6-sf-01a
check("sf-01a j01,j02,j03≈2.405,5.520,8.654", near(j0[0], 2.405, 5e-4) and near(j0[1], 5.520, 5e-4) and near(j0[2], 8.654, 5e-4))
check("sf-01a j01/j02=0.43565", near(j0[0] / j0[1], 0.43565, 5e-6))
check("sf-01a ln(j01/j02)=-0.831", near(mp.log(j0[0] / j0[1]), -0.831, 5e-4))
t, lam = sp.symbols("t lam", positive=True)
yy = sp.besselj(0, lam * sp.exp(x))
check("sf-01a J0(λe^x) 滿足 y''+λ²e^{2x}y=0（數值）", all(abs(complex(sp.N((D(yy, 2) + lam**2 * sp.exp(2 * x) * yy).subs({lam: 2.4048, x: xv}))) ) < 1e-10 for xv in (-1.3, -0.4)))

# ---------------- am6-sf-01b
w = sp.Function("w")
yb = sp.sqrt(x) * w(x)
expr = sp.expand((D(yb, 2) + x * yb) * x**sp.Rational(3, 2))
target = x**2 * sp.diff(w(x), x, 2) + x * sp.diff(w(x), x) + (x**3 - R(1, 4)) * w(x)
check("sf-01b 乘 x^{3/2} 後得 x²w''+xw'+(x³-1/4)w", sp.simplify(expr - target) == 0)
check("sf-01b x^3=(9/4)t^2", sp.simplify(x**3 - R(9, 4) * (R(2, 3) * x**R(3, 2)) ** 2) == 0)
for nu in (R(1, 3), R(-1, 3)):
    f = lambda xv, nu=nu: mp.sqrt(xv) * J(nu, mp.mpf(2) / 3 * xv**1.5)
    ok = all(abs(mp.diff(f, xv, 2) + xv * f(xv)) < 1e-12 for xv in (mp.mpf("0.7"), mp.mpf("2.3")))
    check(f"sf-01b √x J_{nu}(2/3 x^1.5) 滿足 y''+xy=0", ok)
check("sf-01b a3=-a0/6, a4=-a1/12", R(-1, 3 * 2) == R(-1, 6) and R(-1, 4 * 3) == R(-1, 12))

# ---------------- am6-sf-01c / ex-2
check("sf-01c m=1/2 問題格係數 (1-2m)=0", 1 - 2 * R(1, 2) == 0)
check("sf-01c m=3/2：(1-3)a1=0、3(3-3)=0", 1 - 3 == -2 and 3 * (3 - 3) == 0)
check("sf-01c n=2k 時 n(n-2m)=4k(k-m)", sp.expand((2 * k) * (2 * k - 2 * m) - 4 * k * (k - m)) == 0)
check("ex-2 J_{-1}=-J_1（數值）", all(abs(J(-1, z) + J(1, z)) < 1e-25 for z in (0.5, 3.3)))
check("ex-2 J_{-2}=J_2、J_{-3}=-J_3", abs(J(-2, 1.7) - J(2, 1.7)) < 1e-25 and abs(J(-3, 1.7) + J(3, 1.7)) < 1e-25)
check("ex-2 J_{-1} 前兩項 -x/2+x^3/16", R(-1, 1) / 2 == R(-1, 2) and R(1, 2) * R(1, 8) == R(1, 16))

# ---------------- am6-ex-3
J0s = 1 - x**2 / 4 + x**4 / 64
sq = sp.expand(sp.series(J0s**2, x, 0, 5).removeO())
check("ex-3 J0^2=1-x^2/2+3x^4/32", sq == 1 - x**2 / 2 + R(3, 32) * x**4)
check("ex-3 1/16+2/64=3/32", R(1, 16) + R(2, 64) == R(3, 32))
inv = sp.expand(sp.series(1 / J0s**2, x, 0, 5).removeO())
check("ex-3 1/J0^2=1+x^2/2+5x^4/32", inv == 1 + x**2 / 2 + R(5, 32) * x**4)
check("ex-3 -3/32+1/4=5/32", R(-3, 32) + R(1, 4) == R(5, 32))
u = sp.log(x) + x**2 / 4 + R(5, 128) * x**4
check("ex-3 u 逐項積分", sp.simplify(D(u) - sp.expand(inv / x)) == 0)
nonlog = sp.expand(sp.series((u - sp.log(x)) * J0s, x, 0, 5).removeO())
check("ex-3 y2 非對數 x^2/4-3x^4/128", nonlog == x**2 / 4 - R(3, 128) * x**4)
check("ex-3 5/128-1/16=-3/128", R(5, 128) - R(1, 16) == R(-3, 128))
J0b = Jser(0, 4)
y2 = J0b * sp.log(x) + x**2 / 4 - R(3, 128) * x**4
res = sp.expand(x**2 * D(y2, 2) + x * D(y2) + x**2 * y2)
res = sp.expand(res - sp.log(x) * sp.expand(x**2 * D(J0b, 2) + x * D(J0b) + x**2 * J0b))
check("ex-3 y2 代回殘差到 x^4 為 0", all(res.coeff(x, p) == 0 for p in range(0, 5)))
check("ex-3 γ_E≈0.5772", near(mp.euler, 0.5772, 5e-5))

# ---------------- am6-k114-2
L = lambda y: x**2 * D(y, 2) + x * D(y) + (x**2 - R(1, 4)) * y
check("k114-2 sin x/√x、cos x/√x 是解", sp.simplify(L(sp.sin(x) / sp.sqrt(x))) == 0 and sp.simplify(L(sp.cos(x) / sp.sqrt(x))) == 0)
check("k114-2 係數 -1/6,1/120,-1/2,1/24", R(-1, 3 * 2) == R(-1, 6) and R(1, 6 * 20) == R(1, 120) and R(-1, 2) * R(-1, 12) == R(1, 24))
check("k114-2 √(π/2) J_{1/2}=sin x/√x", abs(mp.sqrt(mp.pi / 2) * J(0.5, 1.3) - mp.sin(1.3) / mp.sqrt(1.3)) < 1e-25)

# ---------------- am6-sf-02a
n = sp.symbols("n", integer=True, nonnegative=True)
check("sf-02a n!Γ(n+3/2)=√π(2n+1)!/2^{2n+1}（n=0..6）", all(sp.simplify(sp.factorial(nn) * sp.gamma(nn + R(3, 2)) - sp.sqrt(sp.pi) * sp.factorial(2 * nn + 1) / 2 ** (2 * nn + 1)) == 0 for nn in range(7)))
check("sf-02a n!Γ(n+1/2)=√π(2n)!/2^{2n}（n=0..6）", all(sp.simplify(sp.factorial(nn) * sp.gamma(nn + R(1, 2)) - sp.sqrt(sp.pi) * sp.factorial(2 * nn) / 2 ** (2 * nn)) == 0 for nn in range(7)))
check("sf-02a Γ(n+3/2)=1·3…(2n+1)/2^{n+1}√π（n=0..5）", all(sp.simplify(sp.gamma(nn + R(3, 2)) - sp.prod([2 * i + 1 for i in range(nn + 1)]) / 2 ** (nn + 1) * sp.sqrt(sp.pi)) == 0 for nn in range(6)))
check("sf-02a J_{±1/2} 封閉形式（數值）", all(abs(J(0.5, z) - mp.sqrt(2 / (mp.pi * z)) * mp.sin(z)) < 1e-25 and abs(J(-0.5, z) - mp.sqrt(2 / (mp.pi * z)) * mp.cos(z)) < 1e-25 for z in (0.4, 2.0, 7.5)))
check("sf-02a 零點 nπ = 3.14, 6.28, 9.42", [round(float(kk * mp.pi), 2) for kk in (1, 2, 3)] == [3.14, 6.28, 9.42])
check("sf-02a 板書 J0 零點間距 3.1、3.2", round(5.5 - 2.4, 1) == 3.1 and round(8.7 - 5.5, 1) == 3.2)
check("sf-02a J_{1/2}^2+J_{-1/2}^2=2/(πx)", abs(J(0.5, 1.9) ** 2 + J(-0.5, 1.9) ** 2 - 2 / (mp.pi * 1.9)) < 1e-25)
Lam = lambda y, lv: x**2 * D(y, 2) + x * D(y) + (lv**2 * x**2 - R(1, 4)) * y
check("sf-02a λ=nπ：sin(nπx)/√x 滿足方程且 y(1)=0", all(sp.simplify(Lam(sp.sin(nn * sp.pi * x) / sp.sqrt(x), nn * sp.pi)) == 0 and sp.sin(nn * sp.pi) == 0 for nn in (1, 2, 3)))

# ---------------- am6-sf-02b
for mm in (R(1, 3), R(1, 2), R("0.7")):
    z = mp.mpf("1.6")
    W = J(mm, z) * mp.diff(lambda s: J(-mm, s), z) - mp.diff(lambda s: J(mm, s), z) * J(-mm, z)
    check(f"sf-02b W(J_m,J_-m)=-2sin(mπ)/(πx)，m={mm}", abs(W + 2 * mp.sin(mm * mp.pi) / (mp.pi * z)) < 1e-20)
check("sf-02b Γ(1+m)Γ(1-m)=mπ/sin mπ（m=1/3）", abs(mp.gamma(1 + mp.mpf(1) / 3) * mp.gamma(1 - mp.mpf(1) / 3) - (mp.pi / 3) / mp.sin(mp.pi / 3)) < 1e-25)
check("sf-02b m=1 時 W=0", abs(J(1, 1.6) * mp.diff(lambda s: J(-1, s), 1.6) - mp.diff(lambda s: J(1, s), 1.6) * J(-1, 1.6)) < 1e-20)

# ---------------- am6-sf-02c
check("sf-02c m=1/2：u=-cot x，y2=-cos x/√x", sp.simplify(D(-sp.cot(x)) - 1 / sp.sin(x) ** 2) == 0 and sp.simplify(sp.sin(x) / sp.sqrt(x) * (-sp.cot(x)) + sp.cos(x) / sp.sqrt(x)) == 0)
J1s = x / 2 - x**3 / 16 + x**5 / 384
sq = sp.expand(sp.series(J1s**2, x, 0, 7).removeO())
check("sf-02c J1^2=x^2/4(1-x^2/4+5x^4/192)", sq == sp.expand(x**2 / 4 * (1 - x**2 / 4 + R(5, 192) * x**4)))
check("sf-02c 1/64+2/192=5/192、1/16-5/192=7/192", R(1, 64) + R(2, 192) == R(5, 192) and R(1, 16) - R(5, 192) == R(7, 192))
integrand = sp.expand(sp.series(1 / (x * J1s**2), x, 0, 2).removeO())
check("sf-02c 1/(xJ1^2)=4/x^3+1/x+7x/48", sp.simplify(integrand - (4 / x**3 + 1 / x + R(7, 48) * x)) == 0)
u = -2 / x**2 + sp.log(x) + R(7, 96) * x**2
check("sf-02c u 逐項積分", sp.simplify(D(u) - integrand) == 0)
nonlog = sp.expand(sp.series((u - sp.log(x)) * J1s, x, 0, 4).removeO())
check("sf-02c y2 非對數 -1/x+x/8+x^3/32", sp.simplify(nonlog - (-1 / x + x / 8 + x**3 / 32)) == 0)
check("sf-02c -1/192+7/192=1/32", R(-1, 192) + R(7, 192) == R(1, 32))
J1b = Jser(1, 4)
y2 = J1b * sp.log(x) - 1 / x + x / 8 + x**3 / 32
L1 = lambda y: x**2 * D(y, 2) + x * D(y) + (x**2 - 1) * y
res = sp.expand(L1(y2) - sp.log(x) * sp.expand(L1(J1b)))
check("sf-02c y2 代回殘差到 x^4 為 0", all(sp.simplify(res.coeff(x, p)) == 0 for p in range(-1, 5)))

# ---------------- am6-k113-3
check("k113-3 λ=j0n/3≈0.802,1.840,2.885", [round(float(z / 3), 3) for z in j0] == [0.802, 1.840, 2.885])
check("k113-3 J0(λx) 是解（λ=0.8016）", all(abs(complex(sp.N((x**2 * D(sp.besselj(0, 0.80160 * x), 2) + x * D(sp.besselj(0, 0.80160 * x)) + 0.80160**2 * x**2 * sp.besselj(0, 0.80160 * x)).subs(x, xv)))) < 1e-10 for xv in (0.7, 2.2)))
check("k113-3 λ=0：c1+c2 ln x 是 Cauchy-Euler 解", sp.simplify(x**2 * D(sp.log(x), 2) + x * D(sp.log(x))) == 0)

# ---------------- am6-k113b-2
check("k113b-2 j01^2=5.783, π²/4=2.467", near(j0[0] ** 2, 5.783, 5e-4) and near(mp.pi**2 / 4, 2.467, 5e-4))
check("k113b-2 E0 係數 8.251", near(j0[0] ** 2 + mp.pi**2 / 4, 8.251, 5e-4))
check("k113b-2 j11=3.83, j21=5.14", near(j1[0], 3.83, 5e-3) and near(j21, 5.14, 5e-3))
check("k113b-2 候選 17.15、15.65", near(j1[0] ** 2 + mp.pi**2 / 4, 17.15, 5e-3) and near(j0[0] ** 2 + mp.pi**2, 15.65, 5e-3))
cands = sorted(float(mp.besseljzero(p, nr) ** 2 + (nz * mp.pi / 2) ** 2) for p in range(3) for nr in (1, 2) for nz in (1, 2, 3))
check("k113b-2 最小組合就是 8.251", near(cands[0], 8.251, 5e-4))

# ---------------- am6-sf-03a
check("sf-03a 零點 3.832, 5.136", near(j1[0], 3.832, 5e-4) and near(j21, 5.136, 5e-4))
check("sf-03a 比值 1.593, 2.136, 2.295", [round(float(z / j0[0]), 3) for z in (j1[0], j21, j0[1])] == [1.593, 2.136, 2.295])
check("sf-03a 節線圓 0.4357R", near(j0[0] / j0[1], 0.4357, 5e-5))
check("sf-03a f11=159.3 Hz", round(float(100 * j1[0] / j0[0]), 1) == 159.3)
f = lambda kap: J(0, kap / 2) * Y(0, kap) - J(0, kap) * Y(0, kap / 2)
check("sf-03a f(6.2)=+0.0033, f(6.3)=-0.0038", near(f(6.2), 0.0033, 5e-5) and near(f(6.3), -0.0038, 5e-5))
check("sf-03a 內插 6.246", round(6.2 + 0.1 * 0.0033 / (0.0033 + 0.0038), 3) == 6.246)
root = mp.findroot(f, 6.25)
check("sf-03a 真根≈6.246", near(root, 6.246, 1e-3))
check("sf-03a 2π=6.283，差 0.6%", round(float(2 * mp.pi), 3) == 6.283 and round((6.283 - 6.246) / 6.246 * 100, 1) == 0.6)
check("sf-03a 6.246/2.405=2.60", round(6.246 / 2.405, 2) == 2.60)

# ---------------- am6-sf-03b
J1a = J(1, j0[0])
check("sf-03b J1(j01)=0.51915", near(J1a, 0.51915, 5e-6))
check("sf-03b ½(0.51915)^2=0.1348", round(0.5 * 0.51915**2, 4) == 0.1348)
check("sf-03b 註：½(0.5191)^2 四捨五入是 0.1347", round(0.5 * 0.5191**2, 4) == 0.1347)
check("sf-03b 數值積分 ∫x J0(αx)^2 = ½J1(α)^2", abs(mp.quad(lambda s: s * J(0, j0[0] * s) ** 2, [0, 1]) - J1a**2 / 2) < 1e-20)
check("sf-03b 正交 ∫x J0(j01x)J0(j02x)=0", abs(mp.quad(lambda s: s * J(0, j0[0] * s) * J(0, j0[1] * s), [0, 1])) < 1e-20)

# ---------------- am6-sf-03c
check("sf-03c J0'=-J1（級數）", sp.expand(D(Jser(0, 6)) + Jser(1, 5)) == 0)
check("sf-03c (xJ1)'=xJ0（級數）", sp.expand(D(x * Jser(1, 6)) - x * Jser(0, 6)) == 0)
asym = lambda mm, nn: (nn + mm / 2 - 0.25) * mp.pi
check("sf-03c 漸近 J0：2.356,5.498,8.639", [round(float(asym(0, nn)), 3) for nn in (1, 2, 3)] == [2.356, 5.498, 8.639])
check("sf-03c 漸近 J1：3.927,7.069,10.210", [round(float(asym(1, nn)), 3) for nn in (1, 2, 3)] == [3.927, 7.069, 10.210])
check("sf-03c 精確 J1 零點 3.832,7.016,10.173", [round(float(z), 3) for z in j1] == [3.832, 7.016, 10.173])
check("sf-03c 誤差 J0：-0.049,-0.022,-0.014", [round(float(asym(0, nn + 1) - j0[nn]), 3) for nn in range(3)] == [-0.049, -0.022, -0.014])
check("sf-03c 誤差 J1：+0.095,+0.053,+0.037", [round(float(asym(1, nn + 1) - j1[nn]), 3) for nn in range(3)] == [0.095, 0.053, 0.037])
check("sf-03c 交錯 j01<j11<j02<j12<j03<j13", j0[0] < j1[0] < j0[1] < j1[1] < j0[2] < j1[2])

# ---------------- am6-ex-4
check("ex-4 0.1289/8=0.0161125", abs(0.1289 / 8 - 0.0161125) < 1e-12)
check("ex-4 0.0196-0.0161125=0.0034875", abs(0.0196 - 0.1289 / 8 - 0.0034875) < 1e-12)
check("ex-4 ③ x^{-3}J4=-(x^{-3}J3)'（數值）", abs(mp.diff(lambda s: s**-3 * J(3, s), mp.mpf('1.5')) + mp.mpf('1.5')**-3 * J(4, mp.mpf('1.5'))) < 1e-20)

# ---------------- am6-k111-4
check("k111-4 J0(2)=0.2239, J1(2)=0.5767", near(J(0, 2), 0.2239, 5e-5) and near(J(1, 2), 0.5767, 5e-5))
check("k111-4 0.5767-0.2239=0.3528, ÷2=0.1764", abs(0.5767 - 0.2239 - 0.3528) < 1e-12 and abs(0.3528 / 2 - 0.1764) < 1e-12)
I = mp.quad(lambda r: (r - r**3) * J(0, 2 * r), [0, 1])
check("k111-4 數值積分 = ½J2(2)", abs(I - J(2, 2) / 2) < 1e-20)
check("k111-4 ∫x^3J0 = x^3J1-2x^2J2（數值，0→2）", abs(mp.quad(lambda s: s**3 * J(0, s), [0, 2]) - (8 * J(1, 2) - 8 * J(2, 2))) < 1e-20)

# ---------------- am6-sf-04a
check("sf-04a ①（m=1/3）", abs(mp.diff(lambda s: s ** (mp.mpf(1) / 3) * J(mp.mpf(1) / 3, s), 1.2) - 1.2 ** (mp.mpf(1) / 3) * J(mp.mpf(1) / 3 - 1, 1.2)) < 1e-20)
check("sf-04a ③（m=1/3）", abs(mp.diff(lambda s: s ** (-mp.mpf(1) / 3) * J(mp.mpf(1) / 3, s), 1.2) + 1.2 ** (-mp.mpf(1) / 3) * J(mp.mpf(4) / 3, 1.2)) < 1e-20)
z = mp.mpf("2.7")
check("sf-04a ④⑤（m=2）", abs(J(2, z) - z * (J(1, z) + J(3, z)) / 4) < 1e-25 and abs(2 * mp.diff(lambda s: J(2, s), z) - (J(1, z) - J(3, z))) < 1e-20)
check("sf-04a J_{3/2} 封閉形式", abs(J(1.5, z) - mp.sqrt(2 / (mp.pi * z)) * (mp.sin(z) / z - mp.cos(z))) < 1e-25)

# ---------------- am6-sf-04b
z14 = mp.mpf("1.4")
check("sf-04b ∫J3 = -J0-2J2 = J0-4J1/x（導數）", abs(mp.diff(lambda s: -J(0, s) - 2 * J(2, s), z14) - J(3, z14)) < 1e-20 and abs((-J(0, z14) - 2 * J(2, z14)) - (J(0, z14) - 4 / z14 * J(1, z14))) < 1e-25)
check("sf-04b ∫x^4J1 = x^4J2-2x^3J3（導數）", abs(mp.diff(lambda s: s**4 * J(2, s) - 2 * s**3 * J(3, s), z14) - z14**4 * J(1, z14)) < 1e-18)
check("sf-04b ∫J2 = ∫J0-2J1（導數）", abs(J(2, 1.4) - (J(0, 1.4) - 2 * mp.diff(lambda s: J(1, s), 1.4))) < 1e-20)
check("sf-04b 16(0.3528-0.1289)=16×0.2239=3.582", round(16 * (0.3528 - 0.1289), 3) == 3.582 and abs(0.3528 - 0.1289 - 0.2239) < 1e-12)
check("sf-04b -0.2239-0.7056+1=0.0705", round(-0.2239 - 2 * 0.3528 + 1, 4) == 0.0705)
check("sf-04b 數值積分 3.5823、0.07044", near(mp.quad(lambda s: s**4 * J(1, s), [0, 2]), 3.5823, 5e-5) and near(mp.quad(lambda s: J(3, s), [0, 2]), 0.07044, 5e-6))

# ---------------- am6-sf-04c
J1z = [J(1, z) for z in j0]
check("sf-04c J1(j_n)=0.5191,-0.3403,0.2715", [round(float(v), 4) for v in J1z] == [0.5191, -0.3403, 0.2715])
check("sf-04c 2.4048^3=13.907（書寫版用四位零點）", round(2.4048**3, 3) == 13.907)
check("sf-04c 8/(13.907×0.5191)=1.108", round(8 / (13.907 * 0.5191), 3) == 1.108)
c = [8 / (j0[i] ** 3 * J1z[i]) for i in range(3)]
check("sf-04c c1=1.108, c2=-0.1398, c3=0.0455", round(float(c[0]), 3) == 1.108 and round(float(c[1]), 4) == -0.1398 and round(float(c[2]), 4) == 0.0455)
check("sf-04c 積分 = 4J1(j)/j^3（數值）", all(abs(mp.quad(lambda s: s * (1 - s**2) * J(0, j0[i] * s), [0, 1]) - 4 * J1z[i] / j0[i] ** 3) < 1e-20 for i in range(3)))
check("sf-04c ∫_0^j x^3J0 = j^3J1-2j^2J2（數值）", abs(mp.quad(lambda s: s**3 * J(0, s), [0, j0[0]]) - (j0[0] ** 3 * J1z[0] - 2 * j0[0] ** 2 * J(2, j0[0]))) < 1e-18)
check("sf-04c ln(2×1.108)=0.7957", near(mp.log(2 * 1.108), 0.7957, 5e-5))
tau = mp.log(2 * 1.108) / 5.783
check("sf-04c τ=0.1376", round(float(tau), 4) == 0.1376)
check("sf-04c j2^2=30.47", near(j0[1] ** 2, 30.47, 5e-3))
check("sf-04c 第二項 -0.0021", round(float(-0.1398 * mp.exp(-30.47 * 0.1376)), 4) == -0.0021)

# ---------------- am6-sf-04d
check("sf-04d 積分表示 J_n=1/π∫cos(nθ-x sinθ)", all(abs(mp.quad(lambda th: mp.cos(nn * th - z * mp.sin(th)), [0, mp.pi]) / mp.pi - J(nn, z)) < 1e-20 for nn in (0, 1, 3) for z in (mp.mpf("2.4048"), mp.mpf(5))))
tt = sp.symbols("tt")
g = sp.exp(x / 2 * tt) * sp.exp(-x / (2 * tt))
ser_x = sp.expand(sp.series(sp.exp(x * tt / 2), x, 0, 7).removeO() * sp.series(sp.exp(-x / (2 * tt)), x, 0, 7).removeO())
coef = sp.expand(ser_x).coeff(tt, 2)
check("sf-04d t^2 係數 = J2 到 x^6", sp.simplify(sp.expand(sp.series(coef, x, 0, 7).removeO()) - sp.expand(Jser(2, 2))) == 0)

print(f"\n{COUNT[0]} checks, {len(FAILS)} failed")
if FAILS:
    print("FAILED:", FAILS)
    sys.exit(1)
print("ALL CHECKS PASSED")
