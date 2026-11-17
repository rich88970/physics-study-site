"""熱學第 1 章 §1.3–1.5（代理 B）所有題目卡的數值／符號驗算。

python tools/verify_thermal_ch01_B.py
常數：k = 1.381e-23 J/K、R = 8.315 J/(mol·K)、N_A = 6.022e23、1 atm = 1.013e5 Pa、u = 1.6605e-27 kg、g = 9.8 m/s²。
交叉核對：Schroeder 解答手冊（取 1 atm = 1e5 Pa 的數字另外檢查）、熱學小考（上）答案卷（1.24、1.39、1.40）。
"""
import math
import sympy as sp

k, R, NA, atm, u, g = 1.381e-23, 8.315, 6.022e23, 1.013e5, 1.6605e-27, 9.8
L = 1e-3
fails = 0


def check(name, got, want, rtol=5e-3):
    global fails
    ok = abs(got - want) <= rtol * abs(want) if want != 0 else abs(got) < 1e-12
    print(("PASS" if ok else "FAIL"), name, f"got={got:.6g}", f"want={want:.6g}")
    if not ok:
        fails += 1


def same(name, a, b):
    global fails
    ok = sp.simplify(a - b) == 0
    print(("PASS" if ok else "FAIL"), name)
    if not ok:
        fails += 1


T0 = 300.0
# ================= §1.3 =================
# sc-ex-dof：一莫耳在 300 K
check("sc-ex-dof He 3/2 RT", 1.5 * R * T0, 3742, 1e-3)
check("sc-ex-dof air 5/2 RT", 2.5 * R * T0, 6236, 1e-3)
check("sc-ex-dof solid 3 RT", 3 * R * T0, 7484, 1e-3)
check("sc-ex-dof 1/2 kT (J)", 0.5 * k * T0, 2.07e-21)
check("sc-ex-dof 1/2 kT (eV)", 0.5 * k * T0 / 1.602e-19, 0.0129, 1e-2)

# sc-1-23：U = f/2 PV
PV = atm * L
check("sc-1-23 PV (J)", PV, 101.3, 1e-3)
check("sc-1-23 He 3/2 PV", 1.5 * PV, 152, 1e-2)
check("sc-1-23 air 5/2 PV", 2.5 * PV, 253, 1e-2)
check("sc-1-23 SM (P=1e5) He", 1.5 * 1e5 * L, 150)
check("sc-1-23 SM (P=1e5) air", 2.5 * 1e5 * L, 250)
check("sc-1-23 N (molecules)", PV / (k * T0), 2.45e22, 1e-2)

# sc-1-24：一克鉛，f=6
n_pb = 1 / 207.2
check("sc-1-24 n (mol)", n_pb, 4.83e-3, 1e-2)
check("sc-1-24 U = 3nRT", 3 * n_pb * R * T0, 36.1, 3e-3)
check("sc-1-24 小考答案卷 36.15 J (M=207)", 3 * (1 / 207) * R * T0, 36.15, 1e-3)

# sc-1-25：水蒸氣 3+3+2*3 = 12
check("sc-1-25 dof", 3 + 3 + 2 * 3, 12)
check("sc-1-25 room-temp effective (3+3)", 3 + 3, 6)

# tk1-114-2：v_rms
mH2 = 2.016 * u
mO2 = 32.00 * u
vH = math.sqrt(3 * k * T0 / mH2)
vO = math.sqrt(3 * k * T0 / mO2)
check("tk1-114-2 v_rms H2 300K", vH, 1927, 2e-3)
check("tk1-114-2 v_rms O2 300K", vO, 484, 2e-3)
check("tk1-114-2 ratio", vH / vO, 3.98, 2e-3)
check("tk1-114-2 ratio sqrt(32/2)=4", math.sqrt(32 / 2), 4)
check("tk1-114-2 v_rms H2 293K", math.sqrt(3 * k * 293 / mH2), 1904, 2e-3)

