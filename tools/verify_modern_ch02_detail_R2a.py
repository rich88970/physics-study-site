"""近代物理第 2 章「詳細解題」改寫（R2a：01–06 節，40 張題目卡）新出現數值的獨立驗算。

用法：python tools/verify_modern_ch02_detail_R2a.py
改寫時把每一步的中間值都寫了出來（代入式、拆開的步驟、補充的例子）。這裡逐一重算，
和網站上寫的數字比較（預設相對誤差 2%，有效位數較多的用更嚴的門檻）；全部通過才 exit 0。
"""
import sys
from math import sqrt, exp, log, sin, cos, asin, radians, degrees, pi, e as E

import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")

h = 6.626e-34      # J s
h3 = 6.63e-34      # 課本三位數
hev = 4.136e-15    # eV s
c = 2.998e8
c3 = 3.00e8
qe = 1.602e-19
HC = 1240.0        # eV nm
kB = 1.381e-23
me_c2 = 511.0      # keV
me = 9.11e-31

fails = []


def check(name, got, want, rel=0.02):
    ok = abs(got - want) <= rel * abs(want) + 1e-300
    print(f"{'OK ' if ok else 'BAD'} {name:<40} 算得 {got:.6g}  網站 {want:.6g}")
    if not ok:
        fails.append(name)


def truth(name, cond):
    print(f"{'OK ' if cond else 'BAD'} {name}")
    if not cond:
        fails.append(name)


# ================= 01 電磁波 =================
# sf-2-01a：E1=E0, E2=E0/2
t, d = sp.symbols("t delta", real=True)
E0 = 1
avg = lambda f: sp.integrate(f, (t, 0, 2 * sp.pi)) / (2 * sp.pi)
E1 = E0 * sp.cos(t); E2 = sp.Rational(1, 2) * E0 * sp.cos(t + d)
I = sp.simplify(avg(sp.expand((E1 + E2) ** 2)))
truth("sf-2-01a <E^2>=(5+4cos d)/8", sp.simplify(I - sp.Rational(1, 8) * (5 + 4 * sp.cos(d))) == 0)
truth("sf-2-01a <E1^2>=1/2", sp.simplify(avg(E1 ** 2) - sp.Rational(1, 2)) == 0)
truth("sf-2-01a <E2^2>=1/8", sp.simplify(avg(E2 ** 2) - sp.Rational(1, 8)) == 0)
truth("sf-2-01a 2<E1E2>=cos(d)/2", sp.simplify(avg(2 * E1 * E2) - sp.cos(d) / 2) == 0)
check("sf-2-01a Imax/Imin", 9 / 1, 9); check("sf-2-01a V", (9 - 1) / (9 + 1), 0.8, 1e-9)
check("sf-2-01a V general", 2 * 1 * 0.5 / (1 + 0.25), 0.8, 1e-9)
Ie = sp.simplify(avg(sp.expand((sp.cos(t) + sp.cos(t + d)) ** 2)))
truth("sf-2-01a equal amp: 2cos^2(d/2)", sp.simplify(Ie - 2 * sp.cos(d / 2) ** 2) == 0)
# sf-2-01b
Ld = 1.0 / 2.0e-4; check("sf-2-01b L/d", Ld, 5000, 1e-9)
for m, lo, hi in ((1, 2.0, 3.5), (2, 4.0, 7.0), (3, 6.0, 10.5)):
    check(f"sf-2-01b m={m} violet mm", Ld * m * 400e-9 * 1e3, lo, 1e-6); check(f"sf-2-01b m={m} red mm", Ld * m * 700e-9 * 1e3, hi, 1e-6)
truth("sf-2-01b overlap m>4/3", 700 * 1 <= 400 * 2 and 700 * 2 > 400 * 3)
check("sf-2-01b 6.5mm m=2", 6.5e-3 / (Ld * 2) * 1e9, 650, 1e-6); check("sf-2-01b 6.5mm m=3", 6.5e-3 / (Ld * 3) * 1e9, 433, 0.002)
check("sf-2-01b 6.5mm m=1", 6.5e-3 / Ld * 1e9, 1300, 1e-6); check("sf-2-01b 6.5mm m=4", 6.5e-3 / (Ld * 4) * 1e9, 325, 1e-6)
th = 0.0105; check("sf-2-01b tan-sin rel %", (1 / cos(th) - 1) * 100, 0.0055, 0.1)

