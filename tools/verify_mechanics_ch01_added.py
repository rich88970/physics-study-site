"""獨立驗算力學 Lecture 1 本次新增的題目（講義 p.26、p.33–34、p.50、p.84–85，課本 1-16，以及每節 2 題自編難題）。

用法：python tools/verify_mechanics_ch01_added.py   （需要 numpy、sympy）
每一題都用和網站詳解不同的方式（數值積分、隨機測試、有限差分、符號運算）重算。
"""
import math
import sys

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(("OK  " if cond else "FAIL"), name)


def close(name, got, want, tol=1e-6):
    good = np.allclose(np.array(got, dtype=float), np.array(want, dtype=float), atol=tol, rtol=tol)
    check(f"{name}: {np.round(np.array(got, dtype=float), 6).tolist()} vs {want}", good)


def zero(name, expr):
    check(name + " (sympy = 0)", sp.simplify(expr) == 0)


rng = np.random.default_rng(2026)
x, y, z, t, s = sp.symbols("x y z t s", real=True)
r_, th, ph = sp.symbols("r theta phi", positive=True)

# ---------- 講義 p.26：沿 î 與沿 B 的分量 ----------
for _ in range(3):
    A = rng.normal(size=3); B = rng.normal(size=3)
    cos = A @ B / np.linalg.norm(A) / np.linalg.norm(B)
    close("p26 A_B = |A|cosθ", A @ B / np.linalg.norm(B), np.linalg.norm(A) * cos)
    close("p26 A_1 = A·î", A @ np.array([1, 0, 0]), A[0])

A = np.array([2.0, 1.0, -2.0]); B = np.array([3.0, 0.0, 4.0])
close("p26 數值 A_1=2, A_B=-0.4", [A @ [1, 0, 0], A @ B / np.linalg.norm(B)], [2, -0.4])
close("p26 |A|cosθ = -0.4", np.linalg.norm(A) * (A @ B) / (np.linalg.norm(A) * np.linalg.norm(B)), -0.4)

# ---------- 講義 p.33–34：v = ω×r，|v| = rω sinα = Rω ----------
for _ in range(3):
    w = rng.normal(size=3); r = rng.normal(size=3)
    alpha = math.acos(w @ r / np.linalg.norm(w) / np.linalg.norm(r))
    R = np.linalg.norm(r - (r @ w) / (w @ w) * w)  # 到轉軸的距離
    v = np.cross(w, r)
    close("p34 |ω×r| = rω sinα", np.linalg.norm(v), np.linalg.norm(r) * np.linalg.norm(w) * math.sin(alpha))
    close("p34 r sinα = R", np.linalg.norm(r) * math.sin(alpha), R)
    close("p34 v ⊥ ω, v ⊥ r", [v @ w, v @ r], [0, 0])
    # 原點沿軸平移，v 不變
    close("p34 原點沿軸移動 v 不變", np.cross(w, r - 2.7 * w), v)
# 數值：繞 z 軸逆時針轉，(1,0,0) 的速度朝 +y
close("p34 方向", np.cross([0, 0, 1], [1, 0, 0]), [0, 1, 0])

# ---------- 講義 p.50：λ2(φ)λ1(θ) ----------
c1, s1, c2, s2 = sp.cos(th), sp.sin(th), sp.cos(ph), sp.sin(ph)
L1 = sp.Matrix([[c1, s1, 0], [-s1, c1, 0], [0, 0, 1]])
L2 = sp.Matrix([[1, 0, 0], [0, c2, s2], [0, -s2, c2]])
want = sp.Matrix([[c1, s1, 0], [-c2 * s1, c2 * c1, s2], [s2 * s1, -s2 * c1, c2]])
zero("p50 λ2λ1 公式", (L2 * L1 - want).norm())
zero("p50 λ2λ1 正交", ((L2 * L1) * (L2 * L1).T - sp.eye(3)).norm())
check("p50 θ=φ=90° 回到 λ3", (L2 * L1).subs({th: sp.pi / 2, ph: sp.pi / 2}) == sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]]))
check("p50 λ1λ2 ≠ λ2λ1", sp.simplify((L1 * L2 - L2 * L1).subs({th: sp.pi / 3, ph: sp.pi / 4})) != sp.zeros(3))
# 數值：主動驗證——先轉 θ 再轉 φ，點在 x'' 系的座標 = 逐步套用
thv, phv = 0.7, -1.1
P = rng.normal(size=3)
Lf1 = np.array(L1.subs(th, thv).evalf(), dtype=float); Lf2 = np.array(L2.subs(ph, phv).evalf(), dtype=float)
close("p50 逐步 = 合成", Lf2 @ (Lf1 @ P), np.array(want.subs({th: thv, ph: phv}).evalf(), dtype=float) @ P)

# ---------- 講義 p.84–85：F = -∇V，指向下坡、垂直等高線 ----------
V = sp.exp(-(x - 1) ** 2 - y ** 2) + 0.7 * sp.exp(-(x + 1) ** 2 - 2 * y ** 2)
gV = sp.Matrix([sp.diff(V, x), sp.diff(V, y)])
for p in [(0.3, 0.4), (-0.8, 0.2), (1.5, -0.6)]:
    g = np.array([float(e.subs({x: p[0], y: p[1]})) for e in gV])
    F = -g
    tang = np.array([-g[1], g[0]])  # 沿等高線
    close(f"p84 F·(等高線切線)=0 at {p}", F @ tang, 0)
    # 沿 F 走一小步，V 變小
    h = 1e-4
    V0 = float(V.subs({x: p[0], y: p[1]})); V1 = float(V.subs({x: p[0] + h * F[0], y: p[1] + h * F[1]}))
    check(f"p84 沿 F 走 V 下降 at {p}", V1 < V0)
# 功能定理：dW = F·ds = -dV
zero("p84 F·ds = -dV（任意 ds）", (-gV).dot(sp.Matrix([sp.Symbol('dx'), sp.Symbol('dy')])) + gV.dot(sp.Matrix([sp.Symbol('dx'), sp.Symbol('dy')])))

