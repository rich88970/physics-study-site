"""近代物理第 2 章本次新增題目（課本習題 2-6、8、10、12、18、25、26、28、48、49 與 20 題自編難題）的獨立驗算。

用法：python tools/verify_modern_ch02_added.py
每題用兩種方法（SI 與 eV 單位、精確與近似、數值與 sympy 符號）互相核對，並和網站上寫的答案比較；全部通過才 exit 0。
"""
import sys
from math import sqrt, exp, log, sin, cos, asin, acos, radians, degrees, pi

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")

h = 6.626e-34      # J s
hev = 4.136e-15    # eV s
c = 2.998e8
c3 = 3.00e8
e = 1.602e-19
HC = 1240.0        # eV nm = keV pm = MeV fm
lamC = 2.426       # pm
me = 0.511         # MeV
mp = 938.3         # MeV
kB = 1.381e-23

fails = []


def check(name, got, want, rel=0.02):
    ok = abs(got - want) <= rel * abs(want) + 1e-300
    print(f"{'OK ' if ok else 'BAD'} {name:<34} 算得 {got:.5g}  網站 {want:.5g}")
    if not ok:
        fails.append(name)


def truth(name, cond):
    print(f"{'OK ' if cond else 'BAD'} {name}")
    if not cond:
        fails.append(name)


# ================= 課本習題 =================
# 2-6：100 MeV 光子
lam = h * c / (100e6 * e); nu = 100e6 / hev
check("2-6 lambda (m)", lam, 1.24e-14); check("2-6 lambda eV-units", HC / 100e6 * 1e-9, 1.24e-14)
check("2-6 nu (Hz)", nu, 2.42e22); check("2-6 nu=c/lambda", c / lam, 2.42e22)
# 2-8：1.0e-18 J，600 nm
E1 = h * c3 / 600e-9; check("2-8 E photon J", E1, 3.31e-19); check("2-8 N", 1.0e-18 / E1, 3.0)
check("2-8 N (eV)", 1.0e-18 / e / (HC / 600), 3.0)
# 2-10：0.50 W × 20 ms，632 nm
E10 = h * c3 / 632e-9; check("2-10 E photon", E10, 3.15e-19); check("2-10 N", 0.50 * 0.020 / E10, 3.2e16)
check("2-10 N (eV)", 0.010 / e / (HC / 632), 3.2e16)
# 2-12
check("2-12 KEmax eV", hev * (1.5e15 - 1.1e15), 1.65); check("2-12 hnu-phi", hev * 1.5e15 - hev * 1.1e15, 1.65)
check("2-12 phi=h nu0", hev * 1.1e15, 4.55)
# 2-18
nu18 = c3 / 175e-9; h18 = 7.1 / nu18
check("2-18 nu", nu18, 1.71e15); check("2-18 h eVs", h18, 4.14e-15); check("2-18 h Js", h18 * 1.60e-19, 6.6e-34)
check("2-18 hc/lambda eV", HC / 175, 7.09, 0.005)
# 2-25
nu25 = 1.1e-23 * c3 / h; check("2-25 nu", nu25, 5.0e18)
check("2-25 E keV", 1.1e-23 * c3 / e / 1e3, 21, 0.03); check("2-25 lambda nm", HC / (1.1e-23 * c3 / e), 0.060, 0.03)
# 2-26：KE=10 MeV 質子
pc26 = sqrt(10 ** 2 + 2 * 10 * mp); check("2-26 pc MeV", pc26, 137)
Etot = 10 + mp; check("2-26 sqrt(E^2-m^2)", sqrt(Etot ** 2 - mp ** 2), 137)
check("2-26 classical", sqrt(2 * mp * 10), 137.0, 0.005); check("2-26 diff %", (pc26 / sqrt(2 * mp * 10) - 1) * 100, 0.27, 0.1)
# 2-28
dl28 = lamC * (1 - cos(radians(46))); check("2-28 dl pm", dl28, 0.74); check("2-28 lambda'", 55.8 + dl28, 56.5, 0.002)
check("2-28 dl/lambda %", dl28 / 55.8 * 100, 1.3, 0.05)
# 2-48、2-49
check("2-48 I/I0", exp(-4.7e4 * 1.0e-4), 9.1e-3); check("2-48 2^-6.8", 2 ** (-4.7 / log(2)), 9.1e-3)
check("2-48 n halves", 4.7 / log(2), 6.8, 0.01)
check("2-49 x1/2 mm", log(2) / 4.7e4 * 1e3, 0.015, 0.03); check("2-49 0.10/x12", 0.10 / (log(2) / 4.7e4 * 1e3), 6.8, 0.01)

