"""近代物理第 1 章 §1–§7 詳解改寫（R1a）中新寫出的中間數值驗算：python tools/verify_modern_ch01_detail_R1a.py

每個 chk(名稱, 算出值, 頁面上寫的值, 相對誤差容許) 都必須通過。
"""
import sys
from math import sqrt, pi, atan, tan, radians, degrees, log10

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

C3 = 3.00e8      # 頁面多數題目用的 c
C = 2.998e8      # 例題 1.1 等用的 c
FAIL = []


def g(b):
    return 1 / sqrt(1 - b * b)


def chk(name, got, shown, rel=0.01):
    ok = abs(got - shown) <= rel * abs(shown) if shown != 0 else abs(got) < 1e-12
    print(("OK  " if ok else "FAIL"), name, f"算出 {got:.6g}", f"頁面 {shown:.6g}")
    if not ok:
        FAIL.append(name)


# ---------------- 01-postulates ----------------
# bz-1-1：汽車 100 km/h
v = 100 / 3.6
chk("bz-1-1 100 km/h in m/s", v, 27.8, 0.005)
chk("bz-1-1 gamma-1 現在光速", v**2 / (2 * C3**2), 4.3e-15, 0.02)
chk("bz-1-1 c=200km/h 時 gamma", g(0.5), 1.155, 0.001)
chk("bz-1-1 鐘少走比例", 1 - 1 / g(0.5), 0.134, 0.01)
# sf-01-1：Michelson–Morley
b = 3.0e4 / C3
chk("sf-01-1 beta", b, 1.0e-4)
chk("sf-01-1 dt", 11 / C3 * b**2, 3.7e-16, 0.02)
chk("sf-01-1 dt 精確式", (2 * 11 / C3) * (1 / (1 - b * b) - 1 / sqrt(1 - b * b)), 3.7e-16, 0.02)
chk("sf-01-1 光程差", 11 * b**2, 1.1e-7)
chk("sf-01-1 條紋", 2 * 11 * b**2 / 590e-9, 0.37, 0.02)
chk("sf-01-1 條紋/上限", 2 * 11 * b**2 / 590e-9 / 0.01, 37, 0.02)
# sf-01-2：發射理論雙星
b = 3.0e4 / C3
dt_y = 1000 * 2 * b / (1 - b * b)
chk("sf-01-2 dt 年", dt_y, 0.20)
chk("sf-01-2 dt 天", dt_y * 365, 73)
chk("sf-01-2 抵達差", 5 - dt_y * 365, -68)

