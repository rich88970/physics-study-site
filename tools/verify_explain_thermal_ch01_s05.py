"""熱學第 1 章第五節（05-compression.html）16 張卡「詳細說明」（跟著詳解一步步講）裡新出現的數值獨立重算。

涵蓋：補出的中間結果、「這步容易錯」裡錯誤算法的數字、「做完回頭看」的驗算、「如果題目改成……」的答案。
t1-self-05b 是範本（不在此檔，也沒有改動）。

用法：python -X utf8 tools/verify_explain_thermal_ch01_s05.py
全部通過時最後印出 ALL CHECKS PASSED。
網站慣例：1 atm·L = 101.3 J（考古 114-7 依題目取 1 atm = 1e5 Pa）、R = 8.315 J/(mol·K)、空氣 M = 0.029 kg/mol。
"""
import sys
from math import exp, log, log2, log10, sqrt

import sympy as sp

FAIL = []
ATML = 101.3   # J / (atm·L)
R = 8.315


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


V, c = sp.symbols("V c", positive=True)

# ---------- sc-ex-100j ----------
check("100j 壓縮 1 L", -1e5 * (-1e-3), 100)
check("100j 膨脹 1 L", -1e5 * (+1e-3), -100)
check("100j 100 L 槽等溫少 1 L 的壓力倍數", 100 / 99, 1.01)
check("100j 公升沒換的離譜答案", -1e5 * (-1), 1e5)
check("100j 1 atm = 100 J/L", 1e5 * 1e-3, 100)
check("100j 1 kg 舉高 10 m", 1 * 9.8 * 10, 98)
check("100j 5 atm 槽壓掉 1 L", -5e5 * (-1e-3), 500)
check("100j 2 L 小槽等溫壓到 1 L", 1e5 * 2e-3 * log(2), 139)
check("100j 小槽：用初壓估", 1e5 * 1e-3, 100)
check("100j 小槽：用末壓估", 2e5 * 1e-3, 200)

# ---------- sc-1-31 ----------
cc = 1.0                                   # atm/L
check("1.31 末壓力", cc * 3, 3)
W31 = -cc / 2 * (3 ** 2 - 1 ** 2)
check("1.31 W（atm·L）", W31, -4)
check("1.31 W（J）", W31 * ATML, -405)
check("1.31 梯形面積", (1 + 3) / 2 * 2, 4)
check("1.31 錯用末壓", -3 * 2, -6)
check("1.31 錯用初壓", -1 * 2, -2)
dU31 = 1.5 * (9 - 1)
check("1.31 ΔU（atm·L）", dU31, 12)
check("1.31 ΔU（J）", dU31 * ATML, 1216)
Q31 = dU31 - W31
check("1.31 Q（atm·L）", Q31, 16)
check("1.31 Q（J）", Q31 * ATML, 1621)
check("1.31 錯寫 Q=ΔU+W", dU31 + W31, 8)
true("1.31 比例 1:3:4", (-W31, dU31, Q31) == (4, 12, 16))
expr = sp.integrate(c * V, (V, 1, 3)) - sp.Rational(1, 2) * (c * 9 - c * 1)
true("1.31 P∝V：∫P dV = Δ(PV)/2", sp.simplify(expr) == 0)
check("1.31 解答手冊 W（1e5 Pa）", -4 * 100, -400)
check("1.31 與手冊差 1.3%", ATML / 100 - 1, 0.013)
check("1.31 到 4 L：W", -0.5 * (16 - 1), -7.5)
check("1.31 到 4 L：ΔU", 1.5 * 15, 22.5)
check("1.31 到 4 L：Q", 1.5 * 15 + 0.5 * 15, 30)
check("1.31 氮：ΔU", 2.5 * 8, 20)
check("1.31 氮：Q", 2.5 * 8 + 4, 24)
true("1.31 氮：比例 1:5:6", (4 / 4, 20 / 4, 24 / 4) == (1, 5, 6))