# ---------- 課本 1-16：r·a = c 是垂直 a、離原點 c/a 的平面 ----------
a = np.array([2.0, -1.0, 2.0]); c = 6.0
d = c / np.linalg.norm(a)
close("1-16 最近點 r0 = c a/a²", (c / (a @ a)) * a @ a, c)
close("1-16 距離 c/|a|", d, 2.0)
for _ in range(4):
    u = np.cross(a, rng.normal(size=3))  # 平面內的方向
    r = (c / (a @ a)) * a + rng.normal() * u
    close("1-16 r0 + 平面內方向仍滿足 r·a=c", r @ a, c)
    check("1-16 |r| ≥ c/a", np.linalg.norm(r) >= d - 1e-12)

# ========== 自編難題 ==========
# s01-1 a = -k v
k, v0, w = sp.symbols("k v_0 omega", positive=True)
vt = v0 * sp.exp(-k * t); xt = v0 / k * (1 - sp.exp(-k * t))
zero("s01-1 dv/dt = -k v", sp.diff(vt, t) + k * vt)
zero("s01-1 dx/dt = v", sp.diff(xt, t) - vt)
check("s01-1 x(∞) = v0/k", sp.limit(xt, t, sp.oo) == v0 / k)
check("s01-1 k→0 回到 x=v0 t", sp.limit(xt, k, 0) == v0 * t)
close("s01-1 數值 v0=20,k=0.5：停止距離 40 m", float((v0 / k).subs({v0: 20, k: 0.5})), 40)
close("s01-1 t=2 s 時 x", float(xt.subs({v0: 20, k: 0.5, t: 2})), 40 * (1 - math.exp(-1)))
cc = sp.Symbol("c", positive=True)
v2 = v0 / (1 + cc * v0 * t); x2 = sp.log(1 + cc * v0 * t) / cc
zero("s01-1(b) dv/dt = -c v²", sp.diff(v2, t) + cc * v2 ** 2)
zero("s01-1(b) dx/dt = v", sp.diff(x2, t) - v2)
check("s01-1(b) x(∞) = ∞", sp.limit(x2, t, sp.oo) == sp.oo)
check("s01-1(b) c→0 回到 v0 t", sp.limit(x2, cc, 0) == v0 * t)
zero("s01-1(b) v = v0 e^{-cx}", v2 - v0 * sp.exp(-cc * x2))
# 數值積分 ODE 驗證兩種阻力
from scipy.integrate import solve_ivp
sol = solve_ivp(lambda T, Y: [Y[1], -0.5 * Y[1]], [0, 60], [0, 20], rtol=1e-10, atol=1e-12)
close("s01-1(a) 數值積分 x(60)≈40", sol.y[0, -1], 40, 1e-6)
sol = solve_ivp(lambda T, Y: [Y[1], -0.1 * Y[1] ** 2], [0, 1000], [0, 20], rtol=1e-10, atol=1e-12)
close("s01-1(b) 數值積分 x(1000)", sol.y[0, -1], math.log(1 + 0.1 * 20 * 1000) / 0.1, 1e-6)
# s01-2 a = -ω² x，v dv = a dx
x0, A = sp.symbols("x_0 A", real=True)
X = x0 * sp.cos(w * t) + v0 / w * sp.sin(w * t)  # 真正的解
Vx = sp.diff(X, t)
zero("s01-2 v² = v0² + ω²(x0² - x²)", Vx ** 2 - (v0 ** 2 + w ** 2 * (x0 ** 2 - X ** 2)))
amp = sp.sqrt(x0 ** 2 + v0 ** 2 / w ** 2)
zero("s01-2 振幅² = x0² + v0²/ω²", sp.simplify((sp.sqrt((x0 * sp.cos(w * t) + v0 / w * sp.sin(w * t)) ** 2).subs(t, sp.atan2(v0 / w, x0) / w)) ** 2 - amp ** 2))
close("s01-2 數值 x0=0.03,v0=0.4,ω=10：A=0.05", float(amp.subs({x0: 0.03, v0: 0.4, w: 10})), 0.05)
close("s01-2 x=0.04 時 |v|=0.3", math.sqrt(0.4 ** 2 + 100 * (0.03 ** 2 - 0.04 ** 2)), 0.3)

# s02-1 A1B2 - A2B1 不變，A1B1 會變
for thv in [0.3, 1.2, math.pi / 2]:
    R2 = np.array([[math.cos(thv), math.sin(thv)], [-math.sin(thv), math.cos(thv)]])
    Av, Bv = np.array([3.0, 1.0]), np.array([1.0, 2.0])
    Ap, Bp = R2 @ Av, R2 @ Bv
    close(f"s02-1 A1B2-A2B1 不變 θ={thv:.2f}", Ap[0] * Bp[1] - Ap[1] * Bp[0], 5)
    close(f"s02-1 A1B1+A2B2 不變 θ={thv:.2f}", Ap @ Bp, 5)
R90 = np.array([[0, 1], [-1, 0]])
close("s02-1 θ=90° 時 A1'B1' = 2（原本 3）", (R90 @ [3, 1])[0] * (R90 @ [1, 2])[0], 2)
a1, a2, b1, b2 = sp.symbols("a1 a2 b1 b2", real=True)
xp = lambda u, vv: (u * sp.cos(th) + vv * sp.sin(th), -u * sp.sin(th) + vv * sp.cos(th))
(A1p, A2p), (B1p, B2p) = xp(a1, a2), xp(b1, b2)
zero("s02-1 符號：A1'B2'-A2'B1' = A1B2-A2B1", A1p * B2p - A2p * B1p - (a1 * b2 - a2 * b1))
# s02-2 長 8、與 z 夾 30°、再加垂直條件
A1s, A2s = sp.symbols("A1 A2", real=True)
A3v = 4 * sp.sqrt(3)
sols = sp.solve([A1s ** 2 + A2s ** 2 - 16, A1s + A2s], [A1s, A2s], dict=True)
check(f"s02-2(a) 兩解 {sols}", len(sols) == 2 and all(abs(abs(float(d[A1s])) - 2 * math.sqrt(2)) < 1e-12 and float(d[A1s] + d[A2s]) == 0 for d in sols))
for d in sols:
    v = np.array([float(d[A1s]), float(d[A2s]), float(A3v)])
    close("s02-2(a) 長度 8、與 z 夾 30°、⊥(1,1,0)", [np.linalg.norm(v), math.degrees(math.acos(v[2] / 8)), v @ [1, 1, 0]], [8, 30, 0])
