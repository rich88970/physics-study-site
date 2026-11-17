"""力學 Lecture 1 第 08、09、11–16 節「詳細解題」改寫後新增／拆開的中間數值獨立驗算（代號 M1b）。

用法：python tools/verify_mechanics_ch01_detail_M1b.py   全部通過時結束碼為 0。
"""
import math
import sys

import numpy as np
import sympy as sp

ok = True


def check(name, got, want, tol=1e-6):
    global ok
    try:
        good = bool(np.allclose(np.array(got, dtype=float), np.array(want, dtype=float), atol=tol, rtol=0))
    except Exception as e:  # noqa: BLE001
        good = False
        got = f"{got} ({e})"
    ok &= good
    print(("OK  " if good else "FAIL"), name)
    if not good:
        print("     got", got, "want", want)


def zero(name, expr):
    check(name, float(sp.simplify(expr) == 0), 1.0)


def lam2(t):
    return np.array([[math.cos(t), math.sin(t)], [-math.sin(t), math.cos(t)]])


def lamx(t):
    c, s = math.cos(t), math.sin(t)
    return np.array([[1, 0, 0], [0, c, s], [0, -s, c]])


def lamz(t):
    c, s = math.cos(t), math.sin(t)
    return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])


rng = np.random.default_rng(7)


def rand_orth(det=1):
    q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    if np.linalg.det(q) * det < 0:
        q[:, 0] *= -1
    return q


deg = math.radians

# ===================== 08 矩陣 =====================
A = np.array([[2, 1, 3], [-2, 2, 4], [-1, -3, -4]]); B = np.array([[-1, -2], [1, 2], [3, 4]])
check("ex-p39 AB", A @ B, [[8, 10], [16, 24], [-14, -20]])
check("ex-p39 拆開的和", [-2 + 1 + 9, -4 + 2 + 12, 2 + 2 + 12, 4 + 4 + 16, 1 - 3 - 12, 2 - 6 - 16], [8, 10, 16, 24, -14, -20])

A = np.array([[2, 1], [-1, 3]]); B = np.array([[-1, 2], [4, -2]])
check("ex-p40 AB", A @ B, [[2, 2], [13, -8]])
check("ex-p40 BA", B @ A, [[-4, 5], [10, -2]])
check("ex-p40 驗算 tr(AB)=tr(BA)=-6", [np.trace(A @ B), np.trace(B @ A)], [-6, -6])
check("ex-p40 驗算 |AB|=|BA|=|A||B|=-42", [np.linalg.det(A @ B), np.linalg.det(B @ A), np.linalg.det(A), np.linalg.det(B)], [-42, -42, 7, -6])
check("tm-1-4 驗算 B^T A^T", B.T @ A.T, [[2, 13], [2, -8]])

A = np.array([[1, 2, -1], [0, 3, 1], [2, 0, 1]]); B = np.array([[2, 1, 0], [0, -1, 2], [1, 1, 3]]); C = np.array([[2, 1], [4, 3], [1, 0]])
AB = A @ B
check("tm-1-14 AB", AB, [[1, -2, 1], [1, -2, 9], [5, 3, 3]])
check("tm-1-14 三個子行列式 -33,-42,13", [(-2) * 3 - 9 * 3, 1 * 3 - 9 * 5, 1 * 3 - (-2) * 5], [-33, -42, 13])
check("tm-1-14 (a) |AB|", np.linalg.det(AB), -104)
check("tm-1-14 |A|,|B|", [np.linalg.det(A), np.linalg.det(B)], [13, -8])
check("tm-1-14 (b) AC", A @ C, [[9, 7], [13, 9], [5, 2]])
check("tm-1-14 (c) (AB)C = A(BC)", [AB @ C, A @ (B @ C)], [[[-5, -5], [3, -5], [25, 14]]] * 2)
check("tm-1-14 (d)", AB - B.T @ A.T, [[0, -3, -4], [3, 0, 6], [4, -6, 0]])

X = rng.normal(size=(3, 4)); Y = rng.normal(size=(4, 2))
check("tm-1-4 (a) 隨機 (XY)^T = Y^T X^T", (X @ Y).T, Y.T @ X.T, 1e-12)
P = rng.normal(size=(3, 3)); Q = rng.normal(size=(3, 3))
check("tm-1-4 (b) 隨機 (PQ)^-1 = Q^-1 P^-1", np.linalg.inv(P @ Q), np.linalg.inv(Q) @ np.linalg.inv(P), 1e-9)

a, b, c, d = sp.symbols("a b c d")
As = sp.Matrix([[1, 1], [0, 1]]); Bs = sp.Matrix([[a, b], [c, d]]); N = sp.Matrix([[0, 1], [0, 0]])
check("self-s08-1 NB, BN", [list(N * Bs - sp.Matrix([[c, d], [0, 0]])) == [0] * 4, list(Bs * N - sp.Matrix([[0, a], [0, c]])) == [0] * 4], [1, 1])
sol = sp.solve(list(As * Bs - Bs * As), [c, d], dict=True)
check("self-s08-1 解 c=0, d=a", [len(sol) == 1 and sol[0] == {c: 0, d: a}], [1])
A2 = np.array([[1, 1], [0, 1]]); D2 = np.array([[1, 0], [0, 2]])
check("self-s08-1 例子 AB, BA", [A2 @ D2, D2 @ A2], [[[1, 2], [0, 2]], [[1, 1], [0, 2]]])
E = np.array([[2, 3], [0, 2]])
check("self-s08-1 驗算 a=2,b=3", [A2 @ E, E @ A2], [[[2, 5], [0, 2]]] * 2)

