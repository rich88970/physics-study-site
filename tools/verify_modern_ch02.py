"""近代物理第 2 章（Beiser Particle Properties of Waves）所有數值答案的獨立重算：python tools/verify_modern_ch02.py"""
from math import sqrt, exp, log, sin, cos, tan, atan, atan2, asin, acos, radians, degrees, pi

h = 6.626e-34          # J s
hev = 4.136e-15        # eV s
c = 2.998e8
c3 = 3.00e8
e = 1.602e-19
HC = 1.240e-6          # eV m
lamC = 2.426e-12       # m
me = 0.511             # MeV
kB = 1.381e-23
G = 6.67e-11


def show(k, *v):
    print(f"{k:<14}", *[(f"{x:.5g}" if isinstance(x, float) else x) for x in v])


# ---------- 2.2 黑體 ----------
show("Ex2.1 fork J", 6.63e-34 * 660, "ratio", 0.04 / (6.63e-34 * 660))
E2 = 6.63e-34 * 5.00e14; show("Ex2.1 atom J eV", E2, E2 / 1.60e-19)
# Wien 峰值：x e^x/(e^x-1)=3 (頻率) 與 =5 (波長)
def root(f, a, b):
    for _ in range(200):
        m = (a + b) / 2
        if f(a) * f(m) <= 0: b = m
        else: a = m
    return (a + b) / 2
xnu = root(lambda x: 3 * (1 - exp(-x)) - x, 1, 5); xla = root(lambda x: 5 * (1 - exp(-x)) - x, 1, 8)
show("Wien x_nu x_lam", xnu, xla)
for T in (1200, 1500, 1800):
    show(f"peak nu T={T}", xnu * kB * T / h)
show("Wien b (m K)", h * c / (xla * kB))
show("hnu/kT 5e14 1500K", h * 5e14 / (kB * 1500))

# ---------- 2.3 光電 ----------
lam = 350e-9; Ep = HC / lam; show("Ex2.2 Ep eV", Ep, "KE", 3.5 - 2.2, "J", Ep * e)
npho = 1.00 * 1.00e-4 / 5.68e-19; show("Ex2.2 np ne", npho, 0.005 * npho)
# 107-6 鈉 2.28 eV
for L in (410, 560):
    E = 1240 / L; show(f"107-6 {L}nm", E, "KE", E - 2.28)