close("s02-2(a) 方位角 -45° 與 135°", sorted(math.degrees(math.atan2(float(d[A2s]), float(d[A1s]))) for d in sols), [-45, 135])
sols_b = sp.solve([A1s ** 2 + A2s ** 2 - 16, A1s + A2s + A3v], [A1s, A2s], dict=True)
check(f"s02-2(b) 無實數解（解={sols_b}）", len(sols_b) == 0)
# 掃描所有方位角：A·(1,1,1) 的範圍
ph_ = np.linspace(0, 2 * np.pi, 100001)
dots = 4 * np.cos(ph_) + 4 * np.sin(ph_) + 4 * math.sqrt(3)
check(f"s02-2(b) A·(1,1,1) 恆 > 0（最小 {dots.min():.4f}）", dots.min() > 0)
close("s02-2(b) 夾角範圍 24.7°～84.7°", [math.degrees(math.acos(dots.max() / 8 / math.sqrt(3))), math.degrees(math.acos(dots.min() / 8 / math.sqrt(3)))], [54.7356 - 30, 54.7356 + 30], 1e-3)

# s03-1 重心
Pa, Pb, Pc = np.array([0, 0, 0.0]), np.array([6, 0, 0.0]), np.array([0, 3, 3.0])
G = (Pa + Pb + Pc) / 3
for P1, P2, P3 in [(Pa, Pb, Pc), (Pb, Pc, Pa), (Pc, Pa, Pb)]:
    M = (P2 + P3) / 2
    close("s03-1 中線 2/3 處 = G", P1 + 2 / 3 * (M - P1), G)
close("s03-1 G = (2,1,1)", G, [2, 1, 1])
close("s03-1 GA+GB+GC = 0", (Pa - G) + (Pb - G) + (Pc - G), [0, 0, 0])
# s03-2 渡河
u, vb, W = 3.0, 5.0, 120.0
phi = math.asin(u / vb)
vg = np.array([u - vb * math.sin(phi), vb * math.cos(phi)])
close("s03-2(a) 上游偏 36.87°", math.degrees(phi), 36.8699, 1e-4)
close("s03-2(a) 對地速度 (0,4)", vg, [0, 4])
close("s03-2(a) t=30 s", W / vg[1], 30)
close("s03-2(b) t=24 s, 漂 72 m", [W / vb, u * W / vb], [24, 72])
# 任意航向的渡河時間 W/(vb cosφ) 在 φ=0 最小
ts = [W / (vb * math.cos(p)) for p in np.linspace(-1.2, 1.2, 241)]
close("s03-2(b) 最短時間在 φ=0", min(ts), 24)
phis = np.linspace(-1.5, 1.5, 300001)
D = 120 * (3 - 2 * np.sin(phis)) / (2 * np.cos(phis))
i = np.argmin(D)
close("s03-2(c) 最佳 sinφ = 2/3", math.sin(phis[i]), 2 / 3, 1e-4)
close("s03-2(c) φ = 41.8°", math.degrees(phis[i]), math.degrees(math.asin(2 / 3)), 1e-3)
close("s03-2(c) D_min = 60√5", D[i], 60 * math.sqrt(5), 1e-6)
close("s03-2(c) t = 36√5", 120 / (2 * math.sqrt(5) / 3), 36 * math.sqrt(5))
close("s03-2(c) 對地速度 ⊥ 船對水", np.array([3 - 4 / 3, 2 * math.sqrt(5) / 3]) @ np.array([-4 / 3, 2 * math.sqrt(5) / 3]), 0)
close("s03-2(c) 船頭正北漂 180 m", 120 * 3 / 2, 180)

# s04-1 點到直線距離
Pv = np.array([1, 2, 3.0]); uhat = np.array([1, 1, 1]) / math.sqrt(3)
par = (Pv @ uhat) * uhat; perp = Pv - par
close("s04-1 平行分量 (2,2,2)", par, [2, 2, 2])
close("s04-1 垂直分量 (-1,0,1)", perp, [-1, 0, 1])
close("s04-1 距離 √2", np.linalg.norm(perp), math.sqrt(2))
close("s04-1 外積驗算 |P×û|", np.linalg.norm(np.cross(Pv, uhat)), math.sqrt(2))
ts = np.linspace(-5, 5, 200001)
close("s04-1 暴力最小距離", np.min(np.linalg.norm(Pv[None, :] - ts[:, None] * uhat[None, :], axis=1)), math.sqrt(2), 1e-5)
# s04-2 半圓上的圓周角
for _ in range(3):
    e = rng.normal(size=3); e /= np.linalg.norm(e); Rr = 2.5
    q = rng.normal(size=3); q = Rr * q / np.linalg.norm(q)  # 球面上任一點
    close("s04-2 (P-A)·(P-B)=0", (q + Rr * e) @ (q - Rr * e), 0)
close("s04-2 數值 R=5, P=(3,4)", (np.array([3, 4]) - [-5, 0]) @ (np.array([3, 4]) - [5, 0]), 0)