check("self-s08-2 λ(72°)^5 = 1", np.linalg.matrix_power(lam2(deg(72)), 5), np.eye(2), 1e-12)
check("self-s08-2 n=1..4 不是 1", [np.abs(np.linalg.matrix_power(lam2(deg(72)), n) - np.eye(2)).max() > 0.1 for n in range(1, 5)], [1] * 4)
check("self-s08-2 λ(144°) 最小 n=5、λ(90°) 最小 n=4",
      [min(n for n in range(1, 20) if np.allclose(np.linalg.matrix_power(lam2(deg(t)), n), np.eye(2))) for t in (144, 90)], [5, 4])
ds = [abs(math.sin(n)) + abs(1 - math.cos(n)) for n in range(1, 10001)]
nbest = int(np.argmin(ds)) + 1
check("self-s08-2 λ(1)^n 最接近 1 的 n=710、差約 6e-5", [nbest, abs(math.sin(710))], [710, 6.0e-5], 1e-5)

# ===================== 09 旋轉 =====================
check("ex-p43 θ=π/2", lam2(math.pi / 2) @ np.array([3.0, 5.0]), [5, -3], 1e-12)
P49 = lamx(deg(30)) @ np.array([2, 1, 3])
check("ex-p49 新座標", P49, [2, (3 + math.sqrt(3)) / 2, (3 * math.sqrt(3) - 1) / 2], 1e-12)
check("ex-p49 小數 2.366、2.098", P49[1:], [2.366, 2.098], 1e-3)
s3 = math.sqrt(3)
check("ex-p49 平方 (12+6√3)/4、(28-6√3)/4、總和 14", [P49[1] ** 2, P49[2] ** 2, P49 @ P49], [(12 + 6 * s3) / 4, (28 - 6 * s3) / 4, 14], 1e-12)

L1 = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]); L2 = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
check("tb-rot2 λ1 = λz(90°)、λ2 = λx(90°)", [lamz(deg(90)), lamx(deg(90))], [L1, L2], 1e-12)
check("tb-rot2 λ3 = λ2λ1", L2 @ L1, [[0, 1, 0], [0, 0, 1], [1, 0, 0]])
check("tb-rot2 λ4 = λ1λ2", L1 @ L2, [[0, 0, 1], [-1, 0, 0], [0, -1, 0]])
check("tb-rot2 det", [np.linalg.det(L2 @ L1), np.linalg.det(L1 @ L2)], [1, 1])

th, ph = sp.symbols("theta phi", real=True)
l1 = sp.Matrix([[sp.cos(th), sp.sin(th), 0], [-sp.sin(th), sp.cos(th), 0], [0, 0, 1]])
l2 = sp.Matrix([[1, 0, 0], [0, sp.cos(ph), sp.sin(ph)], [0, -sp.sin(ph), sp.cos(ph)]])
want50 = sp.Matrix([[sp.cos(th), sp.sin(th), 0], [-sp.cos(ph) * sp.sin(th), sp.cos(ph) * sp.cos(th), sp.sin(ph)],
                    [sp.sin(ph) * sp.sin(th), -sp.sin(ph) * sp.cos(th), sp.cos(ph)]])
zero("ex-p50 λ2λ1 一般式", sum(abs(e) for e in (l2 * l1 - want50)))
zero("ex-p50 λ1λ2 第 1 列", sum(abs(e) for e in ((l1 * l2).row(0) - sp.Matrix([[sp.cos(th), sp.sin(th) * sp.cos(ph), sp.sin(th) * sp.sin(ph)]]))))
check("ex-p50 θ=φ=90°", np.array(want50.subs({th: sp.pi / 2, ph: sp.pi / 2}), dtype=float), [[0, 1, 0], [0, 0, 1], [1, 0, 0]])
zero("ex-p50 第 2 列長度 1", sp.simplify(sum(e ** 2 for e in want50.row(1)) - 1))

r2 = 1 / math.sqrt(2)
x2p = np.array([0, 1, 0]); x3p = np.array([r2, 0, r2]); x1p = np.cross(x2p, x3p)
check("tm-1-1 x1' = x2' × x3'", x1p, [r2, 0, -r2], 1e-12)
L11 = np.array([x1p, x2p, x3p])
check("tm-1-1 λ = λy(45°)", L11, [[r2, 0, -r2], [0, 1, 0], [r2, 0, r2]], 1e-12)
check("tm-1-1 det=1、正交", [np.linalg.det(L11), np.abs(L11 @ L11.T - np.eye(3)).max()], [1, 0], 1e-12)

