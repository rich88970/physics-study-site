"""熱學第 1 章 §1.7（過程的速率）07-rates.html 所有數值答案的獨立驗算（代理 D）。

用法：python tools/verify_thermal_ch01_D.py   全部通過時結束碼 0。
"""
import math
import sys

import numpy as np
import sympy as sp

k = 1.380649e-23      # J/K
u = 1.66054e-27       # kg
atm = 1.01325e5       # Pa
Rgas = 8.314          # J/(mol K)
NA = 6.02214e23

fails = []


def check(name, got, want, rel=0.02):
    ok = abs(got - want) <= rel * abs(want)
    print(f"{'OK ' if ok else 'BAD'} {name}: {got:.5g}（網站 {want:.5g}）")
    if not ok:
        fails.append(name)


# ---------- 課本例題 ----------
check("sc-ex-window 玻璃 Q/Δt", 0.8 * 1 * 20 / 0.0032, 5000)
VN = k * 300 / atm
check("sc-ex-mfp V/N", VN, 4.09e-26)
ell = VN / (4 * math.pi * (1.5e-10) ** 2)
check("sc-ex-mfp ℓ", ell, 1.45e-7)
check("sc-ex-mfp 分子間距 (V/N)^(1/3)", VN ** (1 / 3), 3.45e-9)
check("sc-ex-mfp ℓ/間距", ell / VN ** (1 / 3), 42, rel=0.03)
check("sc-ex-mfp Δt", 1.5e-7 / 500, 3e-10)
cvV = 2.5 * 1e5 / 300
check("sc-ex-kt-air CV/V", cvV, 833)
check("sc-ex-kt-air kt", 0.5 * cvV * 1.5e-7 * 500, 0.031)
check("sc-ex-dye Δt", 0.1 ** 2 / 1e-9, 1e7)
check("sc-ex-dye 天數", 1e7 / 86400, 116, rel=0.01)

# ---------- 1.56 ----------
check("sc-1-56", 0.026 * 1 * 20 / 0.001, 520)

# ---------- 1.57 ----------
Rg = 3.2e-3 / 0.8
Ra = 1e-3 / 0.026
check("sc-1-57a R_glass", Rg, 0.0040)
check("sc-1-57a R_air", Ra, 0.0385)
Btu = 453.6 * 4.186 * 5 / 9
check("sc-1-57b 1 Btu", Btu, 1055)
conv = 1.8 * (1 / 0.3048) ** 2 / (1 / Btu * 3600)  # 1 K·m²/W → °F·ft²·hr/Btu
check("sc-1-57b 換算因子", conv, 5.68)
check("sc-1-57b R_glass 英制", Rg * conv, 0.023, rel=0.03)
check("sc-1-57b R_air 英制", Ra * conv, 0.22, rel=0.03)
# (c) 串聯：用 sympy 解中間溫度並求總 R
T1, T3, R1, R2, A_ = sp.symbols("T1 T3 R1 R2 A", positive=True)
T2 = sp.symbols("T2")
sol = sp.solve(sp.Eq((T2 - T1) / R1, (T3 - T2) / R2), T2)[0]
Rtot = sp.simplify((T3 - T1) / ((T3 - sol) / R2))
print("sc-1-57c R_total =", Rtot)
if sp.simplify(Rtot - (R1 + R2)) != 0:
    fails.append("sc-1-57c")
Rt = Rg + 2 * Ra
check("sc-1-57d R_total SI", Rt, 0.0809)
check("sc-1-57d R_total 英制", Rt * conv, 0.46)
check("sc-1-57d Q/Δt", 20 / Rt, 247)

# ---------- 1.58 ----------
R358 = 3.5 * 0.0254 / 0.026
check("sc-1-58 R SI", R358, 3.42)
check("sc-1-58 R 英制", R358 * conv, 19.4)
check("sc-1-58 兩層靜止空氣 英制", 2 * Ra * conv, 0.44, rel=0.03)