# ---------- tk1-114-7 ----------
PiVi, PfVf = 1e5 * 1e-3, 4e5 * 4e-3
check("114-7 P_iV_i（J）", PiVi, 100)
check("114-7 P_fV_f（J）", PfVf, 1600)
check("114-7 W", -0.5 * (PfVf - PiVi), -750)
check("114-7 c 的 SI 值", 1e5 / 1e-3, 1e8)
check("114-7 V_f^2", (4e-3) ** 2, 1.6e-5)
check("114-7 錯用末壓", -4e5 * 3e-3, -1200)
check("114-7 錯用初壓", -1e5 * 3e-3, -300)
check("114-7 ΔU", 1.5 * (PfVf - PiVi), 2250)
check("114-7 錯用 5/2", 2.5 * (PfVf - PiVi), 3750)
check("114-7 梯形（atm·L）", (1 + 4) / 2 * 3, 7.5)
check("114-7 ΔU/|W| = f", 2250 / 750, 3)
check("114-7 溫度倍數", PfVf / PiVi, 16)
check("114-7 300 K 起的末溫", 300 * 16, 4800)
check("114-7 用 101.3 J：W", -7.5 * ATML, -760)
check("114-7 用 101.3 J：ΔU", 22.5 * ATML, 2280)
P2V2 = 2e5 * 2e-3
check("114-7 到 2 L：P_fV_f", P2V2, 400)
check("114-7 到 2 L：W", -0.5 * (P2V2 - PiVi), -150)
check("114-7 到 2 L：ΔU", 1.5 * (P2V2 - PiVi), 450)
check("114-7 到 2 L：Q", 2.0 * (P2V2 - PiVi), 600)

# ---------- sc-1-32 ----------
W32 = -0.5 * (1 + 200) * (-0.01)
check("1.32 W（atm·L）", W32, 1.005)
check("1.32 W（J）", W32 * ATML, 102)
check("1.32 全用 SI（J）", 0.5 * 201 * 1.013e5 * 1e-5, 102)
check("1.32 錯用末壓（atm·L）", 200 * 0.01, 2)
check("1.32 mgh", 10 * 9.8 * 1, 100, rel=0.03)
check("1.32 100 J 讓 1 kg 水升溫", 100 / 4186, 0.024, rel=0.02)
B = 199 / 0.01
check("1.32 B（atm）", B, 2e4)
check("1.32 B（Pa）", B * 1.013e5, 2e9, rel=0.02)
check("1.32 ½BV(ΔV/V)^2（B=2e4）", 0.5 * 2e4 * 1 * 0.01 ** 2, 1.0)
check("1.32 ½BV(ΔV/V)^2（B=19900）", 0.5 * B * 1 * 0.01 ** 2, 1.0)
check("1.32 10 L 水（J）", 10 * W32 * ATML, 1000, rel=0.02)
Pf98 = 1 + B * 0.02          # B = 199/0.01
check("1.32 壓到 98% 所需壓力", Pf98, 399, rel=0.005)
check("1.32 壓到 98% 的功（atm·L）", 0.5 * (1 + Pf98) * 0.02, 4.0)
check("1.32 壓到 98% 的功（J）", 0.5 * (1 + Pf98) * 0.02 * ATML, 405)

# ---------- sc-1-33 ----------
pts = [(1, 1), (2, 1), (2, 2), (1, 1)]   # (V, P)


def cycle(fdof):
    out = []
    for (V1, P1), (V2, P2) in zip(pts[:-1], pts[1:]):
        W = -0.5 * (P1 + P2) * (V2 - V1)
        dU = fdof / 2 * (P2 * V2 - P1 * V1)
        out.append((W, dU, dU - W))
    return out


c3 = cycle(3)
for name, got, want in [("A W", c3[0][0], -1), ("A ΔU", c3[0][1], 1.5), ("A Q", c3[0][2], 2.5),
                        ("B W", c3[1][0], 0), ("B ΔU", c3[1][1], 3), ("B Q", c3[1][2], 3),
                        ("C W", c3[2][0], 1.5), ("C ΔU", c3[2][1], -4.5), ("C Q", c3[2][2], -6)]:
    check("1.33 f=3 " + name, got, want)
check("1.33 f=3 整圈 W", sum(s[0] for s in c3), 0.5)
check("1.33 三角形面積", 0.5 * 1 * 1, 0.5)
check("1.33 f=3 整圈 ΔU", sum(s[1] for s in c3), 0)
check("1.33 f=3 整圈 Q", sum(s[2] for s in c3), -0.5)
c5 = cycle(5)
for name, got, want in [("A ΔU", c5[0][1], 2.5), ("A Q", c5[0][2], 3.5), ("B ΔU", c5[1][1], 5),
                        ("B Q", c5[1][2], 5), ("C ΔU", c5[2][1], -7.5), ("C Q", c5[2][2], -9)]:
    check("1.33 f=5 " + name, got, want)
