"""獨立重算網站中出現的數值答案。"""
import math
import numpy as np

ok = True
def check(name, got, want, tol=1e-3):
    global ok
    good = np.allclose(np.array(got, dtype=float), np.array(want, dtype=float), atol=tol)
    ok &= bool(good)
    print(("OK  " if good else "FAIL"), name, np.round(np.array(got, dtype=float), 4).tolist(), "expected", want)

# 第一節：自由落體 x(1)
check("freefall x(1)", -4.9 + 5 + 20, 20.1)
# 第二節：(-1, √3) 的極座標
check("polar r,theta", [math.hypot(-1, math.sqrt(3)), math.degrees(math.atan2(math.sqrt(3), -1))], [2, 120])
# p.27 / p.28
check("p27 dot", np.dot([3, -1, 2], [-1, -1, 1]), 0)
check("p28 angle", math.degrees(math.acos(2 / (math.sqrt(2) * 2))), 45)
# Example 1.5
A = np.array([1, 2, -2]); B = np.array([4, 2, -3])
check("ex1.5 |A-B|", np.linalg.norm(A - B), math.sqrt(10))
check("ex1.5 theta", math.degrees(math.acos(A @ B / (np.linalg.norm(A) * np.linalg.norm(B)))), 29.94, 0.01)
check("ex1.5 B_A", A @ B / np.linalg.norm(A), 14 / 3)
# 1-7
d1 = np.array([1, 1, 1]); d2 = np.array([-1, 1, 1])
check("1-7 angle", math.degrees(math.acos(d1 @ d2 / 3)), 70.53, 0.01)
# 1-9
A = np.array([1, 2, -1]); B = np.array([-2, 3, 1])
check("1-9a", list(A - B) + [np.linalg.norm(A - B)], [3, -1, -2, math.sqrt(14)])
check("1-9b", A @ B / np.linalg.norm(A), math.sqrt(6) / 2)
check("1-9c", math.degrees(math.acos(A @ B / (np.linalg.norm(A) * np.linalg.norm(B)))), 70.89, 0.01)
check("1-9d", np.cross(A, B), [5, 1, 7])
check("1-9e", np.cross(A - B, A + B), [10, 2, 14])
# 1-12 例子
a, b, c = np.array([1, 0, 0]), np.array([0, 2, 0]), np.array([0, 0, 3])
n = np.cross(b - a, c - a)
check("1-12 n", n, [6, 3, 2]); check("1-12 d", abs(a @ np.cross(b, c)) / np.linalg.norm(n), 6 / 7); check("1-12 area", np.linalg.norm(n) / 2, 3.5)
# 1-13 隨機驗證
rng = np.random.default_rng(1)
Av = rng.normal(size=3); X = rng.normal(size=3); Bv = np.cross(Av, X); phi = Av @ X
check("1-13 X", (phi * Av - np.cross(Av, Bv)) / (Av @ Av), X)
# 自編角速度
check("omega x r", np.cross([0, 0, 2], [1, 0, 1]), [0, 2, 0])
# 1-10 在 wt = pi/2，b = w = 1
wt = math.pi / 2
v = np.array([2 * math.cos(wt), -math.sin(wt)]); acc = np.array([-2 * math.sin(wt), -math.cos(wt)])
check("1-10 v.a", v @ acc, 0)
# 1-27 隨機數值驗證（有限差分）
def f(t):
    r = np.array([math.sin(t), t * t, math.cos(2 * t)]); vv = np.array([math.cos(t), 2 * t, -2 * math.sin(2 * t)])
    return np.cross(r, np.cross(vv, r))
