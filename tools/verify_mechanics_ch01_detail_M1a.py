"""驗算力學 Lecture 1 第 1–7 節（01-calculus … 07-derivative）詳細解法中新寫出的數值與中間式。

用法：python tools/verify_mechanics_ch01_detail_M1a.py   （需要 numpy、sympy）
這些卡片改寫成「條件表 → 為什麼這樣解 → 逐步代入」後，新增了許多中間值（例如 464.5、0.9232、16.155、
3/√84、19/49…）與分成多行的推導；這裡逐項重算，並用隨機向量、符號運算檢查各個恆等式。
"""
import itertools
import math
import sys

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
ok = True
rng = np.random.default_rng(20261021)


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(("OK  " if cond else "FAIL"), name)


def close(name, got, want, tol=1e-6):
    g = np.array(got, dtype=float); w = np.array(want, dtype=float)
    check(f"{name}: {np.round(g, 6).tolist()} vs {np.round(w, 6).tolist()}", np.allclose(g, w, atol=tol, rtol=tol))


def zero(name, expr):
    check(name + " (sympy = 0)", sp.simplify(expr) == 0)


def eps(i, j, k):
    return int(np.sign((j - i) * (k - i) * (k - j)))


deg = math.degrees
x, t, s_ = sp.symbols("x t s", real=True)

# ===================== 01 微積分 =====================
close("ex-p7a 導數在 π/2", float(sp.diff(x * sp.sin(x), x).subs(x, sp.pi / 2)), 1)
f = lambda u: u * math.sin(u)
close("ex-p7a 有限差分", (f(1.5708 + 0.001) - f(1.5708 - 0.001)) / 0.002, 1.000, tol=1e-3)
zero("ex-p7b 商數律", sp.diff(sp.sin(x) / x, x) - (x * sp.cos(x) - sp.sin(x)) / x**2)
check("ex-p7b x→0 分子 ≈ -x³/3", sp.series(x * sp.cos(x) - sp.sin(x), x, 0, 4).removeO() == -x**3 / 3)
k, b = sp.symbols("k b", nonzero=True)
zero("ex-p8 對答案微分", sp.diff(sp.log(k * x + b) / k, x) - 1 / (k * x + b))
zero("ex-p9 對答案微分", sp.diff(sp.log(1 + x**2) / 2, x) - x / (1 + x**2))
v0, kk, c = sp.symbols("v0 k c", positive=True)
v_a = v0 * sp.exp(-kk * t)
zero("self-s01-1 (a) v 滿足 dv/dt=-kv", sp.diff(v_a, t) + kk * v_a)
zero("self-s01-1 (a) x(t)", sp.integrate(v_a.subs(t, s_), (s_, 0, t)) - v0 / kk * (1 - sp.exp(-kk * t)))
close("self-s01-1 (a) 停止位置 20/0.5", 20 / 0.5, 40)
v_b = v0 / (1 + c * v0 * t)
zero("self-s01-1 (b) v 滿足 dv/dt=-cv²", sp.diff(v_b, t) + c * v_b**2)
zero("self-s01-1 (b) x(t)", sp.simplify(sp.integrate(v_b.subs(t, s_), (s_, 0, t)) - sp.log(1 + c * v0 * t) / c))
xb = sp.log(1 + c * v0 * t) / c
zero("self-s01-1 (b) v=v0 e^{-cx}", v0 * sp.exp(-c * xb) - v_b)
A2 = 0.03**2 + 0.4**2 / 10**2
close("self-s01-2 A²、A", [0.03**2, 0.4**2 / 100, A2, math.sqrt(A2)], [0.0009, 0.0016, 0.0025, 0.05])
v2 = 0.4**2 + 100 * (0.03**2 - 0.04**2)
close("self-s01-2 v²=0.16-0.07、|v|", [100 * (0.0009 - 0.0016), v2, math.sqrt(v2)], [-0.07, 0.09, 0.3])
# 數值積分 x''=-ω²x 驗證振幅
ts = np.linspace(0, 2, 200001); w = 10.0
xs = 0.03 * np.cos(w * ts) + 0.4 / w * np.sin(w * ts)
close("self-s01-2 數值軌道振幅", np.max(np.abs(xs)), 0.05, tol=1e-4)

