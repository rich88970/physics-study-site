"""應用數學 第 1 章：考古題盤點後新增的題目卡（108級、109級考古題）用 sympy 獨立驗算。

用法：python tools/verify_applied_math_ch01_exams.py     全部通過時結束碼為 0。
驗法：
- 顯式解 y(x)：代回方程化簡為 0 ＋ 初始條件。
- 隱式解 G(x,y)=C：檢查 G_x N - G_y M = 0（dG 與 M dx + N dy 成比例），初始點代入 G 得 C。
- 數值答案：直接算出來比對。
"""
import random
import sys

import sympy as sp

x, y, t = sp.symbols("x y t", real=True)
results = []


def ok(name, cond):
    results.append((name, bool(cond)))


def zero(expr, syms=None, lo=0.3, hi=1.3):
    e = sp.simplify(sp.expand(expr))
    if e == 0:
        return True
    syms = syms or sorted(e.free_symbols, key=str)
    for _ in range(8):
        vals = {s: random.uniform(lo, hi) for s in syms}
        if abs(complex(e.evalf(subs=vals))) > 1e-9:
            return False
    return True


def implicit(name, G, M, N, pt, Cval, lo=0.3, hi=1.3):
    ok(name + "：dG ∥ M dx + N dy", zero(sp.diff(G, x) * N - sp.diff(G, y) * M, [x, y], lo, hi))
    ok(name + "：初始點代入", sp.simplify(G.subs({x: pt[0], y: pt[1]}) - Cval) == 0)


# ---- 109級下 第1次期中 1(a)（＝108級下 ODE1 1(a)）：dy/dx = y cos x/(1+2y^2)，y(0)=1
G = sp.log(y) + y**2 - sp.sin(x)
implicit("1(a) ln y + y^2 = sin x + 1", G, -y * sp.cos(x), 1 + 2 * y**2, (0, 1), 1)
# 老師答案寫 -sin x + 1：檢查它「不」滿足方程（誤植）
Gbad = sp.log(y) + y**2 + sp.sin(x)
ok("1(a) 老師版 ln y + y^2 = -sin x + 1 不滿足方程（確認誤植）",
   not zero(sp.diff(Gbad, x) * (1 + 2 * y**2) - sp.diff(Gbad, y) * (-y * sp.cos(x)), [x, y]))

# ---- 1(b)：(x+y)dx + x ln x dy = 0，y(1)=1
M, N = x + y, x * sp.log(x)
G = x + y * sp.log(x)
implicit("1(b) x + y ln x = 1", G, M, N, (1, 1), 1, 1.5, 3)
yb = (1 - x) / sp.log(x)
ok("1(b) 顯式 y=(1-x)/ln x 代回", zero((M + N * sp.diff(yb, x)).subs(y, yb), [x], 1.5, 3))
ok("1(b) x→1 時 y→-1（不是 1：初始點在奇異點 x ln x = 0 上）", sp.limit(yb, x, 1) == -1)
# 積分因子 1/x 使其正合
ok("1(b) 乘 1/x 後正合", sp.simplify(sp.diff(M / x, y) - sp.diff(N / x, x)) == 0)

# ---- 1(c)（＝108級 1(h)）Bernoulli：y' + y/x = x y^2，y(1)=1 → 1/(xy) = 2 - x
yc = 1 / (x * (2 - x))
ok("1(c) y=1/(x(2-x)) 代回", zero(sp.diff(yc, x) + yc / x - x * yc**2))
ok("1(c) y(1)=1", yc.subs(x, 1) == 1)

# ---- 1(d)：(2x+4y)dx + (y-x)dy = 0，y(1)=0 → (y+2x)^3 = 8(y+x)^2
M, N = 2 * x + 4 * y, y - x
G = (y + 2 * x)**3 / (y + x)**2
implicit("1(d) (y+2x)^3 = 8(y+x)^2", G, M, N, (1, 0), 8)
v = sp.symbols("v")
ok("1(d) 部分分式 (v-1)/((v+1)(v+2)) = -2/(v+1)+3/(v+2)",
   sp.simplify((v - 1) / ((v + 1) * (v + 2)) - (-2 / (v + 1) + 3 / (v + 2))) == 0)

