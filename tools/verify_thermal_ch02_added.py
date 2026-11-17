"""熱學第 2 章本次新增題目（課本 2.4、2.12、2.21、2.24、2.41 與 20 題自編難題）的獨立驗算。

用法：python -X utf8 tools/verify_thermal_ch02_added.py
精確組合數用 Python 整數；連續量用 numpy / sympy；高斯尾巴用 math.erfc。
每一項和網站上寫的數值比對，全部通過才印 ALL CHECKS PASSED。
"""
import sys
from math import comb, log, log10, exp, sqrt, pi, e, erfc, lgamma
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy.optimize import brentq

sys.stdout.reconfigure(encoding="utf-8")
k = 1.380649e-23
R = 8.314
NA = 6.022e23
FAIL = []


def check(name, got, want, rel=0.01):
    ok = abs(got - want) <= rel * abs(want) if want != 0 else abs(got) < 1e-12
    print(f"{'OK ' if ok else 'XX '} {name}: {got:.6g}（網站 {want:.6g}）")
    if not ok:
        FAIL.append(name)


def same(name, got, want):
    ok = got == want
    print(f"{'OK ' if ok else 'XX '} {name}: {got}（網站 {want}）")
    if not ok:
        FAIL.append(name)


def ein(N, q):
    return comb(q + N - 1, q)


print("=== 課本 2.4 撲克牌 ===")
hands = comb(52, 5)
same("C(52,5)", hands, 2598960)
check("P(royal flush)", 4 / hands, 1.54e-6)

print("=== 課本 2.12 ln ===")
check("ln 1.1", log(1.1), 0.0953)
check("ln(1.1) 誤差", (0.1 - log(1.1)) / log(1.1), 0.049, 0.03)
check("ln 1.01", log(1.01), 0.00995)
check("ln(1.01) 誤差", (0.01 - log(1.01)) / log(1.01), 0.0050, 0.03)
x = sp.symbols("x", positive=True)
assert sp.simplify(sp.diff(sp.log(x), x) - 1 / x) == 0
assert sp.series(sp.log(1 + x), x, 0, 3).removeO() == x - x**2 / 2
print("OK  d/dx ln x = 1/x；ln(1+x) = x - x²/2 + …")

print("=== 課本 2.21 [4z(1-z)]^N 的 1/e 半寬 ===")
for N, want in [(1, 0.398), (10, 0.154), (100, 0.0499), (1000, 0.0158), (10000, 0.0050)]:
    hw = sqrt(1 - exp(-1 / N)) / 2
    check(f"N={N} 半寬", hw, want)
    check(f"N={N} 近似 1/(2√N)", 1 / (2 * sqrt(N)), {1: 0.5, 10: 0.158, 100: 0.05, 1000: 0.0158, 10000: 0.005}[N])

print("=== 課本 2.24(d) 一百萬枚硬幣 ===")
N = 10**6
check("半寬 sqrt(N/2)", sqrt(N / 2), 707)
check("x=1000: e^{-2x²/N}", exp(-2 * 1000**2 / N), 0.135)
check("x=10000: e^{-200}", exp(-200), 1.4e-87, 0.02)
lnP = lambda n: lgamma(N + 1) - lgamma(n + 1) - lgamma(N - n + 1) - N * log(2)
check("P(恰好 501000) 精確", exp(lnP(501000)), 1.08e-4)
check("P(恰好 500000) 精確", exp(lnP(500000)), 7.98e-4)
check("P(恰好 510000) log10", lnP(510000) / log(10), -90.0, 0.005)
sigma = sqrt(N) / 2
check("σ = √N/2", sigma, 500)
check("P(≥501000) ≈ ½erfc(2/√2)", 0.5 * erfc(1000 / sigma / sqrt(2)), 0.0228)
check("P(≥510000) ≈ ½erfc(20/√2)", 0.5 * erfc(10000 / sigma / sqrt(2)), 2.8e-89, 0.05)
# 精確尾巴（對數加總）
tail = sum(exp(lnP(n)) for n in range(501000, 520000))
check("P(≥501000) 精確加總", tail, 0.0228, 0.03)