check("1.33 f=5 整圈 W", sum(s[0] for s in c5), 0.5)
check("1.33 f=5 整圈 Q", sum(s[2] for s in c5), -0.5)
true("1.33 每段 ΔU 與 −W 同號或為零（f=3）",
     all(s[1] * (-s[0]) >= 0 for s in c3))

# ---------- sc-1-34 ----------
p1, p2, v1, v2 = sp.symbols("P1 P2 V1 V2", positive=True)
QA = sp.Rational(5, 2) * v1 * (p2 - p1)
QB = sp.Rational(7, 2) * p2 * (v2 - v1)
QC = -sp.Rational(5, 2) * v2 * (p2 - p1)
QD = -sp.Rational(7, 2) * p1 * (v2 - v1)
true("1.34 四個 Q 相加 = ΔPΔV", sp.simplify(QA + QB + QC + QD - (p2 - p1) * (v2 - v1)) == 0)
dUsum = sp.Rational(5, 2) * ((v1 * p2 - v1 * p1) + (p2 * v2 - p2 * v1) + (v2 * p1 - v2 * p2) + (p1 * v1 - p1 * v2))
true("1.34 ΔU 八項相消", sp.simplify(dUsum) == 0)
true("1.34 Q_B = ΔU_B − W_B", sp.simplify(sp.Rational(5, 2) * p2 * (v2 - v1) + p2 * (v2 - v1) - QB) == 0)
P1, P2, V1, V2 = 1, 2, 1, 3


def rect(fdof):
    a = fdof / 2
    A = (0, a * V1 * (P2 - P1))
    Bq = (-P2 * (V2 - V1), a * P2 * (V2 - V1))
    C = (0, -a * V2 * (P2 - P1))
    D = (P1 * (V2 - V1), -a * P1 * (V2 - V1))
    return [(W, dU, dU - W) for W, dU in (A, Bq, C, D)]


r5 = rect(5)
for name, got, want in [("A Q", r5[0][2], 2.5), ("B W", r5[1][0], -4), ("B ΔU", r5[1][1], 10),
                        ("B Q", r5[1][2], 14), ("C Q", r5[2][2], -7.5), ("D W", r5[3][0], 2),
                        ("D ΔU", r5[3][1], -5), ("D Q", r5[3][2], -7)]:
    check("1.34 數值 " + name, got, want)
check("1.34 整圈 W", sum(s[0] for s in r5), -2)
check("1.34 整圈 Q", sum(s[2] for s in r5), 2)
check("1.34 吸熱 A+B", r5[0][2] + r5[1][2], 16.5)
check("1.34 效率", 2 / 16.5, 0.12, rel=0.02)
r3 = rect(3)
check("1.34 f=3 整圈 W", sum(s[0] for s in r3), -2)
check("1.34 f=3 吸熱", r3[0][2] + r3[1][2], 11.5)
check("1.34 f=3 效率", 2 / 11.5, 0.17, rel=0.03)
true("1.34 |Q_C| > |Q_A|", abs(r5[2][2]) > abs(r5[0][2]))

# ---------- sc-ex-isotherm ----------
check("等溫 W", ATML * log(2), 70.2)
check("等溫 ln2", log(2), 0.693, rel=0.001)
check("等溫 末壓力", 1 * 1 / 0.5, 2)
check("等溫 錯用 log10", ATML * log10(2), 30.5)
check("等溫 平均壓力", log(2) / 0.5, 1.39, rel=0.005)
check("等溫 用初壓估", 1 * 0.5 * ATML, 50.7)
check("等溫 用末壓估", 2 * 0.5 * ATML, 101)
check("等溫 0.5→0.25 L 同樣 70.2 J", ATML * log(0.5 / 0.25), 70.2)
check("等溫 膨脹 1→2 L", -ATML * log(2), -70.2)
check("等溫 壓到 0.1 L", ATML * log(10), 233)

# ---------- sc-ex-adiabat ----------
check("絕熱 單原子壓一半倍數", 2 ** (2 / 3), 1.59)
check("絕熱 雙原子壓一半倍數", 2 ** 0.4, 1.32)
check("絕熱 單原子 300 K 壓一半", 300 * 2 ** (2 / 3), 476)
check("絕熱 雙原子 300 K 壓一半", 300 * 2 ** 0.4, 396)
check("絕熱 雙原子膨脹兩倍", 300 * 2 ** -0.4, 227)
fs = sp.symbols("f", positive=True)
Pp, Vp, g = sp.symbols("P0 V0 gamma", positive=True)
true("絕熱 P∝V^-(1+2/f) 的指數 = γ", sp.simplify(1 + 2 / fs - (fs + 2) / fs) == 0)
slope_ad = sp.diff(Pp * (Vp / V) ** g, V).subs(V, Vp)
slope_iso = sp.diff(Pp * Vp / V, V).subs(V, Vp)
true("絕熱線斜率 = γ × 等溫線斜率（−γP/V 對 −P/V）",
     sp.simplify(slope_ad + g * Pp / Vp) == 0 and sp.simplify(slope_iso + Pp / Vp) == 0)