l11, l12, l21, l22 = sp.symbols("l11 l12 l21 l22", real=True)
lag = (l11 ** 2 + l12 ** 2) * (l21 ** 2 + l22 ** 2) - (l11 * l21 + l12 * l22) ** 2 - (l11 * l22 - l12 * l21) ** 2
zero("tm-1-5 直接展開恆等式（長度積 − 內積平方 = det²）", sp.expand(lag))
check("tm-1-5 旋轉 det=+1、鏡射 det=-1", [np.linalg.det(lam2(0.7)), np.linalg.det(np.array([[math.cos(0.7), math.sin(0.7)], [math.sin(0.7), -math.cos(0.7)]]))], [1, -1], 1e-12)

for al, tdeg in ((r2, -45), (-r2, 135)):
    M = np.array([[1, 0, 0], [0, al, -al], [0, al, al]])
    check(f"tm-1-15 α={al:+.4f} 正交、det=1", [np.abs(M @ M.T - np.eye(3)).max(), np.linalg.det(M)], [0, 1], 1e-12)
    check(f"tm-1-15 α={al:+.4f} = λx({tdeg}°)", M, lamx(deg(tdeg)), 1e-12)

n = np.ones(3) / math.sqrt(3)
check("tm-1-3 夾角 54.7°", math.degrees(math.acos(n[0])), 54.7356, 1e-3)
u = np.array([1.0, 0, 0]); phi = deg(120)
urot = u * math.cos(phi) + np.cross(n, u) * math.sin(phi) + n * (n @ u) * (1 - math.cos(phi))
check("tm-1-3 Rodrigues x1 → x2", urot, [0, 1, 0], 1e-12)
L13 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
check("tm-1-3 λ(1,1,1)=(1,1,1)", L13 @ np.ones(3), np.ones(3), 1e-12)
check("tm-1-3 trace=1+2cos120°=0、det=1", [np.trace(L13), 1 + 2 * math.cos(phi), np.linalg.det(L13)], [0, 0, 1], 1e-12)

mu, la = rand_orth(), rand_orth()
check("tb-orth 隨機 (μλ)^T(μλ)=I", (mu @ la).T @ (mu @ la), np.eye(3), 1e-12)
check("tb-orth det(μλ)=+1", np.linalg.det(mu @ la), 1, 1e-12)
check("tb-ex14 |λ2|=1、|λ6|=-1", [np.linalg.det(L2), np.linalg.det(-np.eye(3))], [1, -1], 1e-12)
lm = rand_orth()
check("tm-1-6 Σ_i λij λik = δjk", lm.T @ lm, np.eye(3), 1e-12)
xv = rng.normal(size=3)
check("tm-1-6 長度不變", np.linalg.norm(lm @ xv), np.linalg.norm(xv), 1e-12)
Av, Bv = rng.normal(size=3), rng.normal(size=3)
check("tb-inv 內積不變", (lm @ Av) @ (lm @ Bv), Av @ Bv, 1e-12)

check("self-s09-1 λ(φ)λ(θ)=λ(θ+φ)", lam2(0.4) @ lam2(1.1), lam2(1.5), 1e-12)
check("self-s09-1 cos75° = (√6−√2)/4", math.cos(deg(75)), (math.sqrt(6) - math.sqrt(2)) / 4, 1e-12)
check("self-s09-1 λ^T = λ(−θ) = λ^-1", [lam2(0.9).T, np.linalg.inv(lam2(0.9))], [lam2(-0.9)] * 2, 1e-12)
dt = 0.01
eps = np.array([[0, dt, 0], [-dt, 0, 0], [0, 0, 0]])
check("self-s09-2 ε² = diag(-δθ², -δθ², 0)", eps @ eps, np.diag([-dt ** 2, -dt ** 2, 0]), 1e-15)
xx = np.array([1.3, -0.4, 2.0])
check("self-s09-2 εx = −δθ×x", eps @ xx, -np.cross([0, 0, dt], xx), 1e-15)
check("self-s09-2 一次近似誤差 ≈ δθ²/2", np.abs(lamz(dt) @ np.array([1, 0, 0]) - np.array([1, -dt, 0])).max(), dt ** 2 / 2, 1e-7)

# ===================== 11 極座標 =====================
r, R, rho, Th = sp.symbols("r R rho Theta", positive=True)
check("ex-p57 I = ½ρπR⁴", [sp.simplify(rho * sp.integrate(r ** 3, (r, 0, R)) * 2 * sp.pi - rho * sp.pi * R ** 4 / 2) == 0], [1])
check("ex-p57 漏掉 r 的錯誤結果 2πρR³/3", [sp.simplify(rho * sp.integrate(r ** 2, (r, 0, R)) * 2 * sp.pi - sp.Rational(2, 3) * sp.pi * rho * R ** 3) == 0], [1])
check("ex-p63 驗算 r=2,v=4: v²/r = rω² = 8", [4 ** 2 / 2, 2 * (4 / 2) ** 2], [8, 8])

