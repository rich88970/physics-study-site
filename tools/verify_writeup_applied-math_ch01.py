"""應用數學 第 1 章：考試書寫版（exam.html）改寫成「背公式 → 代數字」格式後，
新出現的中間式子與數值用 sympy 逐一驗算。

用法：python tools/verify_writeup_applied-math_ch01.py     全部通過時結束碼為 0。
"""
import math
import random
import sys

import sympy as sp

x, y, t, v, u = sp.symbols("x y t v u", real=True)
a, b = sp.symbols("a b", real=True)
R, Cc, V0, w, eps, m, g, k = sp.symbols("R C V0 omega epsilon m g k", positive=True)
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


def ode_ok(name, yexpr, rhs, lo=0.3, hi=1.3, var=x):
    """顯式解 y(var) 代回 y' = rhs(var, y)。"""
    ok(name, zero(sp.diff(yexpr, var) - rhs.subs(y, yexpr), None, lo, hi))


def implicit(name, G, M, N, pt, Cval, lo=0.3, hi=1.3):
    ok(name + "：dG ∥ M dx + N dy", zero(sp.diff(G, x) * N - sp.diff(G, y) * M, [x, y], lo, hi))
    ok(name + "：初始點代入", sp.simplify(G.subs({x: pt[0], y: pt[1]}) - Cval) == 0)


def pf(expr, var, parts):
    ok("部分分式 " + str(expr), zero(sp.together(expr - sum(parts)), [var], 3.3, 4.3))


# ===== 第 1 節 可分離 =====
# am1-ex-sep
ok("ex-sep C=-768", (0 + 4) ** 4 * (1 - 4 * 1) == -768)
ode_ok("ex-sep y=1/4+192/(x^2+4)^4", sp.Rational(1, 4) + 192 / (x**2 + 4) ** 4, (2 * x - 8 * x * y) / (x**2 + 4))
ok("ex-sep ∫dy/(1-4y)=-1/4 ln|1-4y|", zero(sp.diff(-sp.log(1 - 4 * y) / 4, y) - 1 / (1 - 4 * y), [y], -2, -1))
# am1-hw-1
implicit("hw-1 x^4 sin(y^2)=1", x**4 * sp.sin(y**2), 2 * sp.sin(y**2), x * y * sp.cos(y**2), (1, sp.sqrt(sp.pi / 2)), 1)
# am1-113a-m2
pf(1 / (9 - y**2), y, [sp.Rational(1, 6) / (3 - y), sp.Rational(1, 6) / (3 + y)])
ode_ok("113a-m2 y=3tanh3x", 3 * sp.tanh(3 * x), 9 - y**2)
ok("113a-m2 3(e^6x-1)/(e^6x+1)=3tanh3x", zero(3 * (sp.exp(6 * x) - 1) / (sp.exp(6 * x) + 1) - 3 * sp.tanh(3 * x), [x]))
# am1-109b-1a
implicit("109b-1a ln y+y^2=sin x+1", sp.log(y) + y**2 - sp.sin(x), -y * sp.cos(x), 1 + 2 * y**2, (0, 1), 1)
Gbad = sp.log(y) + y**2 + sp.sin(x)
ok("109b-1a 考卷 -sin x 微分後 y'=-y cos x/(1+2y^2)",
   zero(-sp.diff(Gbad, x) / sp.diff(Gbad, y) + y * sp.cos(x) / (1 + 2 * y**2), [x, y]))
