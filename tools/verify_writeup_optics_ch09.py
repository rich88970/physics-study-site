"""光學第九章「考試書寫版」（exam.html）改寫後出現的中間數值驗算。

相量疊加題：每一項的改寫鏈（sin→cos、cos 偶函數、負係數加減 π）逐段在多個 ωt 取樣比對，
再算分量和、E0、tan α、tan⁻¹ 值與象限調整，和卡片答案（sections/*.html）比較。
其餘題目（5-2、5-8～5-11、駐波、海浪）重算書寫版上出現的每一個數字。
DATA 也給 scratchpad 的產生器用來排版，所以排版與驗算用同一份資料。

用法：python tools/verify_writeup_optics_ch09.py   全部通過時結束碼 0。
"""
import math
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp

PI = math.pi
FAIL = []
WT = np.linspace(-3.0, 9.0, 97)


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        FAIL.append(name)


def near(name, got, want, tol):
    ok(f"{name}: {got:.6g}（書寫版 {want}）", abs(got - want) <= tol)


# 每一項：(係數, 函數, P, q, 括號原文)；括號 = P·π + q·ωt
DATA = {
    "o9-2018m1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="2\\pi>\\alpha\\ge0", mode="02pi",
                      terms=[(3, "sin", F(1, 3), -1, "\\tfrac{\\pi}{3}-\\omega t"),
                             (-2, "sin", F(1, 6), 1, "\\tfrac{\\pi}{6}+\\omega t"),
                             (-4, "cos", F(3, 4), 1, "\\tfrac{3}{4}\\pi+\\omega t")],
                      want=(4.427, -0.404, "4.44", "6.192", "354.8")),
    "o9-2020m1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(2, "sin", F(1, 4), 1, "\\tfrac{\\pi}{4}+\\omega t"),
                             (3, "cos", F(1, 6), 1, "\\tfrac{\\pi}{6}+\\omega t"),
                             (-4, "sin", F(1, 3), 1, "\\tfrac{\\pi}{3}+\\omega t"),
                             (-2, "cos", F(-1, 3), 1, "-\\tfrac{\\pi}{3}+\\omega t")],
                      want=(-0.452, -3.818, "3.84", "-1.689", "-96.7")),
    "o9-2022m1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(-3, "cos", F(1, 6), 1, "\\tfrac{\\pi}{6}+\\omega t"),
                             (4, "sin", F(2, 3), 1, "\\tfrac{2\\pi}{3}+\\omega t"),
                             (1, "cos", F(-1, 4), 1, "-\\tfrac{\\pi}{4}+\\omega t"),
                             (-2, "sin", F(1, 3), -1, "\\tfrac{\\pi}{3}-\\omega t")],
                      want=(-0.159, 1.207, "1.22", "1.702", "97.5")),
    "o9-2024m1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(-2, "cos", F(1, 6), 1, "\\tfrac{\\pi}{6}+\\omega t"),
                             (-3, "sin", F(1, 3), 1, "\\tfrac{\\pi}{3}+\\omega t"),
                             (4, "cos", F(-1, 3), 1, "-\\tfrac{\\pi}{3}+\\omega t"),
                             (1, "sin", F(-1, 4), -1, "-\\tfrac{\\pi}{4}-\\omega t")],
                      want=(-3.037, 2.257, "3.78", "2.503", "143.4")),
    "o9-2025m1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="2\\pi>\\alpha\\ge0", mode="02pi",
                      terms=[(2, "cos", F(5, 6), 1, "\\tfrac{5\\pi}{6}+\\omega t"),
                             (1, "sin", F(3, 4), 1, "\\tfrac{3\\pi}{4}+\\omega t"),
                             (-4, "cos", F(1, 3), 1, "\\tfrac{\\pi}{3}+\\omega t"),
                             (-3, "sin", F(4, 3), -1, "\\tfrac{4\\pi}{3}-\\omega t")],
                      want=(-0.427, 0.257, "0.50", "2.600", "149.0")),
    "o9-2008m3": dict(lhs="E_0\\cos(\\alpha-\\omega t)", e0c="E_0>0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(-4, "sin", F(1, 3), 1, "\\tfrac{\\pi}{3}+\\omega t"),
                             (-3, "cos", F(1, 6), 1, "\\omega t+\\tfrac{\\pi}{6}"),
                             (2, "sin", F(-1, 4), 1, "\\omega t-\\tfrac{\\pi}{4}")],
                      want=(-7.476, 0.914, "7.53", "3.020", "173.0")),
    "o9-2011m3": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0>0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(-2, "cos", F(1, 3), 1, "\\omega t+\\tfrac{\\pi}{3}"),
                             (4, "sin", F(-1, 4), 1, "\\omega t-\\tfrac{\\pi}{4}"),
                             (-4, "sin", F(1, 6), 1, "\\tfrac{\\pi}{6}+\\omega t")],
                      want=(-5.828, 1.096, "5.93", "2.956", "169.3")),
    "o9-2011q2": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(-3, "sin", F(1, 4), 1, "\\tfrac{\\pi}{4}+\\omega t"),
                             (-2, "cos", F(1, 3), 1, "\\omega t+\\tfrac{\\pi}{3}"),
                             (4, "sin", F(-1, 6), 1, "\\omega t-\\tfrac{\\pi}{6}")],
                      want=(-5.121, 3.075, "5.97", "2.601", "149.0")),
    "o9-2012q1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(-3, "cos", F(-1, 6), 1, "\\omega t-\\tfrac{\\pi}{6}"),
                             (-2, "sin", F(1, 4), 1, "\\omega t+\\tfrac{\\pi}{4}"),
                             (4, "sin", F(-1, 3), 1, "\\omega t-\\tfrac{\\pi}{3}")],
                      want=(-7.476, -0.914, "7.53", "-3.020", "-173.0")),
    "o9-2013q1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(2, "sin", F(1, 3), -1, "\\tfrac{\\pi}{3}-\\omega t"),
                             (-3, "sin", F(1, 6), 1, "\\tfrac{\\pi}{6}+\\omega t"),
                             (-1, "cos", F(-1, 4), 1, "\\omega t-\\tfrac{\\pi}{4}")],
                      want=(-0.475, -4.305, "4.33", "-1.681", "-96.3")),
    "o9-2013m1": dict(lhs="E_0\\cos(\\alpha-\\omega t)", e0c="E_0>0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(2, "sin", F(-1, 3), 1, "\\omega t-\\tfrac{\\pi}{3}"),
                             (-1, "cos", F(1, 4), 1, "\\omega t+\\tfrac{\\pi}{4}"),
                             (-3, "sin", F(2, 3), 1, "\\tfrac{2}{3}\\pi+\\omega t")],
                      want=(-5.037, 3.207, "5.97", "2.575", "147.5")),
    "o9-2014q1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="\\pi\\ge\\alpha\\ge-\\pi", mode="pm",
                      terms=[(3, "sin", F(1, 6), 1, "\\tfrac{\\pi}{6}+\\omega t"),
                             (-4, "sin", F(1, 4), -1, "\\tfrac{\\pi}{4}-\\omega t"),
                             (-2, "cos", F(1, 3), 1, "\\tfrac{\\pi}{3}+\\omega t")],
                      want=(-2.328, 7.159, "7.53", "1.885", "108.0")),
    "o9-2017q1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="\\pi\\ge\\alpha>-\\pi", mode="pm",
                      terms=[(2, "sin", F(1, 6), -1, "\\tfrac{\\pi}{6}-\\omega t"),
                             (-3, "sin", F(1, 3), 1, "\\tfrac{\\pi}{3}+\\omega t"),
                             (-1, "cos", F(1, 4), 1, "\\tfrac{\\pi}{4}+\\omega t")],
                      want=(-2.305, -2.525, "3.42", "-2.311", "-132.4")),
    "o9-2007m4": dict(lhs="E=E_0\\sin(\\omega t+\\phi)", e0c="E_0\\ge0", rng="0\\le\\phi\\lt2\\pi", mode="sinphi",
                      terms=[(3, "cos", F(-1, 4), 1, "\\omega t-\\tfrac{\\pi}{4}"),
                             (-2, "cos", F(1, 3), 1, "\\omega t+\\tfrac{\\pi}{3}"),
                             (4, "sin", F(3, 4), -1, "-\\omega t+\\tfrac{3}{4}\\pi")],
                      want=(3.950, 6.682, "7.76", "1.037", "59.4", "0.534", "30.6")),
    "o9-2010m4": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="-\\pi\\lt\\alpha\\le\\pi", mode="pm",
                      terms=[(2, "sin", F(1, 6), -1, "\\tfrac{\\pi}{6}-\\omega t"),
                             (-3, "cos", F(1, 4), 1, "\\omega t+\\tfrac{\\pi}{4}"),
                             (-1, "sin", F(-1, 3), 1, "\\omega t-\\tfrac{\\pi}{3}"),
                             (1, "cos", F(-1, 3), 1, "\\omega t-\\tfrac{\\pi}{3}")],
                      want=(0.245, 0.755, "0.79", "1.257", "72.0")),
    "o9-2021m1": dict(lhs="E=E_0\\cos(\\alpha-\\omega t)", e0c="E_0\\ge0", rng="180^\\circ\\ge\\alpha>-180^\\circ", mode="deg",
                      terms=[(3, "sin", F(1, 3), 1, "\\tfrac{\\pi}{3}+\\omega t"),
                             (-2, "cos", F(1, 4), 1, "\\tfrac{\\pi}{4}+\\omega t"),
                             (-4, "sin", F(1, 6), -1, "\\tfrac{\\pi}{6}-\\omega t"),
                             (3, "cos", F(-1, 3), 1, "-\\tfrac{\\pi}{3}+\\omega t")],
                      want=(0.684, 8.976, "9.00", "1.495", "85.6")),
}