# ---------- 1.59 ----------
walls = 95 / 2.3
roof = 120 / 5.3
floor = 120 / 3.5
win = 15 / 0.35
tot = walls + roof + floor + win
check("sc-1-59 牆 A/R", walls, 41.3)
check("sc-1-59 屋頂 A/R", roof, 22.6)
check("sc-1-59 地板 A/R", floor, 34.3)
check("sc-1-59 窗 A/R", win, 42.9)
check("sc-1-59 總 A/R", tot, 141)
P59 = tot * 25
check("sc-1-59 功率", P59, 3530, rel=0.01)
E59 = P59 * 30 * 24 * 3600
check("sc-1-59 一個月能量 J", E59, 9.15e9, rel=0.01)
kWh = E59 / 3.6e6
check("sc-1-59 kWh", kWh, 2540, rel=0.01)
check("sc-1-59 電費 $", kWh * 0.07, 178, rel=0.01)
therm = 1e5 * Btu
check("sc-1-59 1 therm J", therm, 1.055e8, rel=0.01)
check("sc-1-59 therms", E59 / therm, 86.7, rel=0.01)
check("sc-1-59 瓦斯費 $", E59 / therm * 0.5, 43.4, rel=0.01)

# ---------- 1.60 ----------
rho, c, kti = 7900.0, 450.0, 80.0
dt60 = rho * c * 0.1 ** 2 * 40 / (kti * 160)
check("sc-1-60 兩段模型 Δt", dt60, 111)
K = kti / (rho * c)
check("sc-1-60 K", K, 2.25e-5)
# 精確解：x=0 固定 200°C、x=L 絕熱（無側面散熱），初溫 20°C；用鏡像級數求末端升溫 40 K 的時間
from math import erfc
L = 0.2


def rise_end(t):
    s = 0.0
    for n in range(0, 30):
        s += (-1) ** n * 2 * erfc((2 * n + 1) * L / (2 * math.sqrt(K * t)))
    return 180 * s


lo, hi = 1.0, 1e5
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if rise_end(mid) < 40:
        lo = mid
    else:
        hi = mid
check("sc-1-60 精確解（絕熱末端）", lo, 350, rel=0.03)
# 用有限差分再驗一次
N = 200
dx = L / N
x = np.linspace(0, L, N + 1)
T = np.full(N + 1, 20.0)
T[0] = 200.0
dtn = 0.4 * dx * dx / K
t = 0.0
while T[-1] < 60.0:
    Tn = T.copy()
    Tn[1:-1] = T[1:-1] + K * dtn / dx ** 2 * (T[2:] - 2 * T[1:-1] + T[:-2])
    Tn[-1] = T[-1] + K * dtn / dx ** 2 * 2 * (T[-2] - T[-1])
    T = Tn
    t += dtn
check("sc-1-60 有限差分", t, 350, rel=0.03)
check("sc-1-60 L²/K", L ** 2 / K, 1780, rel=0.01)

# ---------- 1.61 ----------
q61 = 2.5 * 20 / 1000
check("sc-1-61 每平方公尺", q61, 0.05)
Aearth = 4 * math.pi * 6.4e6 ** 2
check("sc-1-61 地表面積", Aearth, 5.15e14, rel=0.01)
check("sc-1-61 總熱流", q61 * Aearth, 2.6e13)

# ---------- 1.62 熱方程與解 ----------
xs, ts, Ks, Aa, T0 = sp.symbols("x t K A T0", positive=True)
Tsol = T0 + Aa / sp.sqrt(ts) * sp.exp(-xs ** 2 / (4 * Ks * ts))
res = sp.simplify(sp.diff(Tsol, ts) - Ks * sp.diff(Tsol, xs, 2))
print("sc-1-62 熱方程殘差 =", res)
if res != 0:
    fails.append("sc-1-62 解")
area = sp.simplify(sp.integrate(Tsol - T0, (xs, -sp.oo, sp.oo)))
print("sc-1-62 ∫(T−T0)dx =", area)
if sp.simplify(area - 2 * Aa * sp.sqrt(sp.pi * Ks)) != 0:
    fails.append("sc-1-62 面積")
# 半高寬：e^{-x²/4Kt}=1/2 → x=√(4Kt ln2)
check("sc-1-62 半高半寬係數 √(4 ln2)", math.sqrt(4 * math.log(2)), 1.665)

# ---------- 1.63 ----------
P63 = k * 300 / (4 * math.pi * (1.5e-10) ** 2 * 0.1)
check("sc-1-63 P (Pa)", P63, 0.147)
check("sc-1-63 P (atm)", P63 / atm, 1.45e-6)

