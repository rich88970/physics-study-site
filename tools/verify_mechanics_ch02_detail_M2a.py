"""力學 Lecture 2 第 1–8 節（M2a 詳解擴寫）：驗算詳解裡新寫出的每個中間值與答案。

範圍：sections/01-laws … 08-projectile 的題目卡（範本卡 c2-tm-2-6 除外）。
每個 check 的期望值就是網頁上印出的數字，容許誤差取最後一位的一半左右。
用法：python -X utf8 tools/verify_mechanics_ch02_detail_M2a.py（需要 numpy、scipy、sympy）
"""
import math

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

ok = True
g = 9.8
deg = math.pi / 180


def check(name, got, want, tol):
    """|got-want| <= tol"""
    global ok
    good = abs(float(got) - float(want)) <= tol
    ok &= good
    print(("OK  " if good else "FAIL"), name, round(float(got), 6), "expected", want)


def zero(name, expr):
    """sympy 化簡後應該是 0"""
    global ok
    z = sp.simplify(expr)
    good = z == 0
    ok &= bool(good)
    print(("OK  " if good else "FAIL"), name, "" if good else z)


t, x, y, k, m, v, v0, h, a, b, c, A, L, M, X = sp.symbols("t x y k m v v0 h a b c A L M X", positive=True)
th, al, be, mu, lam, ph = sp.symbols("theta alpha beta mu lambda phi", positive=True)

# ===================== 01 牛頓三定律 =====================
# c2-self-01a
V = sp.symbols("V", real=True)
m1s, m2s, v1s, v2s = sp.symbols("m1 m2 v1 v2", real=True)
T = m1s * v1s**2 / 2 + m2s * v2s**2 / 2
Tp = m1s * (v1s - V) ** 2 / 2 + m2s * (v2s - V) ** 2 / 2
zero("01a (a) T' = T - V P + M V^2/2", Tp - (T - V * (m1s * v1s + m2s * v2s) + (m1s + m2s) * V**2 / 2))
m1, m2, v1 = 2, 1, 3
u1, u2 = (m1 - m2) / (m1 + m2) * v1, 2 * m1 / (m1 + m2) * v1
check("01a u1", u1, 1, 1e-12)
check("01a u2", u2, 4, 1e-12)
check("01a T前", 0.5 * m1 * v1**2, 9, 1e-12)
check("01a T後", 0.5 * m1 * u1**2 + 0.5 * m2 * u2**2, 9, 1e-12)
check("01a T'前", 0.5 * m1 * (v1 - 3) ** 2 + 0.5 * m2 * (0 - 3) ** 2, 4.5, 1e-12)
check("01a T'後", 0.5 * m1 * (u1 - 3) ** 2 + 0.5 * m2 * (u2 - 3) ** 2, 4.5, 1e-12)
check("01a 套 (a)", 9 - 3 * 6 + 0.5 * 3 * 9, 4.5, 1e-12)

# c2-self-01b
hh, muv = 1.0, 0.05
mc = muv / math.tan(30 * deg)
check("01b mu cot30", mc, 0.0866, 5e-5)
check("01b 1-mu cot30", 1 - mc, 0.9134, 5e-5)
check("01b cot10", 1 / math.tan(10 * deg), 5.671, 5e-4)
check("01b 分母 10°", 1 + muv / math.tan(10 * deg), 1.2836, 5e-5)
check("01b h'(30)", hh * (1 - mc) / (1 + mc), 0.841, 5e-4)
check("01b h'(10)", hh * (1 - mc) / (1 + muv / math.tan(10 * deg)), 0.712, 5e-4)
check("01b s", hh * (1 - mc) / muv, 18.3, 0.05)

# ===================== 02 參考座标系 =====================
w2R = 0.0339
check("02a delta_max rad", w2R / (2 * g), 1.73e-3, 5e-6)
check("02a delta_max deg", w2R / (2 * g) / deg, 0.099, 5e-4)
lk = 22.6 * deg
num, den = w2R * math.sin(lk) * math.cos(lk), g - w2R * math.cos(lk) ** 2
check("02a sin22.6", math.sin(lk), 0.3843, 5e-5)
check("02a cos22.6", math.cos(lk), 0.9232, 5e-5)
check("02a cos^2 22.6", math.cos(lk) ** 2, 0.8523, 5e-5)
check("02a 分子", num, 0.01203, 5e-6)
check("02a 分母", den, 9.771, 5e-4)
check("02a tan delta", num / den, 1.23e-3, 5e-6)
check("02a delta deg", math.atan(num / den) / deg, 0.0705, 5e-5)
check("02a 讀數少 %", w2R * math.cos(lk) ** 2 / g * 100, 0.29, 0.005)
check("02a 赤道 %", w2R / g * 100, 0.35, 0.005)
geff = math.hypot(den, num)
print("     02a 垂直分量對 |g_eff| 的相對影響（應為 1e-6 量級）:", (geff - den) / den)
aa, HH = 1.5, 1.0
check("02b t_f", math.sqrt(2 * HH / g), 0.452, 5e-4)
check("02b dx", aa * HH / g, 0.153, 5e-4)
check("02b tan phi", aa / g, 0.153, 5e-4)
check("02b phi", math.degrees(math.atan(aa / g)), 8.7, 0.05)