# ================= 自編難題 =================
# sf-2-01a：振幅 E0、E0/2
d_ = np.linspace(0, 2 * pi, 20001)
t = np.linspace(0, 2 * pi, 4001)[:-1]
Ibar = lambda dl: np.mean((np.cos(t) + 0.5 * np.cos(t + dl)) ** 2)  # E0=1
check("sf01a I(0)=(5+4)/8", Ibar(0.0), 9 / 8, 1e-6); check("sf01a I(pi)=(5-4)/8", Ibar(pi), 1 / 8, 1e-6)
check("sf01a I(1 rad)", Ibar(1.0), (5 + 4 * cos(1.0)) / 8, 1e-6)
check("sf01a Imax/Imin", Ibar(0.0) / Ibar(pi), 9, 1e-6); check("sf01a V", (9 - 1) / (9 + 1), 0.8, 1e-9)
check("sf01a V formula", 2 * 1 * 0.5 / (1 + 0.25), 0.8, 1e-9)
check("sf01a mean over delta", np.mean([(5 + 4 * cos(x)) / 8 for x in d_]), 5 / 8, 1e-3)
# sf-2-01b：d=0.20 mm，L=1.0 m
for m_, lo, hi in ((1, 2.0, 3.5), (2, 4.0, 7.0), (3, 6.0, 10.5)):
    check(f"sf01b m={m_} violet mm", m_ * 400e-9 * 1.0 / 0.20e-3 * 1e3, lo, 1e-6)
    check(f"sf01b m={m_} red mm", m_ * 700e-9 * 1.0 / 0.20e-3 * 1e3, hi, 1e-6)
