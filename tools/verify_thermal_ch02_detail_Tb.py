"""熱學第 2 章 06–10 節「詳細解題」改寫時新增或拆開的數值的獨立驗算（代理 Tb）。

用法：python -X utf8 tools/verify_thermal_ch02_detail_Tb.py
涵蓋 sections/06-sharpness.html、07-ideal-gas.html、08-entropy.html、09-gas-entropy.html、10-mixing.html
每張題目卡在「從題目讀出的條件」「詳解」中出現的中間值與答案。精確組合數用 Python 整數或 lgamma，
連續量用 math / sympy。全部通過才印 ALL CHECKS PASSED。
"""
import sys
from math import comb, log, log10, exp, sqrt, pi, e, erfc, lgamma
import sympy as sp
from scipy.optimize import brentq

sys.stdout.reconfigure(encoding="utf-8")
k = 1.38e-23          # 網站代入用的取位
kx = 1.380649e-23
h = 6.63e-34
G = 6.67e-11
c = 3.00e8
NA = 6.02e23
R = 8.314
u = 1.66e-27
FAIL = []


def check(name, got, want, rel=0.02):
    ok = abs(got - want) <= rel * abs(want) if want != 0 else abs(got) < 1e-12
    print(f"{'OK ' if ok else 'XX '} {name}: {got:.6g}（網站 {want:.6g}）")
    if not ok:
        FAIL.append(name)


def truth(name, cond):
    print(f"{'OK ' if cond else 'XX '} {name}")
    if not cond:
        FAIL.append(name)


def lnC(n, r):
    return lgamma(n + 1) - lgamma(r + 1) - lgamma(n - r + 1)


def ein(N, q):          # 愛因斯坦固體精確多重度
    return comb(q + N - 1, q)


def sci(x):              # 很大的整數 → (尾數, 指數)
    s = str(x)
    return float(s[0] + "." + s[1:6]), len(s) - 1


# ======================= 06 =======================
print("=== sc-2-20 ===")
check("縮小倍數 1e8 m/0.2 m", 1e8 / 0.2, 5e8)
check("新峰寬", 1e-2 / 5e8, 2e-11)
check("相對寬度 1/sqrt(1e20)", 1 / sqrt(1e20), 1e-10)
check("頁寬 25 cm 時", 0.25e-10, 2.5e-11)

print("=== sc-2-21 ===")
z = sp.symbols("z")
truth("d/dz 4z(1-z)=4(1-2z)", sp.simplify(sp.diff(4 * z * (1 - z), z) - 4 * (1 - 2 * z)) == 0)
truth("q^2 z(1-z) = (q/2)^2 * 4z(1-z)", sp.simplify(sp.Symbol("q")**2 * z * (1 - z) - (sp.Symbol("q") / 2)**2 * 4 * z * (1 - z)) == 0)
Nn = sp.symbols("N", positive=True)
sol = sp.solve(4 * z**2 - 4 * z + sp.exp(-1 / Nn), z)
want_roots = sorted([0.5 - 0.5 * sqrt(1 - exp(-1 / 7)), 0.5 + 0.5 * sqrt(1 - exp(-1 / 7))])
got_roots = sorted(complex(r.subs(Nn, 7).evalf()).real for r in sol)
truth("二次方程解 1/2 ± 1/2 sqrt(1-e^{-1/N})（N=7）", all(abs(g - w) < 1e-12 for g, w in zip(got_roots, want_roots)))
for s in sol:
    v = complex(s.subs(Nn, 7).evalf())
    truth(f"  解代回 N=7: 4z(1-z)=e^(-1/7)", abs(4 * v * (1 - v) - exp(-1 / 7)) < 1e-12)
check("e^-0.1", exp(-0.1), 0.9048, 0.001)
check("N=10 w=1/2 sqrt(0.0952)", 0.5 * sqrt(0.0952), 0.154)
for N, want in [(1, 0.398), (10, 0.154), (100, 0.0499), (1000, 0.0158), (10000, 0.0050)]:
    check(f"N={N} w", 0.5 * sqrt(1 - exp(-1 / N)), want)
check("N=1 近似差 25%", 0.5 / (0.5 * sqrt(1 - exp(-1))) - 1, 0.258, 0.05)
check("0.96^1000", 0.96**1000, 1.9e-18)

print("=== sc-2-22 ===")
for N in (50, 200):
    lnOmNN = lnC(2 * N - 1, N)
    approx = 2 * N * log(2) - 0.5 * log(4 * pi * N)
    check(f"Ω(N,N)≈2^(2N)/sqrt(4πN) 的 ln（N={N}）", approx, lnOmNN, 0.001)
check("sqrt(π/2e23)", sqrt(pi / 2e23), 4.0e-12)
check("π/2e23", pi / 2e23, 1.57e-23)
ratio = comb(199, 100) / comb(99, 50)**2
check("N=50 精確 C(199,100)/C(99,50)^2", ratio, 17.8)
check("sqrt(100π)", sqrt(100 * pi), 17.7)
Ns = sp.symbols("N", positive=True)
truth("4πN/sqrt(8πN) = sqrt(2πN)", sp.simplify(4 * sp.pi * Ns / sp.sqrt(8 * sp.pi * Ns) - sp.sqrt(2 * sp.pi * Ns)) == 0)
truth("sqrt(2πN)/(2N) = sqrt(π/(2N))", sp.simplify(sp.sqrt(2 * sp.pi * Ns) / (2 * Ns) - sp.sqrt(sp.pi / (2 * Ns))) == 0)