# ===================== 03 第二、第三定律 =====================
G, ma, mb, d, w = sp.symbols("G m_a m_b d omega", positive=True)
r1 = mb * d / (ma + mb)
w2 = sp.solve(sp.Eq(G * ma * mb / d**2, ma * w**2 * r1), w**2)[0]
zero("2-49 omega^2", w2 - G * (ma + mb) / d**3)
zero("2-48 omega^2（r=d/2）", sp.solve(sp.Eq(G * m**2 / d**2, m * w**2 * d / 2), w**2)[0] - 2 * G * m / d**3)
# 2-2：球座標加速度（sympy 直接微分）
tt = sp.symbols("t")
TH, PH = sp.Function("TH")(tt), sp.Function("PH")(tt)
R = sp.symbols("R", positive=True)
er = sp.Matrix([sp.sin(TH) * sp.cos(PH), sp.sin(TH) * sp.sin(PH), sp.cos(TH)])
et = sp.Matrix([sp.cos(TH) * sp.cos(PH), sp.cos(TH) * sp.sin(PH), -sp.sin(TH)])
ep = sp.Matrix([-sp.sin(PH), sp.cos(PH), 0])
acc = (R * er).diff(tt, 2)
Td, Pd = TH.diff(tt), PH.diff(tt)
zero("2-2 a·e_r", acc.dot(er) + R * (Td**2 + Pd**2 * sp.sin(TH) ** 2))
zero("2-2 a·e_theta", acc.dot(et) - R * (TH.diff(tt, 2) - Pd**2 * sp.sin(TH) * sp.cos(TH)))
zero("2-2 a·e_phi", acc.dot(ep) - R * (PH.diff(tt, 2) * sp.sin(TH) + 2 * Td * Pd * sp.cos(TH)))
zero("2-2 de_r/dt", (er.diff(tt) - (Td * et + Pd * sp.sin(TH) * ep)).norm())
# c2-self-03a
lm, xx = sp.symbols("lambda_ x", positive=True)
vv = sp.sqrt(2 * g * xx)
# dp/dt = λ[-v·v + (L-x)g]，N = Mg - dp/dt
N_expr = lm * L * g - (-lm * vv**2 + lm * (L - xx) * g)
zero("03a N = 3 λ g x", N_expr - 3 * lm * g * xx)
check("03a λ", 0.50 / 1.0, 0.50, 1e-12)
check("03a N(0.5)", 3 * 0.5 * g * 0.5, 7.35, 1e-9)
check("03a 秤上重量", 0.5 * g * 0.5, 2.45, 1e-9)
check("03a N_max", 3 * 0.50 * g, 14.7, 1e-9)
# c2-self-03b
Mb, mp, Lw = 120.0, 60.0, 3.0
check("03b dx_b", -mp * Lw / (Mb + mp), -1.0, 1e-12)
check("03b dx_人", -mp * Lw / (Mb + mp) + Lw, 2.0, 1e-12)
check("03b ∫u dt", quad(lambda s: 0.75 * (1 - math.cos(math.pi * s / 2)), 0, 4)[0], 3.0, 1e-9)


def boat(tq, Y, bb):
    xb, vb = Y
    ud = 0.75 * (math.pi / 2) * math.sin(math.pi * tq / 2) if tq < 4 else 0.0
    return [vb, (-mp * ud - bb * vb) / (Mb + mp)]


s4 = solve_ivp(boat, [0, 4], [0, 0], args=(30.0,), rtol=1e-10, atol=1e-12)
check("03b 人停下時船退", s4.y[0, -1], -0.72, 0.005)
sinf = solve_ivp(boat, [4, 400], s4.y[:, -1], args=(30.0,), rtol=1e-10, atol=1e-12)
check("03b 最後 x_b", sinf.y[0, -1], 0.0, 1e-4)
check("03b 人停下時船速向前", s4.y[1, -1] > 0, 1, 0)

# ===================== 04 解題策略 =====================
kk, alp = 1.0, 0.5
check("2-23 a_max", kk / (alp * math.e), 0.736, 5e-4)
check("2-23 k/mα²", kk / alp**2, 4, 1e-12)
aF = lambda s: s * math.exp(-s / 2)
vF = lambda s: 4 * (1 - (1 + s / 2) * math.exp(-s / 2))
xF = lambda s: 4 * (s - 4 + (s + 4) * math.exp(-s / 2))
for tq, av, vvv, xv in [(2, 0.736, 1.06, 0.83), (5, 0.410, 2.85, 6.96), (10, 0.067, 3.84, 24.4), (20, 0.001, 4.00, 64.0)]:
    check(f"2-23 表 a({tq})", aF(tq), av, 5e-4)
    check(f"2-23 表 v({tq})", vF(tq), vvv, 5e-3)
    check(f"2-23 表 x({tq})", xF(tq), xv, 0.05 if xv > 20 else 5e-3)