# ================= 02 黑體輻射 =================
hn1 = h3 * 660; check("ex2.1 h nu1", hn1, 4.38e-31, 0.002)
check("ex2.1 n=E/h nu1", 0.04 / hn1, 9e28, 0.02)
hn2 = h3 * 5.00e14; check("ex2.1 h nu2 J", hn2, 3.32e-19, 0.002)
check("ex2.1 h nu2 eV (3.32/1.60)", 3.32e-19 / 1.60e-19, 2.08, 0.003)
check("ex2.1 h nu2 eV (4.136e-15)", hev * 5.00e14, 2.07, 0.002)
check("ex2.1 nu2/nu1", 5.00e14 / 660, 7.6e11, 0.005)
check("2-1 nu_c=kT/h at 300K", kB * 300 / h, 6.3e12, 0.01)
x = sp.symbols("x", positive=True)
truth("2-1 h->0 eps->kT", sp.limit(x / (sp.exp(x) - 1), x, 0) == 1)
lam, nu, T, hh, cc, kk = sp.symbols("lambda nu T h c k", positive=True)
unu = 8 * sp.pi * hh / cc ** 3 * nu ** 3 / (sp.exp(hh * nu / (kk * T)) - 1)
ulam = sp.simplify(unu.subs(nu, cc / lam) * cc / lam ** 2)
truth("2-2 u(lambda)", sp.simplify(ulam - 8 * sp.pi * hh * cc / lam ** 5 / (sp.exp(hh * cc / (lam * kk * T)) - 1)) == 0)
truth("2-2 coefficient 8 pi h c / lam^5", sp.simplify(8 * sp.pi * hh / cc ** 3 * cc ** 3 / lam ** 3 * cc / lam ** 2 - 8 * sp.pi * hh * cc / lam ** 5) == 0)
truth("sf-2-02a series 1-x/2", sp.series(x / (sp.exp(x) - 1), x, 0, 2).removeO() == 1 - x / 2)
f = lambda z: exp(z) - 1 - 2 * z
check("sf-2-02a e^1.2-1", exp(1.2) - 1, 2.320, 0.001); check("sf-2-02a e^1.3-1", exp(1.3) - 1, 2.669, 0.001)
check("sf-2-02a f(1.25)", f(1.25), -0.010, 0.05); check("sf-2-02a f(1.26)", f(1.26), 0.005, 0.1)
root = float(sp.nsolve(sp.exp(x) - 1 - 2 * x, x, 1.25)); check("sf-2-02a root", root, 1.256, 0.0005)
check("sf-2-02a interp", 1.25 + 0.01 * 0.010 / 0.015, 1.256, 0.001)
nu02 = root * kB * 1500 / h; check("sf-2-02a nu", nu02, 3.93e13, 0.003); check("sf-2-02a lambda um", c / nu02 * 1e6, 7.6, 0.01)
check("sf-2-02a back-sub 1.256/(e^1.256-1)", 1.256 / (exp(1.256) - 1), 0.500, 0.002)
truth("sf-2-02b int x^3/(e^x-1)=pi^4/15", abs(float(sp.Integral(x ** 3 / (sp.exp(x) - 1), (x, 0, sp.oo)).evalf()) - pi ** 4 / 15) < 1e-9)
check("sf-2-02b pi^4/15", pi ** 4 / 15, 6.49, 0.001); check("sf-2-02b 2^4", 2 ** 4, 16, 1e-9)
check("sf-2-02b e^5", exp(5), 148.4, 0.001); check("sf-2-02b ratio high", (exp(10) - 1) / (exp(5) - 1), 149, 0.003)

