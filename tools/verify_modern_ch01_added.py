"""獨立驗算 modern/ch01 本次新增的課本習題與自編難題（numpy / sympy / scipy）。

用法：python tools/verify_modern_ch01_added.py
每一題用和網站詳解不同的算法（數值解、符號運算、精確式 vs 近似式）重算，並和網站上寫的數字比對。
奇數題另和 Beiser 書末答案（PDF p.530）比對。
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

C = 3.00e8          # 題目計算用的 c
C4 = 2.998e8        # 四位有效數字的 c
E_CH = 1.602e-19
ME = 0.511          # MeV
FAIL = []


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


# ---------------- 課本習題 ----------------
# 1-3 概念：太空船量到 γ t0 > t0
check_true("1-3 spacecraft time longer", g(0.5) * 10.0 > 10.0)

# 1-7  γ=2
b = brentq(lambda b: g(b) - 2, 0, 0.999)
check("1-7 v (m/s)", b * C, 2.60e8)
check("1-7 book 2.6e8", b * C, 2.6e8, 0.02)

# 1-8 Apollo：精確 (γ-1)·86400 用高精度
v = 1.08e4
xx8 = (v / C) ** 2
dg = math.expm1(-0.5 * math.log1p(-xx8))   # γ-1 的精確值（避免相減失去精度）
check("1-8 extra time (s)", dg * 86400, 5.6e-5, 0.02)

# 1-13 精確數值解（不用近似）
f = lambda b: 1e9 / (1 + b) - 1e9 * math.sqrt((1 - b) / (1 + b)) - 1
b13 = brentq(f, 1e-7, 1e-3)
check("1-13 v (m/s)", b13 * C, 1.34e4)

# 1-18
check("1-18 L0 (m)", 1.3 * g(0.6), 1.625)

# 1-19
check("1-19 t (s)", math.sqrt(1 - 0.01) / (0.1 * C), 3.32e-8, 0.005)

# 1-27
check("1-27 fraction", 5.4e6 / C ** 2, 6.0e-11)

# 1-28
check("1-28 m_i (kg)", 1.00 * C ** 2 / 3.34e5, 2.69e11)

# 1-30
check("1-30 J/kg", (g(0.9) - 1) * C ** 2, 1.16e17)

# 1-32 符號：級數展開 sqrt(1-x) 的一階 = 1 - x/2；並數值檢查
x = sp.symbols("x")
check_true("1-32 series", sp.simplify(sp.series(sp.sqrt(1 - x), x, 0, 2).removeO() - (1 - x / 2)) == 0)
check("1-32 E=21E0", 1 - 0.5 / 21 ** 2, 0.99887, 1e-4)

# 1-37 符號：KE - ½γmv² = (γ-1)²/(2γ) mc²
bb = sp.symbols("beta", positive=True)
G = 1 / sp.sqrt(1 - bb ** 2)
diff = (G - 1) - sp.Rational(1, 2) * G * bb ** 2 - (G - 1) ** 2 / (2 * G)
check_true("1-37 identity", sp.simplify(diff) == 0)
check("1-37 v=0.8c diff", (5 / 3 - 1) - 0.5 * (5 / 3) * 0.64, 0.133, 0.01)

# 1-40
check("1-40 MeV/c^2 (kg)", 1.602e-13 / C4 ** 2, 1.783e-30, 0.001)
check("1-40 MeV/c (kg m/s)", 1.602e-13 / C4, 5.344e-22, 0.001)

# 1-43
check("1-43 p", g(0.6) * ME * 0.6, 0.383, 0.002)
check("1-43 via E", math.sqrt((g(0.6) * ME) ** 2 - ME ** 2), 0.383, 0.002)

# 1-44
gp = g(0.9)
check("1-44 E", gp * 0.938, 2.15, 0.003)
check("1-44 KE", (gp - 1) * 0.938, 1.21, 0.004)
check("1-44 p", gp * 0.938 * 0.9, 1.94, 0.003)

# 1-45
check("1-45 pc (keV)", math.sqrt((2 * 511) ** 2 - 511 ** 2), 885, 0.001)

# 1-46 符號
m, vv, cc = sp.symbols("m v c", positive=True)
gg = 1 / sp.sqrt(1 - vv ** 2 / cc ** 2)
check_true("1-46 pc/E = v/c", sp.simplify((gg * m * vv * cc) / (gg * m * cc ** 2) - vv / cc) == 0)

# 1-48
check("1-48 E", math.hypot(0.940, 1.200), 1.524, 0.001)

# 1-53 用勞倫茲轉換的光速度，與網站公式比較（數組角度）
for beta in (0.3, 0.7, 0.95):
    for th in np.radians([20, 60, 90, 135]):
        Vx, Vy = -math.cos(th), -math.sin(th)
        Vxp = (Vx - beta) / (1 - beta * Vx)
        Vyp = Vy * math.sqrt(1 - beta ** 2) / (1 - beta * Vx)
        thp = math.atan2(-Vyp, -Vxp)
        site = math.atan2(math.sin(th) * math.sqrt(1 - beta ** 2), math.cos(th) + beta)
        if abs(thp - site) > 1e-12 or abs(math.hypot(Vxp, Vyp) - 1) > 1e-12:
            FAIL.append("1-53")
check_true("1-53 aberration formula & |V'|=c", "1-53" not in FAIL)

# ---------------- 自編難題 ----------------
# sf-01-1 Michelson–Morley：精確時間差 vs 近似
L, vE, lam = 11.0, 3.0e4, 5.9e-7
be = vE / C
tpar = L / (C - vE) + L / (C + vE)
tper = 2 * L / math.sqrt(C ** 2 - vE ** 2)
check("sf-01-1 dt", tpar - tper, 3.7e-16)
check("sf-01-1 fringes", 2 * C * (tpar - tper) / lam, 0.37)
check("sf-01-1(c) contracted", (2 * L * math.sqrt(1 - be ** 2) * C / (C ** 2 - vE ** 2)) / tper, 1.0, 1e-12)

# sf-01-2 binary (精確)
D_days = 1000 * 365.25
dt = D_days * (1 / (1 - 1e-4) - 1 / (1 + 1e-4))
check("sf-01-2 dt days", dt, 73)
check("sf-01-2 arrival diff", 5 - dt, -68, 0.01)

# sf-02-1 muon ring
gm, tau0, R = 29.3, 2.197e-6, 7.0
bm = math.sqrt(1 - 1 / gm ** 2)
check("sf-02-1 beta", bm, 0.99942, 1e-5)
check("sf-02-1 lab life", gm * tau0, 64.4e-6, 0.002)
d = bm * C * gm * tau0
check("sf-02-1 d", d, 1.93e4, 0.003)
check("sf-02-1 revs", d / (2 * math.pi * R), 440, 0.01)
check("sf-02-1 a/g", (bm * C) ** 2 / R / 9.8, 1.3e15, 0.03)

# sf-02-2  γβ=10
b22 = brentq(lambda b: b * g(b) - 10, 0.5, 0.99999)
check("sf-02-2 beta", b22, 0.99504, 1e-5)
check("sf-02-2 1-beta", 1 - b22, 4.96e-3, 0.002)
check("sf-02-2 T", 100 / b22, 100.5, 0.001)

# sf-03-1
br = brentq(lambda b: (1 - b) / (1 + b) - 0.81, 0, 0.9)
check("sf-03-1 beta", br, 0.105, 0.005)
check("sf-03-1 approx", 0.19 / 2, 0.095)

# sf-03-2 Ives–Stilwell
b, l0 = 0.005, 486.1
lf = l0 * math.sqrt((1 - b) / (1 + b))
lb = l0 * math.sqrt((1 + b) / (1 - b))
check("sf-03-2 lf", lf, 483.68, 1e-5)
check("sf-03-2 lb", lb, 488.54, 1e-5)
check("sf-03-2 shift", (lf + lb) / 2 - l0, 6.1e-3, 0.01)
check("sf-03-2 mean=gamma*l0", (lf + lb) / 2 / (g(b) * l0), 1.0, 1e-12)

# sf-04-1
g41 = g(0.8)
check("sf-04-1 station", 120 / g41 / (0.8 * C), 3.0e-7)
check("sf-04-1 ship", 120 / (0.8 * C), 5.0e-7)
check("sf-04-1 ratio", (120 / (0.8 * C)) / (120 / g41 / (0.8 * C)), 5 / 3, 1e-12)

# sf-04-2 用頂點座標直接算菱形
gam = g(0.6)
P = np.array([[1 / gam, 0], [0, 1], [-1 / gam, 0], [0, -1]]) * (math.sqrt(2) / 2)  # a=1
s01 = np.linalg.norm(P[1] - P[0])
u, w = P[3] - P[0], P[1] - P[0]
ang = math.degrees(math.acos(np.dot(u, w) / (np.linalg.norm(u) * np.linalg.norm(w))))
area = 0.5 * abs(np.cross(P[2] - P[0], P[3] - P[1]))
check("sf-04-2 front angle", ang, 102.7, 0.001)
check("sf-04-2 side", s01, 0.906, 0.001)
check("sf-04-2 area", area, 0.80, 1e-9)

# sf-05-1 asymmetric twin，逐年模擬訊號抵達時刻
D, b1, b2 = 4.8, 0.6, 0.8
TE = D / b1 + D / b2
TA = D / b1 / g(b1) + D / b2 / g(b2)
check("sf-05-1 TB", TE, 14.0, 1e-9)
check("sf-05-1 TA", TA, 10.0, 1e-9)
# A 收到 B 的訊號：B 在 t=0,1,...,14 發；A 的世界線 x(t)
def xA(t):
    return b1 * t if t <= D / b1 else D - b2 * (t - D / b1)
recv = 0.0
for n in range(1, 15):  # B 在第 n 年發的光何時追上 A
    tr = brentq(lambda t: (t - n) - xA(t), n, TE + 1e-9) if n < TE else TE
    if tr <= TE + 1e-9:
        recv += 1
check("sf-05-1 A receives (integer count incl. last)", recv, 14, 1e-9)
check("sf-05-1 B sees turnaround", D / b1 + D, 12.8, 1e-9)
check("sf-05-1 B receives", (D / b1 / g(b1)) + (TE - 12.8) * math.sqrt((1 + b2) / (1 - b2)), 10.0, 1e-9)

# sf-05-2 (k+1/k)/2 = γ（符號）
k = sp.sqrt((1 + bb) / (1 - bb))
check_true("sf-05-2 identity", all(abs(float(((k + 1 / k) / 2 - G).subs(bb, t))) < 1e-12 for t in (0.1, 0.37, 0.6, 0.8, 0.99)))
check("sf-05-2 example", 15 * (3 + 1 / 3), 50, 1e-9)

# sf-06-1 符號：λ' = γβ²λ0，F = F'/γ = q v μ0 I /(2π r)
lam0, q, r, eps0, mu0 = sp.symbols("lambda0 q r epsilon0 mu0", positive=True)
lamp = G * lam0 - lam0 / G
check_true("sf-06-1 lambda'", sp.simplify(lamp - G * bb ** 2 * lam0) == 0)
Fp = q * lamp / (2 * sp.pi * eps0 * r)
F_lab = sp.simplify(Fp / G)
# 代 c=1/sqrt(eps0 mu0)，v=beta c，I=λ0 v
cexpr = 1 / sp.sqrt(eps0 * mu0)
target = q * (bb * cexpr) * mu0 * (lam0 * bb * cexpr) / (2 * sp.pi * r)
check_true("sf-06-1 F = qvB", sp.simplify(F_lab - target) == 0)

# sf-06-2
n_e, A, I, dd = 8.5e28, 1e-6, 10, 0.01
EPS0, MU0 = 8.854e-12, 4e-7 * math.pi
l0 = n_e * E_CH * A
vd = I / l0
check("sf-06-2 lambda0", l0, 1.36e4, 0.005)
check("sf-06-2 v", vd, 7.3e-4, 0.01)
check("sf-06-2 beta^2", (vd / C) ** 2, 6.0e-24, 0.01)
check("sf-06-2 lambda'", l0 * (vd / C) ** 2, 8.2e-20, 0.01)
check("sf-06-2 F/l electric", l0 * l0 * (vd / C) ** 2 / (2 * math.pi * EPS0 * dd), 2.0e-3, 0.01)
check("sf-06-2 F/l magnetic", MU0 * I * I / (2 * math.pi * dd), 2.0e-3, 1e-6)
check("sf-06-2 no cancel", l0 ** 2 / (2 * math.pi * EPS0 * dd), 3.3e20, 0.02)

# sf-07-1 數值積分 v(t)
me, Ef = 9.11e-31, 1.0e6
F = 1.60e-19 * Ef
gb = 0.99 * g(0.99)
t1 = gb * me * C / F
check("sf-07-1 t", t1, 1.20e-8, 0.005)
check("sf-07-1 classical t", 0.99 * me * C / F, 1.69e-9, 0.005)
vt = lambda t: (F * t / me) / math.sqrt(1 + (F * t / (me * C)) ** 2)
xnum, _ = quad(vt, 0, t1)
check("sf-07-1 x (numerical)", xnum, 3.1, 0.01)

# sf-07-2
gl, mp, rr = 7.46e3, 1.673e-27, 2804
p = gl * mp * C * math.sqrt(1 - 1 / gl ** 2)
check("sf-07-2 p", p, 3.74e-15, 0.003)
check("sf-07-2 B", p / (1.60e-19 * rr), 8.3, 0.01)

# sf-08-1 解兩條守恆（數值 fsolve 形式）
from scipy.optimize import fsolve
sol = fsolve(lambda z: [g(z[0]) * z[1] * z[0] - g(0.6) * 0.6, g(z[0]) * z[1] - (g(0.6) + 1)], [0.3, 2.0])
check("sf-08-1 V", sol[0], 1 / 3, 1e-6)
check("sf-08-1 M", sol[1], 2.12, 0.002)
check("sf-08-1 KE lost", (g(0.6) - 1) - (g(sol[0]) - 1) * sol[1], 0.121, 0.003)
check("sf-08-1 KE lost = M-2m", (g(0.6) - 1) - (g(sol[0]) - 1) * sol[1], sol[1] - 2, 1e-6)

# sf-08-2
Kth = brentq(lambda K: math.sqrt(2 * K) / math.sqrt(1 - 1 / (1 + K) ** 2) - 1.01, 1e-6, 1)
check("sf-08-2 K", Kth, 0.01337, 0.001)
check("sf-08-2 kV", Kth * 511, 6.8, 0.01)
K25 = 25 / 511
check("sf-08-2 25 kV ratio", math.sqrt(2 * K25) / math.sqrt(1 - 1 / (1 + K25) ** 2), 1.036, 5e-4)

# sf-09-1 用數值解動量守恆
mpi, mmu = 139.57, 105.66
pp = brentq(lambda p: math.hypot(mmu, p) + p - mpi, 0, mpi)
Emu = math.hypot(mmu, pp)
check("sf-09-1 E_mu", Emu, 109.78, 1e-4)
check("sf-09-1 E_nu", pp, 29.79, 1e-4)
check("sf-09-1 KE_mu", Emu - mmu, 4.12, 0.002)
check("sf-09-1 beta_mu", pp / Emu, 0.271, 0.003)

# sf-09-2 向量直接算系統質量
Eg = 1.0
def M_sys(th):
    p1 = np.array([Eg, 0]); p2 = Eg * np.array([math.cos(th), math.sin(th)])
    return math.sqrt((2 * Eg) ** 2 - np.sum((p1 + p2) ** 2))
check("sf-09-2 formula", M_sys(1.1), 2 * Eg * math.sin(0.55), 1e-12)
thmin = brentq(lambda th: M_sys(th) - 2 * ME, 0.1, math.pi)
check("sf-09-2 theta_min", math.degrees(thmin), 61.5, 0.002)

# sf-10-1 數值積分偏折
Gc, Ms, Rs = 6.674e-11, 1.989e30, 6.96e8
iu, _ = quad(lambda u: 1 / (1 + u * u) ** 1.5, -np.inf, np.inf)   # x = R u
integ = Gc * Ms / Rs * iu                                          # = ∫ g⊥ dx
alpha_newton = integ / C4 / C4
check("sf-10-1 elevator drop", 0.5 * 9.8 * (10 / C) ** 2, 5.4e-15, 0.01)
check("sf-10-1 alpha newton (rad)", alpha_newton, 4.24e-6, 0.003)
check("sf-10-1 alpha GR arcsec", math.degrees(2 * alpha_newton) * 3600, 1.75, 0.003)
check("sf-10-1 alpha GR deg", math.degrees(2 * alpha_newton), 4.9e-4, 0.01)
check("sf-10-1 dime deg", math.degrees(0.0179 / 1609), 6.4e-4, 0.01)

# sf-10-2
check("sf-10-2 Pound-Rebka", 9.8 * 22.5 / C4 ** 2, 2.45e-15, 0.003)
GM, rg, RE = 3.986e14, 2.656e7, 6.371e6
grav = GM / C4 ** 2 * (1 / RE - 1 / rg)
vs = math.sqrt(GM / rg)
sr = 1 - math.sqrt(1 - vs ** 2 / C4 ** 2)   # 精確式
check("sf-10-2 grav/day us", grav * 86400e6, 45.7, 0.002)
check("sf-10-2 v", vs, 3.87e3, 0.002)
check("sf-10-2 sr/day us", sr * 86400e6, 7.2, 0.01)
check("sf-10-2 net us", (grav - sr) * 86400e6, 38.5, 0.003)
check("sf-10-2 distance km", C * (grav - sr) * 86400 / 1e3, 12, 0.05)

# sf-11-1 竿子與穀倉：完整勞倫茲轉換
vb = math.sqrt(3) / 2
gb11 = g(vb)
tB = gb11 * (0 - vb * 10 / C)
xB = gb11 * (10 - vb * C * 0)
check("sf-11-1 gamma", gb11, 2.0, 1e-12)
check("sf-11-1 tB' (s)", tB, -5.77e-8, 0.001)
check("sf-11-1 xB'", xB, 20, 1e-12)
check("sf-11-1 barn moved", vb * C * abs(tB), 15, 1e-9)

# sf-11-2
seq, vcur = [], 0.0
for _ in range(5):
    vcur = (vcur + 0.5) / (1 + 0.5 * vcur)
    seq.append(vcur)
for got, want in zip(seq, [0.5, 0.8, 0.9286, 0.9756, 0.9918]):
    check("sf-11-2 seq", got, want, 1e-4)
check("sf-11-2 tanh(5 phi)", math.tanh(5 * math.atanh(0.5)), seq[-1], 1e-12)
check("sf-11-2 n", math.atanh(0.99) / math.atanh(0.5), 4.82, 0.002)
a_, b_ = sp.symbols("a b")
check_true("sf-11-2 tanh addition", sp.simplify(sp.tanh(a_ + b_).rewrite(sp.exp) - ((sp.tanh(a_) + sp.tanh(b_)) / (1 + sp.tanh(a_) * sp.tanh(b_))).rewrite(sp.exp)) == 0)

# sf-12-1
check("sf-12-1 (ii)", 2 * math.sqrt(25 - 9), 8.0, 1e-12)
check_true("sf-12-1 (iii) return leg spacelike", 2 ** 2 - 4 ** 2 < 0)
# 隨機轉折點：τ ≤ 10
rng = np.random.default_rng(0)
ok = True
for _ in range(2000):
    t1_ = rng.uniform(0, 10); x1 = rng.uniform(-1, 1) * min(t1_, 10 - t1_)
    tau = math.sqrt(t1_ ** 2 - x1 ** 2) + math.sqrt((10 - t1_) ** 2 - x1 ** 2)
    ok &= tau <= 10 + 1e-12
check_true("sf-12-1 tau<=10 for random turning points", ok)

# sf-12-2 用實驗室中直接解（質心速度法）交叉驗證
mp_, mpi0 = 938.27, 134.98
Kth2 = mpi0 * (4 * mp_ + mpi0) / (2 * mp_)
# 交叉：給定 KE，質心能量 sqrt(2 mp^2 + 2 E1 mp) 恰等於 2mp+mpi
E1 = Kth2 + mp_
check("sf-12-2 sqrt(s)", math.sqrt(2 * mp_ ** 2 + 2 * E1 * mp_), 2 * mp_ + mpi0, 1e-12)
check("sf-12-2 KE_th", Kth2, 279.7, 1e-3)
check("sf-12-2 check 1-38 (6mc^2)", ((4) ** 2 - (2) ** 2) / 2, 6, 1e-12)
check("sf-12-2 collider per beam", mpi0 / 2, 67.5, 0.001)

print()
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("ALL ADDED-PROBLEM CHECKS PASSED")