# tm-1-26：把 θ̇ 寫成 θ 的函數，d/dt f(θ) = f'(θ) θ̇
k, v = sp.symbols("k v", positive=True)
q = sp.symbols("q", real=True)  # θ
rq = k * (1 + sp.cos(q))
td = v / (k * sp.sqrt(2 * (1 + sp.cos(q))))
ddt = lambda f: sp.diff(f, q) * td  # noqa: E731
rd = ddt(rq); rdd = ddt(rd); tdd = ddt(td)
num = {k: 1.3, v: 0.8, q: 0.9}
check("tm-1-26 速率固定", float((rd ** 2 + rq ** 2 * td ** 2).subs(num)), 0.8 ** 2, 1e-12)
check("tm-1-26 θ̇ = v/√(2kr)", float(td.subs(num)), float((v / sp.sqrt(2 * k * rq)).subs(num)), 1e-12)
check("tm-1-26 θ̈", float(tdd.subs(num)), float((v ** 2 * sp.sin(q) / (4 * k ** 2 * (1 + sp.cos(q)) ** 2)).subs(num)), 1e-12)
check("tm-1-26 r̈ = −v²/4k", float(rdd.subs(num)), -0.8 ** 2 / (4 * 1.3), 1e-12)
ar = rdd - rq * td ** 2; at = rq * tdd + 2 * rd * td
check("tm-1-26 a_r = −3v²/4k", float(ar.subs(num)), -3 * 0.8 ** 2 / (4 * 1.3), 1e-12)
check("tm-1-26 a_θ", float(at.subs(num)), float((-3 * v ** 2 * sp.sin(q) / (4 * k * (1 + sp.cos(q)))).subs(num)), 1e-12)
check("tm-1-26 |a|", float(sp.sqrt(ar ** 2 + at ** 2).subs(num)), float((3 * v ** 2 / (4 * k) * sp.sqrt(2 / (1 + sp.cos(q)))).subs(num)), 1e-12)
check("tm-1-26 θ̇ = v/(2k cos(θ/2))", float(td.subs(num)), 0.8 / (2 * 1.3 * math.cos(0.45)), 1e-12)

t, w, r0 = sp.symbols("t omega r0", positive=True)
rt = r0 * sp.cosh(w * t)
zero("self-s11-1 r̈ = ω²r", sp.diff(rt, t, 2) - w ** 2 * rt)
check("self-s11-1 初始條件", [float(rt.subs({t: 0, r0: 1.7})), float(sp.diff(rt, t).subs({t: 0, r0: 1.7, w: 2}))], [1.7, 0])
zero("self-s11-1 N = 2mωṙ = 2mr0ω²sinh", 2 * w * sp.diff(rt, t) - 2 * r0 * w ** 2 * sp.sinh(w * t))

Aa = sp.integrate(sp.integrate(r, (r, 1, 1 + sp.cos(Th))), (Th, -sp.pi / 2, sp.pi / 2))
Ab = sp.integrate(sp.integrate(r, (r, 1 + sp.cos(Th), 1)), (Th, sp.pi / 2, 3 * sp.pi / 2))
check("self-s11-2 (a) 2+π/4、(b) 2−π/4", [float(Aa), float(Ab)], [2 + math.pi / 4, 2 - math.pi / 4], 1e-12)
check("self-s11-2 心臟線總面積 3π/2、重疊 5π/4−2", [float(sp.integrate((1 + sp.cos(Th)) ** 2 / 2, (Th, 0, 2 * sp.pi))), 1.5 * math.pi - float(Aa), math.pi - float(Ab)],
      [1.5 * math.pi, 1.25 * math.pi - 2, 1.25 * math.pi - 2], 1e-12)
pts = rng.uniform([-1, -1.6], [2, 1.6], size=(400000, 2))
rr = np.hypot(pts[:, 0], pts[:, 1]); tt = np.arctan2(pts[:, 1], pts[:, 0])
box = 3 * 3.2
mc_a = np.mean((rr <= 1 + np.cos(tt)) & (rr > 1)) * box
mc_b = np.mean((rr <= 1) & (rr > 1 + np.cos(tt))) * box
check("self-s11-2 Monte Carlo（40 萬點）在 2.785、1.215 附近（±0.03）", [mc_a, mc_b], [2 + math.pi / 4, 2 - math.pi / 4], 0.03)

# ===================== 12 柱座標與球座標 =====================
tt_ = sp.symbols("t", real=True)
rf, pf, zf = sp.Function("r")(tt_), sp.Function("p")(tt_), sp.Function("z")(tt_)
pos = sp.Matrix([rf * sp.cos(pf), rf * sp.sin(pf), zf])
acc = sp.diff(pos, tt_, 2)
rh = sp.Matrix([sp.cos(pf), sp.sin(pf), 0]); phh = sp.Matrix([-sp.sin(pf), sp.cos(pf), 0])
zero("ex-p66 a_r", (acc.dot(rh)) - (sp.diff(rf, tt_, 2) - rf * sp.diff(pf, tt_) ** 2))
zero("ex-p66 a_φ", (acc.dot(phh)) - (2 * sp.diff(rf, tt_) * sp.diff(pf, tt_) + rf * sp.diff(pf, tt_, 2)))