# ===================== 02 純量與向量 =====================
A = np.array([3, 1]); B = np.array([1, 2])
rot = lambda V, th: np.array([V[0] * math.cos(th) + V[1] * math.sin(th), -V[0] * math.sin(th) + V[1] * math.cos(th)])
Ap, Bp = rot(A, math.pi / 2), rot(B, math.pi / 2)
close("self-s02-1 A'、B'（90°）", [*Ap, *Bp], [1, -3, 2, -1])
close("self-s02-1 (a) 2 vs 3", [Ap[0] * Bp[0], A[0] * B[0]], [2, 3])
close("self-s02-1 (b)(c) 數值", [Ap @ Bp, Ap[0] * Bp[1] - Ap[1] * Bp[0], A @ B, A[0] * B[1] - A[1] * B[0]], [5, 5, 5, 5])
th = sp.symbols("theta", real=True)
a1, a2, b1, b2 = sp.symbols("A1 A2 B1 B2", real=True)
cs, sn = sp.cos(th), sp.sin(th)
A1p, A2p = a1 * cs + a2 * sn, -a1 * sn + a2 * cs
B1p, B2p = b1 * cs + b2 * sn, -b1 * sn + b2 * cs
zero("self-s02-1 (b) 展開不變", sp.expand(A1p * B1p + A2p * B2p - (a1 * b1 + a2 * b2)).subs(sn**2, 1 - cs**2))
zero("self-s02-1 (c) 展開不變", sp.expand(A1p * B2p - A2p * B1p - (a1 * b2 - a2 * b1)).subs(sn**2, 1 - cs**2))
zero("self-s02-1 A1'B1' 展開式", sp.expand(A1p * B1p) - (a1 * b1 * cs**2 + a1 * b2 * cs * sn + a2 * b1 * sn * cs + a2 * b2 * sn**2))
zero("self-s02-1 A2'B1' 展開式", sp.expand(A2p * B1p) - (-a1 * b1 * sn * cs - a1 * b2 * sn**2 + a2 * b1 * cs**2 + a2 * b2 * cs * sn))
close("self-s02-2 A3、影子長", [8 * math.cos(math.radians(30)), 8 * math.sin(math.radians(30))], [4 * math.sqrt(3), 4])
close("self-s02-2 A1=±2√2", math.sqrt(8), 2 * math.sqrt(2))
for sol, az in (((2 * 2**.5, -2 * 2**.5, 4 * 3**.5), -45), ((-2 * 2**.5, 2 * 2**.5, 4 * 3**.5), 135)):
    v = np.array(sol)
    close(f"self-s02-2 解 {az}°：長 8、⊥(1,1,0)、和 z 夾 30°、方位角",
          [np.linalg.norm(v), v @ [1, 1, 0], deg(math.acos(v[2] / 8)), deg(math.atan2(v[1], v[0]))], [8, 0, 30, az])
close("self-s02-2 -4√3、4√2", [-4 * 3**.5, 4 * 2**.5], [-6.9282, 5.6569], tol=1e-4)
phis = np.linspace(0, 2 * np.pi, 100001)
check("self-s02-2 (b) 圓錐上 A1+A2+A3 恆 > 0（無解）", np.min(4 * np.cos(phis) + 4 * np.sin(phis) + 4 * 3**.5) > 0)
thC = deg(math.acos(1 / 3**.5))
close("self-s02-2 54.7°、24.7°、84.7°", [thC, thC - 30, thC + 30], [54.7356, 24.7356, 84.7356], tol=1e-4)

