"""光學 ch10（講義第十章｜光的干涉，課本 Pedrotti 第 7 章）所有題目卡的數值獨立驗算。

用法：python tools/verify_optics_ch10.py    全部通過時印出 ALL OK，否則結束碼 1。
"""
import math
import sys

import numpy as np

EPS0, C = 8.854e-12, 3.0e8
fails = []


def check(name, got, want, rel=2e-3):
    ok = abs(got - want) <= rel * abs(want) + 1e-15
    print(f"{'OK ' if ok else 'BAD'} {name}: {got:.6g} (預期 {want:.6g})")
    if not ok:
        fails.append(name)


def visibility(N):
    return 2 * math.sqrt(N) / (N + 1)


def ratio_from_V(V):
    """V = 2√N/(N+1) 反解 N（取 N>1 的根）：√N = (1+√(1-V²))/V"""
    s = (1 + math.sqrt(1 - V * V)) / V
    return s * s


# ---------- 作業 7-1：兩道同調光的照度、干涉項、淨照度、對比度 ----------
I1 = 0.5 * EPS0 * C * 3000 ** 2
I2 = 0.5 * EPS0 * C * 4000 ** 2
delta = math.pi / 3 + (math.pi / 5 - math.pi / 6)   # 相位 (ks1+π/5)-(ks2+π/6)，k(s1-s2)=+π/3
I12 = 2 * math.sqrt(I1 * I2) * math.cos(delta)
check("7-1 I1 (W/m^2)", I1, 11950, 2e-3)
check("7-1 I2 (W/m^2)", I2, 21250, 2e-3)
check("7-1 delta (deg)", math.degrees(delta), 66.0)
check("7-1 I12 (W/m^2)", I12, 12960, 2e-3)
check("7-1 I (W/m^2)", I1 + I2 + I12, 46170, 2e-3)
check("7-1 V", 2 * math.sqrt(I1 * I2) / (I1 + I2), 0.96, 1e-6)
# 直接數值疊加驗證：時間平均 <(E1+E2)^2>
t = np.linspace(0, 2 * np.pi, 200001)[:-1]
E = 3000 * np.cos(math.pi / 3 + math.pi / 5 - t) + 4000 * np.cos(math.pi / 6 - t)
check("7-1 I 直接時間平均", EPS0 * C * np.mean(E ** 2), I1 + I2 + I12, 1e-6)

# ---------- 作業 7-6：436 nm 第 4 暗紋 = 另一波長第 3 亮紋 ----------
check("7-6 lambda (nm)", 3.5 * 436 / 3, 508.7)

# ---------- 作業 7-11：雙稜鏡角 ----------
lam, n, dy = 589.3e-9, 1.5, 0.03e-2
alpha = 3 * lam / (2 * (n - 1) * dy)
check("7-11 alpha (rad)", alpha, 5.893e-3)
check("7-11 alpha (arcmin)", math.degrees(alpha) * 60, 20.26)

# ---------- 作業 7-14：油膜 525、675 nm 反射消光 ----------
for m in range(0, 10):
    if abs((m + 1.5) * 525 - (m + 0.5) * 675) < 1e-9:
        m675 = m
check("7-14 m(675)", m675, 3)
tt = (m675 + 0.5) * 675 / (2 * 1.30)
check("7-14 t (nm)", tt, 908.65)
check("7-14 t 由 525 nm, m=4", 4.5 * 525 / 2.6, tt, 1e-9)

# ---------- 作業 7-20：空氣楔 40 條亮紋 ----------
check("7-20 t (um)", 39.5 * 589e-9 / 2 * 1e6, 11.63)

# ---------- 作業 7-23：第 10 亮環直徑 7.89 mm ----------
r = 7.89e-3 / 2
check("7-23 R (m)", r ** 2 / (9.5 * 546.1e-9), 3.000)

# ---------- 對比度考古題 ----------
for name, N in (("2013期中 N=4", 4), ("2017平時 N=3", 3)):
    check(name + " V", visibility(N), {4: 0.8, 3: math.sqrt(3) / 2}[N])
for name, V, want in (("2009/2012 V=1/2", 0.5, 7 + 4 * math.sqrt(3)),
                      ("2018 V=3/4", 0.75, ((4 + math.sqrt(7)) / 3) ** 2),
                      ("2014 V=2/3", 2 / 3, (7 + 3 * math.sqrt(5)) / 2),
                      ("2013/2017 V=1/3", 1 / 3, 17 + 12 * math.sqrt(2))):
    N = ratio_from_V(V)
    check(name + " N", N, want, 1e-9)
    check(name + " 代回 V", visibility(N), V, 1e-9)