ph_, th_ = sp.symbols("phi theta", real=True)
check("ex-p69 V = 4πR³/3、漏掉 r²sinθ 的 2π²R", [float(sp.integrate(r ** 2, (r, 0, 1)) * sp.integrate(sp.sin(th_), (th_, 0, sp.pi)) * 2 * sp.pi), 2 * math.pi ** 2],
      [4 * math.pi / 3, 2 * math.pi ** 2], 1e-12)
check("ex-p70 ∫sin³ = 4/3", float(sp.integrate(sp.sin(th_) ** 3, (th_, 0, sp.pi))), 4 / 3, 1e-12)
check("ex-p70 I = 8πρR⁵/15 = 2MR²/5；∫r²dm = 3MR²/5", [8 / 15 * math.pi, 0.4 * 4 / 3 * math.pi, 4 * math.pi / 5, 0.6 * 4 / 3 * math.pi],
      [float(sp.integrate(r ** 4, (r, 0, 1)) * sp.Rational(4, 3) * 2 * sp.pi)] * 2 + [float(sp.integrate(r ** 4, (r, 0, 1)) * 2 * 2 * sp.pi)] * 2, 1e-12)
R1, R2, L, M = 0.3, 1.1, 2.0, 5.0
V71 = math.pi * L * (R2 ** 2 - R1 ** 2); rho71 = M / V71
check("ex-p71 I = M(R1²+R2²)/2", rho71 * (R2 ** 4 - R1 ** 4) / 4 * 2 * math.pi * L, M / 2 * (R1 ** 2 + R2 ** 2), 1e-12)

rs, ts, ps = sp.Function("r")(tt_), sp.Function("th")(tt_), sp.Function("ph")(tt_)
pos = rs * sp.Matrix([sp.sin(ts) * sp.cos(ps), sp.sin(ts) * sp.sin(ps), sp.cos(ts)])
acc = sp.diff(pos, tt_, 2)
er = sp.Matrix([sp.sin(ts) * sp.cos(ps), sp.sin(ts) * sp.sin(ps), sp.cos(ts)])
et = sp.Matrix([sp.cos(ts) * sp.cos(ps), sp.cos(ts) * sp.sin(ps), -sp.sin(ts)])
ep = sp.Matrix([-sp.sin(ps), sp.cos(ps), 0])
D = lambda f, n=1: sp.diff(f, tt_, n)  # noqa: E731
zero("tm-1-25 a_r", acc.dot(er) - (D(rs, 2) - rs * D(ts) ** 2 - rs * D(ps) ** 2 * sp.sin(ts) ** 2))
zero("tm-1-25 a_θ", acc.dot(et) - (rs * D(ts, 2) + 2 * D(rs) * D(ts) - rs * D(ps) ** 2 * sp.sin(ts) * sp.cos(ts)))
zero("tm-1-25 a_φ", acc.dot(ep) - (rs * D(ps, 2) * sp.sin(ts) + 2 * D(rs) * D(ps) * sp.sin(ts) + 2 * rs * D(ts) * D(ps) * sp.cos(ts)))
zero("tm-1-25 φ̂' = −(sinθ r̂ + cosθ θ̂)", sum(abs(e) for e in (sp.diff(ep, ps) + sp.sin(ts) * er + sp.cos(ts) * et)))

xs = sp.symbols("x", real=True)
check("tm-1-35 V = 16a³/3（a=1）", float(sp.integrate(4 * (1 - xs ** 2), (xs, -1, 1))), 16 / 3, 1e-12)
pts = rng.uniform(-1, 1, size=(400000, 3))
check("tm-1-35 Monte Carlo（±0.05）", np.mean((pts[:, 0] ** 2 + pts[:, 1] ** 2 <= 1) & (pts[:, 0] ** 2 + pts[:, 2] ** 2 <= 1)) * 8, 16 / 3, 0.05)

zc = sp.integrate(r ** 3, (r, 0, 1)) * sp.integrate(sp.cos(th_) * sp.sin(th_), (th_, 0, sp.pi / 2)) * 2 * sp.pi / (sp.Rational(2, 3) * sp.pi)
zs_ = sp.symbols("zz", real=True)
zd = sp.integrate(zs_ * (1 - zs_ ** 2), (zs_, 0, 1)) / sp.integrate(1 - zs_ ** 2, (zs_, 0, 1))
zsh = sp.integrate(sp.cos(th_) * sp.sin(th_), (th_, 0, sp.pi / 2)) * 2 * sp.pi / (2 * sp.pi)
zst = sp.integrate(r / 2 * r ** 2, (r, 0, 1)) / sp.integrate(r ** 2, (r, 0, 1))
check("self-s12-1 3/8、3/8、1/2、3/8（R=1）", [float(zc), float(zd), float(zsh), float(zst)], [3 / 8, 3 / 8, 1 / 2, 3 / 8], 1e-12)
al = sp.symbols("alpha", positive=True)
Vc = sp.integrate(r ** 2, (r, 0, 1)) * sp.integrate(sp.sin(th_), (th_, 0, al)) * 2 * sp.pi
check("self-s12-2 V(60°)=π/3、α=π/2、α=π", [float(Vc.subs(al, sp.pi / 3)), float(Vc.subs(al, sp.pi / 2)), float(Vc.subs(al, sp.pi))], [math.pi / 3, 2 * math.pi / 3, 4 * math.pi / 3], 1e-12)
check("self-s12-2 圓錐 π/8 + 球冠 5π/24", [math.pi * 0.75 * 0.5 / 3, float(sp.integrate(sp.pi * (1 - zs_ ** 2), (zs_, sp.Rational(1, 2), 1)))], [math.pi / 8, 5 * math.pi / 24], 1e-12)