ts = sp.symbols("t", positive=True)
zero("2-23 ∫(1+ατ)e^{-ατ}", sp.integrate((1 + al * ts) * sp.exp(-al * ts), (ts, 0, t)) - (2 - (2 + al * t) * sp.exp(-al * t)) / al)
zero("2-23 v(t) 分部積分", sp.integrate(ts * sp.exp(-al * ts), (ts, 0, t)) - (1 - (1 + al * t) * sp.exp(-al * t)) / al**2)
cc = g / (2 * 331)
check("2-30 g/2v_s", cc, 0.014804, 5e-7)
check("2-30 4cT", 4 * cc * 4.021, 0.2381, 5e-5)
t1 = (-1 + math.sqrt(1 + 4 * cc * 4.021)) / (2 * cc)
check("2-30 分子", math.sqrt(1 + 4 * cc * 4.021) - 1, 0.11270, 5e-6)
check("2-30 t1", t1, 3.807, 5e-4)
check("2-30 h", 0.5 * g * t1**2, 71.0, 0.05)
check("2-30 t2", 0.5 * g * t1**2 / 331, 0.214, 5e-4)
# c2-self-04a
w0 = sp.symbols("omega", positive=True)
zero("04a x=A cos ωt 滿足 ẍ=-ω²x", sp.diff(A * sp.cos(w0 * t), t, 2) + w0**2 * A * sp.cos(w0 * t))
zero("04a ∫0^A dx/sqrt(A²-x²) = π/2", sp.integrate(1 / sp.sqrt(A**2 - x**2), (x, 0, A)) - sp.pi / 2)
# c2-self-04b
check("04b x∞", 20 * math.sqrt(math.pi / (2 * 0.5)), 35.4, 0.05)
th_ = math.sqrt(2 * math.log(2) / 0.5)
check("04b t1/2", th_, 1.67, 0.005)
check("04b t1/2（四位）", th_, 1.665, 5e-4)
check("04b k", math.log(2) / th_, 0.416, 5e-4)
check("04b 線性阻力距離", 20 / (math.log(2) / th_), 48.0, 0.05)
zero("04b 高斯積分", sp.integrate(sp.exp(-b * t**2 / 2), (t, 0, sp.oo)) - sp.sqrt(sp.pi / (2 * b)))

# ===================== 05 斜面 =====================
check("ex21 a(30°)", g * math.sin(30 * deg), 4.9, 1e-9)
check("ex22 θc", math.degrees(math.atan(0.4)), 21.8, 0.05)
check("ex23 sin-μcos", 0.5 - 0.3 * math.cos(30 * deg), 0.240, 5e-4)
check("ex23 0.3×0.866", 0.3 * 0.866, 0.260, 5e-4)
check("ex23 a", g * (0.5 - 0.3 * math.cos(30 * deg)), 2.35, 0.005)
check("2-16 sin26", math.sin(26 * deg), 0.438, 5e-4)
check("2-16 g sin26", g * math.sin(26 * deg), 4.30, 0.005)
check("2-16 t", 2 * 2.4 / (g * math.sin(26 * deg)), 1.12, 0.005)
# 2-32
s_ = sp.symbols("s", positive=True)
quad_ = 4 * (1 + mu**2) * s_**2 - 4 * s_ + (1 - 4 * mu**2)
zero("2-32 二次式 = 平方後的式子", sp.expand(quad_ - ((1 - 2 * s_) ** 2 - 4 * mu**2 * (1 - s_**2))))
root = (1 - mu * sp.sqrt(3 + 4 * mu**2)) / (2 * (1 + mu**2))
zero("2-32 負號根滿足二次式", quad_.subs(s_, root))
mk = 0.1
check("2-32 sqrt(3.04)", math.sqrt(3 + 4 * mk**2), 1.7436, 5e-5)
check("2-32 分子", 1 - mk * math.sqrt(3 + 4 * mk**2), 0.8256, 5e-5)
sv = (1 - mk * math.sqrt(3 + 4 * mk**2)) / (2 * (1 + mk**2))
check("2-32 sinθ", sv, 0.4087, 5e-5)
check("2-32 θ", math.degrees(math.asin(sv)), 24.1, 0.05)
check("2-32 代回", 2 * sv + 2 * mk * math.cos(math.asin(sv)), 1.000, 5e-4)
check("2-32 正號根 > 1/2", (1 + mk * math.sqrt(3.04)) / 2.02 > 0.5, 1, 0)
# 2-24
s17, c17 = math.sin(17 * deg), math.cos(17 * deg)
check("2-24 sin17", s17, 0.2924, 5e-5)
check("2-24 cos17", c17, 0.9563, 5e-5)
check("2-24 分母", 100 * c17 + 70, 165.63, 0.005)
muS = 100 * s17 / (100 * c17 + 70)
check("2-24 μ", muS, 0.1765, 5e-5)
check("2-24 v_B²", 2 * 0.1765 * g * 70, 242.2, 0.05)
check("2-24 v_B", math.sqrt(2 * muS * g * 70), 15.6, 0.05)
# 2-29
thr = math.atan(0.08)
check("2-29 θ", math.degrees(thr), 4.57, 0.005)
check("2-29 cos", math.cos(thr), 0.9968, 5e-5)
check("2-29 sin", math.sin(thr), 0.0797, 5e-5)
check("2-29 μcos", 0.45 * math.cos(thr), 0.4486, 5e-5)
ad = g * (0.45 * math.cos(thr) - math.sin(thr))
check("2-29 a", ad, 3.61, 0.005)
v25 = 25 * 1609 / 3600
check("2-29 25 MPH", v25, 11.17, 0.005)
check("2-29 Δx", v25**2 / (2 * ad), 17.3, 0.05)
check("2-29 Δx（用印出的 11.17、3.61）", 11.17**2 / (2 * 3.61), 17.3, 0.05)
vmin = math.sqrt(2 * ad * 30)
check("2-29 v0min", vmin, 14.7, 0.05)
check("2-29 MPH", vmin * 3600 / 1609, 32.9, 0.05)
# c2-self-05a
mg = 20 * g
check("05a mg", mg, 196, 1e-9)
check("05a sin20", math.sin(20 * deg), 0.3420, 5e-5)
check("05a μcos20", 0.4 * math.cos(20 * deg), 0.3759, 5e-5)
check("05a sqrt(1.16)", math.sqrt(1.16), 1.0770, 5e-5)
F0 = mg * (math.sin(20 * deg) + 0.4 * math.cos(20 * deg))
check("05a F(0)", F0, 140.7, 0.05)
Fmin = F0 / math.sqrt(1.16)
check("05a Fmin", Fmin, 130.6, 0.05)
check("05a φ*", math.degrees(math.atan(0.4)), 21.8, 0.05)
check("05a sin21.8", math.sin(math.atan(0.4)), 0.371, 5e-4)
check("05a 196cos20", mg * math.cos(20 * deg), 184.2, 0.05)
check("05a F sinφ", Fmin * math.sin(math.atan(0.4)), 48.5, 0.05)
check("05a N", mg * math.cos(20 * deg) - Fmin * math.sin(math.atan(0.4)), 135.7, 0.05)
check("05a 省 %", (1 - Fmin / F0) * 100, 7, 0.5)
Dphi = sp.cos(ph) + mu * sp.sin(ph)
zero("05a D(φ*) = sqrt(1+μ²)", Dphi.subs(ph, sp.atan(mu)) - sp.sqrt(1 + mu**2))
# c2-self-05b
zero("05b tan(θ-λ) 恆等式", sp.simplify((sp.sin(th) - sp.tan(lam) * sp.cos(th)) / (sp.cos(th) + sp.tan(lam) * sp.sin(th)) - sp.tan(th - lam)))
zero("05b tan(θ+λ) 恆等式", sp.simplify((sp.sin(th) + sp.tan(lam) * sp.cos(th)) / (sp.cos(th) - sp.tan(lam) * sp.sin(th)) - sp.tan(th + lam)))
lmd = math.degrees(math.atan(0.2))
check("05b λ", lmd, 11.31, 0.005)
check("05b tan18.69", math.tan((30 - lmd) * deg), 0.3383, 5e-5)
check("05b tan41.31", math.tan((30 + lmd) * deg), 0.8788, 5e-5)
check("05b a_min", g * math.tan((30 - lmd) * deg), 3.32, 0.005)
check("05b a_max", g * math.tan((30 + lmd) * deg), 8.61, 0.005)
check("05b 光滑", g * math.tan(30 * deg), 5.66, 0.005)