# ===================== 03 向量加減 =====================
a, bb, cc = np.array([0, 0, 0]), np.array([6, 0, 0]), np.array([0, 3, 3])
g = (a + bb + cc) / 3
close("self-s03-1 a+b+c、G", [*(a + bb + cc), *g], [6, 3, 3, 2, 1, 1])
close("self-s03-1 GA、GB、GC、和", [*(a - g), *(bb - g), *(cc - g), *((a - g) + (bb - g) + (cc - g))],
      [-2, -1, -1, 4, -1, -1, -2, 2, 2, 0, 0, 0])
for P, Q, R in ((a, bb, cc), (bb, cc, a), (cc, a, bb)):
    close("self-s03-1 從頂點走 2/3 中線", P + 2 / 3 * ((Q + R) / 2 - P), g)
phi = math.asin(0.6)
close("self-s03-2 (a) 36.9°、cos、北向 4、30 s", [deg(phi), math.cos(phi), 5 * math.cos(phi), 120 / (5 * math.cos(phi))], [36.8699, 0.8, 4, 30], tol=1e-4)
close("self-s03-2 (b) 24 s、72 m", [120 / 5, 3 * 24], [24, 72])
ph = sp.symbols("phi", real=True)
Dsym = 60 * (3 - 2 * sp.sin(ph)) / sp.cos(ph)
zero("self-s03-2 (c) D 的導數", sp.diff((3 - 2 * sp.sin(ph)) / sp.cos(ph), ph) - (3 * sp.sin(ph) - 2) / sp.cos(ph)**2)
ph0 = math.asin(2 / 3)
Dn = lambda p: 60 * (3 - 2 * np.sin(p)) / np.cos(p)
grid = np.linspace(-1.5, 1.5, 300001)
close("self-s03-2 (c) 數值極小位置", grid[np.argmin(Dn(grid))], ph0, tol=1e-4)
close("self-s03-2 (c) 41.8°、cos=√5/3", [deg(ph0), math.cos(ph0)], [41.8103, 5**.5 / 3], tol=1e-4)
close("self-s03-2 (c) D=60·5/3·3/√5=300/√5=60√5≈134", [60 * (3 - 4 / 3) / (5**.5 / 3), 300 / 5**.5, 60 * 5**.5], [134.164] * 3, tol=1e-3)
close("self-s03-2 (c) t=180/√5=36√5≈80", [120 / (2 * 5**.5 / 3), 180 / 5**.5, 36 * 5**.5], [80.4984] * 3, tol=1e-3)
close("self-s03-2 北向時漂 180 m", 3 * 120 / 2, 180)

# ===================== 04 內積 =====================
A = np.array([2, 1, -2]); B = np.array([3, 0, 4])
close("ex-p26 A1、A·B、|B|、A_B", [A[0], A @ B, np.linalg.norm(B), A @ B / np.linalg.norm(B)], [2, -2, 5, -0.4])
A = np.array([3, -1, 2]); B = np.array([-1, -1, 1])
close("ex-p27 A·B、|A|²、|B|²", [A @ B, A @ A, B @ B], [0, 14, 3])
A = np.array([1, 1]); B = np.array([2, 0])
close("ex-p28 A·B、|A|、|B|、θ", [A @ B, np.linalg.norm(A), np.linalg.norm(B), deg(math.acos(A @ B / np.linalg.norm(A) / np.linalg.norm(B)))], [2, 2**.5, 2, 45])
A = np.array([1, 2, -2]); B = np.array([4, 2, -3]); C = A - B
close("ex-p29 C、|C|", [*C, np.linalg.norm(C)], [-3, 0, 1, 3.1623], tol=1e-4)
close("ex-p29 A·B、|A|、|B|、3√29、cos、θ、B_A",
      [A @ B, np.linalg.norm(A), np.linalg.norm(B), 3 * 29**.5, 14 / (3 * 29**.5), deg(math.acos(14 / (3 * 29**.5))), 14 / 3],
      [14, 3, 5.3852, 16.155, 0.8666, 29.93, 4.6667], tol=2e-3)
