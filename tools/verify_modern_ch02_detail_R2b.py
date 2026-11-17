"""近代物理第 2 章 §2.7–§2.9（07-compton、08-pair-production、09-absorption、10-gravity）詳解改寫的數值驗算，
以及 7.4「老師指定必考：光電效應與康普頓效應的差異」六題（pe-cp-1～6）的獨立驗算。

用法：python tools/verify_modern_ch02_detail_R2b.py
每個數字都和網站上寫的值比較（預設相對誤差 2%，四捨五入較粗的地方另外放寬），全部通過才 exit 0。
"""
import sys
from math import sqrt, exp, log, sin, cos, tan, atan, acos, radians, degrees, pi

import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")

h = 6.626e-34      # J s
hev = 4.136e-15    # eV s
c = 3.00e8
e = 1.602e-19
HC = 1240.0        # eV nm = keV pm = MeV fm
lamC = 2.426       # pm
me = 0.511         # MeV
meK = 511.0        # keV
mp = 938.3         # MeV
G = 6.67e-11
g = 9.8

fails = []


def check(name, got, want, rel=0.02):
    ok = abs(got - want) <= rel * abs(want) + 1e-300
    print(f"{'OK ' if ok else 'BAD'} {name:<44} 算得 {got:.6g}  網站 {want:.6g}")
    if not ok:
        fails.append(name)


def truth(name, cond):
    print(f"{'OK ' if cond else 'BAD'} {name}")
    if not cond:
        fails.append(name)


def compton(lam, th_deg, lc=lamC):
    return lam + lc * (1 - cos(radians(th_deg)))