# ===================== 06 阻力 =====================
zd = sp.Function("z")(tt)
kk_, gg, v0_, h_ = sp.symbols("k g v_0 h", positive=True)
zsol = h_ - gg * tt / kk_ + (kk_ * v0_ + gg) / kk_**2 * (1 - sp.exp(-kk_ * tt))
zero("ex25 z(t) 滿足方程式", sp.diff(zsol, tt, 2) + kk_ * sp.diff(zsol, tt) + gg)
zero("ex25 z(0)=h", zsol.subs(tt, 0) - h_)
zero("ex25 ż(0)=v0", sp.diff(zsol, tt).subs(tt, 0) - v0_)
xs = v0_ / kk_ * (1 - sp.exp(-kk_ * tt))
zero("ex24 v = v0 - kx", sp.diff(xs, tt) - (v0_ - kk_ * xs))
# 2-11
v1_ = sp.symbols("v_1", positive=True)
fs = sp.log((gg - kk_ * v0_**2) / (gg - kk_ * v1_**2)) / (2 * kk_)
zero("2-11 ds/dv1 = v1/(g-k v1²)", sp.diff(fs, v1_) - v1_ / (gg - kk_ * v1_**2))
zero("2-11 s(v0→v0)=0", fs.subs(v1_, v0_))
s11 = quad(lambda u: u / (g - 0.01 * u * u), 5, 20)[0]
check("2-11 數值積分 vs 公式（k=0.01, 5→20 m/s）", s11, math.log((g - 0.01 * 25) / (g - 0.01 * 400)) / 0.02, 1e-9)
# 2-9
zero("2-9 v(t_m')=0", (-gg / kk_ + (kk_ * v0_ + gg) / kk_ * sp.exp(-kk_ * sp.log(1 + kk_ * v0_ / gg) / kk_)).simplify())
# 2-34
al_, bt_, vv_ = sp.symbols("alpha beta v", positive=True)
zero("2-34 帶分式", vv_ / (m * gg - al_ * vv_) - (-1 / al_ + (m * gg / al_) / (m * gg - al_ * vv_)))
ya = -m / al_ * vv_ - m**2 * gg / al_**2 * sp.log(1 - al_ * vv_ / (m * gg))
zero("2-34 (a) dy/dv = mv/(mg-αv)", sp.diff(ya, vv_) - m * vv_ / (m * gg - al_ * vv_))
yb = -m / (2 * bt_) * sp.log((m * gg - bt_ * vv_**2) / (m * gg))
zero("2-34 (b) v²(y) 反解", (m * gg / bt_ * (1 - sp.exp(-2 * bt_ * yb / m))) - vv_**2)
# 2-15
lamb = sp.sqrt(kk_ * gg * sp.sin(th))
xt = sp.log(sp.cosh(lamb * tt)) / kk_
vt_ = sp.diff(xt, tt)
zero("2-15 x(t) 滿足 v̇ = g sinθ - k v²", sp.diff(vt_, tt) - (gg * sp.sin(th) - kk_ * vt_**2))
# 2-13
aa_ = sp.symbols("a", positive=True)
zero("2-13 部分分式", 1 / (vv_ * (vv_**2 + aa_**2)) - (1 / vv_ - vv_ / (vv_**2 + aa_**2)) / aa_**2)
xv13 = lambda V0, aq, kq: quad(lambda u: 1 / (kq * (u * u + aq * aq)), 0, V0)[0]
check("2-13 v0=1000a 時 x/(π/2ka)", xv13(1000.0, 1.0, 1.0) / (math.pi / 2), 0.9994, 5e-5)
# 2-51
tb = 999 * 200 / (0.2 * 2)
check("2-51 t", tb, 4.995e5, 1)
check("2-51 天", tb / 86400, 5.8, 0.05)
check("2-51 ln1000", math.log(1000), 6.908, 5e-4)
check("2-51 x", 1000 * math.log(1000), 6.9e3, 50)
# 2-54
check("2-54 v_t", g / 0.01, 980, 1e-9)
check("2-54 kv0/g", 1.2 / g, 0.12245, 5e-6)
check("2-54 ln", math.log(1 + 1.2 / g), 0.115513, 5e-7)
check("2-54 98000 ln", 98000 * math.log(1 + 1.2 / g), 11320, 0.5)
ymax = 12000 - 98000 * math.log(1 + 1.2 / g)
check("2-54 y_max", ymax, 680, 0.5)
# 2-10
check("2-10 v(10)", 10 * math.exp(-1), 3.679, 5e-4)
check("2-10 x(10)", 100 * (1 - math.exp(-1)), 63.21, 0.005)
check("2-10 ln2/k", math.log(2) / 0.1, 6.9, 0.05)
# 2-33
rho, cw, rw = 1.3, 0.5, 1000.0


