"""熱學第 1 章 §1.6 熱容量（06-heat-capacity.html，代理 C）所有題目數值與符號答案的獨立重算。

用法：python -X utf8 tools/verify_thermal_ch01_C.py
每一題獨立從題目數據算起（不沿用網站的中間值）；代數與偏微分用 sympy。全部通過時最後印出 ALL CHECKS PASSED。
「網站」欄是 06-heat-capacity.html 上寫的數值；交叉核對的解答手冊數值寫在註解裡。
"""
import sys

import sympy as sp

FAIL = []

# 常數（題目沒給時網站用的標準值）
k = 1.381e-23        # J/K
R = 8.315            # J/(mol K)
NA = 6.022e23
cal = 4.186          # J/cal
c_w = 4.186          # J/(g K) 水
c_ice = 0.5 * cal    # J/(g K) 冰（題目 1.47 給 0.5 cal/g°C）
l_f = 333.0          # J/g 冰熔化
l_v = 2260.0         # J/g 水沸騰（100°C）
G = 6.674e-11
m_p = 1.673e-27
eV = 1.602e-19
atm = 1.013e5


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


# ---------- 課文：均分定理預測莫耳熱容量 ----------
check("sc-ex-6-cv 單原子 CV/mol=3R/2", 1.5 * R, 12.47)
check("sc-ex-6-cv 雙原子 CV/mol=5R/2", 2.5 * R, 20.79)
check("sc-ex-6-cv 雙原子含振動 7R/2", 3.5 * R, 29.10)
check("sc-ex-6-cv Dulong-Petit 3R", 3 * R, 24.94)
check("sc-ex-6-cv 1 g 水 CV=4.186 J/K", 1 * c_w, 4.186)

# ---------- 課文：CP = CV + Nk（sympy 偏微分） ----------
N_, kk, T_, P_, f_ = sp.symbols("N k T P f", positive=True)
V_of_TP = N_ * kk * T_ / P_
U_ = f_ / 2 * N_ * kk * T_
CP_expr = sp.diff(U_, T_) + P_ * sp.diff(V_of_TP, T_)
true("sc-ex-6-cpcv (∂V/∂T)_P = Nk/P", sp.simplify(sp.diff(V_of_TP, T_) - N_ * kk / P_) == 0)
true("sc-ex-6-cpcv CP - CV = Nk", sp.simplify(CP_expr - sp.diff(U_, T_) - N_ * kk) == 0)
true("sc-ex-6-cpcv gamma=(f+2)/f", sp.simplify(CP_expr / sp.diff(U_, T_) - (f_ + 2) / f_) == 0)
check("sc-ex-6-cpcv 單原子 CP/mol=5R/2", 2.5 * R, 20.79)

# ---------- 課文：沸騰一莫耳水 ----------
check("sc-ex-6-boil 每克 ΔH", 40660 / 18, 2259)
check("sc-ex-6-boil PV=RT at 373 K", R * 373, 3101, rel=0.005)
check("sc-ex-6-boil 比例", R * 373 / 40660, 0.0763, rel=0.01)
check("sc-ex-6-boil ΔU", 40660 - R * 373, 37560, rel=0.002)

# ---------- 1.41 ----------
Qw = 250 * c_w * (24 - 20)
check("1.41(a) Q_water", Qw, 4186)
check("1.41(c) C_metal", Qw / (100 - 24), 55.1)      # 手冊 55 J/°C
check("1.41(d) c_metal J/(g K)", Qw / (100 - 24) / 100, 0.551)  # 手冊 0.55

# ---------- 1.42 ----------
mw, mp_, cp_ = 1500, 340, 1.8
Tf = (mw * c_w * 100 + mp_ * cp_ * 25) / (mw * c_w + mp_ * cp_)
check("1.42 末溫", Tf, 93.3, rel=0.001)                 # 手冊 93.3°C
check("1.42 降溫", 100 - Tf, 6.7, rel=0.02)

