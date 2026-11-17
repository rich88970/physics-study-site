"""熱學第 1 章 §1.1、§1.2（代理 A）所有數值答案的獨立驗算。
執行：python tools/verify_thermal_ch01_A.py  → 全部通過時印出 ALL PASS。
常數與課本一致：R=8.31 J/(mol·K)、k=1.381e-23 J/K、N_A=6.02e23、1 atm=1.013e5 Pa、室溫 300 K。
"""
import math
import sys

import numpy as np
import sympy as sp

R, k, NA, atm, g, u, eV = 8.31, 1.381e-23, 6.02e23, 1.013e5, 9.8, 1.6605e-27, 1.602e-19
FAILS = []


def check(name, got, want, rel=0.01, absol=None):
    ok = abs(got - want) <= (absol if absol is not None else rel * abs(want))
    print(f"{'ok ' if ok else 'FAIL'} {name}: got {got:.6g}, want {want:.6g}")
    if not ok:
        FAILS.append(name)


# ---------------- §1.1 ----------------
# sc-ex-fig13：Fig. 1.3 中間那條線的兩個讀數（由 PDF 向量圖座標換算）
T1, P1, T2, P2 = -76.0, 0.66, 95.0, 1.21
s = (P2 - P1) / (T2 - T1)
check("fig13 斜率 atm/°C", s, 0.003216, rel=0.002)
T0 = T1 - P1 / s
check("fig13 外插零點 °C", T0, -281.2, absol=1.0)
# PDF 向量座標的五點最小平方（中間線）：零點約 -280
xs = np.array([269.26, 289.88, 310.49, 335.99, 362.03]); ys = np.array([140.74, 131.48, 119.88, 108.61, 96.16])
Tc = (xs - 310.49) / 0.5425; Pc = 0.2 + (177.98 - ys) * 0.2 / 16.173
A_ = np.polyfit(Tc, Pc, 1)
check("fig13 五點擬合零點", -A_[1] / A_[0], -280.0, absol=8)

# 1.1
F = lambda c: 9 / 5 * c + 32
check("1.1 0°C→°F", F(0), 32, absol=1e-9); check("1.1 100°C→°F", F(100), 212, absol=1e-9)
check("1.1 絕對零度 °F", F(-273.15), -459.67, absol=0.01)
# 1.2
check("1.2 室溫 300 K → °R", 9 / 5 * 300, 540, absol=1e-9)
check("1.2 °R=°F+459.67（以 300 K 驗）", F(300 - 273.15) + 459.67, 540, absol=0.01)
# 1.3
for nm, c, kv in [("體溫", 37, 310.15), ("沸點", 100, 373.15), ("寒流 5°C", 5, 278.15), ("液態氮", -196, 77.15), ("鉛熔點", 327, 600.15)]:
    check("1.3 " + nm, c + 273.15, kv, absol=1e-9)
# 1.4
check("1.4 20°C/10°C 的 kelvin 比", 293.15 / 283.15, 1.0353, rel=1e-3)
check("1.4 鉛熔點/室溫", 600 / 300, 2, absol=1e-9)
# 1.7 (a)：球泡直徑 4 mm、長 8 mm；1°C 刻度 5 mm
beta_hg = 1 / 5500
Vb = math.pi * 2 ** 2 * 8
check("1.7 球泡體積 mm^3", Vb, 100.5, rel=0.002)
dV = beta_hg * Vb * 1
check("1.7 ΔV mm^3", dV, 0.01828, rel=0.003)
Acap = dV / 5
dcap = 2 * math.sqrt(Acap / math.pi)
check("1.7 毛細管截面 mm^2", Acap, 0.003655, rel=0.003)
check("1.7 毛細管內徑 mm", dcap, 0.0682, rel=0.005)
check("1.7 β 數值", beta_hg, 1.818e-4, rel=1e-3)
# 1.8 (a)：ΔT ≈ 25 K（台灣：冬夜 10°C、夏日 35°C）
check("1.8 ΔL (m) ΔT=25K", 1.1e-5 * 1000 * 25, 0.275, rel=1e-6)
check("1.8 ΔL 115 級答案卷 ΔT=15K", 1.1e-5 * 1000 * 15, 0.165, rel=1e-6)
check("1.8 ΔL 解答手冊 ΔT=70K", 1.1e-5 * 1000 * 70, 0.77, rel=1e-6)
# 1.8 (c)：符號推導
ax, ay, az, Lx, Ly, Lz, dT = sp.symbols("alpha_x alpha_y alpha_z L_x L_y L_z dT", positive=True)
V1 = Lx * (1 + ax * dT) * Ly * (1 + ay * dT) * Lz * (1 + az * dT)
beta_sym = sp.diff(V1, dT).subs(dT, 0) / (Lx * Ly * Lz)
assert sp.simplify(beta_sym - (ax + ay + az)) == 0
print("ok  1.8(c) β = αx+αy+αz（sympy）")