# s05-1 歪斜線距離
P1, u1 = np.array([0, 0, 0.0]), np.array([1, 0, 0.0])
P2, u2 = np.array([0, 1, 1.0]), np.array([0, 1, -1.0])
n = np.cross(u1, u2)
close("s05-1 n = (0,1,1)", n, [0, 1, 1])
close("s05-1 d = √2", abs((P2 - P1) @ n) / np.linalg.norm(n), math.sqrt(2))
S, T = np.meshgrid(np.linspace(-3, 3, 1201), np.linspace(-3, 3, 1201))
D = np.sqrt((S - 0) ** 2 + (0 - (1 + T)) ** 2 + (0 - (1 - T)) ** 2)
close("s05-1 暴力最小距離", D.min(), math.sqrt(2), 1e-5)
# s05-2 投影面積定理
Pp, Qp, Rp = np.array([1, 0, 1.0]), np.array([2, 2, 1.0]), np.array([0, 1, 3.0])
n = np.cross(Qp - Pp, Rp - Pp)
close("s05-2 n = (4,-2,3)", n, [4, -2, 3])
close("s05-2 面積 √29/2", np.linalg.norm(n) / 2, math.sqrt(29) / 2)
def area2d(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) / 2
Axy = area2d(Pp[[0, 1]], Qp[[0, 1]], Rp[[0, 1]]); Ayz = area2d(Pp[[1, 2]], Qp[[1, 2]], Rp[[1, 2]]); Azx = area2d(Pp[[2, 0]], Qp[[2, 0]], Rp[[2, 0]])
close("s05-2 三個投影面積 (2,1,1.5)", [Ayz, Azx, Axy], [2, 1, 1.5])
close("s05-2 平方和 = 面積²", Ayz ** 2 + Azx ** 2 + Axy ** 2, 29 / 4)
for _ in range(3):
    p, q, r = rng.normal(size=(3, 3))
    nn = np.cross(q - p, r - p) / 2
    close("s05-2 隨機三角形", area2d(p[[1, 2]], q[[1, 2]], r[[1, 2]]) ** 2 + area2d(p[[2, 0]], q[[2, 0]], r[[2, 0]]) ** 2 + area2d(p[[0, 1]], q[[0, 1]], r[[0, 1]]) ** 2, nn @ nn)

# s06-1 地球自轉
Tsid = 86164.0; Re = 6.37e6; lat = math.radians(22.6)
wE = 2 * math.pi / Tsid
rvec = Re * np.array([math.cos(lat), 0, math.sin(lat)])  # 在 xz 平面（x 指向該點經線）
vv = np.cross([0, 0, wE], rvec)
close("s06-1 ω = 7.292e-5", wE, 7.292e-5, 1e-3)
close("s06-1 v ≈ 428.6 m/s", np.linalg.norm(vv), 428.6, 2e-3)
close("s06-1 v 朝東（+y）", vv / np.linalg.norm(vv), [0, 1, 0])
close("s06-1 赤道 465 m/s", wE * Re, 464.5, 2e-3)
# s06-2 由兩點速度求 ω
om = np.array([1, 2, 3.0])
close("s06-2 v1", np.cross(om, [1, 0, 0]), [0, 3, -2])
close("s06-2 v2", np.cross(om, [0, 1, 0]), [-3, 0, 1])
close("s06-2 (1,1,1) 的速度", np.cross(om, [1, 1, 1]), [-1, 2, -1])
close("s06-2 只給 v1 時 ω+λî 也行", np.cross(om + 5 * np.array([1, 0, 0]), [1, 0, 0]), [0, 3, -2])
# 用最小平方獨立解 ω
def crossmat(r):
    return np.array([[0, r[2], -r[1]], [-r[2], 0, r[0]], [r[1], -r[0], 0]])  # ω×r = M ω
Mm = np.vstack([crossmat([1, 0, 0]), crossmat([0, 1, 0])]); rhs = np.hstack([[0, 3, -2], [-3, 0, 1]])
close("s06-2 最小平方解 ω", np.linalg.lstsq(Mm, rhs, rcond=None)[0], [1, 2, 3])
check("s06-2 單點方程秩 2（少一個條件）", np.linalg.matrix_rank(crossmat([1, 0, 0])) == 2)

# s07-1 螺旋線
Rh, b = sp.symbols("R b", positive=True)
rr = sp.Matrix([Rh * sp.cos(w * t), Rh * sp.sin(w * t), b * t])
vv_ = rr.diff(t); aa_ = vv_.diff(t)
zero("s07-1 v² = R²ω² + b²", vv_.dot(vv_) - (Rh ** 2 * w ** 2 + b ** 2))
zero("s07-1 a·v = 0", aa_.dot(vv_))
zero("s07-1 |a| = Rω²", sp.sqrt(aa_.dot(aa_)) - Rh * w ** 2)
zero("s07-1 a 指向軸", (aa_ + w ** 2 * sp.Matrix([rr[0], rr[1], 0])).norm())
# s07-2 r×v 守恆
rr = sp.Matrix([2 * b * sp.sin(w * t), b * sp.cos(w * t), 0])
L = rr.cross(rr.diff(t))
zero("s07-2 r×v = -2b²ω k", (L - sp.Matrix([0, 0, -2 * b ** 2 * w])).norm())
zero("s07-2 d(r×v)/dt = r×a = 0", (rr.cross(rr.diff(t, 2))).norm())
zero("s07-2 a = -ω² r", (rr.diff(t, 2) + w ** 2 * rr).norm())
close("s07-2 面積速度 × 週期 = 橢圓面積 2πb²", (2 * 1.3 ** 2 * 0.7 / 2) * (2 * math.pi / 0.7), math.pi * 2 * 1.3 * 1.3)

# s08-1 和 A 可交換的矩陣
a_, b_, c_, d_ = sp.symbols("a b c d")
Am = sp.Matrix([[1, 1], [0, 1]]); Bm = sp.Matrix([[a_, b_], [c_, d_]])
sol = sp.solve(list(Am * Bm - Bm * Am), [a_, b_, c_, d_], dict=True)
check(f"s08-1 解為 c=0, d=a：{sol}", len(sol) == 1 and sol[0].get(c_) == 0 and sp.simplify(sol[0].get(d_, d_) - a_) == 0 or (len(sol) == 1 and sol[0].get(c_) == 0 and sp.simplify(sol[0].get(a_, a_) - d_) == 0))
Bc = sp.Matrix([[a_, b_], [0, a_]])
zero("s08-1 AB-BA = 0", (Am * Bc - Bc * Am).norm())
check("s08-1 反例 [[1,0],[0,2]] 不交換", Am * sp.diag(1, 2) != sp.diag(1, 2) * Am)
# s08-2 λ(θ)ⁿ = λ(nθ) 與回到原位的條件
lam2 = lambda a: sp.Matrix([[sp.cos(a), sp.sin(a)], [-sp.sin(a), sp.cos(a)]])
zero("s08-2 λ(θ)λ(φ) = λ(θ+φ)", sp.simplify(sp.expand_trig(lam2(th) * lam2(ph) - lam2(th + ph))).norm())
for nn in range(1, 7):
    zero(f"s08-2 λ(θ)^{nn} = λ({nn}θ)", sp.simplify(sp.expand_trig(lam2(th) ** nn - lam2(nn * th))).norm())