print("=== sc-2-23 ===")
check("sqrt(2/(π·1e23))", sqrt(2 / (pi * 1e23)), 2.5e-12)
check("其倒數 4e11", 1 / sqrt(2 / (pi * 1e23)), 4e11, 0.03)
check("log10(4e11)", log10(4e11), 11.6, 0.01)
check("1e23·log10 2", 1e23 * log10(2), 3.0e22)
check("一年秒數", 365.25 * 24 * 3600, 3.16e7, 0.002)
check("1e10 年", 1e10 * 3.16e7, 3.16e17, 0.001)
check("經歷微觀態數", 1e9 * 3.16e17, 3e26, 0.06)
check("log10(3e26)", log10(3.16e26), 26.5, 0.01)

print("=== tk-115-6 ===")
x = sp.symbols("x")
f = (Ns / 2 + x) * sp.log(Ns / 2 + x) + (Ns / 2 - x) * sp.log(Ns / 2 - x)
ser = sp.series(f.subs(Ns, sp.Symbol("M")), x, 0, 3).removeO()
truth("f(x) 展開 = N ln(N/2) + 2x²/N", sp.simplify(ser - (sp.Symbol("M") * sp.log(sp.Symbol("M") / 2) + 2 * x**2 / sp.Symbol("M"))) == 0)
f2 = Ns / 2 * sp.log((Ns / 2)**2 - x**2) + x * sp.log((Ns / 2 + x) / (Ns / 2 - x))
truth("重排 f = N/2 ln[(N/2)²−x²] + x ln[(N/2+x)/(N/2−x)]", abs(float((f - f2).subs({Ns: 1000, x: 37}))) < 1e-9)
check("第一項的 x² 係數 −2/N（N=1000, x=5 數值）", float((Ns / 2 * sp.log((Ns / 2)**2 - x**2) - Ns * sp.log(Ns / 2)).subs({Ns: 1000, x: 5})), -2 * 25 / 1000, 0.01)
check("第二項 4x²/N（N=1000, x=5）", float((x * sp.log((Ns / 2 + x) / (Ns / 2 - x))).subs({Ns: 1000, x: 5})), 4 * 25 / 1000, 0.01)
for xx in (0, 10, 22):
    exact = lnC(1000, 500 + xx)
    approx = 1000 * log(2) + 0.5 * log(2 / (pi * 1000)) - 2 * xx**2 / 1000
    check(f"N=1000, x={xx} 高斯 vs 精確（ln）", approx, exact, 0.0005)
check("sqrt(2/1e20)", sqrt(2 / 1e20), 1.4e-10, 0.02)

print("=== tkx-3 ===")
Nu, NN, mu, B, kk = sp.symbols("N_u N mu B k", positive=True)
S = kk * (NN * sp.log(NN) - Nu * sp.log(Nu) - (NN - Nu) * sp.log(NN - Nu))
dS = sp.simplify(sp.diff(S, Nu) / kk - sp.log((NN - Nu) / Nu))
truth("∂(S/k)/∂N↑ = ln(N↓/N↑)", sp.simplify(sp.expand_log(dS, force=True)) == 0)
U = sp.symbols("U")
Nu_of_U = (NN - U / (mu * B)) / 2
truth("dN↑/dU = −1/(2μB)", sp.simplify(sp.diff(Nu_of_U, U) + 1 / (2 * mu * B)) == 0)
invT = (kk / (2 * mu * B)) * sp.log(Nu / (NN - Nu))
truth("1/T = k/(2μB) ln(N↑/N↓)", sp.simplify(sp.expand_log(sp.diff(S, Nu) * (-1 / (2 * mu * B)) - invT, force=True)) == 0)
truth("N↑=N/2 時 S/k = N ln2", sp.simplify(sp.expand_log((S / kk).subs(Nu, NN / 2) - NN * sp.log(2), force=True)) == 0)

print("=== sc-2-24 ===")
N = 10**6
sig = sqrt(N) / 2
check("σ", sig, 500)
check("1/e 半寬 sqrt(N/2)", sqrt(N / 2), 707, 0.001)
check("e^-2", exp(-2), 0.135, 0.005)
check("x0/(√2σ)=√2", 1000 / (sqrt(2) * 500), sqrt(2))
check("erfc(√2)", erfc(sqrt(2)), 0.0455, 0.005)
check("P ≥ 501000", 0.5 * erfc(sqrt(2)), 0.023, 0.02)
check("1/0.0228 ≈ 44", 1 / 0.0228, 44, 0.01)
check("剛好 501000 的機率", sqrt(2 / (pi * N)) * exp(-2), 1.1e-4, 0.03)
check("剛好 500000 的機率", sqrt(2 / (pi * N)), 8.0e-4, 0.01)
check("e^-200", exp(-200), 1.4e-87, 0.02)
check("z=1e4/707", 1e4 / 707, 14.1, 0.01)
check("P ≥ 510000", 0.5 * exp(-200) / (sqrt(200) * sqrt(pi)), 2.8e-89, 0.02)
check("精確 erfc(14.142)/2", 0.5 * erfc(sqrt(200)), 2.8e-89, 0.03)

