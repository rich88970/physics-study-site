"""熱學第 2 章（Schroeder, The Second Law）所有數值答案的獨立重算。

用法：python -X utf8 tools/verify_thermal_ch02.py
大數用 Python 的整數（精確）與 math.lgamma（對數）計算，並和網站上寫的數值比對。
"""
from math import comb, factorial, log, log10, exp, sqrt, pi, e, lgamma

k = 1.380649e-23      # J/K（考卷給 1.38e-23）
h = 6.626e-34         # J·s
NA = 6.022e23
u = 1.6605e-27        # kg
FAIL = []


def check(name, got, want, rel=0.02):
    ok = abs(got - want) <= rel * abs(want) if want != 0 else abs(got) < 1e-12
    print(f"{'OK ' if ok else 'XX '} {name}: {got:.6g}（網站 {want:.6g}）")
    if not ok:
        FAIL.append(name)


def ein(N, q):
    """Einstein 固體精確多重度 C(q+N-1, q)"""
    return comb(q + N - 1, q)


def lnf(n):
    return lgamma(n + 1)


def sci(x):
    """很大的整數 → (尾數, 指數)"""
    s = str(x)
    return float(s[0] + "." + s[1:6]), len(s) - 1


print("=== §2.1 兩態系統 ===")
check("100 枚 Ω(2)", comb(100, 2), 4950)
check("100 枚 Ω(3)", comb(100, 3), 161700)
check("100 枚 2^100", 2 ** 100, 1.27e30)
check("100 枚 P(50)", comb(100, 50) / 2 ** 100, 0.0796)
for n, w in zip(range(5), [1, 4, 6, 4, 1]):
    check(f"習題 2.1 Ω({n})", comb(4, n), w)
check("考古 114-6 微觀態", 2 ** 20, 1048576)
check("考古 114-6 P(序列)", 1 / 2 ** 20, 9.54e-7)
check("考古 114-6 C(20,12)", comb(20, 12), 125970)
check("考古 114-6 P(12H)", comb(20, 12) / 2 ** 20, 0.120)
check("考古 115-3 微觀態", 2 ** 10, 1024)
check("考古 115-3 P(序列)", 1 / 1024, 9.77e-4)
check("考古 115-3 C(10,7)", comb(10, 7), 120)
check("考古 115-3 P(7H)", 120 / 1024, 0.117)
check("習題 2.3 2^50", 2 ** 50, 1.13e15)
check("習題 2.3 Ω(25)", comb(50, 25), 1.26e14)
check("習題 2.3 P(25)", comb(50, 25) / 2 ** 50, 0.112)
check("習題 2.3 P(30)", comb(50, 30) / 2 ** 50, 0.0419)
check("習題 2.3 P(40)", comb(50, 40) / 2 ** 50, 9.1e-6)
check("習題 2.3 P(50)", 1 / 2 ** 50, 8.88e-16)

print("=== §2.2 愛因斯坦固體 ===")
for q, w in zip(range(4), [1, 3, 6, 10]):
    check(f"N=3 Ω({q})", ein(3, q), w)
for (N, q), w in {(3, 4): 15, (3, 5): 21, (3, 6): 28, (4, 2): 10, (4, 3): 20, (1, 7): 1, (9, 1): 9}.items():
    check(f"習題 2.5 Ω({N},{q})", ein(N, q), w)
# 用窮舉驗證 (2.9)
from itertools import product
for N, q in [(3, 4), (3, 6), (4, 3)]:
    cnt = sum(1 for t in product(range(q + 1), repeat=N) if sum(t) == q)
    check(f"窮舉 N={N}, q={q}", cnt, ein(N, q), 0)
check("習題 2.6 Ω(30,30)", ein(30, 30), 5.91e16)