for _ in range(3):
    u1 = rng.normal(size=3); u1 /= np.linalg.norm(u1); u2 = rng.normal(size=3); u2 /= np.linalg.norm(u2)
    close("tm-1-2 (1.10)", u1 @ u1, 1)
    S = u1 @ u2
    close("tm-1-2 |PP'|² = 2-2Σ = 2-2cosθ", [np.sum((u1 - u2)**2), 2 - 2 * S], [2 - 2 * S, 2 - 2 * math.cos(math.acos(S))])
d = [np.array(v) for v in ((1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1))]
dots = [int(d[i] @ d[j]) for i, j in itertools.combinations(range(4), 2)]
check(f"tm-1-7 六對內積 {dots}", dots == [1, 1, 1, -1, -1, -1])
close("tm-1-7 70.5°、109.5°", [deg(math.acos(1 / 3)), deg(math.acos(-1 / 3))], [70.5288, 109.4712], tol=1e-4)
for _ in range(3):
    A = rng.normal(size=3); B = rng.normal(size=3)
    th = math.acos(A @ B / np.linalg.norm(A) / np.linalg.norm(B))
    close("tm-1-17 餘弦定律", np.sum((A - B)**2), A @ A + B @ B - 2 * np.linalg.norm(A) * np.linalg.norm(B) * math.cos(th))
    Q = A + np.cross(A, rng.normal(size=3))  # PQ ⟂ A
    close("tm-1-8 平面上的點滿足 A·r=A²", A @ Q, A @ A)
av = np.array([2, -1, 2]); cval = 6; r0 = cval / (av @ av) * av
close("tm-1-16 r0、|r0|=c/a", [*r0, np.linalg.norm(r0)], [4 / 3, -2 / 3, 4 / 3, 2])
aa = sp.symbols("a")
zero("tm-1-41 內積 = 2a(a-1)", sp.expand(2 * aa * aa + (-2) * (2 * aa) + aa * 2 - 2 * aa * (aa - 1)))
for av_ in (0, 1):
    close(f"tm-1-41 a={av_} 垂直", np.array([2 * av_, -2, av_]) @ np.array([av_, 2 * av_, 2]), 0)
P = np.array([1, 2, 3]); u = np.array([1, 1, 1]) / 3**.5
close("self-s04-1 P·û=2√3、P∥、P⊥、|P⊥|", [P @ u, *((P @ u) * u), *(P - (P @ u) * u), np.linalg.norm(P - (P @ u) * u)],
      [2 * 3**.5, 2, 2, 2, -1, 0, 1, 2**.5])
tt = np.linspace(-10, 10, 200001)
dist2 = np.sum((P[None, :] - tt[:, None] * u[None, :])**2, axis=1)
close("self-s04-1 數值最短距離與 t", [math.sqrt(dist2.min()), tt[np.argmin(dist2)]], [2**.5, 2 * 3**.5], tol=1e-4)
Rr = 5; P = np.array([3, 4]); PA = np.array([-5, 0]) - P; PB = np.array([5, 0]) - P
close("self-s04-2 PA、PB、內積", [*PA, *PB, PA @ PB], [-8, -4, 2, -4, 0])
for _ in range(3):
    e = rng.normal(size=3); e /= np.linalg.norm(e); Pv = rng.normal(size=3) * 2; Rv = 1.7
    close("self-s04-2 PA·PB = |P|²-R²", (-Rv * e - Pv) @ (Rv * e - Pv), Pv @ Pv - Rv**2)