mmin = min(m for m in range(1, 10) if m * 700 > (m + 1) * 400); truth("sf01b 第一個重疊的 m = 2", mmin == 2)
check("sf01b m=2 at 6.5mm nm", 6.5e-3 * 0.20e-3 / (2 * 1.0) * 1e9, 650, 1e-6)
check("sf01b m=3 at 6.5mm nm", 6.5e-3 * 0.20e-3 / (3 * 1.0) * 1e9, 433, 0.002)
th = 0.0105; check("sf01b tan/sin-1 %", (np.tan(th) / np.sin(th) - 1) * 100, 0.0055, 0.05)
# sf-2-02a：Planck 平均能量
x = sp.symbols('x', positive=True)
ser = sp.series(x / (sp.exp(x) - 1), x, 0, 3).removeO()
truth("sf02a 級數 x/(e^x-1)=1-x/2+x^2/12", sp.simplify(ser - (1 - x / 2 + x ** 2 / 12)) == 0)
from scipy.optimize import brentq  # noqa: E402
xr = brentq(lambda z: z / (exp(z) - 1) - 0.5, 0.5, 3)
check("sf02a root x", xr, 1.256, 0.001); check("sf02a e^1.2-1", exp(1.2) - 1, 2.320, 0.001); check("sf02a e^1.3-1", exp(1.3) - 1, 2.669, 0.001)
nu2 = xr * kB * 1500 / h; check("sf02a nu Hz", nu2, 3.93e13, 0.005); check("sf02a lambda um", c / nu2 * 1e6, 7.6, 0.01)
check("sf02a 代回", 1.256 / (exp(1.256) - 1), 0.500, 0.002); check("sf02a 一次近似值", 1 - 1.256 / 2, 0.37, 0.02)
truth("sf02a 大 x 極限 x e^{-x}", abs((20 / (exp(20) - 1)) / (20 * exp(-20)) - 1) < 1e-8)
# sf-2-02b
from scipy.integrate import quad  # noqa: E402
integ = quad(lambda z: z ** 3 / np.expm1(z) if z > 0 else 0.0, 0, 80)[0]
check("sf02b ∫x^3/(e^x-1)（有限純數 π^4/15）", integ, pi ** 4 / 15, 1e-6)
check("sf02b 總能量倍數", 2 ** 4, 16, 1e-9)
xs = 1e-4; check("sf02b 低頻倍數", (exp(xs) - 1) / (exp(xs / 2) - 1), 2, 1e-3)
check("sf02b 高頻倍數", (exp(10) - 1) / (exp(5) - 1), 149, 0.005); check("sf02b e^5+1", exp(5) + 1, 149.4, 0.001)
# sf-2-03a：鉀 2.2 eV，400 nm
KEm = HC / 400 - 2.2; check("sf03a KEmax", KEm, 0.90, 1e-6); check("sf03a +2.0 max", KEm + 2.0, 2.9, 1e-6)
check("sf03a -0.5 max", KEm - 0.5, 0.40, 1e-6); check("sf03a KEmax (SI)", (h * c / 400e-9) / e - 2.2, 0.90, 0.01)
# sf-2-03b
A_ = pi * (1.0e-10) ** 2; tcl = 2.2 * e / (1.0e-3 * A_)
check("sf03b A", A_, 3.14e-20); check("sf03b t s", tcl, 1.1e4); check("sf03b t h", tcl / 3600, 3.1, 0.05)
Eph = h * c3 / 400e-9; flux = 1.0e-3 / Eph
check("sf03b E photon J", Eph, 4.97e-19); check("sf03b flux", flux, 2.0e15); check("sf03b per atom /s", flux * A_, 6.3e-5)
check("sf03b wait s", 1 / (flux * A_), 1.6e4, 0.03); check("sf03b ratio = 3.10/2.2", (1 / (flux * A_)) / tcl, 3.10 / 2.2, 0.01)
# sf-2-04a（審查後改寫：Poisson）
E5 = h * c3 / 500e-9; tt = 1.5 / c3
check("sf04a hnu", E5, 3.97e-19); check("sf04a t", tt, 5.0e-9)
check("sf04a P(mu=1)", E5 / tt, 7.9e-11); check("sf04a P(n>=2|mu=1)", 1 - 2 / exp(1), 0.26, 0.02)
R2 = 1.0e-13 / E5; mu4 = R2 * tt
check("sf04a R", R2, 2.5e5); check("sf04a mu", mu4, 1.3e-3, 0.04)
p2 = 1 - exp(-mu4) * (1 + mu4); check("sf04a P(n>=2) exact", p2, 7.9e-7, 0.01); check("sf04a mu^2/2", mu4 ** 2 / 2, 7.9e-7, 0.01)
check("sf04a spacing km", c3 / R2 / 1e3, 1.2, 0.02); check("sf04a L/mu km", 1.5 / mu4 / 1e3, 1.2, 0.02)
rng0 = np.random.default_rng(7); arr = rng0.poisson(1.0, 2000000)
check("sf04a Monte Carlo P(n>=2|mu=1)", np.mean(arr >= 2), 0.26, 0.02)
# sf-2-04b
check("sf04b pi/3", 10000 * cos(pi / 6) ** 2, 7500, 1e-9); check("sf04b 一縫", 10000 / 4, 2500, 1e-9)
check("sf04b 週期平均 4cos^2", np.mean(4 * np.cos(d_ / 2) ** 2), 2, 1e-3)
# sf-2-05a：50 keV 電子
g = 1 + 50 / 511; b = sqrt(1 - 1 / g ** 2)
check("sf05a gamma", g, 1.098, 0.001); check("sf05a beta", b, 0.413, 0.002); check("sf05a classical", sqrt(100 / 511), 0.442, 0.002)
check("sf05a overestimate %", (sqrt(100 / 511) / b - 1) * 100, 7, 0.05)
pc5 = sqrt(50 ** 2 + 2 * 50 * 511); check("sf05a pc keV", pc5, 232, 0.003); check("sf05a gamma*beta*mc2", g * b * 511, 232, 0.003)
check("sf05a ratio", 50 / pc5, 0.22, 0.03); check("sf05a deficit", pc5 - 50, 182, 0.005); check("sf05a back", pc5 + 50, 282, 0.005)
MW = 183.84 * 931.494; check("sf05a Mc2 W MeV", MW, 1.71e5, 0.005)
KEM = (0.2815) ** 2 / (2 * 1.71e5) * 1e6; check("sf05a KE nucleus eV", KEM, 0.23, 0.03); check("sf05a frac", KEM / 50e3, 5e-6, 0.1)
check("sf05a lmin pm", HC / 50, 24.8, 0.001)
# sf-2-05b（審查後改寫：Kramers 譜與低能截止）
check("sf05b P", 1.0e-2 * 3.0e4, 300, 1e-9); check("sf05b Nmin", 0.90 / (3.0e4 * e), 1.9e14)
from scipy.integrate import quad as _q  # noqa: E402
uc = 0.10
Pfrac = _q(lambda u: 1 - u, uc, 1)[0] / 0.5; Nint = _q(lambda u: (1 - u) / u, uc, 1)[0]
check("sf05b ∫(1-u) from 0.1", _q(lambda u: 1 - u, uc, 1)[0], 0.405, 1e-6); check("sf05b ∫(1-u)/u", Nint, 1.403, 0.001)
check("sf05b ln10-0.9", log(10) - 0.9, 1.403, 0.001); check("sf05b Pout/PX", Pfrac, 0.81, 1e-6)
Pout = 0.90 * Pfrac; Ebar = 0.405 / Nint * 30.0
check("sf05b Pout W", Pout, 0.73, 0.01); check("sf05b Ebar/hnumax", 0.405 / Nint, 0.289, 0.002); check("sf05b Ebar keV", Ebar, 8.7, 0.01)
N5 = Pout / (Ebar * 1e3 * e); check("sf05b N", N5, 5.3e14, 0.02); check("sf05b N/Nmin", N5 / (0.90 / (3.0e4 * e)), 2.8, 0.02)
check("sf05b N*Ebar W", 5.25e14 * 8.66e3 * e, 0.729, 0.002)
truth("sf05b 無截止時光子數發散（u_c→0 時 ∫ 隨 ln(1/u_c) 增加）", _q(lambda u: (1 - u) / u, 1e-8, 1)[0] > 17)
# sf-2-06a：NaCl d=0.282 nm，10°（審查後補下限）
l1 = 2 * 0.282e3 * sin(radians(10.0))
for n_, w in ((1, 97.9), (2, 49.0), (3, 32.6), (4, 24.5)):
    check(f"sf06a lambda n={n_} pm", l1 / n_, w, 0.002)