# ======================= 07 康普頓效應 =======================
print("== 07 康普頓效應 ==")
# 例題 2.4
check("ex2.4 1-cos45", 1 - cos(radians(45)), 0.2929, 0.001)
check("ex2.4 dlam 45", lamC * (1 - cos(radians(45))), 0.71, 0.01)
check("ex2.4 (a) lam'", compton(10.0, 45), 10.7, 0.005)
check("ex2.4 (b) lam'max", compton(10.0, 180), 14.9, 0.005)
hcJpm = h * c * 1e12
check("ex2.4 hc J·pm", hcJpm, 1.988e-13, 0.001)
check("ex2.4 1/10-1/14.9", 1 / 10.0 - 1 / 14.9, 0.0329, 0.005)
KE24 = hcJpm * (1 / 10.0 - 1 / 14.9)
check("ex2.4 KEmax J", KE24, 6.54e-15, 0.005)
check("ex2.4 KEmax keV", KE24 / e / 1e3, 40.8, 0.005)
check("ex2.4 check 2E^2/(mc2+2E)", 2 * 124**2 / (511 + 248), 40.5, 0.005)
check("ex2.4 unrounded KE keV", HC * (1 / 10.0 - 1 / compton(10.0, 180)), 40.5, 0.005)
# 考古 107-7
KE7 = h * 0.3e19
check("107-7 KE J", KE7, 1.99e-15, 0.005)
check("107-7 KE eV", KE7 / e, 1.24e4, 0.005)
check("107-7 eV·s", hev * 3.0e18, 1.24e4, 0.005)
check("107-7 dlam pm", c / 1.2e19 * 1e12 - c / 1.5e19 * 1e12, 5.0, 0.001)
truth("107-7 dlam > 2 lamC", 5.0 > 2 * lamC)
# 2-25
check("2-25 pc J", 1.1e-23 * c, 3.3e-15, 0.001)
check("2-25 nu", 1.1e-23 * c / h, 5.0e18, 0.01)
check("2-25 E keV", 1.1e-23 * c / e / 1e3, 21, 0.02)
check("2-25 lam nm", HC / (1.1e-23 * c / e), 0.060, 0.02)
# 2-26
check("2-26 (pc)^2", 10**2 + 2 * 10 * 938.3, 18866, 0.0001)
check("2-26 pc", sqrt(10**2 + 2 * 10 * 938.3), 137, 0.005)
check("2-26 classical", sqrt(2 * 938.3 * 10), 137.0, 0.001)
check("2-26 diff %", (sqrt(18866) - sqrt(18766)) / sqrt(18866) * 100, 0.3, 0.2)
# 2-27
check("2-27 m c", 3.82e-26 * 3.0e8, 1.146e-17, 0.001)
lCNa = h / (3.82e-26 * 3.0e8)
check("2-27 lamC Na", lCNa, 5.8e-17, 0.01)
check("2-27 ratio", 2 * lCNa / 1e-10, 1e-6, 0.2)
check("2-27 check via electron", 2.426e-12 * 9.11e-31 / 3.82e-26, 5.8e-17, 0.01)
# 2-28
check("2-28 cos46", cos(radians(46)), 0.6947, 0.001)
check("2-28 1-cos46", 1 - cos(radians(46)), 0.305, 0.002)
check("2-28 dlam", lamC * (1 - cos(radians(46))), 0.74, 0.01)
check("2-28 lam'", compton(55.8, 46), 56.5, 0.002)
check("2-28 percent", lamC * (1 - cos(radians(46))) / 55.8 * 100, 1.3, 0.03)
# 2-29
check("2-29 lam", 2.2 - lamC * (1 - cos(radians(45))), 1.5, 0.01)
check("2-29 E keV", HC / 1.49, 830, 0.01)
check("2-29 frac", 0.71 / 1.49, 0.48, 0.02)
# 2-31
check("2-31 1/nu", 1 / 3.0e19, 3.33e-20, 0.002)
check("2-31 lamC/c", 2.426e-12 / 3.0e8, 0.809e-20, 0.002)
check("2-31 sum", 1 / 3.0e19 + 2.426e-12 / 3.0e8, 4.14e-20, 0.002)
nu31 = 1 / (1 / 3.0e19 + 2.426e-12 / 3.0e8)
check("2-31 nu'", nu31, 2.4e19, 0.01)
check("2-31 check lam'", compton(c / 3.0e19 * 1e12, 90), 12.4, 0.005)
# 2-32
E = sp.symbols("E", positive=True)
sol = [float(s) for s in sp.solve(sp.Eq(50, 2 * E**2 / (511 + 2 * E)), E)]
check("2-32 E sympy", sol[0], 141, 0.005)
check("2-32 sqrt(214400)", sqrt(100**2 + 8 * 25550), 463, 0.001)
check("2-32 quadratic", (100 + sqrt(214400)) / 4, 141, 0.005)
truth("2-32 25550 = 50*511", 50 * 511 == 25550)
lam32 = HC / 140.76
check("2-32 check lam", lam32, 8.81, 0.002)
check("2-32 check E'", HC / (lam32 + 2 * lamC), 90.8, 0.003)
# 2-33
check("2-33 1/90-1/100", 1 / 90 - 1 / 100, 0.001111, 0.001)
cphi33 = 1 - 511 * (1 / 90 - 1 / 100)
check("2-33 cos", cphi33, 0.432, 0.002)
check("2-33 phi", degrees(acos(cphi33)), 64, 0.01)
check("2-33 check dlam", HC / 90 - HC / 100, 1.38, 0.003)
check("2-33 check 1-cos", (HC / 90 - HC / 100) / lamC, 0.568, 0.003)
# 2-34
dl34 = lamC * 1.5
check("2-34 dlam", dl34, 3.64, 0.002)
check("2-34 lam'/lam", (80 + dl34) / 80, 1.0455, 0.0002)
t34 = sin(radians(120)) / ((80 + dl34) / 80 - cos(radians(120)))
check("2-34 tan", t34, 0.560, 0.003)
check("2-34 theta", degrees(atan(t34)), 29, 0.02)
check("2-34 1/80-1/83.639", 1 / 80 - 1 / (80 + dl34), 5.439e-4, 0.001)
KE34 = 1.240e6 * (1 / 80 - 1 / (80 + dl34))
check("2-34 KE eV", KE34, 674, 0.002)
check("2-34 KE J", KE34 * e, 1.08e-16, 0.005)
check("2-34 frac", KE34 / (HC / 80 * 1e3), 0.04, 0.12)
# 2-35 / 2-38 符號推導
hnu, mc2, E0s = sp.symbols("hnu mc2 E0", positive=True)
lam_s, lC_s = sp.symbols("lam lC", positive=True)
nup_over_nu = lam_s / (lam_s + 2 * lC_s)
expr = hnu * (1 - nup_over_nu.subs(lC_s, lam_s * hnu / mc2))
truth("2-35 KEmax formula", sp.simplify(expr - (2 * hnu**2 / mc2) / (1 + 2 * hnu / mc2)) == 0)
truth("2-35 = 2E^2/(mc2+2E)", sp.simplify((2 * hnu**2 / mc2) / (1 + 2 * hnu / mc2) - 2 * hnu**2 / (mc2 + 2 * hnu)) == 0)
Ep38 = 1 / (1 / hnu + 2 / E0s)
truth("2-38 E'", sp.simplify(Ep38 - hnu * E0s / (E0s + 2 * hnu)) == 0)
truth("2-38 KEmax", sp.simplify(hnu - Ep38 - 2 * hnu**2 / (E0s + 2 * hnu)) == 0)
check("2-35 check ex2.4", 2 * 124**2 / (511 + 248), 40.5, 0.005)
# 2-36
cphi36 = 1 - 0.5 / lamC
check("2-36 1-cos", 0.5 / lamC, 0.206, 0.003)
check("2-36 cos", cphi36, 0.794, 0.001)
phi36 = acos(cphi36)
check("2-36 phi", degrees(phi36), 37.4, 0.003)
pg, pgp = h / 10.0e-12, h / 10.5e-12
check("2-36 h/lam", pg, 6.626e-23, 0.001)
check("2-36 h/lam'", pgp, 6.310e-23, 0.001)
check("2-36 sin", sin(phi36), 0.608, 0.002)
check("2-36 (6.310)(0.794)", 6.310 * 0.794, 5.010, 0.001)
px, py = pg - pgp * cos(phi36), -pgp * sin(phi36)
check("2-36 px", px, 1.62e-23, 0.005)
check("2-36 py", py, -3.84e-23, 0.005)
check("2-36 p", sqrt(px**2 + py**2), 4.2e-23, 0.02)
check("2-36 tan", abs(py) / px, 2.37, 0.005)
check("2-36 theta", degrees(atan(abs(py) / px)), 67, 0.01)
KE36 = 1240 * (1 / 10.0 - 1 / 10.5)  # keV
check("2-36 check KE keV", KE36, 5.9, 0.01)
pc36 = sqrt(KE36**2 + 2 * KE36 * 511)
check("2-36 check pc", pc36, 77.9, 0.002)
check("2-36 check p", pc36 * 1e3 * e / c, 4.16e-23, 0.003)
# 2-37
check("2-37 tan40", tan(radians(40)), 0.839, 0.001)
check("2-37 tan(phi/2)", 1 / (2 * tan(radians(40))), 0.596, 0.002)
phi37 = 2 * atan(1 / (2 * tan(radians(40))))
check("2-37 phi/2", degrees(phi37) / 2, 30.8, 0.003)
check("2-37 phi", degrees(phi37), 61.6, 0.002)
check("2-37 cos phi", cos(phi37), 0.476, 0.003)
check("2-37 E'", 511 / (2 - cos(phi37)), 335, 0.003)
# 半角恆等式
ph = sp.symbols("ph", positive=True)
truth("2-37 half-angle identity (numeric)", all(abs(sin(t) / (2 - 2 * cos(t)) - 0.5 / tan(t / 2)) < 1e-12 for t in (0.3, 1.0, 1.7, 2.9)))
# 一般的反衝角公式與精確角度比較
lp37 = HC / 511 + lamC * (1 - cos(phi37))
truth("2-37 recoil formula", abs(degrees(atan(sin(phi37) / (lp37 / (HC / 511) - cos(phi37)))) - 40) < 0.05)
pc37 = sqrt(176**2 + 2 * 176 * 511)
check("2-37 check pc", pc37, 459, 0.002)
check("2-37 check transverse", pc37 * sin(radians(40)), 295, 0.003)
check("2-37 check photon", 335 * sin(phi37), 295, 0.003)
# sf-2-07a
E1 = 1 / (1 / 1.00 + 1 / me)
check("sf07a 1/0.511", 1 / me, 1.957, 0.001)
check("sf07a 1/E1", 1 / E1, 2.957, 0.001)
check("sf07a E1", E1, 0.338, 0.002)
E2 = 1 / (1 / E1 + 1 / me)
check("sf07a 1/E2", 1 / E2, 4.914, 0.001)
check("sf07a E2", E2, 0.204, 0.005)
check("sf07a electron1", 1.00 - E1, 0.662, 0.002)
check("sf07a electron2", E1 - E2, 0.135, 0.005)
check("sf07a total", 1.00 - E2, 0.796, 0.002)
check("sf07a 180", 1 / (1 + 2 / me), 0.204, 0.005)
check("sf07a 3x60 -> cos", 1 - 3 * 0.5, -0.5, 0.0001)
check("sf07a lam check MeV", HC / (1.24 + 2 * lamC) / 1e3, 0.204, 0.01)  # keV·pm / pm -> keV -> MeV
# sf-2-07b
check("sf07b 2*662^2", 2 * 662**2, 876488, 0.00001)
check("sf07b KEmax", 2 * 662**2 / (511 + 2 * 662), 478, 0.002)
check("sf07b 1/662", 1 / 662, 0.001511, 0.001)
check("sf07b 2/511", 2 / 511, 0.003914, 0.001)
Eb = 1 / (1 / 662 + 2 / 511)
check("sf07b E'", Eb, 184, 0.003)
check("sf07b sum", 2 * 662**2 / (511 + 2 * 662) + Eb, 662, 0.0005)
check("sf07b check lam", HC / 662, 1.873, 0.001)
check("sf07b check E'", HC / (HC / 662 + 2 * lamC), 184, 0.003)