# ---- 1(e)（＝108級 1(d)）正合
M, N = 3 * x**2 - 2 * x * y + 2, 6 * y**2 - x**2 + 3
ok("1(e) 正合 M_y = N_x", sp.simplify(sp.diff(M, y) - sp.diff(N, x)) == 0)
G = x**3 - x**2 * y + 2 * x + 2 * y**3 + 3 * y
implicit("1(e) 2y^3 - x^2y + 3y + x^3 + 2x = 3", G, M, N, (1, 0), 3)

# ---- 1(f)（＝108級 1(g)）：F(y)=1/sin y
M, N = (x + y) * sp.sin(y), x * sp.sin(y) + sp.cos(y)
D = sp.diff(M, y) - sp.diff(N, x)
ok("1(f) Δ/M = cot y", sp.simplify(D / M - sp.cot(y)) == 0)
F = sp.exp(-sp.integrate(sp.cot(y), y))
ok("1(f) F = 1/sin y", sp.simplify(F - 1 / sp.sin(y)) == 0)
ok("1(f) 乘 F 後正合", sp.simplify(sp.diff(M * F, y) - sp.diff(N * F, x)) == 0)
G = x**2 / 2 + x * y + sp.log(sp.sin(y))
implicit("1(f) x^2/2 + xy + ln sin y = 0", G, M, N, (0, sp.pi / 2), 0)

# ---- 1(g)：dy/dx = e^{9y-x}，y(0)=0 → y = [x - ln(9 - 8e^x)]/9
yg = (x - sp.log(9 - 8 * sp.exp(x))) / 9
ok("1(g) 代回", zero(sp.diff(yg, x) - sp.exp(9 * yg - x), [x], -1, 0.1))
ok("1(g) y(0)=0", sp.simplify(yg.subs(x, 0)) == 0)
ok("1(g) 存在區間端點 x = ln(9/8)", sp.simplify(sp.solve(9 - 8 * sp.exp(x), x)[0] - sp.log(sp.Rational(9, 8))) == 0)

# ---- 1(h)：F = x^a y^b，a=3, b=1
a, b = sp.symbols("a b")
M, N = 5 * x * y**2 - 2 * y, 3 * x**2 * y - x
Fab = x**a * y**b
expr = sp.expand((sp.diff(Fab * M, y) - sp.diff(Fab * N, x)) / (x**a * y**b))
sol = sp.solve([sp.Poly(expr, x, y).coeff_monomial(x * y), sp.Poly(expr, x, y).coeff_monomial(1)], [a, b], dict=True)
ok("1(h) a=3、b=1", sol == [{a: 3, b: 1}])
G = x**5 * y**3 - x**4 * y**2 / 2
implicit("1(h) x^5y^3 - x^4y^2/2 = 1/2", G, M, N, (1, 1), sp.Rational(1, 2))

# ---- 108級 1(c)：x y' - 4y = x^6 e^x，y(1)=1 → y = x^4 (x e^x - e^x + 1)
yc8 = x**4 * (x * sp.exp(x) - sp.exp(x) + 1)
ok("108 1(c) 代回", zero(x * sp.diff(yc8, x) - 4 * yc8 - x**6 * sp.exp(x)))
ok("108 1(c) y(1)=1", sp.simplify(yc8.subs(x, 1)) == 1)

# ---- 108級 1(e)（別名卡 am1-112a-m2，初始條件不同）：y(0)=3 → x^2e^{3y}+e^x-y^3/3 = -8
G = x**2 * sp.exp(3 * y) + sp.exp(x) - y**3 / 3
ok("108 1(e) y(0)=3 → C = -8", sp.simplify(G.subs({x: 0, y: 3}) + 8) == 0)

# ---- 108級 1(f)：(3xy+y^2)dx + (x^2+xy)dy = 0，y(1)=1，F = x
M, N = 3 * x * y + y**2, x**2 + x * y
D = sp.diff(M, y) - sp.diff(N, x)
ok("108 1(f) Δ/N = 1/x", sp.simplify(D / N - 1 / x) == 0)
G = x**3 * y + x**2 * y**2 / 2
implicit("108 1(f) x^3y + x^2y^2/2 = 3/2", G, M, N, (1, 1), sp.Rational(3, 2))
# 與老師的對數形式等價：4 ln x + ln(y/x) + ln(y/x+2) = ln 3 ⇔ x^2 y (y+2x) = 3
ok("108 1(f) 老師對數形式等價", sp.simplify(sp.expand(x**4 * (y / x) * (y / x + 2)) - (x**2 * y**2 + 2 * x**3 * y)) == 0)