# ---------- 1.64 ----------
m_he = 4.0026 * u
v_he = math.sqrt(3 * k * 300 / m_he)
check("sc-1-64 v_rms He", v_he, 1370, rel=0.01)
m_air = 29 * u
v_air = math.sqrt(3 * k * 300 / m_air)
check("sc-1-64 v_rms air", v_air, 508, rel=0.01)
ell_he = VN / (4 * math.pi * (1.0e-10) ** 2)
check("sc-1-64 ℓ He", ell_he, 3.25e-7)
cvV_he = 1.5 * atm / 300
check("sc-1-64 CV/V He", cvV_he, 507, rel=0.01)
kt_he = 0.5 * cvV_he * ell_he * v_he
check("sc-1-64 kt He", kt_he, 0.113, rel=0.03)
check("sc-1-64 與空氣比", kt_he / 0.026, 4.3, rel=0.04)
ratio = (1.5 / 1.0) ** 2 * math.sqrt(29 / 4.0026) * 3 / 5
check("sc-1-64 因子相乘", ratio, 3.6, rel=0.03)

# ---------- 1.65 ----------
ell65 = 2 * 0.026 / (833 * 508)
check("sc-1-65 ℓ", ell65, 1.23e-7)
Vliq = 0.028 / 807  # 液態氮莫耳體積
check("sc-1-65 液氮莫耳體積", Vliq, 3.47e-5)
Vgas = Rgas * 300 / atm
check("sc-1-65 氣體莫耳體積", Vgas, 0.0246)
r65 = math.pi / 2 * ell65 * Vliq / Vgas
check("sc-1-65 r", r65, 2.72e-10)
NA65 = Vliq / (2 * r65) ** 3
check("sc-1-65 N_A 估計", NA65, 2.2e23, rel=0.05)
# 另一條路：由 ℓ 與 r 直接 N/V_gas
check("sc-1-65 一致性 N_A=V_gas/(4πr²ℓ)", Vgas / (4 * math.pi * r65 ** 2 * ell65), 2.2e23, rel=0.05)

# ---------- 1.66 ----------
rho_air = atm * 0.029 / (Rgas * 300)
check("sc-1-66 ρ_air", rho_air, 1.18)
eta = 0.5 * rho_air * 1.5e-7 * 500
check("sc-1-66 η", eta, 4.4e-5)
check("sc-1-66 η/η_exp", eta / 19e-6, 2.3, rel=0.03)
check("sc-1-66 ρℓ=m/(4πr²)", rho_air * VN / (4 * math.pi * (1.5e-10) ** 2), m_air / (4 * math.pi * (1.5e-10) ** 2), rel=0.02)

# ---------- 1.67 ----------
check("sc-1-67 Δx", math.sqrt(1e-9 * 60), 2.4e-4, rel=0.03)

# ---------- 1.68 ----------
dt68 = 5 ** 2 / 2e-5
check("sc-1-68 Δt", dt68, 1.25e6)
check("sc-1-68 天", dt68 / 86400, 14.5, rel=0.01)

# ---------- 1.69 ----------
Dd, n0, a = sp.symbols("D n0 a", positive=True)
nsol = n0 + a / sp.sqrt(ts) * sp.exp(-xs ** 2 / (4 * Dd * ts))
res = sp.simplify(sp.diff(nsol, ts) - Dd * sp.diff(nsol, xs, 2))
print("sc-1-69 Fick 第二定律殘差 =", res)
if res != 0:
    fails.append("sc-1-69")
# 均方位移 <x²> = 2Dt
w = sp.exp(-xs ** 2 / (4 * Dd * ts))
msd = sp.simplify(sp.integrate(xs ** 2 * w, (xs, -sp.oo, sp.oo)) / sp.integrate(w, (xs, -sp.oo, sp.oo)))
print("sc-1-69 <x²> =", msd)
if sp.simplify(msd - 2 * Dd * ts) != 0:
    fails.append("sc-1-69 msd")

# ---------- 1.70 ----------
check("sc-1-70 D", 0.5 * 1.5e-7 * 500, 3.75e-5)
check("sc-1-70 D/D_exp", 3.75e-5 / 2e-5, 1.9, rel=0.02)
check("sc-1-70 2^(3/2)", 2 ** 1.5, 2.83)