L72 = np.array([[math.cos(math.radians(72)), math.sin(math.radians(72))], [-math.sin(math.radians(72)), math.cos(math.radians(72))]])
pw = [np.linalg.matrix_power(L72, nn) for nn in range(1, 6)]
check("s08-2 λ(72°)^5 = 1", np.allclose(pw[4], np.eye(2), atol=1e-12))
check("s08-2 λ(72°)^n ≠ 1，n=1..4", all(not np.allclose(pw[i], np.eye(2), atol=1e-6) for i in range(4)))
L1 = np.array([[math.cos(1), math.sin(1)], [-math.sin(1), math.cos(1)]])
Mx = np.eye(2); dmin, nbest = 9.0, 0
for nn in range(1, 10001):
    Mx = Mx @ L1
    dd = np.abs(Mx - np.eye(2)).max()
    if dd < dmin:
        dmin, nbest = dd, nn
check(f"s08-2 λ(1)^n 在 n≤10⁴ 最接近 1 的是 n={nbest}，最大元素差 {dmin:.2e}（> 0）", nbest == 710 and 1e-5 < dmin < 1e-4)
check("s08-2 π 是無理數（sympy）", sp.pi.is_rational is False)
check("s08-2 λ(144°) 最小 n=5", [nn for nn in range(1, 11) if (144 * nn) % 360 == 0][0] == 5)
check("s08-2 λ(90°) 最小 n=4", [nn for nn in range(1, 11) if (90 * nn) % 360 == 0][0] == 4)

# s09-1 λ(φ)λ(θ) = λ(θ+φ)
lam = lambda a: sp.Matrix([[sp.cos(a), sp.sin(a)], [-sp.sin(a), sp.cos(a)]])
zero("s09-1 λ(φ)λ(θ) - λ(θ+φ)", sp.simplify(sp.expand_trig((lam(ph) * lam(th) - lam(th + ph)))).norm())
zero("s09-1 λ(θ)ᵀ = λ(-θ)", (lam(th).T - lam(-th)).norm())
zero("s09-1 可交換", sp.simplify(lam(ph) * lam(th) - lam(th) * lam(ph)).norm())
close("s09-1 數值 cos75°", float(sp.cos(sp.pi / 6) * sp.cos(sp.pi / 4) - sp.sin(sp.pi / 6) * sp.sin(sp.pi / 4)), math.cos(math.radians(75)))
# s09-2 無窮小旋轉
e = sp.Symbol("epsilon")
Lz = sp.Matrix([[sp.cos(e), sp.sin(e), 0], [-sp.sin(e), sp.cos(e), 0], [0, 0, 1]])
L1st = sp.Matrix([[1, e, 0], [-e, 1, 0], [0, 0, 1]])
zero("s09-2 一階展開", (sp.series(Lz[0, 1], e, 0, 2).removeO() - e) + (sp.series(Lz[0, 0], e, 0, 2).removeO() - 1))
G2 = sp.expand(L1st * L1st.T - sp.eye(3))
check(f"s09-2 λλᵀ - 1 只剩 ε² 項：{G2.tolist()}", all(sp.Poly(g, e).degree() >= 2 or g == 0 for g in G2))
xv = sp.Matrix([x, y, z])
zero("s09-2 x' - x = -δθ×x", (L1st * xv - xv + sp.Matrix([0, 0, e]).cross(xv)).norm())
eps_ = L1st - sp.eye(3)
zero("s09-2 ε 反對稱", (eps_ + eps_.T).norm())
# 數值：小角度誤差 ~ ε²
for ev in [1e-2, 1e-3]:
    Lf = np.array(Lz.subs(e, ev).evalf(), dtype=float); L1f = np.array(L1st.subs(e, ev).evalf(), dtype=float)
    check(f"s09-2 ε={ev} 誤差 < ε²", np.abs(Lf - L1f).max() < ev ** 2)