print("=== §2.3 交互作用的系統 ===")
tab = [(qa, ein(3, qa), ein(3, 6 - qa)) for qa in range(7)]
check("Fig 2.4 Ω_total(qA=3)", tab[3][1] * tab[3][2], 100)
check("Fig 2.4 總數", sum(a * b for _, a, b in tab), 462)
check("Fig 2.4 C(11,6)", comb(11, 6), 462)
check("Fig 2.4 P(qA=3)", 100 / 462, 0.216)
check("Fig 2.4 P(qA=0)", 28 / 462, 0.0606)


def two(NA_, NB_, q):
    rows = [ein(NA_, a) * ein(NB_, q - a) for a in range(q + 1)]
    tot = sum(rows)
    return rows, tot


rows, tot = two(300, 200, 100)
check("Fig 2.5 Ω(qA=0)", rows[0], 2.8e81, 0.05)
imax = max(range(101), key=lambda i: rows[i])
check("Fig 2.5 最可能 qA", imax, 60, 0)
check("Fig 2.5 Ω_max", rows[60], 6.9e114, 0.03)
check("Fig 2.5 總數", tot, 9.3e115, 0.02)
check("Fig 2.5 P(qA=60)", rows[60] / tot, 0.074, 0.03)
check("Fig 2.5 Ω_max/Ω_min", rows[60] / rows[0], 2.5e33, 0.05)
check("Fig 2.5 Ω_max/Ω(qA=100)", rows[60] / rows[100], 4.1e18, 0.02)
check("Stirling N=1 誤差", 1 - sqrt(2 * pi) / e, 0.078, 0.01)
check("2.30 相對大小 27/2.77e23", 27.4 / 2.77e23, 1e-22, 0.02)
check("2.42 黑洞/太陽熵 10^77/10^58", 1.06e77 / 1e58, 1.06e19, 0.01)
check("Fig 2.5 精確 P(qA<10) / 課本上界", 1e-20 / (sum(rows[:10]) / tot), 122, 0.05)
p_out = (sum(rows[:30]) + sum(rows[91:])) / tot
print("    P(qA<30 或 >90) =", p_out, "（課本：小於百萬分之一）")
p10 = sum(rows[:10]) / tot
print("    P(qA<10) =", p10, "（課本：小於 1e-20）")
FAIL += [] if p_out < 1e-6 and p10 < 1e-20 else ["Fig 2.5 機率"]

# 習題 2.8
check("習題 2.8 總數", ein(20, 20), 6.89e10)
check("習題 2.8 Ω_A(10,20)", ein(10, 20), 1.00e7)
check("習題 2.8 P(全在 A)", ein(10, 20) / ein(20, 20), 1.45e-4)
check("習題 2.8 Ω(10,10)^2", ein(10, 10) ** 2, 8.53e9)
check("習題 2.8 P(各半)", ein(10, 10) ** 2 / ein(20, 20), 0.124)
# 習題 2.9
rows, tot = two(6, 4, 6)
check("習題 2.9 總數", tot, 5005, 0)
check("習題 2.9 最可能 qA=4", max(range(7), key=lambda i: rows[i]), 4, 0)
check("習題 2.9 P(qA=4)", rows[4] / tot, 0.252)
check("習題 2.9 P(qA=0)", rows[0] / tot, 0.0168)
# 習題 2.10
rows, tot = two(200, 100, 100)
i = max(range(101), key=lambda i: rows[i])
check("習題 2.10 最可能 qA", i, 67, 0)
check("習題 2.10 P(67)", rows[67] / tot, 0.073)
check("習題 2.10 P(0)", rows[0] / tot, 2.7e-38, 0.03)
# 習題 2.11 兩個順磁體 N=100, q=80
rows = [comb(100, a) * comb(100, 80 - a) for a in range(81)]
tot = sum(rows)
check("習題 2.11 總數 C(200,80)", tot, comb(200, 80), 0)
check("習題 2.11 P(40)", rows[40] / tot, 0.114)
check("習題 2.11 P(0)", rows[0] / tot, 3.3e-37, 0.03)
# 考古 115-5：N_A=10, N_B=20, q=60
rows, tot = two(10, 20, 60)
check("考古 115-5 總數 = C(89,60)", tot, comb(89, 60), 0)
check("考古 115-5 總數數值", tot, 2.244e23, 0.01)
pa = ein(10, 60) / tot
check("考古 115-5 C(69,60)", ein(10, 60), 5.67e10, 0.01)
check("考古 115-5 P(全在 A)", pa, 2.53e-13, 0.01)
imax = max(range(61), key=lambda i: rows[i])
check("考古 115-5 最可能 qA", imax, 19, 0)
check("考古 115-5 Ω_max", rows[19], 1.412e22, 0.01)
check("考古 115-5 P(最可能)", rows[19] / tot, 0.0629, 0.01)
check("考古 115-5 qA=20 比 19", rows[20] / rows[19], 0.991, 0.002)
# 考古 114-4：N_A=3, N_B=2, q=5
rows, tot = two(3, 2, 5)
print("    114-4 表：", [(a, ein(3, a), ein(2, 5 - a), rows[a]) for a in range(6)])
check("考古 114-4 總數", tot, 126, 0)
check("考古 114-4 C(9,5)", comb(9, 5), 126, 0)