print("=== sc-2-25 ===")
check("σ_X=sqrt(1e4)", sqrt(1e4), 100)
check("X_1/e=sqrt(2e4)", sqrt(2e4), 141, 0.005)
Nst = 1 / 3e-10
check("一秒步數", Nst, 3.3e9, 0.02)
check("2N", 2 * Nst, 6.7e9, 0.01)
check("sqrt(2N)", sqrt(2 * Nst), 8.2e4, 0.01)
check("X_1/e (m)", sqrt(2 * Nst) * 1.5e-7, 0.012, 0.03)
check("方均根 (m)", sqrt(Nst) * 1.5e-7, 0.0087, 0.01)
check("總路程", Nst * 1.5e-7, 500, 0.01)
truth("T 的指數：1 − 1/4 = 3/4", sp.Rational(1) - sp.Rational(1, 4) == sp.Rational(3, 4))
ell, vb, t, Dt = sp.symbols("ell vbar t Delta_t", positive=True)
truth("4Dt = 2ℓ²(t/Δt) 當 D=ℓv̄/2、v̄=ℓ/Δt", sp.simplify(4 * (ell * vb / 2) * t - 2 * ell**2 * t / Dt).subs(vb, ell / Dt) == 0)

print("=== sf-06a ===")
q, xx_ = sp.symbols("q x", positive=True)
Nsym = sp.symbols("N", positive=True)
lnO = Nsym * sp.log(q / 3 + xx_) + 2 * Nsym * sp.log(2 * q / 3 - xx_)
s2 = sp.series(lnO, xx_, 0, 3).removeO()
truth("一次項為 0", sp.simplify(s2.coeff(xx_, 1)) == 0)
truth("二次項 = −27N/(4q²)", sp.simplify(s2.coeff(xx_, 2) + 27 * Nsym / (4 * q**2)) == 0)
check("2/sqrt(27)", 2 / sqrt(27), 0.385, 0.002)
check("6/sqrt(27)", 6 / sqrt(27), 1.155, 0.001)
check("3/sqrt(27)", 3 / sqrt(27), 0.577, 0.001)
NA_, NB_ = sp.symbols("N_A N_B", positive=True)
Nt = NA_ + NB_
sec = -NA_ / (NA_ * q / Nt)**2 - NB_ / (NB_ * q / Nt)**2
truth("二階導數 = −N_tot³/(q² N_A N_B)", sp.simplify(sec + Nt**3 / (q**2 * NA_ * NB_)) == 0)
truth("N_A=N_B=N：q/(2√N)", sp.simplify(q * sp.sqrt(2 * Nsym**2 / (2 * Nsym)**3) - q / (2 * sp.sqrt(Nsym))) == 0)
truth("N_B=2N_A：2q/√(27N)", sp.simplify(q * sp.sqrt(2 * Nsym * 2 * Nsym / (3 * Nsym)**3) - 2 * q / sp.sqrt(27 * Nsym)) == 0)
nA, nB, qq = 2000, 4000, 10**6
xs = round(qq * sqrt(2 * nA * nB / (nA + nB)**3))
qa0 = qq // 3


def lnOm(qa):
    return lnC(qa + nA - 1, qa) + lnC(qq - qa + nB - 1, qq - qa)


check("N_A=2000,N_B=4000 精確 Ω/Ωmax at x_1/e", exp(lnOm(qa0 + xs) - lnOm(qa0)), 0.37, 0.02)

print("=== sf-06b ===")
sg = sp.symbols("sigma", positive=True)
truth("σ² = q²/(8N)", sp.simplify(sp.solve(sp.Eq(4 * Nsym / q**2, 1 / (2 * sg**2)), sg)[0] - q / (2 * sp.sqrt(2 * Nsym))) == 0)
dl = sp.symbols("delta", positive=True)
truth("z = δ√N", sp.simplify((dl * q / 2) / (sp.sqrt(2) * q / (2 * sp.sqrt(2 * Nsym))) - dl * sp.sqrt(Nsym)) == 0)
check("e^-100", exp(-100), 3.7e-44, 0.01)
check("10√π", 10 * sqrt(pi), 17.7, 0.002)
check("erfc(10) 近似", exp(-100) / (10 * sqrt(pi)), 2.1e-45, 0.01)
check("erfc(10) 精確", erfc(10), 2.088e-45, 0.001)
zz = brentq(lambda t: erfc(t) - 0.5, 0.1, 2)
check("erfc(z)=0.5 → z", zz, 0.477, 0.002)
check("δ_50%", zz / 1e10, 4.8e-11, 0.01)
check("一兆次 × 宇宙年齡", 1e12 * 1.38e10 * 3.16e7, 4e29, 0.1)

# ======================= 07 =======================
print("=== sc-ex-half ===")
check("100·log10 2", 100 * log10(2), 30.1, 0.001)
check("2^-100", 2.0**-100, 7.9e-31, 0.01)

