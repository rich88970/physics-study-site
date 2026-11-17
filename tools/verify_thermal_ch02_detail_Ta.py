"""熱學第 2 章第 1–5 節（01-two-state … 05-large-solid）詳解改寫後，新寫出的中間值與答案的獨立重算。

用法：python -X utf8 tools/verify_thermal_ch02_detail_Ta.py
大數用 Python 整數（精確）、math.lgamma（對數）；代數用 sympy。全部通過時最後印出 ALL CHECKS PASSED。
另外直接讀 sections/02-einstein.html，確認習題 2.5 列出的微觀態清單與窮舉完全相同。
"""
import itertools
import os
import re
import sys
from collections import Counter
from fractions import Fraction as F
from math import comb, e, exp, factorial, lgamma, log, log10, pi, sqrt

import sympy as sp

FAIL = []
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEC = os.path.join(ROOT, "subjects", "thermal", "ch02", "sections")


def check(name, got, want, rel=0.01):
    got, want = float(got), float(want)
    ok = abs(got - want) <= rel * abs(want) if want != 0 else abs(got) < 1e-12
    print(f"{'OK ' if ok else 'XX '} {name}: {got:.6g}（網站 {want:.6g}）")
    if not ok:
        FAIL.append(name)


def true(name, cond):
    print(f"{'OK ' if cond else 'XX '} {name}")
    if not cond:
        FAIL.append(name)


def ein(N, q):
    return comb(q + N - 1, q)


def lc(n, k):
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)


def ein_states(N, q):
    return [s for s in itertools.product(range(q + 1), repeat=N) if sum(s) == q]