T_ = sp.symbols("T", positive=True)
sol = sp.dsolve(sp.Eq(fs / 2 * sp.Function("T")(V).diff(V) / sp.Function("T")(V), -1 / V))
true("絕熱 微分方程解 T ∝ V^(-2/f)", sp.simplify(sp.diff(sp.log(sol.rhs), V) + 2 / (fs * V)) == 0)

# ---------- sc-1-35 ----------
gam = (fs + 2) / fs
true("1.35 (1+f/2)(2/f) = (f+2)/f", sp.simplify((1 + fs / 2) * 2 / fs - gam) == 0)
true("1.35 (γ−1)/γ = 2/(f+2)", sp.simplify((gam - 1) / gam - 2 / (fs + 2)) == 0)
check("1.35 單原子 γ", 5 / 3, 1.667, rel=0.001)
check("1.35 雙原子 γ", 7 / 5, 1.4)
check("1.35 單原子壓一半 P 倍數", 2 ** (5 / 3), 3.17)
check("1.35 雙原子壓一半 P 倍數", 2 ** 1.4, 2.64)

# ---------- tk1x-1e ----------
Nk, CV = sp.symbols("Nk C_V", positive=True)
true("1e Nk/C_V = γ−1（C_P = C_V + Nk）", sp.simplify(Nk / CV - ((CV + Nk) / CV - 1)) == 0)
check("1e 單原子 γ", (5 / 2) / (3 / 2), 5 / 3)
check("1e 雙原子 γ", (7 / 2) / (5 / 2), 1.4)
P_ = sp.symbols("P", positive=True)
e1 = T_ * (Nk * T_ / P_) ** (g - 1)
e2 = (Nk) ** (g - 1) * T_ ** g * P_ ** (1 - g)
true("1e T(NkT/P)^(γ−1) = (Nk)^(γ−1) T^γ P^(1−γ)", sp.simplify(sp.expand_power_base(e1, force=True) - e2) == 0)
check("1e 單原子膨脹 8 倍 T 比", 8 ** (-2 / 3), 0.25)
check("1e 單原子膨脹 8 倍 P 比", 8 ** (-5 / 3), 1 / 32)

# ---------- sc-1-36 ----------
check("1.36 ln7", log(7), 1.946, rel=0.001)
check("1.36 ln7 × 5/7", log(7) * 5 / 7, 1.390, rel=0.001)
Vf = (1 / 7) ** (5 / 7)
check("1.36 V_f", Vf, 0.249)
check("1.36 e^-1.390", exp(-1.390), 0.249)
check("1.36 等溫 V_f", 1 / 7, 0.143)
check("1.36 錯用 γ 次方的 V_f", (1 / 7) ** 1.4, 0.066, rel=0.02)
PfVf36 = 7 * Vf
check("1.36 P_fV_f", PfVf36, 1.743, rel=0.002)
W36 = 2.5 * (PfVf36 - 1)
check("1.36 W（atm·L）", W36, 1.86)
check("1.36 W（J）", W36 * ATML, 188)
check("1.36 積分公式驗算", 1 / 0.4 * ((1 / Vf) ** 0.4 - 1), 1.86)
check("1.36 V_i/V_f", 1 / Vf, 4.01)
check("1.36 (V_i/V_f)^0.4", (1 / Vf) ** 0.4, 1.744, rel=0.002)
check("1.36 T_f", 300 * (1 / Vf) ** 0.4, 523)
check("1.36 體積比 × 溫度比 = 7", (1 / Vf) * PfVf36, 7)
VHe = (1 / 7) ** (3 / 5)
check("1.36 氦 V_f", VHe, 0.311)
check("1.36 氦 W（atm·L）", 1.5 * (7 * VHe - 1), 1.77)
check("1.36 氦 W（J）", 1.5 * (7 * VHe - 1) * ATML, 179)
check("1.36 氦 溫度倍數", 7 * VHe, 2.18)
check("1.36 氦 T_f", 300 * 7 * VHe, 653)
check("1.36 等溫到 7 atm W", ATML * log(7), 197)
true("1.36 同末壓：等溫功 > 絕熱功", ATML * log(7) > W36 * ATML)