# am1-109b-1g
ok("109b-1g C=8/9", sp.Rational(-1, 9) + 1 == sp.Rational(8, 9))
yg = (x - sp.log(9 - 8 * sp.exp(x))) / 9
ode_ok("109b-1g y", yg, sp.exp(9 * y - x), -0.5, 0.1)
ok("109b-1g -1/9 ln(9e^-x-8) 同式", zero(-sp.log(9 * sp.exp(-x) - 8) / 9 - yg, [x], -0.5, 0.1))
ok("109b-1g ln(9/8)≈0.118", abs(math.log(9 / 8) - 0.118) < 5e-4)
# am1-109b-1d
ok("109b-1d xv'=(v+1)(v+2)/(1-v)", zero((2 + 4 * v) / (1 - v) - v - (v + 1) * (v + 2) / (1 - v), [v], -0.5, 0.5))
pf((1 - v) / ((v + 1) * (v + 2)), v, [2 / (v + 1), -3 / (v + 2)])
implicit("109b-1d (y+x)^2/(y+2x)^3=K", (y + x) ** 2 / (y + 2 * x) ** 3, 2 * x + 4 * y, y - x, (1, 0), sp.Rational(1, 8))
ok("109b-1d K=1/8", sp.Rational(1, 8) * 8 == 1)
# am1-self-01a
ode_ok("self-01a y=tan x-x-1", sp.tan(x) - x - 1, (x + y + 1) ** 2, -1, 1)
# am1-self-01b
pf(1 / (y**2 - 1), y, [sp.Rational(1, 2) / (y - 1), -sp.Rational(1, 2) / (y + 1)])
for lab, ys, Kv in [("(a)", (1 - x**2) / (1 + x**2), -1), ("(c)", (2 + x**2) / (2 - x**2), sp.Rational(1, 2))]:
    ode_ok("self-01b " + lab, ys, (y**2 - 1) / x, 0.3, 1.3)
    ok("self-01b %s (y-1)/(y+1)=Kx^2" % lab, zero((ys - 1) / (ys + 1) - Kv * x**2, [x]))

