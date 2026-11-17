"""近代物理第 2 章：考古題補齊（2026-10-21）新增卡的驗算。

kg-109-2  109 學年上學期考古第 2 題：顯示光的粒子性的現象（常數與數值）
kg-109-4  109 學年上學期考古第 4 題：KE = 3 MeV 的正子湮滅
kg-104-4  104 級上學期考古第 4 題：1 MeV 光子被質子散射 45°
執行：python tools/verify_modern_ch02_exams.py（需要 numpy）
"""
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
ok = True


def check(name, got, want, rtol=2e-3):
    global ok
    good = np.isclose(got, want, rtol=rtol, atol=0)
    print(('PASS ' if good else 'FAIL ') + f'{name}: {got:.6g} (want {want})')
    ok = ok and bool(good)


h = 6.626e-34; c = 2.998e8; e = 1.602e-19; me = 9.109e-31
mec2 = 0.511; mpc2 = 938.3          # MeV

# ---- kg-109-2 ----
check('kg-109-2 hc (eV·m)', h * c / e, 1.240e-6)
lamC = h / (me * c)
check('kg-109-2 電子康普頓波長 (m)', lamC, 2.426e-12)
check('kg-109-2 最大位移 2 lambda_C (pm)', 2 * lamC * 1e12, 4.85)
check('kg-109-2 成對產生門檻 2mc^2 (MeV)', 2 * mec2, 1.022)

# ---- kg-109-4 ----
KE = 3.0
Etot = KE + 2 * mec2
pc = np.sqrt(KE**2 + 2 * KE * mec2)
E1 = (Etot + pc) / 2; E2 = (Etot - pc) / 2
check('kg-109-4 E1+E2 (MeV)', Etot, 4.022)
check('kg-109-4 pc (MeV)', pc, 3.474)
check('kg-109-4 E1 (MeV)', E1, 3.748)
check('kg-109-4 E2 (MeV)', E2, 0.274)
check('kg-109-4 E1E2 = (Etot^2-(pc)^2)/4', E1 * E2, (Etot**2 - pc**2) / 4, 1e-9)
Mc2 = np.sqrt(2 * mec2 * (KE + 2 * mec2))
check('kg-109-4 不變質量 Mc^2 (MeV)', Mc2, 2.027)
check('kg-109-4 E1E2 = (Mc^2)^2/4 (MeV^2)', E1 * E2, Mc2**2 / 4, 1e-9)
check('kg-109-4 E1E2 數值 (MeV^2)', E1 * E2, 1.028)
# 手寫解答用 pc = 3.45 得到 3.735 / 0.285（數值誤差）
check('kg-109-4 解答的 E1 (pc=3.45)', (4.02 + 3.45) / 2, 3.735, 1e-6)
check('kg-109-4 解答的 E2 (pc=3.45)', (4.02 - 3.45) / 2, 0.285, 1e-6)
# 高能極限：E2 -> mc^2/2
KEbig = 1e6
E2big = (KEbig + 2 * mec2 - np.sqrt(KEbig**2 + 2 * KEbig * mec2)) / 2
check('kg-109-4 KE->inf 時 E2 -> mc^2/2', E2big, mec2 / 2, 1e-3)

# ---- kg-104-4 ----
E = 1.0; th = np.radians(45)
inv = 1 / E + (1 - np.cos(th)) / mpc2
Ep = 1 / inv
KEp = E - Ep
check('kg-104-4 (1-cos45)/mpc2 (1/MeV)', (1 - np.cos(th)) / mpc2, 3.1215e-4, 1e-3)
check('kg-104-4 E\' (MeV)', Ep, 0.999688, 1e-6)
check('kg-104-4 KE_p (MeV)', KEp, 3.12e-4)
check('kg-104-4 KE_p (eV)', KEp * 1e6, 312, 2e-3)
hcMeV = h * c / e / 1e6       # MeV·m
check('kg-104-4 質子康普頓波長 (m)', hcMeV / mpc2, 1.32e-15, 3e-3)
check('kg-104-4 Δλ (m)', hcMeV / mpc2 * (1 - np.cos(th)), 3.9e-16, 1e-2)
check('kg-104-4 λ (pm)', hcMeV / E * 1e12, 1.24, 1e-3)
px = E - Ep * np.cos(th); py = Ep * np.sin(th)
check('kg-104-4 p_x c (MeV)', px, 0.29311, 1e-4)
check('kg-104-4 p_y c (MeV)', py, 0.70689, 1e-4)
check('kg-104-4 |p|c 由分量', np.hypot(px, py), 0.7652, 1e-3)
check('kg-104-4 |p|c 由動能', np.sqrt(KEp**2 + 2 * KEp * mpc2), np.hypot(px, py), 1e-6)
check('kg-104-4 反衝角 (deg)', np.degrees(np.arctan2(py, px)), 67.5, 1e-3)
inv_e = 1 + (1 - np.cos(th)) / mec2
check('kg-104-4 對照：電子 1/E\'', inv_e, 1.5732, 1e-4)
check('kg-104-4 對照：電子 E\' (MeV)', 1 / inv_e, 0.636, 1e-3)
check('kg-104-4 對照：電子 KE (MeV)', 1 - 1 / inv_e, 0.364, 2e-3)

print('ALL PASS' if ok else 'SOME FAILED')
sys.exit(0 if ok else 1)