# ---------- 1.43 ----------
C_molec = 18 * c_w / NA
check("1.43 每分子 C (J/K)", C_molec, 1.251e-22)
check("1.43 C/k", C_molec / k, 9.06)                   # 手冊 9.07k
check("1.43 f=2C/k", 2 * C_molec / k, 18.1)

# ---------- 1.44（預測值 vs 表） ----------
check("1.44 單原子 CP=5R/2", 2.5 * R, 20.79)
check("1.44 線形雙原子 CP=7R/2", 3.5 * R, 29.10)
check("1.44 非線形 CP=4R", 4 * R, 33.26)
check("1.44 固體 3R", 3 * R, 24.94)
check("1.44 NaCl 6R", 6 * R, 49.9)
check("1.44 CaCl2 9R", 9 * R, 74.8)
check("1.44 SiO2 9R", 9 * R, 74.8)
check("1.44 CaCO3 15R", 15 * R, 124.7)
check("1.44 Al2SiO5 24R", 24 * R, 199.6)
check("1.44 glucose 72R", 72 * R, 598.7)
check("1.44 H2O(l) 9R", 9 * R, 74.8)
check("1.44 CO2 若含 2 個彎曲振動 CP=7R/2+2R", 5.5 * R, 45.7)

# ---------- 1.45 ----------
x, y, z = sp.symbols("x y z", positive=True)
w_xy = x * y
w_xz = x**2 / z           # 由 y = x/z
w_yz = y**2 * z           # 由 x = yz
sub = {x: y * z}
true("1.45(a) w=x^2/z 與 w=y^2 z 一致", sp.simplify((w_xz - w_yz).subs(sub)) == 0)
true("1.45(b) (∂w/∂x)_y = y", sp.diff(w_xy, x) == y)
true("1.45(b) (∂w/∂x)_z = 2x/z = 2y", sp.simplify(sp.diff(w_xz, x).subs(sub) - 2 * y) == 0)
true("1.45(c) (∂w/∂y)_x = x", sp.diff(w_xy, y) == x)
true("1.45(c) (∂w/∂y)_z = 2yz = 2x", sp.simplify((sp.diff(w_yz, y) - 2 * x).subs(sub)) == 0)
true("1.45(c) (∂w/∂z)_x = -x^2/z^2 = -y^2", sp.simplify(sp.diff(w_xz, z).subs(sub) + y**2) == 0)
true("1.45(c) (∂w/∂z)_y = y^2", sp.diff(w_yz, z) == y**2)

# ---------- 1.46 ----------
V_ = N_ * kk * T_ / P_
beta = sp.simplify(sp.diff(V_, T_) / V_)
kap = sp.simplify(-sp.diff(V_, P_) / V_)
dPdT_V = sp.diff(N_ * kk * T_ / sp.Symbol("V", positive=True), T_)
true("1.46(d) β = 1/T", sp.simplify(beta - 1 / T_) == 0)
true("1.46(d) κ_T = 1/P", sp.simplify(kap - 1 / P_) == 0)
Vs = sp.Symbol("V", positive=True)
true("1.46(d) (∂P/∂T)_V = Nk/V = β/κ_T", sp.simplify((dPdT_V - beta / kap).subs(P_, N_ * kk * T_ / Vs)) == 0)
dP_w = 2.57e-4 / 4.52e-10 * 10
dP_hg = 1.81e-4 / 4.04e-11 * 10
check("1.46(e) 水 ΔP (Pa)", dP_w, 5.69e6)             # 手冊 5.69e6 Pa = 56 atm
check("1.46(e) 水 ΔP (atm)", dP_w / atm, 56.1)
check("1.46(e) 汞 ΔP (Pa)", dP_hg, 4.48e7)            # 手冊 4.48e7 Pa = 440 atm
check("1.46(e) 汞 ΔP (atm)", dP_hg / atm, 442)
# 小考答案卷：水寫成 5.611 atm（Pa→atm 換算錯一個 10 倍），汞 442 atm 正確
true("1.46 小考答案 5.611 atm 是換算錯誤", abs(dP_w * 9.8692e-6 - 56.1) < 0.2)