# ===== 第 2 節 線性 =====
I = sp.exp(2 * x) * (2 * sp.sin(x) - sp.cos(x)) / 5
ok("ex-lin ∫e^{2x}sin x", zero(sp.diff(I, x) - sp.exp(2 * x) * sp.sin(x), [x]))
ok("ex-lin C=6/5", sp.Rational(-1, 5) + sp.Rational(6, 5) == 1)
ode_ok("ex-lin y", sp.exp(x) / 5 * (2 * sp.sin(x) - sp.cos(x)) + sp.Rational(6, 5) * sp.exp(-x), sp.exp(x) * sp.sin(x) - y)
# 公式 ∫e^{ax}sin bx
Fs = sp.exp(a * x) * (a * sp.sin(b * x) - b * sp.cos(b * x)) / (a**2 + b**2)
ok("公式 ∫e^{ax}sin bx", zero(sp.diff(Fs, x) - sp.exp(a * x) * sp.sin(b * x), [x, a, b]))
Fc = sp.exp(a * x) * (a * sp.cos(b * x) + b * sp.sin(b * x)) / (a**2 + b**2)
ok("公式 ∫e^{ax}cos bx", zero(sp.diff(Fc, x) - sp.exp(a * x) * sp.cos(b * x), [x, a, b]))
# am1-hw-2
xs = sp.cosh(y)
ok("hw-2 x=cosh y 滿足 dx/dy=e^y-x", zero(sp.diff(xs, y) - (sp.exp(y) - xs), [y]))
ok("hw-2 xe^y=e^{2y}/2+1/2 ⟺ x=cosh y", zero(xs * sp.exp(y) - sp.exp(2 * y) / 2 - sp.Rational(1, 2), [y]))
# am1-hw-3
F = x * sp.exp(x)
ok("hw-3 F'=pF", zero(sp.diff(F, x) - (1 / x + 1) * F, [x]))
yh = -sp.exp(-x) * sp.cos(2 * x) / (2 * x) + 3 * sp.exp(-x) / x
ode_ok("hw-3 y", yh, (sp.exp(-x) * sp.sin(2 * x) - (1 + x) * y) / x)
# am1-112a-m1
ode_ok("112a-m1 y", (x**2 / 2 + 1) * sp.exp(-x**2), x * sp.exp(-x**2) - 2 * x * y)
# am1-114a-m1
pf(3 * x / ((x - 2) * (x + 1)), x, [2 / (x - 2), 1 / (x + 1)])
F = (x - 2) ** 2 * (x + 1)
ok("114a-m1 F'=pF", zero(sp.diff(F, x) - 3 * x / ((x - 2) * (x + 1)) * F, [x], -0.5, 1.5))
ok("114a-m1 Fq=(x-2)^3", zero(F * (x - 2) / (x + 1) - (x - 2) ** 3, [x], -0.5, 1.5))
ok("114a-m1 C=7/4", 2 - sp.Rational(1, 4) == sp.Rational(7, 4))
ode_ok("114a-m1 y", ((x - 2) ** 4 + 7) / (4 * (x - 2) ** 2 * (x + 1)), (x**2 - 4 * x + 4 - 3 * x * y) / (x**2 - x - 2), -0.5, 1.5)
# am1-109b-1b
ok("109b-1b ∫dx/(x ln x)=ln ln x", zero(sp.diff(sp.log(sp.log(x)), x) - 1 / (x * sp.log(x)), [x], 1.5, 3))
ode_ok("109b-1b y=(1-x)/ln x", (1 - x) / sp.log(x), -(x + y) / (x * sp.log(x)), 1.5, 3)
ok("109b-1b x→1 極限 -1", sp.limit((1 - x) / sp.log(x), x, 1) == -1)
# am1-108b-1c
ok("108b-1c ∫xe^x", zero(sp.diff(x * sp.exp(x) - sp.exp(x), x) - x * sp.exp(x), [x]))
ode_ok("108b-1c y", x**4 * (x * sp.exp(x) - sp.exp(x) + 1), (x**6 * sp.exp(x) + 4 * y) / x)
# am1-109b-1c
vv = 2 * x - x**2
ok("109b-1c v'-v/x=-x", zero(sp.diff(vv, x) - vv / x + x, [x]))
ode_ok("109b-1c y=1/(2x-x^2)", 1 / vv, x * y**2 - y / x, 0.3, 1.7)
# am1-self-02a
vs = x + sp.Rational(1, 2) + sp.exp(2 * x) / 2
ok("self-02a v'-2v=-2x", zero(sp.diff(vs, x) - 2 * vs + 2 * x, [x]))
ok("self-02a ∫-2xe^{-2x}", zero(sp.diff(x * sp.exp(-2 * x) + sp.exp(-2 * x) / 2, x) + 2 * x * sp.exp(-2 * x), [x]))
ode_ok("self-02a y=v^{-1/2}", vs ** sp.Rational(-1, 2), x * y**3 - y, 0, 1)
vf = lambda z: z + 0.5 + 0.5 * math.exp(2 * z)
ok("self-02a v(-0.6)≈0.0506", abs(vf(-0.6) - 0.0506) < 5e-5)
ok("self-02a v(-0.65)≈-0.0137", abs(vf(-0.65) + 0.0137) < 5e-5)
ok("self-02a 1+e^{-1.3}≈1.2725", abs(1 + math.exp(-1.3) - 1.2725) < 5e-5)
x1 = -0.65 - vf(-0.65) / (1 + math.exp(-1.3))
ok("self-02a 牛頓一步 ≈-0.6392", abs(x1 + 0.6392) < 5e-5)
root = float(sp.nsolve(vs, x, -0.64))
ok("self-02a x*≈-0.639", abs(root + 0.639) < 5e-4)
# am1-self-02b
y1 = 0.5 * (1 - math.exp(-2))
ok("self-02b e^-2≈0.1353", abs(math.exp(-2) - 0.1353) < 5e-5)
ok("self-02b y(1)=0.4323", abs(y1 - 0.4323) < 5e-5)
C2 = 0.5 * (math.exp(2) - 1)
ok("self-02b C2 連續", abs(C2 * math.exp(-2) - y1) < 1e-12)
ok("self-02b y(2)=0.0585", abs(C2 * math.exp(-4) - 0.0585) < 5e-5)

# ===== 第 3 節 正合 =====
def exact_ok(name, M, N, f, pt, Cval):
    ok(name + " M_y=N_x", zero(sp.diff(M, y) - sp.diff(N, x), [x, y]))
    ok(name + " f_x=M", zero(sp.diff(f, x) - M, [x, y]))
    ok(name + " f_y=N", zero(sp.diff(f, y) - N, [x, y]))
    ok(name + " C", sp.simplify(f.subs({x: pt[0], y: pt[1]}) - Cval) == 0)