# t1-self-03a：AFM 懸臂
ks, mc = 0.05, 1e-11
xr = math.sqrt(k * T0 / ks)
vr = math.sqrt(k * T0 / mc)
check("t1-self-03a kT", k * T0, 4.143e-21, 1e-3)
check("t1-self-03a x_rms (m)", xr, 2.88e-10, 2e-3)
check("t1-self-03a v_rms (m/s)", vr, 2.04e-5, 3e-3)
w = math.sqrt(ks / mc)
check("t1-self-03a omega", w, 7.07e4, 1e-3)
check("t1-self-03a v/x = omega", vr / xr, w, 1e-9)
check("t1-self-03a f0 (Hz)", w / (2 * math.pi), 1.125e4, 2e-3)
check("t1-self-03a x_rms at 4 K", math.sqrt(k * 4 / ks), 3.32e-11, 3e-3)
check("t1-self-03a stiffness for 0.01 nm", k * T0 / (1e-11) ** 2, 41.4, 3e-3)

# t1-self-03b：1 mol He 400 K + 1 mol N2 250 K（剛性絕熱容器、導熱固定隔板）
Tf = (3 * 400 + 5 * 250) / 8
check("t1-self-03b T_f", Tf, 306.25, 1e-6)
Qhe = 1.5 * R * (Tf - 400)
Qn2 = 2.5 * R * (Tf - 250)
check("t1-self-03b Q_He", Qhe, -1169, 1e-3)
check("t1-self-03b Q_N2", Qn2, 1169, 1e-3)
check("t1-self-03b Q sum 0", Qhe + Qn2 + 1, 1, 1e-9)
check("t1-self-03b v_rms He / N2", math.sqrt(28.0 / 4.0), 2.646, 1e-3)
check("t1-self-03b v_rms He at Tf", math.sqrt(3 * R * Tf / 4.003e-3), 1381, 2e-3)
check("t1-self-03b v_rms N2 at Tf", math.sqrt(3 * R * Tf / 28.01e-3), 522, 2e-3)
check("t1-self-03b naive average (wrong)", (400 + 250) / 2, 325)

# tk1x-1b：只有敘述；1(a) 的 3/2 kT = 3 × 1/2 kT
check("tk1x-1b 3*(1/2)", 3 * 0.5, 1.5)

# ================= §1.4 =================
# sc-ex-cal
check("sc-ex-cal 1 kg at 1 m/s KE", 0.5 * 1 * 1 ** 2, 0.5)
check("sc-ex-cal 1 Cal = 4184 J", 1000 * 4.184, 4184)
check("sc-ex-cal 1 kg water 1 K", 1000 * 4.184, 4184)
check("sc-ex-cal 4184 J lift 1 kg (m)", 4184 / (1 * 9.8), 427, 1e-3)

# sc-1-28：200 g 水 20→100°C，600 W
Q28 = 200 * 4.186 * 80
check("sc-1-28 energy (J)", Q28, 66976, 1e-4)
check("sc-1-28 time (s)", Q28 / 600, 111.6, 1e-3)
check("sc-1-28 SM 110 s", 67000 / 600, 110, 2e-2)

# sc-1-29
check("sc-1-29 ΔU (J)", 200 * 4.186 * 5, 4186, 1e-4)
check("sc-1-29 ΔU (cal)", 200 * 1 * 5, 1000)

# sc-1-30：每半次搖晃水走 0.3 m、0.125 s
v30 = 0.3 / 0.125
dT_half = v30 ** 2 / (2 * 4186)
check("sc-1-30 v (m/s)", v30, 2.4)
check("sc-1-30 ΔT per half-shake", dT_half, 6.88e-4, 2e-3)
check("sc-1-30 per minute (8 half-shakes/s)", dT_half * 8 * 60, 0.33, 1e-2)
check("sc-1-30 10 minutes", dT_half * 8 * 600, 3.3, 1e-2)