check("2009 N 數值", ratio_from_V(0.5), 13.93)
check("2018 N 數值", ratio_from_V(0.75), 4.907)
check("2014 N 數值", ratio_from_V(2 / 3), 6.854)
check("2013 N 數值", ratio_from_V(1 / 3), 33.97)

# ---------- 2018 期中第 4 題：楊氏 ----------
a, lam = 0.6e-3, 550e-9
L = a * 1e-3 / lam
check("2018 Young L (m)", L, 1.0909)
shift = (1.5 - 1) * 200e-6 * L / a
check("2018 Young shift (cm)", shift * 100, 18.18)
check("2018 Young 移動條紋數", (1.5 - 1) * 200e-6 / lam, 181.8)

# ---------- 雙稜鏡 ----------
def biprism(lam, n, d, k, dy):
    Lt = d + k * d
    sep = Lt * lam / dy
    return sep, sep / (2 * d * (n - 1))
sep, al = biprism(589.3e-9, 1.8, 0.10, 2, 0.02e-2)
check("2017 biprism a (cm)", sep * 100, 0.08840)
check("2017 biprism alpha (rad)", al, 5.525e-3)
sep, al = biprism(632.8e-9, 1.6, 0.20, 3, 0.04e-2)
check("2022 biprism a (cm)", sep * 100, 0.1266)
check("2022 biprism alpha (rad)", al, 5.273e-3)

# ---------- 2007 平時考第 1 題：三層膜 ----------
vis = [8000 / (m - 0.5) for m in range(1, 40) if 400 <= 8000 / (m - 0.5) <= 700]
check("2007 可見光個數", len(vis), 9)
check("2007 最長可見", vis[0], 695.65)
check("2007 最短可見", vis[-1], 410.26)

# ---------- 2007 期中第 2 題：TM 薄膜，兩面反射相位差恆為 π ----------
n0, n1 = 1.0, 1.2
thp = math.degrees(math.atan(n1 / n0))
check("2007期中 Brewster (deg)", thp, 50.194)
def rTM(ni, nt, ti):
    tt_ = math.asin(ni * math.sin(ti) / nt)
    return (-nt * math.cos(ti) + ni * math.cos(tt_)) / (nt * math.cos(ti) + ni * math.cos(tt_)), tt_
bad = 0
for deg in list(range(0, 50)) + list(range(51, 90)):
    ti = math.radians(deg)
    rt, tt_ = rTM(n0, n1, ti)
    rb, _ = rTM(n1, n0, tt_)
    if not (rt * rb < 0):
        bad += 1
check("2007期中 上下兩面 r_TM 異號的角度（應全部）", 89 - bad, 89)

# ---------- 2017 期中第 4 題：膜厚 ----------
check("2017 film d (nm)", 0.8 / 1 * 546.1 / 2, 218.44)

# ---------- 牛頓環：亮環 r²=(m-1/2)λR，暗環 r²=mλR（第一暗環 m=1，中心暗點不算）----------
def bright(m, lam, R):
    return math.sqrt((m - 0.5) * lam * R)
def dark(m, lam, R):
    return math.sqrt(m * lam * R)
# 2007 平時考：第一暗環 2 mm
R = (2e-3) ** 2 / 633e-9
check("2007 R (m)", R, 6.319)
check("2007 f (m)", R / 0.5, 12.64)
# 2012 平時考
R = (1e-3) ** 2 / 633e-9
check("2012 R (m)", R, 1.580)
check("2012 f (m)", R / 0.5, 3.160)
check("2012 r5 dark (mm)", dark(5, 633e-9, R) * 1e3, math.sqrt(5))
# 2008：n=7/4, f=10 m
R = (7 / 4 - 1) * 10
check("2008 R", R, 7.5)
check("2008 r1 bright (mm)", bright(1, 633e-9, R) * 1e3, 1.5408)
check("2008 r5 dark (mm)", dark(5, 633e-9, R) * 1e3, 4.8723)
# 2010：n=1.720, f=6
R = 0.72 * 6
check("2010 r1 dark (mm)", dark(1, 633e-9, R) * 1e3, 1.6537)
check("2010 r3 bright (mm)", bright(3, 633e-9, R) * 1e3, 2.6147)
# 2011：n=8/5, f=8
R = 0.6 * 8
check("2011 r1 dark (m)", dark(1, 532e-9, R), 1.598e-3)
check("2011 r5 bright (m)", bright(5, 532e-9, R), 3.390e-3)
# 2021：f=5.00, n=1.7076
R = 0.7076 * 5
check("2021 R", R, 3.538)
check("2021 r3 bright (mm)", bright(3, 656.3e-9, R) * 1e3, 2.4093)
check("2021 r6 bright (mm)", bright(6, 656.3e-9, R) * 1e3, 3.5733)
# 2025：f=6.00, n=1.7328
R = 0.7328 * 6
check("2025 R", R, 4.3968)
check("2025 r2 bright (mm)", bright(2, 486.1e-9, R) * 1e3, 1.7908)
check("2025 r4 dark (mm)", dark(4, 486.1e-9, R) * 1e3, 2.9239)
# 精確式 R=(r²+t²)/2t 與近似 r²=2Rt 的差（以 2025 第 4 暗環為例）
t4 = 4 * 486.1e-9 / 2
r_exact = math.sqrt(2 * R * t4 - t4 ** 2)
check("2025 近似與精確差 < 1e-6 相對", r_exact, dark(4, 486.1e-9, R), 1e-6)