# ---- 108級 2：冷卻 T(0)=100、Ts=25、T(3)=90，求 T=50 的時間
k = sp.log(sp.Rational(15, 13)) / 3
T = 25 + 75 * sp.exp(-k * t)
ok("108 2 T(3)=90", sp.simplify(T.subs(t, 3) - 90) == 0)
tt = sp.log(3) / k
ok("108 2 T(t*)=50", sp.simplify(T.subs(t, tt) - 50) == 0)
ok("108 2 t* ≈ 23.03 min", abs(float(tt) - 23.03) < 0.01)

# ---- 108級 3：RC 串聯，V = V0 cos ωt，求 i(t)
R, Cc, V0, w, Kc = sp.symbols("R C V_0 omega K", positive=True)
i_t = V0 / R / ((1 / (R * Cc))**2 + w**2) * (-w * sp.sin(w * t) / (R * Cc) + w**2 * sp.cos(w * t)) + Kc * sp.exp(-t / (R * Cc))
ok("108 3 R i' + i/C = -ω V0 sin ωt", zero(R * sp.diff(i_t, t) + i_t / Cc + w * V0 * sp.sin(w * t)))
# 穩態部分 = V0/|Z| cos(ωt+θ)，tanθ = 1/(ωRC)
iss = i_t.subs(Kc, 0)
th = sp.atan(1 / (w * R * Cc))
ok("108 3 穩態 = V0/sqrt(R^2+1/(ωC)^2) cos(ωt+θ)",
   zero(iss - V0 / sp.sqrt(R**2 + 1 / (w * Cc)**2) * sp.cos(w * t + th)))

# ---- 109級上 第2次期中(Euler) 4：RC 串聯，V0 sin ωt，求電阻電流（穩態）
q = sp.Function("q")
i_ss = V0 / sp.sqrt(R**2 + 1 / (w * Cc)**2) * sp.sin(w * t + th)
qss = sp.integrate(i_ss, t)
ok("109a E4 穩態 i 滿足 R i' + i/C = ω V0 cos ωt", zero(R * sp.diff(i_ss, t) + i_ss / Cc - w * V0 * sp.cos(w * t)))
ok("109a E4 對應的 q 滿足 R q' + q/C = V0 sin ωt", zero(R * sp.diff(qss, t) + qss / Cc - V0 * sp.sin(w * t)))
# 老師答案 φ = -arctan(ωRC) 配 sin：不滿足（應配 cos）
i_teacher = V0 / sp.sqrt(R**2 + 1 / (w * Cc)**2) * sp.sin(w * t - sp.atan(w * R * Cc))
ok("109a E4 老師版 sin(ωt − arctan ωRC) 不滿足（確認誤植）",
   not zero(R * sp.diff(i_teacher, t) + i_teacher / Cc - w * V0 * sp.cos(w * t)))
i_cos = V0 / sp.sqrt(R**2 + 1 / (w * Cc)**2) * sp.cos(w * t - sp.atan(w * R * Cc))
ok("109a E4 改成 cos(ωt − arctan ωRC) 即正確", zero(i_cos - i_ss))

# ---- 新自編 2a：y' + y = x y^3，y(0)=1
ys = 1 / sp.sqrt(x + sp.Rational(1, 2) + sp.exp(2 * x) / 2)
ok("自編 2a 代回", zero(sp.diff(ys, x) + ys - x * ys**3, [x], -0.5, 1.5))
ok("自編 2a y(0)=1", sp.simplify(ys.subs(x, 0)) == 1)
xs = sp.nsolve(x + sp.Rational(1, 2) + sp.exp(2 * x) / 2, x, -0.6)
ok("自編 2a 存在區間左端 x* ≈ -0.6392", abs(float(xs) + 0.6392) < 1e-3)

bad = [n for n, c in results if not c]
for n, c in results:
    print(("PASS " if c else "FAIL ") + n)
print(f"{len(results) - len(bad)}/{len(results)} passed")
sys.exit(1 if bad else 0)