# ===================== 05 外積 =====================
for _ in range(3):
    A, B, Cv, D = (rng.normal(size=3) for _ in range(4))
    lhs = sum(eps(i, j, k) * A[i] * B[j] * D[k] for i in range(3) for j in range(3) for k in range(3))
    rhs = sum(eps(i, j, k) * D[i] * A[j] * B[k] for i in range(3) for j in range(3) for k in range(3))
    close("tb-ex16 ε 三重求和兩邊相等", [lhs, rhs], [A @ np.cross(B, D), D @ np.cross(A, B)])
    close("tb-ex16 推論 A·(A×D)=0", A @ np.cross(A, D), 0)
    close("tm-1-21 ε 和 = 行列式", sum(eps(i, j, k) * A[i] * B[j] * Cv[k] for i in range(3) for j in range(3) for k in range(3)), np.linalg.det(np.array([A, B, Cv])))
    six = A[0]*B[1]*Cv[2] + A[1]*B[2]*Cv[0] + A[2]*B[0]*Cv[1] - A[0]*B[2]*Cv[1] - A[1]*B[0]*Cv[2] - A[2]*B[1]*Cv[0]
    close("tm-1-21 六項展開", six, A @ np.cross(B, Cv))
    close("tm-1-22 BAC-CAB", np.cross(A, np.cross(B, Cv)), (A @ Cv) * B - (A @ B) * Cv)
    close("tm-1-11 循環輪換、點叉互換", [np.cross(B, Cv) @ A, np.cross(Cv, A) @ B, A @ np.cross(B, Cv)], [np.cross(A, B) @ Cv] * 3)
    det3 = (Cv[0] * (A[1] * B[2] - A[2] * B[1]) - Cv[1] * (A[0] * B[2] - A[2] * B[0]) + Cv[2] * (A[0] * B[1] - A[1] * B[0]))
    close("tm-1-11 沿第三列展開", det3, np.linalg.det(np.array([A, B, Cv])))
    close("tb-ex17", np.cross(A, B) @ np.cross(Cv, D), (A @ Cv) * (B @ D) - (B @ Cv) * (A @ D))
    close("tb-ex17 點叉互換一步", np.cross(A, B) @ np.cross(Cv, D), A @ np.cross(B, np.cross(Cv, D)))
    lhs23 = np.cross(np.cross(A, B), np.cross(Cv, D))
    close("tm-1-23 第一式", lhs23, (A @ np.cross(B, D)) * Cv - (A @ np.cross(B, Cv)) * D)
    close("tm-1-23 第二式", lhs23, (A @ np.cross(Cv, D)) * B - (B @ np.cross(Cv, D)) * A)
    e = Cv / np.linalg.norm(Cv)
    close("tm-1-24 分解", e * (A @ e) + np.cross(e, np.cross(A, e)), A)
    close("tm-1-24 第二項 ⟂ ê、長 A sinθ", [e @ np.cross(e, np.cross(A, e)), np.linalg.norm(np.cross(e, np.cross(A, e)))],
          [0, np.linalg.norm(A) * math.sin(math.acos(A @ e / np.linalg.norm(A)))])
    # 1-13：造一個 X，再由 A×X、A·X 反解
    X = rng.normal(size=3); Bx = np.cross(A, X); phi_ = A @ X
    close("tm-1-13 解出 X", (phi_ * A + np.cross(Bx, A)) / (A @ A), X)
    close("tm-1-13 A·B=0", A @ Bx, 0)
    # 1-18：三角形正弦定律
    Ct = A - B
    tO = math.acos(A @ B / np.linalg.norm(A) / np.linalg.norm(B))
    tQ = math.acos(Ct @ (-B) / np.linalg.norm(Ct) / np.linalg.norm(B))
    tP = math.acos((-A) @ (-Ct) / np.linalg.norm(A) / np.linalg.norm(Ct))
    close("tm-1-18 內角和 180°", deg(tO + tP + tQ), 180)
    close("tm-1-18 三個外積", [np.cross(Ct, B), -np.cross(A, Ct)], [np.cross(A, B), np.cross(A, B)])
    close("tm-1-18 正弦定律", [math.sin(tQ) / np.linalg.norm(A), math.sin(tP) / np.linalg.norm(B)], [math.sin(tO) / np.linalg.norm(Ct)] * 2)
s20a = [sum(eps(i, j, k) * (i == j) for i in range(3) for j in range(3)) for k in range(3)]
s20b = [[sum(eps(i, j, k) * eps(l, j, k) for j in range(3) for k in range(3)) for l in range(3)] for i in range(3)]
check(f"tm-1-20 (a) {s20a}", s20a == [0, 0, 0])
check("tm-1-20 (b) = 2δ", s20b == [[2 if i == l else 0 for l in range(3)] for i in range(3)])
check("tm-1-20 (c) = 6", sum(eps(i, j, k)**2 for i in range(3) for j in range(3) for k in range(3)) == 6)
bad = [(i, j, l, m) for i, j, l, m in itertools.product(range(3), repeat=4)
       if sum(eps(i, j, k) * eps(l, m, k) for k in range(3)) != (i == l) * (j == m) - (i == m) * (j == l)]
