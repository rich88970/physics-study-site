"""光學 ch08（講義第八章｜電磁波的表示）所有題目卡數值的獨立驗算。

用法：python tools/verify_optics_ch08.py   全部通過時結束碼 0。
慣例（和講義、下學期近代光學考卷的詳解相同）：
  E = E0 ê exp[i(k·r − ωt)]，B = (E0/v) b̂ exp[...]，b̂ = k̂ × ê，v = c0/n
  照度 Ee = ½ n ε0 c0 E0²，瞬時坡印廷向量振幅 ε0 c0² E0 B0（介質中 ε c² = ε0 c0²）
"""
import sys
import numpy as np

EPS = 8.8542e-12
EPS_OLD = 8.854e-12          # 早期考卷與課本解答用的值
C = 3e8
H = 6.626e-34
fails = []


def check(name, got, want, rtol=5e-3):
    ok = np.allclose(got, want, rtol=rtol, atol=0)
    print(f"{'OK ' if ok else 'BAD'} {name}: {np.round(got, 6) if np.ndim(got) else f'{got:.6g}'}  (expected {want})")
    if not ok:
        fails.append(name)


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def ang(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def plane(name, n, f, E0, khat, ehat, eps=EPS, want=None):
    """回傳並檢查 k、ω、B0、b̂、S 振幅、照度。want: dict 期望值。"""
    khat, ehat = unit(khat), unit(ehat)
    assert abs(khat @ ehat) < 1e-12, name + " E 不垂直 k"
    k = 2 * np.pi * n * f / C
    w = 2 * np.pi * f
    B0 = n * E0 / C
    bhat = np.cross(khat, ehat)
    S0 = eps * C**2 * E0 * B0
    I = 0.5 * n * eps * C * E0**2
    # 坡印廷方向必須是 k̂
    assert np.allclose(np.cross(ehat, bhat), khat), name + " E×B 不沿 k"
    out = dict(k=k, w=w, B0=B0, bhat=bhat, S0=S0, I=I, lam=C / (n * f))
    for key, val in (want or {}).items():
        check(f"{name} {key}", out[key], val)
    return out


def E0_from_I(n, I, eps=EPS):
    return np.sqrt(2 * I / (n * eps * C))


# ---------- 講義 Example（課本 Example 1–3） ----------
check("Ex1 λ", 2 * np.pi / (3 * np.pi), 2 / 3)
check("Ex1 ν", 10 * np.pi / (2 * np.pi), 5)
check("Ex1 v", 10 * np.pi / (3 * np.pi), 3.333)
check("Ex1 y(0.1,0)", 0.35 * np.sin(3 * np.pi * 0.1 + np.pi / 4), 0.3457)
Ee = 6000 / (np.pi * 1e-3**2)
check("Ex2 Ee", Ee, 1.91e9)
check("Ex2 E0", np.sqrt(2 * Ee / (EPS * C)), 1.20e6)
check("Ex2 B0", np.sqrt(2 * Ee / (EPS * C)) / C, 4.00e-3)
r = 525 / 513
check("Ex3 v/c（近似）", 1 - r, -0.02339)
check("Ex3 v（近似, km/s）", (1 - r) * C / 1e3, -7018)
beta = (1 - r**2) / (1 + r**2)
check("Ex3 v/c（相對論精確式）", beta, -0.02311)

# ---------- 作業 ----------
# 4-4：指數 x²−20xt+100t² = (x−10t)²
x, t = 3.7, 0.21
check("4-4 指數配方", x**2 - 20 * x * t + 100 * t**2, (x - 10 * t) ** 2)
# 4-7
check("4-7 λ (cm)", 2 * np.pi / 628.3, 0.0100)
check("4-7 ν (Hz)", 6283 / (2 * np.pi), 1000)
check("4-7 T (s)", 2 * np.pi / 6283, 1e-3)
check("4-7 v (cm/s)", 6283 / 628.3, 10)
# 4-15
E0 = E0_from_I(1, 1000, EPS_OLD)
check("4-15 E0", E0, 867.7)
check("4-15 B0", E0 / C, 2.892e-6)
# 4-17
I = 0.135 * 1e4
E0 = E0_from_I(1, I, EPS_OLD)
check("4-17 Ee (W/m²)", I, 1350)
check("4-17 E0", E0, 1008.2)
check("4-17 B0", E0 / C, 3.361e-6)
check("4-17 光子通量", I * 700e-9 / (H * C), 4.754e21)
check("4-17 1/λ", 1 / 700e-9, 1.4286e6)
check("4-17 k", 2 * np.pi / 700e-9, 8.976e6)
check("4-17 ν", C / 700e-9, 4.2857e14)
check("4-17 ω", 2 * np.pi * C / 700e-9, 2.693e15)
# 4-18
I = 0.05 * 220 / (4 * np.pi * 10**2)
check("4-18a Ee", I, 8.754e-3)
check("4-18a E0", E0_from_I(1, I, EPS_OLD), 2.567)
I = 2000 / (1e-6 * 1e-4)
check("4-18b Ee", I, 2e13)
check("4-18b E0", E0_from_I(1, I, EPS_OLD), 1.2272e8)
check("4-18b B0", E0_from_I(1, I, EPS_OLD) / C, 0.4091)
# 4-23
v = np.sqrt(3 * 8.314 * 1000 / 0.004)
check("4-23 v_rms", v, 2497)
check("4-23 Δλ (nm)", 706.52 * v / C, 0.00588)
check("4-23 2Δλ (nm)", 2 * 706.52 * v / C, 0.01176)

# ---------- 考古題（下學期近代光學） ----------
# 2007-04-24 期中 Q1：n=1.5, f=1 GHz, E∥ẑ, E0=2, k̂ 在 +x 上方 30°
o = plane("2007", 1.5, 1e9, 2, ang(30), [0, 0, 1], EPS_OLD,
          dict(lam=0.2, k=10 * np.pi, B0=1e-8, bhat=[0.5, -np.sqrt(3) / 2, 0], I=7.969e-3))
check("2007 T", 1 / 1e9, 1e-9)

# 2008-05-05 期中 Q2：E = ẑ 10 cos[π·10^15 (t − x/(0.65 c0))]
w = np.pi * 1e15
check("2008 f", w / (2 * np.pi), 5e14)
check("2008 λ (nm)", 0.65 * C / 5e14 * 1e9, 390)
check("2008 n", 1 / 0.65, 1.538)
check("2008 <S>", 0.5 * (1 / 0.65) * EPS_OLD * C * 10**2, 0.2043)

# 2009-04-27 期中 Q2：n=2, f=1e14, Ee=1e5, k̂ 與 +x 夾 θ, Ê ⟂ k̂（逆時針轉 90°）
E0 = E0_from_I(2, 1e5, EPS_OLD)
check("2009 E0", E0, 6137)
check("2009 B0", 2 * E0 / C, 4.091e-5)
check("2009 k", 2 * np.pi * 2 * 1e14 / C, 4.189e6)
th = np.radians(37)  # 任一 θ：b̂ 都是 +ẑ
check("2009 b̂（任意 θ）", np.cross([np.cos(th), np.sin(th), 0], [-np.sin(th), np.cos(th), 0]), [0, 0, 1])

# 2011-04-06 平時考 Q1：n=1.5, E0=200, f=1e14, k̂ 在 −60°, Ê 在 210°
o = plane("2011q", 1.5, 1e14, 200, ang(-60), ang(210), EPS_OLD, dict(k=np.pi * 1e6))

# 2011-04-06 平時考 Q3：20 mW He-Ne、半徑 1 mm
I = 0.02 / (np.pi * 1e-3**2)
check("2011q3 Ee", I, 6.366e3)
check("2011q3 E0", E0_from_I(1, I, EPS_OLD), 2.190e3)
check("2011q3 B0", E0_from_I(1, I, EPS_OLD) / C, 7.30e-6)

# 2012-04-11 平時考 Q2：n=2, Ee=1e4, f=1e15, k̂ 150°, Ê 60°
E0 = E0_from_I(2, 1e4, EPS_OLD)
check("2012q E0", E0, 1940.3)
o = plane("2012q", 2, 1e15, E0, ang(150), ang(60), EPS_OLD,
          dict(k=4 * np.pi / 3 * 1e7, B0=1.2935e-5, bhat=[0, 0, -1], S0=2e4, I=1e4))

# 2012-05-02 期中 Q2：A exp(Bx²+BC²t²−2BCxt) = A exp[B(x−Ct)²]
Bc, Cc = 0.7, 2.3
check("2012m 配方", Bc * x**2 + Bc * Cc**2 * t**2 - 2 * Bc * Cc * x * t, Bc * (x - Cc * t) ** 2)

# 2013-04-10 平時考 Q2：n=1.5, B∥+ẑ, E0=3, f=2 GHz, k̂ −60°, Ê 30°
o = plane("2013q", 1.5, 2e9, 3, ang(-60), ang(30), EPS,
          dict(lam=0.1, k=20 * np.pi, B0=1.5e-8, bhat=[0, 0, 1], S0=0.03586, I=0.01793))
check("2013q T", 1 / 2e9, 5e-10)

# 2013-04-24 期中 Q2：E = (6î − 2√3ĵ) exp{i[(√2/2 x + √6/2 y)π·10^7 + 2π·10^15 t]} kV/m
a = np.array([np.sqrt(2) / 2, np.sqrt(6) / 2, 0]) * np.pi * 1e7
kvec = -a                       # 寫成 exp[i(k·r − ωt)] 時 k = −a
check("2013m |E| (kV/m)", np.hypot(6, 2 * np.sqrt(3)), 6.928)
check("2013m E⟂k（|cos| ≈ 0，加 1 比較）", 1 + abs(np.dot(unit([6, -2 * np.sqrt(3), 0]), unit(kvec))), 1)
check("2013m |k|", np.linalg.norm(kvec), np.sqrt(2) * np.pi * 1e7)
check("2013m k̂", unit(kvec), [-0.5, -np.sqrt(3) / 2, 0])
check("2013m λ (m)", 2 * np.pi / np.linalg.norm(kvec), 1.4142e-7)
check("2013m T", 2 * np.pi / (2 * np.pi * 1e15), 1e-15)
check("2013m v_p", 2 * np.pi * 1e15 / np.linalg.norm(kvec), 1.4142e8)

# 2013-04-24 期中 Q3：手電筒
P = 0.02 * 3 * 0.2
check("2013m3 光功率", P, 0.012)
check("2013m3 光子/秒", P * 550e-9 / (H * C), 3.32e16)
I = P / 25e-4
check("2013m3 Ee", I, 4.8)
check("2013m3 E0", E0_from_I(1, I, EPS_OLD), 60.13)
check("2013m3 B0", E0_from_I(1, I, EPS_OLD) / C, 2.004e-7)
check("2013m3 E_rms", E0_from_I(1, I, EPS_OLD) / np.sqrt(2), 42.52)

# 2014-04-09 平時考 Q4：−ẑ 傳播, f=1e14, Ê=+x̂, n=3/2, Ee=1e8
E0 = E0_from_I(1.5, 1e8, EPS_OLD)
check("2014q E0", E0, 2.2405e5)
o = plane("2014q", 1.5, 1e14, E0, [0, 0, -1], [1, 0, 0], EPS_OLD,
          dict(k=np.pi * 1e6, B0=1.1202e-3, bhat=[0, -1, 0], S0=2e8))

# 2014-04-23 期中 Q1：f=5e14, B∥+ẑ, n=2, Ee=1e4, k̂ 150°, Ê 240°
E0 = E0_from_I(2, 1e4, EPS_OLD)
o = plane("2014m", 2, 5e14, E0, ang(150), ang(240), EPS_OLD,
          dict(k=2 * np.pi / 3 * 1e7, B0=1.2935e-5, bhat=[0, 0, 1], S0=2e4))

# 2017-04-12 平時考 Q2：k̂ 210°, n=3, Ê=+ẑ, λ_介質=1 mm, Ee=60
E0 = E0_from_I(3, 60)
check("2017q E0", E0, 122.71)
f = (C / 3) / 1e-3
check("2017q f", f, 1e11)
o = plane("2017q", 3, f, E0, ang(210), [0, 0, 1], EPS,
          dict(k=2000 * np.pi, B0=1.2271e-6, bhat=[-0.5, np.sqrt(3) / 2, 0], S0=120))

# 2017-04-26 期中 Q1：k̂=(√2,1,√3)/√6, Ê=(√2,1,−√3)/√6, f=1e12, n=2, Ee=50
E0 = E0_from_I(2, 50)
check("2017m E0", E0, 137.20)
o = plane("2017m", 2, 1e12, E0, [np.sqrt(2), 1, np.sqrt(3)], [np.sqrt(2), 1, -np.sqrt(3)], EPS,
          dict(k=4 * np.pi / 3 * 1e4, B0=9.1467e-7, bhat=[-1 / np.sqrt(3), np.sqrt(2) / np.sqrt(3), 0], S0=100))

# 2018-04-25 期中 Q2：k=(1,2,2) m⁻¹, n=1.5, Ê∥(2,−1,0), Ee=10, ε0=1/(36π)×10⁻⁹
e18 = 1e-9 / (36 * np.pi)
check("2018 c0 由 ε0、μ0", 1 / np.sqrt(e18 * 4e-7 * np.pi), 3e8)
E0 = E0_from_I(1.5, 10, e18)
check("2018 E0 = 40√π", E0, 40 * np.sqrt(np.pi))
check("2018 ω", 3 * C / 1.5, 6e8)
khat, ehat = unit([1, 2, 2]), unit([2, -1, 0])
check("2018 b̂", np.cross(khat, ehat), np.array([2, 4, -5]) / (3 * np.sqrt(5)))
B0 = 1.5 * E0 / C
check("2018 B0 = 2√π×10⁻⁷", B0, 2 * np.sqrt(np.pi) * 1e-7)
check("2018 S0", e18 * C**2 * E0 * B0, 20)

# 2020-04-21 期中 Q2：球面波，λ=2 m，Ê=φ̂，(2,1,3) 處 Ee=2
r0sq = 4 + 1 + 9
A2 = 2 * 2 * r0sq / (EPS * C)
check("2020 ε0c0A²", EPS * C * A2, 56)
check("2020 A", np.sqrt(A2), 145.2)
check("2020 A/c", np.sqrt(A2) / C, 4.840e-7)
check("2020 ω", np.pi * C, 3 * np.pi * 1e8)
p = np.array([2.0, 1.0, 3.0]); rr = np.linalg.norm(p); rho = np.hypot(p[0], p[1])
phi_hat = np.array([-p[1], p[0], 0]) / rho
b_hat = np.array([-p[0] * p[2], -p[1] * p[2], rho**2]) / (rr * rho)
check("2020 φ̂×b̂ = r̂", np.cross(phi_hat, b_hat), p / rr)
check("2020 |S| 振幅於 (2,1,3)", 56 / rr**2, 4)

# 2021-04-27 期中 Q2：k̂ 210°, n=4/3, E0=20, Ê 120°, f=100 GHz
o = plane("2021", 4 / 3, 1e11, 20, ang(210), ang(120), EPS,
          dict(k=8000 * np.pi / 9, B0=8.889e-8, bhat=[0, 0, -1], S0=1.4167, I=0.70833))

# 2022-04-27 期中 Q2：n=3, k̂ 30°, B∥−ẑ, E0=2, f=1e14 → Ê = (½, −√3/2)
o = plane("2022", 3, 1e14, 2, ang(30), ang(-60), EPS,
          dict(k=2 * np.pi * 1e6, B0=2e-8, bhat=[0, 0, -1], S0=0.031875, I=0.0159375))

# 2024-04-23 期中 Q2：n=1.5, k̂=(0, ½, −√3/2), B0=2e-6 沿 −x̂, f=5e13
B0 = 2e-6; E0 = (C / 1.5) * B0
check("2024 E0", E0, 400)
o = plane("2024", 1.5, 5e13, E0, [0, 0.5, -np.sqrt(3) / 2], [0, -np.sqrt(3) / 2, -0.5], EPS,
          dict(k=5 * np.pi * 1e5, w=np.pi * 1e14, B0=2e-6, bhat=[-1, 0, 0], S0=637.5, I=318.75))

# 2025-04-22 期中 Q2：n=2.5, k̂ 240°, Ê 330°, B∥+ẑ, E0=5, f=2e14
o = plane("2025", 2.5, 2e14, 5, ang(240), ang(330), EPS,
          dict(k=10 * np.pi / 3 * 1e6, w=4 * np.pi * 1e14, B0=4.1667e-8, bhat=[0, 0, 1], S0=0.16602, I=0.083008))

# ---------- 考前衝刺變化題 ----------
o = plane("變化1", 2, 3e14, 6, ang(120), [np.sqrt(3) / 2, 0.5, 0], EPS,
          dict(k=4 * np.pi * 1e6, w=6 * np.pi * 1e14, B0=4e-8, bhat=[0, 0, -1], S0=0.19125, I=0.095625))
check("變化2 E0", E0_from_I(1.5, 300), 388.06)
check("變化2 B0", 1.5 * E0_from_I(1.5, 300) / C, 1.9403e-6)
I = 100 / (4 * np.pi * 2**2)
check("變化3 Ee", I, 1.989)
check("變化3 E0", E0_from_I(1, I), 38.70)
check("變化3 A", 2 * E0_from_I(1, I), 77.40)
r = 700 / 656.3
check("變化4 β（精確）", (1 - r**2) / (1 + r**2), -0.06438)
check("變化4 β（近似）", 1 - r, -0.06659)

print()
print("ALL PASS" if not fails else f"FAILED: {fails}")
sys.exit(1 if fails else 0)
