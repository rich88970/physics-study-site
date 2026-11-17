"""熱學第 2 章：考古題盤點（2026-10-21）新增卡片與別名卡片的數值驗算。

python tools/verify_thermal_ch02_exams.py
- tk-114-5：114 級上學期期中第 5 題（Schroeder Problem 3.28）一公升空氣定壓加熱到兩倍體積的熵增加。
- 熱學小考（上）作業題：用小考答案卷上的數字對照網站既有卡片的答案（sc-2-8、2-22、2-27、2-30、2-42）。
"""
import math
import sympy as sp

fails = 0


def check(name, got, want, rtol=5e-3):
    global fails
    ok = abs(got - want) <= rtol * abs(want)
    print(("PASS" if ok else "FAIL"), name, f"got={got:.6g}", f"want={want:.6g}")
    if not ok:
        fails += 1


# ---------- tk-114-5 ----------
# 一般式：Omega ∝ V^N U^(fN/2) ⇒ ΔS = Nk ln(Vf/Vi) + (f/2) Nk ln(Uf/Ui)
N, k, f, V, U, P = sp.symbols("N k f V U P", positive=True)
S = N * k * sp.log(V) + f / 2 * N * k * sp.log(U)
# 定壓：T = PV/(Nk) ∝ V，U = (f/2) N k T ⇒ U ∝ V
Ti = sp.symbols("T_i", positive=True)
Ui = f / 2 * N * k * Ti
Uf = f / 2 * N * k * (2 * Ti)        # T_f = 2 T_i
dS = sp.simplify(S.subs({V: 2 * V, U: Uf}) - S.subs({U: Ui}))
want = sp.Rational(7, 2) * N * k * sp.log(2)
assert sp.simplify(dS.subs(f, 5) - want) == 0, dS
print("PASS tk-114-5 symbolic: ΔS = (1+f/2) Nk ln2 → 7/2 Nk ln2 for f=5")

# 第 3 章做法：ΔS = ∫ C_P dT / T，C_P = (f/2+1) Nk
T = sp.symbols("T", positive=True)
CP = (sp.Rational(5, 2) + 1) * N * k
dS3 = sp.integrate(CP / T, (T, Ti, 2 * Ti))
assert sp.simplify(dS3 - want) == 0
print("PASS tk-114-5 check: ∫C_P dT/T gives the same 7/2 Nk ln2")

Pn, Vi, Tin, kB = 1.013e5, 1.0e-3, 300.0, 1.38e-23
Nk = Pn * Vi / Tin
check("tk-114-5 Nk = PV/T (J/K)", Nk, 0.338)
dSn = 3.5 * Nk * math.log(2)
check("tk-114-5 ΔS (J/K), P=1.013e5", dSn, 0.82, rtol=6e-3)
check("tk-114-5 ΔS (J/K), P=1e5 (課本解答 0.81)", 3.5 * (1e5 * Vi / Tin) * math.log(2), 0.81, rtol=6e-3)
check("tk-114-5 ΔS/k", dSn / kB, 5.9e22, rtol=1e-2)
check("tk-114-5 monatomic mistake 5/2 Nk ln2", 2.5 * Nk * math.log(2), 0.59, rtol=1e-2)
# Q/T 的對數平均溫度驗算：Q = C_P ΔT，ΔS = Q / T_lm，T_lm = ΔT / ln(Tf/Ti)
Q = 3.5 * Nk * Tin
check("tk-114-5 Q / T_logmean", Q / (Tin / math.log(2)), dSn, rtol=1e-9)

# ---------- 熱學小考（上）答案卷數字 vs 網站卡片 ----------
C = math.comb
check("sc-2-8(b) Ω_total = C(39,20)", C(39, 20), 6.89e10)
check("sc-2-8(c) P(all in A) = C(29,20)/C(39,20)", C(29, 20) / C(39, 20), 1.45e-4)
check("sc-2-8(d) P(half) = C(19,10)^2/C(39,20)", C(19, 10) ** 2 / C(39, 20), 0.124)
check("sc-2-22(d) width ratio sqrt(pi/2N), N=1e23", math.sqrt(math.pi / (2 * 1e23)), 4.0e-12, rtol=0.03)
check("sc-2-27 0.99^100", 0.99 ** 100, 0.366)
check("sc-2-27 0.99^10000", 0.99 ** 10000, 2.25e-44, rtol=1e-2)
check("sc-2-27 log10(0.99^1e23) / 1e20", 1e23 * math.log10(0.99) / 1e20, -4.36, rtol=1e-2)
Nn = 1e23
check("sc-2-30(a) ln sqrt(8 pi N)", math.log(math.sqrt(8 * math.pi * Nn)), 28.09, rtol=1e-3)
check("sc-2-30(b) ln(4 pi N)", math.log(4 * math.pi * Nn), 55.49, rtol=1e-3)
G, c, h, Msun = 6.67e-11, 3.0e8, 6.63e-34, 2.0e30
check("sc-2-42(d) S = 8 pi^2 G M^2 k / (h c)", 8 * math.pi ** 2 * G * Msun ** 2 * kB / (h * c), 1.46e54, rtol=1e-2)

print("ALL PASS" if fails == 0 else f"{fails} FAILED")
raise SystemExit(1 if fails else 0)