# 卡片（sections）上的 A_i、α_i（單位 π），用來確認改寫鏈的結果和詳解一致
CARD_ALPHA = {
    "o9-2018m1": [(3, F(-1, 6)), (2, F(-2, 3)), (4, F(1, 4))],
    "o9-2020m1": [(2, F(1, 4)), (3, F(-1, 6)), (4, F(-5, 6)), (2, F(-2, 3))],
    "o9-2022m1": [(3, F(5, 6)), (4, F(-1, 6)), (1, F(1, 4)), (2, F(5, 6))],
    "o9-2024m1": [(2, F(5, 6)), (3, F(-5, 6)), (4, F(1, 3)), (1, F(-3, 4))],
    "o9-2025m1": [(2, F(-5, 6)), (1, F(-1, 4)), (4, F(2, 3)), (3, F(-1, 6))],
    "o9-2008m3": [(4, F(-5, 6)), (3, F(5, 6)), (2, F(3, 4))],
    "o9-2011m3": [(2, F(2, 3)), (4, F(3, 4)), (4, F(-2, 3))],
    "o9-2011q2": [(3, F(-3, 4)), (2, F(2, 3)), (4, F(2, 3))],
    "o9-2012q1": [(3, F(-5, 6)), (2, F(-3, 4)), (4, F(5, 6))],
    "o9-2013q1": [(2, F(-1, 6)), (3, F(-2, 3)), (1, F(-3, 4))],
    "o9-2013m1": [(2, F(5, 6)), (1, F(3, 4)), (3, F(5, 6))],
    "o9-2014q1": [(3, F(1, 3)), (4, F(3, 4)), (2, F(2, 3))],
    "o9-2017q1": [(2, F(-1, 3)), (3, F(-5, 6)), (1, F(3, 4))],
    "o9-2007m4": [(3, F(1, 4)), (2, F(2, 3)), (4, F(1, 4))],
    "o9-2010m4": [(2, F(-1, 3)), (3, F(3, 4)), (1, F(-1, 6)), (1, F(1, 3))],
    "o9-2021m1": [(3, F(1, 6)), (2, F(3, 4)), (4, F(2, 3)), (3, F(1, 3))],
}