show("107-6 cutoff nm", 1240 / 2.28)
show("2-5 eV", 1240 / 700)
show("2-7 photons/s", 1000 / (6.626e-34 * 880e3))
# 2-9
n1 = 1.4e3 / (6.63e-34 * 5.0e14); P = 1.4e3 * 4 * pi * (1.5e11) ** 2
show("2-9 a b c", n1, P, P / (6.63e-34 * 5.0e14), n1 / 3.0e8)
show("2-11 nm", 1240 / (1240 / 230 + 1.5))
show("2-13 nm KE", 1240 / 2.3, 1240 / 200 - 2.3)
show("2-14 V", 1240 / 200 - 4.7)
Np = 1.5e-6 / (6.626e-34 * c / 400e-9); show("2-15 I uA", Np * e * 1e6, "N/s", Np, "1.5mW/E", 1.5e-3 / (HC / 400e-9 * e))
KE = 1240 / 400 - 2.50; show("2-16 V0 v", KE, sqrt(2 * KE * e / 9.109e-31))
hh = (1.97 - 0.52) / (3.5e14); show("2-17 h eVs, J s, phi", hh, hh * e, hh * 8.5e14 - 0.52)
# ---------- 2.5 X 光 ----------
lmin = HC / 5.00e4; show("Ex2.3 lmin nmax", lmin, 3.00e8 / lmin)
show("2-20 V", HC / 30e-12)
show("2-21 nu", 1.0e4 / 4.136e-15, "lam nm", HC / 1e4 * 1e9)
# ---------- 2.6 Bragg ----------
show("2-22 d nm", 0.30 / (2 * sin(radians(28.4))))
show("2-23 deg", degrees(asin(0.030 / (2 * 0.300))))
a = ((3.82e-26 + 5.89e-26) / (2 * 2.16e3)) ** (1 / 3); show("2-24 a m", a)
# ---------- 2.7 Compton ----------
lp = 10.0 + lamC * 1e12 * (1 - cos(radians(45))); show("Ex2.4 a b", lp, 10.0 + 2 * 2.426)
KEm = 6.626e-34 * 3.00e8 / 1e-12 * (1 / 10.0 - 1 / 14.852); show("Ex2.4 KE J keV", KEm, KEm / e / 1e3)
KE7 = 6.626e-34 * (1.5e19 - 1.2e19); show("107-7 KE J keV", KE7, KE7 / e / 1e3)
show("2-26 MeV", sqrt(10 ** 2 + 2 * 10 * 938))
show("2-27 lamC Na", 6.626e-34 / (3.82e-26 * 3.0e8))
show("2-29 pm", 2.2 - 2.426 * (1 - cos(radians(45))))
nu1 = 1 / (1 / 3.0e19 + lamC / c); show("2-31 nu'", nu1)
Ex = (100 + sqrt(100 ** 2 + 4 * 2 * 50 * 511)) / 4; show("2-32 E keV", Ex, "check KEmax", 2 * Ex ** 2 / (511 + 2 * Ex))
cphi = 1 - 511 * (1 / 90 - 1 / 100); show("2-33 deg", degrees(acos(cphi)))
dl = 2.426 * (1 - cos(radians(120))); lp = 80 + dl
th = degrees(atan(sin(radians(120)) / (lp / 80 - cos(radians(120)))))
KE34 = 1240e3 * (1 / 80 - 1 / lp)  # eV, 用 hc=1240 eV nm = 1.240e6 eV pm
show("2-34 dl theta KE eV", dl, th, KE34)
# 2-36
phi = acos(1 - 0.5 / 2.426); px = 1 / 10.0 - cos(phi) / 10.5; py = -sin(phi) / 10.5
p = 6.626e-34 / 1e-12 * sqrt(px ** 2 + py ** 2)
show("2-36 phi p theta", degrees(phi), p, degrees(atan2(py, px)))
# 2-37
t = tan(radians(40)) ** 2; ratio = (1 + 4 * t) / (3 + 4 * t); show("2-37 E' keV phi", 511 * ratio, degrees(acos(1 - (1 / ratio - 1))))
show("2-38 eg E=E0", 2 * 1 / (1 + 2))
# ---------- 2.8 成對產生 ----------
v = 0.5; g = 1 / sqrt(1 - v * v); show("Ex2.6 p1-p2 p1+p2", 2 * g * me * v, 2 * g * me, "E1 E2", g * me * (1 + v), g * me * (1 - v))
# 107-8 / 2-40 正子 KE=2.0 MeV 撞靜止電子
Ep_ = 2.0 + me; pc = sqrt(Ep_ ** 2 - me ** 2); Et = Ep_ + me
show("107-8 pc Etot", pc, Et, "E1 E2", (Et + pc) / 2, (Et - pc) / 2)
ce = (pc / 2) / (Et / 2); show("107-8 sym E th", Et / 2, degrees(acos(ce)))
Ep_ = 3.0 + me; pc = sqrt(Ep_ ** 2 - me ** 2); Et = Ep_ + me; show("KE3 var E1 E2", (Et + pc) / 2, (Et - pc) / 2, pc)
show("2-39 lam pm", HC / 1.511e6 * 1e12)
show("2-42 b MeV", 2 * me * (1 + me / 938.3))
# 吸收
show("Ex2.7 a b", exp(-4.9 * 0.10), log(100) / 4.9)
show("107-9 mm", log(2) / 78 * 1e3)
show("2-43 x1/10", log(10))
show("2-44 err %", (0.1 - (1 - exp(-0.1))) / (1 - exp(-0.1)) * 100, "exact abs", 1 - exp(-0.1))
show("2-46 0.5 5m", exp(-5e-3 * 0.5), exp(-5e-3 * 5))
show("2-47 cm", 10e-3 * 52 / 4.9 * 100)
show("2-48 I/I0", exp(-4.7e4 * 1e-4))
show("2-49 mm", log(2) / 4.7e4 * 1e3)
show("2-50 mm", 10 * 5.8 / 1.1)
# ---------- 2.9 重力 ----------
show("Ex2.8 Hz", 9.8 * 22.5 * 7.3e14 / (3.0e8) ** 2)
r = G * 2.0e30 / (c3 ** 2 * 7.0e8); show("2-51 ratio dl pm", r, 500e-9 * r * 1e12)
r = G * 2.0e30 / (c3 ** 2 * 6.4e6); show("2-52 ratio dl nm", r, 500 * r)
E = 14.4e3 * e; M = 9.5e-26; show("2-53a eV", E ** 2 / (2 * M * c3 ** 2) / e)
show("2-53b eV", E ** 2 / (2 * 1.0e-3 * c3 ** 2) / e)
nu = 14.4e3 / 4.136e-15; show("2-53c nu dnu", nu, 9.8 * 20 * nu / c3 ** 2)
show("2-54 mm", 2 * G * 5.98e24 / c3 ** 2 * 1e3)
show("sun Rs km", 2 * G * 2.0e30 / c3 ** 2 / 1e3)
# ---------- 115-2 能量比較（典型值） ----------
show("pair thr MeV", 2 * me, "lam pm", HC / 1.022e6 * 1e12)
# 104 答案卷：1 MeV 光子被質子散射 45°
Eq = 1 / (1 / 1.0 + (1 - cos(radians(45))) / 938.3); show("var p45 E' KE", Eq, (1 - Eq) * 1e6, "eV")
# 變化題：Compton 1 MeV 光子 180°（電子）
Eb = 1 / (1 / 1.0 + 2 / me); show("var 180 E' KE", Eb, 1 - Eb)
# 變化題 光電：鉀 2.2 eV, 400 nm
show("var K 400", 1240 / 400 - 2.2)
# 變化題 X 光 30 kV
show("var 30kV pm", HC / 3e4 * 1e12)
# 變化題 Bragg NaCl a=0.282 nm, λ=0.154 nm 第二階
show("var bragg n2 deg", degrees(asin(2 * 0.154 / (2 * 0.282))))
# 變化題 鉛 μ=78：減到 1/8
show("var 1/8 mm", 3 * log(2) / 78 * 1e3)
# 變化題 白矮星 Δλ 600nm, M=1.0e30 R=5e6
show("var wd dl nm", 600 * G * 1.0e30 / (c3 ** 2 * 5e6))
# ---------- 考前衝刺變化題 ----------
show("var1 K 400 600", 1240 / 400 - 2.2, 1240 / 600, "cut nm", 1240 / 2.2)
hh = (1.83 - 0.80) / (c3 * (1 / 300e-9 - 1 / 400e-9)); show("var2 h phi", hh, hh * c3 / 300e-9 - 1.83)
nup = 1 / (1 / 1.5e19 + lamC / c3); show("var3 nu' KE keV", nup, 6.626e-34 * (1.5e19 - nup) / e / 1e3)
show("var7 1/8 1% mm", 3 * log(2) / 78 * 1e3, log(100) / 78 * 1e3)
show("var8 30kV 60kV pm", HC / 3e4 * 1e12, HC / 6e4 * 1e12)
for n in (1, 2, 3, 4):
    s_ = n * 0.154 / (2 * 0.282); show(f"var9 n={n}", s_, degrees(asin(s_)) if s_ <= 1 else "none")
