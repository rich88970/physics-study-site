"""光學第八章「考試書寫版」（exam.html）改寫後出現的數值驗算。

每一篇書寫版上出現的中間數值與答案都在這裡重算一次（numpy），
和書寫版寫的數字比對（容許四捨五入誤差）。答案與 sections/*.html 同 id 題目卡一致。

用法：python tools/verify_writeup_optics_ch08.py   全部通過時結束碼 0。
"""
import math
import sys

import numpy as np

PI = math.pi
C = 3e8
EPS = 8.854e-12      # 卷上常數 8.854e-12 或 8.8542e-12，兩者差異不影響有效位數
EPS2 = 8.8542e-12
H = 6.626e-34
FAIL = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        FAIL.append(name)


def near(name, got, want, rel=6e-3):
    """got：重算值；want：書寫版寫的數字。相對誤差 rel 以內算通過。"""
    good = abs(got - want) <= rel * abs(want) if want != 0 else abs(got) < 1e-12
    print(("OK  " if good else "BAD ") + f"{name}: 重算 {got:.6g}，書寫版 {want}")
    if not good:
        FAIL.append(name)


def unit(v):
    v = np.array(v, dtype=float)
    return v / np.linalg.norm(v)


def vec(name, got, want, tol=1e-9):
    good = np.allclose(got, want, atol=tol)
    print(("OK  " if good else "BAD ") + f"{name}: 重算 {np.round(got, 6)}，書寫版 {np.round(want, 6)}")
    if not good:
        FAIL.append(name)


S3 = math.sqrt(3)
S2 = math.sqrt(2)

# ---------------- o8-4-4 ----------------
x, t = np.random.default_rng(0).normal(size=(2, 20))
ok("o8-4-4 x²-20xt+100t² = (x-10t)²", np.allclose(x**2 - 20 * x * t + 100 * t**2, (x - 10 * t) ** 2))

# ---------------- o8-4-7 ----------------
k, w = 628.3, 6283.0
near("o8-4-7 λ=2π/k (cm)", 2 * PI / k, 0.0100)
near("o8-4-7 ν=ω/2π", w / (2 * PI), 1000, 1e-3)
near("o8-4-7 T=2π/ω", 2 * PI / w, 1.00e-3)
near("o8-4-7 v=ω/k", w / k, 10.0)

# ---------------- o8-x13a ----------------
E0 = np.array([6, -2 * S3, 0])
near("o8-x13a |E0|=4√3", np.linalg.norm(E0), 6.93)
vec("o8-x13a ê", unit(E0), [S3 / 2, -0.5, 0])
kv = -PI * 1e7 * np.array([S2 / 2, math.sqrt(6) / 2, 0])
near("o8-x13a k=√2π×10^7", np.linalg.norm(kv), 4.44e7)
vec("o8-x13a k̂ (240°)", unit(kv), [math.cos(math.radians(240)), math.sin(math.radians(240)), 0])
ok("o8-x13a E0·k=0", abs(E0 @ kv) < 1e-6)
kk = np.linalg.norm(kv)
near("o8-x13a λ (nm)", 2 * PI / kk * 1e9, 141)
near("o8-x13a T", 2 * PI / (2 * PI * 1e15), 1e-15)
near("o8-x13a vp", 2 * PI * 1e15 / kk, 1.41e8)

# ---------------- o8-x08 ----------------
nu = PI * 1e15 / (2 * PI)
near("o8-x08 ν", nu, 5e14)
near("o8-x08 v=0.65c", 0.65 * C, 1.95e8)
near("o8-x08 λ (nm)", 0.65 * C / nu * 1e9, 390)
n = 1 / 0.65
near("o8-x08 n", n, 1.54)
near("o8-x08 Ee", 0.5 * 1.538 * EPS * C * 10**2, 0.204)