print("=== tk-115-7 ===")
NN2 = sp.symbols("N", positive=True, integer=True)
r = sp.symbols("r", positive=True)
lhs = 2 * sp.pi**NN2 / sp.factorial(NN2 - 1) * r**(2 * NN2 - 1)
rhs = (2 * NN2 / r) * sp.pi**NN2 / sp.factorial(NN2) * r**(2 * NN2)
truth("2π^N/(N−1)! r^(2N−1) = (2N/r)·π^N/N!·r^(2N)", all(abs(float((lhs - rhs).subs({NN2: n, r: 1.7}))) < 1e-9 for n in (1, 2, 5, 9)))
truth("d=2N 時 2π^(d/2)/(d/2−1)! r^(d−1)（d=2：圓周 2πr）", sp.simplify(lhs.subs(NN2, 1) - 2 * sp.pi * r) == 0)

print("=== sc-2-27 ===")
check("ln 0.99", log(0.99), -0.01005, 0.001)
check("0.99^100", 0.99**100, 0.366, 0.002)
check("100.5/2.303", 10000 * -log(0.99) / log(10), 43.65, 0.001)
check("0.99^10000", 0.99**10000, 2.2e-44, 0.03)
check("log10 0.99", log10(0.99), -0.004365, 0.001)
check("1e23·log10 0.99", 1e23 * log10(0.99), -4.4e20, 0.01)

print("=== sf-07a ===")
pp = sp.symbols("p", positive=True)
nn = 6
truth("二項分布加總為 1（N=6 符號驗算）", sp.simplify(sum(sp.binomial(nn, i) * pp**i * (1 - pp)**(nn - i) for i in range(nn + 1)) - 1) == 0)
mean = sum(i * sp.binomial(nn, i) * pp**i * (1 - pp)**(nn - i) for i in range(nn + 1))
var = sum(i**2 * sp.binomial(nn, i) * pp**i * (1 - pp)**(nn - i) for i in range(nn + 1)) - mean**2
truth("平均 Np、變異數 Np(1−p)", sp.simplify(mean - nn * pp) == 0 and sp.simplify(var - nn * pp * (1 - pp)) == 0)
nd = 1.013e5 / (k * 300)
check("數密度", nd, 2.45e25, 0.003)
check("v=1e4/nd", 1e4 / 2.45e25, 4.1e-22, 0.01)
check("L", (1e4 / 2.45e25)**(1 / 3), 7.4e-8, 0.01)
check("1 mm³ 分子數", 2.45e25 * 1e-9, 2.45e16)
check("相對擾動", 1 / sqrt(2.45e16), 6.4e-9, 0.01)

print("=== sf-07b ===")
a, b = 1.5, 3.0
check("(a+b)^3/N^3 = 729/8", (a + b)**3, 91.1, 0.001)
check("2ab/N² = 9", 2 * a * b, 9)
check("sqrt(9/91.125)", sqrt(9 / 91.125), 0.314, 0.002)
check("sqrt(6.02e23)", sqrt(6.02e23), 7.76e11, 0.001)
check("比值", sqrt(9 / 91.125) / sqrt(6.02e23), 4.0e-13, 0.02)
aa, bb, Ut = sp.symbols("a b U", positive=True)
sec2 = -aa / (aa * Ut / (aa + bb))**2 - bb / (bb * Ut / (aa + bb))**2
truth("二階導數 = −(a+b)³/(ab U²)", sp.simplify(sec2 + (aa + bb)**3 / (aa * bb * Ut**2)) == 0)

# ======================= 08 =======================
print("=== sc-ex-sein ===")
check("ln100+1", log(100) + 1, 5.61, 0.001)
check("S/k", 1e22 * (log(100) + 1), 5.6e22, 0.003)
check("S (J/K)", 5.6e22 * k, 0.77, 0.005)
check("log10 Ω", 5.605e22 / log(10), 2.4e22, 0.02)
check("q/N=1000 時", log(1000) + 1, 7.9, 0.002)

print("=== sc-2-28 ===")
f52 = 1
for i in range(1, 53):
    f52 *= i
check("52!", float(f52), 8.07e67, 0.001)
check("ln 8.07", log(8.07), 2.09, 0.002)
check("67 ln10", 67 * log(10), 154.27, 0.0001)
check("ln52!", lgamma(53), 156.4, 0.001)
check("52 ln52", 52 * log(52), 205.5, 0.001)
check("½ ln(104π)", 0.5 * log(104 * pi), 2.9, 0.01)
check("Stirling 含根號", 52 * log(52) - 52 + 0.5 * log(104 * pi), 156.4, 0.001)
check("S（2 位有效數字）", 156.36 * k, 2.2e-21, 0.03)
check("纖維素每原子 g/mol", 162 / 21, 8, 0.04)
check("牌的原子數", 100 / 8 * 6e23, 1e25, 0.3)
check("S_熱", 7.5e24 * k, 100, 0.05)
truth("比值 ≥ 1e22", 100 / 2.2e-21 > 1e22)