# t1-self-04a：Joule 落錘
W4 = 20 * 2.0 * g * 1.5
check("t1-self-04a W (J)", W4, 588)
check("t1-self-04a ΔT water 0.5 kg", W4 / (0.5 * 4186), 0.281, 2e-3)
check("t1-self-04a ΔT in cal", W4 / 4.184 / 500, 0.281, 2e-3)

# t1-self-04b：系統邊界
Qa, Wa = 500 - 100, -200
check("t1-self-04b system gas: ΔU", Qa + Wa, 200)
Qb, Wb = -100, 500 - 200
check("t1-self-04b system gas+resistor: ΔU", Qb + Wb, 200)
check("t1-self-04b engineering W_by=200, Q=400", 400 - 200, 200)

# ================= §1.5 =================
check("sc-ex-100j W = PΔV (P=1e5)", 1e5 * 1e-3, 100)
check("sc-ex-100j W (P=1.013e5)", atm * 1e-3, 101.3, 1e-3)

# sc-ex-isotherm：符號
N_, k_, T_, Vi, Vf, V = sp.symbols("N k T V_i V_f V", positive=True)
Wiso = -sp.integrate(N_ * k_ * T_ / V, (V, Vi, Vf))
same("sc-ex-isotherm W = NkT ln(Vi/Vf)", sp.expand_log(Wiso, force=True), sp.expand_log(N_ * k_ * T_ * sp.log(Vi / Vf), force=True))
check("sc-ex-isotherm 1 L air halved: W = PV ln2", PV * math.log(2), 70.2, 2e-3)

# sc-ex-adiabat：f/2 dT/T = -dV/V ⇒ V T^{f/2} 常數 ⇒ P V^γ 常數
f_, Ti, Tf_ = sp.symbols("f T_i T_f", positive=True)
Tsol = Ti * (Vi / Vf) ** (2 / f_)
same("sc-ex-adiabat V T^{f/2} const", sp.simplify(Vf * Tsol ** (f_ / 2) - Vi * Ti ** (f_ / 2)), 0)
Pi_ = N_ * k_ * Ti / Vi
Pf_ = N_ * k_ * Tsol / Vf
gam = (f_ + 2) / f_
same("sc-ex-adiabat P V^γ const", sp.simplify(sp.powsimp(Pf_ * Vf ** gam / (Pi_ * Vi ** gam), force=True)), 1)

# sc-1-31：P ∝ V，1 L、1 atm → 3 L
W31 = -0.5 * (3 ** 2 - 1 ** 2)          # atm·L
check("sc-1-31 W (atm·L)", W31, -4)
check("sc-1-31 W (J)", W31 * atm * L, -405.2, 1e-3)
dU31 = 1.5 * (3 * 3 - 1 * 1)
check("sc-1-31 ΔU (atm·L)", dU31, 12)
check("sc-1-31 ΔU (J)", dU31 * atm * L, 1215.6, 1e-3)
check("sc-1-31 Q (J)", (dU31 - W31) * atm * L, 1620.8, 1e-3)
check("sc-1-31 SM (1e5) W,ΔU,Q", (-4 + 12 + 16) * 100, 2400)
check("sc-1-31 T_f / T_i", 9.0, 9.0)

# tk1-114-7：1 L、1 atm(≈1e5) → 4 L
W7 = -0.5 * (4 ** 2 - 1)
check("tk1-114-7 W (atm·L)", W7, -7.5)
check("tk1-114-7 W (J, 1e5)", W7 * 1e5 * L, -750)
dU7 = 1.5 * (4 * 4 - 1)
check("tk1-114-7 ΔU (J, 1e5)", dU7 * 1e5 * L, 2250)
check("tk1-114-7 Q (J, 1e5)", (dU7 - W7) * 1e5 * L, 3000)
check("tk1-114-7 W (J, 1.013e5)", W7 * atm * L, -759.8, 1e-3)
check("tk1-114-7 ΔU (J, 1.013e5)", dU7 * atm * L, 2279, 1e-3)