# ---------- 1.47 ----------
Q_tea = 200 * 1 * (100 - 65)                      # cal
per_g = 0.5 * 15 + 80 + 1 * 65                    # cal/g
check("1.47 Q (cal)", Q_tea, 7000)
check("1.47 每克冰吸熱 (cal/g)", per_g, 152.5)
check("1.47 冰 m (g)", Q_tea / per_g, 45.9)         # 手冊 46 g

# ---------- 115-1（換數字：100 g、60°C） ----------
Q115 = 100 * 1 * (100 - 60)
per115 = 0.5 * 15 + 80 + 1 * 60
check("115-1 Q (cal)", Q115, 4000)
check("115-1 每克冰 (cal/g)", per115, 147.5)
check("115-1 冰 m (g)", Q115 / per115, 27.1)        # 學生答案卷 27.12 g（10 分）

# ---------- 1.48 ----------
rho_ice = 917.0
E_melt = rho_ice * 1.0 * l_f * 1e3                # J/m^2（1 m^3 冰）
P_abs = 0.10 * 1000                               # W/m^2
E_day = P_abs * 8 * 3600
check("1.48 每平方公尺融冰能量 (J)", E_melt, 3.05e8)
check("1.48 每天吸收 (J)", E_day, 2.88e6)
check("1.48 天數", E_melt / E_day, 106)
check("1.48 週數", E_melt / E_day / 7, 15.1)
check("1.48 上限：全天日照的週數", E_melt / (P_abs * 86400) / 7, 5.05)

# ---------- 1.49 ----------
Wat = 1.5 * R * 298
check("1.49 大氣做功 (J)", Wat, 3717)
check("1.49 系統能量減少 (kJ)", 285.83 - Wat / 1e3, 282.1)

# ---------- 1.50 ----------
fH = dict(CH4=-74.81, CO2=-393.51, H2Og=-241.82, H2Ol=-285.83, glucose=-1273.0, H=217.97)
a = -fH["CH4"]
b = fH["CO2"] + 2 * fH["H2Og"]
c_ = a + b
check("1.50(a)", a, 74.81)
check("1.50(b)", b, -877.15)
check("1.50(c)", c_, -802.34)
cl = a + fH["CO2"] + 2 * fH["H2Ol"]
check("1.50(e) 液態水 ΔH", cl, -890.36)
check("1.50(e) 2RT (kJ)", 2 * R * 298 / 1e3, 4.956)
check("1.50(e) 液態水 ΔU", cl + 2 * R * 298 / 1e3, -885.40, rel=1e-4)
mol_sun = 2e30 / 0.080
E_sun = mol_sun * 802.34e3
t_sun = E_sun / 3.9e26
check("1.50(f) 莫耳數", mol_sun, 2.5e31)
check("1.50(f) 總能量 (J)", E_sun, 2.0e37)
check("1.50(f) 秒", t_sun, 5.1e10, rel=0.02)
check("1.50(f) 年", t_sun / 3.156e7, 1630, rel=0.01)  # 手冊約 1600 年
check("1.50(f) 只算甲烷質量的年數", 2e30 / 0.016 * 802.34e3 / 3.9e26 / 3.156e7, 8150, rel=0.01)

# ---------- 1.51 ----------
g1 = -fH["glucose"] + 6 * fH["CO2"] + 6 * fH["H2Ol"]
check("1.51 ΔH (液態水)", g1, -2803.0, rel=1e-4)      # 手冊 -2803 kJ
check("1.51 ΔH (水蒸氣)", -fH["glucose"] + 6 * fH["CO2"] + 6 * fH["H2Og"], -2539.0, rel=1e-4)
check("1.51 每克 (kJ/g)", 2803.0 / 180.16, 15.56)
check("1.51 每克 (kcal/g)", 2803.0 / 180.16 / cal, 3.72)

# ---------- 1.52（假設價格：汽油 NT$30/L，玉米片 NT$150/500 g） ----------
gas_cost = 30 * 3.8
cf_cost = 150 / 500 * 28
check("1.52 一加侖汽油 NT$", gas_cost, 114)
check("1.52 一盎司玉米片 NT$", cf_cost, 8.4)
check("1.52 汽油 NT$/kcal", gas_cost / 31000, 3.68e-3)
check("1.52 玉米片 NT$/kcal", cf_cost / 100, 0.084)
check("1.52 倍數", (cf_cost / 100) / (gas_cost / 31000), 22.8)