# s11-1 轉動細桿上的珠子
r0 = sp.Symbol("r_0", positive=True)
rt = r0 * sp.cosh(w * t)
zero("s11-1 r̈ - rω² = 0", rt.diff(t, 2) - rt * w ** 2)
check("s11-1 r(0)=r0, ṙ(0)=0", rt.subs(t, 0) == r0 and rt.diff(t).subs(t, 0) == 0)
zero("s11-1 a_θ = 2ṙω = 2r0ω² sinh", 2 * rt.diff(t) * w - 2 * r0 * w ** 2 * sp.sinh(w * t))
# 數值積分直角座標的運動：只受垂直於桿的力
from math import cosh, sinh
r0v, wv, m = 0.1, 3.0, 0.2
tt = 0.8
rv = r0v * cosh(wv * tt)
pos = lambda T: np.array([r0v * cosh(wv * T) * math.cos(wv * T), r0v * cosh(wv * T) * math.sin(wv * T)])
h = 1e-4
acc = (pos(tt + h) - 2 * pos(tt) + pos(tt - h)) / h ** 2
rhat = np.array([math.cos(wv * tt), math.sin(wv * tt)]); thhat = np.array([-math.sin(wv * tt), math.cos(wv * tt)])
close("s11-1 有限差分：a·r̂ = 0（桿無徑向力）", acc @ rhat, 0, 1e-4)
close("s11-1 有限差分：N = m a_θ", m * (acc @ thhat), 2 * m * r0v * wv ** 2 * sinh(wv * tt), 1e-4)
# s11-2 心臟線與圓之間
aa = sp.Symbol("a", positive=True)
Aa = sp.integrate(sp.integrate(r_, (r_, aa, aa * (1 + sp.cos(th)))), (th, -sp.pi / 2, sp.pi / 2))
Ab = sp.integrate(sp.integrate(r_, (r_, aa * (1 + sp.cos(th)), aa)), (th, sp.pi / 2, 3 * sp.pi / 2))
zero("s11-2(a) (2+π/4)a²", Aa - (2 + sp.pi / 4) * aa ** 2)
zero("s11-2(b) (2-π/4)a²", Ab - (2 - sp.pi / 4) * aa ** 2)
Acard = sp.integrate(sp.integrate(r_, (r_, 0, aa * (1 + sp.cos(th)))), (th, 0, 2 * sp.pi))
zero("s11-2 心臟線總面積 3πa²/2", Acard - sp.Rational(3, 2) * sp.pi * aa ** 2)
zero("s11-2 重疊面積兩種算法一致", (Acard - Aa) - (sp.pi * aa ** 2 - Ab))
check("s11-2 交點 θ=±π/2", set(sp.solve(sp.cos(th), th)) >= {sp.pi / 2})
N_ = 400000
px_ = rng.uniform(-1.2, 2.2, N_); py_ = rng.uniform(-1.7, 1.7, N_); box = 3.4 * 3.4
rr_ = np.hypot(px_, py_); tt_ = np.arctan2(py_, px_)
inC = rr_ <= 1 + np.cos(tt_); inO = rr_ <= 1
close("s11-2 Monte Carlo (a)", (inC & ~inO).mean() * box, 2 + math.pi / 4, 2e-2)
close("s11-2 Monte Carlo (b)", (inO & ~inC).mean() * box, 2 - math.pi / 4, 3e-2)
# s12-1 實心半球的質心
Rs = sp.Symbol("R", positive=True)
Vh = sp.integrate(r_ ** 2 * sp.sin(th), (r_, 0, Rs), (th, 0, sp.pi / 2), (ph, 0, 2 * sp.pi))
Zh = sp.integrate(r_ * sp.cos(th) * r_ ** 2 * sp.sin(th), (r_, 0, Rs), (th, 0, sp.pi / 2), (ph, 0, 2 * sp.pi))
zero("s12-1 V = 2πR³/3", Vh - 2 * sp.pi * Rs ** 3 / 3)
zero("s12-1 ∫z dV = πR⁴/4", Zh - sp.pi * Rs ** 4 / 4)
zero("s12-1 z_cm = 3R/8", Zh / Vh - 3 * Rs / 8)
# 用圓盤切片（柱座標）獨立算
zz = sp.Symbol("zz", positive=True)
zero("s12-1 切片法", sp.integrate(zz * sp.pi * (Rs ** 2 - zz ** 2), (zz, 0, Rs)) / sp.integrate(sp.pi * (Rs ** 2 - zz ** 2), (zz, 0, Rs)) - 3 * Rs / 8)
shell = sp.integrate(Rs * sp.cos(th) * Rs ** 2 * sp.sin(th), (th, 0, sp.pi / 2), (ph, 0, 2 * sp.pi)) / (2 * sp.pi * Rs ** 2)
zero("s12-1(b) 薄半球殼 z_cm = R/2", shell - Rs / 2)
zero("s12-1(c) 薄殼加權 = 3R/8", sp.integrate(r_ / 2 * 2 * sp.pi * r_ ** 2, (r_, 0, Rs)) / sp.integrate(2 * sp.pi * r_ ** 2, (r_, 0, Rs)) - 3 * Rs / 8)
zero("s12-1(b) 環帶面積 2πR dz 與高度無關", sp.diff(2 * sp.pi * Rs ** 2 * (1 - sp.cos(th)), th) / sp.diff(Rs * (1 - sp.cos(th)), th) - 2 * sp.pi * Rs)
# s12-2 冰淇淋筒
al = sp.Symbol("alpha", positive=True)
Vc = sp.integrate(r_ ** 2 * sp.sin(th), (r_, 0, Rs), (th, 0, al), (ph, 0, 2 * sp.pi))
zero("s12-2 V = 2πR³(1-cosα)/3", Vc - 2 * sp.pi * Rs ** 3 * (1 - sp.cos(al)) / 3)
zero("s12-2 α=π 回到整球", Vc.subs(al, sp.pi) - 4 * sp.pi * Rs ** 3 / 3)
close("s12-2 α=60°、R=1：π/3", float(Vc.subs({al: sp.pi / 3, Rs: 1})), math.pi / 3)
# 柱座標獨立算 α=60°：錐 + 球冠
hgt = sp.Rational(1, 2)  # R cos60
cone = sp.pi * (sp.sqrt(3) / 2) ** 2 * hgt / 3
cap = sp.integrate(sp.pi * (1 - zz ** 2), (zz, hgt, 1))
zero("s12-2 錐 + 球冠 = π/3", cone + cap - sp.pi / 3)

# s13-1 沿梯度走的路徑
Tf = 100 - x ** 2 - 2 * y ** 2
gx, gy = sp.diff(Tf, x), sp.diff(Tf, y)
# 路徑 y = x² 的切線 (1, 2x) 與 ∇T 平行
zero("s13-1 y=x² 的切線 ∥ ∇T", (gx * 2 * x - gy * 1).subs(y, x ** 2))
check("s13-1 過 (1,1)", (x ** 2).subs(x, 1) == 1)
# 數值：沿 ∇T 方向積分（RK4）
p = np.array([1.0, 1.0]); hstep = 1e-3
gradT = lambda q: np.array([-2 * q[0], -4 * q[1]])
for _ in range(3000):
    k1 = gradT(p); k2 = gradT(p + hstep / 2 * k1); k3 = gradT(p + hstep / 2 * k2); k4 = gradT(p + hstep * k3)
    p = p + hstep / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    if p[0] < 1e-3:
        break