# ---------------- 02-time ----------------
r = 1 - (3600 / 3601) ** 2
chk("bz-ex1-1 7201/12967201", 7201 / 12967201, 5.553e-4, 0.001)
chk("bz-ex1-1 1-(t0/t)^2", r, 5.553e-4, 0.001)
chk("bz-ex1-1 sqrt", sqrt(r), 0.02357, 0.001)
chk("bz-ex1-1 v", C * sqrt(r), 7.1e6, 0.01)
chk("bz-1-3 gamma_u-1 跑者", 10**2 / (2 * C3**2), 5.6e-16, 0.01)
chk("bz-1-3 gamma(0.6)", g(0.6), 1.25, 1e-9)
chk("bz-1-4 sqrt(1-0.49)", sqrt(0.51), 0.714, 0.001)
chk("bz-1-4 t0", 40 * 0.714, 28.6, 0.002)
s = sqrt(1 - (2 / 3) ** 2)
chk("bz-1-5 sqrt5/3", s, 0.7454, 0.0001)
chk("bz-1-5 1-0.7454", 1 - 0.7454, 0.2546, 1e-6)
chk("bz-1-5 t", 1 / (1 - s), 3.93, 0.002)
chk("bz-1-5 B 讀數", 3.93 * 0.7454, 2.93, 0.002)
chk("bz-1-6 beta", 300 / C3, 1.0e-6)
chk("bz-1-6 v^2/2c^2", (300 / C3) ** 2 / 2, 5.0e-13)
chk("bz-1-6 t", 1 / 5.0e-13, 2.0e12)
chk("bz-1-6 年", 2.0e12 / 3.16e7, 6.3e4, 0.01)
chk("bz-1-7 beta", sqrt(3) / 2, 0.866, 0.001)
chk("bz-1-7 v", 0.866 * C3, 2.60e8, 0.002)
chk("bz-1-8 v^2", 1.08e4**2, 1.166e8, 0.001)
chk("bz-1-8 v^2/2c^2", 1.08e4**2 / (2 * C3**2), 6.48e-10, 0.001)
chk("bz-1-8 dt", 6.48e-10 * 86400, 5.6e-5, 0.01)
chk("bz-1-9 1-0.99^2", 1 - 0.99**2, 0.0199, 1e-6)
chk("bz-1-9 sqrt", sqrt(0.0199), 0.1411, 0.001)
chk("bz-1-9 gamma", g(0.99), 7.09, 0.001)
chk("bz-1-9 d", 0.99 * C3 * 7.09e-7, 210, 0.01)
chk("bz-1-9 古典 d", 0.99 * C3 * 1e-7, 29.7, 0.001)
b = sqrt(1 - 1 / 29.3**2)
chk("sf-02-1 29.3^2", 29.3**2, 858.5, 0.0005)
chk("sf-02-1 1/858.5", 1 / 858.5, 0.001165, 0.001)
chk("sf-02-1 beta", b, 0.99942, 1e-5)
chk("sf-02-1 tau", 29.3 * 2.197, 64.4, 0.001)
chk("sf-02-1 d", b * C3 * 64.4e-6, 1.93e4, 0.005)
chk("sf-02-1 周長", 2 * pi * 7.0, 44.0, 0.001)
chk("sf-02-1 N", 1.93e4 / (2 * pi * 7.0), 440, 0.01)
chk("sf-02-1 古典距離", b * C3 * 2.197e-6, 659, 0.001)
chk("sf-02-1 古典圈數", 659 / 44.0, 15, 0.01)
chk("sf-02-1 v", b * C3, 2.998e8, 0.0002)
chk("sf-02-1 a", (b * C3) ** 2 / 7.0, 1.3e16, 0.02)
chk("sf-02-1 a/g", (b * C3) ** 2 / 7.0 / 9.8, 1.3e15, 0.02)
b = 10 / sqrt(101)
chk("sf-02-2 beta", b, 0.99504, 1e-5)
chk("sf-02-2 1-beta", 1 - b, 4.96e-3, 0.002)
chk("sf-02-2 gamma", g(b), 10.05, 0.001)
chk("sf-02-2 gamma*beta", g(b) * b, 10.0, 1e-9)
chk("sf-02-2 T", sqrt(10**2 + 100**2), 100.5, 0.001)

# ---------------- 03-doppler ----------------
chk("bz-ex1-2 5.6^2", 5.6**2, 31.36, 1e-9)
chk("bz-ex1-2 4.8^2", 4.8**2, 23.04, 1e-9)
b = 8.32 / 54.40
chk("bz-ex1-2 beta", b, 0.153, 0.002)
chk("bz-ex1-2 v", b * C3, 4.59e7, 0.002)
chk("bz-ex1-2 km/h", 4.59e7 * 3.6, 1.65e8, 0.002)
chk("bz-ex1-2 罰款", b * C3 * 3.6 - 80, 1.65e8, 0.002)
b = 6.12e7 / C3
chk("kg-107-1 beta", b, 0.204, 1e-6)
chk("kg-107-1 1.204/0.796", 1.204 / 0.796, 1.513, 0.0005)
chk("kg-107-1 factor", sqrt((1 + b) / (1 - b)), 1.230, 0.0005)
chk("kg-107-1 lambda", 500 * sqrt((1 + b) / (1 - b)), 615, 0.001)
chk("kg-107-1 dlambda", 500 * sqrt((1 + b) / (1 - b)) - 500, 115, 0.01)
chk("bz-1-10 0.03/1.97", 0.03 / 1.97, 0.01523, 0.001)
chk("bz-1-10 factor", sqrt(0.03 / 1.97), 0.1234, 0.001)
chk("bz-1-10 rate", 1e4 * sqrt(0.03 / 1.97), 1.23e3, 0.005)
b = 1.5e7 / C3
chk("bz-1-11 beta", b, 0.050)
chk("bz-1-11 1.05/0.95", 1.05 / 0.95, 1.105, 0.001)
chk("bz-1-11 factor", sqrt(1.05 / 0.95), 1.051, 0.001)
chk("bz-1-11 lambda", 550 * sqrt(1.05 / 0.95), 578, 0.001)
chk("bz-1-12 beta", 5 / 13, 0.385, 0.001)
chk("bz-1-12 回代", sqrt((1 - 5 / 13) / (1 + 5 / 13)), 2 / 3, 1e-9)
chk("bz-1-12 v", 5 / 13 * C3, 1.15e8, 0.005)
chk("bz-1-13 beta", sqrt(2e-9), 4.47e-5, 0.001)
chk("bz-1-13 v", sqrt(2e-9) * C3, 1.34e4, 0.002)
# 精確解（不用近似）也要給 1.34e4
lo, hi = 1e-6, 1e-3
for _ in range(200):
    mid = (lo + hi) / 2
    f = 1e9 / (1 + mid) * (1 - sqrt(1 - mid * mid)) - 1
    lo, hi = (mid, hi) if f < 0 else (lo, mid)
