"""熱學第 1 章考前衝刺（08-exam.html）變化題的數值驗算。"""
import math

k, NA, R, amu, atm = 1.381e-23, 6.022e23, 8.315, 1.6605e-27, 1.013e5
ok = True
def check(name, got, want, tol=0.01):
    global ok
    good = abs(got - want) <= tol * abs(want)
    ok &= good
    print(("✔" if good else "✘"), name, f"{got:.5g}", "期望", want)

# 變化題 1：200 g 咖啡 90°C 加 0°C 冰降到 70°C
c, Lf = 4.186, 333.0
check("冰的質量 g", 200 * c * 20 / (Lf + c * 70), 26.7)
# 變化題 2：氦 P∝V 由 2 L 到 4 L，初壓 1 atm
PiVi, PfVf = 1 * 2 * atm * 1e-3, 2 * 4 * atm * 1e-3
W = -0.5 * (PfVf - PiVi); dU = 1.5 * (PfVf - PiVi)
check("W", W, -304); check("ΔU", dU, 912); check("Q", dU - W, 1216)
# 變化題 3：300 K 氦與氬的 v_rms
vHe = math.sqrt(3 * k * 300 / (4.0026 * amu)); vAr = math.sqrt(3 * k * 300 / (39.95 * amu))
check("v_rms He", vHe, 1368); check("v_rms Ar", vAr, 433); check("比值", vHe / vAr, 3.16)
# 變化題 4：空氣絕熱壓縮到 1/10
check("T_f", 300 * 10 ** 0.4, 754); check("P_f/P_i", 10 ** 1.4, 25.1)
# 變化題 5：1 mol 300 K 等溫壓縮到一半
check("W 等溫", R * 300 * math.log(2), 1729)
# 變化題 6：30 m 鋼軌升溫 40 K
check("ΔL (m)", 1.1e-5 * 30 * 40, 0.0132)
# 變化題 7：2 mol 雙原子定壓升溫 10 K
check("Q", 2 * 3.5 * R * 10, 582); check("ΔU", 2 * 2.5 * R * 10, 416); check("W", -2 * R * 10, -166)
# 變化題 8：2 m²、4 mm 玻璃、溫差 15 K
check("熱流 W", 0.8 * 2 * 15 / 0.004, 6000)
# 變化題 9：高空 10 km 的平均自由徑
check("ℓ 地面 (m)", k * 300 / (4 * math.pi * (1.5e-10) ** 2 * atm), 1.45e-7)
check("ℓ 10 km (m)", k * 223 / (4 * math.pi * (1.5e-10) ** 2 * 0.26 * atm), 4.14e-7)
# 變化題 10：擴散 1 cm，D=1e-9
check("t (s)", (1e-2) ** 2 / 1e-9, 1e5)
print("ALL PASS" if ok else "有錯")