exact_ok("ex-exact", x**2 - 2 * x * y, sp.sin(y) - x**2, x**3 / 3 - x**2 * y - sp.cos(y), (1, 0), sp.Rational(-2, 3))
exact_ok("110a-m1", 4 + 12 * x * y, 2 * y + sp.exp(y) + 6 * x**2, 4 * x + 6 * x**2 * y + y**2 + sp.exp(y), (0, 0), 1)
f112 = x**2 * sp.exp(3 * y) + sp.exp(x) - y**3 / 3
exact_ok("112a-m2", 2 * x * sp.exp(3 * y) + sp.exp(x), 3 * x**2 * sp.exp(3 * y) - y**2, f112, (0, 1), sp.Rational(2, 3))
ok("112a-m2 (0,3) C=-8", f112.subs({x: 0, y: 3}) == -8)
M113 = sp.exp(2 * y) - y * sp.cos(x * y)
N113 = 2 * x * sp.exp(2 * y) - x * sp.cos(x * y) + 2 * y
ok("113a-m1 M_y 展開式", zero(sp.diff(M113, y) - (2 * sp.exp(2 * y) - sp.cos(x * y) + x * y * sp.sin(x * y)), [x, y]))
exact_ok("113a-m1", M113, N113, x * sp.exp(2 * y) - sp.sin(x * y) + y**2, (0, 2), 4)
exact_ok("109b-1e", 3 * x**2 - 2 * x * y + 2, 6 * y**2 - x**2 + 3, x**3 - x**2 * y + 2 * x + 2 * y**3 + 3 * y, (1, 0), 3)
M3a = y * sp.cos(x) + 2 * x * sp.exp(y)
N3a = sp.sin(x) + x**2 * sp.exp(y) + y
ok("self-03a N(0,y)=y", sp.simplify(N3a.subs(x, 0) - y) == 0)
exact_ok("self-03a", M3a, N3a, y * sp.sin(x) + x**2 * sp.exp(y) + y**2 / 2, (0, 1), sp.Rational(1, 2))
exact_ok("self-03b", 2 * x * y + 3, x**2 - 1, x**2 * y + 3 * x - y, (0, 2), -2)
F = 1 - x**2
ok("self-03b 線性 F'=pF", zero(sp.diff(F, x) - 2 * x / (x**2 - 1) * F, [x], -0.9, 0.9))
ok("self-03b 線性 Fq=3", zero(F * (-3) / (x**2 - 1) - 3, [x], -0.9, 0.9))
ode_ok("self-03b y=(2+3x)/(1-x^2)", (2 + 3 * x) / (1 - x**2), -(2 * x * y + 3) / (x**2 - 1), -0.9, 0.9)

# ===== 第 4 節 非正合 =====
def nonexact_ok(name, M, N, Delta, F, f, pt=None, Cval=None):
    ok(name + " Δ", zero(sp.diff(M, y) - sp.diff(N, x) - Delta, [x, y]))
    ok(name + " (FM)_y=(FN)_x", zero(sp.diff(F * M, y) - sp.diff(F * N, x), [x, y]))
    ok(name + " f_x=FM", zero(sp.diff(f, x) - F * M, [x, y]))
    ok(name + " f_y=FN", zero(sp.diff(f, y) - F * N, [x, y]))
    if pt is not None:
        ok(name + " C", sp.simplify(f.subs({x: pt[0], y: pt[1]}) - Cval) == 0)