# ============ 7.4 老師指定必考：光電效應與康普頓效應的差異 ============
print("== 7.4 老師指定必考 pe-cp-1～6 ==")
# pe-cp-1
check("pe1 2lamC", 2 * lamC, 4.85, 0.001)
check("pe1 visible ratio", 2 * lamC * 1e-3 / 500, 1e-5, 0.03)
check("pe1 X 0.1nm ratio", 2 * lamC * 1e-3 / 0.1, 0.05, 0.03)
# pe-cp-2 （符號證明 + 數值）
Es, m2, E0, p0c, ca = sp.symbols("E mc2 E0 p0c cosa", positive=True)
truth("pe2 static: (E+mc2)^2-(mc2^2+E^2)=2E mc2", sp.expand((Es + m2)**2 - (m2**2 + Es**2)) == 2 * Es * m2)
S_before = (Es + E0)**2 - (Es**2 + 2 * Es * p0c * ca + p0c**2)
truth("pe2 moving: S = E0^2-p0c^2+2E(E0-p0c cos)", sp.expand(S_before - (E0**2 - p0c**2 + 2 * Es * (E0 - p0c * ca))) == 0)
check("pe2 Cu Mc2 eV", 63.5 * 931.5e6, 5.92e10, 0.002)
check("pe2 Kmax", 5.0 - 4.7, 0.3, 0.001)
pec = sqrt(2 * 511e3 * 0.3)
check("pe2 p_e c eV", pec, 554, 0.002)
check("pe2 ratio", pec / 5.0, 1.1e2, 0.02)
# 原子承接的是 p_gamma - p_e（審查 D 修正）：大小介於 p_e c - 5.0 與 p_e c + 5.0
check("pe2 p_atom min", pec - 5.0, 549, 0.002)
check("pe2 p_atom max", pec + 5.0, 559, 0.002)
KEat = (pec + 5.0)**2 / (2 * 5.92e10)
check("pe2 atom KE upper eV", KEat, 2.6e-6, 0.02)
check("pe2 atom KE ~3e-6", KEat, 3e-6, 0.15)
check("pe2 wrong photon-only value", 5.0**2 / (2 * 5.92e10), 2e-10, 0.06)
check("pe2 underestimate factor", KEat / (5.0**2 / (2 * 5.92e10)), 1e4, 0.3)
truth("pe2 atom KE << phi", KEat < 1e-5 * 4.7)
check("pe2 check pc from energy", sqrt(1.511**2 - 0.511**2), 1.422, 0.001)
# pe-cp-3
E1 = HC / 400
E2 = HC / 0.0500
check("pe3 E1 eV", E1, 3.10, 0.001)
check("pe3 E2 eV", E2, 2.48e4, 0.001)
check("pe3 Kmax1", E1 - 2.28, 0.82, 0.005)
check("pe3 Kmax2", E2 - 2.28, 24797.7, 0.00001)
check("pe3 dl/l vis 90", lamC * 1e-3 / 400, 6.1e-6, 0.01)
check("pe3 dl/l X 90", lamC / 50.0, 0.0485, 0.001)
check("pe3 dl/l vis 180", 2 * lamC * 1e-3 / 400, 1.2e-5, 0.02)
check("pe3 dl/l X 180", 2 * lamC / 50.0, 0.097, 0.001)
K1 = E1 - HC / (400 + lamC * 1e-3)
check("pe3 K1 exact", K1, 1.9e-5, 0.02)
check("pe3 K1 formula", E1 * (lamC * 1e-3) / (400 + lamC * 1e-3), 1.9e-5, 0.02)
K2 = (HC / 50.0 - HC / (50.0 + lamC))  # keV
check("pe3 K2 keV", K2, 1.15, 0.003)
check("pe3 K2 formula", 24.8 * lamC / 52.43, 1.15, 0.003)
check("pe3 lam'", 50.0 + lamC, 52.43, 0.0001)
check("pe3 E' keV", HC / 52.43, 23.65, 0.0005)
check("pe3 phi frac", 2.28 / 24800, 1e-4, 0.1)
check("pe3 ratio K", K1 / 0.82, 2e-5, 0.2)
# pe-cp-4
E4 = HC / 71.0
check("pe4 E", E4, 17.46, 0.0005)
lp4 = compton(71.0, 90)
check("pe4 lam'", lp4, 73.43, 0.0001)
Ep4 = HC / lp4
check("pe4 E'", Ep4, 16.89, 0.0005)
K4 = E4 - Ep4
check("pe4 K", K4, 0.577, 0.002)
check("pe4 tan theta_e", 71.0 / lp4, 0.967, 0.001)
the4 = degrees(atan(sin(radians(90)) / (lp4 / 71.0 - cos(radians(90)))))
check("pe4 theta_e", the4, 44.0, 0.002)
check("pe4 photoelectron", E4 - 8.98, 8.48, 0.002)
Kmax4 = 2 * E4**2 / (511 + 2 * E4)
check("pe4 2E", 2 * E4, 34.9, 0.002)
check("pe4 KEmax", Kmax4, 1.12, 0.005)
check("pe4 frac Compton 90", K4 / E4, 0.033, 0.01)
check("pe4 frac Compton max", Kmax4 / E4, 0.064, 0.01)
check("pe4 frac photo", (E4 - 8.98) / E4, 0.486, 0.002)
pc4 = sqrt(0.577**2 + 2 * 0.577 * 511)
check("pe4 check pc", pc4, 24.29, 0.0005)
check("pe4 check transverse", pc4 * sin(radians(44.0)), 16.87, 0.001)
check("pe4 check longitudinal", pc4 * cos(radians(44.0)), 17.47, 0.001)
# 動量守恆以精確角度完整檢查
pe_vec = (E4 - Ep4 * cos(radians(90)), Ep4 * sin(radians(90)))  # keV/c
Kexact = sqrt(pe_vec[0]**2 + pe_vec[1]**2 + 511**2) - 511
check("pe4 momentum->KE consistency", Kexact, K4, 0.002)
# pe-cp-5
E5 = HC / 135.0
check("pe5 E", E5, 9.185, 0.0005)
truth("pe5 E > B_K", E5 > 8.98)
lp60 = compton(135.0, 60)
check("pe5 lam' 60", lp60, 136.21, 0.00005)
check("pe5 E' 60", HC / lp60, 9.103, 0.0003)
check("pe5 Kmax 60", HC / lp60 - 0.0047, 9.099, 0.0003)
check("pe5 1-cos150", 1 - cos(radians(150)), 1.866, 0.0005)
lp150 = compton(135.0, 150)
check("pe5 lam' 150", lp150, 139.53, 0.00005)
check("pe5 E' 150", HC / lp150, 8.887, 0.0003)
check("pe5 Kmax 150", HC / lp150 - 0.0047, 8.882, 0.0003)
lamK = HC / 8.98
check("pe5 lamK", lamK, 138.08, 0.0001)
truth("pe5 60 can eject K", lp60 < lamK)
truth("pe5 150 cannot eject K", lp150 > lamK)
check("pe5 K-shell KE 60", HC / lp60 - 8.98, 0.123, 0.01)
check("pe5 lamK 3 decimals", lamK, 138.085, 0.00001)
x5 = (lamK - 135.0) / lamC
check("pe5 1-cos thc", x5, 1.2715, 0.0002)
check("pe5 cos thc", 1 - x5, -0.2715, 0.001)
check("pe5 thc", degrees(acos(1 - x5)), 105.75, 0.0003)
check("pe5 thc ~105.8", degrees(acos(1 - x5)), 105.8, 0.001)
# 常數敏感度：hc=1239.84 eV·nm、lamC=2.4263 pm
check("pe5 sensitivity thc (hc=1239.84)", degrees(acos(1 - (1239.84 / 8.98 - 135.0) / 2.4263)), 105.3, 0.002)
x5e = 511 * (1 / 8.98 - 1 / E5)
check("pe5 energy diff", 1 / 8.98 - 1 / 9.1852, 0.002488, 0.0005)
check("pe5 energy form", x5e, 1.271, 0.0005)
check("pe5 energy thc", degrees(acos(1 - x5e)), 105.7, 0.001)
lam0K = HC / 2.2
check("pe5 lam0 potassium", lam0K, 564, 0.001)
truth("pe5 visible all angles", 500 + 2 * lamC * 1e-3 < lam0K)
check("pe5 visible Kmax", HC / 500 - 2.2, 0.28, 0.001)
check("pe5 visible dK", HC / 500 - HC / (500 + 2 * lamC * 1e-3), 2.4e-5, 0.02)
# pe-cp-6
nu250, nu300, nu350, nu400 = c / 250e-9, c / 300e-9, c / 350e-9, c / 400e-9
check("pe6 nu250", nu250, 1.200e15, 0.0005)
check("pe6 nu300", nu300, 1.000e15, 0.0005)
check("pe6 nu350", nu350, 8.571e14, 0.0005)
check("pe6 nu400", nu400, 7.50e14, 0.0005)
# 數據本身由 phi=3.20 eV、hc=1240 產生，檢查三位小數四捨五入
for lam, V in [(250, 1.76), (300, 0.93), (350, 0.34)]:
    check(f"pe6 data V0({lam})", HC / lam - 3.20, V, 0.01)
