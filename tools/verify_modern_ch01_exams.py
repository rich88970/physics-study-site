"""近代物理第 1 章：考古題補齊（2026-10-21）新增卡的驗算。

kg-109-1  109 學年上學期考古第 1 題：由對稱碰撞推出 p = gamma m v
執行：python tools/verify_modern_ch01_exams.py（需要 sympy）
"""
import sys
import sympy as sp

sys.stdout.reconfigure(encoding='utf-8')
ok = True


def check(name, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name)
    ok = ok and bool(cond)


# ---- kg-109-1 ----
L, T0, v, c, mA, mB = sp.symbols('L T0 v c m_A m_B', positive=True)
g = 1 / sp.sqrt(1 - v**2 / c**2)
VA = L / T0                      # 步驟 1
T = g * T0                       # 步驟 2：時間膨脹
VB = L / T
check('kg-109-1 V_B = (L/T0) sqrt(1-v^2/c^2)', sp.simplify(VB - L / T0 * sp.sqrt(1 - v**2 / c**2)) == 0)
sol = sp.solve(sp.Eq(mA * VA, mB * VB), mB)[0]   # 步驟 3–4：p_A = p_B
check('kg-109-1 m_B = m_A / sqrt(1-v^2/c^2)', sp.simplify(sol - mA / sp.sqrt(1 - v**2 / c**2)) == 0)
# 驗算：v = 0.6c
num = {v: sp.Rational(3, 5) * c}
check('kg-109-1 v=0.6c: gamma = 1.25', sp.simplify(g.subs(num)) == sp.Rational(5, 4))
check('kg-109-1 v=0.6c: V_B = 0.8 V_A', sp.simplify((VB / VA).subs(num)) == sp.Rational(4, 5))
check('kg-109-1 m_B V_B = m_A V_A', sp.simplify((sol * VB - mA * VA)) == 0)
# 速度轉換：u_y = u'_y / (gamma (1 + v u'_x / c^2))，u'_x = 0
uyp = VA
check('kg-109-1 速度轉換給出同樣的 V_B', sp.simplify(uyp / g - VB) == 0)
# 低速極限
check('kg-109-1 v<<c 時 gamma -> 1', sp.limit(g, v, 0) == 1)

print('ALL PASS' if ok else 'SOME FAILED')
sys.exit(0 if ok else 1)