def chain(c, fn, P, q):
    """改寫鏈：回傳 (beta1, rule, A, alpha)。beta1 是改成 cos(beta1 - ωt) 後的角（單位 π），
    alpha 是係數變正之後的角（單位 π，落在 (-1, 1]）。"""
    if fn == "cos":
        beta = P if q == -1 else -P
        rule = "none" if q == -1 else "even"
    else:
        beta = P - F(1, 2) if q == -1 else F(1, 2) - P
        rule = "sin-" if q == -1 else "sin+"
    beta1 = beta
    if c < 0:
        alpha = beta + 1 if beta <= 0 else beta - 1
    else:
        alpha = beta
    return beta1, rule, abs(c), alpha


def term_value(c, fn, P, q, w):
    arg = P * PI + q * w
    return c * (np.sin(arg) if fn == "sin" else np.cos(arg))


def solve(pid):
    d = DATA[pid]
    rows = []
    for (c, fn, P, q, _) in d["terms"]:
        beta1, rule, A, al = chain(c, fn, P, q)
        orig = term_value(c, fn, float(P), q, WT)
        mid = c * np.cos(float(beta1) * PI - WT)
        fin = A * np.cos(float(al) * PI - WT)
        rows.append(dict(c=c, fn=fn, P=P, q=q, beta1=beta1, rule=rule, A=A, al=al,
                         ok_mid=np.allclose(orig, mid), ok_fin=np.allclose(orig, fin),
                         x=A * math.cos(float(al) * PI), y=A * math.sin(float(al) * PI)))
    X = sum(r["x"] for r in rows)
    Y = sum(r["y"] for r in rows)
    E0 = math.hypot(X, Y)
    t = Y / X
    at = math.atan(t)
    if X > 0 and Y >= 0:
        quad, shift = 1, 0.0
    elif X < 0 and Y >= 0:
        quad, shift = 2, PI
    elif X < 0 and Y < 0:
        quad, shift = 3, -PI
    else:
        quad, shift = 4, 0.0
    alpha = at + shift
    if d["mode"] == "02pi" and alpha < 0:
        alpha += 2 * PI
    return rows, X, Y, E0, t, at, quad, shift, alpha