truth("pe6 data 400 no current", HC / 400 < 3.20)
h6 = (1.76 - 0.34) / (nu250 - nu350)
check("pe6 h eV s", h6, 4.14e-15, 0.002)
check("pe6 h J s", h6 * e, 6.63e-34, 0.002)
check("pe6 dnu", nu250 - nu350, 3.429e14, 0.0005)
phi6 = h6 * nu250 - 1.76
check("pe6 h nu250", h6 * nu250, 4.97, 0.001)
check("pe6 phi", phi6, 3.21, 0.002)
check("pe6 300 check", h6 * nu300 - phi6, 0.93, 0.01)
check("pe6 h nu400", h6 * nu400, 3.11, 0.002)
truth("pe6 400 below threshold", h6 * nu400 < phi6)
check("pe6 lam0 nm", h6 * c / phi6 * 1e9, 387, 0.003)
check("pe6 h vs standard", abs(h6 - hev) / hev, 0.001, 1.0)
dls = {45: 71.51 - 70.80, 90: 73.23 - 70.80, 135: 74.94 - 70.80}
check("pe6 dl135", dls[135], 4.14, 0.001)
check("pe6 1-cos135", 1 - cos(radians(135)), 1.707, 0.0005)
lC6 = dls[135] / (1 - cos(radians(135)))
check("pe6 lamC", lC6, 2.425, 0.001)
check("pe6 lamC 45", dls[45] / (1 - cos(radians(45))), 2.42, 0.005)
check("pe6 lamC 90", dls[90] / 1.0, 2.43, 0.001)
# 數據由 lamC=2.426 產生
for th, peak in [(45, 71.51), (90, 73.23), (135, 74.94)]:
    check(f"pe6 data peak {th}", compton(70.80, th), peak, 0.0001)