close("s13-1 數值路徑仍在 y=x² 上", p[1], p[0] ** 2, 1e-6)
close("s13-1 起點 ∇T = (-2,-4)", [float(gx.subs({x: 1, y: 1})), float(gy.subs({x: 1, y: 1}))], [-2, -4])
close("s13-1 起點最大升溫率 2√5", math.hypot(2, 4), 2 * math.sqrt(5))
# s13-2 非等向彈簧
kk = sp.Symbol("k", positive=True)
Vs = kk * (x ** 2 + 4 * y ** 2) / 2
F = [-sp.diff(Vs, x), -sp.diff(Vs, y)]
check("s13-2 F = (-kx, -4ky)", F == [-kk * x, -4 * kk * y])
Fv = np.array([-2.0, -4.0]); mr = np.array([-2.0, -1.0])
close("s13-2 cos = 0.8", Fv @ mr / np.linalg.norm(Fv) / np.linalg.norm(mr), 0.8)
close("s13-2 夾角 36.87°", math.degrees(math.acos(0.8)), 36.8699, 1e-4)
# F 與 r 平行 ⟺ F×r = 0 ⟺ xy=0
zero("s13-2 F×r 的 z 分量 = 3kxy", (F[0] * y - F[1] * x) - 3 * kk * x * y)
# F ⊥ 等位線：等位線切線 (−∂V/∂y, ∂V/∂x)
zero("s13-2 F ⊥ 等位線", F[0] * (-sp.diff(Vs, y)) + F[1] * sp.diff(Vs, x))