def drop(mq, rq, H=100.0):
    Aq = math.pi * rq**2
    cra = cw * rho * Aq
    vt = math.sqrt(2 * mq * g / cra)
    L2 = vt**2 / g
    vH = vt * math.sqrt(1 - math.exp(-2 * H / L2))
    tH = vt / g * math.acosh(math.exp(H / L2))
    return Aq, cra, vt, L2, vH, tH


Ab, crb, vtb, Lb, vHb, tHb = drop(0.145, 0.0366)
check("2-33 棒球 A", Ab, 4.208e-3, 5e-7)
check("2-33 棒球 cWρA", crb, 2.735e-3, 5e-7)
check("2-33 棒球 v_t", vtb, 32.23, 0.005)
check("2-33 棒球 v_t²/g", Lb, 106, 0.5)
check("2-33 棒球 2gH/v_t²", 200 / Lb, 1.887, 5e-4)
check("2-33 棒球 e^-1.887", math.exp(-200 / Lb), 0.152, 5e-4)
check("2-33 棒球 v_H", vHb, 29.7, 0.05)
check("2-33 棒球 %", vHb / vtb * 100, 92, 0.5)
check("2-33 棒球 gH/v_t²", 100 / Lb, 0.9433, 5e-5)
check("2-33 棒球 t_H（用印出的數字）", 32.23 / g * math.acosh(math.exp(0.9433)), 5.25, 0.005)
check("2-33 棒球 t_H", tHb, 5.25, 0.005)
Ap, crp, vtp, Lp, vHp, tHp = drop(0.0024, 0.019)
check("2-33 乒乓 A", Ap, 1.134e-3, 5e-7)
check("2-33 乒乓 cWρA", crp, 7.372e-4, 5e-8)
check("2-33 乒乓 v_t", vtp, 7.99, 0.005)
check("2-33 乒乓 v_t²/g", Lp, 6.5, 0.05)
check("2-33 乒乓 H/(v_t²/g)", 100 / Lp, 15.36, 0.005)
check("2-33 乒乓 v_H", vHp, 7.99, 0.005)
check("2-33 乒乓 t_H（近似 u+ln2）", vtp / g * (100 / Lp + math.log(2)), 13.1, 0.05)
check("2-33 乒乓 t_H（精確）", tHp, 13.1, 0.05)
mr = 4 / 3 * math.pi * 0.003**3 * rw
check("2-33 雨滴 m", mr, 1.131e-4, 5e-8)
Ar, crr, vtr, Lr, vHr, tHr = drop(mr, 0.003)
check("2-33 雨滴 A", Ar, 2.827e-5, 5e-9)
check("2-33 雨滴 v_t", vtr, 11.0, 0.05)
check("2-33 雨滴 v_t²/g", Lr, 12.3, 0.05)
check("2-33 雨滴 H/(v_t²/g)", 100 / Lr, 8.125, 5e-4)
check("2-33 雨滴 v_t（四位）", vtr, 10.98, 0.005)
check("2-33 雨滴 t_H（近似，用印出的數字）", 10.98 / g * (8.125 + 0.693), 9.88, 0.005)
check("2-33 雨滴 t_H", tHr, 9.88, 0.005)
check("2-33 無阻力 t", math.sqrt(200 / g), 4.52, 0.005)
check("2-33 無阻力 v", math.sqrt(2 * g * 100), 44.3, 0.05)
check("2-33 (e) 棒球", crb / (2 * 0.145), 9.4e-3, 5e-5)
check("2-33 (e) 乒乓", crp / (2 * 0.0024), 0.154, 5e-4)
check("2-33 (e) 倍數", (crp / 0.0048) / (crb / 0.29), 16, 0.5)
coef = 8 * rw * g / (3 * cw * rho)
check("2-33 (f) 係數", coef, 4.02e4, 50)
check("2-33 (f) 80.4", coef * 0.002, 80.4, 0.05)
check("2-33 (f) 160.8", coef * 0.004, 160.8, 0.05)
check("2-33 (f) 2mm", math.sqrt(coef * 0.002), 8.97, 0.005)
check("2-33 (f) 4mm", math.sqrt(coef * 0.004), 12.7, 0.05)
# c2-self-06a
acoth = lambda u: 0.5 * math.log((u + 1) / (u - 1))
check("06a coth⁻¹(1.2)", acoth(1.2), 1.199, 5e-4)
check("06a coth⁻¹(11)", acoth(11), 0.091, 5e-4)
check("06a v_t/g", 5 / g, 0.510, 5e-4)
check("06a 差", acoth(1.2) - acoth(11), 1.108, 5e-4)
t6 = 5 / g * (acoth(1.2) - acoth(11))
check("06a t", t6, 0.565, 5e-4)
check("06a 3000/11", 3000 / 11, 272.7, 0.05)
check("06a ln", math.log(3000 / 11), 5.608, 5e-4)
check("06a 25/19.6", 25 / 19.6, 1.276, 5e-4)
check("06a y", 25 / 19.6 * math.log(3000 / 11), 7.15, 0.005)
check("06a 減速度/g", 55**2 / 25 - 1, 120, 1e-9)
sol6 = solve_ivp(lambda s, Y: [Y[1], g * (1 - Y[1] ** 2 / 25)], [0, 1], [0, 55], events=lambda s, Y: Y[1] - 6, rtol=1e-10, atol=1e-12)
check("06a 數值 t", sol6.t_events[0][0], 0.565, 5e-4)
check("06a 數值 y", sol6.y_events[0][0][0], 7.15, 0.005)
# c2-self-06b
k6, v06 = 0.2, 20.0
check("06b kv0/g", k6 * v06 / g, 0.4082, 5e-5)
L6 = math.log(1 + k6 * v06 / g)
check("06b ln1.4082", L6, 0.3423, 5e-5)
check("06b ln（五位）", L6, 0.34229, 5e-6)
check("06b t_up", L6 / k6, 1.711, 5e-4)
H6 = v06 / k6 - g / k6**2 * L6
check("06b H", H6, 16.14, 0.005)
fall = lambda s: g / k6 * s - g / k6**2 * (1 - math.exp(-k6 * s))
check("06b 試 1.90", fall(1.90), 15.65, 0.005)
check("06b 試 1.95", fall(1.95), 16.43, 0.005)
td = brentq(lambda s: fall(s) - H6, 1, 3)
check("06b t_down", td, 1.932, 5e-4)
check("06b e^-0.3864", math.exp(-0.3864), 0.6795, 5e-5)
vb6 = g / k6 * (1 - math.exp(-k6 * td))
check("06b v_back", vb6, 15.70, 0.005)
check("06b 400-246.5", 0.5 * (400 - vb6**2), 76.7, 0.05)
check("06b 15.70²", 15.70**2, 246.5, 0.05)
check("06b %", (1 - vb6**2 / 400) * 100, 38, 0.5)