# 自編 01a：鋼捲尺（20°C 校正）在 40°C 量鋁棒（20°C 時 1.000 m）
aAl, aS = 2.3e-5, 1.1e-5
Lrod = 1.000 * (1 + aAl * 20); unit = 1.000 * (1 + aS * 20)
check("01a 鋁棒 40°C 真長 m", Lrod, 1.00046, rel=1e-7)
check("01a 捲尺讀數 m", Lrod / unit, 1.000240, rel=2e-7)
check("01a 讀數多出 mm", (Lrod / unit - 1) * 1000, 0.240, rel=0.01)
# (b) 鋁環內徑 99.95 mm、鋼軸 100.00 mm（20°C）
dT_ring = 0.05 / (99.95 * aAl)
check("01a 只加熱鋁環 ΔT", dT_ring, 21.75, rel=0.002)
dT_both = 0.05 / (99.95 * aAl - 100.00 * aS)
check("01a 一起加熱 ΔT", dT_both, 41.71, rel=0.002)
check("01a 一起加熱的溫度 °C", 20 + dT_both, 61.7, absol=0.1)

# 自編 01b：水的 β(T) 取通過 (0,-0.68e-4)、(4,0)、(100,7.5e-4) 的二次式
Ts = sp.symbols("T")
c0, c1, c2 = sp.symbols("c0 c1 c2")
sol = sp.solve([c0 + 0 * c1 - sp.Rational(-68, 10 ** 6),
                c0 + 4 * c1 + 16 * c2,
                c0 + 100 * c1 + 10000 * c2 - sp.Rational(75, 10 ** 5)], [c0, c1, c2])
bq = sol[c0] + sol[c1] * Ts + sol[c2] * Ts ** 2
check("01b c1 (1/K^2)", float(sol[c1]), 1.73675e-5, rel=1e-4)
check("01b c2 (1/K^3)", float(sol[c2]), -9.1875e-8, rel=1e-4)
I = sp.integrate(bq, (Ts, 0, Ts))
I100 = float(I.subs(Ts, 100)); I50 = float(I.subs(Ts, 50))
check("01b ∫0^100 β dT", I100, 0.049413, rel=1e-4)
check("01b ∫0^50 β dT", I50, 0.014481, rel=1e-4)
check("01b 50°C 時的讀數 θ", 100 * I50 / I100, 29.31, rel=1e-3)
check("01b 讀數 = 0 的另一個真溫度 °C", float(sp.nsolve(I, Ts, 8)), 8.06, rel=1e-3)
check("01b 4°C 時的讀數 θ", 100 * float(I.subs(Ts, 4)) / I100, -0.2733, rel=2e-3)
check("01b β(20°C) 二次式", float(bq.subs(Ts, 20)), 2.07e-4, rel=0.2)