print("=== sc-2-29 ===")
tot = [ein(300, qa) * ein(200, 100 - qa) for qa in range(101)]
truth("最可能 q_A=60", max(range(101), key=lambda i: tot[i]) == 60)
truth("最不可能 q_A=0", min(range(101), key=lambda i: tot[i]) == 0)
truth("Ω_B(q_B)=C(299−q_A,100−q_A)", all(ein(200, 100 - qa) == comb(299 - qa, 100 - qa) for qa in range(101)))
truth("總和 = C(599,100)", sum(tot) == comb(599, 100))
for name, val, want in [("Ω(60)", tot[60], (6.87, 114)), ("Ω(0)", tot[0], (2.77, 81)), ("總和", sum(tot), (9.26, 115))]:
    mnt, ex = sci(val)
    truth(f"{name} = {mnt:.4f}e{ex}（網站 {want[0]}e{want[1]}）", ex == want[1] and abs(mnt - want[0]) < 0.006)
check("ln 6.87", log(6.87), 1.93, 0.002)
check("114 ln10", 114 * log(10), 262.5, 0.0005)
check("S(60)", log(tot[60]), 264.4, 0.0003)
check("ln 2.77", log(2.77), 1.02, 0.005)
check("81 ln10", 81 * log(10), 186.5, 0.0005)
check("S(0)", log(tot[0]), 187.5, 0.0003)
check("ln 9.26", log(9.26), 2.23, 0.002)
check("115 ln10", 115 * log(10), 264.8, 0.0003)
check("S(all)", log(sum(tot)), 267.0, 0.0003)

print("=== sc-2-30 ===")
N = 1e23
check("4N ln2", 4 * N * log(2), 2.77e23, 0.002)
check("8πN", 8 * pi * N, 2.51e24, 0.002)
check("ln(8πN)", log(8 * pi * N), 56.2, 0.001)
check("½ ln(8πN)", 0.5 * log(8 * pi * N), 28.1, 0.002)
check("4πN", 4 * pi * N, 1.26e24, 0.005)
check("ln(4πN)", log(4 * pi * N), 55.5, 0.001)
check("差", log(4 * pi * N) - 0.5 * log(8 * pi * N), 27.4, 0.002)
check("相對", 27.4 / 2.77e23, 1e-22, 0.02)
check("27.4 k", 27.4 * k, 3.8e-22, 0.01)

print("=== sc-2-36 ===")
check("1000/12", 1000 / 12, 83, 0.005)
check("書 N", 83 * NA, 5e25, 0.01)
check("書 S", 5e25 * k, 700, 0.02)
check("400 kg 水 mol", 4e5 / 18, 2.2e4, 0.02)
check("麋鹿 N", 4e5 / 18 * NA, 1.3e28, 0.03)
check("原子數 ×3", 3 * 1.34e28, 4e28, 0.01)
truth("麋鹿 S 在 1e5–1e6 J/K", 1e5 <= 1.3e28 * k <= 1e6 and 1e5 <= 4e28 * k * 10 <= 1e7)
check("太陽 N", 2 * 2e30 / 1.67e-27, 2.4e57, 0.002)
check("太陽 Nk", 2.4e57 * k, 3.3e34, 0.01)
truth("太陽 (10–20)Nk 在 1e35–1e36 J/K", 1e35 <= 10 * 3.3e34 and 20 * 3.3e34 <= 1e36)

print("=== sf-08a ===")
check("ln(4/3)", log(4 / 3), 0.288, 0.002)
check("2ln2000−ln3000−ln1000", 2 * log(2000) - log(3000) - log(1000), 0.288, 0.002)
check("ΔS (J/K)", 0.2877 * 1e22 * k, 0.040, 0.01)
qa, qb = sp.symbols("q_a q_b", positive=True)
truth("(qa+qb)²−4qa qb = (qa−qb)²", sp.expand((qa + qb)**2 - 4 * qa * qb - (qa - qb)**2) == 0)
n0 = 200
ex = 2 * lnC(4 * 10**5 + n0 - 1, 4 * 10**5) - lnC(6 * 10**5 + n0 - 1, 6 * 10**5) - lnC(2 * 10**5 + n0 - 1, 2 * 10**5)
check("N=200 精確 ΔS/k", ex, 57.2, 0.003)

print("=== sf-08b ===")
check("100 ln2", 100 * log(2), 69.3, 0.001)
check("ΔS coins", 69.3 * k, 9.6e-22, 0.005)
check("Q/T", 10 / 310, 0.032, 0.01)
check("比", (10 / 310) / 9.6e-22, 3e19, 0.15)
check("Cu 原子數", 5 / 63.5 * NA, 4.7e22, 0.01)
check("Cu S", 4.74e22 * k, 0.65, 0.01)
check("比例", log(2) / 4.7e22, 1.5e-23, 0.02)

# ======================= 09 =======================
print("=== sc-2-31 / tk-114-3(d) / tkx-1j：Sackur–Tetrode 代數 ===")
V, Uu, m, hh, Np = sp.symbols("V U m h N", positive=True)
lnO = (Np * sp.log(V) - 3 * Np * sp.log(hh) + sp.Rational(3, 2) * Np * sp.log(sp.pi) + sp.Rational(3, 2) * Np * sp.log(2 * m * Uu)
       - (Np * sp.log(Np) - Np) - (sp.Rational(3, 2) * Np * sp.log(sp.Rational(3, 2) * Np) - sp.Rational(3, 2) * Np))