# ===================== 07 由速度求力 =====================
alq, beq = sp.symbols("alpha beta", positive=True)
vt39 = -sp.log(alq * beq / m * t + sp.exp(-beq * v0)) / beq
zero("2-39 v(t) 滿足 m v̇ = -α e^{βv}", m * sp.diff(vt39, t) + alq * sp.exp(beq * vt39))
tend = m / (alq * beq) * (1 - sp.exp(-beq * v0))
zero("2-39 v(t_end)=0", vt39.subs(t, tend))
dd = sp.integrate(vt39, (t, 0, tend))
zero("2-39 距離（直接積 v(t)）", sp.simplify(dd - m / (alq * beq**2) * (1 - (1 + beq * v0) * sp.exp(-beq * v0))))
zero("2-39 分部積分", sp.diff(-(v * sp.exp(-beq * v) + sp.exp(-beq * v) / beq) / beq, v) - v * sp.exp(-beq * v))
zero("2-37 F", sp.Rational(1, 2) * m * sp.diff((alq / x) ** 2, x) + m * alq**2 / x**3)
n_ = sp.symbols("n", positive=True)
x38 = ((n_ + 1) * alq * t) ** (1 / (n_ + 1))
zero("2-38 ẋ = α x^-n", sp.simplify(sp.diff(x38, t) - alq * x38 ** (-n_)))
zero("2-38 F(t)", sp.simplify(m * sp.diff(x38, t, 2) + m * n_ * alq**2 * ((n_ + 1) * alq * t) ** (-(2 * n_ + 1) / (n_ + 1))))
F_, m0, cl = sp.symbols("F m_0 c", positive=True)
v50 = (F_ * t / m0) / sp.sqrt(1 + (F_ * t / (m0 * cl)) ** 2)
zero("2-50 p(v(t)) = Ft", sp.simplify(m0 * v50 / sp.sqrt(1 - v50**2 / cl**2) - F_ * t))
x50 = m0 * cl**2 / F_ * (sp.sqrt(1 + (F_ * t / (m0 * cl)) ** 2) - 1)
zero("2-50 ẋ = v", sp.simplify(sp.diff(x50, t) - v50))
cS = 3.00e8
check("2-50 u(0.5)", 0.5 / math.sqrt(0.75), 0.577, 5e-4)
check("2-50 u(0.99)", 0.99 / math.sqrt(1 - 0.9801), 7.02, 0.005)
check("2-50 t(0.5)", 0.5 / math.sqrt(0.75) * cS / 10, 1.73e7, 5e4)
check("2-50 t(0.99)", 0.99 / math.sqrt(0.0199) * cS / 10, 2.1e8, 5e6)
check("2-50 年(0.5)", 0.5 / math.sqrt(0.75) * cS / 10 / 3.156e7, 0.55, 0.005)
check("2-50 年(0.99)", 0.99 / math.sqrt(0.0199) * cS / 10 / 3.156e7, 6.7, 0.05)
# c2-self-07a
zero("07a F = -(m/L) v²", sp.Rational(1, 2) * m * sp.diff((v0 * sp.exp(-x / L)) ** 2, x) + m / L * (v0 * sp.exp(-x / L)) ** 2)
x7 = L * sp.log(1 + v0 * t / L)
zero("07a ẋ = v0 e^{-x/L}", sp.simplify(sp.diff(x7, t) - v0 * sp.exp(-x7 / L)))
# c2-self-07b
xb = X * (sp.sqrt(1 + (cl * t / X) ** 2) - 1)
zero("07b 雙曲線", sp.expand((xb + X) ** 2 - (cl * t) ** 2 - X**2))
zero("07b 有理化", sp.simplify((cl * t - xb) - (X - X**2 / (cl * t + sp.sqrt(X**2 + cl**2 * t**2)))))
Xv = 2.998e8**2 / 10
check("07b X", Xv, 8.99e15, 5e12)
check("07b 光年", Xv / 9.461e15, 0.95, 0.005)