print("=== 課本 2.41 估計 ===")
check("煞車 ΔS = ½mv²/T", 0.5 * 1000 * 20**2 / 300, 667)
check("冰塊 10 g 在 300 K 水中 ΔS", 3340 * (1 / 273 - 1 / 300), 1.10)
check("冰的相變熵 Q/273", 3340 / 273, 12.2)
check("溫水失熵 Q/300", 3340 / 300, 11.1)

print("=== 自編 01a 固定能量的順磁體 ===")
Nup = 4
same("N_up", (6 + 2) // 2, 4)
same("Ω=C(6,4)", comb(6, 4), 15)
check("P(#1 up)", comb(5, 3) / comb(6, 4), 2 / 3)
check("P(#1,#2 up)", comb(4, 2) / comb(6, 4), 0.4)
check("(2/3)^2", (2 / 3) ** 2, 0.444)
# 窮舉
import itertools
states = [s for s in itertools.product([1, -1], repeat=6) if sum(s) == 2]
same("窮舉微觀態數", len(states), 15)
check("窮舉 P(#1,#2 up)", sum(1 for s in states if s[0] == 1 and s[1] == 1) / 15, 0.4)
check("N=600,N_up=400: P(兩個都 up)", 400 * 399 / (600 * 599), 0.4441, 0.001)

print("=== 自編 01b 磁化量與解析度 ===")
same("M 可能值個數", len(set(2 * n - 100 for n in range(101))), 101)
check("Ω(M=0)/Ω(M=2μ)", comb(100, 50) / comb(100, 51), 1.02)
P5 = sum(comb(100, n) for n in range(48, 53)) / 2**100
check("P(|M|≤5μ)=P(48≤N_up≤52)", P5, 0.383)
check("P(M=0)", comb(100, 50) / 2**100, 0.0796)
P10 = sum(comb(100, n) for n in range(45, 56)) / 2**100
check("P(|M|≤10μ)", P10, 0.729)

print("=== 自編 02a 單一振子的能量分布 ===")
Pn = [Fr(ein(2, 4 - n), ein(3, 4)) for n in range(5)]
same("P(n), N=3,q=4", Pn, [Fr(5, 15), Fr(4, 15), Fr(3, 15), Fr(2, 15), Fr(1, 15)])
same("平均 n", sum(n * p for n, p in enumerate(Pn)), Fr(4, 3))
Nb, qb = 1000, 1000
r = [ein(Nb - 1, qb - n - 1) / ein(Nb - 1, qb - n) for n in range(3)]
check("N=q=1000: P(1)/P(0)", r[0], 0.5, 0.002)
check("N=q=1000: P(0)", ein(Nb - 1, qb) / ein(Nb, qb), 0.5, 0.002)

print("=== 自編 02b 遞迴式 ===")
for N in range(2, 8):
    for q in range(0, 9):
        assert ein(N, q) == sum(ein(N - 1, q - n) for n in range(q + 1))
same("N=3,q=3 遞迴", sum(ein(2, 3 - n) for n in range(4)), 10)
print("OK  Ω(N,q)=Σ Ω(N-1,q-n) 對 N=2..7、q=0..8 成立")

print("=== 自編 03a 不用電腦找峰 ===")
qA_star = brentq(lambda a: (a + 300) * (100 - a) - (a + 1) * (299 - a), 0, 100)
check("300,200,100 交叉點", qA_star, 59.64)
tot = [ein(300, a) * ein(200, 100 - a) for a in range(101)]
same("精確峰", max(range(101), key=lambda a: tot[a]), 60)
qA2 = brentq(lambda a: (a + 10) * (60 - a) - (a + 1) * (79 - a), 0, 60)
check("10,20,60 交叉點", qA2, 18.61)
tot2 = [ein(10, a) * ein(20, 60 - a) for a in range(61)]
same("10,20,60 精確峰", max(range(61), key=lambda a: tot2[a]), 19)
check("比例分配 60·10/30", 60 * 10 / 30, 20)

print("=== 自編 03b 固體＋順磁體 ===")
def solid_para(q):
    return {a: ein(3, a) * comb(3, q - a) for a in range(q + 1) if 0 <= q - a <= 3}
t3 = solid_para(3)
same("q=3 表", [t3[a] for a in range(4)], [1, 9, 18, 10])
same("q=3 總和", sum(t3.values()), 38)
check("q=3 P(qA=2)", 18 / 38, 0.474)
t6 = solid_para(6)
same("q=6 表", [t6[a] for a in range(3, 7)], [10, 45, 63, 28])
same("q=6 總和", sum(t6.values()), 146)
check("q=6 P(qA=5)", 63 / 146, 0.432)
check("q=3 <qB>", sum((3 - a) * w for a, w in t3.items()) / 38, 1.03)
check("q=6 <qB>", sum((6 - a) * w for a, w in t6.items()) / 146, 1.25)
tbig = solid_para(10**6)
check("q→∞ <qB>", sum((10**6 - a) * w for a, w in tbig.items()) / sum(tbig.values()), 1.5, 0.001)
# 生成函數交叉核對：(1-x)^{-3}(1+x)^3 的係數
X = sp.symbols("X")
ser = sp.series((1 + X) ** 3 / (1 - X) ** 3, X, 0, 7).removeO()
same("生成函數 x^3、x^6 係數", (ser.coeff(X, 3), ser.coeff(X, 6)), (38, 146))

print("=== 自編 04a C(2N,N) 與平手 ===")
for n in (10, 100, 1000):
    check(f"C(2N,N)√(πN)/4^N, N={n}", float(Fr(comb(2 * n, n), 4**n)) * sqrt(pi * n), 1 - 1 / (8 * n), 1e-4)
check("Stirling 門檻 N=1e4/π", 1e4 / pi, 3183)
exact_thr = next(n for n in range(3000, 3400) if Fr(comb(2 * n, n), 4**n) < Fr(1, 100))
same("精確門檻 N", exact_thr, 3183)
check("N=3183 精確", float(Fr(comb(6366, 3183), 4**3183)), 0.0099998, 1e-5)
check("N=3182 精確", float(Fr(comb(6364, 3182), 4**3182)), 0.0100013, 1e-5)
check("N=3183 Stirling 值", 1 / sqrt(pi * 3183), 0.0100002, 1e-5)
check("100 枚(N=50) 平手機率", float(Fr(comb(100, 50), 2**100)), 0.0796)
check("100 枚 Stirling", 1 / sqrt(pi * 50), 0.0798)

print("=== 自編 04b 比較很大的數 ===")
Nn = 1e23
logA = (Nn * log(Nn) - Nn + 0.5 * log(2 * pi * Nn)) / log(10)
check("log10 (10^23)!", logA, 2.2566e24, 1e-4)
check("log10 (10^24)^(10^23)", 1e23 * 24, 2.4e24)
check("log10 A/C", logA - 2.4e24, -1.434e23, 1e-3)
check("log10 [A·10^(10^23)]", logA + 1e23, 2.3566e24, 1e-4)

print("=== 自編 05a (2.20) 的修正項 ===")
r_ = sp.symbols("r", positive=True)
f = (1 + r_) * sp.log(1 + r_) - r_ * sp.log(r_)
u_ = sp.symbols("u", positive=True)
ser5 = sp.series(f.subs(r_, 1 / u_) + sp.log(u_), u_, 0, 3).removeO()
assert sp.simplify(ser5 - (1 + u_ / 2 - u_**2 / 6)) == 0
print("OK  f(r) = ln r + 1 + 1/(2r) - 1/(6r²) + …")
fN = lambda rr: (1 + rr) * log(1 + rr) - rr * log(rr)
check("N=50,q=5000: (2.21)+N²/2q", 50 * (log(100) + 1) + 50 / 200, 280.51, 1e-4)
check("N=50,q=5000: (2.18)", 50 * fN(100), 280.51, 1e-4)
check("N=50,q=5000: (2.20)", 50 * (log(100) + 1) + 2500 / 5000, 280.76, 1e-4)
r1 = brentq(lambda rr: (fN(rr) - (log(rr) + 1)) / fN(rr) - 0.01, 1, 1000)
check("1% 門檻 q/N（精確 f）", r1, 13.4, 0.01)
r2 = brentq(lambda rr: rr * (log(rr) + 1) - 50, 1, 1000)
check("1% 門檻（只留 1/2r）", r2, 13.8, 0.02)
check("q=N: 2ln2 vs 1", (2 * log(2) - 1) / (2 * log(2)), 0.28, 0.02)

print("=== 自編 05b 加一份能量 ===")
N5 = 10**22
check("低溫 (q+N)/(q+1)", (1e20 + 1e22) / (1e20 + 1), 101)
check("低溫 ln", log(101), 4.62)
check("高溫 (q+N)/(q+1)", (1e24 + 1e22) / (1e24 + 1), 1.01)
check("高溫 ln", log(1.01), 0.00995)
check("轉移一份：101/1.01", 101 / 1.01, 100)

print("=== 自編 06a 大小不同的兩固體 ===")
xs, q_, Nn_ = sp.symbols("x q N", positive=True)
lnO = Nn_ * sp.log(q_ / 3 + xs) + 2 * Nn_ * sp.log(2 * q_ / 3 - xs)
d1 = sp.diff(lnO, xs).subs(xs, 0)
d2 = sp.diff(lnO, xs, 2).subs(xs, 0)
assert sp.simplify(d1) == 0 and sp.simplify(d2 + sp.Rational(27, 2) * Nn_ / q_**2) == 0
print("OK  峰在 q/3，二階導數 -27N/(2q²)")
check("1/e 半寬係數 2/√27", 2 / sqrt(27), 0.385)
check("一般式 √(2NANB/Ntot³) N,2N", sqrt(2 * 1 * 2 / 27), 0.385)
check("一般式 N,N", sqrt(2 / 8), 0.5)
check("A 的相對擾動 x/(q/3)·√N", 3 * 2 / sqrt(27), 1.155)
check("B 的相對擾動 x/(2q/3)·√N", 1.5 * 2 / sqrt(27), 0.577)
# 數值：N=2000, 4000 振子，q=10^6 高溫精確（lgamma）
NA_, NB_, qq = 2000, 4000, 10**6
lnE = lambda N, q: lgamma(q + N) - lgamma(q + 1) - lgamma(N)
a0 = round(qq / 3)
xw = 2 * qq / sqrt(27 * NA_)
ratio = exp(lnE(NA_, a0 + round(xw)) + lnE(NB_, qq - a0 - round(xw)) - lnE(NA_, a0) - lnE(NB_, qq - a0))
check("數值：x=半寬時 Ω/Ωmax", ratio, exp(-1), 0.02)

print("=== 自編 06b 看到 1e-9 的擾動 ===")
check("erfc(10)", erfc(10), 2.09e-45, 0.01)
d50 = brentq(lambda d: erfc(d * 1e10) - 0.5, 1e-13, 1e-9, xtol=1e-16)
check("50% 時的 δ", d50, 4.8e-11, 0.01)

print("=== 自編 07a 小體積的擾動 ===")
n_air = 101325 / (k * 300)
check("n = P/kT", n_air, 2.45e25)
v = 1e4 / n_air
check("v (n=10^4)", v, 4.08e-22)
check("L", v ** (1 / 3), 7.4e-8)
check("1 mm³ 相對擾動", 1 / sqrt(n_air * 1e-9), 6.4e-9)
# 二項分布交叉核對
from scipy.stats import binom
check("binom 相對 std (N=1e6,p=0.01)", binom.std(10**6, 0.01) / binom.mean(10**6, 0.01), sqrt(0.99 / 1e4), 1e-6)

print("=== 自編 07b 氣體＋固體 ===")
a_, b_ = 1.5, 3.0
check("U_gas/U_solid", a_ / b_, 0.5)
check("氣體能量比例", a_ / (a_ + b_), 1 / 3)
check("相對半寬係數 √(2ab/(a+b)³)", sqrt(2 * a_ * b_ / (a_ + b_) ** 3), 0.3143, 1e-3)
check("N=6.02e23 時 x/U_tot", sqrt(2 * a_ * b_ / (a_ + b_) ** 3) / sqrt(NA), 4.05e-13)
UA, UB = sp.symbols("U_A U_B", positive=True)
Nsym = sp.symbols("N", positive=True)
sol = sp.solve(sp.Eq(sp.Rational(3, 2) * Nsym / UA, 3 * Nsym / UB), UA)
same("U_A = U_B/2", sp.simplify(sol[0] - UB / 2), 0)

print("=== 自編 08a 熱接觸的熵 ===")
check("ΔS/Nk = ln(400/300)", log(400 / 300), 0.2877)
check("N=1e22: ΔS", 0.2877e22 * k, 0.0397)
# 精確兩固體（中等大小）核對：N=200 振子各，qA0=3000N,qB0=1000N
lnE2 = lambda N, q: lgamma(q + N) - lgamma(q + 1) - lgamma(N)
dS = 2 * lnE2(200, 400000) - lnE2(200, 600000) - lnE2(200, 200000)
check("精確 N=200: ΔS/k ≈ 200 ln(4/3)", dS, 200 * log(4 / 3), 0.01)  # 差的 0.3 是根號因子，N 大時可忽略

print("=== 自編 08b 排硬幣 ===")
check("S/k = 100 ln2", 100 * log(2), 69.3)
check("S = 100 k ln2", 100 * k * log(2), 9.57e-22)
check("身體 10 J / 310 K", 10 / 310, 0.032)
check("比值", (10 / 310) / (100 * k * log(2)), 3.4e19, 0.02)
check("一枚 5 g 銅幣原子數", 5 / 63.5 * NA, 4.7e22)

print("=== 自編 09a 自由膨脹再壓回 ===")
check("R ln2", R * log(2), 5.76)
check("300 K 時放熱 RT ln2", R * 300 * log(2), 1729)

print("=== 自編 09b 加熱的熵 ===")
check("定容 1.5 R ln2", 1.5 * R * log(2), 8.64)
check("定壓 2.5 R ln2", 2.5 * R * log(2), 14.41)
check("等熵 V 縮小 2^{3/2}", 2 ** 1.5, 2.83)
# 直接用 Sackur–Tetrode 數值核對
h = 6.626e-34
m = 4.0026 * 1.6605e-27
def ST(V, N, U):
    return N * k * (log(V / N * (4 * pi * m * U / (3 * N * h**2)) ** 1.5) + 2.5)
V1 = NA * k * 300 / 101325
U1, U2 = 1.5 * NA * k * 300, 1.5 * NA * k * 600
check("S–T 定容差", ST(V1, NA, U2) - ST(V1, NA, U1), 8.64)
check("S–T 定壓差", ST(2 * V1, NA, U2) - ST(V1, NA, U1), 14.41)

print("=== 自編 10a 同種氣體不同密度 ===")
check("He+He ΔS/R = ln(32/27)", log(2 / 3) + 2 * log(4 / 3), 0.170, 0.005)
check("He+He ΔS", R * log(32 / 27), 1.41)
check("He+Ar ΔS = 3R ln2", 3 * R * log(2), 17.29)
check("混合部分 R ln(27/4)", R * log(27 / 4), 15.88)
xm = 2 / 3
check("−3R[x ln x+(1−x)ln(1−x)]", -3 * R * (xm * log(xm) + (1 - xm) * log(1 - xm)), 15.88)
# S–T 直接核對（同溫，U/N 相同）
U_per = 1.5 * k * 300
S_init = ST(0.010, NA, NA * U_per) + ST(0.010, 2 * NA, 2 * NA * U_per)
S_fin = ST(0.020, 3 * NA, 3 * NA * U_per)
check("S–T 直接：He+He", S_fin - S_init, 1.41)

print("=== 自編 10b 小溫差熱流 ===")
d = sp.symbols("delta", positive=True)
expr = -sp.log(1 - d**2)
assert sp.series(expr, d, 0, 5).removeO() == d**2 + d**4 / 2
print("OK  -ln(1-δ²) = δ² + δ⁴/2 + …")
check("1 mol, δ=0.01: ΔS=1.5Rδ²", 1.5 * R * 1e-4, 1.25e-3)
check("ΔS 精確", -1.5 * R * log(1 - 1e-4), 1.25e-3)
check("δ=0.01 時 ΔS/(Q/T)=δ", (1.5 * R * 1e-4) / (1.5 * R * 300 * 0.01 / 300), 0.01)

check("10b: Q/T", 1.5 * R * 0.01, 0.125)
check("06a: N=1e20 A 相對擾動", 1.155e-10, 1.2e-10, 0.05)
check("06b: erfc 近似 e^-100/(10√π)", exp(-100) / (10 * sqrt(pi)), 2.1e-45)
check("07b: x/U (N=6.02e23)", 0.3143 / sqrt(NA), 4.0e-13, 0.02)
print()
if FAIL:
    print("FAILED:", *FAIL, sep="\n  ")
    sys.exit(1)
print("ALL CHECKS PASSED")