check(f"tm-1-22 ε-δ 恆等式 81 種組合（不符 {len(bad)}）", not bad)
A = np.array([1, 2, -1]); B = np.array([-2, 3, 1])
close("tm-1-9 A-B、|A-B|", [*(A - B), np.linalg.norm(A - B)], [3, -1, -2, 3.7417], tol=1e-4)
close("tm-1-9 A·B、|A|、B_A", [A @ B, np.linalg.norm(A), A @ B / np.linalg.norm(A), 6**.5 / 2], [3, 6**.5, 1.2247, 1.2247], tol=1e-4)
close("tm-1-9 |B|、cos、θ", [np.linalg.norm(B), 3 / 84**.5, deg(math.acos(3 / 84**.5))], [14**.5, 0.3273, 70.893], tol=1e-3)
close("tm-1-9 A×B、2A×B", [*np.cross(A, B), *np.cross(A - B, A + B)], [5, 1, 7, 10, 2, 14])
a_, b_, c_ = np.array([1, 0, 0]), np.array([0, 2, 0]), np.array([0, 0, 3])
n = np.cross(b_ - a_, c_ - a_)
close("tm-1-12 n、|n|、S、d", [*n, np.linalg.norm(n), np.linalg.norm(n) / 2, a_ @ n / np.linalg.norm(n)], [6, 3, 2, 7, 3.5, 0.857143], tol=1e-5)
close("tm-1-12 n = a×b+b×c+c×a", np.cross(a_, b_) + np.cross(b_, c_) + np.cross(c_, a_), n)
close("tm-1-12 a·n = a·(b×c)", a_ @ n, a_ @ np.cross(b_, c_))
for _ in range(2):
    a3, b3, c3 = (rng.normal(size=3) for _ in range(3))
    nn = np.cross(b3 - a3, c3 - a3)
    close("tm-1-12 一般公式：距離（與平面上投影比較）", abs(a3 @ np.cross(b3, c3)) / np.linalg.norm(np.cross(a3, b3) + np.cross(b3, c3) + np.cross(c3, a3)),
          abs((b3 - 0) @ nn) / np.linalg.norm(nn))
nh = n / 7; w_ = np.array([1, 1, 1]) - a_
close("tm-1-39 d=5/7", w_ @ nh, 5 / 7)
r0 = np.array([1, 1, 1]) - (5 / 7) * nh
close("tm-1-39 最近點 ×49", r0 * 49, [19, 34, 39])
close("tm-1-39 平面方程式：三點、最近點、(1,1,1) 的值", [n @ a_, n @ b_, n @ c_, n @ r0, n @ np.array([1, 1, 1])], [6, 6, 6, 6, 11])
for _ in range(2):
    al, be = rng.uniform(-3, 3, size=2)
    ah = np.array([math.cos(al), math.sin(al), 0]); bh = np.array([math.cos(be), math.sin(be), 0])
    close("tm-1-19 內積給 cos(α-β)、外積給 sin(α-β)", [ah @ bh, np.cross(bh, ah)[2]], [math.cos(al - be), math.sin(al - be)])