# ---------- 自編 t1-self-07a 結冰 ----------
kice, rice, Lf = 2.2, 917.0, 3.33e5
t10 = rice * Lf * 0.1 ** 2 / (2 * kice * 10)
check("t1-self-07a t(10 cm) s", t10, 6.94e4)
check("t1-self-07a t(10 cm) h", t10 / 3600, 19.3)
check("t1-self-07a t(20 cm) h", 4 * t10 / 3600, 77.1)
check("t1-self-07a 10→20 cm h", 3 * t10 / 3600, 57.8)
check("t1-self-07a 顯熱/潛熱", 2100 * 5 / Lf, 0.032, rel=0.03)
Kice = kice / (rice * 2100)
check("t1-self-07a K_ice", Kice, 1.14e-6)
check("t1-self-07a x²/K (h)", 0.1 ** 2 / Kice / 3600, 2.43)
# 數值積分 dx/dt = kΔT/(ρ L x) 驗 √t 律
xx, tt, h = 1e-4, rice * Lf * 1e-8 / (2 * kice * 10), 1.0
while xx < 0.1:
    xx += kice * 10 / (rice * Lf * xx) * h
    tt += h
check("t1-self-07a 數值積分", tt, 6.94e4, rel=0.01)

# ---------- 自編 t1-self-07b 由 η 推 kt 與 D ----------
cv_mass = 2.5 * k / m_air
check("t1-self-07b c_V", cv_mass, 717)
kt_pred = 19e-6 * cv_mass
check("t1-self-07b kt 預測", kt_pred, 0.0136)
check("t1-self-07b kt 實測/預測", 0.026 / kt_pred, 1.91, rel=0.02)
D_pred = 19e-6 / rho_air
check("t1-self-07b D 預測", D_pred, 1.61e-5)
check("t1-self-07b D 預測/實測", D_pred / 2e-5, 0.81, rel=0.02)
gam = 1.4
check("t1-self-07b Eucken 因子", (9 * gam - 5) / 4, 1.9)
check("t1-self-07b Eucken kt", (9 * gam - 5) / 4 * kt_pred, 0.0259, rel=0.01)
# 比值的推導（符號）
CVV, rho_s, l_s, v_s = sp.symbols("C_V/V rho ell v", positive=True)
print("t1-self-07b kt/η =", sp.simplify((CVV * l_s * v_s / 2) / (rho_s * l_s * v_s / 2)), "；D·ρ/η =", sp.simplify((l_s * v_s / 2) * rho_s / (rho_s * l_s * v_s / 2)))

# ---------- 正文與檢查欄裡另外提到的數字 ----------
check("sc-1-59 單層窗 A/R", 15 / Rt, 185, rel=0.01)
check("sc-1-59 窗佔比", win / tot, 0.30, rel=0.03)
check("sc-1-61 太陽 240 W/m² ÷ 地熱", 240 / q61, 4800)
ell_he85 = VN / (4 * math.pi * (0.85e-10) ** 2)
check("sc-1-64 r=0.85Å 時 kt", 0.5 * cvV_he * ell_he85 * v_he, 0.15, rel=0.05)
check("sc-1-65 N2 v_rms", math.sqrt(3 * Rgas * 300 / 0.028), 520, rel=0.01)
check("sc-1-62 半高全寬係數", 2 * math.sqrt(4 * math.log(2)), 3.33)
check("sc-ex-mfp 每秒碰撞次數", 1 / 3e-10, 3.3e9, rel=0.02)
check("sc-1-63 比例法", 1 / (0.1 / 1.5e-7), 1.5e-6)
check("sc-1-67 比例法", 1e7 / (0.1 / 2.45e-4) ** 2, 60, rel=0.05)
check("sc-1-68 一分鐘擴散距離", math.sqrt(2e-5 * 60), 0.035, rel=0.02)
check("sc-1-57 用錯 1 mm 玻璃", 20 / (1e-3 / 0.8 + 2 * Ra), 256, rel=0.01)
check("sc-1-57 玻璃溫降", 20 / Rt * Rg, 1.0, rel=0.02)
check("t1-self-07a t/(x²/K)=L/(2cΔT)", Lf / (2 * 2100 * 10), 7.9, rel=0.01)
check("t1-self-07b 單原子 Eucken 因子", (9 * 5 / 3 - 5) / 4, 2.5)
check("t1-window 圖 a=1 熱流", 20 / (0.004 + 2 * 1e-3 / 0.026), 247, rel=0.01)

print()
if fails:
    print("失敗：", fails)
    sys.exit(1)
print("全部通過")
