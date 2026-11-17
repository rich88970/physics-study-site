"""光學第九章（波的疊加）所有數值答案的獨立驗算。

相量疊加題：直接把原式在一個週期內取樣，用傅立葉投影求 E0cosα、E0sinα（不經過改寫規則），
和網站卡片上的答案比較；其餘題目用 numpy / sympy 重算。用法：python tools/verify_optics_ch09.py
"""
import math
import sys

import numpy as np
import sympy as sp

PI = math.pi
FAIL = []


def check(name, got, want, tol=5e-3):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print(f"{'OK ' if ok else 'BAD'} {name}: {got:.5g}（卡片 {want:.5g}）")
    if not ok:
        FAIL.append(name)


def fit(expr):
    """expr(wt) → (E0, alpha)，alpha ∈ (-π, π]，滿足 expr = E0 cos(alpha - wt)。"""
    t = np.linspace(0, 2 * PI, 4096, endpoint=False)
    y = expr(t)
    C = 2 * np.mean(y * np.cos(t))
    S = 2 * np.mean(y * np.sin(t))
    resid = np.max(np.abs(y - (C * np.cos(t) + S * np.sin(t))))
    assert resid < 1e-9, "不是單一同頻率弦波"
    return math.hypot(C, S), math.atan2(S, C)


s, c = np.sin, np.cos
# (名稱, 原式, 卡片 E0, 卡片相位, 相位範圍)
PHASOR = [
    ("5-2", lambda w: 2 * c(w) + 7 * c(PI / 4 - w), 8.53, 0.619, "pm"),
    ("Example 1", lambda w: 7 * c(PI / 3 - w) + 12 * s(PI / 4 - w) + 20 * c(PI / 5 - w), 29.67, 0.32, "pm"),
    ("2008 期中 3", lambda w: -4 * s(PI / 3 + w) - 3 * c(w + PI / 6) + 2 * s(w - PI / 4), 7.53, 3.020, "pm"),
    ("2011 期中 3", lambda w: -2 * c(w + PI / 3) + 4 * s(w - PI / 4) - 4 * s(PI / 6 + w), 5.93, 2.956, "pm"),
    ("2011 平時考 2", lambda w: -3 * s(PI / 4 + w) - 2 * c(w + PI / 3) + 4 * s(w - PI / 6), 5.97, 2.601, "pm"),
    ("2012 平時考 1", lambda w: -3 * c(w - PI / 6) - 2 * s(w + PI / 4) + 4 * s(w - PI / 3), 7.53, -3.020, "pm"),
    ("2013 平時考 1", lambda w: 2 * s(PI / 3 - w) - 3 * s(PI / 6 + w) - c(w - PI / 4), 4.33, -1.681, "pm"),
    ("2013 期中 1", lambda w: 2 * s(w - PI / 3) - c(w + PI / 4) - 3 * s(2 * PI / 3 + w), 5.97, 2.575, "pm"),
    ("2014 平時考 1", lambda w: 3 * s(PI / 6 + w) - 4 * s(PI / 4 - w) - 2 * c(PI / 3 + w), 7.53, 1.885, "pm"),
    ("2017 平時考 1", lambda w: 2 * s(PI / 6 - w) - 3 * s(PI / 3 + w) - c(PI / 4 + w), 3.42, -2.311, "pm"),
    ("2018 期中 1", lambda w: 3 * s(PI / 3 - w) - 2 * s(PI / 6 + w) - 4 * c(3 * PI / 4 + w), 4.44, 6.192, "02pi"),
    ("2007 期中 4（φ）", lambda w: 3 * c(w - PI / 4) - 2 * c(w + PI / 3) + 4 * s(-w + 3 * PI / 4), 7.76, 0.534, "phi"),
    ("2010 期中 4", lambda w: 2 * s(PI / 6 - w) - 3 * c(w + PI / 4) - s(w - PI / 3) + c(w - PI / 3), 0.79, 1.258, "pm"),
    ("2020 期中 1", lambda w: 2 * s(PI / 4 + w) + 3 * c(PI / 6 + w) - 4 * s(PI / 3 + w) - 2 * c(-PI / 3 + w), 3.84, -1.689, "pm"),
    ("2021 期中 1（度）", lambda w: 3 * s(PI / 3 + w) - 2 * c(PI / 4 + w) - 4 * s(PI / 6 - w) + 3 * c(-PI / 3 + w), 9.00, 85.6, "deg"),
    ("2022 期中 1", lambda w: -3 * c(PI / 6 + w) + 4 * s(2 * PI / 3 + w) + c(-PI / 4 + w) - 2 * s(PI / 3 - w), 1.22, 1.702, "pm"),
    ("2024 期中 1", lambda w: -2 * c(PI / 6 + w) - 3 * s(PI / 3 + w) + 4 * c(-PI / 3 + w) + s(-PI / 4 - w), 3.78, 2.503, "pm"),
    ("2025 期中 1", lambda w: 2 * c(5 * PI / 6 + w) + s(3 * PI / 4 + w) - 4 * c(PI / 3 + w) - 3 * s(4 * PI / 3 - w), 0.498, 2.600, "02pi"),
    ("變化題 1", lambda w: 2 * c(PI / 3 + w) - s(PI / 6 - w) + 3 * s(PI / 4 + w) - c(PI / 2 - w), 2.63, 0.097, "pm"),
    ("變化題 2（φ）", lambda w: 4 * c(w + PI / 6) - 3 * s(w - PI / 3), 7.0, 2 * PI / 3, "phi"),
]