# ---------------- §1.2 ----------------
check("sc-ex-k k=R/N_A", R / NA, 1.380e-23, rel=1e-3)
check("sc-ex-k 1 L·atm (J)", atm * 1e-3, 101.3, rel=1e-3)
check("sc-ex-k 1 mol: nR = N k", 6.02e23 * 1.381e-23, 8.31, rel=1e-3)
# 1.9
Vm = R * 300 / atm
check("1.9 V (m^3)", Vm, 0.02461, rel=2e-3)
# 1.10 房間 4×4×3 m
Nroom = atm * 48 / (k * 300)
check("1.10 N", Nroom, 1.174e27, rel=2e-3)
check("1.10 莫耳數", Nroom / NA, 1950, rel=5e-3)
# 1.12
vpm = k * 300 / atm
check("1.12 V/N (m^3)", vpm, 4.090e-26, rel=2e-3)
check("1.12 間距 (nm)", vpm ** (1 / 3) * 1e9, 3.45, rel=3e-3)
# 1.13、1.14
check("1.13 H2O", 2 * 1 + 16, 18, absol=0); check("1.13 SiO2", 28 + 32, 60, absol=0)
Mair = 0.78 * 28 + 0.21 * 32 + 0.01 * 40
check("1.14 M_air (g)", Mair, 28.96, rel=1e-4)
# 1.15 直徑 15 m、外面 300 K、1 atm、負載 500 kg、M=0.029
Vbal = 4 / 3 * math.pi * 7.5 ** 3
check("1.15 V (m^3)", Vbal, 1767, rel=1e-3)
term = 500 * R / (0.029 * atm * Vbal)
check("1.15 M R/(m P V) (1/K)", term, 8.004e-4, rel=2e-3)
Tin = 1 / (1 / 300 - term)
check("1.15 T_in (K)", Tin, 394.8, rel=2e-3)
Mair_in = 0.029 * atm * Vbal / (R * Tin)
check("1.15 內部空氣質量 kg", Mair_in, 1582, rel=3e-3)
check("1.15 浮力驗算 (ρ0-ρ)V = 500", 0.029 * atm * Vbal / R * (1 / 300 - 1 / Tin), 500, rel=1e-6)
# 1.16 T=280 K、M=0.029
H = R * 280 / (0.029 * g)
check("1.16 標高 kT/mg (m)", H, 8187, rel=2e-3)
for nm, z, pv in [("Ogden", 1430, 0.840), ("Leadville", 3090, 0.686), ("Whitney", 4420, 0.583), ("Everest", 8850, 0.339)]:
    check("1.16 " + nm, math.exp(-z / H), pv, rel=3e-3)
zz, Pf, mm, gg, kk, TT = sp.symbols("z P m g k T", positive=True)
Pz = sp.Function("P")
solde = sp.dsolve(sp.Eq(Pz(zz).diff(zz), -mm * gg / (kk * TT) * Pz(zz)), ics={Pz(0): Pf})
assert sp.simplify(solde.rhs - Pf * sp.exp(-mm * gg * zz / (kk * TT))) == 0
print("ok  1.16(c) dsolve")
# 1.17 (a)
Bdat = {100: -160, 200: -35, 300: -4.2, 400: 9.0, 500: 16.9, 600: 21.3}
want = {100: -0.0195, 200: -0.00213, 300: -0.000171, 400: 0.000274, 500: 0.000412, 600: 0.000433}
for T, B in Bdat.items():
    check(f"1.17(a) B/(V/n) at {T} K", B * 1e-6 / (R * T / atm), want[T], rel=5e-3)