# ===================== 08 拋體 =====================
check("ex26 sin110", math.sin(110 * deg), 0.940, 5e-4)
check("ex26 sin55", math.sin(55 * deg), 0.819, 5e-4)
check("ex26 R", 1450**2 * math.sin(110 * deg) / g / 1000, 202, 0.5)
check("ex26 T", 2 * 1450 * math.sin(55 * deg) / g, 242, 0.5)
check("ex26 v0 sinθ", 1450 * math.sin(55 * deg), 1188, 0.5)
check("ex26 y_max", (1450 * math.sin(55 * deg)) ** 2 / (2 * g) / 1000, 72, 0.5)
v0s = sp.symbols("v_0", positive=True)
xq = v0s * sp.cos(th) * t
yq = v0s * sp.sin(th) * t - gg * t**2 / 2
zero("ex26 v²", sp.expand(sp.diff(xq, t) ** 2 + sp.diff(yq, t) ** 2 - (v0s**2 + gg**2 * t**2 - 2 * v0s * gg * t * sp.sin(th))).subs(sp.cos(th) ** 2, 1 - sp.sin(th) ** 2).expand())
zero("2-3 差角", sp.simplify(sp.sin(al) - sp.cos(al) * sp.tan(be) - sp.sin(al - be) / sp.cos(be)))
# 2-8
roots = sp.solve(gg * x**2 - v0s**2 * x + v0s**2 * h, x)
zero("2-8 d²", sp.expand((roots[1] - roots[0]) ** 2 - v0s**2 / gg**2 * (v0s**2 - 4 * gg * h)) if len(roots) == 2 else 1)
# 2-14
zero("2-14 導數 = cos(2α-β)", sp.simplify(sp.diff(sp.cos(al) * sp.sin(al - be), al) - sp.cos(2 * al - be)))
zero("2-14 積化和差", sp.simplify(2 * sp.cos(al) * sp.sin(al - be) - (sp.sin(2 * al - be) - sp.sin(be))))
dq = 2 * v0s**2 * sp.cos(al) * sp.sin(al - be) / (gg * sp.cos(be) ** 2)
zero("2-14 落點在軌跡上", sp.simplify(dq * sp.cos(be) * sp.tan(al) - gg * (dq * sp.cos(be)) ** 2 / (2 * v0s**2 * sp.cos(al) ** 2) - dq * sp.sin(be)))
# 2-19
check("2-19 sqrt(8/9)", math.sqrt(8 / 9), 0.943, 5e-4)
check("2-19 θmax", math.degrees(math.asin(math.sqrt(8 / 9))), 70.5, 0.05)
r2 = v0s**2 * t**2 - v0s * gg * t**3 * sp.sin(th) + gg**2 * t**4 / 4
zero("2-19 d(r²)/dt", sp.expand(sp.diff(r2, t) - t * (gg**2 * t**2 - 3 * v0s * gg * sp.sin(th) * t + 2 * v0s**2)))
# 2-5
check("2-5 990²", 990**2, 9.80e5, 500)
check("2-5 8g", 8 * g, 78.4, 1e-9)
check("2-5 R", 990**2 / (8 * g), 1.25e4, 50)
check("2-5 只看 v²/R≤9g", 990**2 / (9 * g) / 1000, 11.1, 0.05)
# 2-4
check("2-4 t空中", 4 * 0.9 - 0.9, 2.7, 1e-9)
check("2-4 v0", g * 2.7 / 2, 13.2, 0.05)
check("2-4 H", (g * 2.7 / 2) ** 2 / (2 * g), 8.9, 0.05)
check("2-4 H（用 13.2）", 13.2**2 / (2 * g), 8.9, 0.05)
# 2-17
t35 = math.tan(35 * deg)
check("2-17 tan35", t35, 0.7002, 5e-5)
check("2-17 60tan35", 60 * t35, 42.01, 0.005)
check("2-17 60tan35-1.3", 60 * t35 - 1.3, 40.71, 0.005)
check("2-17 cos²35", math.cos(35 * deg) ** 2, 0.6710, 5e-5)
check("2-17 9.8×3600", 9.8 * 3600, 35280, 1e-6)
v017 = g * 3600 / (2 * math.cos(35 * deg) ** 2 * (60 * t35 - 1.3))
check("2-17 v0²", v017, 645.7, 0.05)
check("2-17 v0", math.sqrt(v017), 25.4, 0.05)
check("2-17 km/h", math.sqrt(v017) * 3.6, 91, 0.5)
# 2-36
for V0, hq, angw, Rw in [(100, 100, 42.4, 1116), (50, 100, 36.8, 341), (30, 200, 23.4, 213)]:
    Rf = lambda q: V0 * math.cos(q) / g * (V0 * math.sin(q) + math.sqrt(V0**2 * math.sin(q) ** 2 + 2 * g * hq))
    qs = np.linspace(0.01, math.pi / 2 - 0.01, 200001)
    Rs = np.array([Rf(q) for q in qs[::50]])
    i = int(np.argmax(Rs))
    check(f"2-36 掃描 θ* ({V0},{hq})", math.degrees(qs[::50][i]), angw, 0.05)
    check(f"2-36 掃描 Rmax ({V0},{hq})", Rs[i], Rw, 0.5)
    check(f"2-36 解析 θ* ({V0},{hq})", math.degrees(math.asin(V0 / math.sqrt(2 * (V0**2 + g * hq)))), angw, 0.05)
    check(f"2-36 解析 Rmax ({V0},{hq})", V0 / g * math.sqrt(V0**2 + 2 * g * hq), Rw, 0.5)