# ================= 03 光電效應 =================
Ep = 1.24e-6 / 350e-9; check("ex2.2 Ep eV", Ep, 3.543, 0.0005)
check("ex2.2 KEmax", Ep - 2.2, 1.3, 0.04); check("ex2.2 P=IA", 1.00 * 1.00e-4, 1.00e-4, 1e-9)
check("ex2.2 Ep J", Ep * qe, 5.68e-19, 0.002); check("ex2.2 n_p", 1e-4 / (Ep * qe), 1.76e14, 0.003)
check("ex2.2 n_e", 0.0050 * 1e-4 / (Ep * qe), 8.8e11, 0.005)
check("107-6 lambda0", HC / 2.28, 544, 0.001); check("107-6 410 eV", HC / 410, 3.02, 0.002)
check("107-6 KE", HC / 410 - 2.28, 0.74, 0.01); check("107-6 KE J", 0.74 * qe, 1.2e-19, 0.02)
check("107-6 560 eV", HC / 560, 2.21, 0.002); truth("107-6 560 no emission", HC / 560 < 2.28)
check("2-3 example KE", 3.0 - 2.3, 0.7, 1e-9); check("2-3 example KE doubled", 6.0 - 2.3, 3.7, 1e-9)
check("2-5 eV", 1.240e-6 / 700e-9, 1.77, 0.002); check("2-5 J", 1.771 * qe, 2.84e-19, 0.002)
check("2-5 J SI", h * c / 7.00e-7, 2.84e-19, 0.002)
check("2-6 lambda", 1.240e-6 / 1e8, 1.24e-14, 1e-6); check("2-6 nu", 1e8 / hev, 2.42e22, 0.002)
check("2-7 h nu", h * 8.80e5, 5.83e-28, 0.001); check("2-7 N/t", 1e3 / (h * 8.80e5), 1.72e30, 0.003)
check("2-8 E", h * c3 / 600e-9, 3.31e-19, 0.002); check("2-8 N", 1.0e-18 / (h * c3 / 600e-9), 3.0, 0.01)
E29 = h3 * 5.0e14; check("2-9 h nu", E29, 3.3e-19, 0.01); check("2-9 h nu 4sf", E29, 3.315e-19, 0.001)
check("2-9 flux", 1.4e3 / E29, 4.2e21, 0.01); check("2-9 sphere area", 4 * pi * (1.5e11) ** 2, 2.83e23, 0.002)
P9 = 1.4e3 * 4 * pi * (1.5e11) ** 2; check("2-9 P", P9, 4.0e26, 0.02); check("2-9 P 3sf", P9, 3.96e26, 0.002)
check("2-9 N/t", P9 / E29, 1.2e45, 0.01); check("2-9 n", 1.4e3 / E29 / 3.0e8, 1.4e13, 0.01)
check("2-9 flux 3sf", 1.4e3 / E29, 4.22e21, 0.002); check("2-15 Ne 3sf", 0.0010 * 1.5e-3 / (HC / 400 * qe), 3.02e12, 0.002)
check("sf-2-04a R 3sf", 1.0e-13 / (h * c / 500e-9), 2.52e5, 0.002); check("sf-2-05b Pout 3sf", 0.90 * 0.81, 0.729, 1e-6)
check("sf-2-05b Ebar 3sf", 0.405 / (log(10) - 0.9) * 30, 8.66, 0.002)
check("2-10 E pulse", 0.50 * 20e-3, 1.0e-2, 1e-9); check("2-10 E photon", h * c3 / 632e-9, 3.15e-19, 0.002)
check("2-10 N", 1.0e-2 / (h * c3 / 632e-9), 3.2e16, 0.01)
phiW = HC / 230; check("2-11 phi", phiW, 5.39, 0.001); check("2-11 h nu", 1.5 + phiW, 6.89, 0.001)
check("2-11 lambda", HC / (1.5 + phiW), 180, 0.002)
check("2-12 nu-nu0", 1.5e15 - 1.1e15, 0.40e15, 1e-6); check("2-12 KE", hev * 0.40e15, 1.65, 0.005)
check("2-13 lambda max nm", 1.240e-6 / 2.3 * 1e9, 539, 0.001); check("2-13 200nm eV", HC / 200, 6.2, 1e-6)
check("2-13 KE", HC / 200 - 2.3, 3.9, 1e-6)
check("2-14 KE", HC / 200 - 4.7, 1.5, 1e-6)
Ep15 = HC / 400 * qe; check("2-15 Ep eV", HC / 400, 3.10, 1e-6); check("2-15 Ep J", Ep15, 4.97e-19, 0.002)
Np = 1.5e-3 / Ep15; check("2-15 Np", Np, 3.0e15, 0.01); check("2-15 Np 3sf", Np, 3.02e15, 0.002)
check("2-15 Ne", 0.0010 * Np, 3.0e12, 0.01); check("2-15 I", 0.0010 * Np * qe, 4.8e-7, 0.01)
check("2-16 KE", HC / 400 - 2.50, 0.60, 1e-6); check("2-16 KE/mc2", 0.60 / 5.11e5, 1.2e-6, 0.03)
check("2-16 v^2", 2 * 0.60 * qe / me, 2.11e11, 0.002); check("2-16 v", sqrt(2 * 0.60 * qe / me), 4.6e5, 0.01)
h17 = (1.97 - 0.52) / 3.5e14; check("2-17 h eVs", h17, 4.14e-15, 0.001); check("2-17 h Js", h17 * qe, 6.6e-34, 0.01)
check("2-17 phi", 4.14e-15 * 8.5e14 - 0.52, 3.0, 0.002); check("2-17 h nu1", 4.14e-15 * 8.5e14, 3.52, 0.001)
nu18 = 3.00e8 / 175e-9; check("2-18 nu", nu18, 1.71e15, 0.003); check("2-18 h eVs", 7.1 / nu18, 4.14e-15, 0.002)
check("2-18 h Js", 4.14e-15 * 1.60e-19, 6.6e-34, 0.01)
pe, m_, cc2 = sp.symbols("p_e m c", positive=True)
truth("2-19 expansion -> 2 p c m c^2 = 0", sp.expand((pe * cc2 + m_ * cc2 ** 2) ** 2 - (pe * cc2) ** 2 - (m_ * cc2 ** 2) ** 2) == 2 * pe * m_ * cc2 ** 3)
KE3 = HC / 400 - 2.2; check("sf-2-03a KEmax", KE3, 0.90, 1e-6)
check("sf-2-03a (b) hi", KE3 + 2.0, 2.9, 1e-6); check("sf-2-03a (c) hi", KE3 - 0.50, 0.40, 1e-6)
A = pi * (1.0e-10) ** 2; check("sf-2-03b A", A, 3.14e-20, 0.001)
check("sf-2-03b phi J", 2.2 * qe, 3.52e-19, 0.002); check("sf-2-03b IA", 1.0e-3 * A, 3.14e-23, 0.001)
tcl = 2.2 * qe / (1.0e-3 * A); check("sf-2-03b t", tcl, 1.1e4, 0.03)
flux = 1.0e-3 / Ep15; check("sf-2-03b flux", flux, 2.0e15, 0.01)
rate = flux * A; check("sf-2-03b per-atom rate", rate, 6.3e-5, 0.01); check("sf-2-03b wait s", 1 / rate, 1.6e4, 0.02)
check("sf-2-03b wait h", 1 / rate / 3600, 4.4, 0.01); check("sf-2-03b ratio", (1 / rate) / tcl, 3.10 / 2.2, 0.002)