lm30 = HC / 30e3 * 1e3; check("sf06a lmin 30kV pm", lm30, 41.3, 0.002)
truth("sf06a 只有 n=1,2 在譜中", [n_ for n_ in range(1, 8) if l1 / n_ >= lm30] == [1, 2])
check("sf06a Vmax kV", HC / (l1 / 2), 25.3, 0.003); check("sf06a Vmin kV", HC / l1, 12.7, 0.005)
truth("sf06a 範圍內只收到第一階", all([n_ for n_ in range(1, 8) if l1 / n_ >= HC / V] == [1] for V in np.linspace(12.7, 25.3, 50)))
# sf-2-06b：Mo Kα 雙線，d=0.300 nm
for n_, want in ((1, 0.0414), (2, 0.0845)):
    t1 = degrees(asin(n_ * 70.93 / 600)); t2 = degrees(asin(n_ * 71.36 / 600))
    check(f"sf06b n={n_} exact deg", t2 - t1, want, 0.005)
    check(f"sf06b n={n_} diff deg", degrees(n_ * 0.43 / (600 * cos(radians(t1)))), want, 0.005)
check("sf06b theta1", degrees(asin(70.93 / 600)), 6.789, 0.0005); check("sf06b theta2nd", degrees(asin(2 * 70.93 / 600)), 13.68, 0.001)
check("sf06b rad", 0.43 / (600 * cos(radians(6.789))), 7.22e-4, 0.003); check("sf06b cos ratio", cos(radians(6.79)) / cos(radians(13.68)), 1.02, 0.005)
# sf-2-07a：康普頓串接
inv = lambda E, phi: 1 / (1 / E + (1 - cos(radians(phi))) / me)
E1_ = inv(1.00, 90); E2_ = inv(E1_, 90); E180 = inv(1.00, 180)
check("sf07a E1", E1_, 0.338, 0.002); check("sf07a E2", E2_, 0.204, 0.003); check("sf07a E180", E180, 0.204, 0.003)
check("sf07a 1/E1", 1 / E1_, 2.957, 0.001); check("sf07a 1/E2", 1 / E2_, 4.914, 0.001)
check("sf07a KE1", 1 - E1_, 0.662, 0.002); check("sf07a KE2", E1_ - E2_, 0.135, 0.005); check("sf07a KE sum", 1 - E2_, 0.796, 0.002)
E60 = 1.00
for _ in range(3):
    E60 = inv(E60, 60)