Mn, Nn = 3 * x * sp.sin(2 * y) - 2 * y, 2 * x**2 * sp.cos(2 * y) - x
ok("ex-nonexact Δ/N=1/x", zero((2 * x * sp.cos(2 * y) - 1) / Nn - 1 / x, [x, y]))
nonexact_ok("ex-nonexact", Mn, Nn, 2 * x * sp.cos(2 * y) - 1, x, x**3 * sp.sin(2 * y) - x**2 * y)
Mh, Nh = sp.cos(y), -2 * (x - y) * sp.sin(y) - sp.cos(y)
ok("hw-5 Δ/M=tan y", zero(sp.sin(y) / Mh - sp.tan(y), [y]))
ok("hw-5 e^{-∫tan y}=cos y", zero(sp.diff(sp.cos(y), y) / sp.cos(y) + sp.tan(y), [y]))
hp = y * sp.sin(2 * y) - sp.cos(y) ** 2
ok("hw-5 ∫y sin2y", zero(sp.diff(-y / 2 * sp.cos(2 * y) + sp.sin(2 * y) / 4, y) - y * sp.sin(2 * y), [y]))
ok("hw-5 ∫cos^2 y", zero(sp.diff(y / 2 + sp.sin(2 * y) / 4, y) - sp.cos(y) ** 2, [y]))
ok("hw-5 h=-y cos^2 y", zero(sp.diff(-y * sp.cos(y) ** 2, y) - hp, [y]) and zero(-y / 2 * sp.cos(2 * y) - y / 2 + y * sp.cos(y) ** 2, [y]))
nonexact_ok("hw-5", Mh, Nh, sp.sin(y), sp.cos(y), (x - y) * sp.cos(y) ** 2, (1, 0), 1)
M1, N1 = y**2 + x * y**3, 5 * y**2 - x * y + y**3 * sp.sin(y)
ok("111a-m1 Δ/M=3/y", zero(3 * y * (1 + x * y) / M1 - 3 / y, [x, y]))
nonexact_ok("111a-m1", M1, N1, 3 * y * (1 + x * y), y**-3, x / y + x**2 / 2 + 5 * sp.log(y) - sp.cos(y), (0, sp.pi / 2), 5 * sp.log(sp.pi / 2))
Mf, Nf = (x + y) * sp.sin(y), x * sp.sin(y) + sp.cos(y)
ok("109b-1f Δ/M=cot y", zero((x + y) * sp.cos(y) / Mf - sp.cot(y), [x, y]))
nonexact_ok("109b-1f", Mf, Nf, (x + y) * sp.cos(y), 1 / sp.sin(y), x**2 / 2 + x * y + sp.log(sp.sin(y)), (0, sp.pi / 2), 0)
# 109b-1h：x^a y^b
Mh8, Nh8 = 5 * x * y**2 - 2 * y, 3 * x**2 * y - x
Fab = x**a * y**b
lhs = sp.expand(sp.diff(Fab * Mh8, y) / (x**a * y**b))
rhs = sp.expand(sp.diff(Fab * Nh8, x) / (x**a * y**b))
ok("109b-1h (FM)_y 展開", zero(lhs - (5 * (b + 2) * x * y - 2 * (b + 1)), [x, y, a, b]))
ok("109b-1h (FN)_x 展開", zero(rhs - (3 * (a + 2) * x * y - (a + 1)), [x, y, a, b]))
ok("109b-1h a=3,b=1", sp.solve([5 * (b + 2) - 3 * (a + 2), 2 * (b + 1) - (a + 1)], [a, b]) == {a: 3, b: 1})
nonexact_ok("109b-1h", Mh8, Nh8, 4 * x * y - 1, x**3 * y, x**5 * y**3 - x**4 * y**2 / 2, (1, 1), sp.Rational(1, 2))
M8, N8 = 3 * x * y + y**2, x**2 + x * y
nonexact_ok("108b-1f", M8, N8, x + y, x, x**3 * y + x**2 * y**2 / 2, (1, 1), sp.Rational(3, 2))
ok("108b-1f 考卷對數式 ⟺ x^2y(y+2x)=3",
   zero(sp.exp(4 * sp.log(x) + sp.log(y / x) + sp.log(y / x + 2)) - x**2 * y * (y + 2 * x), [x, y]))
M4, N4 = 3 * y + 4 * x * y**2, 2 * x + 3 * x**2 * y
lhs = sp.expand(sp.diff(Fab * M4, y) / (x**a * y**b))
rhs = sp.expand(sp.diff(Fab * N4, x) / (x**a * y**b))
ok("self-04a (FM)_y 展開", zero(lhs - (3 * (b + 1) + 4 * (b + 2) * x * y), [x, y, a, b]))
ok("self-04a (FN)_x 展開", zero(rhs - (2 * (a + 1) + 3 * (a + 2) * x * y), [x, y, a, b]))
ok("self-04a a=2,b=1", sp.solve([3 * (b + 1) - 2 * (a + 1), 4 * (b + 2) - 3 * (a + 2)], [a, b]) == {a: 2, b: 1})
ok("self-04a Δ/N、Δ/M", zero((1 + 2 * x * y) / N4 - (1 + 2 * x * y) / (x * (2 + 3 * x * y)), [x, y])
   and zero((1 + 2 * x * y) / M4 - (1 + 2 * x * y) / (y * (3 + 4 * x * y)), [x, y]))