print("== 相量疊加（取樣投影，獨立於改寫規則）==")
for name, f, E0, ph, rng in PHASOR:
    e0, al = fit(f)
    if rng == "02pi":
        al = al % (2 * PI)
    elif rng == "phi":
        al = (PI / 2 - al) % (2 * PI)
        # 直接驗 E0 sin(ωt+φ)
        t = np.linspace(0, 2 * PI, 64)
        assert np.max(np.abs(f(t) - e0 * np.sin(t + al))) < 1e-9
    elif rng == "deg":
        al = math.degrees(al)
    check(name + " E0", e0, E0, tol=6e-3 if E0 > 1 else 1e-2)
    check(name + " 相位", al, ph, tol=3e-3 if abs(ph) > 0.2 else 2e-2)

print("== 5-2 餘弦定律交叉核對 ==")
check("5-2 E0（式 9）", math.sqrt(4 + 49 + 28 * math.cos(PI / 4)), 8.53)

print("== 駐波 ==")
x, t = sp.symbols("x t", real=True)
e12 = 50 * sp.sin(4 * sp.pi * x + 5 * sp.pi * t) + 50 * sp.sin(5 * sp.pi * t - 4 * sp.pi * x)
assert sp.simplify(sp.expand_trig(e12 - 100 * sp.cos(4 * sp.pi * x) * sp.sin(5 * sp.pi * t))) == 0
check("2012 期中 λ", 2 * PI / (4 * PI), 0.5)
check("2012 期中 ν", 5 * PI / (2 * PI), 2.5)
lam = 20 / 5
k, w = 2 * PI / lam, 2 * PI * 5
check("2014 平時考 λ", lam, 4)
check("2014 平時考 k", k, PI / 2)
check("2014 平時考 ω", w, 10 * PI)
e14 = 10 * sp.cos(sp.pi / 2 * x - 10 * sp.pi * t) + 10 * sp.cos(sp.pi / 2 * x + 10 * sp.pi * t)
assert sp.simplify(sp.expand_trig(e14 - 20 * sp.cos(sp.pi / 2 * x) * sp.cos(10 * sp.pi * t))) == 0
nodes = [float(v) for v in sp.solve(sp.cos(sp.pi / 2 * x), x)]
assert all(abs(v % 2 - 1) < 1e-12 for v in nodes), nodes
print("OK  2014 平時考 節點", nodes, "（x=2n+1）")
e18 = 50 * sp.sin(sp.pi / 3 * x + 6 * sp.pi * t) + 50 * sp.sin(sp.pi / 3 * x - 6 * sp.pi * t)
assert sp.simplify(sp.expand_trig(e18 - 100 * sp.sin(sp.pi / 3 * x) * sp.cos(6 * sp.pi * t))) == 0
e_v5 = 30 * sp.cos(2 * sp.pi * x - 8 * sp.pi * t) - 30 * sp.cos(2 * sp.pi * x + 8 * sp.pi * t)
assert sp.simplify(sp.expand_trig(e_v5 - 60 * sp.sin(2 * sp.pi * x) * sp.sin(8 * sp.pi * t))) == 0
print("OK  2012/2014/2018/變化題 5 的積化和差（sympy 展開相等）")