chk("bz-1-13 精確 v", lo * C3, 1.34e4, 0.002)
v = 150 / 3.6
chk("bz-1-14 v", v, 41.7, 0.001)
chk("bz-1-14 beta", v / C3, 1.39e-7, 0.002)
chk("bz-1-14 dnu", 2 * v / C3 * 15e9, 4.2e3, 0.01)
chk("bz-1-14 精確 dnu", 15e9 * ((1 + v / C3) / (1 - v / C3) - 1), 4.2e3, 0.01)
b = 0.19 / 1.81
chk("sf-03-1 beta", b, 0.105, 0.001)
chk("sf-03-1 近似 beta", 0.19 / 2, 0.095, 1e-9)
chk("sf-03-1 誤差", (0.105 - 0.095) / 0.105, 0.095, 0.01)
b = 0.0050
ff = sqrt((1 - b) / (1 + b)); fb = sqrt((1 + b) / (1 - b))
chk("sf-03-2 前因子", ff, 0.995012, 1e-6)
chk("sf-03-2 後因子", fb, 1.005013, 1e-6)
chk("sf-03-2 lam_f", 486.1 * ff, 483.68, 1e-5)
chk("sf-03-2 lam_b", 486.1 * fb, 488.54, 1e-5)
chk("sf-03-2 平均=gamma*lam0", (486.1 * ff + 486.1 * fb) / 2, g(b) * 486.1, 1e-12)
chk("sf-03-2 位移", (g(b) - 1) * 486.1, 6.1e-3, 0.01)
chk("sf-03-2 b^2/2", b * b / 2, 1.25e-5, 1e-9)
chk("sf-03-2 (483.68+488.54)/2", (483.68 + 488.54) / 2, 486.11, 1e-6)

# ---------------- 04-length ----------------
chk("bz-1-17 sqrt(0.19)", sqrt(0.19), 0.436, 0.001)
chk("bz-1-17 L", 6 * 0.436, 2.6, 0.01)
chk("bz-1-18 L0", 1.3 / 0.8, 1.6, 0.02)
chk("bz-1-18 錯誤做法", 1.3 * 0.8, 1.04, 1e-9)
chk("bz-1-19 L", sqrt(0.99), 0.995, 0.0005)
chk("bz-1-19 t", 0.995 / 3.0e7, 3.32e-8, 0.002)
chk("bz-1-20 beta", sqrt(0.75), 0.866, 0.001)
chk("bz-1-20 v", 0.866 * C3, 2.60e8, 0.002)
chk("bz-1-20 t", 0.5 / (0.866 * C3), 1.92e-9, 0.003)
chk("bz-1-21 tan10", tan(radians(10)), 0.176, 0.002)
chk("bz-1-21 sqrt(0.51)", sqrt(0.51), 0.714, 0.001)
chk("bz-1-21 tan", tan(radians(10)) / sqrt(0.51), 0.247, 0.002)
chk("bz-1-21 deg", degrees(atan(tan(radians(10)) / sqrt(0.51))), 13.9, 0.003)
gm = g(0.8)
chk("sf-04-1 gamma", gm, 5 / 3, 1e-9)
chk("sf-04-1 L", 120 / gm, 72, 1e-9)
chk("sf-04-1 t站", 72 / (0.8 * C3), 3.0e-7, 1e-9)
chk("sf-04-1 t船", 120 / (0.8 * C3), 5.0e-7, 1e-9)
chk("sf-04-1 比值", 5.0 / 3.0, gm, 1e-9)
gm = g(0.6)
chk("sf-04-2 gamma", gm, 1.25, 1e-9)
chk("sf-04-2 d_par", sqrt(2) / gm, 1.131, 0.001)
chk("sf-04-2 alpha", degrees(atan(gm)), 51.3, 0.001)
chk("sf-04-2 2alpha", 2 * degrees(atan(gm)), 102.7, 0.001)
chk("sf-04-2 另角", 180 - 2 * degrees(atan(gm)), 77.3, 0.002)
chk("sf-04-2 s", sqrt((1 + 1 / gm**2) / 2), 0.906, 0.001)
chk("sf-04-2 A", 1 / gm, 0.80, 1e-9)