# ---------------- o8-x20 ----------------
k = 2 * PI / 2
near("o8-x20 k=π", k, PI)
near("o8-x20 ω=3π×10^8", k * C, 3 * PI * 1e8)
r0sq = 2**2 + 1**2 + 3**2
ok("o8-x20 r0²=14", r0sq == 14)
near("o8-x20 ε0c0A²=56", 2 * 2 * r0sq, 56)
A = math.sqrt(56 / (EPS2 * C))
near("o8-x20 A", A, 145.2, 1e-3)
near("o8-x20 A/c0", A / C, 4.84e-7)
# 方向：r̂×φ̂ = −θ̂，在 (2,1,3) 檢查直角座標式
p = np.array([2.0, 1.0, 3.0]); xx, yy, zz = p; r = np.linalg.norm(p); rho = math.hypot(xx, yy)
rhat = p / r
phi = np.array([-yy, xx, 0]) / rho
mth = np.array([-xx * zz, -yy * zz, rho**2]) / (r * rho)
vec("o8-x20 r̂×φ̂ = 書寫版 −θ̂", np.cross(rhat, phi), mth)
near("o8-x20 (2,1,3) 處 |S| 振幅 = 56/r²", EPS2 * C * (A / r) ** 2, 4)
near("o8-x20 (2,1,3) 處照度 = ½|S|", 0.5 * EPS2 * C * (A / r) ** 2, 2)

# ---------------- o8-x09 ----------------
E0 = math.sqrt(2 * 1e5 / (2 * EPS * C))
near("o8-x09 E0", E0, 6137, 1e-3)
near("o8-x09 B0", 2 * E0 / C, 4.09e-5)
near("o8-x09 k=4π/3×10^6", 2 * PI * 2 * 1e14 / C, 4.19e6)
for th in np.linspace(0, 2 * PI, 7):
    kh = np.array([math.cos(th), math.sin(th), 0]); eh = np.array([-math.sin(th), math.cos(th), 0])
    if not np.allclose(np.cross(kh, eh), [0, 0, 1]):
        FAIL.append("o8-x09 k̂×ê=ẑ")
ok("o8-x09 k̂×ê=ẑ（各 θ）", "o8-x09 k̂×ê=ẑ" not in FAIL)

# ---------------- o8-q11 ----------------
near("o8-q11 k=π×10^6", 2 * PI * 1.5 * 1e14 / C, PI * 1e6)
kh = np.array([math.cos(math.radians(-60)), math.sin(math.radians(-60)), 0])
eh = np.array([math.cos(math.radians(210)), math.sin(math.radians(210)), 0])
vec("o8-q11 k̂", kh, [0.5, -S3 / 2, 0])
vec("o8-q11 ê", eh, [-S3 / 2, -0.5, 0])
ok("o8-q11 k̂·ê=0", abs(kh @ eh) < 1e-12)

# ---------------- o8-4-15 ----------------
E0 = math.sqrt(2 * 1000 / (EPS * C))
near("o8-4-15 E0", E0, 868, 1e-3)
near("o8-4-15 B0", 868 / C, 2.89e-6)

# ---------------- o8-4-17 ----------------
Ee = 0.135 / 1e-4
near("o8-4-17 Ee", Ee, 1350)
E0 = math.sqrt(2 * Ee / (EPS * C))
near("o8-4-17 E0", E0, 1008, 1e-3)
near("o8-4-17 B0", 1008 / C, 3.36e-6)
near("o8-4-17 N", Ee * 7e-7 / (H * C), 4.75e21)
near("o8-4-17 k", 2 * PI / 7e-7, 8.98e6)
near("o8-4-17 ω", 2 * PI * C / 7e-7, 2.69e15)

# ---------------- o8-4-18 ----------------
Ee = 11 / (4 * PI * 100)
near("o8-4-18a Φ=0.05×220", 0.05 * 220, 11)
near("o8-4-18a Ee", Ee, 8.75e-3)
near("o8-4-18a E0", math.sqrt(2 * 8.75e-3 / (EPS * C)), 2.57)
near("o8-4-18b Ee", 2000 / 1e-10, 2e13)
E0 = math.sqrt(2 * 2e13 / (EPS * C))
near("o8-4-18b E0", E0, 1.23e8)
near("o8-4-18b E0（多一位）", E0, 1.227e8, 1e-3)
near("o8-4-18b B0", 1.227e8 / C, 0.409, 1e-3)