check("2-36 sinθ*(100,100)", 100 / math.sqrt(2 * (10000 + 980)), 0.6748, 5e-5)
Tq = (v0s * sp.sin(th) + sp.sqrt(v0s**2 * sp.sin(th) ** 2 + 2 * gg * h)) / gg
zero("2-36 y(T) = -h", sp.expand(v0s * sp.sin(th) * Tq - gg * Tq**2 / 2 + h))
# 2-40
Aq_, alq_ = sp.symbols("A alpha", positive=True)
X40 = Aq_ * (2 * alq_ * t - sp.sin(alq_ * t))
Y40 = Aq_ * (1 - sp.cos(alq_ * t))
vx, vy = sp.diff(X40, t), sp.diff(Y40, t)
ax_, ay_ = sp.diff(vx, t), sp.diff(vy, t)
zero("2-40 v²", sp.simplify(vx**2 + vy**2 - Aq_**2 * alq_**2 * (5 - 4 * sp.cos(alq_ * t))))
zero("2-40 外積", sp.simplify(vx * ay_ - vy * ax_ - Aq_**2 * alq_**3 * (2 * sp.cos(alq_ * t) - 1)))
zero("2-40 a_t", sp.simplify(sp.diff(Aq_ * alq_ * sp.sqrt(5 - 4 * sp.cos(alq_ * t)), t) - 2 * Aq_ * alq_**2 * sp.sin(alq_ * t) / sp.sqrt(5 - 4 * sp.cos(alq_ * t))))
cq = sp.symbols("c")
zero("2-40 f'(c)", sp.simplify(sp.diff((2 * cq - 1) ** 2 / (5 - 4 * cq), cq) - 4 * (2 * cq - 1) * (4 - 2 * cq) / (5 - 4 * cq) ** 2))
# c2-self-08a
check("08a 400/19.6", 400 / 19.6, 20.41, 0.005)
check("08a 9.8×900/800", 9.8 * 900 / 800, 11.03, 0.005)
check("08a 邊界高度", 400 / 19.6 - 9.8 * 900 / 800, 9.38, 0.005)
aw = g * 900 / (2 * 400)
check("08a a", aw, 11.025, 1e-9)
check("08a 4a(y+a)", 4 * aw * (8 + aw), 839.0, 0.05)
check("08a sqrt", math.sqrt(900 - 4 * aw * (8 + aw)), 7.81, 0.005)
u_hi, u_lo = (30 + math.sqrt(900 - 4 * aw * (8 + aw))) / (2 * aw), (30 - math.sqrt(900 - 4 * aw * (8 + aw))) / (2 * aw)
check("08a u 高", u_hi, 1.715, 5e-4)
check("08a u 低", u_lo, 1.006, 5e-4)
check("08a θ 高", math.degrees(math.atan(u_hi)), 59.8, 0.05)
check("08a θ 低", math.degrees(math.atan(u_lo)), 45.2, 0.05)
for uq in (u_hi, u_lo):
    check("08a 代回 y(30)", 30 * uq - aw * (1 + uq**2), 8.00, 0.005)
zero("08a (c) x_max²", sp.solve(sp.Eq(-h, v0s**2 / (2 * gg) - gg * x**2 / (2 * v0s**2)), x)[0] ** 2 - v0s**2 / gg**2 * (v0s**2 + 2 * gg * h))
# c2-self-08b
check("08b v0min²", g * 500 / 20, 245, 1e-9)
check("08b v0min", math.sqrt(g * 500 / 20), 15.7, 0.05)

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
raise SystemExit(0 if ok else 1)