m6 = h / (lC6 * 1e-12 * c)
check("pe6 mass", m6, 9.11e-31, 0.003)
check("pe6 carbon mass", 12 * 1.661e-27, 1.99e-26, 0.003)
lCC = h / (1.99e-26 * c)
check("pe6 carbon lamC pm", lCC * 1e12, 1.1e-4, 0.02)
check("pe6 carbon max shift pm", 2 * lCC * 1e12, 2.2e-4, 0.02)
check("pe6 cross-check mass", h6 * e / (lC6 * 1e-12 * c), 9.1e-31, 0.01)

# ======================= 08 成對產生與湮滅 =======================
print("== 08 成對產生與湮滅 ==")
gam = 1 / sqrt(1 - 0.25)
check("ex2.6 gamma", gam, 1.155, 0.001)
check("ex2.6 p1-p2", 2 * gam * me * 0.5, 0.590, 0.002)
check("ex2.6 p1+p2", 2 * gam * me, 1.180, 0.001)
p1 = (2 * gam * me * 0.5 + 2 * gam * me) / 2
check("ex2.6 p1", p1, 0.885, 0.001)
check("ex2.6 p2", 2 * gam * me - p1, 0.295, 0.002)
check("ex2.6 ratio", p1 / (2 * gam * me - p1), 3.00, 0.001)
check("ex2.6 doppler", me * sqrt(3), 0.885, 0.001)
# 107-8
Et = 2.0 + 2 * me
pc8 = sqrt(2.0**2 + 2 * 2.0 * me)
check("107-8 Etot", Et, 3.022, 0.0001)
check("107-8 pc^2", 2.0**2 + 2 * 2.0 * me, 6.044, 0.0001)
check("107-8 pc", pc8, 2.458, 0.0005)
check("107-8 E1", (Et + pc8) / 2, 2.740, 0.0005)
check("107-8 E2", (Et - pc8) / 2, 0.282, 0.002)
check("107-8 equal-angle", degrees(acos((pc8 / 2) / (Et / 2))), 35.6, 0.002)
check("107-8 E1E2", ((Et + pc8) / 2) * ((Et - pc8) / 2), 0.772, 0.002)
check("107-8 Mc2", sqrt(Et**2 - pc8**2), 1.758, 0.001)
# 2-39
check("2-39 E", 1.00 + me, 1.511, 0.0001)
check("2-39 lam m", 1.240e-6 / 1.511e6, 8.21e-13, 0.001)
check("2-39 lam pm (keV)", HC / 1511, 0.821, 0.001)
check("2-39 511 keV photon", HC / 511, 2.43, 0.002)
# 2-41
truth("2-41 lam_max = lamC/2", abs(HC / (2 * 511) - lamC / 2) / (lamC / 2) < 0.001)
truth("2-41 cos60 = 1/2", abs(cos(radians(60)) - 0.5) < 1e-12)
# 2-42
Ms, ms_ = sp.symbols("M m", positive=True)
Emin = sp.solve(sp.Eq(2 * E * Ms + Ms**2, (2 * ms_ + Ms)**2), E)[0]
truth("2-42 Emin = 2m(1+m/M)", sp.simplify(Emin - 2 * ms_ * (1 + ms_ / Ms)) == 0)
check("2-42 m/M", me / mp, 5.45e-4, 0.001)
check("2-42 Emin proton", 1.022 * (1 + me / mp), 1.0226, 0.0001)
check("2-42 percent", me / mp * 100, 0.05, 0.1)
# sf-2-08a
check("sf08a s", c * 0.40e-9 / 2, 0.060, 0.001)
pc8a = sqrt(2 * 10 * 511e3)
check("sf08a pc", pc8a, 3.2e3, 0.01)
d8 = pc8a / 511e3
check("sf08a delta", d8, 6.3e-3, 0.01)
check("sf08a deg", degrees(d8), 0.36, 0.01)
check("sf08a offset", 0.40 * d8, 2.5e-3, 0.01)
# sf-2-08b
KE8 = (5.00 - 1.022) / 2
check("sf08b KE", KE8, 1.989, 0.0001)
check("sf08b KE^2", KE8**2, 3.956, 0.0005)
check("sf08b 2KEmc2", 2 * KE8 * me, 2.033, 0.0005)
pc8b = sqrt(KE8**2 + 2 * KE8 * me)
check("sf08b pc", pc8b, 2.447, 0.0005)
check("sf08b 2pc", 2 * pc8b, 4.894, 0.0005)
check("sf08b deficit", 5.00 - 2 * pc8b, 0.106, 0.01)
KEn = (5.00 - 2 * pc8b)**2 / (2 * 1.93e5)
check("sf08b KE nucleus MeV", KEn, 2.9e-8, 0.02)
check("sf08b KE nucleus eV", KEn * 1e6, 0.03, 0.05)
check("sf08b fraction", KEn / 5.00, 6e-9, 0.05)
check("sf08b check", sqrt((KE8 + me)**2 - me**2), 2.447, 0.0005)