ST = Np * (sp.log(V / Np * (4 * sp.pi * m * Uu / (3 * Np * hh**2))**sp.Rational(3, 2)) + sp.Rational(5, 2))
vals = {V: 0.025, Uu: 3700, m: 6.64e-27, hh: 6.63e-34, Np: 6.02e23}
check("Stirling 展開 = Sackur–Tetrode（數值）", float(lnO.subs(vals)), float(ST.subs(vals)), 1e-10)
mid = Np * (sp.log(V) + sp.Rational(3, 2) * sp.log(2 * sp.pi * m * Uu / hh**2)) - (Np * sp.log(Np) - Np) - (sp.Rational(3, 2) * Np * sp.log(sp.Rational(3, 2) * Np) - sp.Rational(3, 2) * Np)
check("合併 h、π、2mU 後同值", float(mid.subs(vals)), float(lnO.subs(vals)), 1e-12)
truth("(2πmU/h²)÷(3N/2) = 4πmU/(3Nh²)", sp.simplify((2 * sp.pi * m * Uu / hh**2) / (sp.Rational(3, 2) * Np) - 4 * sp.pi * m * Uu / (3 * Np * hh**2)) == 0)
truth("∂S/∂U = 3Nk/(2U)", sp.simplify(sp.diff(ST, Uu) - sp.Rational(3, 2) * Np / Uu) == 0)

print("=== tk-114-3 (b)(c) ===")
Tt, Vv, Cv = sp.symbols("T V C_V", positive=True)
gam = sp.Rational(5, 2) / sp.Rational(3, 2)
truth("γ = 5/3", gam == sp.Rational(5, 3))
truth("Nk/C_V = γ−1", sp.simplify((sp.Rational(5, 2) - sp.Rational(3, 2)) / sp.Rational(3, 2) - (gam - 1)) == 0)
Tf = sp.Function("T")
sol = sp.dsolve(sp.Eq(sp.Rational(3, 2) * Tf(Vv).diff(Vv), -Tf(Vv) / Vv), Tf(Vv))
truth("絕熱 ODE 解 T ∝ V^(−2/3)", sp.simplify(sol.rhs * Vv**sp.Rational(2, 3)).free_symbols <= {sp.Symbol("C1")})
check("一莫耳氦 T=2U/(3R)", 2 * 3700 / (3 * R), 297, 0.002)

print("=== sc-ex-helium ===")
VN = 0.025 / 6.02e23
UN = 3700 / 6.02e23
check("V/N", VN, 4.15e-26, 0.002)
check("U/N", UN, 6.15e-21, 0.002)
num = 4 * pi * 6.64e-27 * 6.15e-21
den = 3 * (6.63e-34)**2
check("分子 4πm(U/N)", num, 5.13e-46, 0.003)
check("分母 3h²", den, 1.32e-66, 0.003)
check("括號", num / den, 3.9e20, 0.01)
check("3/2 次方", (num / den)**1.5, 7.7e30, 0.01)
arg = VN * (num / den)**1.5
check("對數裡的數", arg, 3.2e5, 0.01)
check("ln3.2", log(3.2), 1.16, 0.003)
check("5 ln10", 5 * log(10), 11.51, 0.001)
check("ln(3.2e5)", log(3.2e5), 12.7, 0.002)
check("S/Nk", log(arg) + 2.5, 15.2, 0.003)
check("S", 15.2 * 8.31, 126, 0.003)
check("S/k", 15.2 * 6.02e23, 9.1e24, 0.01)
kg, mtr, sec = sp.symbols("kg m s", positive=True)
J = kg * mtr**2 / sec**2
truth("單位 kg·J/(J·s)² = m^-2", sp.simplify(kg * J / (J * sec)**2 - mtr**-2) == 0)

print("=== sc-2-34 ===")
Vi, Vf, T = sp.symbols("V_i V_f T", positive=True)
Q = sp.integrate(Np * sp.Symbol("k") * T / Vv, (Vv, Vi, Vf))
truth("Q = NkT ln(Vf/Vi)", sp.simplify(sp.expand_log(Q - Np * sp.Symbol("k") * T * sp.log(Vf / Vi), force=True)) == 0)

print("=== sc-2-32 ===")
A = sp.symbols("A", positive=True)
lnO2 = Np * sp.log(2 * sp.pi * m * Uu * A / hh**2) - 2 * (Np * sp.log(Np) - Np)
S2 = Np * (sp.log(A / Np * 2 * sp.pi * m * Uu / (Np * hh**2)) + 2)
truth("二維熵代數", sp.simplify(sp.expand_log(lnO2 - S2, force=True)) == 0)