check("1.17(a) V/n at 100 K (m^3/mol)", R * 100 / atm, 0.008203, rel=1e-3)
# 1.17 (c)：凡得瓦 → 維里係數
n_, V_, a_, b_, RT = sp.symbols("n V a b RT", positive=True)
x = sp.symbols("x", positive=True)  # x = n/V
PV_over_nRT = (1 / (1 - b_ * x) - a_ * x / RT)
ser = sp.series(PV_over_nRT, x, 0, 3).removeO()
assert sp.simplify(ser.coeff(x, 1) - (b_ - a_ / RT)) == 0 and sp.simplify(ser.coeff(x, 2) - b_ ** 2) == 0
print("ok  1.17(c) B=b-a/RT, C=b^2（sympy 級數）")
# 1.17 (d)：最小平方擬合 B = b - a/(R T)
Tv = np.array(list(Bdat)); Bv = np.array(list(Bdat.values())) * 1e-6
Amat = np.vstack([np.ones_like(Tv, dtype=float), -1 / (R * Tv)]).T
(bfit, afit), *_ = np.linalg.lstsq(Amat, Bv, rcond=None)
check("1.17(d) 最小平方 b (m^3/mol)", bfit, 6.42e-5, rel=0.002)
check("1.17(d) 最小平方 a (J·m^3/mol^2)", afit, 0.1822, rel=0.002)
check("1.17(d) 兩點 (300 K 過零、b=30e-6) 的 a", 30e-6 * R * 300, 0.0748, rel=2e-3)
Bfit100 = bfit - afit / (R * 100)
check("1.17(d) 擬合在 100 K 的 B (cm^3/mol)", Bfit100 * 1e6, -155.1, rel=0.002)
Bfit600 = bfit - afit / (R * 600)
check("1.17(d) 擬合在 600 K 的 B (cm^3/mol)", Bfit600 * 1e6, 27.7, rel=0.003)
check("1.17(d) Boyle 溫度 a/(bR) (K)", afit / (bfit * R), 341.5, rel=0.002)
# sc-ex-kT
kT = k * 300
check("sc-ex-kT kT (J)", kT, 4.143e-21, rel=1e-3)
check("sc-ex-kT k (eV/K)", k / eV, 8.62e-5, rel=1e-3)
check("sc-ex-kT kT (eV)", kT / eV, 0.02586, rel=2e-3)
check("sc-ex-kT K_trans (J)", 1.5 * kT, 6.21e-21, rel=2e-3)
check("sc-ex-kT K_trans (eV)", 1.5 * kT / eV, 0.0388, rel=3e-3)
# 1.18
check("1.18 N2 vrms (m/s)", math.sqrt(3 * R * 300 / 0.028), 516.7, rel=1e-3)
check("1.18 用 k、m 直接算", math.sqrt(3 * k * 300 / (28 * u)), 516.7, rel=3e-3)
# 1.19
check("1.19 H2/O2 速率比", math.sqrt(32 / 2), 4, absol=1e-12)
# 1.20
v238 = math.sqrt(3 * R * 300 / 0.352); v235 = math.sqrt(3 * R * 300 / 0.349)
check("1.20 vrms(238UF6)", v238, 145.76, rel=5e-4)
check("1.20 vrms(235UF6)", v235, 146.38, rel=5e-4)
check("1.20 比值", v235 / v238, 1.00429, rel=1e-5)
# 1.21
dvx = 2 * 15 * math.cos(math.radians(45))
check("1.21 Δv_x (m/s)", dvx, 21.21, rel=1e-3)
Fav = 30 * 0.002 * dvx
check("1.21 平均力 (N)", Fav, 1.273, rel=1e-3)
Phail = Fav / 0.5
check("1.21 壓力 (Pa)", Phail, 2.546, rel=1e-3)
check("1.21 atm/P", atm / Phail, 3.98e4, rel=3e-3)
# 1.22
c = math.sqrt(R * 300 / 0.029)
check("1.22(d) sqrt(kT/m) (m/s)", c, 293.2, rel=1e-3)
tau = 2 * 1e-3 / (1e-6 * c)
check("1.22(d) τ (s)", tau, 6.82, rel=2e-3)
Vt = math.pi * 0.012 ** 2 * 2.1
check("1.22(e) 輪胎體積 (m^3)", Vt, 9.50e-4, rel=2e-3)
Ah = 2 * Vt / (3600 * c)
check("1.22(e) 洞面積 (m^2)", Ah, 1.80e-9, rel=3e-3)
check("1.22(e) 洞直徑 (mm)", 2 * math.sqrt(Ah / math.pi) * 1e3, 0.0479, rel=3e-3)
tauf = 2 * 20 / (0.1 * c)
check("1.22(f) τ (s)", tauf, 1.364, rel=3e-3)
check("1.22(f) 開窗 1 s 漏掉比例", 1 - math.exp(-1 / tauf), 0.520, rel=3e-3)
check("1.22(f) 開窗 0.5 s 漏掉比例", 1 - math.exp(-0.5 / tauf), 0.307, rel=3e-3)
# 1.22(c) ODE
t_, N0, Ah_, V2, cc = sp.symbols("t N0 A V c", positive=True)
Nf = sp.Function("N")
sol2 = sp.dsolve(sp.Eq(Nf(t_).diff(t_), -Ah_ / (2 * V2) * cc * Nf(t_)), ics={Nf(0): N0})
assert sp.simplify(sol2.rhs - N0 * sp.exp(-t_ * Ah_ * cc / (2 * V2))) == 0
print("ok  1.22(c) dsolve")