nonexact_ok("self-04a", M4, N4, 1 + 2 * x * y, x**2 * y, x**3 * y**2 + x**4 * y**3, (1, 1), 2)
M4b, N4b = y, 2 * x - y * sp.exp(y)
ok("self-04b ∫y^2e^y", zero(sp.diff((y**2 - 2 * y + 2) * sp.exp(y), y) - y**2 * sp.exp(y), [y]))
nonexact_ok("self-04b (a)", M4b, N4b, -1, y, x * y**2 - (y**2 - 2 * y + 2) * sp.exp(y), (0, 1), -sp.E)
xb = ((y**2 - 2 * y + 2) * sp.exp(y) - sp.E) / y**2
ok("self-04b (b) x'+2x/y=e^y", zero(sp.diff(xb, y) + 2 * xb / y - sp.exp(y), [y]))
ok("self-04b (b) x(1)=0", sp.simplify(xb.subs(y, 1)) == 0)

# ===== 第 5 節 應用 =====
q = sp.Function("q")
qd = Cc * eps * sp.exp(-t / (R * Cc))
ok("ex-rc 放電 q/C+Rq'=0", zero(qd / Cc + R * sp.diff(qd, t), [t, R, Cc, eps]))
ok("ex-rc i=-ε/R e^{-t/RC}", zero(sp.diff(qd, t) + eps / R * sp.exp(-t / (R * Cc)), [t, R, Cc, eps]))
qc = Cc * eps * (1 - sp.exp(-t / (R * Cc)))
ok("ex-rc 充電 q/C+Rq'=ε 且 q(0)=0", zero(qc / Cc + R * sp.diff(qc, t) - eps, [t, R, Cc, eps]) and qc.subs(t, 0) == 0)
ok("ex-rc ε/R·RC=Cε", sp.simplify(eps / R * R * Cc - Cc * eps) == 0)
# ex-ac
A = 1 / (R * Cc)
lhs = V0 / R * (R**2 * Cc**2) / (1 + w**2 * R**2 * Cc**2) * (sp.sin(w * t) / (R * Cc) - w * sp.cos(w * t))
rhs = (Cc * V0 * sp.sin(w * t) - w * R * Cc**2 * V0 * sp.cos(w * t)) / (1 + w**2 * R**2 * Cc**2)
ok("ex-ac 乘進括號", zero(lhs - rhs, [t, R, Cc, V0, w]))
ok("ex-ac a^2+b^2", zero(A**2 + w**2 - (1 + w**2 * R**2 * Cc**2) / (R**2 * Cc**2), [R, Cc, w]))
K = sp.Symbol("K")
qa = rhs + K * sp.exp(-t / (R * Cc))
ok("ex-ac q 滿足方程", zero(sp.diff(qa, t) + qa / (R * Cc) - V0 / R * sp.sin(w * t), [t, R, Cc, V0, w, K]))
phi = sp.atan(w * R * Cc)
ok("ex-ac 合成 sin(ωt-φ)", zero(Cc * V0 / sp.sqrt(1 + w**2 * R**2 * Cc**2) * sp.sin(w * t - phi) - rhs, [t, R, Cc, V0, w]))
# 110a-m2
vt = sp.sqrt(m * g / k)
vsol = vt * sp.tanh(sp.sqrt(g * k / m) * t)
ok("110a-m2 m v'=mg-kv^2", zero(m * sp.diff(vsol, t) - (m * g - k * vsol**2), [t, m, g, k]))
ok("110a-m2 2k v_t/m=2√(gk/m)", zero(2 * k * vt / m - 2 * sp.sqrt(g * k / m), [m, g, k]))
vv = sp.Symbol("vv", positive=True)
VT = sp.Symbol("VT", positive=True)
ok("110a-m2 部分分式", zero(1 / (VT**2 - vv**2) - (1 / (VT - vv) + 1 / (VT + vv)) / (2 * VT), [vv, VT], 0.1, 0.5))
# 108b-2
kk = math.log(15 / 13) / 3
ok("108b-2 e^{-3k}=13/15", abs(math.exp(-3 * kk) - 13 / 15) < 1e-12)
ok("108b-2 k≈0.04770", abs(kk - 0.04770) < 5e-6)
ok("108b-2 ln3≈1.09861、ln(15/13)≈0.14310", abs(math.log(3) - 1.09861) < 5e-6 and abs(math.log(15 / 13) - 0.14310) < 5e-6)
ok("108b-2 t*≈23.0", abs(math.log(3) / kk - 23.0) < 0.05)
# 108b-3
ii = V0 / R / (A**2 + w**2) * (-A * w * sp.sin(w * t) + w**2 * sp.cos(w * t)) + K * sp.exp(-A * t)
ok("108b-3 Ri'+i/C=-ωV0 sin ωt", zero(R * sp.diff(ii, t) + ii / Cc + w * V0 * sp.sin(w * t), [t, R, Cc, V0, w, K]))
ee = -w * V0 / R * sp.exp(A * t) * (A * sp.sin(w * t) - w * sp.cos(w * t)) / (A**2 + w**2)
ok("108b-3 e^{at}i 式", zero(sp.diff(ee, t) + w * V0 / R * sp.exp(A * t) * sp.sin(w * t), [t, R, Cc, V0, w]))
# 109a-e4
ie = w * V0 / R * (A * sp.cos(w * t) + w * sp.sin(w * t)) / (A**2 + w**2)
ok("109a-e4 Ri'+i/C=ωV0 cos ωt", zero(R * sp.diff(ie, t) + ie / Cc - w * V0 * sp.cos(w * t), [t, R, Cc, V0, w]))
theta = sp.atan(1 / (w * R * Cc))
amp = V0 / sp.sqrt(R**2 + 1 / (w**2 * Cc**2))
ok("109a-e4 振幅化簡", zero(w * V0 / (R * sp.sqrt(A**2 + w**2)) - amp, [R, Cc, V0, w]))
ok("109a-e4 合成 sin(ωt+θ)", zero(amp * sp.sin(w * t + theta) - ie, [t, R, Cc, V0, w]))
ok("109a-e4 改寫 cos(ωt-tan⁻¹ωRC)", zero(amp * sp.cos(w * t - sp.atan(w * R * Cc)) - ie, [t, R, Cc, V0, w]))
ok("109a-e4 考卷 sin(ωt-tan⁻¹ωRC) 不對", not zero(amp * sp.sin(w * t - sp.atan(w * R * Cc)) - ie, [t, R, Cc, V0, w]))
# self-05a
Q = 2 * (100 + t) - 2 * 10**6 / (100 + t) ** 2
ok("self-05a Q'=6-2Q/(100+t)", zero(sp.diff(Q, t) - (6 - 2 * Q / (100 + t)), [t], 0, 100))
ok("self-05a Q(0)=0", Q.subs(t, 0) == 0)
ok("self-05a Q(100)=350、1.75 g/L", Q.subs(t, 100) == 350 and sp.Rational(350, 200) == sp.Rational(7, 4))
# self-05b
v0n, vtn, gn = 20.0, 30.0, 9.8
ok("self-05b 30/9.8≈3.061、atan(2/3)≈0.5880", abs(vtn / gn - 3.061) < 5e-4 and abs(math.atan(2 / 3) - 0.5880) < 5e-5)
ok("self-05b t_top≈1.800", abs(vtn / gn * math.atan(v0n / vtn) - 1.800) < 5e-4)
ok("self-05b 900/19.6≈45.92、ln(13/9)≈0.3677", abs(900 / 19.6 - 45.92) < 5e-3 and abs(math.log(13 / 9) - 0.3677) < 5e-5)
# 精確值 16.8853，四捨五入 16.89（2026-10-25 已把正文、答案、書寫版由 16.88 改成 16.89）
ok("self-05b h≈16.89", abs(vtn**2 / (2 * gn) * math.log(1 + v0n**2 / vtn**2) - 16.89) < 5e-3)
ok("self-05b 真空 2.041 s、20.41 m", abs(v0n / gn - 2.041) < 5e-4 and abs(v0n**2 / (2 * gn) - 20.41) < 5e-3)
VTs = sp.Symbol("VTs", positive=True)
ok("self-05b ∫dv/(1+v²/c²)=c·atan(v/c)", zero(sp.diff(VTs * sp.atan(vv / VTs), vv) - 1 / (1 + vv**2 / VTs**2), [vv, VTs]))
ok("self-05b ∫v dv/(1+v²/c²)=(c²/2)ln u", zero(sp.diff(VTs**2 / 2 * sp.log(1 + vv**2 / VTs**2), vv) - vv / (1 + vv**2 / VTs**2), [vv, VTs]))

bad = [n for n, r in results if not r]
for n, r in results:
    print(("OK  " if r else "FAIL") + "  " + n)
print(f"\n{len(results) - len(bad)}/{len(results)} 通過")
sys.exit(1 if bad else 0)