# ---------------- o8-q17 ----------------
near("o8-q17 k=2000π", 2 * PI / 1e-3, 2000 * PI)
near("o8-q17 v", C / 3, 1e8)
near("o8-q17 ν", (C / 3) / 1e-3, 1e11)
kh = np.array([-S3 / 2, -0.5, 0])
vec("o8-q17 k̂ (210°)", kh, [math.cos(math.radians(210)), math.sin(math.radians(210)), 0])
E0 = math.sqrt(2 * 60 / (3 * EPS2 * C))
near("o8-q17 E0", E0, 122.7, 1e-3)
near("o8-q17 B0", 3 * 122.7 / C, 1.227e-6, 1e-3)
vec("o8-q17 b̂=k̂×ẑ", np.cross(kh, [0, 0, 1]), [-0.5, S3 / 2, 0])
near("o8-q17 nε0cE0²", 3 * EPS2 * C * 122.7**2, 120)

# ---------------- o8-x14 ----------------
kh = np.array([-math.sin(math.radians(60)), math.cos(math.radians(60)), 0])
vec("o8-x14 k̂ (150°)", kh, [math.cos(math.radians(150)), math.sin(math.radians(150)), 0])
near("o8-x14 k=2π/3×10^7", 2 * PI * 2 * 5e14 / C, 2 * PI / 3 * 1e7)
near("o8-x14 ω", 2 * PI * 5e14, PI * 1e15)
E0 = math.sqrt(2 * 1e4 / (2 * EPS * C))
near("o8-x14 E0", E0, 1940, 1e-3)
near("o8-x14 B0", 2 * 1940 / C, 1.29e-5)
eh = np.cross([0, 0, 1], kh)
vec("o8-x14 ê=ẑ×k̂", eh, [-0.5, -S3 / 2, 0])
vec("o8-x14 ê 與圖（−y 往左 30°）一致", eh, [-math.sin(math.radians(30)), -math.cos(math.radians(30)), 0])
near("o8-x14 nε0cE0²", 2 * EPS * C * 1940**2, 2.0e4)

# ---------------- o8-x18 ----------------
eps18 = 1e-9 / (36 * PI)
near("o8-x18 ε0c0=1/120π", eps18 * C, 1 / (120 * PI), 1e-9)
ok("o8-x18 (1,2,2)·(2,-1,0)=0", np.dot([1, 2, 2], [2, -1, 0]) == 0)
near("o8-x18 k=3", np.linalg.norm([1, 2, 2]), 3)
near("o8-x18 ω=6×10^8", 3 * C / 1.5, 6e8)
E0 = math.sqrt(2 * 10 / (1.5 * eps18 * C))
near("o8-x18 E0=40√π", E0, 40 * math.sqrt(PI), 1e-9)
near("o8-x18 B0=2√π×10^-7", 1.5 * E0 / C, 2 * math.sqrt(PI) * 1e-7, 1e-9)
vec("o8-x18 k̂×ê", np.cross(unit([1, 2, 2]), unit([2, -1, 0])), np.array([2, 4, -5]) / (3 * math.sqrt(5)))
near("o8-x18 nε0cE0²=20", 1.5 * eps18 * C * E0**2, 20, 1e-9)

# ---------------- o8-x22 ----------------
near("o8-x22 v", C / 3, 1e8)
near("o8-x22 λ", 1e8 / 1e14, 1e-6)
near("o8-x22 k", 2 * PI / 1e-6, 2 * PI * 1e6)
kh = np.array([S3 / 2, 0.5, 0])
vec("o8-x22 ê=(−ẑ)×k̂", np.cross([0, 0, -1], kh), [0.5, -S3 / 2, 0])
near("o8-x22 B0=E0/v", 2 / 1e8, 2e-8)
near("o8-x22 nε0cE0²", 3 * EPS2 * C * 4, 0.0319, 2e-3)
near("o8-x22 Ee", 0.5 * 3 * EPS2 * C * 4, 0.0159, 3e-3)