# ================= 04 光是什麼 =================
check("2-4 2 eV in J", 2 * qe, 3.2e-19, 0.002); check("2-4 N/t for 1 W", 1 / (2 * qe), 3e18, 0.05)
hn4 = h * c / 500e-9; check("sf-2-04a h nu", hn4, 3.97e-19, 0.002)
t4 = 1.5 / c; check("sf-2-04a t", t4, 5.0e-9, 0.002); check("sf-2-04a P(mu=1)", hn4 / t4, 7.9e-11, 0.01)
check("sf-2-04a P(n>=2|mu=1)", 1 - 2 / E, 0.26, 0.02)
R = 1.0e-13 / hn4; check("sf-2-04a R", R, 2.5e5, 0.01); mu = R * t4; check("sf-2-04a mu", mu, 1.3e-3, 0.04)
check("sf-2-04a mu 3sf", mu, 1.26e-3, 0.002)
check("sf-2-04a P(n>=2) approx", mu ** 2 / 2, 7.9e-7, 0.01); check("sf-2-04a P(n>=2) exact", 1 - exp(-mu) * (1 + mu), 7.9e-7, 0.01)
mm = sp.symbols("mu")
truth("sf-2-04a series e^-mu(1+mu)=1-mu^2/2+..", sp.series(sp.exp(-mm) * (1 + mm), mm, 0, 3).removeO() == 1 - mm ** 2 / 2)
check("sf-2-04a spacing m", c / R, 1.2e3, 0.01); check("sf-2-04a L/mu", 1.5 / mu, 1.2e3, 0.01)
dd = sp.symbols("delta", real=True)
Ib = sp.simplify(avg(sp.expand((sp.cos(t) + sp.cos(t + dd)) ** 2)))
truth("sf-2-04b <E^2>=1+cos d (E0=1)", sp.simplify(Ib - (1 + sp.cos(dd))) == 0)
check("sf-2-04b I1 count", 10000 / 4, 2500, 1e-9)
check("sf-2-04b pi/3", 10000 * cos(pi / 6) ** 2, 7500, 1e-9); check("sf-2-04b pi", 10000 * cos(pi / 2) ** 2 + 1, 1, 1e-9)