# sc-1-32：水 1 L 壓到 99%，壓力 1 → 200 atm
W32 = 0.5 * (1 + 200) * atm * 0.01 * L
check("sc-1-32 W (J)", W32, 101.8, 2e-3)
check("sc-1-32 lift height of 10 kg", W32 / (10 * g), 1.04, 1e-2)

# sc-1-34：f = 5，矩形循環（符號）
P1, P2, V1, V2 = sp.symbols("P_1 P_2 V_1 V_2", positive=True)
steps = {"A": ((P1, V1), (P2, V1)), "B": ((P2, V1), (P2, V2)), "C": ((P2, V2), (P1, V2)), "D": ((P1, V2), (P1, V1))}
tot = [0, 0, 0]
for s, ((pa, va), (pb, vb)) in steps.items():
    Wst = -pa * (vb - va) if pa == pb else 0
    dU = sp.Rational(5, 2) * (pb * vb - pa * va)
    Q = dU - Wst
    tot = [tot[0] + Wst, tot[1] + dU, tot[2] + Q]
    print("     ", s, "W =", sp.factor(Wst), " ΔU =", sp.factor(dU), " Q =", sp.factor(Q))
same("sc-1-34 net W = -(P2-P1)(V2-V1)", tot[0], -(P2 - P1) * (V2 - V1))
same("sc-1-34 net ΔU = 0", tot[1], 0)
same("sc-1-34 net Q = (P2-P1)(V2-V1)", tot[2], (P2 - P1) * (V2 - V1))
same("sc-1-34 B: Q = 7/2 P2 (V2-V1)", sp.Rational(5, 2) * (P2 * V2 - P2 * V1) + P2 * (V2 - V1), sp.Rational(7, 2) * P2 * (V2 - V1))

# sc-1-33：U = f/2 PV 的正負（數值例：V 1→2，P 1→2，C 沿直線回 (1,1)）
cyc = [((1, 1), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (1, 1))]
signs = []
for (va, pa), (vb, pb) in cyc:
    Wst = -0.5 * (pa + pb) * (vb - va)
    dU = 1.5 * (pb * vb - pa * va)
    signs.append((math.copysign(1, Wst) if Wst else 0, math.copysign(1, dU), math.copysign(1, dU - Wst)))
check("sc-1-33 A signs (W-,U+,Q+)", signs[0][0] * 100 + signs[0][1] * 10 + signs[0][2], -100 + 10 + 1)
check("sc-1-33 B signs (W0,U+,Q+)", signs[1][0] * 100 + signs[1][1] * 10 + signs[1][2], 0 + 10 + 1)
check("sc-1-33 C signs (W+,U-,Q-)", signs[2][0] * 100 + signs[2][1] * 10 + signs[2][2], 100 - 10 - 1)
Wnet = sum(-0.5 * (pa + pb) * (vb - va) for (va, pa), (vb, pb) in cyc)
check("sc-1-33 net W = enclosed area 0.5", Wnet, 0.5)

# sc-1-35：符號
P_, C_ = sp.symbols("P C", positive=True)
same("sc-1-35 exponent (1+f/2)(2/f) = γ", sp.simplify((1 + f_ / 2) * (2 / f_)), (f_ + 2) / f_)

# sc-1-36：一公升空氣絕熱壓到 7 atm
gm = 7 / 5
Vf36 = 1.0 * (1 / 7) ** (1 / gm)
check("sc-1-36 V_f (L)", Vf36, 0.249, 2e-3)
r = (1 / Vf36) ** (gm - 1)
check("sc-1-36 (Vi/Vf)^{γ-1} = 7^{2/7}", r, 7 ** (2 / 7), 1e-12)
check("sc-1-36 7^{2/7}", 7 ** (2 / 7), 1.744, 1e-3)
W36 = atm * L / (gm - 1) * (r - 1)
check("sc-1-36 W (J)", W36, 188.3, 2e-3)
check("sc-1-36 W = ΔU = 5/2(PfVf-PiVi)", 2.5 * (7 * Vf36 - 1) * atm * L, W36, 1e-9)
check("sc-1-36 T_f (K)", 300 * r, 523, 2e-3)
check("sc-1-36 T_f via PV: 300*7*Vf", 300 * 7 * Vf36, 300 * r, 1e-9)