# ======================= 09 光子的吸收 =======================
print("== 09 光子的吸收 ==")
check("115-2 2mc2", 2 * me, 1.02, 0.002)
check("ex2.7 mux", 4.9 * 0.10, 0.49, 0.0001)
check("ex2.7 I/I0", exp(-0.49), 0.61, 0.005)
check("ex2.7 ln100", log(100), 4.61, 0.002)
check("ex2.7 x", log(100) / 4.9, 0.94, 0.005)
check("ex2.7 check n", log(100) / 0.49, 9.4, 0.005)
check("107-9 x1/2", log(2) / 78, 8.9e-3, 0.002)
check("107-9 check", exp(-78 * 0.0089), 0.50, 0.005)
check("2-43 ln2", log(2), 0.693, 0.001)
check("2-43 ln10", log(10), 2.30, 0.002)
check("2-43 ratio", log(10) / log(2), 3.32, 0.001)
check("2-43 check", 0.5 ** (log(10) / log(2)), 0.100, 0.001)
check("2-44 e^-0.1", exp(-0.1), 0.9048, 0.0001)
check("2-44 exact", 1 - exp(-0.100), 0.0952, 0.001)
check("2-44 error %", (0.100 - (1 - exp(-0.1))) / (1 - exp(-0.1)) * 100, 5.1, 0.01)
check("2-46 mux1", 5.0e-3 * 0.50, 2.5e-3, 0.0001)
check("2-46 I1", exp(-0.0025), 0.9975, 0.0001)
check("2-46 mux2", 5.0e-3 * 5.0, 0.025, 0.0001)
check("2-46 I2", exp(-0.025), 0.975, 0.0005)
check("2-46 reduce2 %", (1 - exp(-0.025)) * 100, 2.5, 0.02)
check("2-47 x water", 10 * 52 / 4.9, 106, 0.002)
check("2-47 check mux", 4.9 * 0.106, 0.52, 0.002)
check("2-47 check T", exp(-0.52), 0.59, 0.01)
check("2-48 mux", 4.7e4 * 1.0e-4, 4.7, 0.0001)
check("2-48 I/I0", exp(-4.7), 9.1e-3, 0.005)
check("2-48 halving", 4.7 / log(2), 6.8, 0.005)
check("2-48 2^-6.8", 2 ** -6.8, 0.0090, 0.005)
check("2-49 x1/2", 0.693 / 4.7e4, 1.5e-5, 0.02)
check("2-49 check n", 0.10 / 0.015, 6.8, 0.02)
check("2-50 x iron", 10 * 5.8 / 1.1, 53, 0.006)
check("2-50 keV", HC / 0.05, 25e3, 0.01)
check("sf09a mu/rho Pb", 52 / 11.3e3, 4.6e-3, 0.005)
check("sf09a mu/rho water", 4.9 / 1.00e3, 4.9e-3, 0.001)
check("sf09a Z/A water", 10 / 18, 0.56, 0.01)
check("sf09a Z/A lead", 82 / 207.2, 0.40, 0.02)
check("sf09a ratio", (10 / 18) / (82 / 207.2), 1.4, 0.01)
check("sf09a Pb kg/m2", 11.3e3 * 0.010, 113, 0.001)
check("sf09a water kg/m2", 1.00e3 * 0.106, 106, 0.001)
check("sf09a wall exponent", 52 * 0.0050 + 4.9 * 0.20, 1.24, 0.001)
check("sf09a wall T", exp(-1.24), 0.29, 0.01)
check("sf09a Pb thinner", 52 / 4.9, 10.6, 0.002)
check("sf09a check", 4.6e-3 * 56.5 + 4.9e-3 * 200, 1.24, 0.002)
xs = sp.symbols("x", positive=True)
mus = sp.symbols("mu", positive=True)
truth("sf09b normalisation", sp.simplify(sp.integrate(mus * sp.exp(-mus * xs), (xs, 0, sp.oo)) - 1) == 0)
truth("sf09b mean = 1/mu", sp.simplify(sp.integrate(xs * mus * sp.exp(-mus * xs), (xs, 0, sp.oo)) - 1 / mus) == 0)
check("sf09b 1/mu mm", 1 / 78 * 1e3, 12.8, 0.002)
check("sf09b x1/2 mm", 0.693 / 78 * 1e3, 8.9, 0.002)
check("sf09b 1-e^-1", 1 - exp(-1), 0.63, 0.005)
check("sf09b 1/ln2", 1 / log(2), 1.44, 0.002)
check("sf09b check", 8.9 * 1.44, 12.8, 0.002)