# ===================== 13 梯度 =====================
x, y, z = sp.symbols("x y z", real=True)
gb = lambda f, p: [float(sp.diff(f, x).subs({x: p[0], y: p[1]})), float(sp.diff(f, y).subs({x: p[0], y: p[1]}))]  # noqa: E731
fb = -(x - 3) ** 2 - (y - 3) ** 2
check("ex-p81 (b) 三點", [gb(fb, (1, 1)), gb(fb, (3, 3)), gb(fb, (1, 3))], [[4, 4], [0, 0], [4, 0]])
fc = y ** 2 * sp.sin(x)
check("ex-p81 (c) 三點", [gb(fc, (1, 1)), gb(fc, (math.pi / 2, 1)), gb(fc, (math.pi, 3))], [[0.540, 1.683], [0, 2], [-9, 0]], 2e-3)
L90 = lamz(deg(90))
check("tb-grad 驗算：φ=x1，轉 90° 後梯度 (0,-1,0)", L90 @ np.array([1, 0, 0]), [0, -1, 0], 1e-12)
check("tm-1-30 驗算 ∇(xy)=(y,x,0)", [sp.diff(x * y, x) - y == 0, sp.diff(x * y, y) - x == 0], [1, 1])
check("tm-1-28 ∂/∂x ½ln(r²) = x/r²", [sp.simplify(sp.diff(sp.log(x ** 2 + y ** 2 + z ** 2) / 2, x) - x / (x ** 2 + y ** 2 + z ** 2)) == 0], [1])

g1 = np.array([4, -4, 2]); g2 = np.array([1, 1, 2])
cs = g1 @ g2 / (np.linalg.norm(g1) * np.linalg.norm(g2))
check("tm-1-29 點在曲面上", [2 ** 2 + 2 ** 2 + 1, 2 - 2 + 1], [9, 1])
check("tm-1-29 內積 4、長度 6 與 √6、cos=0.272、74.2°、補角 105.8°",
      [g1 @ g2, np.linalg.norm(g1), np.linalg.norm(g2), cs, math.degrees(math.acos(cs)), 180 - math.degrees(math.acos(cs))],
      [4, 6, math.sqrt(6), 0.2722, 74.21, 105.79], 5e-3)

h = 2 * x * y - 3 * x ** 2 - 4 * y ** 2 - 18 * x + 28 * y + 12
top = sp.solve([sp.diff(h, x), sp.diff(h, y)], [x, y])
check("tm-1-40 (a) 山頂 (-2,3)、72 m", [top[x], top[y], h.subs(top)], [-2, 3, 72])
hx, hy = [float(sp.diff(h, s).subs({x: 1, y: 1})) for s in (x, y)]
check("tm-1-40 (b) ∇h(1,1)=(-22,22)、坡度 31.1、α=88.2°、tanα=31.1",
      [hx, hy, math.hypot(hx, hy), math.degrees(math.acos(1 / math.sqrt(hx ** 2 + hy ** 2 + 1))), math.tan(math.acos(1 / math.sqrt(969)))],
      [-22, 22, 31.11, 88.16, 31.11], 1e-2)

T = 100 - x ** 2 - 2 * y ** 2
check("self-s13-1 ∇T(1,1)=(-2,-4)、2√5", gb(T, (1, 1)) + [math.hypot(2, 4)], [-2, -4, 2 * math.sqrt(5)], 1e-12)
for xp in (1.0, 0.5, 0.2):
    gx, gy = gb(T, (xp, xp ** 2))
    check(f"self-s13-1 y=x² 在 x={xp} 的切線平行 ∇T", 1 * gy - 2 * xp * gx, 0, 1e-12)
Fv = np.array([-2.0, -4.0]); toO = np.array([-2.0, -1.0])
cb = Fv @ toO / (np.linalg.norm(Fv) * np.linalg.norm(toO))
check("self-s13-2 cosβ=0.8、β=36.9°", [cb, math.degrees(math.acos(cb))], [0.8, 36.87], 1e-2)
kk = sp.symbols("k", positive=True)
Fx, Fy = -kk * x, -4 * kk * y
zero("self-s13-2 (F×r)_z = 3kxy", Fx * y - Fy * x - 3 * kk * x * y)
check("self-s13-2 橢圓 x²+4y²=8、法向量 (4,8)", [2 ** 2 + 4 * 1, 2 * 2, 8 * 1], [8, 4, 8])