# ---------------- o8-x25 ----------------
kh = np.array([-math.sin(math.radians(30)), -math.cos(math.radians(30)), 0])
vec("o8-x25 k̂ (240°)", kh, [math.cos(math.radians(240)), math.sin(math.radians(240)), 0])
near("o8-x25 k=10π/3×10^6", 2 * PI * 2.5 * 2e14 / C, 10 * PI / 3 * 1e6)
eh = np.cross([0, 0, 1], kh)
vec("o8-x25 ê=ẑ×k̂", eh, [S3 / 2, -0.5, 0])
near("o8-x25 B0", 2.5 * 5 / C, 4.17e-8)
near("o8-x25 nε0cE0²", 2.5 * EPS2 * C * 25, 0.166)
near("o8-x25 Ee", 0.5 * 2.5 * EPS2 * C * 25, 0.0830)

# ---------------- o8-4-23 ----------------
v = math.sqrt(3 * 8.314 * 1000 / 0.004)
near("o8-4-23 v_rms", v, 2497, 1e-3)
dl = 706.52 * 2497 / C
near("o8-4-23 Δλ (nm)", dl, 5.88e-3)
near("o8-4-23 2Δλ", 2 * 5.88e-3, 0.0118, 5e-3)

# ---------------- o8-x12 ----------------
import sympy as sp
xs, ts, Bs, Cs = sp.symbols("x t B C", positive=True)
ok("o8-x12 Bx²+BC²t²−2BCxt = B(x−Ct)²",
   sp.simplify(Bs * xs**2 + Bs * Cs**2 * ts**2 - 2 * Bs * Cs * xs * ts - Bs * (xs - Cs * ts) ** 2) == 0)

# ---------------- o8-x07 ----------------
near("o8-x07 T", 1 / 1e9, 1e-9)
near("o8-x07 λ", C / (1.5 * 1e9), 0.2)
near("o8-x07 k=10π", 2 * PI / 0.2, 10 * PI)
near("o8-x07 B0", 1.5 * 2 / C, 1e-8)
vec("o8-x07 b̂=k̂×ẑ", np.cross([S3 / 2, 0.5, 0], [0, 0, 1]), [0.5, -S3 / 2, 0])
near("o8-x07 Ee", 0.5 * 1.5 * EPS * C * 4, 7.97e-3)

# ---------------- o8-x17 ----------------
kh = np.array([S2, 1, S3]) / math.sqrt(6); eh = np.array([S2, 1, -S3]) / math.sqrt(6)
near("o8-x17 |k̂|", np.linalg.norm(kh), 1.0)
ok("o8-x17 k̂·ê=0", abs(kh @ eh) < 1e-12)
near("o8-x17 k=4π/3×10^4", 2 * PI * 2 * 1e12 / C, 4 * PI / 3 * 1e4)
E0 = math.sqrt(2 * 50 / (2 * EPS2 * C))
near("o8-x17 E0", E0, 137.2, 1e-3)
near("o8-x17 B0", 2 * 137.2 / C, 9.15e-7)
vec("o8-x17 6·(k̂×ê) 未約分", np.cross([S2, 1, S3], [S2, 1, -S3]), [-2 * S3, 2 * math.sqrt(6), 0])
vec("o8-x17 b̂", np.cross(kh, eh), [-S3 / 3, math.sqrt(6) / 3, 0])
near("o8-x17 nε0cE0²", 2 * EPS2 * C * 137.2**2, 100, 2e-3)