print("== He-Ne Example 2 ==")
cc = 3e8
check("m", 2 * 0.3 / 632.8e-9, 948166, tol=1e-6)
check("Δν_gain", cc / 632.800e-9 - cc / 632.802e-9, 1.50e9)
check("c/2d", cc / 0.6, 5e8)

print("== 群速度 ==")
lam_s, g, T, rho = sp.symbols("lambda g T rho", positive=True)
for name, vp, want in [("長波長", sp.sqrt(g * lam_s / (2 * sp.pi)), sp.Rational(1, 2)),
                       ("短波長", sp.sqrt(2 * sp.pi * T / (lam_s * rho)), sp.Rational(3, 2)),
                       ("變化題 3", 1 / lam_s, 2)]:
    vg = vp - lam_s * sp.diff(vp, lam_s)
    r = sp.simplify(vg / vp)
    assert r == want, (name, r)
    print(f"OK  海浪/冪次 {name}: vg/vp = {r}")
# 5-8：精確式 vg = c/(n + ω n')，與起點式等價
om = sp.symbols("omega", positive=True)
cs = sp.symbols("c", positive=True)
nf = sp.Function("n")(om)
vp = cs / nf
lam_m = 2 * sp.pi * cs / (nf * om)
vg = vp - lam_m * sp.diff(vp, om) / sp.diff(lam_m, om)
assert sp.simplify(vg - cs / (nf + om * sp.diff(nf, om))) == 0
print("OK  5-8 v_g = c/(n+ω dn/dω)")
# 5-11：dk/dω 與 dK/dω
Kf = sp.Function("K")(om)
kk = sp.sqrt(Kf) * om / cs
assert sp.simplify(sp.diff(kk, om) - sp.sqrt(Kf) / cs * (1 + om / (2 * Kf) * sp.diff(Kf, om))) == 0
A, w0 = sp.symbols("A omega_0", positive=True)
Kx = 1 + A / (w0 ** 2 - om ** 2)
assert sp.simplify(sp.diff(Kx, om) - 2 * A * om / (w0 ** 2 - om ** 2) ** 2) == 0
print("OK  5-11 dk/dω 與 dK/dω")

# 5-9
dn = (1 / 30) * (1.50 - 1)
slope = dn / (4861 - 6563)
vg59 = cc / 1.5 * (1 + 5890 / 1.5 * slope)
check("5-9 dn/dλ (Å⁻¹)", slope, -9.79e-6)
check("5-9 v_g", vg59, 1.92e8)
check("5-9 c/v_g", cc / vg59, 1.56)
check("5-9 精確群折射率", 1.5 - 5890 * slope, 1.558)
# 5-10
n510 = 1.40 + 2.5e6 / 5000 ** 2
d510 = -2 * 2.5e6 / 5000 ** 3
vg510 = cc / n510 * (1 + 5000 / n510 * d510)
check("5-10 n", n510, 1.50)
check("5-10 dn/dλ", d510, -4.0e-5)
check("5-10 v_g", vg510, 1.73e8)
check("5-10 c/v_g", cc / vg510, 1.73)
check("5-10 精確群折射率", n510 - 5000 * d510, 1.70)
# Example 3
for lam_n, want in [(400, 1.5557), (500, 1.5448), (700, 1.5353)]:
    check(f"Ex3 n({lam_n})", 1.5255 + 4825 / lam_n ** 2, want, tol=1e-4)
vp3 = cc / (1.5255 + 4825 / 500 ** 2)
check("Ex3 v_p", vp3, 1.942e8)
check("Ex3 v_g", vp3 * (1 - 9650 / ((1.5255 + 4825 / 500 ** 2) * 500 ** 2)), 1.893e8)
# 變化題 4
n4 = 1.50 + 4000 / 400 ** 2
check("變化題 4 n", n4, 1.525)
check("變化題 4 v_p", cc / n4, 1.967e8)
check("變化題 4 v_g", cc / n4 * (1 + 400 / n4 * (-8000 / 400 ** 3)), 1.903e8)

print()
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("ALL CHECKS PASSED")