print("=== §2.4 大數與 Stirling ===")
for N, ex, st, err in [(10, 3628800, 3598696, 0.0083), (100, factorial(100), 9.32e157, 0.00083)]:
    s = N ** N * exp(-N) * sqrt(2 * pi * N) if N < 150 else None
    check(f"Stirling N={N}", s, st, 0.001)
    check(f"Stirling 誤差 N={N}", 1 - s / ex, err, 0.03)
check("ln 10!", lnf(10), 15.10)
check("10 ln10 - 10", 10 * log(10) - 10, 13.03)
check("ln 100!", lnf(100), 363.74)
check("100ln100-100", 100 * log(100) - 100, 360.52)
check("習題 2.12 ln1.1", log(1.1), 0.0953)
check("習題 2.12 ln1.01", log(1.01), 0.00995)
check("習題 2.14 x", 1e23 / log(10), 4.34e22)
s50 = 50 ** 50 * exp(-50) * sqrt(100 * pi)
check("習題 2.15 50!", factorial(50), 3.0414e64, 0.0001)
check("習題 2.15 Stirling", s50, 3.0363e64, 0.0001)
check("習題 2.15 誤差", 1 - s50 / factorial(50), 0.00167, 0.01)
check("習題 2.15 ln50!", lnf(50), 148.48, 0.0005)
check("習題 2.15 50ln50-50", 50 * log(50) - 50, 145.60, 0.0005)
check("習題 2.15 ln 誤差", 1 - (50 * log(50) - 50) / lnf(50), 0.0194, 0.01)
p500 = comb(1000, 500) / 2 ** 1000
check("習題 2.16 P(500) 精確", p500, 0.02523, 0.001)
check("習題 2.16 P(500) Stirling", 1 / sqrt(500 * pi), 0.02523, 0.001)
p600 = comb(1000, 600) / 2 ** 1000
check("習題 2.16 P(600) 精確", p600, 4.63e-11, 0.01)
p600s = exp(600 * log(5 / 6) + 400 * log(5 / 4)) / sqrt(480 * pi)
check("習題 2.16 P(600) Stirling", p600s, 4.63e-11, 0.01)