# sc-1-37：Diesel 20 倍
check("sc-1-37 20^{0.4}", 20 ** 0.4, 3.314, 1e-3)
check("sc-1-37 T_f (K)", 300 * 20 ** 0.4, 994, 2e-3)
check("sc-1-37 P_f (atm)", 20 ** 1.4, 66.3, 2e-3)

# sc-1-38：數值例：壓力比 2
check("sc-1-38 B grows ×2", 2.0, 2.0)
check("sc-1-38 A grows ×2^{5/7}", 2 ** (5 / 7), 1.64, 3e-3)
check("sc-1-38 A temperature ratio 2^{-2/7}", 2 ** (-2 / 7), 0.820, 2e-3)

# sc-1-39
V_, Cc = sp.symbols("V C", positive=True)
Piso = N_ * k_ * T_ / V_
same("sc-1-39 B_iso = P", -V_ * sp.diff(Piso, V_), Piso)
gs = sp.symbols("gamma", positive=True)
Pad = Cc / V_ ** gs
same("sc-1-39 B_ad = γP", sp.simplify(-V_ * sp.diff(Pad, V_)), gs * Pad)
M_air = 0.029
cs = math.sqrt(1.4 * R * T0 / M_air)
check("sc-1-39 c_s air 300K", cs, 347, 2e-3)
check("sc-1-39 小考 347.02", cs, 347.02, 1e-3)
vr_air = math.sqrt(3 * R * T0 / M_air)
check("sc-1-39 v_rms air", vr_air, 508, 2e-3)
check("sc-1-39 ratio sqrt(3/1.4)", vr_air / cs, 1.464, 1e-3)
check("sc-1-39 c_s at 273 K", math.sqrt(1.4 * R * 273 / M_air), 331, 2e-3)

# sc-1-40：乾絕熱遞減率
Tq, Pq = sp.symbols("T P", positive=True)
# 由 T ∝ P^{2/(f+2)}（P V^γ、PV=NkT 消去 V）驗 dT/dP
Tfun = Cc * Pq ** (2 / (f_ + 2))
same("sc-1-40(a) dT/dP = 2/(f+2) T/P", sp.simplify(sp.diff(Tfun, Pq) - 2 / (f_ + 2) * Tfun / Pq), 0)
lapse = -(2 / 7) * M_air * g / R
check("sc-1-40(b) dT/dz (K/m)", lapse, -9.77e-3, 2e-3)
check("sc-1-40 小考答案卷 -9.765 K/km", lapse * 1000, -9.765, 1e-3)

# tk1x-1e：γ = C_P/C_V，C_P = C_V + Nk ⇒ Nk/C_V = γ - 1
CV = sp.symbols("C_V", positive=True)
same("tk1x-1e Nk/C_V = γ-1", (CV + N_ * k_) / CV - 1, N_ * k_ / CV)
check("tk1x-1e γ monatomic 5/3", (2.5) / (1.5), 5 / 3, 1e-12)

# t1-self-05a：1 L 空氣 1 atm 300 K 壓到 1/10
Wiso10 = PV * math.log(10)
check("t1-self-05a isothermal W (J)", Wiso10, 233.3, 2e-3)
r10 = 10 ** 0.4
Wad10 = PV / 0.4 * (r10 - 1)
check("t1-self-05a 10^{0.4}", r10, 2.512, 1e-3)
check("t1-self-05a adiabatic W (J)", Wad10, 382.9, 2e-3)
check("t1-self-05a T after adiabatic", 300 * r10, 753.6, 1e-3)
check("t1-self-05a P after adiabatic (atm)", 10 ** 1.4, 25.1, 2e-3)
check("t1-self-05a P after cooling (atm)", 10.0, 10.0)
check("t1-self-05a heat released when cooling = W_ad", 2.5 * (10 ** 1.4 * 0.1 - 10 * 0.1) * PV, Wad10, 1e-9)
check("t1-self-05a extra work", Wad10 - Wiso10, 149.6, 3e-3)
check("t1-self-05a isothermal Q", -Wiso10, -233.3, 2e-3)