# 自編 02a：離心機，壁速 ωa = 500 m/s、300 K、Δm = 3 u
dm = 3 * u
expo = dm * 500 ** 2 / (2 * k * 300)
check("02a 指數 Δm ω²a²/2kT", expo, 0.1503, rel=3e-3)
check("02a 分離因子", math.exp(expo), 1.162, rel=2e-3)
check("02a 相當的擴散級數", expo / math.log(v235 / v238), 35.1, rel=0.01)
expo_P = 352 * u * 500 ** 2 / (2 * k * 300)
check("02a UF6 壁/軸壓力比指數", expo_P, 17.64, rel=3e-3)
check("02a UF6 壁/軸壓力比", math.exp(expo_P), 4.58e7, rel=0.02)
# 驗證 n(r)=n0 exp(mω²r²/2kT) 滿足 dP/dr = ρ ω² r
r_, w_, m_, kT_, n0 = sp.symbols("r omega m kT n0", positive=True)
nr = n0 * sp.exp(m_ * w_ ** 2 * r_ ** 2 / (2 * kT_))
assert sp.simplify(sp.diff(nr * kT_, r_) - m_ * nr * w_ ** 2 * r_) == 0
print("ok  02a 離心平衡 dP/dr = ρω²r")

# 自編 02b：熱流逸 P1/√T1 = P2/√T2
P2b = 100 * math.sqrt(600 / 300)
check("02b P2 (Pa)", P2b, 141.4, rel=1e-3)
check("02b 數密度比 n2/n1", (P2b / 600) / (100 / 300), 0.7071, rel=1e-3)
# 用精確通量 P/√(2πmkT) 結果相同（比值與常數因子無關）
m2 = 29 * u
J1 = 100 / math.sqrt(2 * math.pi * m2 * k * 300); J2 = P2b / math.sqrt(2 * math.pi * m2 * k * 600)
check("02b 精確通量相等", J2 / J1, 1.0, rel=1e-9)

# ---------------- 補充：正文中其他出現的數字 ----------------
check("1.2 300K→°F+459.67", (300 - 273.15) * 9 / 5 + 32 + 459.67, 540.0, absol=0.01)
check("1.4 華氏比 68/50", F(20) / F(10), 1.36, rel=1e-3)
check("1.5 ln(13/0.1)", math.log(130), 4.87, rel=2e-3)
e_skin = math.sqrt(0.37 * 1100 * 3400); e_st = math.sqrt(50 * 7800 * 470); e_wd = math.sqrt(0.12 * 500 * 1700)
check("1.6 e 皮膚", e_skin, 1180, rel=0.01); check("1.6 e 鋼", e_st, 13500, rel=0.01); check("1.6 e 木", e_wd, 320, rel=0.01)
check("1.6 接觸溫度 鋼", (1180 * 33 + 13500 * 20) / 14680, 21.0, absol=0.06)
check("1.6 接觸溫度 木", (1180 * 33 + 320 * 20) / 1500, 30.2, absol=0.06)
check("01a 代回 環", 99.95 * (1 + aAl * dT_both), 100.046, rel=3e-6)
check("01a 代回 軸", 100.00 * (1 + aS * dT_both), 100.046, rel=3e-6)
check("01b β 的另一根 (°C)", float(sol[c0] / sol[c2]) / 4, 185.0, rel=3e-3)
check("1.10 房間空氣質量 kg", Nroom / NA * 0.029, 57, rel=0.01)
check("1.11 303/293 質量比", 293 / 303, 0.967, rel=1e-3)
check("1.15 外部空氣質量 kg", 0.029 * atm * Vbal / (R * 300), 2082, rel=2e-3)
check("1.19 vrms H2", math.sqrt(3 * R * 300 / 0.002), 1934, rel=1e-3)
check("1.19 vrms O2", math.sqrt(3 * R * 300 / 0.032), 483, rel=2e-3)
check("1.21 非彈性壓力", Phail / 2, 1.27, rel=3e-3)
check("sc-ex-k R in L·atm", R / 101.3, 0.0820, rel=2e-3)
check("1.17 Boyle 用擬合", afit / (bfit * R), 342, rel=3e-3)

print()
if FAILS:
    print("FAILED:", FAILS)
    sys.exit(1)
print("ALL PASS")
