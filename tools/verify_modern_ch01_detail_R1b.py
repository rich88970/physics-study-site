"""獨立驗算 modern/ch01 第 8–12 節詳細化後的數值，以及新增「相對論綜合難題」（12x-challenge.html）。

用法：python tools/verify_modern_ch01_detail_R1b.py
第一部分重算第 8–12 節題目卡上（含新寫出的中間值）的數字；
第二部分對綜合題 cx-01～cx-10 用和網站詳解不同的方法重算：
直接做勞倫茲轉換／矩陣、在地球座標系追光數訊號、數值積分雙曲運動、
把光子火箭拆成很多小脈衝、Monte Carlo 衰變與散射。全部通過才回傳 0。
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

C = 3.00e8
C4 = 2.998e8
FAIL = []
rng = np.random.default_rng(12345)


def g(b):
    return 1 / math.sqrt(1 - b * b)


def check(name, got, want, rel=0.01):
    ok = abs(got - want) <= rel * abs(want) if want != 0 else abs(got) < 1e-12
    print(f"{'OK ' if ok else 'BAD'} {name}: got {got:.6g}, site {want:.6g}")
    if not ok:
        FAIL.append(name)


def check_true(name, cond):
    print(f"{'OK ' if cond else 'BAD'} {name}")
    if not cond:
        FAIL.append(name)


def vadd(u, v):
    """一維速度合成（以 c 為單位）"""
    return (u + v) / (1 + u * v)


def boost(beta):
    """沿 x 的勞倫茲轉換矩陣，作用在 (ct, x, y)：S -> S'（S' 以 beta 沿 +x 運動）"""
    G = g(beta)
    return np.array([[G, -G * beta, 0], [-G * beta, G, 0], [0, 0, 1]])


def to_frame(beta, ct, x, y=0.0):
    return boost(beta) @ np.array([ct, x, y])


# =================== 第 8 節 ===================
check("kg-107-2 gamma", g(0.6), 1.25)
check("kg-107-2 M", g(0.6) * 20, 25)
check("ex1-7 4pi r^2", 4 * math.pi * (1.5e11) ** 2, 2.83e23)
P = 1.4e3 * 4 * math.pi * (1.5e11) ** 2
check("ex1-7 P", P, 4.0e26, 0.02)
check("ex1-7 dm/dt", P / (3.0e8) ** 2, 4.4e9)
check("1-27 E0", 1 * C ** 2, 9.0e16)
check("1-27 ratio", 5.4e6 / C ** 2, 6.0e-11)
check("1-28 mi", C ** 2 / 3.34e5, 2.69e11)
check("1-28 Lf/c2", 3.34e5 / C ** 2, 3.7e-12)
b29 = brentq(lambda b: g(b) - 1 - 1, 0, 0.999)
check("1-29 beta", b29, 0.866)
check("1-29 v", b29 * C, 2.60e8)
check("1-30 gamma", g(0.9), 2.294)
check("1-30 KE/m", (g(0.9) - 1) * C ** 2, 1.16e17)
check("1-30 classical", 0.5 * (0.9 * C) ** 2, 3.6e16, 0.02)
bcl = math.sqrt(2 * 0.1 / 0.511)
check("1-31 classical beta", bcl, 0.626)
check("1-31 classical v", bcl * C, 1.88e8)
G31 = 1 + 0.1 / 0.511
check("1-31 gamma", G31, 1.196)
check("1-31 1/g^2", 1 / G31 ** 2, 0.699, 0.003)
b31 = brentq(lambda b: (g(b) - 1) * 0.511 - 0.1, 0, 0.99)
check("1-31 beta (numeric)", b31, 0.548)
check("1-31 v", b31 * C, 1.64e8)
check("1-31 overestimate", bcl / b31, 1.14)
check("1-32 exact 10E0", math.sqrt(0.99), 0.994987, 1e-6)
check("1-32 21E0 approx", 1 - 0.5 / 441, 0.99887, 1e-5)
check("1-33 1-1/441", 1 - 1 / 441, 0.997732, 1e-6)
check("1-33 beta", math.sqrt(1 - 1 / 441), 0.99887, 1e-5)
for b, w in ((0.2, 0.02062), (0.4, 0.09109), (0.8, 0.6667)):
    check(f"1-34 gamma-1 at {b}", g(b) - 1, w, 0.002)
check("1-34 (a)", (g(0.4) - 1) / (g(0.2) - 1), 4.42)
check("1-34 (b)", (g(0.8) - 1) / (g(0.4) - 1), 7.32)
check("1-35 gamma1", g(1.2e8 / C), 1.091)
check("1-35 gamma2", g(2.4e8 / C), 1.667)
check("1-35 W", (g(0.8) - g(0.4)) * 0.511, 0.294)
check("1-35 classical", 0.5 * 0.511 * (0.64 - 0.16), 0.123)
check("1-36 sqrt", 1 - 1 / 2.25, 0.5556, 0.001)
check("1-36 gamma", 1.5 / math.sqrt(1.5 ** 2 - 1), 1.342)
check("1-36 KE", (1.5 / math.sqrt(1.25) - 1) * 0.511, 0.175)
Gs, bs = sp.symbols("gamma beta", positive=True)
diff = (Gs - 1 - sp.Rational(1, 2) * Gs * (1 - 1 / Gs ** 2)) - (Gs - 1) ** 2 / (2 * Gs)
check_true("1-37 identity KE - g m v^2/2 = (g-1)^2/(2g)", sp.simplify(diff) == 0)
check("1-37 at 0.8c", (5 / 3 - 1) ** 2 / (2 * 5 / 3), 0.133)
x = sp.symbols("x", positive=True)
low = sp.series(((1 / sp.sqrt(1 - x) - 1) ** 2 / (2 / sp.sqrt(1 - x))), x, 0, 3).removeO()
check_true("1-37 low-speed diff = beta^4/8", sp.simplify(low.coeff(x, 2) - sp.Rational(1, 8)) == 0)
M, m, L, S = sp.symbols("M m L S")
com = (M / 2 - m) * (-L / 2 - S) + (M / 2 + m) * (L / 2 - S)
check_true("1-39 COM expands to mL - MS", sp.expand(com - (m * L - M * S)) == 0)
# sf-08-1
p_tot = g(0.6) * 0.6
E_tot = g(0.6) + 1
V = p_tot / E_tot
Mf = math.sqrt(E_tot ** 2 - p_tot ** 2)
check("sf-08-1 V", V, 1 / 3)
check("sf-08-1 gammaV", g(V), 1.061)
check("sf-08-1 M", Mf, 2.121)
check("sf-08-1 KEf", (g(V) - 1) * Mf, 0.129)
check("sf-08-1 loss", 0.25 - (g(V) - 1) * Mf, 0.121)
Kx = brentq(lambda K: (1 + K) / math.sqrt(1 + K / 2) - 1.01, 1e-6, 0.1)
check("sf-08-2 K exact", Kx, 0.01337, 0.002)
check("sf-08-2 KE keV", Kx * 511, 6.83)
K25 = 25 / 511
check("sf-08-2 25kV ratio", (1 + K25) / math.sqrt(1 + K25 / 2), 1.036, 0.001)

# =================== 第 9 節 ===================
check("ex1-8 E", math.sqrt(0.511 ** 2 + 4), 2.064, 0.001)
mc2 = (335 ** 2 - 62 ** 2) / (2 * 62)
check("kg-107-3 mc2", mc2, 874)
check("kg-107-3 v/c", 335 / (62 + mc2), 0.358, 0.002)
check("kg-115-3 m^2", 4 ** 2 - 1.45 ** 2, 13.90, 0.001)
check("kg-115-3 mc2", math.sqrt(16 - 1.45 ** 2), 3.73)
check("kg-115-3 KE", 4 - math.sqrt(16 - 1.45 ** 2), 0.272)
check("kg-115-3 E'", math.sqrt(16 - 1.45 ** 2 + 4), 4.23)
E1 = sp.symbols("E1", positive=True)
mm = sp.symbols("m", positive=True)
pp = sp.sqrt(E1 ** 2 - mm ** 2)
sol = sp.solve(sp.Eq((E1 + mm) ** 2 - pp ** 2, 16 * mm ** 2), E1)
check_true("1-38 E1 = 7 m c^2", sp.simplify(sol[0] - 7 * mm) == 0)
check("1-38 KE MeV", 6 * 0.511, 3.07)
check("1-40 c^2", C4 ** 2, 8.988e16, 0.001)
check("1-40 MeV/c^2", 1.602e-13 / C4 ** 2, 1.783e-30, 0.001)
check("1-40 MeV/c", 1.602e-13 / C4, 5.344e-22, 0.001)
G41 = 1e5 * 365.25 * 24 * 60 / 5
check("1-41 gamma", G41, 1.1e10, 0.06)
check("1-41 E eV", G41 * 0.938e9, 1e19, 0.02)
check("1-41 1-beta", 1 / (2 * (1.1e10) ** 2), 4e-21, 0.05)
check("1-42 (pc)^2", 100 + 2 * 10 * 938, 18860)
check("1-42 pc", math.sqrt(18860), 137)
check("1-43 p", 1.25 * 0.511 * 0.6, 0.383)
check("1-43 E", 1.25 * 0.511, 0.639)
check("1-44 E", g(0.9) * 0.938, 2.15)
check("1-44 KE", g(0.9) * 0.938 - 0.938, 1.21)
check("1-44 p", g(0.9) * 0.938 * 0.9, 1.94)
check("1-45 pc keV", math.sqrt(3) * 511, 885)
check("1-45 SI", 0.885 * 5.344e-22, 4.73e-22)
check("1-47 gamma", 3.5 / 0.938, 3.731)
check("1-47 1/g^2", (0.938 / 3.5) ** 2, 0.0718, 0.002)
check("1-47 beta", math.sqrt(1 - (0.938 / 3.5) ** 2), 0.963)
check("1-47 0.938^2", 0.938 ** 2, 0.880, 0.001)
check("1-47 pc", math.sqrt(3.5 ** 2 - 0.938 ** 2), 3.372, 0.001)
check("1-48 E", math.sqrt(0.94 ** 2 + 1.2 ** 2), 1.524, 0.001)
mpi, mmu = 139.57, 105.66
check("sf-09-1 sum sq", mpi ** 2 + mmu ** 2, 30643.8, 1e-4)
check("sf-09-1 diff sq", mpi ** 2 - mmu ** 2, 8315.7, 1e-4)
Emu = (mpi ** 2 + mmu ** 2) / (2 * mpi)
Enu = (mpi ** 2 - mmu ** 2) / (2 * mpi)
check("sf-09-1 Emu", Emu, 109.78, 1e-4)
check("sf-09-1 Enu", Enu, 29.79, 1e-3)
check("sf-09-1 KE", Emu - mmu, 4.12, 0.003)
check("sf-09-1 v", Enu / Emu, 0.271, 0.003)
check("sf-09-2 theta", 2 * math.degrees(math.asin(0.511)), 61.5, 0.002)

# =================== 第 10 節 ===================
check("sf-10-1 (a)", 0.5 * 9.8 * (10 / C) ** 2, 5.4e-15)
b = 1.0  # 積分對 b 是尺度不變的：I*b^2 與 b 無關
I = quad(lambda xx: 1 / (b * b + xx * xx) ** 1.5, -np.inf, np.inf)[0]
check("sf-10-1 integral = 2/b^2", I * b * b, 2.0, 1e-6)
a1 = 2 * 6.674e-11 * 1.989e30 / (6.96e8 * C4 ** 2)
check("sf-10-1 2GM/Rc^2", a1, 4.24e-6)
check("sf-10-1 arcsec half", a1 * 206265, 0.88)
check("sf-10-1 GR rad", 2 * a1, 8.49e-6)
check("sf-10-1 GR arcsec", 2 * a1 * 206265, 1.75)
check("sf-10-1 GR deg", math.degrees(2 * a1), 4.9e-4, 0.02)
check("sf-10-1 coin rad", 0.0179 / 1609, 1.11e-5)
check("sf-10-1 coin deg", math.degrees(0.0179 / 1609), 0.00064, 0.01)
check("sf-10-2 (b)", 9.8 * 22.5 / C4 ** 2, 2.45e-15)
GM, RE, r = 3.986e14, 6.371e6, 2.656e7
dphi = GM / C4 ** 2 * (1 / RE - 1 / r)
check("sf-10-2 dPhi/c2", dphi, 5.29e-10)
vg = math.sqrt(GM / r)
check("sf-10-2 v", vg, 3.87e3)
check("sf-10-2 v^2/2c^2", vg ** 2 / (2 * C4 ** 2), 8.35e-11)
check("sf-10-2 grav us/day", dphi * 86400 * 1e6, 45.7)
check("sf-10-2 vel us/day", vg ** 2 / (2 * C4 ** 2) * 86400 * 1e6, 7.2)
net = (dphi - vg ** 2 / (2 * C4 ** 2)) * 86400
check("sf-10-2 net us/day", net * 1e6, 38.5)
check("sf-10-2 km", C * 38.5e-6 / 1e3, 12, 0.05)

# =================== 第 11 節 ===================
check("ex1-11", vadd(0.5, 0.9), 0.97, 0.005)
y75 = math.sqrt(1 - 0.75 ** 2)
check("kg-107-5 sqrt", y75, 0.661)
check("kg-107-5 Vy'", 0.9 * y75, 0.595)
check("kg-107-5 sum sq", 0.5625 + (0.9 * y75) ** 2, 0.9169, 0.001)
# 獨立：四維速度直接轉換
Gb = g(0.9)
U = np.array([Gb, 0.0, -Gb * 0.9])  # (gamma, gamma*Vx, gamma*Vy) 以 c 為單位
Up = boost(0.75) @ U
Vp = Up[1:] / Up[0]
check("kg-107-5 speed (4-velocity)", float(np.hypot(*Vp)), 0.958)
check("kg-107-5 angle", math.degrees(math.atan2(-Vp[1], -Vp[0])), 38, 0.02)
check("1-54 forward", vadd(0.5, 0.5), 0.8)
check("1-54 backward", vadd(-0.6, 0.5), -0.143, 0.003)
check("1-54 inverse", vadd(-0.143, -0.5), -0.6, 0.003)
check("1-55 A sees B", vadd(-0.9, -0.8), -0.988, 0.001)
check("1-56 KE lab", (g(0.8) - 1) * 0.511, 0.341)
check("1-56 V'", vadd(0.8, -0.5), 0.5)
check("1-56 KE'", (g(0.5) - 1) * 0.511, 0.0790)
Ee, pe = g(0.8) * 0.511, g(0.8) * 0.8 * 0.511
Ep = g(0.5) * (Ee - 0.5 * pe)
check("1-56 E' via transform", Ep, 0.590, 0.002)
for th in np.radians([10, 45, 90, 135, 170]):
    for bb in (0.3, 0.9):
        Vx, Vy = -math.cos(th), -math.sin(th)
        den = 1 - bb * Vx
        Vxp, Vyp = (Vx - bb) / den, Vy * math.sqrt(1 - bb * bb) / den
        ok = abs(math.hypot(Vxp, Vyp) - 1) < 1e-12
        tp = math.atan2(-Vyp, -Vxp)
        ok = ok and abs(math.tan(tp) - math.sin(th) * math.sqrt(1 - bb * bb) / (math.cos(th) + bb)) < 1e-9 * (1 + abs(math.tan(tp)))
        if not ok:
            FAIL.append("1-53")
check_true("1-53 aberration formula & |V'|=c", "1-53" not in FAIL)
dtB = to_frame(-0.6, 0, 2.0)  # Anna 系 -> Bob 系 (Bob 相對 Anna 以 -0.6c)
check("kg-107-4 dt (ns)", dtB[0] / C * 1e9, 5.0)
v51 = 1e5 / 2e-3 / C
check("1-51 v/c", v51, 0.167, 0.002)
check("1-51 dt'", 2.0 * math.sqrt(1 - v51 ** 2), 1.97)
check("1-51 v^2", v51 ** 2, 0.0278, 0.001)
b52 = math.sqrt(1 - 1 / 1.6 ** 2)
check("1-52 1/g^2", 1 / 2.56, 0.391, 0.001)
check("1-52 beta", b52, 0.781)
check("1-52 dt'", 1.6 * b52 * 1e5 / C, 4.16e-4)
check("1-52 interval", math.sqrt(160 ** 2 - 100 ** 2), 125, 0.002)
bp = math.sqrt(3) / 2
eB = to_frame(bp, 0, 10.0)
check("sf-11-1 tB' (s)", eB[0] / C, -5.77e-8)
check("sf-11-1 xB'", eB[1], 20)
check("sf-11-1 barn shift", bp * C * 5.77e-8, 15, 0.002)
seq = [0.0]
for _ in range(5):
    seq.append(vadd(seq[-1], 0.5))
for got, w in zip(seq[1:], (0.5, 0.8, 0.9286, 0.9756, 0.9918)):
    check("sf-11-2 sequence", got, w, 2e-4)
check("sf-11-2 n", math.atanh(0.99) / math.atanh(0.5), 4.82, 0.002)

# =================== 第 12 節 ===================
check("st-ex1 c dt", C * 1e-6, 300)
check("st-ex1 ds^2", 300 ** 2 - 600 ** 2, -2.7e5)
check("st-ex1 v", 300 / 600, 0.5)
check("st-ex1 dx'", to_frame(0.5, 300, 600)[1], 520, 0.002)
check_true("st-ex1 dt'=0", abs(to_frame(0.5, 300, 600)[0]) < 1e-9)
check("sf-12-1 (ii)", 2 * math.sqrt(25 - 9), 8.0)
check("sf-12-1 (iii) out", math.sqrt(64 - 16), 6.9, 0.005)
check("sf-12-1 (iii) back ds^2", 4 - 16, -12)
check("sf-12-2 KEth", 134.98 * (4 * 938.27 + 134.98) / (2 * 938.27), 279.7, 1e-3)

# =================== 綜合題 ===================
print("---- 綜合題 ----")
# cx-01：在地球座標系追光數訊號（不用都卜勒公式）
b, D = 0.96, 24.0
T = 2 * D / b
G = g(b)
check("cx-01 gamma", G, 3.571, 1e-3)
check("cx-01 Earth time", T, 50)
check("cx-01 ship time", T / G, 14)
check("cx-01 distance seen", D / G, 6.72)


def A_pos(t):
    return b * t if t <= D / b else D - b * (t - D / b)


def A_tau(t):
    return t / G


# B 在第 n 年（地球時間）發的訊號：x = t - n，與 A 世界線相交
out = back = 0
for n in range(1, 51):
    tt = brentq(lambda t: A_pos(t) - (t - n), n, T + 1e-9) if n < T else T
    if A_tau(tt) <= 7 + 1e-9:
        out += 1
    elif A_tau(tt) <= 14 + 1e-9:
        back += 1
check("cx-01 A receives outbound", out, 1)
check("cx-01 A receives inbound", back, 49)
# A 在船上第 k 年發的訊號（往 -x 傳回地球）
before = after = 0
for k in range(1, 15):
    te = k * G  # 地球時間
    xe = A_pos(te)
    arrive = te + xe
    if arrive <= 49 + 1e-9:
        before += 1
    elif arrive <= 50 + 1e-9:
        after += 1
check("cx-01 B receives before 49 y", before, 7)
check("cx-01 B receives after", after, 7)
check("cx-01 B sees turnaround", D / b + D, 49)
turn = (D / b, D)  # (t, x)
# 去程座標系：找地球事件 (t_E, 0) 使 t' 相等
tE_out = brentq(lambda tE: to_frame(b, tE, 0)[0] - to_frame(b, turn[0], turn[1])[0], 0, 50)
tE_in = brentq(lambda tE: to_frame(-b, tE, 0)[0] - to_frame(-b, turn[0], turn[1])[0], 0, 60)
check("cx-01 Earth now before turn", tE_out, 1.96)
check("cx-01 Earth now after turn", tE_in, 48.04)
check("cx-01 jump", tE_in - tE_out, 46.08)

# cx-02：在地球座標系數值積分 dβ/dt = (g/c)(1-β^2)^{3/2}
a = 9.80 * 3.156e7 / C4  # 1/y
check("cx-02 g/c (1/y)", a, 1.032, 1e-3)
check("cx-02 c^2/g (ly)", 1 / a, 0.9693, 1e-4)


def rhs(t, y):
    beta = y[0]
    return [a * (1 - beta * beta) ** 1.5, beta, math.sqrt(1 - beta * beta)]


ev = lambda t, y: y[1] - 5.0
ev.terminal = True
sol = solve_ivp(rhs, [0, 20], [0, 0, 0], events=ev, rtol=1e-11, atol=1e-12)
t1n, (bmax, _, tau1n) = sol.t_events[0][0], sol.y_events[0][0]
check("cx-02 cosh phi_m", 1 + 5 * a, 6.158, 1e-4)
check("cx-02 phi_m", math.acosh(1 + 5 * a), 2.504, 1e-3)
check("cx-02 sinh phi_m", math.sinh(math.acosh(1 + 5 * a)), 6.076, 1e-3)
check("cx-02 tau1 (numeric)", tau1n, 2.427, 1e-3)
check("cx-02 t1 (numeric)", t1n, 5.890, 1e-3)
check("cx-02 beta max (numeric)", bmax, 0.9867, 1e-4)
check("cx-02 total ship", 4 * tau1n, 9.71, 1e-3)
check("cx-02 total Earth", 4 * t1n, 23.56, 1e-3)
check("cx-02 gamma*beta = g t/c", g(bmax) * bmax, a * t1n, 1e-6)
check("cx-02 Newton t", math.sqrt(2 * 5 / a), 3.11, 0.002)
check("cx-02 Newton v", a * math.sqrt(2 * 5 / a), 3.21, 0.002)
check("cx-02 average speed", 20 / (4 * t1n), 0.849, 0.002)

# cx-03：四維速度 + 勞倫茲轉換矩陣（S' -> S 用 boost(-v)）
v = 0.8


def launch(ux, uy):
    gu = 1 / math.sqrt(1 - ux * ux - uy * uy) if ux * ux + uy * uy < 1 else None
    if gu is None:  # 光：用四維波向量 (1, ux, uy)
        k = boost(-v) @ np.array([1.0, ux, uy])
        return k[1:] / k[0]
    U = boost(-v) @ np.array([gu, gu * ux, gu * uy])
    return U[1:] / U[0]


Va = launch(0.9, 0)
Vb = launch(-0.9, 0)
Vc = launch(0, 0.9)
check("cx-03 (a)", Va[0], 0.988, 0.001)
check("cx-03 (b)", Vb[0], -0.357, 0.002)
check("cx-03 (c) speed", float(np.hypot(*Vc)), 0.965, 0.001)
check("cx-03 (c) Vy", Vc[1], 0.54)
check("cx-03 (c) angle", math.degrees(math.atan2(Vc[1], Vc[0])), 34.0, 0.003)
thp = brentq(lambda th: launch(0.9 * math.cos(th), 0.9 * math.sin(th))[0], math.pi / 2, math.pi)
Vd = launch(0.9 * math.cos(thp), 0.9 * math.sin(thp))
check("cx-03 (d) theta'", math.degrees(thp), 152.7, 0.001)
check("cx-03 (d) uy'", 0.9 * math.sin(thp), 0.412, 0.002)
check("cx-03 (d) speed", Vd[1], 0.687, 0.002)
Ve = launch(0, 1.0)
check("cx-03 (e) |V|", float(np.hypot(*Ve)), 1.0, 1e-12)
check("cx-03 (e) angle", math.degrees(math.atan2(Ve[1], Ve[0])), 36.9, 0.002)
check("cx-03 gamma_u'", g(0.9), 2.294, 0.001)
check("cx-03 gammaV (c)", 5 / 3 * g(0.9), 3.824, 0.001)
check("cx-03 gammaV (d)", 5 / 3 * g(0.9) * 0.36, 1.376, 0.001)
check("cx-03 Galilean (c)", math.hypot(0.8, 0.9), 1.20, 0.005)
check("cx-03 Galilean angle", math.degrees(math.atan2(0.9, 0.8)), 48.4, 0.002)

# cx-04：三個勞倫茲矩陣相乘
Mtot = boost(-0.5) @ boost(-0.7) @ boost(-0.9)
Gt = Mtot[0, 0]
bt = Mtot[1, 0] / Mtot[0, 0]  # 二號原點的世界線在地球系的 x/ct
check("cx-04 probe1", vadd(0.5, 0.7), 0.8889, 1e-4)
check("cx-04 probe2 (matrix)", bt, 0.9938, 1e-4)
check("cx-04 probe2 = 161/162", bt, 161 / 162, 1e-12)
check("cx-04 probe2 rel mother", vadd(0.7, 0.9), 0.9816, 1e-4)
check("cx-04 phi sum", math.atanh(0.5) + math.atanh(0.7) + math.atanh(0.9), 2.8888, 1e-4)
check("cx-04 order swap", vadd(vadd(0.5, 0.9), 0.7), bt, 1e-12)
check("cx-04 gamma (matrix)", Gt, 9.014, 1e-4)
# 都卜勒：把往 -x 的光子波向量 (1,-1,0)（二號系）逐級轉到地球
kvec = Mtot @ np.array([1.0, -1.0, 0.0])
check("cx-04 f/f0 (photon 4-vector)", kvec[0], 0.0556, 0.002)
check("cx-04 1/sqrt(323)", 1 / math.sqrt(323), 0.0556, 0.002)
check("cx-04 KE Earth", (Gt - 1) * 9e16, 7.21e17)
check("cx-04 KE probe1", (g(0.9) - 1) * 9e16, 1.16e17, 0.005)
check("cx-04 KE ratio", (Gt - 1) / (g(0.9) - 1), 6.19)

# cx-05：世界線 + 勞倫茲轉換
tm = brentq(lambda t: 0.8 * t - (14 - 0.6 * t), 0, 20)
check("cx-05 meet t", tm, 10.0)
check("cx-05 meet x", 0.8 * tm, 8.0)
check("cx-05 Earth sees", tm + 0.8 * tm, 18.0)
check("cx-05 rel speed", vadd(-0.6, -0.8), -0.946, 0.001)
check("cx-05 tauA", tm / g(0.8), 6.0)
check("cx-05 tauB", tm / g(0.6), 8.0)
# A 系 t'=0 的 B 事件
tB = brentq(lambda t: to_frame(0.8, t, 14 - 0.6 * t)[0], 0, 20)
check("cx-05 B event x", 14 - 0.6 * tB, 9.459, 1e-3)
check("cx-05 B event t", tB, 7.568, 1e-3)
check("cx-05 distance in A frame", to_frame(0.8, tB, 14 - 0.6 * tB)[1], 5.676, 1e-3)
meetA = to_frame(0.8, tm, 0.8 * tm)
check("cx-05 meet in A frame t'", meetA[0], 6.0)
check_true("cx-05 meet in A frame x'=0", abs(meetA[1]) < 1e-9)
br = vadd(0.6, 0.8)
check("cx-05 k", math.sqrt((1 + br) / (1 - br)), 6.0, 1e-9)
recv = []
for n in range(0, 9):
    te, xe = g(0.6) * n, 14 - 0.6 * g(0.6) * n
    ta = brentq(lambda t: 0.8 * t - (xe - (t - te)), 0, 30)
    recv.append(ta / g(0.8))
check("cx-05 first signal tauA", recv[0], 4.67, 0.002)
check("cx-05 last signal at meeting", recv[-1], 6.0, 1e-9)
check("cx-05 count before meeting", len([r for r in recv if r <= 6 + 1e-9]), 9)
check("cx-05 interval", recv[1] - recv[0], 1 / 6, 1e-9)

# cx-06：光子火箭拆成很多小脈衝（每次在瞬時靜止系射出一點光）
Mf, beta_t = 1.0e6, 0.8
check("cx-06 KE", (g(0.8) - 1) * Mf * C ** 2, 6.00e22)
check("cx-06 classical", 0.5 * Mf * (0.8 * C) ** 2, 2.88e22)
check("cx-06 ratio", (g(0.8) - 1) / (0.5 * 0.64), 2.08, 0.003)
Mcur, bcur, steps = 1.0, 0.0, 0
eps = 2e-5
while bcur < beta_t:
    e = eps * Mcur  # 這一脈衝光的能量（靜止系，以 c=1）
    Mnew = Mcur * math.sqrt(1 - 2 * e / Mcur)
    dv = e / (Mcur - e)  # 瞬時靜止系中得到的速度
    bcur = vadd(bcur, dv)
    Mcur = Mnew
    steps += 1
check("cx-06 photon rocket mass ratio (bursts)", 1 / Mcur, 3.0, 2e-4)
check("cx-06 formula", math.sqrt(1.8 / 0.2), 3.0, 1e-12)
Eg = g(0.8) * 0.8 * Mf * C ** 2
check("cx-06 E_gamma", Eg, 1.20e23)
check("cx-06 fuel energy", 2 * Mf * C ** 2, 1.80e23)
check("cx-06 efficiency", (g(0.8) - 1) * Mf * C ** 2 / (2 * Mf * C ** 2), 1 / 3)
check("cx-06 system mass after burn", math.sqrt((g(0.8) * Mf + Eg / C ** 2) ** 2 - (g(0.8) * 0.8 * Mf - Eg / C ** 2) ** 2), 3e6, 1e-9)
check("cx-06 decel ratio", 1 / (g(0.8) * 0.2), 3.0, 1e-9)
check("cx-06 round trip", 3 ** 4, 81)
phim = math.acosh(1 + 5 * a)
check("cx-06 1g trip ratio", math.exp(4 * phim), 2.2e4, 0.03)
check("cx-06 chemical exponent", C / (2 * 4.5e3), 3.33e4, 0.002)
check("cx-06 chemical log10", C / (2 * 4.5e3) * math.log10(9), 3.2e4, 0.01)
check("cx-06 chemical round trip log10", 4 * C / (2 * 4.5e3) * math.log10(9), 1.3e5, 0.03)
check("cx-06 Tsiolkovsky log10", 0.8 * C / 4.5e3 / math.log(10), 2.3e4, 0.01)

# cx-07：四維向量 + Monte Carlo 衰變
mp, mpi0 = 938.27, 134.98
Eth = brentq(lambda E: (E + mp) ** 2 - E ** 2 - (mp + mpi0) ** 2, 1, 1000)
check("cx-07 Eth", Eth, 144.7, 1e-3)
Etot, Ptot = Eth + mp, Eth
beta_cm = Ptot / Etot
gam_cm = Etot / (mp + mpi0)
check("cx-07 beta", beta_cm, 0.1336, 1e-3)
check("cx-07 gamma", gam_cm, 1.00905, 1e-5)
Epi, ppi = gam_cm * mpi0, gam_cm * beta_cm * mpi0
check("cx-07 Epi", Epi, 136.20, 1e-4)
check("cx-07 ppi", ppi, 18.20, 1e-3)
check("cx-07 KEp", (gam_cm - 1) * mp, 8.49, 2e-3)
check("cx-07 pp", gam_cm * beta_cm * mp, 126.49, 1e-4)
check("cx-07 momentum conservation", gam_cm * beta_cm * (mp + mpi0), Eth, 1e-9)
cth = rng.uniform(-1, 1, 10000)
cth = np.concatenate([cth, [1.0, -1.0]])
phi_ = rng.uniform(0, 2 * np.pi, cth.size)
sth = np.sqrt(1 - cth ** 2)
Es = mpi0 / 2
E1 = gam_cm * (Es + beta_cm * Es * cth)
E2 = gam_cm * (Es - beta_cm * Es * cth)
p1 = np.stack([gam_cm * (Es * cth + beta_cm * Es), Es * sth * np.cos(phi_), Es * sth * np.sin(phi_)], 1)
p2 = np.stack([gam_cm * (-Es * cth + beta_cm * Es), -Es * sth * np.cos(phi_), -Es * sth * np.sin(phi_)], 1)
cosang = np.sum(p1 * p2, 1) / (np.linalg.norm(p1, axis=1) * np.linalg.norm(p2, axis=1))
check("cx-07 Emax (MC)", float(E1.max()), 77.20, 1e-4)
check("cx-07 Emin (MC)", float(E1.min()), 59.00, 1e-4)
check("cx-07 min opening angle (MC)", float(np.degrees(np.arccos(cosang.max()))), 164.6, 1e-3)
check("cx-07 theta_min formula", 2 * math.degrees(math.asin(mpi0 / Epi)), 164.6, 1e-3)
check("cx-07 Emax*Emin", 77.20 * 59.00, (mpi0 / 2) ** 2, 1e-4)
check("cx-07 products KE", (gam_cm - 1) * mp + (Epi - mpi0), Eth - mpi0, 1e-9)

# cx-08：把事件直接轉到緲子系
h = 12000.0
bm = math.sqrt(0.99)
check("cx-08 v", bm * C, 2.985e8, 1e-3)
tflight = h / (bm * C)
check("cx-08 t", tflight * 1e6, 40.20, 1e-4)
check("cx-08 tau", tflight / 10 * 1e6, 4.020, 1e-4)
check("cx-08 survival", math.exp(-tflight / 10 / 2.197e-6), 0.160, 0.003)
check("cx-08 L", h / 10, 1200)
arrive = to_frame(bm, C * tflight, h)
check("cx-08 arrival t' (us)", arrive[0] / C * 1e6, 4.020, 1e-4)
check_true("cx-08 arrival x'=0", abs(arrive[1]) < 1e-6)
tg0 = brentq(lambda t: to_frame(bm, C * t, h)[0], -1e-3, 1e-3)
check("cx-08 ground clock at start (us)", tg0 * 1e6, 39.80, 1e-4)
check("cx-08 ground clock advance (us)", (tflight - tg0) * 1e6, 0.402, 1e-3)
check("cx-08 nonrel survival", math.exp(-tflight / 2.197e-6), 1.1e-8, 0.03)
check("cx-08 interval", math.sqrt((C * tflight) ** 2 - h ** 2) / C * 1e6, 4.020, 1e-4)

# cx-09：直接解世界線與光線
t1, t2 = 1.0, 9.0
# 未知 beta：脈衝 x=t-t1 追上 x=beta t，回波 x = xr-(t-tr) 在 t2 回到 0
bfit = brentq(lambda bb: (t1 / (1 - bb)) * (1 + bb) - t2, 0.01, 0.99)
tr = t1 / (1 - bfit)
check("cx-09 beta", bfit, 0.800, 1e-9)
check("cx-09 t_R", tr, 5.00)
check("cx-09 x_R", bfit * tr, 4.00)
check("cx-09 tau_R", tr / g(bfit), 3.00)
check("cx-09 k", math.sqrt(t2 / t1), 3.0)
check("cx-09 echo freq GHz", 10.0 * (1 - bfit) / (1 + bfit), 1.11, 0.002)
refl = to_frame(bfit, tr, bfit * tr)
check("cx-09 reflection t' (h)", refl[0], 3.00)
tnow = brentq(lambda t: to_frame(bfit, t, 0)[0] - refl[0], 0, 10)
check("cx-09 Earth now in probe frame", tnow, 1.80)
check("cx-09 Earth distance in probe frame", -to_frame(bfit, tnow, 0)[1], 2.40)
emit = to_frame(bfit, t1, 0)
check("cx-09 emission t'", emit[0], 1.667, 1e-3)
check("cx-09 emission distance", -emit[1], 1.333, 1e-3)
check("cx-09 pulse arrives", emit[0] - emit[1], 3.00)

# cx-10：質心系隨機散射後轉回實驗室
mpr, K1 = 0.938, 2.00
E1l = K1 + mpr
p1l = math.sqrt(E1l ** 2 - mpr ** 2)
check("cx-10 p1", p1l, 2.784, 1e-3)
s_ = 2 * mpr ** 2 + 2 * E1l * mpr
gcm = (E1l + mpr) / math.sqrt(s_)
bcm = p1l / (E1l + mpr)
check("cx-10 gamma_cm^2", gcm ** 2, 2.066, 1e-3)
check("cx-10 gamma_cm", gcm, 1.437, 1e-3)
Es_, ps_ = math.sqrt(s_) / 2, gcm * bcm * mpr
check_true("cx-10 CM speed = beta_cm", abs(ps_ / Es_ - bcm) < 1e-12)
ok = True
for th in rng.uniform(0.05, math.pi - 0.05, 2000):
    a3 = np.array([gcm * (ps_ * math.cos(th) + bcm * Es_), ps_ * math.sin(th)])
    a4 = np.array([gcm * (-ps_ * math.cos(th) + bcm * Es_), -ps_ * math.sin(th)])
    E3 = gcm * (Es_ + bcm * ps_ * math.cos(th))
    E4 = gcm * (Es_ - bcm * ps_ * math.cos(th))
    cosang = a3 @ a4 / (np.linalg.norm(a3) * np.linalg.norm(a4))
    pred = (E3 - mpr) * (E4 - mpr) / (np.linalg.norm(a3) * np.linalg.norm(a4))
    ok = ok and abs(cosang - pred) < 1e-9 and cosang > 0
check_true("cx-10 cos(theta)=K3K4/(p3p4) for random CM angles, all < 90 deg", ok)
a3 = np.array([gcm * bcm * Es_, ps_])
alpha = math.degrees(math.atan2(a3[1], a3[0]))
check("cx-10 alpha (CM 90 deg)", alpha, 34.8, 1e-3)
check("cx-10 opening", 2 * alpha, 69.7, 1e-3)
check("cx-10 tan alpha = 1/gamma_cm", math.tan(math.radians(alpha)), 1 / gcm, 1e-9)
p3 = math.sqrt(1.0 + 2 * 1.0 * mpr)
check("cx-10 p3", p3, 1.696, 1e-3)
check("cx-10 cos theta", 1 / p3 ** 2, 0.3477, 1e-3)
check("cx-10 tan^2 = 2/(g1+1)", 2 / (E1l / mpr + 1), 0.4840, 1e-3)
check("cx-10 momentum check", 2 * p3 * math.cos(math.radians(alpha)), p1l, 1e-6)

print()
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("ALL CHECKS PASSED")