print("=== sc-2-33 ===")
VNa = k * 300 / 1e5
UNa = 1.5 * k * 300
check("V/N", VNa, 4.14e-26, 0.001)
check("U/N", UNa, 6.21e-21, 0.001)
br = 4 * pi * 6.64e-26 * 6.21e-21 / (3 * (6.63e-34)**2)
check("括號", br, 3.9e21, 0.01)
check("3/2 次方", br**1.5, 2.5e32, 0.02)
argA = VNa * br**1.5
check("對數裡的數", argA, 1.0e7, 0.03)
check("7 ln10", 7 * log(10), 16.1, 0.002)
check("ln(argA)+2.5", log(argA) + 2.5, 18.6, 0.003)
check("S", 8.31 * 18.6, 155, 0.003)
check("1.5 R ln10", 1.5 * 8.31 * log(10), 29, 0.02)
check("用氦例題 3.2e5×10^1.5", 3.19e5 * 10**1.5, 1.0e7, 0.01)
check("40 u", 40 * u, 6.64e-26, 0.001)

print("=== sc-2-35 ===")
nV = 1.013e5 / (k * 300)
check("N/V", nV, 2.45e25, 0.003)
check("(N/V)^(2/3)", nV**(2 / 3), 8.4e16, 0.01)
check("e^(5/3)", exp(5 / 3), 5.29, 0.001)
numT = 8.4e16 * (6.63e-34)**2
denT = 2 * pi * 5.29 * 6.64e-27 * k
check("分子", numT, 3.7e-50, 0.01)
check("分母", denT, 3.05e-48, 0.002)
check("T", numT / denT, 0.012, 0.03)
mm, kk2, TT, nv = sp.symbols("m k T n", positive=True)
eq = sp.Eq((1 / nv) * sp.exp(sp.Rational(5, 2)) * (2 * sp.pi * mm * kk2 * TT / hh**2)**sp.Rational(3, 2), 1)
solT = sp.solve(eq, TT)[0]
truth("T = (N/V)^(2/3) h²/(2π e^(5/3) m k)", sp.simplify(solT - nv**sp.Rational(2, 3) * hh**2 / (2 * sp.pi * sp.exp(sp.Rational(5, 3)) * mm * kk2)) == 0)

print("=== sf-09a ===")
check("R ln2", R * log(2), 5.76, 0.001)
check("W_on", R * 300 * log(2), 1729, 0.0005)
check("ΔS_res", 1729 / 300, 5.76, 0.001)

print("=== sf-09b ===")
check("1.5 R ln2", 1.5 * R * log(2), 8.64, 0.001)
check("2.5 R ln2", 2.5 * R * log(2), 14.41, 0.0005)
check("(1/2)^1.5", 0.5**1.5, 0.354, 0.002)
check("2^1.5", 2**1.5, 2.83, 0.001)