# ================= 05 X 射線 =================
lm = 1.24e-6 / 5.00e4; check("ex2.3 lambda min", lm, 2.48e-11, 1e-6); check("ex2.3 nu max", 3.00e8 / lm, 1.21e19, 0.002)
check("2-20 V", 1.24e-6 / 30e-12, 4.1e4, 0.01)
check("2-21 nu", 1.0e4 / hev, 2.4e18, 0.01); check("2-21 lambda nm", HC / 1.0e4, 0.124, 1e-6)
g = 1 + 50 / me_c2; check("sf-2-05a gamma", g, 1.098, 0.0005)
check("sf-2-05a 1-1/g^2", 1 - 1 / g ** 2, 0.170, 0.003); check("sf-2-05a beta", sqrt(1 - 1 / g ** 2), 0.413, 0.002)
bcl = sqrt(100 / me_c2); check("sf-2-05a beta classical", bcl, 0.442, 0.002)
check("sf-2-05a overestimate", bcl / sqrt(1 - 1 / g ** 2), 1.07, 0.003)
pc = sqrt(50 ** 2 + 2 * 50 * me_c2); check("sf-2-05a pc^2", 50 ** 2 + 2 * 50 * me_c2, 53600, 1e-9); check("sf-2-05a pc", pc, 232, 0.003)
check("sf-2-05a pc via gamma beta", g * sqrt(1 - 1 / g ** 2) * me_c2, 232, 0.003)
check("sf-2-05a photon share", 50 / pc, 0.22, 0.02); check("sf-2-05a p nucleus min", pc - 50, 182, 0.005)
check("sf-2-05a p nucleus max", pc + 50, 282, 0.005)
KM = 0.282 ** 2 / (2 * 1.71e5); check("sf-2-05a KE_M MeV", KM, 2.3e-7, 0.02); check("sf-2-05a KE_M eV", KM * 1e6, 0.23, 0.02)
check("sf-2-05a fraction", 0.23 / 50000, 5e-6, 0.1)
check("sf-2-05b P", 1.0e-2 * 3.0e4, 300, 1e-9); PX = 0.0030 * 300; check("sf-2-05b PX", PX, 0.90, 1e-9)
check("sf-2-05b eV J", 3.0e4 * qe, 4.81e-15, 0.001); Nmin = PX / (3.0e4 * qe); check("sf-2-05b Nmin", Nmin, 1.9e14, 0.02)
u, uc = sp.symbols("u u_c", positive=True)
truth("sf-2-05b int(1-u)=1/2", sp.integrate(1 - u, (u, 0, 1)) == sp.Rational(1, 2))
truth("sf-2-05b int (1-u)/u", sp.simplify(sp.integrate((1 - u) / u, (u, uc, 1)) - (sp.log(1 / uc) - (1 - uc))) == 0)
num = float(sp.integrate(1 - u, (u, 0.1, 1))); check("sf-2-05b num 0.405", num, 0.405, 1e-6)
check("sf-2-05b Pout/PX", num / 0.5, 0.81, 1e-6); Pout = PX * num / 0.5; check("sf-2-05b Pout", Pout, 0.73, 0.005)
den = log(10) - 0.9; check("sf-2-05b den", den, 1.403, 0.0005); check("sf-2-05b Ebar/hnumax", num / den, 0.289, 0.002)
Eb = num / den * 30; check("sf-2-05b Ebar keV", Eb, 8.7, 0.01); check("sf-2-05b Ebar J", Eb * 1e3 * qe, 1.39e-15, 0.003)
N5 = Pout / (Eb * 1e3 * qe); check("sf-2-05b N", N5, 5.3e14, 0.01); check("sf-2-05b N/Nmin", N5 / Nmin, 2.8, 0.01)
check("sf-2-05b heat W", 300 - Pout, 299, 0.005)

