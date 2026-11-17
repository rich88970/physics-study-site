"""近代物理第 1 章（Beiser Relativity）所有數值答案的獨立重算：python tools/verify_modern_ch01.py"""
from math import sqrt, atan, tan, radians, degrees
c = 2.998e8
def g(b): return 1/sqrt(1-b*b)
def show(k, *v): print(k, *v)

# Example 1.1
show("Ex1.1 v", c*sqrt(1-(3600/3601)**2))
# Ex 4
show("Ex4 t0 min", 40*sqrt(1-0.49))
# Ex 5
b = 2e8/c; t = 1/(1-sqrt(1-b*b)); show("Ex5 b,t", b, t)
# Ex 6 airplane
b = 300/c; show("Ex6 t s", 2/b**2, "yr", 2/b**2/3.156e7)
# Ex 9
show("Ex9 d m", 0.99*c*g(0.99)*1e-7, g(0.99))
# Ex 1.2 judge
nu, nu0 = 5.60, 4.80
v = c*(nu**2-nu0**2)/(nu**2+nu0**2); show("Ex1.2 v", v, v*3.6, "fine", v*3.6-80)
# Ex 1.3 / 107-1
b = 6.12e7/c; lam = 500*sqrt((1+b)/(1-b)); show("Ex1.3 b lam shift", b, lam, lam-500)
# Ex 10
show("Ex10 rate", 1e4*sqrt(0.03/1.97))
# Ex 12
show("Ex12 b", 5/13)
# Ex 14 radar
v = 150/3.6; show("Ex14 dnu Hz single, double", 15e9*v/c, 2*15e9*v/c)
# Ex 17
show("Ex17 ft", 6*sqrt(1-0.81))
# Ex 20
b = sqrt(1-0.25); show("Ex20 b t", b, 0.5/(b*c))
# Ex 21
show("Ex21 deg", degrees(atan(tan(radians(10))/sqrt(1-0.49))))
# Ex 22
T = 2*12/0.6; tA = T*0.8; show("Ex22 T tA", T, tA)
f_out = sqrt(0.4/1.6); show("Ex22 rec rate out/in", f_out, 1/f_out)
# A receives: outward 16 y own time * 0.5/y = 8, inward 16 * 2 = 32 => 40 ; B receives: out signals arrive over 20+12=32 y at 0.5 -> 16, last 8 y at 2 -> 16 => 32
show("Ex22 A rcv", 16*0.5+16*2, "B rcv", 32*0.5+8*2)
# Ex 23
T = 8/0.9; show("Ex23 T ship diff", T, T*sqrt(1-0.81), T-T*sqrt(1-0.81))
# Ex 1.4 twin
show("Ex1.4", sqrt(1.8/0.2), sqrt(0.2/1.8))
# Ex 24
show("Ex24", 2*g(.4)/g(.2), 2*g(.8)/g(.4))
# Ex 1.6 / 107-2
show("Ex1.6", 2*1/sqrt(1-0.36), 2*10/sqrt(1-0.36))
# Ex 1.7
P = 1.4e3*4*3.14159265*(1.5e11)**2; show("Ex1.7 P m", P, P/(3e8)**2)
# Ex 29
show("Ex29", sqrt(1-1/4))
# Ex 31
show("Ex31 classical b", sqrt(2*0.1/0.511), sqrt(2*0.1/0.511)*c)
gg = 1+0.1/0.511; show("Ex31 rel g b v", gg, sqrt(1-1/gg**2), sqrt(1-1/gg**2)*c)
# Ex 35
b1, b2 = 1.2e8/c, 2.4e8/c
show("Ex35 W MeV", (g(b2)-g(b1))*0.511, b1, b2)
show("Ex35 c=3e8", (g(0.8)-g(0.4))*0.511)
# Ex 36
gm = 1/sqrt(1-1/1.5**2); show("Ex36 KE MeV", (gm-1)*0.511, gm)
# Ex 41
gam = 1e5*365.25*24*60/5; show("Ex41 gamma E eV", gam, gam*938.3e6)
# Ex 42
pc = sqrt(10**2+2*10*938.3); show("Ex42 pc MeV", pc)
# Ex 1.8
show("Ex1.8", sqrt(0.511**2+2**2))
# Ex 47
gg = 3.5/0.938; show("Ex47 b p", sqrt(1-1/gg**2), sqrt(3.5**2-0.938**2))
# Ex 49 / 107-3
m = (335**2-62**2)/(2*62); show("Ex49 m b", m, 335/(m+62))
# Ex 50 / 115-3
m = sqrt(4**2-1.45**2); show("Ex50 m KE E'", m, 4-m, sqrt(m*m+4))
# 107-4 Anna
show("107-4 dt ns", g(0.6)*0.6*c*2/c**2*1e9, "c=3e8", 1.25*0.6*2/3e8*1e9)
# 107-5 motorcycles
vx = -0.75; vy = -0.9*sqrt(1-0.75**2); show("107-5", vx, vy, sqrt(vx*vx+vy*vy))
# Ex 1.11
show("Ex1.11", (0.5+0.9)/(1+0.45))
# Ex 51
dt, dx = 2e-3, 1e5
show("Ex51 v dt'", dx/dt, sqrt(dt**2-(dx/c)**2))
# Ex 52
show("Ex52 dt'", sqrt(160e3**2-100e3**2)/c, "v", sqrt(1-(100/160)**2))
# Ex 54
show("Ex54", (0.5+0.5)/(1+0.25), (-0.6+0.5)/(1-0.3))
# Ex 55
show("Ex55", (0.8+0.9)/(1+0.72))
# Ex 56
u = (0.8-0.5)/(1-0.4); show("Ex56", (g(0.8)-1)*0.511, u, (g(u)-1)*0.511)
# Ex 38 threshold
show("Ex38 E1/mc2", (16-2)/2, "KE", 7-1)
# self AppII
show("AppII v/c dx'", 300/600, sqrt(600**2-300**2))
# ---- variants
show("V twin 0.6c 6ly", 2*6/0.6, 2*6/0.6*0.8)
p1 = g(0.8)*1*0.8; m2 = p1/(g(0.6)*0.6); show("V explode m2 M", m2, g(0.8)*1+g(0.6)*m2)
m = (1.2**2-0.5**2)/(2*0.5); show("V 107-3 m b", m, 1.2/(m+0.5))
show("V Anna 0.8c 3m ns", g(0.8)*0.8*3/3e8*1e9)
vx = -0.6; vy = 0.8*sqrt(1-0.36); show("V moto", vx, vy, sqrt(vx*vx+vy*vy))
show("V clock 1s/day", c*sqrt(1-(86400/86401)**2), c*sqrt(2/86400))
b = 0.6; show("V galaxy 450->? approach 0.1c", 500*sqrt(0.9/1.1))
lam_ratio = 615/500; b = (lam_ratio**2-1)/(lam_ratio**2+1); show("V given shift 500->600 b", ((1.2**2-1)/(1.2**2+1)))
show("V threshold pp", 6*938.3)
show("V E5 p4", sqrt(25-16), 4/5)
# 審查後新增的習題
show("Ex11 lam", 550*sqrt(1.05/0.95))
show("Ex33 b", sqrt(1-1/21**2))
show("Ex34", (g(.4)-1)/(g(.2)-1), (g(.8)-1)/(g(.4)-1))
show("Ex5 (c=3e8)", 1/(1-sqrt(1-(2/3)**2)))