# ---------- sc-1-37 ----------
check("1.37 2000 rpm 一圈（s）", 60 / 2000, 0.03)
check("1.37 壓縮行程（s）", 60 / 2000 / 2, 0.015)
check("1.37 ln20", log(2) + log(10), 3.00, rel=0.002)
check("1.37 e^1.2", exp(1.2), 3.32)
check("1.37 20^0.4", 20 ** 0.4, 3.31)
check("1.37 T_f", 300 * 20 ** 0.4, 994)
check("1.37 錯用攝氏（°C）", 27 * 20 ** 0.4, 89)
check("1.37 錯用 γ 次方", 300 * 20 ** 1.4, 19900)
check("1.37 錯用單原子", 300 * 20 ** (2 / 3), 2210)
check("1.37 末壓力（atm）", 20 ** 1.4, 66)
check("1.37 末壓 = 體積比 × 溫度比", 20 * 20 ** 0.4, 66)
check("1.37 冬天 273 K", 273 * 20 ** 0.4, 905)
check("1.37 530/300", 530 / 300, 1.767, rel=0.001)
check("1.37 剛好 530 K 的壓縮比", (530 / 300) ** 2.5, 4.1, rel=0.02)

# ---------- sc-1-38 ----------
check("1.38 10 m 水壓（Pa）", 1000 * 9.8 * 10, 9.8e4)
check("1.38 10 m 水壓（atm）", 1000 * 9.8 * 10 / 1.013e5, 1, rel=0.04)
check("1.38 A 體積倍數", 2 ** (1 / 1.4), 1.64)
check("1.38 A 溫度倍數", 2 ** (-2 / 7), 0.82)
check("1.38 A 溫度（300 K 起）", 300 * 2 ** (-2 / 7), 246)
check("1.38 V∝T/P：0.82×2", 2 ** (-2 / 7) * 2, 1.64)
true("1.38 2/7 = (γ−1)/γ", abs((1.4 - 1) / 1.4 - 2 / 7) < 1e-12)
check("1.38 20 m：A 體積", 3 ** (1 / 1.4), 2.19)
check("1.38 20 m：A 溫度倍數", 3 ** (-2 / 7), 0.73)
check("1.38 20 m：A 溫度", 300 * 3 ** (-2 / 7), 219)
check("1.38 下沉：A 體積", 2 ** (-1 / 1.4), 0.61)
true("1.38 下沉：A 比 B 大", 2 ** (-1 / 1.4) > 0.5)

# ---------- sc-1-39 ----------
Cc, gg = sp.symbols("C gamma", positive=True)
Nkt = sp.symbols("NkT", positive=True)
true("1.39 等溫 B = P", sp.simplify(-V * sp.diff(Nkt / V, V) - Nkt / V) == 0)
true("1.39 絕熱 B = γP", sp.simplify(-V * sp.diff(Cc * V ** -gg, V) - gg * Cc * V ** -gg) == 0)
tdiff = 0.5 ** 2 / 2e-5
check("1.39 熱擴散時間（s）", tdiff, 1.25e4)
cs = sqrt(1.4 * R * 300 / 0.029)
check("1.39 1 m 波長的週期（s）", 1 / cs, 3e-3, rel=0.05)
true("1.39 擴散時間內的週期數為「幾百萬」", 1e6 < tdiff * cs < 1e7)
check("1.39 c_s/v_rms", sqrt(1.4 / 3), 0.68, rel=0.01)
check("1.39 空氣平均莫耳質量（g/mol）", 0.78 * 28 + 0.21 * 32 + 0.01 * 40, 29, rel=0.01)
check("1.39 γRT", 1.4 * R * 300, 3492)
check("1.39 γRT/M", 1.4 * R * 300 / 0.029, 1.20e5)
check("1.39 c_s", cs, 347)
check("1.39 v_rms", sqrt(3 * R * 300 / 0.029), 508)
check("1.39 M 誤用 29", sqrt(1.4 * R * 300 / 29), 11, rel=0.02)
check("1.39 0°C 聲速", sqrt(1.4 * R * 273 / 0.029), 331)
check("1.39 牛頓等溫聲速", sqrt(R * 300 / 0.029), 293)
check("1.39 低估比例", 1 - 1 / sqrt(1.4), 0.15, rel=0.05)
check("1.39 氦 300 K", sqrt(5 / 3 * R * 300 / 0.004), 1019)
check("1.39 氦/空氣", sqrt(5 / 3 * R * 300 / 0.004) / cs, 3, rel=0.03)
check("1.39 −20°C 聲速", sqrt(1.4 * R * 253 / 0.029), 319)
check("1.39 −20°C 頻率比", sqrt(253 / 300), 0.918)
check("1.39 −20°C 半音數", 12 * log2(sqrt(253 / 300)), -1.5, rel=0.03)