# s14-1 ∇·(rⁿ r⃗)
nn_ = sp.Symbol("n")
rr3 = sp.sqrt(x ** 2 + y ** 2 + z ** 2)
div = sum(sp.diff(rr3 ** nn_ * q, q) for q in (x, y, z))
zero("s14-1 ∇·(rⁿ r⃗) = (n+3) rⁿ", div - (nn_ + 3) * rr3 ** nn_)
zero("s14-1 n=-3 散度 0", div.subs(nn_, -3))
flux = sp.integrate(sp.integrate(Rs ** -3 * Rs * Rs ** 2 * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
zero("s14-1 任意半徑球面通量 4π", flux - 4 * sp.pi)
# 兩個同心球之間的殼：通量差為 0（與散度 0 一致）
zero("s14-1 殼層淨通量 0", flux.subs(Rs, 2) - flux.subs(Rs, 1))
# 數值：偏心的立方體（不含原點）通量為 0；含原點為 4π
def cube_flux(c0, half, N=200):
    g = (np.arange(N) + 0.5) / N * 2 * half - half
    U, Vv = np.meshgrid(g, g)
    dA = (2 * half / N) ** 2; tot = 0
    for ax in range(3):
        for sgn in (+1, -1):
            P = np.zeros((3,) + U.shape)
            others = [i for i in range(3) if i != ax]
            P[ax] = c0[ax] + sgn * half
            P[others[0]] = c0[others[0]] + U; P[others[1]] = c0[others[1]] + Vv
            rn = np.sqrt((P ** 2).sum(0))
            tot += (sgn * P[ax] / rn ** 3).sum() * dA
    return tot
close("s14-1 含原點的立方體通量 ≈ 4π", cube_flux(np.array([0.1, -0.2, 0.05]), 1.0), 4 * math.pi, 2e-3)
close("s14-1 不含原點的立方體通量 ≈ 0", cube_flux(np.array([3.0, 0.5, 0.0]), 1.0), 0, 2e-3)
# s14-2 A = (x³,y³,z³) 穿過球面
divA = sum(sp.diff(q ** 3, q) for q in (x, y, z))
zero("s14-2 ∇·A = 3r²", divA - 3 * (x ** 2 + y ** 2 + z ** 2))
vol = sp.integrate(3 * r_ ** 2 * 4 * sp.pi * r_ ** 2, (r_, 0, Rs))
zero("s14-2 體積分 12πR⁵/5", vol - 12 * sp.pi * Rs ** 5 / 5)
xs, ys, zs = Rs * sp.sin(th) * sp.cos(ph), Rs * sp.sin(th) * sp.sin(ph), Rs * sp.cos(th)
direct = sp.integrate((xs ** 4 + ys ** 4 + zs ** 4) / Rs * Rs ** 2 * sp.sin(th), (th, 0, sp.pi), (ph, 0, 2 * sp.pi))
zero("s14-2 直接面積分 12πR⁵/5", direct - 12 * sp.pi * Rs ** 5 / 5)
zero("s14-2 ∮z⁴ dA = 4πR⁶/5", sp.integrate(zs ** 4 * Rs ** 2 * sp.sin(th), (th, 0, sp.pi), (ph, 0, 2 * sp.pi)) - 4 * sp.pi * Rs ** 6 / 5)

# s15-1 ∇×(ω×r) = 2ω
w1, w2, w3 = sp.symbols("w1 w2 w3")
Om = sp.Matrix([w1, w2, w3]); Vr = Om.cross(sp.Matrix([x, y, z]))
curl = lambda F: sp.Matrix([sp.diff(F[2], y) - sp.diff(F[1], z), sp.diff(F[0], z) - sp.diff(F[2], x), sp.diff(F[1], x) - sp.diff(F[0], y)])
zero("s15-1 ∇×(ω×r) = 2ω", (curl(Vr) - 2 * Om).norm())
zero("s15-1 ∇·(ω×r) = 0", sum(sp.diff(Vr[i], q) for i, q in enumerate((x, y, z))))
# 環流 / 面積 = 2ω（繞 z 軸、半徑 a 的圓）
circ = sp.integrate((sp.Matrix([0, 0, w3]).cross(sp.Matrix([aa * sp.cos(t), aa * sp.sin(t), 0]))).dot(sp.Matrix([-aa * sp.sin(t), aa * sp.cos(t), 0])), (t, 0, 2 * sp.pi))
zero("s15-1 環流/面積 = 2ω3", circ / (sp.pi * aa ** 2) - 2 * w3)
# s15-2 導線的場
Rw = sp.Symbol("R", positive=True)
Fin = sp.Matrix([-y, x, 0]); Fout = Rw ** 2 * sp.Matrix([-y, x, 0]) / (x ** 2 + y ** 2)
zero("s15-2 內部旋度 2k", (curl(Fin) - sp.Matrix([0, 0, 2])).norm())
zero("s15-2 外部旋度 0", curl(Fout).norm())
zero("s15-2 r=R 處連續", (Fin - Fout).subs({x: Rw, y: 0}).norm())
rho = sp.Symbol("rho", positive=True)
circ_out = sp.integrate((Rw ** 2 * sp.Matrix([-rho * sp.sin(t), rho * sp.cos(t), 0]) / rho ** 2).dot(sp.Matrix([-rho * sp.sin(t), rho * sp.cos(t), 0])), (t, 0, 2 * sp.pi))
zero("s15-2 外部任意圓環流 2πR²", circ_out - 2 * sp.pi * Rw ** 2)
zero("s15-2 = 旋度×內部面積", circ_out - 2 * sp.pi * Rw ** 2)
circ_in = sp.integrate(sp.Matrix([-rho * sp.sin(t), rho * sp.cos(t), 0]).dot(sp.Matrix([-rho * sp.sin(t), rho * sp.cos(t), 0])), (t, 0, 2 * sp.pi))
zero("s15-2 內部 ρ<R 環流 2πρ²", circ_in - 2 * sp.pi * rho ** 2)
# 不繞軸的圓（圓心 (3R,0)，半徑 R）環流 0：數值
Rv = 1.0; T = np.linspace(0, 2 * np.pi, 200001)
X_ = 3 * Rv + Rv * np.cos(T); Y_ = Rv * np.sin(T)
Fx = -Y_ / (X_ ** 2 + Y_ ** 2); Fy = X_ / (X_ ** 2 + Y_ ** 2)
close("s15-2 不繞軸的圓環流 0", np.trapz(Fx * (-Rv * np.sin(T)) + Fy * (Rv * np.cos(T)), T), 0, 1e-8)

# s16-1 使 ∮[(y³/3 - y)dx - (x³/3)dy] 最大的封閉曲線
Pf, Qf = y ** 3 / 3 - y, -x ** 3 / 3
curlz = sp.diff(Qf, x) - sp.diff(Pf, y)
zero("s16-1 旋度 = 1 - x² - y²", curlz - (1 - x ** 2 - y ** 2))
Imax = sp.integrate((1 - r_ ** 2) * r_, (r_, 0, 1), (th, 0, 2 * sp.pi))
check(f"s16-1 單位圓盤面積分 = π/2（{Imax}）", sp.simplify(Imax - sp.pi / 2) == 0)
lineU = sp.integrate((Pf * sp.diff(sp.cos(t), t) + Qf * sp.diff(sp.sin(t), t)).subs({x: sp.cos(t), y: sp.sin(t)}), (t, 0, 2 * sp.pi))
check(f"s16-1 直接沿單位圓 = π/2（{sp.simplify(lineU)}）", sp.simplify(lineU - sp.pi / 2) == 0)
sq = sp.integrate(curlz, (x, -1, 1), (y, -1, 1))
check(f"s16-1 正方形 = 4/3（{sq}）", sq == sp.Rational(4, 3))
rho_ = sp.Symbol("rho", positive=True)
Ir = sp.integrate((1 - r_ ** 2) * r_, (r_, 0, rho_)) * 2 * sp.pi
check("s16-1 半徑 ρ 的圓在 ρ=1 最大", sp.solve(sp.diff(Ir, rho_), rho_) == [1])
# 隨機區域（橢圓、偏移圓）都不超過 π/2
gx_, gy_ = np.meshgrid(np.linspace(-2, 2, 801), np.linspace(-2, 2, 801)); dA_ = (4 / 800) ** 2
f_ = 1 - gx_ ** 2 - gy_ ** 2
close("s16-1 數值：圓盤 ≈ π/2", (f_ * (gx_ ** 2 + gy_ ** 2 <= 1)).sum() * dA_, math.pi / 2, 3e-3)
for (aa_, bb_, cx_) in [(1.2, 0.8, 0), (1, 1, 0.3), (0.9, 0.9, 0), (1.1, 1.1, 0)]:
    mask = ((gx_ - cx_) / aa_) ** 2 + (gy_ / bb_) ** 2 <= 1
    check(f"s16-1 數值：橢圓 ({aa_},{bb_},{cx_}) 不超過 π/2", (f_ * mask).sum() * dA_ < math.pi / 2 - 1e-3)
# s16-2 同一邊界、兩個曲面
Fv = sp.Matrix([z, x, y])
check("s16-2 ∇×F = (1,1,1)", curl(Fv) == sp.Matrix([1, 1, 1]))
lineC = sp.integrate(Fv.subs({x: sp.cos(t), y: sp.sin(t), z: 0}).dot(sp.Matrix([-sp.sin(t), sp.cos(t), 0])), (t, 0, 2 * sp.pi))
check("s16-2 線積分 π", sp.simplify(lineC - sp.pi) == 0)
disk = sp.integrate(1 * r_, (r_, 0, 1), (th, 0, 2 * sp.pi))
check("s16-2 平面圓盤 π", sp.simplify(disk - sp.pi) == 0)
nh = sp.Matrix([sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph), sp.cos(th)])
hemi = sp.integrate(sp.Matrix([1, 1, 1]).dot(nh) * sp.sin(th), (th, 0, sp.pi / 2), (ph, 0, 2 * sp.pi))
check("s16-2 上半球面 π", sp.simplify(hemi - sp.pi) == 0)
# 下半球面（法向量朝下才與逆時針邊界一致）
hemi_low = sp.integrate(sp.Matrix([1, 1, 1]).dot(-nh) * sp.sin(th), (th, sp.pi / 2, sp.pi), (ph, 0, 2 * sp.pi))
check("s16-2 下半球面（法向量朝下… 即朝 -r̂）也是 π", sp.simplify(hemi_low - sp.pi) == 0)

print("\nALL PASS" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