u1 = np.array([1, 0, 0]); u2 = np.array([0, 1, -1]); n = np.cross(u1, u2)
close("self-s05-1 n、d", [*n, abs(np.array([0, 1, 1]) @ n) / np.linalg.norm(n)], [0, 1, 1, 2**.5])
S, T = np.meshgrid(np.linspace(-3, 3, 1201), np.linspace(-3, 3, 1201))
D2 = S**2 + (1 + T)**2 + (1 - T)**2
i0 = np.unravel_index(np.argmin(D2), D2.shape)
close("self-s05-1 數值最小：s、t、距離", [S[i0], T[i0], math.sqrt(D2[i0])], [0, 0, 2**.5], tol=1e-6)
P, Q, R = np.array([1, 0, 1]), np.array([2, 2, 1]), np.array([0, 1, 3])
PQ, PR = Q - P, R - P; n = np.cross(PQ, PR)
close("self-s05-2 PQ、PR、n、S", [*PQ, *PR, *n, np.linalg.norm(n) / 2], [1, 2, 0, -1, 1, 2, 4, -2, 3, 29**.5 / 2])
proj = lambda V, kz: np.where(np.arange(3) == kz, 0, V)
Sz = np.linalg.norm(np.cross(proj(PQ, 2), proj(PR, 2))) / 2
Sx = np.linalg.norm(np.cross(proj(PQ, 0), proj(PR, 0))) / 2
Sy = np.linalg.norm(np.cross(proj(PQ, 1), proj(PR, 1))) / 2
close("self-s05-2 投影外積", [*np.cross(proj(PQ, 2), proj(PR, 2)), *np.cross(proj(PQ, 0), proj(PR, 0)), *np.cross(proj(PQ, 1), proj(PR, 1))],
      [0, 0, 3, 4, 0, 0, 0, -2, 0])
close("self-s05-2 Sx、Sy、Sz、平方和", [Sx, Sy, Sz, Sx**2 + Sy**2 + Sz**2], [2, 1, 1.5, 29 / 4])

# ===================== 06 角速度 =====================
for _ in range(3):
    wv = rng.normal(size=3); rv = rng.normal(size=3)
    alpha = math.acos(wv @ rv / np.linalg.norm(wv) / np.linalg.norm(rv))
    rpar = (rv @ wv) / (wv @ wv) * wv
    close("ex-p33 |ω×r| = rω sinα、ω×r = ω×R", [np.linalg.norm(np.cross(wv, rv)), *np.cross(wv, rv - rpar)],
          [np.linalg.norm(rv) * np.linalg.norm(wv) * math.sin(alpha), *np.cross(wv, rv)])
close("ex-p33 驗算 ω k̂ × (R,0,h)", np.cross([0, 0, 2.0], [1.5, 0, 0.7]), [0, 3.0, 0])
wv = np.array([0, 0, 2]); rv = np.array([1, 0, 1])
close("ex-ang v、r、α、rω sinα、R", [*np.cross(wv, rv), np.linalg.norm(rv), deg(math.acos(rv[2] / np.linalg.norm(rv))), 2**.5 * 2 * 2**.5 / 2, np.hypot(1, 0)],
      [0, 2, 0, 2**.5, 45, 2, 1])
om = 2 * math.pi / 86164
lam = math.radians(22.6)
close("self-s06-1 ω、α", [om, 90 - 22.6], [7.292e-5, 67.4], tol=1e-4)
close("self-s06-1 R_Eω、cos22.6°、v", [6.37e6 * om, math.cos(lam), 6.37e6 * om * math.cos(lam)], [464.5, 0.9232, 428.8], tol=5e-4)
check("self-s06-1 v 四捨五入 429", round(6.37e6 * om * math.cos(lam)) == 429)
close("self-s06-1 方向 (0, ωR cosλ, 0)", np.cross([0, 0, om], 6.37e6 * np.array([math.cos(lam), 0, math.sin(lam)])), [0, 6.37e6 * om * math.cos(lam), 0])
close("self-s06-1 赤道 465", 6.37e6 * om, 465, tol=2e-3)
wv = np.array([1, 2, 3])
close("self-s06-2 ω×r1、ω×r2", [*np.cross(wv, [1, 0, 0]), *np.cross(wv, [0, 1, 0])], [0, 3, -2, -3, 0, 1])
close("self-s06-2 |ω|、v3", [np.linalg.norm(wv), *np.cross(wv, [1, 1, 1])], [3.7417, -1, 2, -1], tol=1e-4)
close("self-s06-2 ω+λr1 不改變 v1", np.cross(wv + 2.7 * np.array([1, 0, 0]), [1, 0, 0]), [0, 3, -2])