# ===================== 14 散度 =====================
rr_ = sp.sqrt(x ** 2 + y ** 2 + z ** 2)
nn = sp.symbols("n", real=True)
grad = lambda f: sp.Matrix([sp.diff(f, s) for s in (x, y, z)])  # noqa: E731
div = lambda Fm: sum(sp.diff(Fm[i], s) for i, s in enumerate((x, y, z)))  # noqa: E731
rvec = sp.Matrix([x, y, z])
zero("tm-1-31 (a) ∇rⁿ = n r^(n-2) r⃗", sum(abs(e) for e in (grad(rr_ ** nn) - nn * rr_ ** (nn - 2) * rvec)))
zero("tm-1-31 (c) ∇²ln r = 1/r²", div(grad(sp.log(rr_))) - 1 / rr_ ** 2)
sr = sp.symbols("sr", positive=True)
pt = {x: 0.7, y: -1.2, z: 0.4, nn: 2.5}
for gname, gexpr in (("r^n", lambda s: s ** nn), ("sin r", sp.sin), ("e^-r", lambda s: sp.exp(-s))):
    lhs = div(gexpr(rr_) * rvec)
    rhs = (3 * gexpr(sr) + sr * sp.diff(gexpr(sr), sr)).subs(sr, rr_)
    check(f"tm-1-31 ∇·(g(r) r⃗) = 3g + r g'（g={gname}，代數值）", float(lhs.subs(pt)), float(rhs.subs(pt)), 1e-12)
zero("tm-1-36 ∇·A = 1", div(sp.Matrix([x, -y, z])) - 1)
cc, dd = 1.0, 2.0
ph_n = np.linspace(0, 2 * math.pi, 200001)
side = np.trapz(cc * np.cos(2 * ph_n) * cc, ph_n) * dd
check("tm-1-36 側面 0、總和 πc²d", [side, side + dd * math.pi * cc ** 2], [0, math.pi * cc ** 2 * dd], 1e-6)
zero("tm-1-37 ∇·(r²r⃗) = 5r²", div(rr_ ** 2 * rvec) - 5 * rr_ ** 2)
check("tm-1-37 4πR⁵（R=1.3）", [1.3 ** 3 * 4 * math.pi * 1.3 ** 2, float(sp.integrate(5 * r ** 2 * 4 * sp.pi * r ** 2, (r, 0, sp.Rational(13, 10))))], [4 * math.pi * 1.3 ** 5] * 2, 1e-9)
zero("self-s14-1 ∇·(r⃗/r³) = 0", div(rvec / rr_ ** 3))
check("self-s14-1 球面通量 4π", float(sp.integrate(sp.sin(th_), (th_, 0, sp.pi)) * 2 * sp.pi), 4 * math.pi, 1e-12)
zero("self-s14-2 ∇·A = 3r²", div(sp.Matrix([x ** 3, y ** 3, z ** 3])) - 3 * rr_ ** 2)
z4 = sp.integrate(sp.cos(th_) ** 4 * sp.sin(th_), (th_, 0, sp.pi)) * 2 * sp.pi
check("self-s14-2 ∮z⁴dA = 4π/5（R=1）、通量 12π/5", [float(z4), 3 * float(z4), float(sp.integrate(3 * r ** 2 * 4 * sp.pi * r ** 2, (r, 0, 1)))], [4 * math.pi / 5, 12 * math.pi / 5, 12 * math.pi / 5], 1e-12)
check("self-s14-2 驗算 ∮z²dA = 4π/3", float(sp.integrate(sp.cos(th_) ** 2 * sp.sin(th_), (th_, 0, sp.pi)) * 2 * sp.pi), 4 * math.pi / 3, 1e-12)

# ===================== 15 旋度 =====================
curl = lambda Fm: sp.Matrix([sp.diff(Fm[2], y) - sp.diff(Fm[1], z), sp.diff(Fm[0], z) - sp.diff(Fm[2], x), sp.diff(Fm[1], x) - sp.diff(Fm[0], y)])  # noqa: E731
ff = sp.Function("f")
zero("ex-p99 ∇×[r⃗ f(r)] = 0", sum(abs(sp.simplify(e)) for e in curl(rvec * ff(rr_))))
zero("ex-p99 驗算 r⃗/r³ 的 x 分量", sp.simplify(curl(rvec / rr_ ** 3)[0]))
check("ex-p101 (b) 旋度 2k", list(curl(sp.Matrix([-y, x, 0]))), [0, 0, 2])
zero("ex-p101 (c) 原點外旋度 0", sp.simplify(curl(sp.Matrix([-y / (x ** 2 + y ** 2), x / (x ** 2 + y ** 2), 0]))[2]))
zero("ex-p101 (c) ∂Fy/∂x = (y²−x²)/(x²+y²)²", sp.simplify(sp.diff(x / (x ** 2 + y ** 2), x) - (y ** 2 - x ** 2) / (x ** 2 + y ** 2) ** 2))
tn = np.linspace(0, 2 * math.pi, 200001)
for Rr in (1.0, 2.5):
    X_, Y_ = Rr * np.cos(tn), Rr * np.sin(tn)
    circ_b = np.trapz(-Y_ * np.gradient(X_, tn) + X_ * np.gradient(Y_, tn), tn)
    circ_c = np.trapz((-Y_ * np.gradient(X_, tn) + X_ * np.gradient(Y_, tn)) / Rr ** 2, tn)
    check(f"ex-p101 R={Rr}: (b) 功 2πR²、(c) 功 2π", [circ_b, circ_c], [2 * math.pi * Rr ** 2, 2 * math.pi], 1e-6)