# ---------- 1.53 ----------
dU_H = fH["H"] - 0.5 * R * 298 / 1e3
check("1.53 PΔV (kJ)", 0.5 * R * 298 / 1e3, 1.239)
check("1.53 ΔU (kJ)", dU_H, 216.73, rel=1e-4)
e_diss = dU_H * 1e3 / (0.5 * NA)
check("1.53 每分子 (J)", e_diss, 7.198e-19, rel=0.002)
check("1.53 每分子 (eV)", e_diss / eV, 4.49, rel=0.002)  # 手冊 4.49 eV
check("1.53 若不扣 PΔV (eV)", fH["H"] * 1e3 / (0.5 * NA) / eV, 4.52, rel=0.002)

# ---------- 1.54 ----------
W_climb = 60 * 9.8 * 1500
food = W_climb / 0.25
check("1.54(a) mgh (J)", W_climb, 8.82e5)
check("1.54(a) mgh (kcal)", W_climb / 4186, 210.7)
check("1.54(a) 食物 (kcal)", food / 4186, 843)
check("1.54(a) 碗數", food / 4186 / 100, 8.43)       # 手冊 8.5 碗
heat = 0.75 * food
check("1.54(b) 熱 (kcal)", heat / 4186, 632)
check("1.54(b) ΔT (K)", heat / (60e3 * c_w), 10.5)   # 手冊 10.5°C
check("1.54(c) 蒸發水 (kg)", heat / 4186 / 580, 1.09)  # 手冊 1.1 kg

# ---------- 1.55 ----------
m, v, r = sp.symbols("m v r", positive=True)
Gs = sp.Symbol("G", positive=True)
# 兩顆質量 m、各距質心 r（相距 2r），Newton：G m^2/(2r)^2 = m v^2 / r
v2 = sp.solve(sp.Eq(Gs * m**2 / (2 * r) ** 2, m * v**2 / r), v**2)[0]
Kin = 2 * sp.Rational(1, 2) * m * v2
Pot = -Gs * m**2 / (2 * r)
true("1.55(a) U_pot = -2 U_kin", sp.simplify(Pot + 2 * Kin) == 0)
M, Rs = 2e30, 7e8
T155 = G * M * (0.5 * m_p) / (3 * k * Rs)
check("1.55(e) 太陽平均溫度 (K)", T155, 3.85e6)       # 手冊約 4e6 K
check("1.55(e) 粒子數 N=2M/m_p", 2 * M / m_p, 2.39e57)

# ---------- 某級第 4 題（均勻球 3/5） ----------
rho, rr, Mr = sp.symbols("rho rr M_r", positive=True)
Rsym = sp.Symbol("R", positive=True)
Msym = sp.Symbol("M", positive=True)
rho_val = Msym / (sp.Rational(4, 3) * sp.pi * Rsym**3)
dU = -Gs * (sp.Rational(4, 3) * sp.pi * rr**3 * rho_val) * (4 * sp.pi * rr**2 * rho_val) / rr
Upot_uniform = sp.integrate(dU, (rr, 0, Rsym))
true("tk1x-4(c) 均勻球 U = -3GM^2/(5R)", sp.simplify(Upot_uniform + sp.Rational(3, 5) * Gs * Msym**2 / Rsym) == 0)
T4 = G * M * m_p / (10 * k * Rs)
check("tk1x-4(d) 太陽平均溫度 (K)", T4, 2.31e6)
check("tk1x-4(d) 動能 3GM^2/(10R) (J)", 3 * G * M**2 / (10 * Rs), 1.144e41)
check("tk1x-4(d) 由 K=3/2 N k T 反推", 3 * G * M**2 / (10 * Rs) / (1.5 * (2 * M / m_p) * k), 2.31e6)

