"""光學 ch10 考試書寫版（exam.html 的「背公式＋代數字」寫法）中出現的數值驗算。

只驗算書寫版裡寫出來的中間值與答案（答案本身另由 tools/verify_optics_ch10.py 驗算）。
用法：python tools/verify_writeup_optics_ch10.py    全部通過時印出 ALL OK，否則結束碼 1。
"""
import math
import sys

import sympy as sp

EPS0, C = 8.854e-12, 3.0e8
fails = []


def check(name, got, want, rel=5e-3):  # 三位有效數字四捨五入的誤差上限
    """got 是精確計算值，want 是書寫版上寫的（已四捨五入的）數字。"""
    ok = abs(got - want) <= rel * abs(want) + 1e-15
    print(f"{'OK ' if ok else 'BAD'} {name}: {got:.6g}（書寫版 {want:.6g}）")
    if not ok:
        fails.append(name)


def V(N):
    return 2 * math.sqrt(N) / (N + 1)


def bright(m, lam, R):  # 第 m 亮環半徑
    return math.sqrt((m - 0.5) * lam * R)


def dark(m, lam, R):  # 第 m 暗環半徑
    return math.sqrt(m * lam * R)


# ---------- o10-7-1 ----------
half = 0.5 * EPS0 * C
I1, I2 = half * 3000 ** 2, half * 4000 ** 2
d = math.pi / 3 + (math.pi / 5 - math.pi / 6)
check("7-1 ½ε0c", half, 1.328e-3)
check("7-1 I1", I1, 1.195e4)
check("7-1 I2", I2, 2.125e4)
check("7-1 δ=11π/30 (deg)", math.degrees(d), 66.0)
check("7-1 √(I1I2)", math.sqrt(I1 * I2), 1.594e4)
check("7-1 cos66°", math.cos(math.radians(66)), 0.4067)
I12 = 2 * math.sqrt(I1 * I2) * math.cos(d)
check("7-1 I12", I12, 1.296e4)
check("7-1 I", I1 + I2 + I12, 4.62e4)
check("7-1 V", 24 / 25, 0.96)

# ---------- 對比度反解：用 sympy 解 V = 2x/(x²+1) ----------
x = sp.symbols("x", positive=True)
for pid, Vv, poly, roots_w, N_w, N_exact in [
    ("k18m3", sp.Rational(3, 4), 3 * x**2 - 8 * x + 3, (2.215, 0.451), 4.91, (23 + 8 * sp.sqrt(7)) / 9),
    ("k09m3", sp.Rational(1, 2), x**2 - 4 * x + 1, (2 + math.sqrt(3), 2 - math.sqrt(3)), 13.9, 7 + 4 * sp.sqrt(3)),
    ("k14q2", sp.Rational(2, 3), x**2 - 3 * x + 1, (2.618, 0.382), 6.85, (7 + 3 * sp.sqrt(5)) / 2),
    ("k13m5/k17q4", sp.Rational(1, 3), x**2 - 6 * x + 1, (5.828, 3 - 2 * math.sqrt(2)), 33.97, 17 + 12 * sp.sqrt(2)),
]:
    # 書寫版的二次方程式的根要和 V=2x/(x²+1) 的解相同（下面逐一比對）
    sols = sorted([float(r) for r in sp.solve(sp.Eq(2 * x / (x**2 + 1), Vv), x)], reverse=True)
    check(f"{pid} 大根", sols[0], roots_w[0])
    check(f"{pid} 小根", sols[1], roots_w[1])
    check(f"{pid} 方程式的根相同", sorted(float(r) for r in sp.solve(poly, x))[-1], sols[0], 1e-9)
    check(f"{pid} N=x²", sols[0] ** 2, N_w)
    check(f"{pid} N 精確式", float(N_exact), sols[0] ** 2, 1e-9)
    check(f"{pid} 回代 V", V(sols[0] ** 2), float(Vv), 1e-9)
check("k13m5 V(4)", V(4), 0.8)
check("k17q4 V(3)", V(3), 0.866)
check("k09m3 小根的 N 是倒數", (2 - math.sqrt(3)) ** 2, 1 / 13.93, 1e-3)

# ---------- 7-6 ----------
check("7-6 λ2", 3.5 * 436 / 3, 508.7)

# ---------- k18m4 ----------
L = 6e-4 * 1e-3 / 550e-9
check("k18m4 L", L, 1.09)
check("k18m4 (n-1)t", 0.5 * 200e-6, 1e-4)
check("k18m4 (n-1)t/λ", 1e-4 / 550e-9, 181.8)
check("k18m4 y", 1e-4 * L / 6e-4, 0.182)