def main():
    for pid, d in DATA.items():
        rows, X, Y, E0, t, at, quad, shift, alpha = solve(pid)
        for i, r in enumerate(rows, 1):
            ok(f"{pid} 第 {i} 項改寫鏈（中間式、最後式）", r["ok_mid"] and r["ok_fin"])
            ok(f"{pid} 第 {i} 項 A、α 與卡片一致", (r["A"], r["al"]) == CARD_ALPHA[pid][i - 1])
        # 原式直接投影（不經改寫規則）
        y = sum(term_value(c, fn, float(P), q, WT) for (c, fn, P, q, _) in d["terms"])
        ok(f"{pid} 合成式 E0cos(α-ωt) 與原式相等", np.allclose(y, E0 * np.cos(alpha - WT)))
        w = d["want"]
        near(f"{pid} E0cosα", X, w[0], 6e-4)
        near(f"{pid} E0sinα", Y, w[1], 6e-4)
        ok(f"{pid} E0 = {E0:.4f} → {w[2]}", f"{E0:.2f}" == w[2])
        if d["mode"] == "sinphi":
            ok(f"{pid} α = {alpha:.4f} → {w[3]}", f"{alpha:.3f}" == w[3])
            ok(f"{pid} α° → {w[4]}", f"{math.degrees(alpha):.1f}" == w[4])
            phi = PI / 2 - alpha
            ok(f"{pid} φ = π/2-α = {phi:.4f} → {w[5]}", f"{phi:.3f}" == w[5] and 0 <= phi < 2 * PI)
            ok(f"{pid} φ° → {w[6]}", f"{math.degrees(phi):.1f}" == w[6])
            phi_t = np.allclose(y, E0 * np.sin(WT + phi))
            ok(f"{pid} E0 sin(ωt+φ) 與原式相等", phi_t)
        else:
            ok(f"{pid} α = {alpha:.4f} → {w[3]}", f"{alpha:.3f}" == w[3])
            ok(f"{pid} α° → {w[4]}", f"{math.degrees(alpha):.1f}" == w[4])
        # 書寫版顯示的 tan⁻¹ 值 ± π（或 + 2π）四捨五入後算術一致
        disp = round(at, 3) + (round(shift, 3) if shift else 0.0)
        if d["mode"] == "02pi" and at + shift < 0:
            disp += round(2 * PI, 3)
        ok(f"{pid} 顯示的 tan⁻¹={at:.3f} 調象限後 {disp:.3f} ≈ {alpha:.3f}", abs(disp - alpha) <= 1.5e-3)

    # ---- 5-2 ----
    X = 2 + 7 * math.cos(PI / 4); Y = 7 * math.sin(PI / 4)
    near("5-2 E0cosα", X, 6.950, 6e-4); near("5-2 E0sinα", Y, 4.950, 6e-4)
    near("5-2 7cos45°", 7 * math.cos(PI / 4), 4.950, 6e-4)
    near("5-2 E0", math.hypot(X, Y), 8.53, 6e-3); near("5-2 E0²", X * X + Y * Y, 72.80, 6e-3)
    near("5-2 tanα", Y / X, 0.7122, 6e-5); near("5-2 α", math.atan2(Y, X), 0.619, 6e-4)
    near("5-2 α/π", math.atan2(Y, X) / PI, 0.197, 6e-4)
    near("5-2 α°", math.degrees(math.atan2(Y, X)), 35.5, 0.06)

    # ---- 2018m5 駐波 ----
    x, tt = np.meshgrid(np.linspace(-5, 5, 41), np.linspace(-2, 2, 41))
    lhs = 100 * np.sin(PI / 3 * x) * np.cos(6 * PI * tt)
    ok("2018m5 積化和差", np.allclose(lhs, 50 * np.sin(PI / 3 * x + 6 * PI * tt) + 50 * np.sin(PI / 3 * x - 6 * PI * tt)))

    # ---- 5-8 符號推導 ----
    w, c = sp.symbols("omega c", positive=True)
    n = sp.Function("n")(w)
    vp = c / n; lam = 2 * sp.pi * c / (n * w)
    lam_dvp = sp.simplify(lam * sp.diff(vp, w) / sp.diff(lam, w))
    np_ = sp.diff(n, w)
    ok("5-8 λ dv_p/dλ = (c/n)·ωn'/(n+ωn')", sp.simplify(lam_dvp - c / n * w * np_ / (n + w * np_)) == 0)
    ok("5-8 v_g = c/(n+ωn')", sp.simplify(vp - lam_dvp - c / (n + w * np_)) == 0)
    ok("5-8 dλ/dω = -2πc(n+ωn')/(nω)²", sp.simplify(sp.diff(lam, w) + 2 * sp.pi * c * (n + w * np_) / (n * w) ** 2) == 0)

    # ---- 2007m3 海浪 ----
    L, g, T, rho = sp.symbols("lambda g T rho", positive=True)
    for name, vpx, want in [("長波長", sp.sqrt(g * L / (2 * sp.pi)), sp.Rational(1, 2)),
                            ("短波長", sp.sqrt(2 * sp.pi * T / (L * rho)), sp.Rational(3, 2))]:
        vg = vpx - L * sp.diff(vpx, L)
        ok(f"2007m3 {name} v_g/v_p = {want}", sp.simplify(vg / vpx - want) == 0)

    # ---- 5-9 ----
    d = 1 / 30 * (1.50 - 1); slope = d / (4861 - 6563); corr = 5890 / 1.50 * slope
    near("5-9 n_F-n_C", d, 0.01667, 6e-6); near("5-9 λ_F-λ_C", 4861 - 6563, -1702, 0)
    near("5-9 dn/dλ (×1e-6)", slope * 1e6, -9.79, 6e-3)
    near("5-9 (λ/n)dn/dλ", corr, -0.0385, 6e-5)
    near("5-9 v_g (×1e8)", 2.00 * (1 + corr), 1.92, 6e-3)
    near("5-9 c/v_g", 1.50 / (1 + corr), 1.56, 6e-3)

    # ---- 5-10 ----
    n5 = 1.40 + 2.5e6 / 5000 ** 2; dn = -2 * 2.5e6 / 5000 ** 3; corr = 5000 / 1.50 * dn
    near("5-10 n", n5, 1.50, 1e-12); near("5-10 dn/dλ (×1e-5)", dn * 1e5, -4.0, 1e-9)
    near("5-10 (λ/n)dn/dλ", corr, -0.1333, 6e-5); near("5-10 1+修正", 1 + corr, 0.8667, 6e-5)
    near("5-10 v_g (×1e8)", 2.00 * (1 + corr), 1.73, 6e-3); near("5-10 c/v_g", 1.50 / (1 + corr), 1.73, 6e-3)
    near("5-10 5000³ (×1e11)", 5000 ** 3 / 1e11, 1.25, 1e-12)

    # ---- 5-11 ----
    K = sp.Function("K")(w)
    k = sp.sqrt(K) * w / c
    ok("5-11 dk/dω", sp.simplify(sp.diff(k, w) - sp.sqrt(K) / c * (1 + w / (2 * K) * sp.diff(K, w))) == 0)
    A, w0 = sp.symbols("A omega_0", positive=True)
    Kx = 1 + A / (w0 ** 2 - w ** 2)
    ok("5-11 dK/dω = 2Aω/(ω0²-ω²)²", sp.simplify(sp.diff(Kx, w) - 2 * A * w / (w0 ** 2 - w ** 2) ** 2) == 0)
    eps = w / (2 * Kx) * sp.diff(Kx, w)
    ok("5-11 ε = Aω²/(K(ω0²-ω²)²)", sp.simplify(eps - A * w ** 2 / (Kx * (w0 ** 2 - w ** 2) ** 2)) == 0)

    # ---- 2012m1 ----
    lhs = 100 * np.cos(4 * PI * x) * np.sin(5 * PI * tt)
    ok("2012m1 積化和差", np.allclose(lhs, 50 * np.sin(5 * PI * tt + 4 * PI * x) + 50 * np.sin(5 * PI * tt - 4 * PI * x)))
    near("2012m1 λ", 2 * PI / (4 * PI), 0.5, 1e-12); near("2012m1 ν", 5 * PI / (2 * PI), 2.5, 1e-12)
    near("2012m1 v=νλ", 0.5 * 2.5, 1.25, 1e-12)

    # ---- 2014q3 ----
    lam = 20 / 5; kk = 2 * PI / lam; om = 2 * PI * 5
    near("2014q3 λ", lam, 4, 0); near("2014q3 k/π", kk / PI, 0.5, 1e-12); near("2014q3 ω/π", om / PI, 10, 1e-12)
    s1 = 10 * np.cos(kk * x - om * tt) + 10 * np.cos(kk * x + om * tt)
    ok("2014q3 和差化積", np.allclose(s1, 20 * np.cos(kk * x) * np.cos(om * tt)))
    ok("2014q3 節點 x=2n+1", all(abs(math.cos(kk * (2 * m + 1))) < 1e-12 for m in range(-3, 4)))
    ok("2014q3 波腹 x=2n", all(abs(abs(math.cos(kk * 2 * m)) - 1) < 1e-12 for m in range(-3, 4)))

    print(f"\n共 {len(FAIL)} 項不通過" if FAIL else "\nALL PASS")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