# ---------- sc-1-40 ----------
dT, dP, Tq, Pq, ff = sp.symbols("dT dP T P f", positive=True)
# f/2 dT = -(dT - T/P dP)·(Nk 已除掉) ⟹ 解 dT
solT = sp.solve(sp.Eq(ff / 2 * dT, -dT + Tq / Pq * dP), dT)[0]
true("1.40 dT/dP = 2/(f+2)·T/P", sp.simplify(solT / dP - 2 / (ff + 2) * Tq / Pq) == 0)
mg, kk = sp.symbols("mg k", positive=True)
true("1.40 連鎖律中 T、P 消掉",
     sp.simplify(2 / (ff + 2) * Tq / Pq * (-mg / (kk * Tq) * Pq) + 2 / (ff + 2) * mg / kk) == 0)
check("1.40 Mg/R", 0.029 * 9.8 / R, 0.0342, rel=0.002)
lapse = 2 / 7 * 0.029 * 9.8 / R * 1000
check("1.40 遞減率（K/km）", lapse, 9.77, rel=0.002)
check("1.40 c_P", 3.5 * R / 0.029, 1003)
check("1.40 g/c_P（K/km）", 9.8 / (3.5 * R / 0.029) * 1000, 9.77, rel=0.002)
check("1.40 錯用 f=3", 2 / 5 * 0.029 * 9.8 / R * 1000, 13.7)
check("1.40 上升 2 km", 300 - 2 * 9.77, 280.5, rel=0.001)
check("1.40 標準大氣 2 km 處", 300 - 2 * 6.5, 287)
true("1.40 空氣團比周圍冷 ⟹ 穩定", 300 - 2 * lapse < 300 - 2 * 6.5)
check("1.40 火星", 2 / 7 * 0.044 * 3.71 / R * 1000, 5.6)

# ---------- t1-self-05a ----------
check("05a 末壓力", 1 * 1 * 10, 10)
P2a = 10 ** 1.4
check("05a 中間點壓力", P2a, 25.1)
check("05a 中間點溫度", 300 * 10 ** 0.4, 754)
check("05a T∝PV 驗算倍數", P2a * 0.1 / 1, 2.51)
check("05a 冷卻後壓力", P2a * 300 / (300 * 10 ** 0.4), 10)
check("05a ln10", log(10), 2.303, rel=0.001)
W1 = ATML * log(10)
check("05a 路徑一 W", W1, 233)
W2a = 2.5 * (P2a * 0.1 - 1)
check("05a 絕熱段 W（atm·L）", W2a, 3.78)
check("05a 絕熱段 W（J）", W2a * ATML, 383)
check("05a 冷卻段 ΔU（atm·L）", 2.5 * (1 - P2a * 0.1), -3.78)
check("05a 積分公式驗算", 1 / 0.4 * (10 ** 0.4 - 1), 3.78)
check("05a 差", W2a * ATML - W1, 150, rel=0.02)
check("05a 省的比例", (W2a * ATML - W1) / (W2a * ATML), 0.39, rel=0.02)
check("05a 比 2：等溫", ATML * log(2), 70.2)
W2r2 = 2.5 * (2 ** 0.4 - 1) * ATML
check("05a 比 2：絕熱＋冷卻", W2r2, 80.9)
check("05a 比 2：差", W2r2 - ATML * log(2), 10.7)
check("05a 比 2：差的比例", (W2r2 - ATML * log(2)) / W2r2, 0.13, rel=0.05)
stage = 2.5 * (10 ** 0.2 - 1) * ATML
check("05a 兩段：每段", stage, 148)
check("05a 兩段：合計", 2 * stage, 296)
true("05a 兩段介於等溫與單段之間", W1 < 2 * stage < W2a * ATML)

print()
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("ALL CHECKS PASSED")