# 兩波長重合：(m1 - 1/2)λ1 = (m2 - 1/2)λ2（亮-亮）
def two(m1, lam1, m2, R, kind1="b"):
    k1 = (m1 - 0.5) if kind1 == "b" else m1
    lam2 = k1 * lam1 / (m2 - 0.5)
    t_ = k1 * lam1 / 2
    r_ = math.sqrt(2 * R * t_) if R else None
    return lam2, r_, t_
l2, r_, t_ = two(10, 546e-9, 9, 1.0)
check("2009 lambda2 (nm)", l2 * 1e9, 610.24)
check("2009 r (mm)", r_ * 1e3, 2.2775)
check("2009 t (um)", t_ * 1e6, 2.5935)
l2, r_, t_ = two(11, 546e-9, 10, 1.0)
check("2013平時 lambda2 (nm)", l2 * 1e9, 603.5)
check("2013平時 r (mm, R=1 m)", r_ * 1e3, 2.39)
check("2013平時 t (um)", t_ * 1e6, 2.87)
l2, r_, t_ = two(10, 532e-9, 8, 0.8)
check("2014 lambda2 (nm)", l2 * 1e9, 673.87)
check("2014 r (mm)", r_ * 1e3, 2.0107)
check("2014 t (nm)", t_ * 1e9, 2527)
l2, r_, t_ = two(8, 589e-9, 7, 0.8, kind1="d")
check("2017平時 lambda2 (nm)", l2 * 1e9, 724.92)
check("2017平時 r (mm)", r_ * 1e3, 1.9416)
check("2017平時 t (nm)", t_ * 1e9, 2356)
l2, r_, t_ = two(4, 532e-9, 3, 0.8)
check("2020 lambda2 (nm)", l2 * 1e9, 744.8)
check("2020 r (mm)", r_ * 1e3, 1.2205)
check("2020 t (nm)", t_ * 1e9, 931)
l2, r_, t_ = two(6, 589.2e-9, 8, 0.5)
check("2024 lambda2 (nm)", l2 * 1e9, 432.08)
check("2024 r (mm)", r_ * 1e3, 1.2729)

# ---------- 考前衝刺變化題 ----------
check("var1 V(N=9)", visibility(9), 0.6, 1e-9)
check("var1 N(V=0.8)", ratio_from_V(0.8), 4.0, 1e-9)
check("var2 t (um)", 10 * 600e-9 / 0.6 * 1e6, 10.0)
check("var2 shift (mm)", 10 * 600e-9 * 1 / 0.5e-3 * 1e3, 12.0)
check("var3 dy (mm)", 500e-9 * 1.0 / (2 * 0.05 * 0.5 * 0.01) * 1e3, 1.0)
check("var4 dy (mm)", 600e-9 * 2 / 1e-3 * 1e3, 1.2)
check("var5 r3 bright (mm)", bright(3, 500e-9, 1.0) * 1e3, 1.118)
check("var5 r3 dark (mm)", dark(3, 500e-9, 1.0) * 1e3, 1.2247)
l2, r_, t_ = two(5, 600e-9, 6, 1.0, kind1="d")
check("var6 lambda2 (nm)", l2 * 1e9, 545.45)
check("var6 r (mm)", r_ * 1e3, 1.732)
for m in range(1, 10):
    if abs((m - 0.5) * 630 - (m + 0.5) * 450) < 1e-9:
        mv = m
check("var7 m", mv, 3)
check("var7 t (nm)", 2.5 * 630 / (2 * 1.33), 592.1)

print("ALL OK" if not fails else f"FAILED: {fails}")
sys.exit(1 if fails else 0)