# t1-self-05b：多方過程
nn = sp.symbols("n", positive=True)
Rs, dT = sp.symbols("R dT")
fq = sp.symbols("f", positive=True)
Cpoly = Rs * (fq / 2 - 1 / (nn - 1))
same("t1-self-05b C = R(1/(γ-1) - 1/(n-1))", Cpoly - Rs * (1 / ((fq + 2) / fq - 1) - 1 / (nn - 1)), 0)
same("t1-self-05b n=0 → C_P", Cpoly.subs(nn, 0), Rs * (fq / 2 + 1))
same("t1-self-05b n=γ → 0", sp.simplify(Cpoly.subs(nn, (fq + 2) / fq)), 0)
same("t1-self-05b n→∞ → C_V", sp.limit(Cpoly, nn, sp.oo), Rs * fq / 2)
same("t1-self-05b n=-1 (P∝V) He → 2R", Cpoly.subs({nn: -1, fq: 3}), 2 * Rs)
check("t1-self-05b check vs sc-1-31: Q/(NkΔT)", 1620.8 / (8 * atm * L), 2.0, 1e-3)
ΔT = -30.0
dU5 = 2.5 * R * ΔT
W5 = R * ΔT / (1.2 - 1)
Q5 = dU5 - W5
check("t1-self-05b ΔU (J)", dU5, -623.6, 1e-3)
check("t1-self-05b W (J)", W5, -1247.3, 1e-3)
check("t1-self-05b Q (J)", Q5, 623.6, 1e-3)
check("t1-self-05b C = Q/ΔT", Q5 / ΔT, -20.79, 1e-3)
check("t1-self-05b C/R = 2.5 - 5", Q5 / ΔT / R, -2.5, 1e-9)
check("t1-self-05b V_f/V_i = (300/270)^{1/(n-1)}", (300 / 270) ** (1 / 0.2), 1.694, 2e-3)

# ================= 圖解說明裡的數字（figures-B.js） =================
check("t1-dof air 1 mol 300K", 2.5 * R * 300, 6236, 1e-3)
check("t1-pv-work const P W (atm·L)", -(3 - 1) * 1, -2)
check("t1-pv-work isotherm 3 ln3 (atm·L)", 3 * math.log(3), 3.30, 2e-3)
check("t1-pv-work adiabat W (atm·L)", 3 / 0.4 * (3 ** 0.4 - 1), 4.14, 2e-3)
check("t1-adiabat 1.36 T at r=4.01", 300 * 4.01 ** 0.4, 523, 2e-3)
check("t1-adiabat He r=20", 300 * 20 ** (2 / 3), 2210, 2e-3)
check("t1-first-law 04b(a)", 400 - 200, 200)
# 其他正文數字
check("sc-1-36 P_f V_f (atm·L)", 7 * Vf36, 1.743, 1e-3)
check("sc-1-36 Vi/Vf", 1 / Vf36, 4.01, 2e-3)
check("sc-1-32 精確 (J)", 0.5 * 201 * atm * 1e-5, 102, 5e-3)
check("t1-self-05a P2 V_f (atm·L)", 10 ** 1.4 * 0.1, 2.512, 1e-3)
check("t1-self-05a W_ad (atm·L)", 2.5 * (10 ** 1.4 * 0.1 - 1), 3.78, 2e-3)
check("tk1-114-2 m_H2 (kg)", mH2, 3.348e-27, 1e-3)
check("sc-1-24 lead atoms in 1 g", NA / 207.2, 2.9e21, 1e-2)

print("ALL PASS" if fails == 0 else f"{fails} FAIL")
raise SystemExit(1 if fails else 0)