# ---------- 自編 06a：蒸汽通入冰 ----------
ms, mi = 20.0, 100.0
need_melt = mi * (c_ice * 20 + l_f)
cond = ms * l_v
check("06a 冰升到 0°C 並全熔 (J)", need_melt, 37480, rel=0.002)
check("06a 蒸汽全凝結放熱 (J)", cond, 45200)
check("06a 蒸汽凝結並降到 0°C (J)", ms * (l_v + c_w * 100), 53572, rel=0.001)
T06 = (ms * l_v + ms * c_w * 100 - mi * c_ice * 20 - mi * l_f) / ((ms + mi) * c_w)
check("06a 末溫 (°C)", T06, 32.0, rel=0.005)
true("06a 0 < 末溫 < 100", 0 < T06 < 100)
ms_c = mi * (c_ice * 20 + l_f + c_w * 100) / l_v
check("06a 臨界蒸汽量 (g)", ms_c, 35.1, rel=0.005)
check("06a 每克冰到 100°C 水 (J/g)", c_ice * 20 + l_f + c_w * 100, 793.5, rel=0.001)
W06 = ms / 18 * R * 373
check("06a 大氣做功 nRT (J)", W06, 3446, rel=0.002)
check("06a 佔凝結熱比例", W06 / cond, 0.0762, rel=0.01)

# ---------- 自編 06b：負熱容量恆星 ----------
L_sun = 3.9e26
Etot = G * M**2 / (2 * Rs)
check("06b |U_total| = GM^2/(2R) (J)", Etot, 1.907e41)
check("06b 時標 (s)", Etot / L_sun, 4.89e14)
check("06b 時標 (年)", Etot / L_sun / 3.156e7, 1.55e7)
check("06b 均勻球 時標 (年)", 3 * G * M**2 / (10 * Rs) / L_sun / 3.156e7, 9.3e6)
Nsun = 2 * M / m_p
check("06b dT/dt (K/年)", L_sun / (1.5 * Nsun * k) * 3.156e7, 0.249, rel=0.01)
# dT/dt / T = L/|U|：同一個時標
true("06b (dT/dt)/T = L/|U|", abs((L_sun / (1.5 * Nsun * k)) / T155 - L_sun / Etot) / (L_sun / Etot) < 0.01)

# ---------- 頁面上的其他中間值 ----------
check("1.41 水的熱容量 / 金屬熱容量", 250 * c_w / (Qw / 76), 19.0)
check("1.46 汞/水 壓力比", dP_hg / dP_w, 7.87)
check("1.46 κ_T 比", 4.52e-10 / 4.04e-11, 11.2)
check("1.49 1.5 mol 體積 (L)", 1.5 * R * 298 / 1e5 * 1e3, 37.2)
check("boil 蒸汽體積 (L)", R * 373 / atm * 1e3, 30.6)
check("1.55(e) m_p/2", m_p / 2, 8.37e-28, rel=0.002)
check("1.55(e) 分子", G * M * m_p / 2, 1.117e-7, rel=0.002)
check("1.55(e) 分母", 3 * k * Rs, 2.900e-14, rel=0.002)
check("tk1x-4 分子", G * M * m_p, 2.233e-7, rel=0.002)
check("tk1x-4 分母", 10 * k * Rs, 9.667e-14, rel=0.002)
check("06a 檢查：蒸汽放熱", ms * l_v + ms * c_w * (100 - T06), 50890, rel=0.001)
check("06a 檢查：冰吸熱", need_melt + mi * c_w * T06, 50890, rel=0.001)
check("06a l_v/l_f", l_v / l_f, 6.8, rel=0.01)
check("06b 3/2 N k (J/K)", 1.5 * Nsun * k, 4.95e34)
check("06b L/|U| (1/s)", L_sun / Etot, 2.0e-15, rel=0.03)
check("06b 時標/太陽年齡", Etot / L_sun / 3.156e7 / 4.6e9, 0.0034, rel=0.03)
check("1.54 cal 換算 10.5 kcal/kg", 0.75 * food / 4186 / 60, 10.5, rel=0.01)

print()
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("ALL CHECKS PASSED")