w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
vv = sp.Matrix([w1, w2, w3]).cross(rvec)
check("self-s15-1 v = ω×r 展開", [sp.simplify(e) for e in (vv - sp.Matrix([w2 * z - w3 * y, w3 * x - w1 * z, w1 * y - w2 * x]))], [0, 0, 0])
zero("self-s15-1 ∇×v = 2ω", sum(abs(e) for e in (curl(vv) - 2 * sp.Matrix([w1, w2, w3]))))
zero("self-s15-1 ∇·v = 0", div(vv))
Rw, rho_ = 0.7, 1.9
check("self-s15-2 外部環流 2πR²（ρ=1.9）、ρ=R 時場連續", [Rw ** 2 / rho_ * 2 * math.pi * rho_, Rw ** 2 * Rw / Rw ** 2], [2 * math.pi * Rw ** 2, Rw], 1e-12)
zero("self-s15-2 外部旋度 0", sp.simplify(curl(sp.Matrix([-y, x, 0]) * sp.Rational(49, 100) / (x ** 2 + y ** 2))[2]))

# ===================== 16 Stokes =====================
for (ax_, by_) in ((1.0, 1.0), (2.0, 0.5)):
    X_, Y_ = ax_ * np.cos(tn), by_ * np.sin(tn)
    area = 0.5 * np.trapz(X_ * np.gradient(Y_, tn) - Y_ * np.gradient(X_, tn), tn)
    check(f"ex-p108 橢圓 a={ax_}, b={by_}：½∮(x dy − y dx) = πab", area, math.pi * ax_ * by_, 1e-6)
check("tm-1-38 旋度 (-1,-1,-1)", list(curl(sp.Matrix([y, z, x]))), [-1, -1, -1])
check("tm-1-38 ∮y dx = −π", np.trapz(np.sin(tn) * (-np.sin(tn)), tn), -math.pi, 1e-6)
rr2 = sp.symbols("rr", positive=True)
direct = sp.integrate(sp.integrate((-2 * rr2 * sp.cos(th_) - 2 * rr2 * sp.sin(th_) - 1) * rr2, (rr2, 0, 1)), (th_, 0, 2 * sp.pi))
check("tm-1-38 直接算 −π", float(direct), -math.pi, 1e-12)
Fs = sp.Matrix([y ** 3 / 3 - y, -x ** 3 / 3, 0])
zero("self-s16-1 (∇×F)_z = 1 − x² − y²", curl(Fs)[2] - (1 - x ** 2 - y ** 2))
check("self-s16-1 I_max = π/2", float(sp.integrate((1 - rr2 ** 2) * rr2, (rr2, 0, 1)) * 2 * sp.pi), math.pi / 2, 1e-12)
X_, Y_ = np.cos(tn), np.sin(tn)
line = np.trapz((Y_ ** 3 / 3 - Y_) * (-np.sin(tn)) - X_ ** 3 / 3 * np.cos(tn), tn)
check("self-s16-1 (b) 直接沿單位圓 π/2；∫sin⁴ = 3π/4", [line, np.trapz(np.sin(tn) ** 4, tn)], [math.pi / 2, 3 * math.pi / 4], 1e-6)
check("self-s16-1 (c) 正方形 4/3", float(sp.integrate(sp.integrate(1 - x ** 2 - y ** 2, (x, -1, 1)), (y, -1, 1))), 4 / 3, 1e-12)
check("self-s16-2 旋度 (1,1,1)", list(curl(sp.Matrix([z, x, y]))), [1, 1, 1])
hemi = sp.integrate(sp.integrate((sp.sin(th_) * (sp.cos(ph_) + sp.sin(ph_)) + sp.cos(th_)) * sp.sin(th_), (th_, 0, sp.pi / 2)), (ph_, 0, 2 * sp.pi))
check("self-s16-2 圓盤 π、半球面 π、線積分 π", [math.pi, float(hemi), np.trapz(np.cos(tn) ** 2, tn)], [math.pi] * 3, 1e-6)

# ===================== 審查報告 D 的修正 =====================
check("ex-p70 unit density ρ=1：I = 8π/15·R⁵（R=1）", float(sp.integrate(r ** 4, (r, 0, 1)) * sp.Rational(4, 3) * 2 * sp.pi), 8 * math.pi / 15, 1e-12)
check("self-s06-2 (b) ω×r3 = (bz−cy, cx−az, ay−bx) = (-1,2,-1)", np.cross([1, 2, 3], [1, 1, 1]), [-1, 2, -1])
check("self-s15-1 圓心不在軸上時環流仍是 2ω·面積（ω=k̂，圓心 (0.8,-0.3)，a=0.5）",
      np.trapz(-(0.5 * np.sin(tn) - 0.3) * (-0.5 * np.sin(tn)) + (0.8 + 0.5 * np.cos(tn)) * (0.5 * np.cos(tn)), tn), 2 * math.pi * 0.25, 1e-6)

print("全部通過" if ok else "有失敗項目")
sys.exit(0 if ok else 1)