print("=== 01 兩態系統 ===")
check("3coins 2^3", 2 ** 3, 8)
true("3coins Ω=1,3,3,1", [comb(3, n) for n in (3, 2, 1, 0)] == [1, 3, 3, 1])
check("100coins 1.024^10", 1.024 ** 10, 1.268, 0.001)
check("100coins 2^100", 2 ** 100, 1.27e30, 0.005)
check("100coins 100·99/2", 100 * 99 // 2, 4950)
check("100coins 100·99·98", 100 * 99 * 98, 970200)
check("100coins Ω(3)", comb(100, 3), 161700)
check("100coins Ω(50)", comb(100, 50), 1.01e29, 0.005)
check("100coins P(50)", comb(100, 50) / 2 ** 100, 0.080, 0.006)
true("4coins C(4,n)=1,4,6,4,1 且 24/(0!4!) 等", [comb(4, n) for n in range(5)] == [1, 4, 6, 4, 1] and factorial(4) == 24)
cnt4 = Counter(s.count("H") for s in ("".join(p) for p in itertools.product("HT", repeat=4)))
true("4coins 窮舉分組", [cnt4[n] for n in (4, 3, 2, 1, 0)] == [1, 4, 6, 4, 1])
check("20coins 1024^2", 1024 ** 2, 1048576)
check("20coins P(序列)", 1 / 2 ** 20, 9.54e-7, 0.002)
true("20coins 序列有 12 正 8 反", "HTHHTTTHTHHHTHHHHTHT".count("H") == 12)
check("20coins 20·19·…·13", 20 * 19 * 18 * 17 * 16 * 15 * 14 * 13, 5079110400)
check("20coins 8!", factorial(8), 40320)
check("20coins Ω(12)", 5079110400 // 40320, 125970)
check("20coins P(12)", 125970 / 2 ** 20, 0.120, 0.003)
check("10coins 2^10", 2 ** 10, 1024)
check("10coins P(序列)", 1 / 1024, 9.77e-4, 0.001)
check("10coins 720/6", 10 * 9 * 8 / 6, 120)
check("10coins P(7)", 120 / 1024, 0.117, 0.003)
check("50coins 2^50", 2 ** 50, 1.126e15, 0.001)
check("50coins Ω(25)", comb(50, 25), 1.264e14, 0.001)
check("50coins P(25)", comb(50, 25) / 2 ** 50, 0.112, 0.003)
check("50coins C(50,20)", comb(50, 20), 4.71e13, 0.002)
check("50coins P(30)", comb(50, 20) / 2 ** 50, 0.042, 0.01)
check("50coins C(50,10)", comb(50, 10), 1.03e10, 0.003)
check("50coins P(40)", comb(50, 10) / 2 ** 50, 9.1e-6, 0.01)
check("50coins P(50)", 1 / 2 ** 50, 8.9e-16, 0.005)
check("poker 52·51·50·49·48", 52 * 51 * 50 * 49 * 48, 311875200)
check("poker C(52,5)", 311875200 // 120, 2598960)
check("poker 1/649740", 2598960 / 4, 649740)
check("poker P", 4 / 2598960, 1.54e-6, 0.003)
check("poker 依序", F(20, 52) * F(4, 51) * F(3, 50) * F(2, 49) * F(1, 48), 4 / 2598960, 1e-12)
# sf-01a
Nu, Nd = sp.symbols("Nu Nd")
sol = sp.solve([Nd - Nu + 2, Nu + Nd - 6], [Nu, Nd])
true("sf01a N↑=4, N↓=2", sol[Nu] == 4 and sol[Nd] == 2)
check("sf01a 720/(24·2)", 720 / 48, 15)
check("sf01a P(1↑)", F(comb(5, 3), comb(6, 4)), 2 / 3, 1e-12)
check("sf01a P(1↑2↑)", F(comb(4, 2), 15), 0.400, 1e-12)
check("sf01a (2/3)^2", 4 / 9, 0.444, 0.002)
true("sf01a 一般式 C(N-2,N↑-2)/C(N,N↑)=N↑(N↑-1)/[N(N-1)]",
     all(F(comb(N - 2, k - 2), comb(N, k)) == F(k * (k - 1), N * (N - 1)) for N, k in ((6, 4), (600, 400), (37, 11))))
check("sf01a 400·399", 400 * 399, 159600)
check("sf01a 600·599", 600 * 599, 359400)
check("sf01a P 大系統", 159600 / 359400, 0.4441, 0.0002)
check("sf01a 相對差", 200 / (400 * 599), 8.3e-4, 0.01)
N_, k_ = sp.symbols("N k", positive=True)
true("sf01a 通分化簡", sp.simplify(1 - N_ * (k_ - 1) / (k_ * (N_ - 1)) - (N_ - k_) / (k_ * (N_ - 1))) == 0)
# sf-01b
check("sf01b 51/50", F(comb(100, 50), comb(100, 51)), 1.02, 1e-12)
check("sf01b C(100,50)", comb(100, 50), 1.0089e29, 0.0002)
check("sf01b C(100,49)", comb(100, 49), 9.891e28, 0.0002)
check("sf01b C(100,48)", comb(100, 48), 9.321e28, 0.0002)
s5 = sum(comb(100, n) for n in range(48, 53))
check("sf01b Σ48..52", s5, 4.851e29, 0.0003)
check("sf01b 2^100", 2 ** 100, 1.2677e30, 0.0001)
check("sf01b P(|M|≤5μ)", s5 / 2 ** 100, 0.383, 0.002)
check("sf01b P(M=0)", comb(100, 50) / 2 ** 100, 0.0796, 0.001)
check("sf01b C(100,47)", comb(100, 47), 8.441e28, 0.0002)
check("sf01b C(100,46)", comb(100, 46), 7.347e28, 0.0002)
check("sf01b C(100,45)", comb(100, 45), 6.145e28, 0.0002)
check("sf01b 三對", 2 * (comb(100, 47) + comb(100, 46) + comb(100, 45)), 4.387e29, 0.0003)
s10 = sum(comb(100, n) for n in range(45, 56))
check("sf01b Σ45..55", s10, 9.238e29, 0.0003)
check("sf01b P(|M|≤10μ)", s10 / 2 ** 100, 0.729, 0.002)

print("=== 02 愛因斯坦固體 ===")
true("ein3 Ω(3,q)=1,3,6,10", [ein(3, q) for q in range(4)] == [1, 3, 6, 10] == [len(ein_states(3, q)) for q in range(4)])
pat = Counter(tuple(sorted(s, reverse=True)) for s in ein_states(3, 3))
true("ein3 q=3 型態 3,6,1", pat[(3, 0, 0)] == 3 and pat[(2, 1, 0)] == 6 and pat[(1, 1, 1)] == 1)
want25 = {(3, 4): {(4, 0, 0): 3, (3, 1, 0): 6, (2, 2, 0): 3, (2, 1, 1): 3},
          (3, 5): {(5, 0, 0): 3, (4, 1, 0): 6, (3, 2, 0): 6, (3, 1, 1): 3, (2, 2, 1): 3},
          (3, 6): {(6, 0, 0): 3, (5, 1, 0): 6, (4, 2, 0): 6, (4, 1, 1): 3, (3, 3, 0): 3, (3, 2, 1): 6, (2, 2, 2): 1},
          (4, 2): {(2, 0, 0, 0): 4, (1, 1, 0, 0): 6},
          (4, 3): {(3, 0, 0, 0): 4, (2, 1, 0, 0): 12, (1, 1, 1, 0): 4}}
for (N, q), w in want25.items():
    pat = Counter(tuple(sorted(s, reverse=True)) for s in ein_states(N, q))
    true(f"2.5 N={N},q={q} 型態排法 {dict(w)}", dict(pat) == w and sum(w.values()) == ein(N, q))
# 2.5：網站列出的微觀態清單與窮舉相同
html = open(os.path.join(SEC, "02-einstein.html"), encoding="utf-8").read()


def step_text(sid):
    m = re.search(r'data-step="%s"[^>]*>(.*?)(?=<div class="step"|<div class="part result")' % sid, html, re.S)
    return m.group(1)


for sid, (N, q) in (("t25a", (3, 4)), ("t25b", (3, 5)), ("t25c", (3, 6))):
    listed = re.findall(r"(?<![\d.])(\d{3})(?![\d.])", re.sub(r"\$[^$]*\$", "", step_text(sid)))
    brute = sorted("".join(map(str, s)) for s in ein_states(N, q))
    true(f"2.5 {sid} 清單＝窮舉（{len(brute)} 個）", sorted(listed) == brute)
t = re.sub(r"\$[^$]*\$", "", step_text("t25d"))
listed = re.findall(r"(?<![\d.])(\d{4})(?![\d.])", t)
brute = sorted("".join(map(str, s)) for s in ein_states(4, 2)) + sorted("".join(map(str, s)) for s in ein_states(4, 3))
true("2.5 t25d 清單＝窮舉（10+20 個）", sorted(listed) == sorted(brute))
listed = re.findall(r"(?<![\d.])(\d{3})(?![\d.])", re.sub(r"\$[^$]*\$", "", step_text("te3a")))
true("ein3 清單＝窮舉（q=0..3 共 20 個）", sorted(listed) == sorted("".join(map(str, s)) for qq_ in range(4) for s in ein_states(3, qq_)))
html1 = open(os.path.join(SEC, "01-two-state.html"), encoding="utf-8").read()
for sid, n in (("t3ca", 3), ("t21a", 4)):
    m = re.search(r'data-step="%s"[^>]*>(.*?)(?=<div class="step")' % sid, html1, re.S)
    listed = re.findall(r"(?<![HT])([HT]{%d})(?![HT])" % n, m.group(1))
    true(f"{sid} 列出 {2 ** n} 個硬幣微觀態、不重複", sorted(listed) == sorted("".join(p) for p in itertools.product("HT", repeat=n)))
true("2.5 (f)(g)", all(ein(1, q) == 1 for q in range(20)) and all(ein(N, 1) == N for N in range(1, 20)))
check("2.6 Ω(30,30)", comb(59, 30), 5.91e16, 0.002)
check("2.6 log10 59!", lgamma(60) / log(10), 80.1420, 1e-5)
check("2.6 log10 30!", lgamma(31) / log(10), 32.4237, 1e-5)
check("2.6 log10 29!", lgamma(30) / log(10), 30.9465, 1e-5)
check("2.6 log10 Ω", log10(comb(59, 30)), 16.7718, 1e-5)
check("2.6 10^0.7718", 10 ** 0.7718, 5.91, 0.002)
check("2.7 C(5,2)", comb(5, 2), 10)
true("2.7 4+6", sum(1 for s in ein_states(4, 2) if max(s) == 2) == 4 and sum(1 for s in ein_states(4, 2) if max(s) == 1) == 6)
true("sf02a P(n)=(5-n)/15", all(F(ein(2, 4 - n), ein(3, 4)) == F(5 - n, 15) for n in range(5)))
check("sf02a <n>", sum(F(n * (5 - n), 15) for n in range(5)), 4 / 3, 1e-12)
true("sf02a 比值 m/(m+N-2)", all(F(ein(N - 1, m - 1), ein(N - 1, m)) == F(m, m + N - 2) for N in (3, 10, 1000) for m in (1, 5, 1000)))
check("sf02a N=q=1000 P(0)", F(ein(999, 1000), ein(1000, 1000)), 999 / 1999, 1e-12)
check("sf02a N=q=1000 P(1)/P(0)", F(ein(999, 999), ein(999, 1000)), 1000 / 1998, 1e-12)
true("sf02b Ω(2,q)=q+1、Ω(3,q)=(q+1)(q+2)/2", all(ein(2, q) == q + 1 and ein(3, q) == (q + 1) * (q + 2) // 2 for q in range(30)))
true("sf02b 遞迴式", all(ein(N, q) == sum(ein(N - 1, q - n) for n in range(q + 1)) for N in range(2, 8) for q in range(12)))
true("sf02b Σ C(m+N-2,m)=C(q+N-1,q)", all(sum(comb(m + N - 2, m) for m in range(q + 1)) == comb(q + N - 1, q) for N in range(2, 9) for q in range(15)))

print("=== 03 交互作用的系統 ===")
row = [ein(3, a) * ein(3, 6 - a) for a in range(7)]
true("fig24 表", row == [28, 63, 90, 100, 90, 63, 28] and sum(row) == comb(11, 6) == 462)
check("fig24 P(3)", 100 / 462, 0.216, 0.003)
check("fig24 P(0)", 28 / 462, 0.061, 0.01)
w25 = [ein(300, a) * ein(200, 100 - a) for a in range(101)]
true("fig25 峰 60、谷 0", max(range(101), key=lambda a: w25[a]) == 60 and min(range(101), key=lambda a: w25[a]) == 0)
check("fig25 C(299,100)", comb(299, 100), 2.8e81, 0.02)
check("fig25 C(359,60)", comb(359, 60), 1.30e69, 0.003)
check("fig25 C(239,40)", comb(239, 40), 5.27e45, 0.002)
check("fig25 Ω(60)", w25[60], 6.9e114, 0.01)
check("fig25 Ω(100)", w25[100], 1.7e96, 0.02)
check("fig25 峰/谷", w25[60] / w25[0], 2.5e33, 0.02)
check("fig25 C(599,100)", comb(599, 100), 9.3e115, 0.005)
check("fig25 P(60)", w25[60] / comb(599, 100), 0.074, 0.005)
check("fig25 P(0)", w25[0] / comb(599, 100), 3e-35, 0.02)
check("2.8 C(39,20)", comb(39, 20), 6.89e10, 0.001)
check("2.8 C(29,9)", comb(29, 9), 10015005)
check("2.8 P(全在A)", comb(29, 9) / comb(39, 20), 1.45e-4, 0.003)
check("2.8 C(19,10)", comb(19, 10), 92378)
check("2.8 平方", comb(19, 10) ** 2, 8.53e9, 0.001)
check("2.8 P(一半)", comb(19, 10) ** 2 / comb(39, 20), 0.124, 0.002)
check("2.8 比值", comb(19, 10) ** 2 / comb(29, 9), 850, 0.01)
check("115-5 C(89,60)", comb(89, 60), 2.24e23, 0.002)
check("115-5 C(69,9)", comb(69, 9), 5.67e10, 0.001)
check("115-5 P(全在A)", comb(69, 60) / comb(89, 60), 2.5e-13, 0.02)
qa = sp.symbols("q_A")
true("115-5 展開", sp.expand((qa + 10) * (60 - qa)) == -qa ** 2 + 50 * qa + 600 and sp.expand((qa + 1) * (79 - qa)) == -qa ** 2 + 78 * qa + 79)
check("115-5 521/28", 521 / 28, 18.6, 0.002)
w = [ein(10, a) * ein(20, 60 - a) for a in range(61)]
true("115-5 峰在 19", max(range(61), key=lambda a: w[a]) == 19 and w[19] > w[18] and w[19] > w[20])
check("115-5 C(28,19)", comb(28, 19), 6.91e6, 0.001)
check("115-5 C(60,41)", comb(60, 41), 2.04e15, 0.003)
check("115-5 乘積", comb(28, 19) * comb(60, 41), 1.41e22, 0.003)
check("115-5 P(19)", w[19] / comb(89, 60), 0.063, 0.005)
row = [ein(3, a) * ein(2, 5 - a) for a in range(6)]
true("114-4 表與總和", row == [6, 15, 24, 30, 30, 21] and sum(row) == comb(9, 5) == 126)
check("114-4 P(3)", 30 / 126, 0.24, 0.01)
check("114-4 P(0)", 6 / 126, 0.048, 0.01)
row = [ein(6, a) * ein(4, 6 - a) for a in range(7)]
true("2.9 表", row == [84, 336, 735, 1120, 1260, 1008, 462] and sum(row) == comb(15, 6) == 5005 and comb(8, 3) * comb(6, 3) == 1120)
check("2.9 P(4)", 1260 / 5005, 0.252, 0.002)
check("2.9 P(0)", 84 / 5005, 0.017, 0.02)
check("2.10 q*", (199 * 100 - 99) / 298, 66.4, 0.002)
w = [ein(200, a) * ein(100, 100 - a) for a in range(101)]
true("2.10 峰 67、谷 0", max(range(101), key=lambda a: w[a]) == 67 and min(range(101), key=lambda a: w[a]) == 0)
check("2.10 C(399,100)", comb(399, 100), 1.68e96, 0.002)
check("2.10 C(266,67)", comb(266, 67), 8.91e63, 0.002)
check("2.10 C(132,33)", comb(132, 33), 1.38e31, 0.002)
check("2.10 Ω(67)", w[67], 1.23e95, 0.002)
check("2.10 P(67)", w[67] / comb(399, 100), 0.073, 0.005)
check("2.10 C(199,100)", comb(199, 100), 4.53e58, 0.002)
check("2.10 P(0)", w[0] / comb(399, 100), 2.7e-38, 0.01)
check("2.10 C(299,100)", w[100], 2.8e81, 0.02)
w = [comb(100, a) * comb(100, 80 - a) for a in range(81)]
true("2.11 Vandermonde", sum(w) == comb(200, 80))
true("2.11 峰 40", max(range(81), key=lambda a: w[a]) == 40)
check("2.11 C(200,80)", comb(200, 80), 1.65e57, 0.003)
check("2.11 C(100,40)", comb(100, 40), 1.375e28, 0.001)
check("2.11 C(100,40)^2", comb(100, 40) ** 2, 1.89e56, 0.002)
check("2.11 P(40)（原寫 11.4%，正確 11.5%）", w[40] / comb(200, 80), 0.115, 0.003)
check("2.11 C(100,20)", comb(100, 20), 5.4e20, 0.01)
check("2.11 P(0)", w[0] / comb(200, 80), 3.3e-37, 0.02)
check("sf03a 29701/498", 29701 / 498, 59.64, 0.0002)
true("sf03a (b) 展開", sp.expand((qa + 300) * (100 - qa)) == -qa ** 2 - 200 * qa + 30000 and sp.expand((qa + 1) * (299 - qa)) == -qa ** 2 + 298 * qa + 299)
NA, NB, q = sp.symbols("N_A N_B q")
qs = sp.solve(sp.Eq((NA - 1) * (q - qa), (NB - 1) * (qa + 1)), qa)[0]
true("sf03a 一般解", sp.simplify(qs - ((NA - 1) * q - (NB - 1)) / (NA + NB - 2)) == 0)
true("sf03a 比值公式", all(F(ein(N, k + 1), ein(N, k)) == F(k + N, k + 1) for N in (3, 50) for k in (0, 7, 40)))
check("sf03a Fig2.4 q*", (2 * 6 - 2) / 4, 2.5)
rowA = [ein(3, a) * comb(3, 3 - a) for a in range(4)]
rowB = [ein(3, a) * comb(3, 6 - a) for a in range(3, 7)]
true("sf03b 表", rowA == [1, 9, 18, 10] and rowB == [10, 45, 63, 28] and sum(rowA) == 38 and sum(rowB) == 146)
check("sf03b P q=3", 18 / 38, 0.474, 0.002)
check("sf03b P q=6", 63 / 146, 0.432, 0.002)
check("sf03b <qB> q=3", F(3 * 1 + 2 * 9 + 18, 38), 1.03, 0.005)
check("sf03b <qB> q=6", F(3 * 10 + 2 * 45 + 63, 146), 1.25, 0.003)


def mean_qB(qt):
    ws = [(b, ein(3, qt - b) * comb(3, b)) for b in range(min(3, qt) + 1)]
    return F(sum(b * x for b, x in ws), sum(x for _, x in ws))


true("sf03b 有限 q 時 <qB> < 1.5，且趨近 1.5", all(mean_qB(t) < F(3, 2) for t in range(3, 400)) and abs(float(mean_qB(10 ** 6)) - 1.5) < 1e-5)

print("=== 04 很大的數與 Stirling ===")
check("stirling e^-10", exp(-10), 4.540e-5, 0.0002)
check("stirling sqrt(20π)", sqrt(20 * pi), 7.927, 0.0002)
check("stirling N=10 近似", 10 ** 10 * exp(-10) * sqrt(20 * pi), 3598696, 1e-6)
check("stirling N=10 誤差", 1 - 3598696 / 3628800, 0.0083, 0.01)
check("stirling N=1", exp(-1) * sqrt(2 * pi), 0.922, 0.001)
check("stirling N=1 誤差", 1 - exp(-1) * sqrt(2 * pi), 0.078, 0.01)
check("stirling N=100 誤差", 1 - exp(100 * log(100) - 100 + 0.5 * log(200 * pi) - lgamma(101)), 0.00083, 0.01)
check("stirling ln10!", lgamma(11), 15.104, 0.0001)
check("stirling 10ln10-10", 10 * log(10) - 10, 13.026, 0.0001)
check("stirling (2.16) N=10 誤差", (lgamma(11) - 13.026) / lgamma(11), 0.138, 0.003)
check("stirling (2.16) N=100 誤差", (lgamma(101) - (100 * log(100) - 100)) / lgamma(101), 0.0089, 0.01)
check("2.12 ln1.1", log(1.1), 0.0953, 0.001)
check("2.12 高估 x=0.1", (0.1 - log(1.1)) / log(1.1), 0.049, 0.01)
check("2.12 ln1.01", log(1.01), 0.00995, 0.001)
check("2.12 高估 x=0.01", (0.01 - log(1.01)) / log(1.01), 0.0050, 0.01)
x = sp.symbols("x")
true("2.12 ln(1+x) 的下一項 -x^2/2", sp.series(sp.log(1 + x), x, 0, 3).removeO() == x - x ** 2 / 2)
check("2.13 ln101", log(101), 4.6151, 0.00002)
check("2.13 ln100+0.01", log(100) + 0.01, 4.6152, 0.00002)
check("2.14 x", 1e23 / log(10), 4.34e22, 0.001)
check("2.15 50log50", 50 * log10(50), 84.9485, 1e-6)
check("2.15 -50log e", -50 * log10(e), -21.7147, 1e-5)
check("2.15 ½log(100π)", 0.5 * log10(100 * pi), 1.2486, 1e-4)
check("2.15 總指數", 84.9485 - 21.7147 + 1.2486, 64.4824, 1e-6)
check("2.15 Stirling 值", 50 ** 50 * exp(-50) * sqrt(100 * pi), 3.0363e64, 0.0001)
check("2.15 50!", factorial(50), 3.0414e64, 0.0001)
check("2.15 誤差", 1 - 50 ** 50 * exp(-50) * sqrt(100 * pi) / factorial(50), 0.0017, 0.03)
check("2.15 50ln50", 50 * log(50), 195.601, 1e-5)
check("2.15 ln50!", lgamma(51), 148.478, 1e-5)
check("2.15 對數誤差", (lgamma(51) - (50 * log(50) - 50)) / lgamma(51), 0.019, 0.03)
true("2.16 根號化簡", sp.simplify(sp.sqrt(2000 * sp.pi) / (1000 * sp.pi) - 1 / sp.sqrt(500 * sp.pi)) == 0
     and sp.simplify(sp.sqrt(2000 * sp.pi) / (sp.sqrt(1200 * sp.pi) * sp.sqrt(800 * sp.pi)) - 1 / sp.sqrt(480 * sp.pi)) == 0)
check("2.16 sqrt(500π)", sqrt(500 * pi), 39.63, 0.0002)
check("2.16 P(500)", 1 / sqrt(500 * pi), 0.0252, 0.002)
check("2.16 ln5/6", log(5 / 6), -0.18232, 1e-4)
check("2.16 ln5/4", log(5 / 4), 0.22314, 1e-4)
check("2.16 ln480π", log(480 * pi), 7.3185, 1e-4)
check("2.16 ln P", 600 * log(5 / 6) + 400 * log(5 / 4) - 0.5 * log(480 * pi), -23.795, 1e-4)
check("2.16 P(600)", exp(-23.795), 4.6e-11, 0.01)
check("2.16 精確 P(600)", comb(1000, 600) / 2 ** 1000, 4.63e-11, 0.002)
Nn = sp.symbols("N", positive=True)
st = lambda m: m ** m * sp.exp(-m) * sp.sqrt(2 * sp.pi * m)
true("sf04a C(2N,N)≈4^N/√(πN)", sp.simplify(st(2 * Nn) / st(Nn) ** 2 - 4 ** Nn / sp.sqrt(sp.pi * Nn)) == 0)
check("sf04a sqrt(50π)", sqrt(50 * pi), 12.53, 0.0005)
check("sf04a P N=50", 1 / sqrt(50 * pi), 0.0798, 0.001)
check("sf04a 精確 N=50", comb(100, 50) / 2 ** 100, 0.0796, 0.001)
check("sf04a 10^4/π", 1e4 / pi, 3183.1, 0.00002)
check("sf04a 精確 N=3183", comb(6366, 3183) / 4 ** 3183, 0.0099998, 1e-5)
true("sf04a N=3183 低於 1%、N=3182 高於 1%", comb(6366, 3183) * 100 < 4 ** 3183 < comb(6364, 3182) * 100 * 4)
check("sf04a 精確 N=3182", comb(6364, 3182) / 4 ** 3182, 0.0100013, 1e-5)
check("sf04a Stirling N=3183", 1 / sqrt(pi * 3183), 0.0100002, 1e-5)
check("sf04b log10 A", 1e23 * (23 - log10(e)), 2.257e24, 0.0003)
check("sf04b log10 C", 1e23 * 24, 2.400e24, 1e-9)
check("sf04b log10 A/C", 1e23 * (23 - log10(e) - 24), -1.434e23, 0.0003)
check("sf04b log10(A·10^10^23)", 2.257e24 + 1e23, 2.357e24, 1e-6)
check("sf04b 根號項 ½log10(2π·10^23)", 0.5 * log10(2 * pi * 1e23), 12, 0.03)

print("=== 05 大愛因斯坦固體 ===")
qq, NN = sp.symbols("q N", positive=True)
true("115-4 根號化簡", sp.simplify((NN / (qq + NN) * sp.sqrt(2 * sp.pi * (qq + NN)) / (sp.sqrt(2 * sp.pi * qq) * sp.sqrt(2 * sp.pi * NN))) ** 2
                                  - NN / (2 * sp.pi * qq * (qq + NN))) == 0)
true("115-4 e 的次方抵消", sp.simplify(-(qq + NN) + qq + NN) == 0)
N, q = 50, 5000
exact = lc(q + N - 1, q)
f218 = (q + N) * log(q + N) - q * log(q) - N * log(N)
sq = 0.5 * log(2 * pi * q * (q + N) / N)
check("115-4 精確 lnΩ(50,5000)", exact, 273.02, 0.0001)
check("115-4 (a) 公式", f218 - sq, 273.02, 0.0001)
check("115-4 (2.21)", N * log(q / N) + N, 280.26, 0.0001)
check("115-4 根號項", sq, 7.49, 0.002)
check("115-4 差 7.24", N * log(q / N) + N - exact, 7.24, 0.003)
check("115-4 熵中省略項估計", 0.5 * log(2 * pi * 1e23 * 2e23 / 1e23), 28, 0.02)
S = (qq + NN) * sp.log(qq + NN) - qq * sp.log(qq) - NN * sp.log(NN)
true("tkx-2 ∂S/∂N = ln((q+N)/N)", sp.simplify(sp.diff(S, NN) - sp.log((qq + NN) / NN)) == 0)
Shi = NN * (sp.log(qq) - sp.log(NN) + 1)
true("tkx-2 高溫 ∂S/∂q = N/q", sp.simplify(sp.diff(Shi, qq) - NN / qq) == 0)
Slo = qq * sp.log(NN) - qq * sp.log(qq) + qq
true("tkx-2 低溫 ∂S/∂q = ln(N/q)", sp.simplify(sp.diff(Slo, qq) - sp.log(NN / qq)) == 0)
T, k, eps = sp.symbols("T k epsilon", positive=True)
U = NN * eps * sp.exp(-eps / (k * T))
true("tkx-2 低溫 C_V", sp.simplify(sp.diff(U, T) - NN * k * (eps / (k * T)) ** 2 * sp.exp(-eps / (k * T))) == 0)
true("2.19 (1-x)ln(1-x) = -x + x^2/2 + O(x^3)", sp.series((1 - x) * sp.log(1 - x), x, 0, 3).removeO() == -x + x ** 2 / 2)
check("2.19 ln C(10^6,100)", lc(10 ** 6, 100), 1017.8, 0.0001)
check("2.19 100 ln(10^6 e/100)", 100 * log(1e6 * e / 100), 1021.0, 0.0001)
check("2.19 差", 0.5 * log(2 * pi * 100) + 100 ** 2 / (2 * 10 ** 6), 3.2, 0.01)
r = sp.symbols("r", positive=True)
g = (1 + r) * sp.log(1 + r) - r * sp.log(r)
ser = sp.series(g.subs(r, 1 / x), x, 0, 3).removeO()
true("sf05a 大 r 展開 = ln r + 1 + 1/(2r) - 1/(6r^2)", sp.simplify(sp.expand_log(ser - (-sp.log(x) + 1 + x / 2 - x ** 2 / 6), force=True)) == 0)
true("sf05a (b) (q+N)[N/q-(N/q)^2/2] = N + N^2/(2q) - N^3/(2q^2)",
     sp.simplify((qq + NN) * (NN / qq - (NN / qq) ** 2 / 2) - NN - NN ** 2 / (2 * qq) + NN ** 3 / (2 * qq ** 2)) == 0)
check("sf05a 50(ln100+1)", 50 * (log(100) + 1), 280.26, 0.00002)
check("sf05a N^2/2q", 2500 / 10000, 0.25)
check("sf05a (2.18)", f218, 280.51, 0.00002)
check("sf05a (2.20)", N * log(q / N) + N + N * N / q, 280.76, 0.00002)
gf = lambda t: (1 + t) * log(1 + t) - t * log(t)
lo, hi = 1.0, 100.0
for _ in range(80):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if (gf(m) - (log(m) + 1)) / gf(m) > 0.01 else (lo, m)
check("sf05a 完整解 r", lo, 13.4, 0.003)
check("sf05a 近似解 r(ln r+1)=50", 13.8 * (log(13.8) + 1), 50.0, 0.001)
check("sf05a q=N 低估", (2 * log(2) - 1) / (2 * log(2)), 0.28, 0.01)
check("sf05b (a) 精確", (1e20 + 1e22) / (1e20 + 1), 101, 1e-9)
check("sf05b (a) 低溫公式", (1e22 / 1e20), 100)
check("sf05b (a) (1+1/q)^-(q+1)→1/e", (1 + 1 / 1e6) ** (-(1e6 + 1)), exp(-1), 1e-5)
check("sf05b (b) 精確", (1e24 + 1e22) / (1e24 + 1), 1.01, 1e-9)
check("sf05b (b) 高溫公式 e^0.01", exp(0.01), 1.01, 0.0001)
check("sf05b (c)", 101 / 1.01, 100, 1e-9)
check("sf05b ln101", log(101), 4.62, 0.002)
check("sf05b kT_A", 1 / log(101), 0.22, 0.02)
check("sf05b ln1.01", log(1.01), 0.00995, 0.001)
check("sf05b kT_B", 1 / log(1.01), 100, 0.006)
check("sf05b ln100", log(100), 4.61, 0.002)

print()
if FAIL:
    print("FAILED:", *FAIL, sep="\n  ")
    sys.exit(1)
print("ALL CHECKS PASSED")