# ---------------- 05-twin ----------------
chk("bz-ex1-4 T1", sqrt(1.8 / 0.2), 3, 1e-9)
chk("bz-ex1-4 T2", sqrt(0.2 / 1.8), 1 / 3, 1e-9)
chk("bz-ex1-4 Jane 單程", 20 / 0.8, 25, 1e-9)
chk("bz-ex1-4 Dick 單程", 25 * sqrt(1 - 0.64), 15, 1e-9)
chk("bz-ex1-4 Dick 收", 15 / 3 + 15 * 3, 50, 1e-9)
chk("bz-ex1-4 Jane 收", 45 / 3 + 5 * 3, 30, 1e-9)
chk("bz-1-22 tB", 24 / 0.6, 40, 1e-9)
chk("bz-1-22 tA", 40 * sqrt(1 - 0.36), 32, 1e-9)
chk("bz-1-22 間隔", sqrt(1.6 / 0.4), 2, 1e-9)
chk("bz-1-22 A 收", 16 / 2 + 16 * 2, 40, 1e-9)
chk("bz-1-22 B 收", 32 / 2 + 8 * 2, 32, 1e-9)
t = 8 / 0.9
chk("bz-1-23 t", t, 8.89, 0.001)
chk("bz-1-23 t0", t * sqrt(0.19), 3.87, 0.002)
chk("bz-1-23 差", t - t * sqrt(0.19), 5.0, 0.01)
chk("sf-05-1 tB1", 4.8 / 0.6, 8.0, 1e-9)
chk("sf-05-1 tA1", 8.0 * 0.8, 6.4, 1e-9)
chk("sf-05-1 tB2", 4.8 / 0.8, 6.0, 1e-9)
chk("sf-05-1 tA2", 6.0 * 0.6, 3.6, 1e-9)
chk("sf-05-1 A 收", 6.4 / sqrt(1.6 / 0.4) + 3.6 / sqrt(0.2 / 1.8), 14.0, 1e-9)
chk("sf-05-1 B 收", 12.8 / 2 + 1.2 * 3, 10.0, 1e-9)
for bb in (0.3, 0.6, 0.8, 0.95):
    k = sqrt((1 + bb) / (1 - bb))
    chk(f"sf-05-2 (k+1/k)/2=gamma beta={bb}", (k + 1 / k) / 2, g(bb), 1e-12)
chk("sf-05-2 例題1.4 N", 15 * (3 + 1 / 3), 50, 1e-9)

# ---------------- 06-em ----------------
for bb in (0.1, 0.5, 0.9):
    gm = g(bb)
    chk(f"sf-06-1 gamma-1/gamma = gamma b^2 (b={bb})", gm - 1 / gm, gm * bb * bb, 1e-12)
    chk(f"sf-06-1 gamma^2-1 = gamma^2 b^2 (b={bb})", gm * gm - 1, gm * gm * bb * bb, 1e-12)
eps0, mu0, e = 8.85e-12, 4 * pi * 1e-7, 1.60e-19
chk("sf-06-1 eps0*mu0*c^2", eps0 * mu0 * C**2, 1.0, 0.002)
lam0 = 8.5e28 * e * 1.0e-6
chk("sf-06-2 lambda0", lam0, 1.36e4, 0.001)
v = 10 / lam0
chk("sf-06-2 v", v, 7.3e-4, 0.01)
chk("sf-06-2 v/c", v / C3, 2.45e-12, 0.002)
b2 = (v / C3) ** 2
chk("sf-06-2 beta^2", b2, 6.0e-24, 0.01)
lp = b2 * lam0
chk("sf-06-2 lambda'", lp, 8.2e-20, 0.01)
chk("sf-06-2 e/lambda'", e / lp, 2.0, 0.03)
chk("sf-06-2 nA", 8.5e28 * 1e-6, 8.5e22, 1e-9)
chk("sf-06-2 F/l 電力式", lam0 * lp / (2 * pi * eps0 * 0.010), 2.0e-3, 0.01)
chk("sf-06-2 F/l 安培式", mu0 * 100 / (2 * pi * 0.010), 2.0e-3, 1e-9)
chk("sf-06-2 F/l 無抵消", lam0**2 / (2 * pi * eps0 * 0.010), 3.3e20, 0.01)