show("var12 Sun 6000K nu_max lam_max nm", xnu * kB * 6000 / h, 2.898e-3 / 6000 * 1e9)
show("var11 dl/l 500nm 0.1nm", 2 * 2.426e-12 / 500e-9, 2 * 2.426e-12 / 0.1e-9)
# ---------- 正文中的驗算數字 ----------
show("Ex2.4c book(14.9) keV", 6.626e-34 * 3.00e8 / 1e-12 * (1 / 10.0 - 1 / 14.9) / e / 1e3, "E_in keV", 1240 / 0.0100 / 1e3)
show("2-35 check Ex2.4", 2 * 124 ** 2 / (511 + 248))
KE36 = 1.24e6 * (1 / 10 - 1 / 10.5); pc36 = sqrt(KE36 ** 2 + 2 * KE36 * 511e3); show("2-36 KE eV pc keV p", KE36, pc36 / 1e3, pc36 * e / c3)
pc37 = sqrt(176 ** 2 + 2 * 176 * 511); show("2-37 transverse", 335.3 * sin(radians(61.58)), pc37 * sin(radians(40)))
lam32 = 1.24e6 / 140.8e3; show("2-32 check E' keV", 1.24e6 / (lam32 + 2 * 2.426) / 1e3)
show("107-7 dlambda pm", c * (1 / 1.2e19 - 1 / 1.5e19) * 1e12, "2lamC", 2 * 2.426)
show("107-8 Mc2 E1E2", sqrt(3.022 ** 2 - 2.458 ** 2), 2.740 * 0.282)
show("Ex2.6 ratio", 0.885 / 0.295, 0.511 * sqrt(3), 0.511 / sqrt(3))
show("2-34 E_in keV frac", 1240 / 0.080 / 1e3, 674 / 15500)
show("2-53 grav frac dE eV", 9.8 * 20 / c3 ** 2, 9.8 * 20 / c3 ** 2 * 14.4e3)
show("Ex2.8 frac", 9.8 * 22.5 / c3 ** 2)
show("2-29 photon MeV", 1.24 / 1.5)
show("var4 lamC_p fm dl fm ratio", 6.626e-34 / (1.673e-27 * c3) * 1e15, 1.32 * (1 - cos(radians(45))), 0.387 / 1240)
show("var5 check", 4 * 3.748 * 0.274, 4.022 ** 2 - 3.474 ** 2)
show("var10 ratio Rs m", G * 1.0e30 / (c3 ** 2 * 5.0e6), 2 * G * 1.0e30 / c3 ** 2)
show("var12 c/nu_max nm", c / (xnu * kB * 6000 / h) * 1e9)
show("fig blackbody ratio 4e14 1500K", (exp(h * 4e14 / (kB * 1500)) - 1) / (h * 4e14 / (kB * 1500)))
show("fig bragg ratios", *[2 * 0.315 * sin(radians(a)) / 0.30 for a in (15, 28.4, 50, 72.2)])
show("fig annih KE->inf E2", me / 2)
# 107-7／習題 2-30：兩位有效數字的範圍內，Δλ 最小可到多少（< 2λC 才可能）
show("2-30 dl range pm", c * (1 / 1.25e19 - 1 / 1.45e19) * 1e12, c * (1 / 1.15e19 - 1 / 1.55e19) * 1e12, "2lamC", 2 * 2.426)
x01 = h * 0.1e14 / (kB * 1500); show("fig blackbody ratio 0.1e14 1500K", (exp(x01) - 1) / x01)