# ---------------- o8-x21 ----------------
kh = np.array([-S3 / 2, -0.5, 0]); eh = np.array([-0.5, S3 / 2, 0])
vec("o8-x21 k̂ (210°)", kh, [math.cos(math.radians(210)), math.sin(math.radians(210)), 0])
vec("o8-x21 ê (120°)", eh, [math.cos(math.radians(120)), math.sin(math.radians(120)), 0])
ok("o8-x21 k̂·ê=0", abs(kh @ eh) < 1e-12)
near("o8-x21 k=8000π/9", 2 * PI * (4 / 3) * 1e11 / C, 8000 * PI / 9)
near("o8-x21 B0", (4 / 3) * 20 / C, 8.89e-8)
vec("o8-x21 k̂×ê=−ẑ", np.cross(kh, eh), [0, 0, -1])
near("o8-x21 nε0cE0²", (4 / 3) * EPS2 * C * 400, 1.417, 1e-3)
near("o8-x21 Ee", 0.5 * (4 / 3) * EPS2 * C * 400, 0.708, 1e-3)

# ---------------- o8-q11c ----------------
Ee = 0.02 / (PI * 1e-6)
near("o8-q11c Ee", Ee, 6.37e3)
near("o8-q11c E0", math.sqrt(2 * 6.37e3 / (EPS * C)), 2.19e3)
near("o8-q11c B0", 2.19e3 / C, 7.30e-6)

# ---------------- o8-x13b ----------------
near("o8-x13b P=VI", 3 * 0.2, 0.6)
near("o8-x13b Φ", 0.02 * 0.6, 0.012)
near("o8-x13b N", 0.012 * 550e-9 / (H * C), 3.32e16)
near("o8-x13b Ee", 0.012 / 2.5e-3, 4.8)
near("o8-x13b E0", math.sqrt(2 * 4.8 / (EPS * C)), 60.1)
near("o8-x13b B0", 60.1 / C, 2.0e-7, 2e-3)

# ---------------- o8-q12 ----------------
kh = np.array([-S3 / 2, 0.5, 0]); eh = np.array([0.5, S3 / 2, 0])
ok("o8-q12 k̂·ê=0", abs(kh @ eh) < 1e-12)
near("o8-q12 k=4π/3×10^7", 2 * PI * 2 * 1e15 / C, 4 * PI / 3 * 1e7)
near("o8-q12 E0", math.sqrt(2e4 / (2 * EPS * C)), 1940, 1e-3)
near("o8-q12 B0", 2 * 1940 / C, 1.29e-5)
vec("o8-q12 k̂×ê=−ẑ", np.cross(kh, eh), [0, 0, -1])
near("o8-q12 nε0cE0²", 2 * EPS * C * 1940**2, 2.0e4)

# ---------------- o8-q13 ----------------
kh = np.array([0.5, -S3 / 2, 0]); eh = np.array([S3 / 2, 0.5, 0])
ok("o8-q13 k̂·ê=0", abs(kh @ eh) < 1e-12)
near("o8-q13 T", 1 / 2e9, 5e-10)
near("o8-q13 λ", C / (1.5 * 2e9), 0.1)
near("o8-q13 k=20π", 2 * PI / 0.1, 20 * PI)
near("o8-q13 B0", 1.5 * 3 / C, 1.5e-8)
vec("o8-q13 k̂×ê=+ẑ", np.cross(kh, eh), [0, 0, 1])
near("o8-q13 nε0cE0²", 1.5 * EPS2 * C * 9, 3.59e-2)
near("o8-q13 Ee", 0.5 * 1.5 * EPS2 * C * 9, 1.79e-2, 3e-3)

# ---------------- o8-q14 ----------------
near("o8-q14 k=π×10^6", 2 * PI * 1.5 * 1e14 / C, PI * 1e6)
E0 = math.sqrt(2e8 / (1.5 * EPS * C))
near("o8-q14 E0", E0, 2.24e5)
near("o8-q14 B0", 1.5 * 2.24e5 / C, 1.12e-3)
vec("o8-q14 (−ẑ)×x̂=−ŷ", np.cross([0, 0, -1], [1, 0, 0]), [0, -1, 0])
near("o8-q14 nε0cE0²", 1.5 * EPS * C * 2.24e5**2, 2.0e8, 3e-3)

print()
if FAIL:
    print(f"FAIL {len(FAIL)} 項：", FAIL)
    sys.exit(1)
print("ALL PASS")