t0, h = 0.7, 1e-6
lhs = (f(t0 + h) - f(t0 - h)) / (2 * h)
r = np.array([math.sin(t0), t0 * t0, math.cos(2 * t0)]); vv = np.array([math.cos(t0), 2 * t0, -2 * math.sin(2 * t0)]); aa = np.array([-math.sin(t0), 2, -4 * math.cos(2 * t0)])
rhs = (r @ r) * aa + (r @ vv) * vv - (vv @ vv + r @ aa) * r
check("1-27 identity", lhs, rhs, 1e-5)
# p.39 / p.40
A = np.array([[2, 1, 3], [-2, 2, 4], [-1, -3, -4]]); B = np.array([[-1, -2], [1, 2], [3, 4]])
check("ex1.2 AB", A @ B, [[8, 10], [16, 24], [-14, -20]])
A = np.array([[2, 1], [-1, 3]]); B = np.array([[-1, 2], [4, -2]])
check("ex1.3 AB", A @ B, [[2, 2], [13, -8]]); check("ex1.3 BA", B @ A, [[-4, 5], [10, -2]])
check("1-4 transpose example", B.T @ A.T, [[2, 13], [2, -8]])
# 1-14
A = np.array([[1, 2, -1], [0, 3, 1], [2, 0, 1]]); B = np.array([[2, 1, 0], [0, -1, 2], [1, 1, 3]]); C = np.array([[2, 1], [4, 3], [1, 0]])
check("1-14 AB", A @ B, [[1, -2, 1], [1, -2, 9], [5, 3, 3]])
check("1-14a", np.linalg.det(A @ B), -104); check("detA,detB", [np.linalg.det(A), np.linalg.det(B)], [13, -8])
check("1-14b", A @ C, [[9, 7], [13, 9], [5, 2]])
check("1-14c", A @ B @ C, [[-5, -5], [3, -5], [25, 14]]); check("BC", B @ C, [[8, 5], [-2, -3], [9, 4]])
check("1-14d", A @ B - B.T @ A.T, [[0, -3, -4], [3, 0, 6], [4, -6, 0]])
# 二維旋轉 P=(3,2)
for th, want in [(30, [3.598, 0.232]), (90, [2, -3])]:
    t = math.radians(th)
    check(f"rot2d {th}", [3 * math.cos(t) + 2 * math.sin(t), -3 * math.sin(t) + 2 * math.cos(t)], want)
# Example 1.1
t = math.radians(30)
L = np.array([[1, 0, 0], [0, math.cos(t), math.sin(t)], [0, -math.sin(t), math.cos(t)]])
P2 = L @ [2, 1, 3]
check("ex1.1", P2, [2, 2.366, 2.098]); check("ex1.1 length", P2 @ P2, 14)
# 1-1
s = 1 / math.sqrt(2)
L1 = np.array([[s, 0, -s], [0, 1, 0], [s, 0, s]])
check("1-1 orthogonal", L1 @ L1.T, np.eye(3)); check("1-1 det", np.linalg.det(L1), 1)
check("1-1 new x3 axis", L1[2], [s, 0, s])
# 1-15
for al in (s, -s):
    M = np.array([[1, 0, 0], [0, al, -al], [0, al, al]])
    check(f"1-15 alpha={al:+.3f}", M @ M.T, np.eye(3))
# 1-3
n3 = np.ones(3) / math.sqrt(3)
def rod(u, n, ph):
    c, sn = math.cos(ph), math.sin(ph); return u * c + np.cross(n, u) * sn + n * (n @ u) * (1 - c)
Lr = np.array([rod(e, n3, math.radians(120)) for e in np.eye(3)])
check("1-3 lambda", Lr, [[0, 1, 0], [0, 0, 1], [1, 0, 0]])
check("1-3 lambda^3", np.linalg.matrix_power(np.round(Lr), 3), np.eye(3))
# 第二批圖解中的數字
check("passive P=(3,1) 30deg", [3 * math.cos(t) + math.sin(t), -3 * math.sin(t) + math.cos(t)], [3.098, -0.634])
check("active P=(3,1) 30deg", [3 * math.cos(t) - math.sin(t), 3 * math.sin(t) + math.cos(t)], [2.098, 2.366])
Ax, Xx = np.array([0, 0, 1.6]), np.array([1.2, 0.6, 1.0])
Bx = np.cross(Ax, Xx); phx = Ax @ Xx
check("solve-x B", Bx, [-0.96, 1.92, 0]); check("solve-x AxB", np.cross(Ax, Bx), [-3.072, -1.536, 0])
check("solve-x recover", (phx * Ax - np.cross(Ax, Bx)) / (Ax @ Ax), Xx)
At, Bt = np.array([2, 0, 0]), np.array([0.8, 1.8, 0])
for sh in (0, 1.2):
    check(f"triple volume shear={sh}", np.cross(At, Bt) @ np.array([0.6 + sh, 0.5, 1.6]), 5.76)
check("cosine law 140deg", 25 - 24 * math.cos(math.radians(140)), 43.385, 0.01)
check("polar shadow sqrt5 & |A|", [math.hypot(2, 1), np.linalg.norm([2, 1, 2])], [math.sqrt(5), 3])
# 乘積律動畫數字
check("product corner %", 1.2 * 0.9 / (3 * 1.2 + 4 * 0.9 + 1.2 * 0.9) * 100, 13.04, 0.01)
print("ALL OK" if ok else "SOME FAILED")