# ===================== 07 向量微分 =====================
bs, ws = sp.symbols("b omega", positive=True)
rr = sp.Matrix([2 * bs * sp.sin(ws * t), bs * sp.cos(ws * t), 0])
vv = rr.diff(t); acc = vv.diff(t)
zero("tm-1-10 v", (vv - sp.Matrix([2 * bs * ws * sp.cos(ws * t), -bs * ws * sp.sin(ws * t), 0])).norm())
zero("tm-1-10 a=-ω²r", (acc + ws**2 * rr).norm())
zero("tm-1-10 速率²", sp.simplify(vv.dot(vv) - bs**2 * ws**2 * (1 + 3 * sp.cos(ws * t)**2)))
tq = sp.pi / (2 * ws)
zero("tm-1-10 t=π/2ω 時 v、a、內積", (vv.subs(t, tq) - sp.Matrix([0, -bs * ws, 0])).norm() + (acc.subs(t, tq) - sp.Matrix([-2 * bs * ws**2, 0, 0])).norm() + vv.subs(t, tq).dot(acc.subs(t, tq)))
F = [sp.Function(f"x{i}")(t) for i in range(3)]
rv = sp.Matrix(F); rd = rv.diff(t); rdd = rd.diff(t)
a_c, b_c = sp.symbols("a b")
zero("tm-1-32 d/dt(ar²+b ṙ²)", sp.diff(a_c * rv.dot(rv) + b_c * rd.dot(rd), t) - (2 * a_c * rv.dot(rd) + 2 * b_c * rd.dot(rdd)))
rn = sp.sqrt(rv.dot(rv))
zero("tm-1-33 d/dt(r/|r|)", sp.simplify((rv / rn).diff(t) - (rd / rn - rv * sp.diff(rn, t) / rn**2)).norm())
lhs = rv.cross(rd.cross(rv)).diff(t)
rhs = rv.dot(rv) * rdd + rv.dot(rd) * rd - (rd.dot(rd) + rv.dot(rdd)) * rv
zero("tm-1-27 恆等式", sp.simplify((lhs - rhs).norm()))
zero("tm-1-27 中間式 v×(v×r)+r×(a×r)", sp.simplify((lhs - (rd.cross(rd.cross(rv)) + rv.cross(rdd.cross(rv)))).norm()))
zero("tm-1-34 d/dt(A×Ȧ)=A×Ä", sp.simplify((rv.cross(rd).diff(t) - rv.cross(rdd)).norm()))
Rs, bz = sp.symbols("R b_z", positive=True)
hel = sp.Matrix([Rs * sp.cos(ws * t), Rs * sp.sin(ws * t), bz * t])
hv = hel.diff(t); ha = hv.diff(t)
zero("self-s07-1 速率²", sp.simplify(hv.dot(hv) - (Rs**2 * ws**2 + bz**2)))
zero("self-s07-1 a·v", sp.simplify(ha.dot(hv)))
zero("self-s07-1 a=-ω²(x,y,0)、|a|", sp.simplify((ha + ws**2 * sp.Matrix([hel[0], hel[1], 0])).norm()) + sp.simplify(sp.sqrt(ha.dot(ha)) - Rs * ws**2))
L = rr.cross(vv)
zero("self-s07-2 r×v = -2b²ω k̂", sp.simplify((L - sp.Matrix([0, 0, -2 * bs**2 * ws])).norm()))
zero("self-s07-2 d/dt(r×v) = r×a = 0", sp.simplify(L.diff(t).norm()) + sp.simplify(rr.cross(acc).norm()))
area = sp.integrate(sp.Rational(1, 2) * sp.Abs(L[2]), (t, 0, 2 * sp.pi / ws))
zero("self-s07-2 一週面積 2πb²", sp.simplify(area - 2 * sp.pi * bs**2))

print("\nALL OK" if ok else "\nSOME FAILED")
sys.exit(0 if ok else 1)