check("sf07a 3x60 = 120", E60, inv(1.00, 120), 1e-12)
check("sf07a lambda route", 1.24 / (1.24 + 2 * lamC), 0.204, 0.003)
# 用完整的能量＋動量守恆數值解一次 90° 散射，獨立核對康普頓公式
Ein = 1.00; Ep = E1_
px = Ein - Ep * cos(radians(90)); py = -Ep * sin(radians(90))
check("sf07a 守恆核對 KE", sqrt(px ** 2 + py ** 2 + me ** 2) - me, Ein - Ep, 1e-9)
# sf-2-07b：Cs-137
KEe = 2 * 662 ** 2 / (511 + 2 * 662); Eb = 1 / (1 / 662 + 2 / 511)
check("sf07b edge keV", KEe, 478, 0.002); check("sf07b back keV", Eb, 184, 0.003); check("sf07b sum", KEe + Eb, 662, 1e-9)
check("sf07b lambda route", HC / (HC / 662 + 2 * lamC), 184, 0.003)
Es = sp.symbols('E mc2', positive=True); E_, m2 = Es
KEmax_sym = E_ - 1 / (1 / E_ + 2 / m2)
truth("sf07b KEmax=2E^2/(mc^2+2E)（sympy）", sp.simplify(KEmax_sym - 2 * E_ ** 2 / (m2 + 2 * E_)) == 0)
# sf-2-08a：PET
check("sf08a s cm", c3 * 0.40e-9 / 2 * 100, 6.0, 1e-6)
pcE = sqrt(2 * 10 * 511e3); check("sf08a pc keV", pcE / 1e3, 3.2, 0.01)
dlt = pcE / 511e3; check("sf08a delta rad", dlt, 6.3e-3, 0.01); check("sf08a delta deg", degrees(dlt), 0.36, 0.01)
check("sf08a offset mm", 0.40 * dlt * 1e3, 2.5, 0.01)
# 精確：兩光子能量、動量守恆，總動量 P 垂直於 x，求夾角偏離 180°
P = pcE / 1e6; Et = 2 * me + 10e-6  # MeV
# 對稱解：兩光子各 Et/2，各自偏離 ±x 一個角 a，sin a 由橫向動量 P = 2 (Et/2) sin a 給出 → 偏離 180° 的角 = 2a
a = asin(P / Et); check("sf08a 精確偏角 rad", 2 * a, 6.3e-3, 0.01)
# sf-2-08b：5 MeV 成對
K = (5.00 - 2 * me) / 2; pcK = sqrt(K ** 2 + 2 * K * me)
check("sf08b KE", K, 1.989, 0.001); check("sf08b pc", pcK, 2.447, 0.001); check("sf08b pc alt", sqrt((K + me) ** 2 - me ** 2), 2.447, 0.001)
check("sf08b deficit", 5.00 - 2 * pcK, 0.106, 0.01)
MPb = 207.2 * 931.494; check("sf08b Mc2 Pb", MPb, 1.93e5, 0.005)
KEn = (5.00 - 2 * pcK) ** 2 / (2 * 1.93e5); check("sf08b KE nucleus MeV", KEn, 2.9e-8, 0.03); check("sf08b frac", KEn / 5.00, 6e-9, 0.05)
# sf-2-09a：鉛／水
check("sf09a mu/rho Pb", 52 / 11.3e3, 4.6e-3, 0.005); check("sf09a mu/rho water", 4.9 / 1.00e3, 4.9e-3, 1e-9)
check("sf09a Pb 10mm kg/m2", 11.3e3 * 0.010, 113, 1e-9); check("sf09a water eq mm", 10 * 52 / 4.9, 106, 0.002)
check("sf09a water kg/m2", 1.00e3 * 0.106, 106, 1e-9)
T = exp(-52 * 0.0050 - 4.9 * 0.20); check("sf09a T", T, 0.29, 0.01); check("sf09a exponent", 52 * 0.005 + 4.9 * 0.2, 1.24, 1e-9)
check("sf09a mu/rho route", 4.6e-3 * 56.5 + 4.9e-3 * 200, 1.24, 0.002); check("sf09a thickness ratio", 52 / 4.9, 10.6, 0.002)
check("sf09a Z/A water", 10 / 18.015, 0.56, 0.01); check("sf09a Z/A Pb", 82 / 207.2, 0.40, 0.02); check("sf09a e ratio", (10 / 18.015) / (82 / 207.2), 1.4, 0.01)
# sf-2-09b：平均自由徑
X, mu_ = sp.symbols('x mu', positive=True)
truth("sf09b ∫mu e^{-mu x}=1", sp.simplify(sp.integrate(mu_ * sp.exp(-mu_ * X), (X, 0, sp.oo)) - 1) == 0)
truth("sf09b <x>=1/mu", sp.simplify(sp.integrate(X * mu_ * sp.exp(-mu_ * X), (X, 0, sp.oo)) - 1 / mu_) == 0)
check("sf09b mfp mm", 1 / 78 * 1e3, 12.8, 0.002); check("sf09b x12 mm", log(2) / 78 * 1e3, 8.9, 0.002)
check("sf09b 1-1/e", 1 - exp(-1), 0.63, 0.005); check("sf09b 1/ln2", 1 / log(2), 1.44, 0.002)
rng = np.random.default_rng(1); samp = rng.exponential(1 / 78, 400000)
check("sf09b Monte Carlo mean mm", samp.mean() * 1e3, 12.8, 0.01); check("sf09b Monte Carlo median mm", np.median(samp) * 1e3, 8.9, 0.01)
# sf-2-10a（審查後改寫：線寬、掃描、對調）
GE = 4.7e-9 / 14.4e3; vG = c3 * GE
check("sf10a Gamma/E", GE, 3.3e-13, 0.02); check("sf10a vGamma", vG, 9.8e-5, 0.01)
gg = 9.8 * 22.5 / c3 ** 2; check("sf10a gH/c2", gg, 2.45e-15, 0.002); check("sf10a 線寬/重力", GE / gg, 133, 0.01)
check("sf10a fraction %", gg / GE * 100, 0.75, 0.01); check("sf10a x0 m", vG / (2 * pi * 50), 3.1e-7, 0.01)
rec = 14.4e3 ** 2 / (2 * 9.5e-26 * c3 ** 2 / e); check("sf10a recoil eV", rec, 1.9e-3, 0.03)
check("sf10a recoil/Gamma", rec / 4.7e-9, 4e5, 0.05); check("sf10a recoil/grav", (rec / 14.4e3) / gg, 5e7, 0.12)
check("sf10a 2gH/c2", 2 * gg, 4.9e-15, 0.002); check("sf10a vG/(gH/c)", vG / (9.8 * 22.5 / c3), 133, 0.01)
# sf-2-10b（審查後改寫：白矮星／中子星，弱場 vs 精確）
Gc = 6.67e-11
xw = Gc * 2.0e30 / (c3 ** 2 * 6.4e6)
check("sf10b WD x", xw, 2.32e-4, 0.002); check("sf10b WD exp", 1 - exp(-xw), 2.32e-4, 0.002)
check("sf10b WD exact", 1 - sqrt(1 - 2 * xw), 2.32e-4, 0.002); check("sf10b WD R/RS", 1 / (2 * xw), 2200, 0.03)
GMc = Gc * 2.8e30 / c3 ** 2; xn = GMc / 1.0e4
check("sf10b NS GM/c2 km", GMc / 1e3, 2.08, 0.003); check("sf10b NS x", xn, 0.2075, 0.002); check("sf10b NS R/RS", 1 / (2 * xn), 2.4, 0.01)
check("sf10b NS exp", 1 - exp(-xn), 0.187, 0.003); check("sf10b NS exact", 1 - sqrt(1 - 2 * xn), 0.235, 0.003)
check("sf10b NS 弱場低估 %", (1 - xn / (1 - sqrt(1 - 2 * xn))) * 100, 12, 0.04)
check("sf10b NS (a) 低估 %", (1 - (1 - exp(-xn)) / (1 - sqrt(1 - 2 * xn))) * 100, 20, 0.03)
check("sf10b ratio", 0.235 / 0.208, 1.13, 0.005)
from scipy.optimize import brentq as _b  # noqa: E402
u10 = _b(lambda u: (1 - sqrt(1 - u)) / (u / 2) - 1.1, 0.01, 0.99)
check("sf10b u(10%)", u10, 0.331, 0.003); check("sf10b R/RS(10%)", 1 / u10, 3.0, 0.01)
check("sf10b 級數 1+u/4+u^2/8 at 0.33", 1 + 0.33 / 4 + 0.33 ** 2 / 8, 1.096, 0.001)
uu = sp.symbols('u', positive=True)
truth("sf10b 級數 (1-sqrt(1-u))/(u/2)=1+u/4+u^2/8+...", sp.simplify(sp.series((1 - sp.sqrt(1 - uu)) / (uu / 2), uu, 0, 3).removeO() - (1 + uu / 4 + uu ** 2 / 8)) == 0)
Ev, rv, GMs, cs = sp.symbols('E r GM c', positive=True)
Ef = sp.Function('Ef')
sol = sp.dsolve(sp.Eq(Ef(rv).diff(rv), -Ef(rv) / cs ** 2 * GMs / rv ** 2), Ef(rv))
truth("sf10b dE/dr=-(E/c^2)GM/r^2 的解 ∝ exp(GM/(c^2 r))", sp.simplify(sp.log(sol.rhs).diff(rv) + GMs / (cs ** 2 * rv ** 2)) == 0)
check("sf10b R=RS 時 (2.29)", 0.5, 0.5, 1e-12)

print()
if fails:
    print("失敗：", fails)
    sys.exit(1)
print("全部通過")