# ======================= 10 光子與重力 =======================
print("== 10 光子與重力 ==")
c3 = 3.0e8
check("ex2.8 gH", 9.8 * 22.5, 220.5, 0.0001)
check("ex2.8 gH/c2", 9.8 * 22.5 / c3**2, 2.45e-15, 0.001)
check("ex2.8 dnu", 9.8 * 22.5 / c3**2 * 7.3e14, 1.8, 0.01)
x51 = G * 2.0e30 / (c3**2 * 7.0e8)
check("2-51 GM", G * 2.0e30, 1.33e20, 0.005)
check("2-51 c2R", c3**2 * 7.0e8, 6.3e25, 0.001)
check("2-51 x", x51, 2.1e-6, 0.01)
check("2-51 x unrounded", x51, 2.12e-6, 0.002)
check("2-51 dlam nm", 500 * x51, 1.1e-3, 0.05)
check("2-51 exact-approx", 500 * (1 / (1 - x51) - 1) - 500 * x51, 500 * x51**2, 0.01)
x52 = G * 2.0e30 / (c3**2 * 6.4e6)
check("2-52 c2R", c3**2 * 6.4e6, 5.76e23, 0.001)
check("2-52 x", x52, 2.3e-4, 0.01)
check("2-52 dlam", 500 * x52, 0.12, 0.04)
check("2-52 radius ratio", 7.0e8 / 6.4e6, 109, 0.005)
check("2-52 check", 1.06e-3 * 109, 0.12, 0.04)
EJ = 14.4e3 * e
check("2-53 E J", EJ, 2.307e-15, 0.001)
check("2-53 E^2", EJ**2, 5.32e-30, 0.002)
check("2-53 2Mc2", 2 * 9.5e-26 * c3**2, 1.71e-8, 0.001)
dE = EJ**2 / (2 * 9.5e-26 * c3**2)
check("2-53 dE J", dE, 3.1e-22, 0.01)
check("2-53 dE eV", dE / e, 1.9e-3, 0.03)
check("2-53 (b)", 1.9e-3 * 9.5e-26 / 1.0e-3, 1.8e-25, 0.01)
check("2-53 (b) exact", dE / e * 9.5e-26 / 1.0e-3, 1.8e-25, 0.03)
nu53 = 14.4e3 / hev
check("2-53 nu", nu53, 3.48e18, 0.002)
check("2-53 gH/c2", 9.8 * 20 / c3**2, 2.18e-15, 0.002)
check("2-53 dnu", 9.8 * 20 / c3**2 * nu53, 7.6e3, 0.005)
check("2-53 check energy", 14.4e3 * 9.8 * 20 / c3**2, 3e-11, 0.06)
check("2-54 2GM", 2 * G * 5.98e24, 7.98e14, 0.001)
check("2-54 RS", 2 * G * 5.98e24 / c3**2, 8.9e-3, 0.005)
check("2-54 check", 3.0e3 * 3.0e-6, 9e-3, 0.001)
check("2-54 earth/sun", 5.98e24 / 2.0e30, 3.0e-6, 0.004)
vv, MM, RR, mm, cc = sp.symbols("v M R m c", positive=True)
Gs = sp.Symbol("G", positive=True)
ve = sp.solve(sp.Eq(sp.Rational(1, 2) * mm * vv**2 - Gs * mm * MM / RR, 0), vv)[0]
truth("2-55 v_e = sqrt(2GM/R)", sp.simplify(ve - sp.sqrt(2 * Gs * MM / RR)) == 0)
truth("2-55 v_e=c -> R=2GM/c^2", sp.simplify(sp.solve(sp.Eq(cc**2, 2 * Gs * MM / RR), RR)[0] - 2 * Gs * MM / cc**2) == 0)
check("2-55 earth v_e km/s", sqrt(2 * G * 5.98e24 / 6.4e6) / 1e3, 11, 0.02)
# sf-2-10a
GE = 4.7e-9 / 1.44e4
check("sf10a G/E", GE, 3.3e-13, 0.02)
vG = 3.00e8 * GE
check("sf10a vGamma", vG, 9.8e-5, 0.005)
gHc2 = 9.8 * 22.5 / (3.00e8)**2
check("sf10a gH/c2", gHc2, 2.45e-15, 0.001)
check("sf10a ratio", GE / gHc2, 133, 0.005)
check("sf10a percent", gHc2 / GE * 100, 0.75, 0.01)
check("sf10a x0", 9.8e-5 / (2 * pi * 50), 3.1e-7, 0.01)
check("sf10a recoil/linewidth", 1.9e-3 / 4.7e-9, 4e5, 0.02)
check("sf10a grav energy", 1.44e4 * gHc2, 3.5e-11, 0.01)
check("sf10a recoil/grav", 1.9e-3 / (1.44e4 * gHc2), 5e7, 0.1)
check("sf10a 2gH/c2", 2 * gHc2, 4.9e-15, 0.001)
check("sf10a gH/c", 9.8 * 22.5 / 3.00e8, 7.4e-7, 0.01)
check("sf10a check ratio", 9.8e-5 / 7.4e-7, 133, 0.005)
# sf-2-10b
Ev, rr, Rv, GMc2 = sp.symbols("E r R k", positive=True)
truth("sf10b integral 1/r^2", sp.simplify(sp.integrate(1 / rr**2, (rr, Rv, sp.oo)) - 1 / Rv) == 0)
xwd = G * 2.0e30 / ((3.00e8)**2 * 6.4e6)
check("sf10b WD x", xwd, 2.32e-4, 0.002)
check("sf10b WD 1-e^-x", 1 - exp(-xwd), 2.32e-4, 0.002)
check("sf10b WD exact", 1 - sqrt(1 - 2 * xwd), 2.32e-4, 0.002)
check("sf10b WD R/RS", 1 / (2 * xwd), 2200, 0.02)
GMc = G * 2.8e30 / (3.00e8)**2
check("sf10b NS GM/c2 km", GMc / 1e3, 2.08, 0.005)
xns = GMc / 1.0e4
check("sf10b NS x", xns, 0.2075, 0.001)
check("sf10b NS R/RS", 1 / (2 * xns), 2.4, 0.01)
check("sf10b NS (a)", 1 - exp(-xns), 0.187, 0.003)
check("sf10b NS exact", 1 - sqrt(1 - 2 * xns), 0.235, 0.003)
check("sf10b NS under (2.29) %", (0.235 - 0.2075) / 0.235 * 100, 12, 0.03)
check("sf10b NS under (a) %", (0.235 - 0.187) / 0.235 * 100, 20, 0.03)
u = sp.symbols("u", positive=True)
useries = sp.series((1 - sp.sqrt(1 - u)) / (u / 2), u, 0, 3).removeO()
truth("sf10b series 1+u/4+u^2/8", sp.simplify(useries - (1 + u / 4 + u**2 / 8)) == 0)
usol = float(sp.nsolve((1 - sp.sqrt(1 - u)) / (u / 2) - 1.1, u, 0.3))
check("sf10b u(10%)", usol, 0.331, 0.003)
check("sf10b NS ratio", 0.235 / 0.208, 1.13, 0.005)

print()
if fails:
    print("FAILED:", len(fails), fails)
    sys.exit(1)
print("ALL CHECKS PASSED")