# ---------- 7-11 ----------
a711 = 3 * 589.3e-9 / (2 * 0.5 * 3e-4)
check("7-11 α", a711, 5.89e-3)
check("7-11 α (deg)", math.degrees(a711), 0.338)
check("7-11 α (arcmin)", math.degrees(a711) * 60, 20.3)

# ---------- k22m3 ----------
a22 = 2 * 632.8e-9 / (0.6 * 4e-4)
check("k22m3 L=4d", 4 * 0.20, 0.80)
check("k22m3 α", a22, 5.27e-3)
check("k22m3 a", 2 * 0.20 * 0.6 * a22, 1.27e-3)
check("k22m3 a (cm)", 2 * 0.20 * 0.6 * a22 * 100, 0.127)

# ---------- k17m3 ----------
check("k17m3 L", 0.10 + 0.20, 0.30)
check("k17m3 2d(n-1)", 2 * 0.10 * 0.8, 0.16)
check("k17m3 α", 589.3e-9 * 0.30 / (2 * 0.10 * 0.8 * 2e-4), 5.53e-3)
check("k17m3 a", 589.3e-9 * 0.30 / 2e-4, 8.84e-4)

# ---------- 7-14 ----------
m = sp.symbols("m")
m714 = sp.solve(sp.Eq((m + sp.Rational(1, 2)) * 675, (m + sp.Rational(3, 2)) * 525), m)[0]
check("7-14 m", float(m714), 3)
check("7-14 t(675)", 3.5 * 675 / 2.6, 908.7)
check("7-14 t(525)", 4.5 * 525 / 2.6, 908.7)

# ---------- 7-20 ----------
check("7-20 t (nm)", 39.5 * 589 / 2, 1.163e4)

# ---------- 7-23 ----------
r = 7.89e-3 / 2
check("7-23 r", r, 3.945e-3)
check("7-23 r²", r * r, 1.556e-5)
check("7-23 9.5λ", 9.5 * 546.1e-9, 5.188e-6)
check("7-23 R", r * r / (9.5 * 546.1e-9), 3.00)

# ---------- k25m3 ----------
R = 0.7328 * 6.00
check("k25m3 R", R, 4.397)
check("k25m3 r2²", 1.5 * 486.1e-9 * R, 3.206e-6)
check("k25m3 r2", bright(2, 486.1e-9, R), 1.79e-3)
check("k25m3 r4²", 4 * 486.1e-9 * R, 8.549e-6)
check("k25m3 r4", dark(4, 486.1e-9, R), 2.92e-3)

# ---------- 兩波長重合 ----------
check("k20m4 λ2", 3.5 / 2.5 * 532, 744.8)
check("k20m4 r²", 3.5 * 532e-9 * 0.80, 1.490e-6)
check("k20m4 r", bright(4, 532e-9, 0.80), 1.22e-3)
check("k20m4 t", 3.5 * 532 / 2, 931)
check("k20m4 r=√(2Rt) 一致", math.sqrt(2 * 0.80 * 931e-9), bright(4, 532e-9, 0.80), 1e-6)
check("k24m3 λ2", 5.5 / 7.5 * 589.2, 432.1)
check("k24m3 r²", 5.5 * 589.2e-9 * 0.50, 1.620e-6)
check("k24m3 r", bright(6, 589.2e-9, 0.50), 1.27e-3)
check("k09m4 λ2", 9.5 / 8.5 * 546, 610.2)
check("k09m4 r²", 9.5 * 546e-9 * 1, 5.187e-6)
check("k09m4 r", bright(10, 546e-9, 1), 2.28e-3)
check("k09m4 t", 9.5 * 546 / 2, 2594)
check("k13q3 λ2", 10.5 / 9.5 * 546, 603.5)
check("k13q3 r²", 10.5 * 546e-9 * 1, 5.733e-6)
check("k13q3 r", bright(11, 546e-9, 1), 2.39e-3)
check("k13q3 t", 10.5 * 546 / 2, 2867)
check("k14m3 λ2", 9.5 / 7.5 * 532, 673.9)
check("k14m3 r²", 9.5 * 532e-9 * 0.80, 4.043e-6)
check("k14m3 r", bright(10, 532e-9, 0.80), 2.01e-3)
check("k14m3 t", 9.5 * 532 / 2, 2527)
check("k17q3 λ2", 8 / 6.5 * 589, 724.9)
check("k17q3 r²", 8 * 589e-9 * 0.80, 3.770e-6)
check("k17q3 r", dark(8, 589e-9, 0.80), 1.94e-3)
check("k17q3 t", 8 * 589 / 2, 2356)