print("=== §2.4 大愛因斯坦固體 ===")
# 精確 vs 近似：N=50, q=5000
N, q = 50, 5000
lex = log(ein(N, q))
check("N=50,q=5000 ln Ω 精確", lex, 273.02, 0.001)
check("ln (q+N)!/(q!N!)", lnf(q + N) - lnf(q) - lnf(N), 277.64, 0.001)
l218 = q * log((q + N) / q) + N * log((q + N) / N) - 0.5 * log(2 * pi * q * (q + N) / N)
check("習題 2.18 公式（含根號）", l218, lex, 0.0005)
check("(eq/N)^N 的 ln", N * log(e * q / N), 280.26, 0.001)
check("(2.20) N ln(q/N)+N+N²/q", N * log(q / N) + N + N * N / q, 280.76, 0.001)
# 低溫極限 N=5000, q=50（對稱）
check("低溫 (eN/q)^q 的 ln（N=5000, q=50）", 50 * log(e * 5000 / 50), 280.26, 0.001)
# 某級第 2 題 (b)：化學勢 μ = -kT ln((q+N)/N)（由 S = k[(q+N)ln(q+N) - q ln q - N ln N]）
dSdN = log(q + N) + 1 - log(N) - 1
check("μ/(-kT) = ln((q+N)/N)", dSdN, log((q + N) / N), 1e-9)
# 熵 Einstein 固體 N=1e22, q=1e24
S = 1e22 * k * (log(100) + 1)
check("§2.6 S/Nk", log(100) + 1, 5.6, 0.01)
check("§2.6 S", S, 0.77, 0.02)
# 習題 2.19：順磁體 N↓ ≪ N
N, Nd = 10 ** 6, 100
check("習題 2.19 ln C(N,N↓) vs N↓ ln(Ne/N↓)", log(comb(N, Nd)), Nd * log(N * e / Nd), 0.01)
check("習題 2.19 ln C(1e6,100)", log(comb(N, Nd)), 1017.8, 0.0005)
check("習題 2.19 差 = ½ln(2π·100)+N↓²/2N", Nd * log(N * e / Nd) - log(comb(N, Nd)), 0.5 * log(2 * pi * Nd) + Nd ** 2 / (2 * N), 0.01)
# 變化題
check("變化題 1 C(12,8)/2^12", comb(12, 8) / 2 ** 12, 0.121, 0.01)
rows_v = [ein(4, a) * ein(4, 4 - a) for a in range(5)]
check("變化題 2 總數", sum(rows_v), 330, 0)
check("變化題 2 P(2)", rows_v[2] / 330, 0.303, 0.01)
rows_v = [ein(20, a) * ein(10, 30 - a) for a in range(31)]
check("變化題 3 最可能 qA", max(range(31), key=lambda a: rows_v[a]), 21, 0)
check("變化題 3 P", rows_v[21] / sum(rows_v), 0.108, 0.01)
check("變化題 3 P(全在 A)", ein(20, 30) / sum(rows_v), 3.2e-4, 0.01)
check("變化題 6 R ln3", 8.314 * log(3), 9.13, 0.002)
check("變化題 7", 4 * 8.314 * -(0.25 * log(0.25) + 0.75 * log(0.75)), 18.7, 0.01)
check("變化題 8 0.9^1000", 0.9 ** 1000, 1.7e-46, 0.03)
check("變化題 9 2Nk ln2", 2e23 * k * log(2), 1.9, 0.02)
check("變化題 10 x/q", 1 / (2 * sqrt(1e4)), 0.005)
check("變化題 11 (5/2)R ln2", 2.5 * 8.314 * log(2), 14.4, 0.01)