# ---------------- 07-momentum ----------------
# kg-115-1：符號驗證 d(gamma v)/dv = gamma^3，再看 0.8c 的數值
try:
    import sympy as sp
    vv, cc = sp.symbols("v c", positive=True)
    expr = sp.diff(vv / sp.sqrt(1 - vv**2 / cc**2), vv) - (1 - vv**2 / cc**2) ** sp.Rational(-3, 2)
    ok = sp.simplify(expr) == 0
    print(("OK  " if ok else "FAIL"), "kg-115-1 d(gamma v)/dv = gamma^3（sympy）")
    if not ok:
        FAIL.append("kg-115-1 sympy")
    # sf-07-1 積分 ∫ u/sqrt(1+u^2) du = sqrt(1+u^2)
    u = sp.symbols("u", positive=True)
    ok = sp.simplify(sp.diff(sp.sqrt(1 + u**2), u) - u / sp.sqrt(1 + u**2)) == 0
    print(("OK  " if ok else "FAIL"), "sf-07-1 積分提示（sympy）")
    if not ok:
        FAIL.append("sf-07-1 sympy")
except ImportError:
    print("（沒有 sympy，略過符號驗證）")
gm = g(0.8)
chk("kg-115-1 gamma", gm, 1.67, 0.002)
chk("kg-115-1 gamma^3", gm**3, 4.63, 0.001)
chk("kg-115-1 gamma^2", gm**2, 2.78, 0.001)
chk("bz-1-24 gamma0.2", g(0.2), 1.0206, 1e-4)
chk("bz-1-24 gamma0.4", g(0.4), 1.0911, 1e-4)
chk("bz-1-24 gamma0.8", g(0.8), 1.6667, 1e-4)
chk("bz-1-24 比 a", g(0.4) / g(0.2), 1.069, 0.0005)
chk("bz-1-24 比 b", g(0.8) / g(0.4), 1.528, 0.0005)
chk("bz-1-24 a", 2 * g(0.4) / g(0.2), 2.14, 0.002)
chk("bz-1-24 b", 2 * g(0.8) / g(0.4), 3.06, 0.002)
chk("bz-1-25 gamma(0.6)", g(0.6), 1.25, 1e-9)
chk("bz-1-25 V_B/V_A", 1 / g(0.6), 0.8, 1e-9)
chk("bz-1-25 gamma m V_B", g(0.6) * 0.8, 1.0, 1e-9)
for bb in (0.2, 0.6, 0.9):
    p_over_mc = g(bb) * bb
    chk(f"bz-1-26 sqrt(1+p^2/m^2c^2)=gamma b={bb}", sqrt(1 + p_over_mc**2), g(bb), 1e-12)
chk("bz-1-26 p=mc 時 gamma", sqrt(2), 1.414, 0.0005)
chk("bz-1-26 p=mc 時 beta", sqrt(1 - 1 / 2), 0.707, 0.0005)
m, e, E = 9.11e-31, 1.60e-19, 1.00e6
gb = 0.99 / sqrt(1 - 0.99**2)
chk("sf-07-1 gamma beta", gb, 7.02, 0.001)
chk("sf-07-1 分子", 7.02 * m * C3, 1.92e-21, 0.002)
chk("sf-07-1 eE", e * E, 1.60e-13, 1e-9)
chk("sf-07-1 t", gb * m * C3 / (e * E), 1.20e-8, 0.003)
chk("sf-07-1 t 古典", 0.99 * m * C3 / (e * E), 1.69e-9, 0.003)
chk("sf-07-1 比", 0.99 / 7.02, 1 / 7, 0.02)
chk("sf-07-1 gamma", g(0.99), 7.09, 0.001)
chk("sf-07-1 x", 0.511 * (g(0.99) - 1), 3.1, 0.01)
chk("sf-07-1 sqrt(1+(gb)^2)=gamma", sqrt(1 + gb**2), g(0.99), 1e-12)
# 數值積分確認距離公式
N = 200000
tt = gb * m * C3 / (e * E)
F = e * E
x = sum(F * (i + 0.5) * tt / N / m / sqrt(1 + (F * (i + 0.5) * tt / N / (m * C3)) ** 2) for i in range(N)) * tt / N
chk("sf-07-1 x 數值積分（mc^2 用 c=3.00e8）", x, m * C3**2 / F * (g(0.99) - 1), 1e-6)
gm = 7.46e3
chk("sf-07-2 1-beta", 1 / (2 * gm**2), 9.0e-9, 0.01)
chk("sf-07-2 1-beta 精確", 1 - sqrt(1 - 1 / gm**2), 9.0e-9, 0.01)
p = gm * 1.673e-27 * C3
chk("sf-07-2 p", p, 3.74e-15, 0.002)
chk("sf-07-2 er", 1.60e-19 * 2804, 4.49e-16, 0.002)
chk("sf-07-2 B", p / (1.60e-19 * 2804), 8.3, 0.01)

print()
print("全部通過" if not FAIL else f"失敗 {len(FAIL)} 項：{FAIL}")
sys.exit(1 if FAIL else 0)