# ================= 06 X 射線繞射 =================
check("2-22 sin28.4", sin(radians(28.4)), 0.476, 0.001); d22 = 0.30 / (2 * sin(radians(28.4)))
check("2-22 d", d22, 0.315, 0.002); check("2-22 n=2 sin", 2 * 0.30 / (2 * d22), 0.952, 0.001)
check("2-23 sin", 0.030 / 0.600, 0.050, 1e-9); check("2-23 theta", degrees(asin(0.050)), 2.9, 0.02)
check("2-23 small-angle", 0.050 * 180 / pi, 2.9, 0.02)
a3 = (3.82 + 5.89) * 1e-26 / (2 * 2.16e3); check("2-24 a^3", a3, 2.25e-29, 0.002)
check("2-24 9.71/4.32", 9.71e-26 / 4.32e3, 2.25e-29, 0.002); check("2-24 a", a3 ** (1 / 3), 2.82e-10, 0.002)
check("2-24 22.5^(1/3)", 22.5 ** (1 / 3), 2.82, 0.002)
check("sf-2-06a sin10", sin(radians(10)), 0.1736, 0.0005); l1 = 2 * 282 * sin(radians(10.0))
for n, w in ((1, 97.9), (2, 49.0), (3, 32.6), (4, 24.5)):
    check(f"sf-2-06a lambda_{n} pm", l1 / n, w, 0.002)
lmn = 1.24e-6 / 3.0e4 * 1e12; check("sf-2-06a lambda_min pm", lmn, 41.3, 0.001)
truth("sf-2-06a n=1,2 in, n=3 out", l1 > lmn and l1 / 2 > lmn and l1 / 3 < lmn)
check("sf-2-06a V upper kV", 1.24e-6 / 49.0e-12 / 1e3, 25.3, 0.001); check("sf-2-06a V lower kV", 1.24e-6 / 97.9e-12 / 1e3, 12.7, 0.005)
s1 = 70.93 / 600; check("sf-2-06b sin1", s1, 0.1182, 0.0005); th1 = degrees(asin(s1)); check("sf-2-06b theta1", th1, 6.789, 0.0002)
check("sf-2-06b cos6.79", cos(radians(6.79)), 0.9930, 0.0002)
dt = 0.43 / (600 * cos(radians(th1))); check("sf-2-06b dtheta rad", dt, 7.22e-4, 0.002)
check("sf-2-06b 180/pi", 180 / pi, 57.30, 0.0001); check("sf-2-06b dtheta deg", degrees(dt), 0.0414, 0.002)
check("sf-2-06b exact theta_b", degrees(asin(71.36 / 600)), 6.831, 0.0002)
check("sf-2-06b exact diff", degrees(asin(71.36 / 600)) - th1, 0.0414, 0.003)
s2 = 2 * 70.93 / 600; check("sf-2-06b sin2", s2, 0.2364, 0.0005); th2 = degrees(asin(s2)); check("sf-2-06b theta2", th2, 13.68, 0.0005)
check("sf-2-06b cos13.68", cos(radians(13.68)), 0.9716, 0.0002)
dt2 = 2 * 0.43 / (600 * cos(radians(th2))); check("sf-2-06b dtheta2 rad", dt2, 1.48e-3, 0.005); check("sf-2-06b dtheta2 deg", degrees(dt2), 0.0845, 0.002)
check("sf-2-06b cos ratio", cos(radians(6.79)) / cos(radians(13.68)), 1.02, 0.003)

print()
print("全部通過" if not fails else f"有 {len(fails)} 項不符：{fails}")
sys.exit(1 if fails else 0)