print("=== §2.4 尖銳程度 ===")
check("寬度 q/(2√N) 的比例 N=1e20", 1 / (2 * sqrt(1e20)), 5e-11)
check("e^-100", exp(-100), 3.7e-44, 0.01)
check("習題 2.20 縮小倍數", 1e8 / 0.2, 5e8)
check("習題 2.20 峰寬", 0.01 / 5e8, 2e-11)
# 習題 2.22：N=1e23
N = 1e23
check("習題 2.22 寬度/總寬 √(π/2N)", sqrt(pi / (2 * N)), 3.96e-12, 0.01)
# 小 N 驗證：N=50，總數 = C(4N-1, 2N)，峰 = Ω(N,N)^2
N = 50
tot = ein(2 * N, 2 * N)
pk = ein(N, N) ** 2
check("習題 2.22 (b) N=50 公式/精確", 2 ** (4 * N) / sqrt(8 * pi * N) / tot, 1, 0.01)
check("習題 2.22 (c) N=50 公式/精確", 2 ** (4 * N) / (4 * pi * N) / pk, 1, 0.01)
check("習題 2.22 (d) N=50 寬度 √(2πN)", tot / pk, sqrt(2 * pi * N), 0.01)
# 習題 2.23
check("習題 2.23 √(πN/2) N=1e23", sqrt(pi * 1e23 / 2), 3.96e11, 0.01)
check("習題 2.23 探索數", 1e9 * 1e10 * 3.156e7, 3.16e26, 0.01)
check("習題 2.23 log10 Ω", 1e23 * log10(2), 3.01e22, 0.01)
# 考古 115-6（習題 2.24）：小 N 檢查
N = 1000
for x in [0, 10, 22]:
    exact = comb(N, N // 2 + x)
    approx = 2 ** N * sqrt(2 / (pi * N)) * exp(-2 * x * x / N)
    check(f"考古 115-6 Gaussian N=1000 x={x}", approx / exact, 1, 0.01)
check("考古 115-6 1/e 半寬 √(N/2) N=1000", sqrt(N / 2), 22.36)
# 習題 2.24(d)（變化題）：N=1e6
check("2.24(d) 半寬 √(N/2)", sqrt(1e6 / 2), 707)
check("2.24(d) x=1000 衰減", exp(-2 * 1000 ** 2 / 1e6), 0.135, 0.01)
check("2.24(d) x=10000 衰減 log10", -2 * 1e8 / 1e6 / log(10), -86.9, 0.01)
# 習題 2.25 隨機漫步
check("2.25 √N（rms）", sqrt(1e4), 100)
check("2.25 √(2N)", sqrt(2e4), 141.4, 0.001)
ell, dt = 1.5e-7, 3e-10
Nst = 1 / dt
check("2.25 一秒步數", Nst, 3.3e9, 0.02)
check("2.25 √(2N) ℓ（m）", sqrt(2 * Nst) * ell, 0.0122, 0.02)
# 某級第 3 題（d）與熵的峰
print("=== §2.5 理想氣體 ===")
check("半邊機率 N=100", 2.0 ** -100, 7.9e-31, 0.01)
check("習題 2.27 0.99^100", 0.99 ** 100, 0.366)
check("習題 2.27 0.99^10000", 0.99 ** 10000, 2.25e-44, 0.01)
check("習題 2.27 log10 0.99^1e23", 1e23 * log10(0.99), -4.36e20, 0.01)
# 超球面係數
from math import gamma
check("d=2 係數 2π", 2 * pi ** 1 / gamma(1), 2 * pi, 1e-9)
check("d=3 係數 4π", 2 * pi ** 1.5 / gamma(1.5), 4 * pi, 1e-9)
check("寬度 U/√(3N/2) 比例 N=1e20", 1 / sqrt(1.5e20), 8.2e-11, 0.01)

print("=== §2.6 熵 ===")
check("習題 2.28 52!", factorial(52), 8.07e67, 0.001)
check("習題 2.28 ln 52!", lnf(52), 156.4, 0.001)
check("習題 2.28 S", lnf(52) * k, 2.16e-21, 0.01)
rows, tot = two(300, 200, 100)
check("習題 2.29 S_max/k", log(rows[60]), 264.4, 0.001)
check("習題 2.29 S_min/k", log(rows[0]), 187.5, 0.001)
check("習題 2.29 S_all/k", log(tot), 267.0, 0.001)
N = 1e23
check("習題 2.30 4N ln2", 4 * N * log(2), 2.77e23, 0.001)
check("習題 2.30 ln√(8πN)", log(sqrt(8 * pi * N)), 28.1, 0.002)
check("習題 2.30 ln(4πN)", log(4 * pi * N), 55.5, 0.002)
check("習題 2.30 差", log(4 * pi * N) - log(sqrt(8 * pi * N)), 27.4, 0.002)
# Sackur–Tetrode：一莫耳氦（課本 V=0.025 m³、U=3700 J）
def st_arg(V, U, N, m):
    return V / N * (4 * pi * m * U / (3 * N * h * h)) ** 1.5


m_he = 4.0026 * u
arg = st_arg(0.025, 3700, NA, m_he)
check("He 對數裡的數", arg, 3.2e5, 0.01)
check("He ln", log(arg), 12.7, 0.01)
check("He S/Nk", log(arg) + 2.5, 15.2, 0.01)
check("He S", NA * k * (log(arg) + 2.5), 126, 0.01)
# 習題 2.33 氬（300 K、1e5 Pa）
T, P = 300, 1e5
m_ar = 39.948 * u
argA = (k * T / P) * (4 * pi * m_ar * 1.5 * k * T / (3 * h * h)) ** 1.5
check("Ar 對數裡的數", argA, 1.02e7, 0.02)
check("Ar S", 8.314 * (log(argA) + 2.5), 155, 0.01)
check("(40/4)^1.5", (39.948 / 4.0026) ** 1.5, 31.5, 0.01)
check("He 同條件 S", 8.314 * (log(argA / (39.948 / 4.0026) ** 1.5) + 2.5), 126, 0.01)
# 習題 2.35
n = P / (k * T)
T0 = (1 / n) ** (-2 / 3) * h * h / (2 * pi * e ** (5 / 3) * m_he * k)
check("習題 2.35 T", T0, 0.012, 0.02)
print("    T0 =", T0)
# 習題 2.36
check("2.36 書 Nk", 1000 / 12 * NA * k, 690, 0.05)
check("2.36 麋鹿 粒子數", 400e3 / 18 * NA, 1.3e28, 0.05)
check("2.36 太陽 粒子數", 2e30 / 1.67e-27 * 2, 2.4e57, 0.02)
# 習題 2.34 / 自由膨脹、混合
check("ln 2", log(2), 0.693, 0.001)
check("混合 2R ln2", 2 * 8.314 * log(2), 11.5, 0.01)
# 習題 2.39：可區分
check("2.39 ln(NA*arg)", log(NA * arg), 67.5, 0.002)
check("2.39 S", NA * k * (log(NA * arg) + 1.5), 573, 0.01)
check("2.39 倍數", (log(NA * arg) + 1.5) / (log(arg) + 2.5), 4.5, 0.02)
# 習題 2.37：x=1/2、x=0.25
check("2.37 x=1/2", -(0.5 * log(0.5) * 2), log(2), 1e-9)
check("2.37 x=0.25", -(0.25 * log(0.25) + 0.75 * log(0.75)), 0.562, 0.002)
# 習題 2.38：ln C(N,NA) vs Stirling，N=1000, NA=250
check("2.38 ln C(1000,250)/N", log(comb(1000, 250)) / 1000, 0.5591, 0.002)
# 習題 2.42 黑洞
G, c, M = 6.674e-11, 2.998e8, 2e30
check("2.42 GM/c²", G * M / c ** 2, 1485, 0.01)
check("2.42 GM²/(hc)", G * M ** 2 / (h * c), 1.34e75, 0.01)
check("2.42 S/k", 8 * pi ** 2 * G * M ** 2 / (h * c), 1.06e77, 0.01)
check("2.42 S", 8 * pi ** 2 * G * M ** 2 / (h * c) * k, 1.46e54, 0.02)
# 考古 114-3(d)(e) / 某級 1(j)：1/T = ∂S/∂U = (3/2)Nk/U
U, Nn = 3700.0, NA
dU = 1e-3
Sfun = lambda U_: Nn * k * (log(st_arg(0.025, U_, Nn, m_he)) + 2.5)
Tnum = dU / (Sfun(U + dU) - Sfun(U))
check("1/T=∂S/∂U ⇒ T = 2U/(3Nk)", Tnum, 2 * U / (3 * Nn * k), 0.001)
print("    He 的 T =", 2 * U / (3 * Nn * k), "K")

print()
print("ALL CHECKS PASSED" if not FAIL else "FAILED: " + ", ".join(FAIL))