# ======================= 10 =======================
print("=== sc-ex-mix ===")
check("1.5 R ln10", 1.5 * R * log(10), 29, 0.02)
check("He+Ar 總熵（例題條件）", 126.2 + 126.2 + 1.5 * R * log(10), 281, 0.003)
check("2R ln2", 2 * 8.31 * log(2), 11.5, 0.003)
check("審查 D：1.5·8.31·ln10", 1.5 * 8.31 * log(10), 28.7, 0.002)
check("審查 D：S_He（Sackur–Tetrode）", S_ST0 := 6.022e23 * kx * (log(0.025 / 6.022e23 * (4 * pi * 4.0026 * 1.6605e-27 * 3700 / (3 * 6.022e23 * 6.62607e-34**2))**1.5) + 2.5), 126, 0.005)
check("審查 D：S_Ar = S_He + 28.7", S_ST0 + 1.5 * 6.022e23 * kx * log(39.948 / 4.0026), 155, 0.005)
check("審查 D：126+28.7", 126 + 28.7, 155, 0.002)
from math import comb as _c
check("審查 D sf-01b：48–52 擴到 45–55 多 3 對", float(len([kk for kk in range(45, 56) if not 48 <= kk <= 52]) // 2), 3.0, 0)
check("審查 D sf-01b：P(45–55)", sum(_c(100, kk) for kk in range(45, 56)) / 2**100, 0.7287, 0.0002)
S_ST = lambda Vv_, Uu_, Nn_, mm_: Nn_ * (log(Vv_ / Nn_ * (4 * pi * mm_ * Uu_ / (3 * Nn_ * h**2))**1.5) + 2.5)
mHe = 6.64e-27
truth("(b) S(2N,2U,V) = 2S_He − 2Nk ln2（數值）", abs(S_ST(0.025, 7400, 2 * NA, mHe) - (2 * S_ST(0.025, 3700, NA, mHe) - 2 * NA * log(2))) < 1e-6 * S_ST(0.025, 3700, NA, mHe))

print("=== sc-2-37 ===")
xm = sp.symbols("x", positive=True)
fm = -(xm * sp.log(xm) + (1 - xm) * sp.log(1 - xm))
truth("d/dx = ln((1−x)/x)", sp.simplify(sp.expand_log(sp.diff(fm, xm) - sp.log((1 - xm) / xm), force=True)) == 0)
truth("x=1/2 時 = ln2", sp.simplify(fm.subs(xm, sp.Rational(1, 2)) - sp.log(2)) == 0)

print("=== sc-2-38 ===")
check("ln C(1000,250)/1000", lnC(1000, 250) / 1000, 0.559, 0.002)
check("公式", -(0.25 * log(0.25) + 0.75 * log(0.75)), 0.562, 0.002)
Nn3 = sp.symbols("N", positive=True)
expr = Nn3 * sp.log(Nn3) - (1 - xm) * Nn3 * (sp.log(1 - xm) + sp.log(Nn3)) - xm * Nn3 * (sp.log(xm) + sp.log(Nn3))
truth("ln N 係數抵消", sp.simplify(sp.expand(expr) + Nn3 * (xm * sp.log(xm) + (1 - xm) * sp.log(1 - xm))) == 0)

print("=== sc-2-39 ===")
check("ln(6.02e23)", log(6.02e23), 54.8, 0.001)
check("ln(3.2e5)", log(3.2e5), 12.7, 0.002)
check("和", log(6.02e23) + log(3.2e5), 67.4, 0.001)
check("+1.5", log(6.02e23) + log(3.2e5) + 1.5, 68.9, 0.001)
check("S", 68.9 * 8.31, 573, 0.002)
check("比值", 573 / 126, 4.5, 0.02)
check("R(lnN−1)", 8.31 * (log(6.02e23) - 1), 447, 0.002)
check("k ln N! 精確（lgamma，J/K）", lgamma(6.02e23 + 1) * 1.38e-23, 447, 0.003)

print("=== sc-2-40 ===")
truth("2 C8H18 + 25 O2 → 16 CO2 + 18 H2O：C、H、O 守恆", (2 * 8 == 16) and (2 * 18 == 18 * 2) and (25 * 2 == 16 * 2 + 18))
truth("分子數 27 → 34", 2 + 25 == 27 and 16 + 18 == 34)

print("=== sc-2-41 ===")
check("Q=10×334", 10 * 334, 3340)
check("3340/273", 3340 / 273, 12.2, 0.003)
check("3340/300", 3340 / 300, 11.1, 0.005)
check("ΔS 冰塊", 3340 * (1 / 273 - 1 / 300), 1.1, 0.01)
check("½mv²", 0.5 * 1000 * 20**2, 2e5)
check("ΔS 煞車", 2e5 / 300, 670, 0.01)

print("=== sc-2-42 ===")
aa_, bb_, dd_ = sp.symbols("a b d")
sol = sp.solve([3 * aa_ + bb_ - 1, -aa_ + dd_, -2 * aa_ - bb_], [aa_, bb_, dd_])
truth("指數 a=1, b=−2, d=1", sol == {aa_: 1, bb_: -2, dd_: 1})
M = 2e30
check("R=GM/c²", G * M / c**2, 1.5e3, 0.02)
check("2GM/c² ≈ 3 km", 2 * G * M / c**2, 3e3, 0.02)
truth("N = Mc²/(hc³/GM) = GM²/(hc)", sp.simplify(sp.Symbol("M") * sp.Symbol("c")**2 / (sp.Symbol("h") * sp.Symbol("c")**3 / (sp.Symbol("G") * sp.Symbol("M"))) - sp.Symbol("G") * sp.Symbol("M")**2 / (sp.Symbol("h") * sp.Symbol("c"))) == 0)
Nph = G * M**2 / (h * c)
check("GM²/(hc)（2 位有效數字）", Nph, 1.3e75, 0.04)
check("8π²", 8 * pi**2, 79, 0.002)
check("S/k", 8 * pi**2 * Nph, 1.1e77, 0.04)
check("S", 8 * pi**2 * Nph * k, 1.5e54, 0.03)
truth("1.1e77/1e58–1e57 在 1e19–1e20 倍", 1e19 <= 1.1e77 / 1e58 and 1.1e77 / 1e57 <= 1.2e20)

print("=== sf-10a ===")
check("3ln(20/3)−ln10−2ln5", 3 * log(20 / 3) - log(10) - 2 * log(5), 0.170, 0.002)
check("ln(32/27)", log(32 / 27), 0.170, 0.002)
truth("(20/3)³/(10·25) = 32/27", abs((20 / 3)**3 / 250 - 32 / 27) < 1e-12)
check("ΔS(b)", log(32 / 27) * R, 1.41, 0.003)
check("ΔS(c)", 3 * R * log(2), 17.29, 0.0005)
check("ln(27/4)", log(27 / 4), 1.910, 0.0005)
check("差", 3 * R * log(2) - R * log(32 / 27), 15.88, 0.0005)
check("−[2/3 ln2/3 + 1/3 ln1/3]", -(2 / 3 * log(2 / 3) + 1 / 3 * log(1 / 3)), 0.6365, 0.0005)
truth("換單位常數抵消：n_f=n_1+n_2", 3 == 1 + 2)

print("=== sf-10b ===")
dlt = sp.symbols("delta", positive=True)
truth("2lnU − ln U(1+δ) − ln U(1−δ) = −ln(1−δ²)", all(abs(2 * log(3.0) - log(3.0 * (1 + d)) - log(3.0 * (1 - d)) + log(1 - d * d)) < 1e-12 for d in (0.01, 0.3, 0.7)))
check("ΔS", 1.5 * R * 1e-4, 1.25e-3, 0.003)
check("Q", 1.5 * R * 300 * 0.01, 37.4, 0.002)
check("Q/T", 37.41 / 300, 0.125, 0.003)
check("精確", -1.5 * R * log(1 - 1e-4), 1.2471e-3, 0.0002)

print()
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("ALL CHECKS PASSED")