# ---------- k17m4 ----------
check("k17m4 Δm", 0.8 / 1, 0.8)
check("k17m4 d", 0.8 * 546.1 / 2, 218.4)

# ---------- k07m2 ----------
check("k07m2 θp", math.degrees(math.atan(1.2)), 50.2)
for deg in [0, 20, 40, 49, 51, 60, 80, 89]:
    ti = math.radians(deg)
    tt = math.asin(math.sin(ti) / 1.2)
    ru = (-1.2 * math.cos(ti) + math.cos(tt)) / (1.2 * math.cos(ti) + math.cos(tt))
    rd = (-math.cos(tt) + 1.2 * math.cos(ti)) / (math.cos(tt) + 1.2 * math.cos(ti))
    check(f"k07m2 r下=-r上 @{deg}°", rd, -ru, 1e-12)
    sign_ok = (ru < 0) == (deg < 50.19)
    check(f"k07m2 r上 正負號 @{deg}°", 1.0 if sign_ok else 0.0, 1.0, 0)
    check(f"k07m2 cosθt 式 @{deg}°", math.cos(tt), math.sqrt(1 - math.sin(ti) ** 2 / 1.44), 1e-12)

# ---------- k07q1 ----------
check("k07q1 Δp (μm)", 2 * 2 * 2, 8)
check("k07q1 m 下限 8000/700", 8000 / 700, 11.4)
lams = [8000 / (k - 0.5) for k in range(12, 21)]
for k, want in zip(range(12, 21), [696, 640, 593, 552, 516, 485, 457, 432, 410]):
    check(f"k07q1 λ0(m={k})", 8000 / (k - 0.5), want)
check("k07q1 m=21 已不在可見光", 1.0 if 8000 / 20.5 < 400 and 8000 / 11.5 < 700 else 0.0, 1.0, 0)

# ---------- k07q2 / k12q3 ----------
R = (2e-3) ** 2 / 633e-9
check("k07q2 R", R, 6.32)
check("k07q2 f", 1 / (0.5 * (0 - 1 / (-R))), 12.6)
R = (1e-3) ** 2 / 633e-9
check("k12q3 R", R, 1.58)
check("k12q3 f", 1 / (0.5 / R), 3.16)
check("k12q3 r5", math.sqrt(5) * 1.0, 2.24)
check("k12q3 r5 直接算 (mm)", dark(5, 633e-9, R) * 1e3, 2.24)

# ---------- 由焦距求 R 的牛頓環 ----------
R = 0.75 * 10
check("k08m4 R", R, 7.5)
check("k08m4 r1²", 0.5 * 633e-9 * R, 2.374e-6)
check("k08m4 r1", bright(1, 633e-9, R), 1.54e-3)
check("k08m4 r5²", 5 * 633e-9 * R, 2.374e-5)
check("k08m4 r5", dark(5, 633e-9, R), 4.87e-3)
R = 0.720 * 6
check("k10m5 R", R, 4.32)
check("k10m5 r1²", 633e-9 * R, 2.735e-6)
check("k10m5 r1", dark(1, 633e-9, R), 1.65e-3)
check("k10m5 r3²", 2.5 * 633e-9 * R, 6.836e-6)
check("k10m5 r3", bright(3, 633e-9, R), 2.61e-3)
R = 0.6 * 8
check("k11m4 R", R, 4.8)
check("k11m4 r1²", 532e-9 * R, 2.554e-6)
check("k11m4 r1", dark(1, 532e-9, R), 1.60e-3)
check("k11m4 r5²", 4.5 * 532e-9 * R, 1.149e-5)
check("k11m4 r5", bright(5, 532e-9, R), 3.39e-3)
R = 0.7076 * 5.00
check("k21m5 R", R, 3.538)
check("k21m5 r3²", 2.5 * 656.3e-9 * R, 5.805e-6)
check("k21m5 r3", bright(3, 656.3e-9, R), 2.41e-3)
check("k21m5 r6²", 5.5 * 656.3e-9 * R, 1.277e-5)
check("k21m5 r6", bright(6, 656.3e-9, R), 3.57e-3)

print()
if fails:
    print("FAILED:", ", ".join(fails))
    sys.exit(1)
print("ALL OK")
