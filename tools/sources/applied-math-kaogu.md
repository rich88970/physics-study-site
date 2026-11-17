# 應用數學：2021-2025 期中考古題與歷次作業解題過程

收錄 2021–2025 年期中考考古題 21 題，以及五組作業 16 題，共 37 題。

**注意：** 2025 年考古題第 4 題的功率頻譜附答與其 Fourier 係數不一致；作業一第 1、2 題的指定點不構成通常可微的初值解。兩處都在該題說明。

**主題目錄**（依課程順序分成九個主題；同一主題內先放作業，再依年份由新到舊放期中考古題）：

- 一、一階：可分離變數——作業一第 1 題；2024 年 11 月期中第 2 題（非線性可分離）；2021 年 11 月期中第 2 題（平方速度阻力下自由落體）。
- 二、一階：線性方程與積分因子——作業一第 2 題（先交換變數）、第 3 題；2025 年 10 月期中第 1 題；2023 年 11 月期中第 1 題。
- 三、一階：恰當方程與積分因子——作業一第 4 題、第 5 題（先找積分因子）；2024 年 11 月期中第 1 題；2023 年 11 月期中第 2 題；2022 年 11 月期中第 1 題（非恰當方程與積分因子）；2021 年 11 月期中第 1 題。
- 四、二階齊次常係數——作業二第 1 題（複根、邊界條件）、第 2 題（重根）；2024 年 11 月期中第 3 題（複根）；2022 年 11 月期中第 2 題（純虛根）；2021 年 11 月期中第 3 題（相異實根）。
- 五、降階法——作業二第 3 題（Cauchy–Euler 方程）；2025 年 10 月期中第 2 題（降階法公式證明）。
- 六、二階非齊次：未定係數法與初值問題——作業三第 1 題（sum rule）、第 2 題（multiplication rule）、第 3 題（modification rule）；2025 年 10 月期中第 3 題；2024 年 11 月期中第 4 題（sum rule）；2023 年 11 月期中第 3 題（multiplication rule，三小題）；2022 年 11 月期中第 3 題；2021 年 11 月期中第 4 題（modification rule）。
- 七、冪級數解——作業四第 1、2、3 題。
- 八、Frobenius 法——作業五第 1、2 題。
- 九、Fourier 級數——2025 年 10 月期中第 4 題（實數、複數 Fourier 與功率頻譜）；2023 年 11 月期中第 4 題；2022 年 11 月期中第 4 題（實數、複數 Fourier 與功率頻譜）；2021 年 11 月期中第 5 題（週期二次函數）。

各作業的總符號表放在最相關主題的開頭：作業一放在「一」、作業二放在「四」、作業三放在「六」、作業四放在「七」、作業五放在「八」。

**來源一覽**（原文件的分卷標題）：

- 第一部分：歷屆期中考古題
    - 2025 年 10 月｜應用數學期中考（四大題，含三個 Fourier 小題）
    - 2024 年 11 月｜應用數學期中考（四大題）
    - 2023 年 11 月｜應用數學期中考（四大題；第 3 題有三小題）
    - 2022 年 11 月｜應用數學期中考（四大題；第 4 題有三小題）
    - 2021 年 11 月 9 日｜應用數學期中考（五大題）
- 第二部分：歷次作業
    - 作業一｜First Order ODE：五題詳解
    - 作業二｜二階齊次常微分方程：三題詳解
    - 作業三｜二階線性非齊次 ODE：三題詳解
    - 作業四｜Power Series Solution：三題詳解
    - 作業五｜Frobenius Method：兩題詳解

# 一、一階：可分離變數

## 作業一｜總符號表

| 符號 | 意義與角色 |
|---|---|
| $x$ | 原題的自變數（independent variable）；第 2 題變換後，暫時改作待求函數。 |
| $y=y(x)$ | 原題要找的依變數／未知函數（dependent variable）。 |
| $y'=dy/dx$ | $y$ 對 $x$ 的導數；第 2 題交換變數後，改用 $dx/dy$，兩者不可混寫。 |
| $p(x),g(x)$ | 一階線性標準式中的已知係數、已知右側函數。交換變數後可改依賴 $y$。 |
| $F$ | 積分因子（integrating factor）；在使用區間內須非零，才能保持方程等價。 |
| $M,N$ | 微分形式中分別乘在 $dx,dy$ 前面的函數；每題重新依該題定義。 |
| $f(x,y)$ | 勢函數（potential function）；其偏導數分別等於 $M,N$。小寫 $f$ 不是積分因子 $F$。 |
| $h(y)$ | 對 $x$ 積分後可能留下的、只依賴 $y$ 的未知函數。 |
| $M_y,N_x,f_x,f_y$ | 偏導數的簡寫，例如 $M_y=\partial M/\partial y$；偏微分時另一個座標先固定。 |
| $C,C_1,C_2$ | 積分常數；不同下標表示數值可能已改變，不能在換算後認為仍是同一數字。 |
| $K$ | 第 3 題照片使用的任意常數，與其他題的 $C$ 分開。 |
| $e,\ln,\pi$ | 自然指數的底數、自然對數、圓周率；實數對數的真數須為正。 |

## 作業一第 1 題｜可分離變數

**原題：**（First Order ODE）

$$
xy\cos(y^2)y'+2\sin(y^2)=0,
\qquad y(1)=\sqrt{\frac{\pi}{2}}.
$$

**中文：** 求符合上述方程、並通過指定初始點的解。照片附解為 $x^4\sin(y^2)=1$。

符號：$y(1)=\sqrt{\pi/2}$ 表示 $x=1$ 時 $y=\sqrt{\pi/2}$，即 $y^2=\pi/2$；三角函數用弧度。

**① 分離變數：** 把 $y'$ 換回 $dy/dx$、移項後，含 $y$ 的因子可以集中到一邊，另一邊只剩 $x$。

$$
xy\cos(y^2)\frac{dy}{dx}=-2\sin(y^2).
$$

在 $x\ne0$、$\sin(y^2)\ne0$ 的區域，兩邊除以 $x\sin(y^2)$：

公式（可分離變數）：若方程能寫成 $p(y)\,\dfrac{dy}{dx}=f(x)$，則 $p(y)\,dy=f(x)\,dx$，兩邊分別積分得 $\int p(y)\,dy=\int f(x)\,dx+C$，其中 $x$ 為自變數、$y$ 為待求函數、$p(y)$ 只含 $y$、$f(x)$ 只含 $x$、$C$ 為積分常數；本題 $p(y)=\dfrac{y\cos(y^2)}{\sin(y^2)}$、$f(x)=-\dfrac{2}{x}$。

$$
\frac{y\cos(y^2)}{\sin(y^2)}\,dy
=-\frac{2}{x}\,dx.
\tag{1.1}
$$

**② 左邊換元、右邊直接積分：** 令 $u=\sin(y^2)$，它的微分正好含分子的 $y\cos(y^2)$。

公式（連鎖律）：$\dfrac{d}{dy}f\big(g(y)\big)=f'\big(g(y)\big)\,g'(y)$，即 $d\big[f(g(y))\big]=f'(g(y))\,g'(y)\,dy$，其中 $f$ 為外層函數、$g$ 為內層函數、$f',g'$ 為各自的導數；本題 $f=\sin$、$g(y)=y^2$，故 $f'=\cos$、$g'(y)=2y$。

$$
u=\sin(y^2),
\qquad du=2y\cos(y^2)\,dy.
$$

$du$ 比原分子多一個 $2$，所以要補 $\tfrac12$：

公式（標準積分）：$\int\dfrac{du}{u}=\ln|u|+C$（$u\ne0$），其中 $u$ 為積分變數、$\ln$ 為自然對數、$C$ 為積分常數；本題左邊 $u=\sin(y^2)$，右邊把 $u$ 換成 $x$ 得 $\int\dfrac{dx}{x}=\ln|x|$。

$$
\begin{aligned}
\int\frac{y\cos(y^2)}{\sin(y^2)}\,dy
&=\frac12\int\frac{du}{u}\\
&=\frac12\ln|u|\\
&=\frac12\ln|\sin(y^2)|.
\end{aligned}
$$

右邊對 $x$ 積分：

$$
\int-\frac{2}{x}\,dx=-2\ln|x|.
$$

兩邊的積分常數合成一個 $C_1$：

$$
\frac12\ln|\sin(y^2)|=-2\ln|x|+C_1.
\tag{1.2}
$$

**③ 整理成隱式：** 式（1.2）乘以 $2$、對數項移到左邊，新常數記為 $C_2$：

$$
\ln|\sin(y^2)|+4\ln|x|=C_2.
$$

公式（對數律）：$n\ln|a|=\ln|a|^n$、$\ln|a|+\ln|b|=\ln|ab|$，其中 $a,b$ 為非零實數、$n$ 為實數常數；本題 $n=4$、$a=x$、$b=\sin(y^2)$。

$$
\ln|x^4\sin(y^2)|=C_2.
$$

取指數得 $|x^4\sin(y^2)|=e^{C_2}$，把正負號併入新的帶號常數 $C$（這一族 $C\ne0$）：

$$
x^4\sin(y^2)=C.
\tag{1.3}
$$

**④ 代初值：** $x=1$、$y^2=\pi/2$：

$$
C=1^4\sin\left(\frac{\pi}{2}\right)=1.
$$

$$
\boxed{x^4\sin(y^2)=1.}
\tag{1.4}
$$

**注意：** 給定點代回原方程，$\cos(\pi/2)=0$ 使 $y'$ 項消失，左邊只剩 $2\ne0$，所以原題在 $x=1$ 沒有可微且滿足原式的 $y(x)$；式（1.4）是通過給定點、在該點有垂直切線的積分曲線，實數分支只在 $x>1$ 存在。另外，除以 $\sin(y^2)$ 會漏掉常數解 $y\equiv\pm\sqrt{n\pi}$（$n$ 為非負整數），但它們不符合初值。

## 2024 年 11 月期中第 2 題｜非線性可分離變數（25 分）

**原題：** Solve $y'+y^2=9$ for $y(0)=0$.

**中文：** 解 $y'=9-y^2$ 的一階初值題。

**① 分離變數：** 移項成 $y'=9-y^2$，再除以 $9-y^2$（這會排除平衡解 $y=\pm3$，但它們不符合初值）。

公式（可分離變數）：若方程能寫成 $p(y)\,\dfrac{dy}{dx}=f(x)$，則 $p(y)\,dy=f(x)\,dx$，兩邊分別積分得 $\int p(y)\,dy=\int f(x)\,dx+C$，其中 $x$ 為自變數、$y$ 為待求函數、$p(y)$ 只含 $y$、$f(x)$ 只含 $x$、$C$ 為積分常數；本題 $p(y)=\dfrac{1}{9-y^2}$、$f(x)=1$。

$$
\frac{dy}{9-y^2}=dx=\frac{dy}{(3-y)(3+y)}.
$$

**② 部分分式：** 把左邊拆成兩個一次分母。

公式（部分分式）：$\dfrac{1}{(a-y)(a+y)}=\dfrac{1}{2a}\left(\dfrac{1}{a-y}+\dfrac{1}{a+y}\right)$，其中 $a\ne0$ 為常數、$y\ne\pm a$；本題 $a=3$。

$$
\frac{1}{(3-y)(3+y)}=\frac16\left(\frac1{3-y}+\frac1{3+y}\right).
$$

**③ 兩邊積分：** 注意 $\int dy/(3-y)=-\ln|3-y|$（係數 $c=-1$）。

公式（標準積分）：$\int\dfrac{dy}{b+cy}=\dfrac{1}{c}\ln|b+cy|+C$，其中 $b,c$ 為常數且 $c\ne0$、$y$ 為積分變數、$C$ 為積分常數；本題 $\dfrac{1}{3+y}$ 取 $b=3$、$c=1$，$\dfrac{1}{3-y}$ 取 $b=3$、$c=-1$。

公式（對數律）：$\ln|a|-\ln|b|=\ln\left|\dfrac{a}{b}\right|$，其中 $a,b$ 為非零實數；本題 $a=3+y$、$b=3-y$。

$$
\frac16\big[\ln|3+y|-\ln|3-y|\big]=x+C
\quad\Rightarrow\quad
\frac16\ln\left|\frac{3+y}{3-y}\right|=x+C.
$$

**④ 代初值並解出 $y$：** $y(0)=0$ 給 $C=0$；經過 $y=0$ 的分支上分式為正，絕對值可直接拿掉：

$$
\frac{3+y}{3-y}=e^{6x};\qquad
3+y=3e^{6x}-ye^{6x}.
$$

$$
y(1+e^{6x})=3(e^{6x}-1),
$$

$$
\boxed{y(x)=3\frac{e^{6x}-1}{e^{6x}+1}=3\tanh(3x).}
$$

符號：$\tanh u=\dfrac{e^u-e^{-u}}{e^u+e^{-u}}$（雙曲正切），取 $u=3x$ 即得左邊的分式。特解對所有實數 $x$ 有定義。

## 2021 年 11 月期中第 2 題｜平方速度阻力下自由落體（20 分）

**原題：** An object of mass $m$ falls from rest under gravity subject to an air resistance proportional to the square of its velocity. Taking the $y$-axis as positive down, find $v$ as a function of $t$.

**中文：** 質量為 $m$ 的物體從靜止下落，空氣阻力大小與速度平方成正比；向下為 $y$ 正方向，求速度 $v(t)$。

符號：$m>0$ 質量、$g>0$ 重力加速度、$k>0$ 阻力係數（阻力大小 $kv^2$，向上）、$v=dy/dt$ 向下速度、$t\ge0$ 時間；初值 $v(0)=0$。

**① 列運動方程：** 向下為正，重力 $+mg$、阻力 $-kv^2$。

公式（牛頓第二定律）：$m\dfrac{dv}{dt}=F_{\text{net}}$，其中 $m$ 為質量（kg）、$v$ 為速度（m/s）、$t$ 為時間（s）、$F_{\text{net}}$ 為沿正方向的合力（N）；本題向下為正，重力為 $+mg$、阻力為 $-kv^2$（$v\ge0$ 時向上），故 $F_{\text{net}}=mg-kv^2$。

$$
m\frac{dv}{dt}=mg-kv^2
\Rightarrow
\frac{dv}{dt}=g-\frac{k}{m}v^2.
$$

**② 引入終端速度：** 定義 $v_T=\sqrt{mg/k}$，使 $(k/m)v_T^2=g$：

$$
\frac{dv}{dt}=g\left(1-\frac{v^2}{v_T^2}\right),
$$

**③ 分離變數並換元：**

公式（可分離變數）：若方程能寫成 $p(y)\,\dfrac{dy}{dx}=f(x)$，則 $p(y)\,dy=f(x)\,dx$，兩邊分別積分得 $\int p(y)\,dy=\int f(x)\,dx+C$，其中 $x$ 為自變數、$y$ 為待求函數、$p(y)$ 只含 $y$、$f(x)$ 只含 $x$、$C$ 為積分常數；本題自變數為 $t$、待求函數為 $v$，$p(v)=\dfrac{1}{1-(v/v_T)^2}$、$f(t)=g$。

$$
\frac{dv}{1-(v/v_T)^2}=g\,dt.
$$

令 $u=v/v_T$（$dv=v_Tdu$）：

$$
v_T\int\frac{du}{1-u^2}=gt+C.
$$

**④ 積分：** 從 $u(0)=0$ 起有 $0\le u<1$，所以 $\int du/(1-u^2)=\operatorname{artanh}(u)$：

$$
v_T\operatorname{artanh}\left(\frac{v}{v_T}\right)=gt+C.
$$

符號：$\operatorname{artanh}u=\frac12\ln\frac{1+u}{1-u}$（$|u|<1$），是 $\tanh z=\dfrac{e^z-e^{-z}}{e^z+e^{-z}}$ 的反函數。

**⑤ 代初值：** $v(0)=0$ 給 $C=0$，兩邊取雙曲正切：

$$
\frac{v}{v_T}=\tanh\left(\frac{gt}{v_T}\right).
$$

$$
\boxed{v(t)=\sqrt{\frac{mg}{k}}\,\tanh\left(\sqrt{\frac{gk}{m}}\,t\right),\quad t\ge0.}
$$

# 二、一階：線性方程與積分因子

## 作業一第 2 題｜先交換變數，再用線性積分因子

**原題：**

$$
y'=\frac{1}{e^y-x},\qquad y(1)=0.
$$

**中文：** 求滿足上述微分方程及給定初始條件的解。照片附解為：

$$
xe^y=\frac12e^{2y}+\frac12.
$$

**① 交換變數，改求 $x(y)$：** 以 $y(x)$ 看，原式含 $e^y$，不是線性；但把 $x$ 看成 $y$ 的函數，$x$ 與 $dx/dy$ 都只出現一次。在 $e^y-x\ne0$ 處取倒數：

公式（反函數導數）：若 $y=y(x)$ 在某處 $\dfrac{dy}{dx}\ne0$，則局部可反解為 $x=x(y)$，且 $\dfrac{dx}{dy}=\dfrac{1}{dy/dx}$，其中 $x,y$ 為互相決定的兩個變數；本題 $\dfrac{dy}{dx}=\dfrac{1}{e^y-x}$，故 $\dfrac{dx}{dy}=e^y-x$。

$$
\frac{dx}{dy}=e^y-x.
$$

移項得到以 $y$ 為自變數的線性標準式：

$$
\boxed{\frac{dx}{dy}+x=e^y.}
\tag{2.1}
$$

**② 求積分因子（對 $y$ 積分）：** 式（2.1）中 $x$ 的係數是 $1$。

公式（積分因子）：一階線性方程 $y'+p(x)y=g(x)$ 的積分因子為 $F(x)=e^{\int p(x)\,dx}$，乘上後左邊成為 $\dfrac{d}{dx}\big[F(x)y\big]$，故 $F(x)y=\int F(x)g(x)\,dx+C$，其中 $x$ 為自變數、$y$ 為待求函數、$p(x),g(x)$ 為已知函數、$C$ 為積分常數；本題自變數改為 $y$、待求函數改為 $x$，$p=1$、$g=e^y$。

$$
F(y)=e^{\int1\,dy}=e^y.
\tag{2.2}
$$

乘上積分因子：

$$
e^y\frac{dx}{dy}+e^yx=e^{2y}.
$$

**③ 左邊合成乘積微分：**

公式（乘積律）：$\dfrac{d}{dy}\big[u(y)v(y)\big]=u'(y)v(y)+u(y)v'(y)$，其中 $u,v$ 為可微函數、$'$ 表示對 $y$ 的導數；本題 $u=x(y)$、$v=e^y$。

$$
\frac{d}{dy}(xe^y)
=e^y\frac{dx}{dy}+x\frac{d(e^y)}{dy}
=e^y\frac{dx}{dy}+xe^y.
$$

所以：

$$
\frac{d}{dy}(xe^y)=e^{2y}.
\tag{2.3}
$$

**④ 對 $y$ 積分：**

$$
xe^y=\int e^{2y}\,dy+C.
$$

公式（標準積分）：$\int e^{ay}\,dy=\dfrac{1}{a}e^{ay}+C$，其中 $a\ne0$ 為常數、$y$ 為積分變數、$C$ 為積分常數；本題 $a=2$。

$$
xe^y=\frac12e^{2y}+C.
$$

**⑤ 代初值 $(x,y)=(1,0)$：**

$$
1\cdot e^0=\frac12e^0+C,
\qquad C=\frac12.
$$

$$
\boxed{xe^y=\frac12e^{2y}+\frac12.}
\tag{2.4}
$$

**注意：** 原題分母在 $(1,0)$ 為 $e^0-1=0$，右側無定義，所以原題不存在包含 $x=1$ 的通常可微初值解。式（2.4）除以 $e^y$ 得 $x=\dfrac{e^y+e^{-y}}2$，在 $y=0$ 處 $dx/dy=0$，無法反解成有限導數的 $y(x)$；對原題只能在 $x>1$ 的兩個分支上當解。令 $t=e^y>0$，由 $t^2-2xt+1=0$ 解出分支：

公式（二次公式）：$at^2+bt+c=0$（$a\ne0$）的根為 $t=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$，其中 $a,b,c$ 為係數、$t$ 為未知數；本題 $a=1$、$b=-2x$、$c=1$。

得 $t=x\pm\sqrt{x^2-1}$，兩個分支為 $y_\pm(x)=\ln\left(x\pm\sqrt{x^2-1}\right)$（$x>1$）。

## 作業一第 3 題｜線性方程的積分因子

**原題：**

$$
xy'+(1+x)y=e^{-x}\sin(2x).
$$

**中文：** 求上述微分方程的通解（沒有初始條件，$K$ 不能擅自決定）。照片附解（K is constant：$K$ 是任意常數）：

$$
y=-\frac{e^{-x}}{2x}\cos(2x)+K\frac{e^{-x}}{x}.
$$

**① 化成標準式：** $y$、$y'$ 都是一次、係數只依賴 $x$，是線性方程。在不跨過 $x=0$ 的區間除以 $x$，讓 $y'$ 的係數變成 $1$：

公式（一階線性標準式）：$y'+p(x)y=g(x)$，其中 $x$ 為自變數、$y$ 為待求函數、$p(x)$ 為 $y$ 的係數、$g(x)$ 為右側已知函數，且 $y'$ 的係數必須是 $1$；本題除以 $x$ 後 $p(x)=1+\dfrac1x$、$g(x)=\dfrac{e^{-x}\sin(2x)}{x}$。

$$
y'+\left(1+\frac1x\right)y
=\frac{e^{-x}\sin(2x)}x.
\tag{3.1}
$$

$$
p(x)=1+\frac1x,
\qquad g(x)=\frac{e^{-x}\sin(2x)}x.
$$

**② 求積分因子：**

公式（標準積分）：$\int\dfrac{dx}{x}=\ln|x|+C$（$x\ne0$），其中 $x$ 為積分變數、$C$ 為積分常數；本題用於 $\int\left(1+\dfrac1x\right)dx=x+\ln|x|$，常數可省略（只改變 $F$ 的非零倍數）。

公式（指數律）：$e^{a+b}=e^ae^b$、$e^{\ln u}=u$（$u\gt0$），其中 $a,b$ 為實數、$u$ 為正數；本題 $a=x$、$b=\ln|x|$、$u=|x|$。

$$
\begin{aligned}
F(x)
&=e^{\int p(x)\,dx}\\
&=e^{\int(1+1/x)\,dx}\\
&=e^{x+\ln|x|}\\
&=|x|e^x.
\end{aligned}
$$

在固定 $x>0$ 或 $x<0$ 的區間，$|x|$ 與 $x$ 只差非零常數倍，不影響解法，所以取：

$$
\boxed{F(x)=xe^x.}
\tag{3.2}
$$

**③ 乘上積分因子，辨認乘積微分：** 式（3.1）乘上式（3.2）：

$$
xe^xy'+(x+1)e^xy=\sin(2x).
$$

左側正是 $xe^xy$ 的導數：

公式（乘積律）：$\dfrac{d}{dx}\big[u(x)v(x)\big]=u'(x)v(x)+u(x)v'(x)$，其中 $u,v$ 為可微函數、$'$ 表示對 $x$ 的導數；本題先取 $u=xe^x$、$v=y$，再對 $(xe^x)'$ 取 $u=x$、$v=e^x$。

$$
\begin{aligned}
\frac{d}{dx}(xe^xy)
&=xe^xy'+(xe^x)'y\\
&=xe^xy'+(e^x+xe^x)y\\
&=xe^xy'+(x+1)e^xy.
\end{aligned}
$$

因此：

$$
\frac{d}{dx}(xe^xy)=\sin(2x).
\tag{3.3}
$$

**④ 積分並解出 $y$：**

$$
xe^xy=\int\sin(2x)\,dx+K.
$$

公式（標準積分）：$\int\sin(ax)\,dx=-\dfrac{1}{a}\cos(ax)+C$，其中 $a\ne0$ 為常數、$x$ 為積分變數、$C$ 為積分常數；本題 $a=2$。

$$
\int\sin(2x)\,dx=-\frac12\cos(2x).
$$

$$
xe^xy=-\frac12\cos(2x)+K.
$$

除以 $xe^x$：

$$
\boxed{
 y=-\frac{e^{-x}}{2x}\cos(2x)
 +K\frac{e^{-x}}x,
 \qquad x\ne0.
}
\tag{3.4}
$$

$K$ 在每個連通求解區間內是常數。

**注意：** 原式在 $x=0$ 只要求 $y(0)=0$。取 $K=1/2$ 時解為 $y=e^{-x}\sin^2x/x$，再令 $y(0)=0$，可光滑延伸過 $x=0$（且 $y'(0)=1$）；其餘 $K$ 在 $x\to0$ 發散。

## 2025 年 10 月期中第 1 題｜一階線性方程（25 分）

**原題：** Solve $(x^2-x-2)y'+3xy=x^2-4x+4$ for $y(1)=1$.

**中文：** 解一階 ODE，求通過 $(1,1)$ 的解。

**① 化成標準式：** 因式分解 $x^2-x-2=(x-2)(x+1)$、$x^2-4x+4=(x-2)^2$：

$$
(x-2)(x+1)y'+3xy=(x-2)^2.
$$

在包含 $x=1$、不跨過奇異點 $x=-1,2$ 的區間 $(-1,2)$，除以 $(x-2)(x+1)$：

$$
y'+\frac{3x}{(x-2)(x+1)}y=\frac{x-2}{x+1}.
$$

符號：$P(x)=\dfrac{3x}{(x-2)(x+1)}$、$Q(x)=\dfrac{x-2}{x+1}$ 為標準式 $y'+P(x)y=Q(x)$ 的係數與右側；$A,B$ 為部分分式待定常數。

**② 部分分式拆 $P$：** 設 $3x/[(x-2)(x+1)]=A/(x-2)+B/(x+1)$，由 $A+B=3$、$A-2B=0$ 得 $A=2,B=1$：

$$
P(x)=\frac2{x-2}+\frac1{x+1}.
$$

**③ 求積分因子：** $F(x)=\exp(\int P(x)dx)$，在 $(-1,2)$ 上取非零且方便的形式。

公式（標準積分）：$\int\dfrac{dx}{x-c}=\ln|x-c|+C$，其中 $c$ 為常數、$x\ne c$、$C$ 為積分常數；本題 $c=2$ 與 $c=-1$，在區間 $(-1,2)$ 上 $x+1\gt0$，故 $|x+1|=x+1$。

公式（指數律）：$e^{a+b}=e^ae^b$、$e^{n\ln u}=u^n$（$u\gt0$），其中 $a,b,n$ 為實數、$u$ 為正數；本題 $e^{2\ln|x-2|}=|x-2|^2=(x-2)^2$、$e^{\ln(x+1)}=x+1$。

$$
F(x)=e^{2\ln|x-2|+\ln(x+1)}=(x-2)^2(x+1).
$$

**④ 乘上 $F$，左邊合成 $(Fy)'$：**

公式（乘積律）：$\dfrac{d}{dx}\big[F(x)y\big]=F(x)y'+F'(x)y$，而 $F=e^{\int P\,dx}$ 滿足 $F'(x)=P(x)F(x)$，故 $F(y'+Py)=(Fy)'$，其中 $F$ 為積分因子、$P$ 為標準式中 $y$ 的係數、$y$ 為待求函數；本題 $F=(x-2)^2(x+1)$，右側 $FQ=(x-2)^2(x+1)\cdot\dfrac{x-2}{x+1}=(x-2)^3$。

$$
\frac{d}{dx}\big[(x-2)^2(x+1)y\big]=(x-2)^3.
$$

**⑤ 積分：** 右側令 $u=x-2$（$du=dx$）。

公式（冪次積分）：$\int u^n\,du=\dfrac{u^{n+1}}{n+1}+C$（$n\ne-1$），其中 $u$ 為積分變數、$n$ 為常數指數、$C$ 為積分常數；本題 $u=x-2$、$n=3$。

$$
(x-2)^2(x+1)y=\int(x-2)^3dx=\frac{(x-2)^4}{4}+C.
$$

**⑥ 代初值 $(1,1)$：** 左側 $(-1)^2(2)=2$，右側 $1/4+C$，故 $C=7/4$。

$$
\boxed{y(x)=\frac{(x-2)^4+7}{4(x-2)^2(x+1)},\quad -1<x<2.}
$$

## 2023 年 11 月期中第 1 題｜一階線性初值方程（6 分）

**原題：** Solve $dy+(2xy-xe^{-x^2})dx=0$ for $y(0)=1$.

**中文：** 解 $y'+2xy=xe^{-x^2}$，求通過 $(0,1)$ 的解（指數是 $e^{-x^2}$，不是 $e^{-x}$）。

**① 求積分因子：** 除以 $dx$ 後已是標準式，$P(x)=2x$、$Q(x)=xe^{-x^2}$。

公式（積分因子）：$y'+P(x)y=Q(x)$ 的積分因子為 $F(x)=e^{\int P(x)\,dx}$，乘上後 $\big(F(x)y\big)'=F(x)Q(x)$，其中 $x$ 為自變數、$y$ 為待求函數、$P(x),Q(x)$ 為已知函數；本題 $P(x)=2x$、$Q(x)=xe^{-x^2}$。

公式（冪次積分）：$\int x^n\,dx=\dfrac{x^{n+1}}{n+1}+C$（$n\ne-1$），其中 $x$ 為積分變數、$n$ 為常數指數、$C$ 為積分常數；本題 $\int2x\,dx=x^2$（$n=1$，常數併入 $F$ 的倍數）與 $\int x\,dx=\dfrac{x^2}{2}+C$。

$$
F(x)=e^{\int2x\,dx}=e^{x^2}.
$$

**② 乘上 $F$ 並積分：**

$$
(e^{x^2}y)'=e^{x^2}(xe^{-x^2})=x.
$$

積分得 $e^{x^2}y=\int xdx=x^2/2+C$。

**③ 代初值：** $y(0)=1$ 給 $C=1$：

$$
\boxed{y(x)=e^{-x^2}\left(1+\frac{x^2}{2}\right).}
$$

# 三、一階：恰當方程與積分因子

## 作業一第 4 題｜恰當方程

**原題：**

$$
(2y+e^y+6x^2)y'+4+12xy=0
\quad\text{with }y(0)=0.
$$

**中文：** 求上述微分方程的解，且解曲線須通過 $(0,0)$。照片附解為 $4x+6x^2y+y^2+e^y=1$。

**① 寫成 $M\,dx+N\,dy=0$：** 含 $e^y$ 不是線性，改寫成微分形式。$y'$ 前面的係數乘 $dx$ 後成為 $dy$ 項，所以對應 $N$。

$$
(4+12xy)\,dx+(2y+e^y+6x^2)\,dy=0.
\tag{4.1}
$$

$$
M=4+12xy,
\qquad N=2y+e^y+6x^2.
$$

**② 檢查恰當條件：** 求 $M_y$ 時 $x$ 當常數，求 $N_x$ 時 $y$ 當常數。

公式（恰當條件）：$M(x,y)\,dx+N(x,y)\,dy=0$ 在偏導數連續的單連通區域內為恰當方程的充要條件是 $M_y=N_x$，此時存在勢函數 $f(x,y)$ 使 $f_x=M$、$f_y=N$，解曲線為 $f(x,y)=C$，其中 $M,N$ 為 $dx,dy$ 的係數、$M_y=\partial M/\partial y$、$N_x=\partial N/\partial x$、$C$ 為常數；本題 $M=4+12xy$、$N=2y+e^y+6x^2$。

$$
M_y=12x,
\qquad N_x=12x.
\tag{4.2}
$$

兩者相等，且係數在整個平面連續，所以存在勢函數 $f$，原式即 $df=0$。

**③ 由 $f_x=M$ 對 $x$ 積分：** $y$ 當常數，積分「常數」要寫成只依賴 $y$ 的 $h(y)$。

$$
f_x=4+12xy.
$$

公式（冪次積分）：$\int x^n\,dx=\dfrac{x^{n+1}}{n+1}+C$（$n\ne-1$），其中 $x$ 為積分變數、$n$ 為常數指數、$C$ 為積分常數（對 $x$ 偏積分時改為只依賴 $y$ 的 $h(y)$）；本題 $\int4\,dx=4x$（$n=0$）、$\int12xy\,dx=12y\dfrac{x^2}{2}$（$n=1$，$y$ 視為常數）。

$$
\begin{aligned}
f(x,y)
&=\int(4+12xy)\,dx+h(y)\\
&=4x+12y\frac{x^2}{2}+h(y)\\
&=4x+6x^2y+h(y).
\end{aligned}
\tag{4.3}
$$

**④ 用 $f_y=N$ 決定 $h(y)$：** 式（4.3）對 $y$ 偏微分：

$$
f_y=6x^2+h'(y).
$$

令它等於 $N$：

$$
6x^2+h'(y)=2y+e^y+6x^2.
$$

消去 $6x^2$：

$$
h'(y)=2y+e^y.
$$

公式（標準積分）：$\int e^{ay}\,dy=\dfrac{1}{a}e^{ay}+C$（$a\ne0$），其中 $a$ 為常數、$y$ 為積分變數、$C$ 為積分常數；本題 $a=1$，另一項 $\int2y\,dy=y^2$ 用前面的冪次積分。

$$
h(y)=y^2+e^y.
$$

（加法常數併入最後的總常數。）

$$
f(x,y)=4x+6x^2y+y^2+e^y.
\tag{4.4}
$$

**⑤ 寫成 $f=C$ 並代初值：**

$$
4x+6x^2y+y^2+e^y=C.
$$

代 $(0,0)$：

$$
C=4(0)+6(0)^2(0)+(0)^2+e^0=1.
$$

$$
\boxed{4x+6x^2y+y^2+e^y=1.}
\tag{4.5}
$$

**注意：** $N(0,0)=1\ne0$，初值附近有可微分支；往外延伸時須檢查 $N$ 是否變成零。

## 作業一第 5 題｜先找 $F(y)$，再化成恰當方程

**原題：**

$$
\cos y\,dx-2(x-y)\sin y\,dy-\cos y\,dy=0
\quad\text{with }y(1)=0.
$$

**中文：** 求上述微分方程的解，且解曲線須通過 $(1,0)$。照片附解為 $(x-y)\cos^2y=1$。

**① 合併 $dy$ 項，辨認 $M,N$：**

$$
\underbrace{\cos y}_{M}\,dx
+\underbrace{\big[-2(x-y)\sin y-\cos y\big]}_{N}\,dy=0.
\tag{5.1}
$$

**② 檢查恰當條件：**

公式（恰當條件）：$M(x,y)\,dx+N(x,y)\,dy=0$ 在偏導數連續的單連通區域內為恰當方程的充要條件是 $M_y=N_x$，此時存在勢函數 $f(x,y)$ 使 $f_x=M$、$f_y=N$，解曲線為 $f(x,y)=C$，其中 $M,N$ 為 $dx,dy$ 的係數、$M_y=\partial M/\partial y$、$N_x=\partial N/\partial x$、$C$ 為常數；本題 $M=\cos y$、$N=-2(x-y)\sin y-\cos y$；若 $M_y\ne N_x$ 就不是恰當方程。

$$
M_y=-\sin y,
\qquad N_x=-2\sin y.
$$

兩者不恆等，原式不是恰當方程（只在 $y=0$ 一點相等不夠）。

**③ 算偏導數差，選只依賴 $y$ 的積分因子：** $\Delta$ 表示 $M_y-N_x$。

$$
\Delta=M_y-N_x
=(-\sin y)-(-2\sin y)=\sin y.
\tag{5.2}
$$

只依賴 $y$ 的積分因子用 $-\Delta/M$：

$$
-\frac{\Delta}{M}=-\frac{\sin y}{\cos y}.
\tag{5.3}
$$

它只含 $y$，所以可找 $F(y)$。負號的來源：要求 $FM,FN$ 恰當，

$$
\frac{\partial(FM)}{\partial y}
=\frac{\partial(FN)}{\partial x}.
$$

$F$ 只依賴 $y$，左邊多出 $F'(y)M$：

$$
F'M+FM_y=FN_x.
$$

在 $F\ne0$、$M\ne0$ 處除以 $FM$：

$$
\frac{F'}F=\frac{N_x-M_y}{M}=-\frac{\Delta}{M}.
$$

**④ 求積分因子：**

公式（單變數積分因子）：若 $-\dfrac{\Delta}{M}=\dfrac{N_x-M_y}{M}$ 只含 $y$，則 $F(y)=e^{\int(-\Delta/M)\,dy}$ 使 $FM\,dx+FN\,dy=0$ 成為恰當方程，其中 $\Delta=M_y-N_x$、$M,N$ 為 $dx,dy$ 的係數、$F$ 須在使用區域內非零；本題 $-\dfrac{\Delta}{M}=-\dfrac{\sin y}{\cos y}$。

$$
F(y)=e^{\int-\frac{\sin y}{\cos y}\,dy}.
$$

分子是分母的導數：

公式（標準積分）：$\int\dfrac{u'(y)}{u(y)}\,dy=\ln|u(y)|+C$（$u\ne0$），其中 $u$ 為可微函數、$u'$ 為其對 $y$ 的導數、$C$ 為積分常數；本題 $u=\cos y$、$u'=-\sin y$。

$$
\int-\frac{\sin y}{\cos y}\,dy=\ln|\cos y|.
$$

得 $F(y)=|\cos y|$。從 $y=0$ 出發取 $-\pi/2<y<\pi/2$，此區間 $\cos y>0$，所以：

$$
\boxed{F(y)=\cos y.}
\tag{5.4}
$$

**⑤ 整個方程乘上 $\cos y$，再檢查恰當：** $\widetilde M,\widetilde N$ 為新係數。

$$
\cos^2y\,dx
+\big[-2(x-y)\sin y\cos y-\cos^2y\big]\,dy=0.
\tag{5.5}
$$

$$
\widetilde M=\cos^2y,
\qquad
\widetilde N=-2(x-y)\sin y\cos y-\cos^2y.
$$

公式（連鎖律）：$\dfrac{d}{dy}f\big(u(y)\big)=f'(u)\,u'(y)$，其中 $f$ 為外層函數、$u$ 為內層函數；本題 $f(u)=u^2$、$u=\cos y$，得 $\dfrac{d}{dy}\cos^2y=-2\sin y\cos y$。

$$
\widetilde M_y=-2\sin y\cos y,
\qquad
\widetilde N_x=-2\sin y\cos y.
$$

相等，已成恰當方程。

**⑥ 由 $f_x=\widetilde M$ 對 $x$ 積分：** $\cos^2y$ 視為常數。

$$
f(x,y)=\int\cos^2y\,dx+h(y)
=x\cos^2y+h(y).
\tag{5.6}
$$

對 $y$ 偏微分：

$$
f_y=-2x\sin y\cos y+h'(y).
$$

令它等於 $\widetilde N$（先把 $x-y$ 展開）：

$$
-2x\sin y\cos y+h'(y)
=-2x\sin y\cos y
+2y\sin y\cos y-\cos^2y.
$$

消去 $-2x\sin y\cos y$：

$$
h'(y)=2y\sin y\cos y-\cos^2y.
\tag{5.7}
$$

**⑦ 用乘積律反向辨認 $h(y)$：** 式（5.7）正好是 $-y\cos^2y$ 的導數。

公式（乘積律）：$\dfrac{d}{dy}\big[u(y)v(y)\big]=u'(y)v(y)+u(y)v'(y)$，其中 $u,v$ 為可微函數、$'$ 表示對 $y$ 的導數；本題 $u=-y$、$v=\cos^2y$。

$$
\begin{aligned}
\frac{d}{dy}(-y\cos^2y)
&=(-1)\cos^2y+(-y)\frac{d(\cos^2y)}{dy}\\
&=-\cos^2y+(-y)(-2\sin y\cos y)\\
&=-\cos^2y+2y\sin y\cos y.
\end{aligned}
$$

所以：

$$
h(y)=-y\cos^2y.
$$

代回式（5.6）：

$$
f(x,y)=x\cos^2y-y\cos^2y=(x-y)\cos^2y.
\tag{5.8}
$$

**⑧ 寫成 $f=C$ 並代初值 $(1,0)$：**

$$
(x-y)\cos^2y=C.
$$

$$
C=(1-0)\cos^2(0)=1.
$$

$$
\boxed{(x-y)\cos^2y=1.}
\tag{5.9}
$$

**注意：** 初始斜率 $y'(1)=1$ 有限、積分因子在該點非零，初值附近有合法分支；沿曲線走到 $dx/dy=1+2\sin y/\cos^3y=0$ 處會出現垂直切線，不能把整條曲線當成單一的 $y(x)$。

## 2024 年 11 月期中第 1 題｜恰當方程（25 分）

**原題：** Solve $(e^{2y}-y\cos(xy))dx+(2xe^{2y}-x\cos(xy)+2y)dy=0$ for $x=0$ and $y=2$.

**中文：** 解此一階微分形式，找通過 $(0,2)$ 的積分曲線。$\cos xy$ 按 $\cos(xy)$ 讀取。

**① 辨認 $M,N$：**

$$
M=e^{2y}-y\cos(xy),\quad N=2xe^{2y}-x\cos(xy)+2y.
$$

**② 檢查恰當條件：**

公式（恰當條件）：$M(x,y)\,dx+N(x,y)\,dy=0$ 在偏導數連續的單連通區域內為恰當方程的充要條件是 $M_y=N_x$，此時存在勢函數 $f(x,y)$ 使 $f_x=M$、$f_y=N$，解曲線為 $f(x,y)=C$，其中 $M,N$ 為 $dx,dy$ 的係數、$M_y=\partial M/\partial y$、$N_x=\partial N/\partial x$、$C$ 為常數；本題 $M=e^{2y}-y\cos(xy)$、$N=2xe^{2y}-x\cos(xy)+2y$。

公式（乘積律）：$\dfrac{\partial}{\partial y}\big[u\,v\big]=u_y\,v+u\,v_y$，其中 $u,v$ 為 $x,y$ 的可微函數、下標 $y$ 表示對 $y$ 偏微分（對 $x$ 時同理）；本題 $M$ 中的 $y\cos(xy)$ 取 $u=y$、$v=\cos(xy)$，$N$ 中的 $x\cos(xy)$ 對 $x$ 偏微分時取 $u=x$、$v=\cos(xy)$。

公式（連鎖律）：$\dfrac{\partial}{\partial y}f\big(g(x,y)\big)=f'(g)\,g_y$，其中 $f$ 為外層函數、$g$ 為內層函數、$g_y=\partial g/\partial y$（對 $x$ 時換成 $g_x$）；本題 $\dfrac{\partial}{\partial y}e^{2y}=2e^{2y}$、$\dfrac{\partial}{\partial y}\cos(xy)=-x\sin(xy)$、$\dfrac{\partial}{\partial x}\cos(xy)=-y\sin(xy)$。

$$
M_y=2e^{2y}-\cos(xy)+xy\sin(xy),
$$

$$
N_x=2e^{2y}-\cos(xy)+xy\sin(xy).
$$

兩式相等，是恰當方程。

**③ 由 $f_x=M$ 對 $x$ 積分：** $y$ 當常數；第二項令 $u=xy$、$du=y\,dx$。

公式（標準積分）：$\int\cos(ax)\,dx=\dfrac{1}{a}\sin(ax)+C$（$a\ne0$），其中 $a$ 為不含 $x$ 的常數、$C$ 為積分常數（對 $x$ 偏積分時改為 $h(y)$）；本題 $a=y$，故 $\int y\cos(xy)\,dx=\sin(xy)$，另 $\int e^{2y}\,dx=xe^{2y}$（$e^{2y}$ 視為常數）。

$$
f(x,y)=\int[e^{2y}-y\cos(xy)]dx+h(y)=xe^{2y}-\sin(xy)+h(y).
$$

**④ 用 $f_y=N$ 決定 $h(y)$：**

$$
f_y=2xe^{2y}-x\cos(xy)+h'(y)=2xe^{2y}-x\cos(xy)+2y,
$$

所以 $h'(y)=2y$、$h(y)=y^2$，沿解曲線：

$$
xe^{2y}-\sin(xy)+y^2=C.
$$

**⑤ 代初值 $(0,2)$：** $C=0-0+4=4$。

$$
\boxed{xe^{2y}-\sin(xy)+y^2=4.}
$$

## 2023 年 11 月期中第 2 題｜恰當方程（6 分）

**原題：** Solve $(2xe^{3y}+e^x)dx+(3x^2e^{3y}-y^2)dy=0$ for $y(0)=1$.

**中文：** 求通過 $(0,1)$ 的恰當方程解曲線。

**① 檢查恰當條件：** $M=2xe^{3y}+e^x$、$N=3x^2e^{3y}-y^2$。

公式（恰當條件）：$M(x,y)\,dx+N(x,y)\,dy=0$ 在偏導數連續的單連通區域內為恰當方程的充要條件是 $M_y=N_x$，此時存在勢函數 $f(x,y)$ 使 $f_x=M$、$f_y=N$，解曲線為 $f(x,y)=C$，其中 $M,N$ 為 $dx,dy$ 的係數、$M_y=\partial M/\partial y$、$N_x=\partial N/\partial x$、$C$ 為常數；本題 $M=2xe^{3y}+e^x$、$N=3x^2e^{3y}-y^2$。

$$
M_y=6xe^{3y}=N_x.
$$

所以是恰當方程（exact）。

**② 由 $f_x=M$ 對 $x$ 積分：**

公式（標準積分）：$\int x^n\,dx=\dfrac{x^{n+1}}{n+1}+C$（$n\ne-1$）、$\int e^x\,dx=e^x+C$，其中 $x$ 為積分變數、$n$ 為常數指數、$C$ 為積分常數（對 $x$ 偏積分時改為 $h(y)$）；本題 $\int2xe^{3y}\,dx=x^2e^{3y}$（$n=1$，$e^{3y}$ 視為常數），後面 $\int-y^2\,dy=-\dfrac{y^3}{3}$ 也用冪次公式（$n=2$）。

$$
f(x,y)=\int Mdx=x^2e^{3y}+e^x+h(y).
$$

**③ 用 $f_y=N$ 決定 $h(y)$：**

$$
f_y=3x^2e^{3y}+h'(y)=3x^2e^{3y}-y^2
\Rightarrow h'(y)=-y^2.
$$

$$h(y)=-y^3/3.$$

故 $f=x^2e^{3y}+e^x-y^3/3=C$。

**④ 代初值 $(0,1)$：**

$$
C=0+1-\frac13=\frac23.
$$

$$
\boxed{x^2e^{3y}+e^x-\frac{y^3}{3}=\frac23.}
$$

## 2022 年 11 月期中第 1 題｜非恰當方程與積分因子（5 分）

**原題：** Solve $(y^2+xy^3)dx+(5y^2-xy+y^3\sin y)dy=0$ for $y(0)=\pi/2$.

**中文：** 找此微分形式在 $x=0,y=\pi/2$ 附近的解。

**① 辨認 $M,N$：**

$$
M=y^2+xy^3=y^2(1+xy),\quad N=5y^2-xy+y^3\sin y.
$$

**② 檢查恰當條件：**

公式（恰當條件）：$M(x,y)\,dx+N(x,y)\,dy=0$ 在偏導數連續的單連通區域內為恰當方程的充要條件是 $M_y=N_x$，此時存在勢函數 $f(x,y)$ 使 $f_x=M$、$f_y=N$，解曲線為 $f(x,y)=C$，其中 $M,N$ 為 $dx,dy$ 的係數、$M_y=\partial M/\partial y$、$N_x=\partial N/\partial x$、$C$ 為常數；本題 $M=y^2+xy^3$、$N=5y^2-xy+y^3\sin y$。

$$
M_y=2y+3xy^2,\qquad N_x=-y.
$$

$M_y\neq N_x$，原式非恰當。

**③ 找只依賴 $y$ 的積分因子 $F(y)$：**

公式（單變數積分因子）：若 $\dfrac{N_x-M_y}{M}$ 只含 $y$，則 $F(y)=\exp\left(\int\dfrac{N_x-M_y}{M}\,dy\right)$ 使 $FM\,dx+FN\,dy=0$ 成為恰當方程，其中 $M,N$ 為 $dx,dy$ 的係數、$M_y,N_x$ 為偏導數、$F$ 須在使用區域內非零；本題 $M=y^2(1+xy)$、$N_x-M_y=-y-(2y+3xy^2)$。

$$
\frac{N_x-M_y}{M}
=\frac{-y-(2y+3xy^2)}{y^2(1+xy)}
=\frac{-3y(1+xy)}{y^2(1+xy)}
=-\frac3y.
$$

結果只含 $y$：

公式（標準積分）：$\int\dfrac{dy}{y}=\ln|y|+C$（$y\ne0$），其中 $y$ 為積分變數、$C$ 為積分常數；本題 $\int-\dfrac{3}{y}\,dy=-3\ln|y|$。

公式（指數律）：$e^{n\ln u}=u^n$（$u\gt0$），其中 $n$ 為實數、$u$ 為正數；本題 $n=-3$、$u=|y|$。

$$
F(y)=\exp\left(\int -\frac3y\,dy\right)=e^{-3\ln|y|}=|y|^{-3}.
$$

初值 $y(0)=\pi/2>0$，附近取 $F(y)=y^{-3}$（只在 $y\neq0$ 合法，初值附近不會碰到）。

**④ 乘上 $F$，再檢查恰當：**

$$
\left(\frac1y+x\right)dx+\left(\frac5y-\frac{x}{y^2}+\sin y\right)dy=0.
$$

新係數 $\widetilde M=1/y+x$、$\widetilde N=5/y-x/y^2+\sin y$：

$$
\widetilde M_y=-\frac1{y^2}=\widetilde N_x.
$$

**⑤ 由 $f_x=\widetilde M$ 對 $x$ 積分：** $y$ 當常數。

公式（冪次積分）：$\int x^n\,dx=\dfrac{x^{n+1}}{n+1}+C$（$n\ne-1$），其中 $x$ 為積分變數、$n$ 為常數指數、$C$ 為積分常數（對 $x$ 偏積分時改為只依賴 $y$ 的 $h(y)$）；本題 $\int\dfrac1y\,dx=\dfrac{x}{y}$（$n=0$，$\dfrac1y$ 視為常數）、$\int x\,dx=\dfrac{x^2}{2}$（$n=1$）。

$$
f=\int\left(\frac1y+x\right)dx=\frac{x}{y}+\frac{x^2}2+h(y).
$$

**⑥ 用 $f_y=\widetilde N$ 決定 $h(y)$：**

$$
f_y=-\frac{x}{y^2}+h'(y)=\frac5y-\frac{x}{y^2}+\sin y,
$$

公式（標準積分）：$\int\sin y\,dy=-\cos y+C$，其中 $y$ 為積分變數、$C$ 為積分常數；本題用於 $h(y)$ 的第二項，第一項 $\int\dfrac5y\,dy=5\ln|y|=5\ln y$（$y\gt0$）用前面的 $\int dy/y$。

$$
h'(y)=\frac5y+\sin y,
\quad h(y)=5\ln y-\cos y.
$$

**⑦ 代初值 $(0,\pi/2)$：** $f=x/y+x^2/2+5\ln y-\cos y=C$，代入得 $C=5\ln(\pi/2)$。

$$
\boxed{\frac{x}{y}+\frac{x^2}{2}+5\ln y-\cos y=5\ln\frac\pi2,\quad y>0\text{ 的初值分支}.}
$$

## 2021 年 11 月期中第 1 題｜恰當方程（20 分）

**原題：** Solve $(2y+e^y+6x^2)y'+4+12xy=0$ for $y(0)=0$.

**中文：** 求初始條件 $y(0)=0$ 的一階微分方程解（與作業一第 4 題相同）。

**① 改成 $M\,dx+N\,dy=0$：**

$$
M=4+12xy,\qquad N=2y+e^y+6x^2.
$$

**② 檢查恰當條件：**

公式（恰當條件）：$M(x,y)\,dx+N(x,y)\,dy=0$ 在偏導數連續的單連通區域內為恰當方程的充要條件是 $M_y=N_x$，此時存在勢函數 $f(x,y)$ 使 $f_x=M$、$f_y=N$，解曲線為 $f(x,y)=C$，其中 $M,N$ 為 $dx,dy$ 的係數、$M_y=\partial M/\partial y$、$N_x=\partial N/\partial x$、$C$ 為常數；本題 $M=4+12xy$、$N=2y+e^y+6x^2$。

$M_y=12x=N_x$，所以是恰當方程。

**③ 由 $f_x=M$ 對 $x$ 積分：**

公式（冪次積分）：$\int x^n\,dx=\dfrac{x^{n+1}}{n+1}+C$（$n\ne-1$），其中 $x$ 為積分變數、$n$ 為常數指數、$C$ 為積分常數（對 $x$ 偏積分時改為只依賴 $y$ 的 $h(y)$）；本題 $\int4\,dx=4x$（$n=0$）、$\int12xy\,dx=6x^2y$（$n=1$，$y$ 視為常數）。

$$
f=\int(4+12xy)dx=4x+6x^2y+h(y).
$$

**④ 用 $f_y=N$ 決定 $h(y)$：**

$$
6x^2+h'(y)=2y+e^y+6x^2\Rightarrow h'(y)=2y+e^y,
$$

公式（標準積分）：$\int e^{ay}\,dy=\dfrac{1}{a}e^{ay}+C$（$a\ne0$），其中 $a$ 為常數、$y$ 為積分變數、$C$ 為積分常數；本題 $a=1$，另一項 $\int2y\,dy=y^2$ 用前面的冪次積分。

$$
h(y)=y^2+e^y.
$$

**⑤ 代初值 $(0,0)$：** $f(x,y)=4x+6x^2y+y^2+e^y=C$，代入得 $C=e^0=1$。

$$
\boxed{4x+6x^2y+y^2+e^y=1.}
$$
# 四、二階齊次常係數：實根、重根、複根與邊界條件

## 作業二｜總符號表

| 符號 | 中文意義與角色 |
|---|---|
| $x$ | 自變數；題 1、2 可取任意實數，題 3 的指定實數解使用 $x>0$。 |
| $y=y(x)$ | 待求的實值函數。 |
| $y',y''$ | 分別為 $dy/dx$、$d^2y/dx^2$，不是兩個不同的解。 |
| $r$ | 常係數方程中，試探指數解的指數係數，即特徵根。 |
| $i$ | 虛數單位，滿足 $i^2=-1$。 |
| $C_1,C_2$ | 每一題各自的實積分常數，不能跨題沿用數值。 |
| $y_1,y_2$ | 第 3 題的一個已知解與另一個待求的線性獨立解；下標不是導數。 |
| $v=v(x)$ | 降階時引入的未知倍數函數。 |
| $k_1,k_2$ | 求 $v$ 時得到的兩個積分常數。 |
| $e,\ln$ | 自然對數底數，以及自然對數函數。 |
| $\pi$ | 圓周率；三角函數使用弧度。 |

## 作業二第 1 題｜共軛複數根與邊界條件

**原題：** Solve $y''-2y'+2y=0$ with $y(0)=-3$ and $y(\pi/2)=0$.

**中文：** 求滿足此微分方程，且在 $x=0$ 時函數值為 $-3$、在 $x=\pi/2$ 時函數值為 $0$ 的解。第二個條件是函數值（邊界條件），不是 $y'(0)=0$。

**① 列特徵方程：** 係數都是常數、右側為零，設 $y=e^{rx}$，把微分方程化成代數方程。

公式（特徵方程）：常係數齊次方程 $ay''+by'+cy=0$ 代入試探解 $y=e^{rx}$ 得 $(ar^2+br+c)e^{rx}=0$，因 $e^{rx}\ne0$ 故 $ar^2+br+c=0$，其中 $a,b,c$ 為實常數係數（$a\ne0$）、$r$ 為特徵根；本題 $a=1,b=-2,c=2$。

$$
y=e^{rx}.
$$
$$
y'=re^{rx},\qquad y''=r^2e^{rx}.
$$
代入原式並提出公因式：
$$
r^2e^{rx}-2re^{rx}+2e^{rx}=0.
$$
$$
(r^2-2r+2)e^{rx}=0.
$$
因為 $e^{rx}\neq0$，除去這個因子：
$$
\boxed{r^2-2r+2=0}.
$$

**② 解特徵根，寫實通解：** 配方求根，再用 Euler 公式把複數解拆成實部與虛部。

$$
r^2-2r+2=(r-1)^2+1.
$$
$$
(r-1)^2=-1,
\qquad r-1=\pm i,
\qquad \boxed{r=1\pm i}.
$$

公式（Euler 公式）：$e^{i\theta}=\cos\theta+i\sin\theta$，故 $e^{(\alpha\pm i\beta)x}=e^{\alpha x}(\cos\beta x\pm i\sin\beta x)$，其中 $\theta,\alpha,\beta$ 為實數、$i$ 為虛數單位；本題 $\alpha=1,\beta=1$。

$$
e^{(1+i)x}=e^x(\cos x+i\sin x),
$$
$$
e^{(1-i)x}=e^x(\cos x-i\sin x).
$$
原方程係數是實數，所以實部 $e^x\cos x$、虛部 $e^x\sin x$ 各自是實數解，且互非常數倍。

公式（複根通解）：若特徵方程 $ar^2+br+c=0$ 的根為 $r=\alpha\pm i\beta$（$\beta\gt0$），則實通解為 $y=e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$，其中 $\alpha,\beta$ 為根的實部與虛部、$C_1,C_2$ 為實常數；本題 $\alpha=1,\beta=1$。

$$
\boxed{y=e^x(C_1\cos x+C_2\sin x)}.
$$

**③ 代第一個邊界條件 $y(0)=-3$：** 用 $e^0=1$、$\cos0=1$、$\sin0=0$。

$$
-3=e^0(C_1\cos0+C_2\sin0).
$$
$$
-3=1(C_1\cdot1+C_2\cdot0)=C_1.
$$
$$
\boxed{C_1=-3}.
$$

**④ 代第二個邊界條件 $y(\pi/2)=0$：** 用 $\cos(\pi/2)=0$、$\sin(\pi/2)=1$，再除以非零的 $e^{\pi/2}$。

$$
0=e^{\pi/2}\left[C_1\cos\frac\pi2+C_2\sin\frac\pi2\right].
$$
$$
0=e^{\pi/2}(C_1\cdot0+C_2\cdot1)=e^{\pi/2}C_2.
$$
$$
\boxed{C_2=0}.
$$

代回通解：
$$
\boxed{y(x)=-3e^x\cos x}.
$$
解在全部實數上有定義；視為兩端邊界問題時可限制在 $[0,\pi/2]$。

## 作業二第 2 題｜重根不能漏掉第二個解

**原題：** Solve $4y''+4y'+y=0$ with $y(0)=-2$ and $y'(0)=1$.

**中文：** 求滿足此微分方程，且在 $x=0$ 時函數值為 $-2$、導數為 $1$ 的解（一個約束函數值，一個約束斜率）。

**① 列特徵方程，辨認重根：** 設 $y=e^{rx}$，則 $y'=re^{rx}$、$y''=r^2e^{rx}$。

公式（特徵方程）：常係數齊次方程 $ay''+by'+cy=0$ 代入試探解 $y=e^{rx}$ 得 $(ar^2+br+c)e^{rx}=0$，因 $e^{rx}\ne0$ 故 $ar^2+br+c=0$，其中 $a,b,c$ 為實常數係數（$a\ne0$）、$r$ 為特徵根；本題 $a=4,b=4,c=1$。

$$
4r^2e^{rx}+4re^{rx}+e^{rx}=0.
$$
$$
4r^2+4r+1=0.
$$
$$
(2r+1)^2=0,
\qquad \boxed{r=-\frac12\quad\text{為二重根}}.
$$

**② 寫完整的重根通解：** 同一個解寫兩次只剩一個有效常數，第二個獨立解是 $xe^{-x/2}$。

$$
C_1e^{-x/2}+C_2e^{-x/2}=(C_1+C_2)e^{-x/2},
$$

公式（重根通解）：若特徵方程 $ar^2+br+c=0$ 有二重根 $r=r_0$（即 $b^2-4ac=0$，$r_0=-\dfrac{b}{2a}$），則通解為 $y=(C_1+C_2x)e^{r_0x}$，其中 $a,b,c$ 為常數係數、$C_1,C_2$ 為實常數；本題 $r_0=-\dfrac12$。

$$
\boxed{y=(C_1+C_2x)e^{-x/2}}.
$$

兩項都要先保留，再由初始條件決定係數。

**③ 第二解多乘 $x$ 的由來：** 令 $y=e^{-x/2}v$ 代入原方程，看 $v$ 要滿足什麼（此處 $v$、$k_1,k_2$ 與下一題不共用）。

$$
y=e^{-x/2}v.
$$

公式（乘積律）：$(fg)'=f'g+fg'$，其中 $f=f(x),g=g(x)$ 為可微函數；本題 $f=e^{-x/2}$、$g=v$，求 $y''$ 時對 $y'=e^{-x/2}(v'-\frac12v)$ 再用一次。

公式（指數函數導數）：$\dfrac{d}{dx}e^{ax}=ae^{ax}$，其中 $a$ 為常數；本題 $a=-\dfrac12$。

$$
y'=e^{-x/2}\left(v'-\frac12v\right),
$$
$$
y''=e^{-x/2}\left(v''-v'+\frac14v\right).
$$
代入原方程：
$$
\begin{aligned}
4y''+4y'+y
&=e^{-x/2}\left[4v''-4v'+v+4v'-2v+v\right]\\
&=4e^{-x/2}v''.
\end{aligned}
$$
所以 $v''=0$，積分兩次：
$$
v'=k_1,\qquad v=k_1x+k_2.
$$
$$
y=(k_2+k_1x)e^{-x/2}.
$$
重新命名常數就是上面的重根通解。

**④ 代函數值 $y(0)=-2$：**

$$
-2=(C_1+C_2\cdot0)e^0=C_1.
$$
$$
\boxed{C_1=-2}.
$$

**⑤ 微分通解：** 為了用 $y'(0)=1$，用乘積律把通解完整微分。

$$
\begin{aligned}
y'
&=(C_1+C_2x)'e^{-x/2}
 +(C_1+C_2x)(e^{-x/2})'\\
&=C_2e^{-x/2}
 -\frac12(C_1+C_2x)e^{-x/2}\\
&=e^{-x/2}\left[C_2-\frac12(C_1+C_2x)\right].
\end{aligned}
$$

**⑥ 代導數條件 $y'(0)=1$：** 令 $x=0$，代入 $C_1=-2$。

$$
y'(0)=C_2-\frac12C_1.
$$
$$
1=C_2-\frac12(-2)=C_2+1.
$$
$$
\boxed{C_2=0}.
$$

$$
\boxed{y(x)=-2e^{-x/2}}.
$$
答案沒有 $xe^{-x/2}$ 項，是因為初始條件讓它的係數為零，不是通解可以省略這一項。解定義在所有實數上。

## 2024 年 11 月期中第 3 題｜二階常係數複根（25 分）

**原題：** Solve $4y''+4y'+17y=0$ for $y(0)=4$ and $y'(0)=-6$; express the answer in real functions.

**中文：** 解二階齊次 ODE，並以實數函數表示。

**① 列特徵方程：** 設 $y=e^{rx}$。

公式（特徵方程）：常係數齊次方程 $ay''+by'+cy=0$ 代入試探解 $y=e^{rx}$ 得 $(ar^2+br+c)e^{rx}=0$，因 $e^{rx}\ne0$ 故 $ar^2+br+c=0$，其中 $a,b,c$ 為實常數係數（$a\ne0$）、$r$ 為特徵根；本題 $a=4,b=4,c=17$。

$$
4r^2+4r+17=0.
$$

**② 用二次公式求根：** 判別式 $\Delta=4^2-4(4)(17)=-256$，為負，得共軛複根。

公式（二次公式）：$ar^2+br+c=0$（$a\ne0$）的根為 $r=\dfrac{-b\pm\sqrt{\Delta}}{2a}$，$\Delta=b^2-4ac$，當 $\Delta\lt0$ 時 $\sqrt{\Delta}=i\sqrt{-\Delta}$，其中 $a,b,c$ 為係數、$\Delta$ 為判別式、$i$ 為虛數單位；本題 $a=4,b=4,c=17$，$\Delta=-256$，$\sqrt{-256}=16i$。

$$
r=\frac{-4\pm16i}{8}=-\frac12\pm2i.
$$

**③ 寫實通解：**

公式（複根通解）：若特徵方程 $ar^2+br+c=0$ 的根為 $r=\alpha\pm i\beta$（$\beta\gt0$），則實通解為 $y=e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$，其中 $\alpha,\beta$ 為根的實部與虛部、$C_1,C_2$ 為實常數；本題 $\alpha=-\dfrac12,\beta=2$。

$$
y=e^{-x/2}(C_1\cos2x+C_2\sin2x).
$$

**④ 代 $y(0)=4$，再微分：** $x=0$ 時只剩 $C_1$ 項，得 $C_1=4$；接著用乘積律完整微分。

公式（乘積律）：$(fg)'=f'g+fg'$，其中 $f=f(x),g=g(x)$ 為可微函數；本題 $f=e^{-x/2}$、$g=C_1\cos2x+C_2\sin2x$，且 $(e^{-x/2})'=-\frac12e^{-x/2}$。

公式（三角函數導數）：$\dfrac{d}{dx}\cos\beta x=-\beta\sin\beta x$，$\dfrac{d}{dx}\sin\beta x=\beta\cos\beta x$，其中 $\beta$ 為常數；本題 $\beta=2$。

$$
y'=e^{-x/2}\left[-\frac12(C_1\cos2x+C_2\sin2x)-2C_1\sin2x+2C_2\cos2x\right].
$$

**⑤ 代 $y'(0)=-6$：** $y'(0)=-C_1/2+2C_2=-2+2C_2=-6$，得 $C_2=-2$。

$$
\boxed{y=e^{-x/2}(4\cos2x-2\sin2x).}
$$

## 2022 年 11 月期中第 2 題｜二階齊次常係數（5 分）

**原題：** Solve $y''+y=0$ for $y(0)=1$, $y'(0)=1$.

**中文：** 求二階齊次 ODE 的初值解。

**① 列特徵方程：** 設 $y=e^{rx}$。

公式（特徵方程）：常係數齊次方程 $ay''+by'+cy=0$ 代入試探解 $y=e^{rx}$ 得 $(ar^2+br+c)e^{rx}=0$，因 $e^{rx}\ne0$ 故 $ar^2+br+c=0$，其中 $a,b,c$ 為實常數係數（$a\ne0$）、$r$ 為特徵根；本題 $a=1,b=0,c=1$。

$$
r^2+1=0\quad\Rightarrow\quad r=\pm i.
$$

**② 寫實通解並微分：**

公式（複根通解）：若特徵方程 $ar^2+br+c=0$ 的根為 $r=\alpha\pm i\beta$（$\beta\gt0$），則實通解為 $y=e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$，其中 $\alpha,\beta$ 為根的實部與虛部、$C_1,C_2$ 為實常數；本題 $\alpha=0,\beta=1$，故 $y=C_1\cos x+C_2\sin x$。

$$
y'=-C_1\sin x+C_2\cos x.
$$

**③ 代初值：** $y(0)=1$ 得 $C_1=1$；$y'(0)=1$ 得 $C_2=1$。

$$
\boxed{y=\cos x+\sin x.}
$$

## 2021 年 11 月期中第 3 題｜二階齊次常係數初值題（20 分）

**原題：** Solve $y''+y'-2y=0$ with $y(0)=4$, $y'(0)=-5$.

**中文：** 求符合指定初始值與斜率的二階齊次方程解。

**① 特徵方程與通解：** 特徵方程 $r^2+r-2=(r-1)(r+2)=0$，兩相異實根 $1,-2$。

公式（特徵方程）：常係數齊次方程 $ay''+by'+cy=0$ 代入試探解 $y=e^{rx}$ 得 $(ar^2+br+c)e^{rx}=0$，因 $e^{rx}\ne0$ 故 $ar^2+br+c=0$，其中 $a,b,c$ 為實常數係數（$a\ne0$）、$r$ 為特徵根；本題 $a=1,b=1,c=-2$。

公式（相異實根通解）：若特徵方程 $ar^2+br+c=0$ 有兩相異實根 $r_1\ne r_2$，則齊次通解為 $y=C_1e^{r_1x}+C_2e^{r_2x}$，其中 $r_1,r_2$ 為兩個特徵根、$C_1,C_2$ 為由初值決定的常數；本題 $r_1=1,r_2=-2$。

$$
y=C_1e^x+C_2e^{-2x}.
$$

**② 代初值解聯立：** $y(0)=4$ 給 $C_1+C_2=4$；$y'=C_1e^x-2C_2e^{-2x}$ 及 $y'(0)=-5$ 給 $C_1-2C_2=-5$。兩式相減 $3C_2=9$，得 $C_2=3,C_1=1$：

$$
\boxed{y=e^x+3e^{-2x}.}
$$

# 五、降階法

## 作業二第 3 題｜用已知解降階，找另一個線性獨立解

**原題：** Given that $y_1=\dfrac1{\sqrt{x}}$ is a solution of a Cauchy–Euler equation $4x^2y''+8xy'+y=0$, find the second linearly independent solution $y_2$.

**中文：** 已知 $y_1=1/\sqrt{x}$ 是此 Cauchy–Euler（柯西—尤拉）方程的一個解，求另一個與它線性獨立的解 $y_2$。因為 $1/\sqrt{x}$ 要是實值，全題在 $x>0$ 上處理。

**① 降階代換：** 已知解乘常數不會產生新解，所以改乘一個未知函數 $v(x)$；$x>0$ 時 $y_1\ne0$，代換合法。

$$
\boxed{y=v(x)y_1(x)=vx^{-1/2}}.
$$

**② 算一階、二階導數：** 先微分 $x^{-1/2}$，再用乘積律。

公式（冪函數導數）：$\dfrac{d}{dx}x^n=nx^{n-1}$，其中 $n$ 為實常數、$x\gt0$；本題 $n=-\dfrac12$，第二次微分時再用 $n=-\dfrac32$。

$$
\frac{d}{dx}x^{-1/2}=-\frac12x^{-3/2}.
$$

公式（乘積律）：$(fg)'=f'g+fg'$，其中 $f=f(x),g=g(x)$ 為可微函數；本題 $f=v$、$g=x^{-1/2}$；求 $y''$ 時對 $v'x^{-1/2}$ 與 $vx^{-3/2}$ 各用一次。

$$
\boxed{y'=v'x^{-1/2}-\frac12vx^{-3/2}}.
$$
$$
\begin{aligned}
y''
&=\frac{d}{dx}(v'x^{-1/2})
 -\frac12\frac{d}{dx}(vx^{-3/2})\\
&=v''x^{-1/2}-\frac12v'x^{-3/2}
 -\frac12v'x^{-3/2}+\frac34vx^{-5/2}.
\end{aligned}
$$
合併兩個 $-\frac12v'x^{-3/2}$：
$$
\boxed{y''=v''x^{-1/2}-v'x^{-3/2}+\frac34vx^{-5/2}}.
$$

**③ 代回原方程：** 三部分分開算再相加，含 $v$ 本身的項係數 $3-4+1=0$ 消失。

$$
4x^2y''
=4x^{3/2}v''-4x^{1/2}v'+3x^{-1/2}v,
$$
$$
8xy'=8x^{1/2}v'-4x^{-1/2}v,
$$
$$
y=x^{-1/2}v.
$$
$$
4x^{3/2}v''+(-4+8)x^{1/2}v'
 +(3-4+1)x^{-1/2}v=0.
$$
$$
4x^{3/2}v''+4x^{1/2}v'=0.
$$
$x>0$，除以非零的 $4x^{1/2}$：
$$
\boxed{xv''+v'=0}.
$$

**④ 積分兩次求 $v$：** 左邊正是 $(xv')'$；$k_1,k_2$ 為兩次積分的常數。

$$
\frac{d}{dx}(xv')=v'+xv''.
$$
$$
\frac{d}{dx}(xv')=0.
$$
$$
xv'=k_1.
$$
$$
v'=\frac{k_1}{x}.
$$

公式（標準積分）：$\int\dfrac{1}{x}\,dx=\ln|x|+C$，其中 $C$ 為積分常數；本題 $x\gt0$ 故 $|x|=x$，被積函數多一個常數因子 $k_1$，積分常數記為 $k_2$。

$$
\begin{aligned}
v&=\int\frac{k_1}{x}\,dx+k_2\\
 &=k_1\ln x+k_2.
\end{aligned}
$$
$$
\boxed{v=k_1\ln x+k_2}.
$$

**⑤ 取出新的解：** 代回 $y=vx^{-1/2}$，第二項只是 $y_1$ 的常數倍，第一項才是新形狀；取 $k_1=1$、$k_2=0$。

$$
\begin{aligned}
y
&=(k_1\ln x+k_2)x^{-1/2}\\
&=k_1\frac{\ln x}{\sqrt{x}}+k_2\frac1{\sqrt{x}}.
\end{aligned}
$$

$$
\boxed{y_2(x)=\frac{\ln x}{\sqrt{x}},\qquad x>0}.
$$

**⑥ 說明線性獨立並寫通解：** 兩函數的比值不是常數就線性獨立。

$$
\frac{y_2}{y_1}
=\frac{(\ln x)/\sqrt{x}}{1/\sqrt{x}}
=\ln x.
$$
$$
\frac{d}{dx}\ln x=\frac1x\neq0
\qquad(x>0).
$$
比值不是常數，兩解線性獨立。通解（無初始條件，$C_1,C_2$ 不定值）：
$$
\boxed{
 y=C_1\frac1{\sqrt{x}}+C_2\frac{\ln x}{\sqrt{x}},\qquad x>0
}.
$$

## 2025 年 10 月期中第 2 題｜降階法公式證明（25 分）

**原題：** Consider $y''+P(x)y'+Q(x)y=0$ with one known solution $y_1$. Using reduction of order, show that a second linearly independent solution can be written as $y_2=y_1\int e^{-\int P(x)dx}/y_1^2\,dx$.

**中文：** 已知二階齊次線性方程的一個解 $y_1$，利用降階法推導另一個線性獨立解的公式。

符號：$P,Q$ 是給定的係數函數；$v(x)$ 是要找的新函數；以下在 $y_1\neq0$ 的區間操作。

**① 設 $y_2=vy_1$ 並微分：**

公式（乘積律）：$(fg)'=f'g+fg'$，再微分一次得 $(fg)''=f''g+2f'g'+fg''$，其中 $f=f(x),g=g(x)$ 為二次可微函數；本題 $f=v$、$g=y_1$。

$$
y_2'=v'y_1+vy_1',\qquad y_2''=v''y_1+2v'y_1'+vy_1''.
$$

**② 代回原方程：** $y_1$ 本身是解，所以 $v$ 的係數括號為零；再除以非零的 $y_1$。

$$
y_1v''+(2y_1'+Py_1)v'+(y_1''+Py_1'+Qy_1)v=0.
$$
$$
v''+\left(2\frac{y_1'}{y_1}+P\right)v'=0.
$$

**③ 令 $w=v'$ 降成一階：**

$$
w'+\left(2\frac{y_1'}{y_1}+P\right)w=0.
$$

**④ 分離變數積分：** 取 $w\neq0$ 的非平凡解。

公式（可分離變數）：$\dfrac{dw}{dx}=-g(x)w$ 在 $w\ne0$ 時可寫成 $\dfrac{dw}{w}=-g(x)\,dx$ 再兩邊積分，其中 $w=w(x)$ 為未知函數、$g(x)$ 為已知函數；本題 $g=2\dfrac{y_1'}{y_1}+P$。

$$
\frac{dw}{w}=-\left(2\frac{y_1'}{y_1}+P\right)dx,
$$

公式（對數積分）：$\int\dfrac{f'(x)}{f(x)}\,dx=\ln|f(x)|+C$，其中 $f$ 為可微且 $f\ne0$ 的函數、$C$ 為積分常數；本題左邊 $\int\dfrac{dw}{w}=\ln|w|$，右邊 $\int2\dfrac{y_1'}{y_1}\,dx=2\ln|y_1|$。

$$
\ln|w|=-2\ln|y_1|-\int P(x)dx+C.
$$

**⑤ 指數化、再積分一次：** 非零乘法常數 $e^C$ 併入正規化。

公式（指數與對數）：$e^{A+B}=e^Ae^B$，$e^{k\ln|u|}=|u|^k$，其中 $A,B,k$ 為實數、$u\ne0$；本題 $e^{-2\ln|y_1|}=\dfrac{1}{y_1^2}$，$e^{C}$ 為非零常數。

$$
w=v'=\frac{e^{-\int P(x)dx}}{y_1^2}.
$$

再積分得 $v=\int e^{-\int P}/y_1^2\,dx$，因此
$$
\boxed{y_2=y_1\int\frac{e^{-\int P(x)dx}}{y_1(x)^2}\,dx.}
$$

**⑥ 線性獨立：** Wronskian $W=y_1y_2'-y_1'y_2$，代入 $y_2=vy_1$：

$$
W=y_1^2v'=e^{-\int P(x)dx}\neq0.
$$

所以兩解線性獨立；積分常數造成的 $Cy_1$ 項可被齊次解吸收。

# 六、二階非齊次：未定係數法與初值問題

## 作業三｜共用符號

$x$：自變數；$y$：待求函數；$y_h$：齊次解；$y_p$：非齊次特解；$D=d/dx$：微分算子；$L(D)$：常係數微分多項式；$A,B,C,D_0$：待定係數（$D_0$ 和微分算子 $D$ 不同）；$C_1,C_2$：齊次通解常數。

## 作業三第 1 題｜加總規則 sum rule

**原題：** Solve $y''+2y'+y=\sin x+3\cos2x$ with $y(0)=0$, $y'(0)=0$. Hint: sum rule.

**中文：** 求二階非齊次 ODE 的初值解；分開求右側兩項的特解再相加。

符號：$y_{p1},y_{p2}$：分別對應 $\sin x$、$3\cos2x$ 的特解；$L[y]=y''+2y'+y$。

**① 齊次解：** 特徵方程 $r^2+2r+1=(r+1)^2=0$，重根 $r=-1$。

公式（重根通解）：常係數方程 $ay''+by'+cy=0$ 的特徵方程為 $ar^2+br+c=0$，若有二重根 $r=r_0$，則齊次通解為 $y_h=(C_1+C_2x)e^{r_0x}$，其中 $a,b,c$ 為常數係數、$C_1,C_2$ 為齊次通解常數；本題 $a=1,b=2,c=1$，$r_0=-1$。

$$
\boxed{y_h=(C_1+C_2x)e^{-x}.}
$$

**② 第一組右側 $\sin x$：** 特徵根 $-1$ 不是 $\pm i$，用一般三角試探解。

公式（三角試探解）：若右側為 $k_1\cos\omega x+k_2\sin\omega x$ 且 $\pm i\omega$ 不是左側算子的特徵根，設特解 $y_p=A\cos\omega x+B\sin\omega x$，其中 $k_1,k_2$ 為已知常數、$\omega\gt0$ 為常數、$A,B$ 為待定係數；本題 第一組 $\omega=1$（係數 $A,B$），第二組 $\omega=2$（係數 $C,D_0$），特徵根 $-1$ 不等於 $\pm i$、$\pm2i$。

設 $y_{p1}=A\cos x+B\sin x$：
$$
y_{p1}'=-A\sin x+B\cos x,\qquad y_{p1}''=-A\cos x-B\sin x.
$$
$$
L[y_{p1}]=(-A\cos x-B\sin x)+2(-A\sin x+B\cos x)+(A\cos x+B\sin x)
=2B\cos x-2A\sin x.
$$
與 $\sin x$ 比較：$2B=0$、$-2A=1$，得 $B=0,A=-1/2$：
$$
\boxed{y_{p1}=-\frac12\cos x.}
$$

**③ 第二組右側 $3\cos2x$：** 設 $y_{p2}=C\cos2x+D_0\sin2x$。

$$
y_{p2}'=-2C\sin2x+2D_0\cos2x,
$$
$$
y_{p2}''=-4C\cos2x-4D_0\sin2x.
$$
$$
L[y_{p2}]=(-3C+4D_0)\cos2x+(-4C-3D_0)\sin2x.
$$
比較係數：
$$
-3C+4D_0=3,\qquad -4C-3D_0=0.
$$
由第二式 $C=-3D_0/4$，代入第一式：
$$
\frac94D_0+4D_0=3
\Rightarrow \frac{25}4D_0=3
\Rightarrow D_0=\frac{12}{25},
$$
$$
C=-\frac34\frac{12}{25}=-\frac9{25}.
$$
$$
\boxed{y_{p2}=-\frac9{25}\cos2x+\frac{12}{25}\sin2x.}
$$

**④ 加總得通解：**

公式（疊加原理）：若 $L[y_{p1}]=f_1$、$L[y_{p2}]=f_2$，則 $L[y_{p1}+y_{p2}]=f_1+f_2$，其中 $L$ 為線性微分算子、$f_1,f_2$ 為右側各部分、$y_{p1},y_{p2}$ 為各自的特解；本題 $L[y]=y''+2y'+y$，$f_1=\sin x$、$f_2=3\cos2x$。

公式（非齊次通解）：$y=y_h+y_p$，其中 $y_h$ 為齊次方程的通解（含兩個常數）、$y_p$ 為非齊次方程的任一特解；本題 $y_h=(C_1+C_2x)e^{-x}$，$y_p=y_{p1}+y_{p2}$。

$$
y=(C_1+C_2x)e^{-x}-\frac12\cos x-\frac9{25}\cos2x+\frac{12}{25}\sin2x.
$$

**⑤ 代 $y(0)=0$：** $C_1-1/2-9/25=0$，通分後 $C_1=25/50+18/50=43/50$。

**⑥ 微分並代 $y'(0)=0$：** 重根項用乘積律。

公式（乘積律）：$(fg)'=f'g+fg'$，其中 $f=f(x),g=g(x)$ 為可微函數；本題 $f=C_1+C_2x$、$g=e^{-x}$，且 $(e^{-x})'=-e^{-x}$。

$$
y'=(C_2-C_1-C_2x)e^{-x}+\frac12\sin x+\frac{18}{25}\sin2x+\frac{24}{25}\cos2x.
$$
由 $y'(0)=0$：$0=C_2-C_1+24/25$，所以
$$
C_2=\frac{43}{50}-\frac{48}{50}=-\frac1{10}.
$$

$$
\boxed{y=\frac{43}{50}e^{-x}-\frac1{10}xe^{-x}-\frac12\cos x-\frac9{25}\cos2x+\frac{12}{25}\sin2x.}
$$

## 作業三第 2 題｜乘法規則 multiplication rule

**原題：** Find a particular solution of $y''-4y'-12y=xe^{-4x}$. Hint: multiplication rule.

**中文：** 使用乘法規則求一個非齊次特解（不要求初值或齊次通解）。

**① 用乘法規則去掉指數：** 左側寫成 $L(D)y$，$L(D)=D^2-4D-12$；forcing 是多項式乘 $e^{-4x}$，令 $y_p=e^{-4x}v(x)$。

$$
y_p=e^{-4x}v(x).
$$
$$
L(D)[e^{ax}v]=e^{ax}L(D+a)v.
$$

符號：$a$：指數 $e^{ax}$ 裡的常數；$L(D+a)$：把 $L(D)$ 每個 $D$ 換成 $D+a$ 的算子；$A,B$：待定係數。

本題 $a=-4$：
$$
e^{-4x}L(D-4)v=xe^{-4x}\Rightarrow L(D-4)v=x.
$$

**② 展開平移後的算子：**

$$
L(D-4)=(D-4)^2-4(D-4)-12
=D^2-8D+16-4D+16-12
=D^2-12D+20.
$$

**③ 多項式試探解：** 得 $v''-12v'+20v=x$，右側一次，設 $v=Ax+B$，則 $v'=A$、$v''=0$。

公式（多項式試探解）：若右側為 $n$ 次多項式 $p_n(x)$ 且 $0$ 不是左側算子的特徵根（算子常數項不為零），設特解為 $n$ 次多項式 $A_nx^n+\dots+A_1x+A_0$，其中 $A_0,\dots,A_n$ 為待定係數；本題 算子為 $L(D-4)=D^2-12D+20$，常數項 $20\ne0$，右側 $x$ 為 $n=1$ 次，係數記為 $A,B$。

$$
-12A+20(Ax+B)=20Ax+(20B-12A)=x.
$$
比較 $x^1$、常數項：
$$
20A=1\Rightarrow A=\frac1{20};\qquad
20B-12A=0\Rightarrow B=\frac{12}{20}\frac1{20}=\frac3{100}.
$$

$$
\boxed{y_p=e^{-4x}\left(\frac3{100}+\frac1{20}x\right).}
$$

## 作業三第 3 題｜修正規則 modification rule

**原題：** Find a particular solution of $y''+y=2x\sin x$. Hint: modification rule.

**中文：** 先判斷齊次解與試解的重合，再用修正規則求非齊次特解。

**① 齊次解：** 特徵方程 $r^2+1=0$，根 $r=\pm i$。

公式（複根通解）：常係數方程 $ay''+by'+cy=0$ 的特徵方程為 $ar^2+br+c=0$，若其根為 $r=\alpha\pm i\beta$（$\beta\gt0$），則齊次實通解為 $y_h=e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$，其中 $a,b,c$ 為常數係數、$\alpha,\beta$ 為根的實部與虛部、$C_1,C_2$ 為齊次通解常數；本題 $a=1,b=0,c=1$，$\alpha=0,\beta=1$。

$$
y_h=C_1\cos x+C_2\sin x.
$$

**② 修正試探解：** 正常試解 $(Ax+B)\cos x+(Cx+D_0)\sin x$ 和齊次解重疊，$i$ 是一重根，整體乘 $x$。

公式（修正規則）：右側為 $e^{\alpha x}p_n(x)\cos\beta x$ 或 $e^{\alpha x}p_n(x)\sin\beta x$ 時，正常試解為 $e^{\alpha x}[P_n(x)\cos\beta x+Q_n(x)\sin\beta x]$；若 $\alpha+i\beta$ 是 $s$ 重特徵根，整個試解再乘 $x^s$，其中 $p_n$ 為已知 $n$ 次多項式、$P_n,Q_n$ 為係數待定的 $n$ 次多項式、$s$ 為重數（不是根時 $s=0$）；本題 右側 $2x\sin x$ 對應 $\alpha=0,\beta=1,n=1$，$i$ 是一重特徵根，$s=1$。

$$
y_p=x[(Ax+B)\cos x+(Cx+D_0)\sin x].
$$

**③ 微分代入：** 令 $u=Ax^2+Bx$、$v=Cx^2+D_0x$，則 $y_p=u\cos x+v\sin x$，用乘積律微分兩次。

公式（乘積律）：$(fg)'=f'g+fg'$，再微分一次得 $(fg)''=f''g+2f'g'+fg''$，其中 $f=f(x),g=g(x)$ 為二次可微函數；本題 $f=u$ 或 $v$、$g=\cos x$ 或 $\sin x$。

$$
y_p'= (u'+v)\cos x+(v'-u)\sin x,
$$
$$
y_p''+y_p=(u''+2v')\cos x+(v''-2u')\sin x.
$$
$$
u'=2Ax+B,\quad u''=2A;
\qquad v'=2Cx+D_0,\quad v''=2C.
$$
$$
y_p''+y_p=(2A+4Cx+2D_0)\cos x+(2C-4Ax-2B)\sin x.
$$

**④ 比較係數：** 與 $0\cos x+2x\sin x$ 比較。

$$
4C=0,\quad 2A+2D_0=0,\quad -4A=2,\quad 2C-2B=0.
$$
依次解得 $C=0,A=-1/2,D_0=1/2,B=0$：
$$
\boxed{y_p=-\frac12x^2\cos x+\frac12x\sin x.}
$$

## 2025 年 10 月期中第 3 題｜二階非齊次初值題（25 分）

**原題：** Solve $y''+2y'-8y=-9\cos x-2\sin x$, with $y(0)=4$ and $y'(0)=-6$.

**中文：** 求二階非齊次方程的特定初值解。

**① 齊次解：** 特徵方程兩相異實根 $2,-4$。

公式（特徵方程）：常係數齊次方程 $ay''+by'+cy=0$ 代入試探解 $y=e^{rx}$ 得 $(ar^2+br+c)e^{rx}=0$，因 $e^{rx}\ne0$ 故 $ar^2+br+c=0$，其中 $a,b,c$ 為實常數係數（$a\ne0$）、$r$ 為特徵根；本題 $a=1,b=2,c=-8$。

公式（相異實根通解）：若特徵方程 $ar^2+br+c=0$ 有兩相異實根 $r_1\ne r_2$，則齊次通解為 $y=C_1e^{r_1x}+C_2e^{r_2x}$，其中 $r_1,r_2$ 為兩個特徵根、$C_1,C_2$ 為由初值決定的常數；本題 $r_1=2,r_2=-4$。

$$
r^2+2r-8=(r-2)(r+4)=0,
\quad y_h=C_1e^{2x}+C_2e^{-4x}.
$$

**② 特解：** 右側是正弦與餘弦，設 $y_p=A\cos x+B\sin x$。

公式（三角試探解）：若右側為 $k_1\cos\omega x+k_2\sin\omega x$ 且 $\pm i\omega$ 不是左側算子的特徵根，設特解 $y_p=A\cos\omega x+B\sin\omega x$，其中 $k_1,k_2$ 為已知常數、$\omega\gt0$ 為常數、$A,B$ 為待定係數；本題 $\omega=1$，特徵根 $2,-4$ 不等於 $\pm i$。

$$
y_p'=-A\sin x+B\cos x,\qquad y_p''=-A\cos x-B\sin x.
$$
代入 $y_p''+2y_p'-8y_p$ 並比較係數：
$$
(-9A+2B)\cos x+(-2A-9B)\sin x=-9\cos x-2\sin x,
$$
$$
-9A+2B=-9,\quad -2A-9B=-2.
$$
解得 $A=1,B=0$，所以 $y_p=\cos x$。

**③ 通解：**

公式（非齊次通解）：$y=y_h+y_p$，其中 $y_h$ 為齊次方程的通解（含兩個常數）、$y_p$ 為非齊次方程的任一特解；本題 $y_h=C_1e^{2x}+C_2e^{-4x}$，$y_p=\cos x$。

$$
y=C_1e^{2x}+C_2e^{-4x}+\cos x.
$$

**④ 代初值：** $y(0)=4$ 給 $C_1+C_2+1=4$，即 $C_1+C_2=3$；再用

$$
y'=2C_1e^{2x}-4C_2e^{-4x}-\sin x
$$

及 $y'(0)=-6$ 給 $2C_1-4C_2=-6$。解聯立得 $C_1=1,C_2=2$：

$$
\boxed{y=e^{2x}+2e^{-4x}+\cos x.}
$$

## 2024 年 11 月期中第 4 題｜未定係數法：sum rule（25 分）

**原題：** Find the particular solution $y_p$ of $y''+2y'-8y=(x-1)^2+e^{-2x}-9\cos x-2\sin x$.

**中文：** 求一個特解。右側有多項式、指數函數與三角函數，可由線性加總規則拆成三組。

**① 拆成三組：** 設 $L[y]=y''+2y'-8y$，分別求 $L[y_{p1}]=(x-1)^2$、$L[y_{p2}]=e^{-2x}$、$L[y_{p3}]=-9\cos x-2\sin x$。

公式（疊加原理）：若 $L[y_{pk}]=f_k$（$k=1,2,3$），則 $L[y_{p1}+y_{p2}+y_{p3}]=f_1+f_2+f_3$，其中 $L$ 為線性微分算子、$f_k$ 為右側第 $k$ 部分、$y_{pk}$ 為其特解；本題 $f_1=(x-1)^2$、$f_2=e^{-2x}$、$f_3=-9\cos x-2\sin x$。

符號：$A,B,C,D,E,F$：待定係數。

**② 第一組，多項式：** $(x-1)^2=x^2-2x+1$，設 $y_{p1}=Ax^2+Bx+C$，則 $y_{p1}'=2Ax+B$、$y_{p1}''=2A$，代入並按 $x$ 次數整理。

公式（多項式試探解）：若右側為 $n$ 次多項式 $p_n(x)$ 且 $0$ 不是左側算子的特徵根（算子常數項不為零），設特解為 $n$ 次多項式 $A_nx^n+\dots+A_1x+A_0$，其中 $A_0,\dots,A_n$ 為待定係數；本題 $L[y]=y''+2y'-8y$ 的常數項 $-8\ne0$（特徵根 $2,-4$），右側 $(x-1)^2$ 為 $n=2$ 次，係數記為 $A,B,C$。

$$
L[y_{p1}]=-8Ax^2+(4A-8B)x+(2A+2B-8C).
$$
比較係數：
$$
-8A=1,\quad 4A-8B=-2,\quad 2A+2B-8C=1.
$$
解得 $A=-1/8$、$B=3/16$、$C=-7/64$：
$$
y_{p1}=-\frac18x^2+\frac3{16}x-\frac7{64}.
$$

**③ 第二組，指數：** 設 $y_{p2}=De^{-2x}$，導數為 $-2De^{-2x}$、$4De^{-2x}$。

公式（指數試探解）：若右側為 $qe^{\alpha x}$ 且 $\alpha$ 不是特徵根，設特解 $y_p=Ke^{\alpha x}$，其中 $q$ 為已知常數、$\alpha$ 為常數、$K$ 為待定係數；本題 $q=1,\alpha=-2$，$-2$ 不是特徵根 $2,-4$，係數記為 $D$。

$$
L[y_{p2}]=(4D-4D-8D)e^{-2x}=-8De^{-2x}=e^{-2x},
$$
故 $D=-1/8$。

**④ 第三組，三角：** 設 $y_{p3}=E\cos x+F\sin x$。

公式（三角試探解）：若右側為 $k_1\cos\omega x+k_2\sin\omega x$ 且 $\pm i\omega$ 不是左側算子的特徵根，設特解 $y_p=A\cos\omega x+B\sin\omega x$，其中 $k_1,k_2$ 為已知常數、$\omega\gt0$ 為常數、$A,B$ 為待定係數；本題 $\omega=1$，特徵根 $2,-4$ 不等於 $\pm i$，係數記為 $E,F$。

$$
L[y_{p3}]=(-9E+2F)\cos x+(-2E-9F)\sin x.
$$
令之等於 $-9\cos x-2\sin x$，得 $E=1,F=0$，故 $y_{p3}=\cos x$。

**⑤ 加總：**

$$
\boxed{y_p=-\frac18x^2+\frac3{16}x-\frac7{64}-\frac18e^{-2x}+\cos x.}
$$

## 2023 年 11 月期中第 3 題｜二階非齊次方程（總 18 分，三小題）

**原題：** Consider $y''+2y'+17y=60e^{-4x}\sin(5x)$. (1) Find the complementary solution. (2) Find the particular solution. (3) Find the unique solution for $y(0)=0$, $y'(0)=2$.

**中文：** 依序求齊次解、非齊次特解、滿足初值的完整解。

### (1) Complementary solution（齊次解）

**① 特徵方程求根：** 設 $y_h=e^{rx}$。

公式（特徵方程）：常係數齊次方程 $ay''+by'+cy=0$ 代入試探解 $y=e^{rx}$ 得 $(ar^2+br+c)e^{rx}=0$，因 $e^{rx}\ne0$ 故 $ar^2+br+c=0$，其中 $a,b,c$ 為實常數係數（$a\ne0$）、$r$ 為特徵根；本題 $a=1,b=2,c=17$。

公式（二次公式）：$ar^2+br+c=0$（$a\ne0$）的根為 $r=\dfrac{-b\pm\sqrt{\Delta}}{2a}$，$\Delta=b^2-4ac$，當 $\Delta\lt0$ 時 $\sqrt{\Delta}=i\sqrt{-\Delta}$，其中 $a,b,c$ 為係數、$\Delta$ 為判別式、$i$ 為虛數單位；本題 $a=1,b=2,c=17$，$\Delta=-64$，$\sqrt{-64}=8i$。

$$
r^2+2r+17=0\Rightarrow r=-1\pm4i.
$$

**② 寫齊次解：**

公式（複根通解）：若特徵方程 $ar^2+br+c=0$ 的根為 $r=\alpha\pm i\beta$（$\beta\gt0$），則實通解為 $y=e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$，其中 $\alpha,\beta$ 為根的實部與虛部、$C_1,C_2$ 為實常數；本題 $\alpha=-1,\beta=4$，所得 $y$ 即齊次解 $y_h$。

$$
\boxed{y_h=e^{-x}(C_1\cos4x+C_2\sin4x).}
$$

### (2) Particular solution（特解）

**① 乘法規則：** 右側含 $e^{-4x}$，設 $y_p=e^{-4x}v(x)$，$D=d/dx$。

公式（乘法規則）：$L(D)[e^{ax}v]=e^{ax}L(D+a)v$，其中 $D=d/dx$、$a$ 為常數、$v=v(x)$ 為待求函數、$L(D+a)$ 是把 $L(D)$ 中每個 $D$ 換成 $D+a$ 的算子；本題 $L(D)=D^2+2D+17$、$a=-4$。

$$
(D^2+2D+17)[e^{-4x}v]=e^{-4x}[(D-4)^2+2(D-4)+17]v.
$$
展開 $(D-4)^2+2(D-4)+17=D^2-6D+25$，因此
$$
v''-6v'+25v=60\sin5x.
$$

**② 三角試探解：** 試 $v=A\cos5x+B\sin5x$，則 $v''+25v=0$，只剩 $-6v'=30A\sin5x-30B\cos5x$。

公式（三角試探解）：若右側為 $k_1\cos\omega x+k_2\sin\omega x$ 且 $\pm i\omega$ 不是左側算子的特徵根，設特解 $y_p=A\cos\omega x+B\sin\omega x$，其中 $k_1,k_2$ 為已知常數、$\omega\gt0$ 為常數、$A,B$ 為待定係數；本題 對 $v$ 的方程 $\omega=5$，平移後算子 $D^2-6D+25$ 的特徵根 $3\pm4i$ 不等於 $\pm5i$。

$$
30A=60,\qquad -30B=0
\quad\Rightarrow A=2,\ B=0.
$$
$$
\boxed{y_p=2e^{-4x}\cos5x.}
$$
**注意：** $D^2+25$ 的抵消不代表要額外乘 $x$；齊次根 $-1\pm4i$ 和右側的 $-4\pm5i$ 不重合。

### (3) Unique solution（初值解）

**① 通解：**

公式（非齊次通解）：$y=y_h+y_p$，其中 $y_h$ 為齊次方程的通解（含兩個常數）、$y_p$ 為非齊次方程的任一特解；本題 $y_h=e^{-x}(C_1\cos4x+C_2\sin4x)$，$y_p=2e^{-4x}\cos5x$。

$$
y=e^{-x}(C_1\cos4x+C_2\sin4x)+2e^{-4x}\cos5x.
$$

**② 代 $y(0)=0$：** $C_1+2=0$，故 $C_1=-2$。

**③ 微分並代 $y'(0)=2$：**

公式（乘積律）：$(fg)'=f'g+fg'$，其中 $f=f(x),g=g(x)$ 為可微函數；本題 $f=e^{-x}$、$g=C_1\cos4x+C_2\sin4x$，以及 $f=2e^{-4x}$、$g=\cos5x$，並用 $(e^{ax})'=ae^{ax}$、$(\cos\beta x)'=-\beta\sin\beta x$、$(\sin\beta x)'=\beta\cos\beta x$。

$$
y'=e^{-x}\left[-C_1\cos4x-C_2\sin4x-4C_1\sin4x+4C_2\cos4x\right]
+2e^{-4x}[-4\cos5x-5\sin5x].
$$
代 $x=0$：$y'(0)=-C_1+4C_2-8=2$；代 $C_1=-2$ 得 $2+4C_2-8=2$，所以 $C_2=2$。

$$
\boxed{y=e^{-x}(-2\cos4x+2\sin4x)+2e^{-4x}\cos5x.}
$$

## 2022 年 11 月期中第 3 題｜二階非齊次初值問題（5 分）

**原題：** Solve $y''-2y'+2y=2(x-1)$ with $y(0)=0$, $y'(0)=1$.

**中文：** 求二階非齊次方程的指定初值解。

**① 齊次解：** 特徵方程 $r^2-2r+2=0$，根 $r=1\pm i$。

公式（複根通解）：常係數方程 $ay''+by'+cy=0$ 的特徵方程為 $ar^2+br+c=0$，若其根為 $r=\alpha\pm i\beta$（$\beta\gt0$），則齊次實通解為 $y_h=e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$，其中 $a,b,c$ 為常數係數、$\alpha,\beta$ 為根的實部與虛部、$C_1,C_2$ 為齊次通解常數；本題 $a=1,b=-2,c=2$，$\alpha=1,\beta=1$。

$$
y_h=e^x(C_1\cos x+C_2\sin x).
$$

**② 特解：** 右側是一次多項式 $2x-2$，試 $y_p=Ax+B$，$y_p'=A$、$y_p''=0$。

公式（多項式試探解）：若右側為 $n$ 次多項式 $p_n(x)$ 且 $0$ 不是左側算子的特徵根（算子常數項不為零），設特解為 $n$ 次多項式 $A_nx^n+\dots+A_1x+A_0$，其中 $A_0,\dots,A_n$ 為待定係數；本題 左側常數項 $2\ne0$（特徵根 $1\pm i$），右側 $2x-2$ 為 $n=1$ 次，係數記為 $A,B$。

$$
0-2A+2(Ax+B)=2x-2,
$$
比較係數 $2A=2\Rightarrow A=1$，常數 $-2A+2B=-2\Rightarrow B=0$，所以 $y_p=x$。

**③ 通解：**

公式（非齊次通解）：$y=y_h+y_p$，其中 $y_h$ 為齊次方程的通解（含兩個常數）、$y_p$ 為非齊次方程的任一特解；本題 $y_h=e^x(C_1\cos x+C_2\sin x)$，$y_p=x$。

$$
y=e^x(C_1\cos x+C_2\sin x)+x.
$$

**④ 代初值：** $y(0)=0$ 給 $C_1=0$；再微分。

公式（乘積律）：$(fg)'=f'g+fg'$，其中 $f=f(x),g=g(x)$ 為可微函數；本題 $f=e^x$、$g=C_1\cos x+C_2\sin x$，且 $(e^x)'=e^x$。

$$
y'=e^x\left[(C_1+C_2)\cos x+(C_2-C_1)\sin x\right]+1.
$$
代 $y'(0)=1$：$C_1+C_2+1=1$，所以 $C_2=0$。

$$
\boxed{y(x)=x.}
$$

## 2021 年 11 月期中第 4 題｜修正規則：共振特解（20 分）

**原題：** Find a particular solution of $y''-2y'+2y=2e^x\cos x$.

**中文：** 求一個二階非齊次方程的特解。

**① 檢查共振：** 特徵方程 $r^2-2r+2=0$ 有根 $1\pm i$，$e^x\cos x$ 已是齊次解，直接猜 $e^x(A\cos x+B\sin x)$ 會重疊。

公式（複根通解）：常係數方程 $ay''+by'+cy=0$ 的特徵方程為 $ar^2+br+c=0$，若其根為 $r=\alpha\pm i\beta$（$\beta\gt0$），則齊次實通解為 $y_h=e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$，其中 $a,b,c$ 為常數係數、$\alpha,\beta$ 為根的實部與虛部、$C_1,C_2$ 為齊次通解常數；本題 $a=1,b=-2,c=2$，$\alpha=1,\beta=1$，故 $e^x\cos x$、$e^x\sin x$ 為齊次解。

**② 修正試探解：** 乘上 $x$。

公式（修正規則）：右側為 $e^{\alpha x}p_n(x)\cos\beta x$ 或 $e^{\alpha x}p_n(x)\sin\beta x$ 時，正常試解為 $e^{\alpha x}[P_n(x)\cos\beta x+Q_n(x)\sin\beta x]$；若 $\alpha+i\beta$ 是 $s$ 重特徵根，整個試解再乘 $x^s$，其中 $p_n$ 為已知 $n$ 次多項式、$P_n,Q_n$ 為係數待定的 $n$ 次多項式、$s$ 為重數（不是根時 $s=0$）；本題 右側 $2e^x\cos x$ 對應 $\alpha=1,\beta=1,n=0$，$1+i$ 是一重特徵根，$s=1$。

$$
y_p=xe^x(A\cos x+B\sin x).
$$

**③ 用乘法規則簡化：** 令 $y_p=e^xv$，$v=x(A\cos x+B\sin x)$。

公式（乘法規則）：$L(D)[e^{ax}v]=e^{ax}L(D+a)v$，其中 $D=d/dx$、$a$ 為常數、$v=v(x)$ 為待求函數、$L(D+a)$ 是把 $L(D)$ 中每個 $D$ 換成 $D+a$ 的算子；本題 $L(D)=D^2-2D+2$、$a=1$，$L(D+1)=(D+1)^2-2(D+1)+2=D^2+1$。

$(D^2-2D+2)[e^xv]=e^x(D^2+1)v$，所以
$$
v''+v=2\cos x.
$$

**④ 微分 $v$ 並比較係數：**

公式（乘積律）：$(fg)'=f'g+fg'$，再微分一次得 $(fg)''=f''g+2f'g'+fg''$，其中 $f=f(x),g=g(x)$ 為二次可微函數；本題 $f=x$、$g=A\cos x+B\sin x$。

$$
v''+v=-2A\sin x+2B\cos x.
$$
比較係數 $-2A=0$、$2B=2$，得 $A=0,B=1$：
$$
\boxed{y_p=xe^x\sin x.}
$$
# 七、冪級數解

## 作業四｜逐步解答（冪級數的指標平移與遞迴式）：共用符號

符號：$x$：自變數；$y=y(x)$：待求函數；$a_n$：冪級數中 $x^n$ 的係數；$n$：非負整數索引；$y_1,y_2$：兩個線性獨立解。

統一設

$$
y=\sum_{n=0}^{\infty}a_nx^n,
$$

則

公式（逐項微分）：$\dfrac{d}{dx}\sum_{n=0}^{\infty}a_nx^n=\sum_{n=1}^{\infty}na_nx^{n-1}=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n$，其中 $a_n$ 為 $x^n$ 的係數、$n$ 為非負整數索引，第二個等號是把 $n-1$ 改記為 $n$ 的指標平移；此處對 $y$ 用一次得 $y'$，對 $y'$ 再用一次（係數換成 $(n+1)a_{n+1}$）得 $y''$。

$$
y'=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n,
$$

$$
y''=\sum_{n=0}^{\infty}(n+2)(n+1)a_{n+2}x^n.
$$

## 作業四第 1 題｜冪級數解：求兩個線性獨立解

**原題：** Solve $y''+x^2y'+xy=0$.

**中文：** 利用冪級數法解此方程，並找兩個線性獨立解。

**① 代入冪級數：** 寫出 $y,y',y''$ 的級數，再把 $x^2y'$、$xy$ 平移成 $x^n$ 的形式，三個級數才能逐項合併。

公式（逐項微分）：$\dfrac{d}{dx}\sum_{n=0}^{\infty}a_nx^n=\sum_{n=1}^{\infty}na_nx^{n-1}=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n$，其中 $a_n$ 為 $x^n$ 的係數、$n$ 為非負整數索引，第二個等號是把 $n-1$ 改記為 $n$ 的指標平移；本題對 $y$ 用一次得 $y'$，對 $y'$ 再用一次得 $y''$。

$$
y=\sum_{n=0}^{\infty}a_nx^n,
\quad
y'=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n,
\quad
y''=\sum_{n=0}^{\infty}(n+2)(n+1)a_{n+2}x^n.
$$

符號：$a_n$：冪級數中 $x^n$ 的係數；$n$：非負整數索引；下文 $k$：另一個索引，$k=n-1$。

對 $x^2y'$：

$$
x^2y'=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^{n+2}.
$$

令 $n+2\to n$，得

公式（指標平移）：$\sum_{n=0}^{\infty}c_nx^{n+m}=\sum_{n=m}^{\infty}c_{n-m}x^n$，其中 $c_n$ 為第 $n$ 項的係數、$m$ 為正整數，做法是把 $n+m$ 改記為 $n$；本題 $c_n=(n+1)a_{n+1}$、$m=2$，故 $c_{n-2}=(n-1)a_{n-1}$；下方 $xy$ 同理取 $c_n=a_n$、$m=1$。

$$
\boxed{x^2y'=\sum_{n=2}^{\infty}(n-1)a_{n-1}x^n}.
$$

另外

$$
xy=\sum_{n=0}^{\infty}a_nx^{n+1}
=\boxed{\sum_{n=1}^{\infty}a_{n-1}x^n}.
$$

代回原方程：

$$
\sum_{n=0}^{\infty}(n+2)(n+1)a_{n+2}x^n
+\sum_{n=2}^{\infty}(n-1)a_{n-1}x^n
+\sum_{n=1}^{\infty}a_{n-1}x^n=0.
$$

**② 比較低次項：** 三個級數起點不同（$n=0,2,1$），$x^0$、$x^1$ 要先單獨處理。

$x^0$ 項：

公式（係數比較）：若 $\sum_{n=0}^{\infty}c_nx^n=0$ 對 $x=0$ 附近所有 $x$ 都成立，則每個 $c_n=0$，其中 $c_n$ 為所有級數合併後 $x^n$ 的總係數；本題取 $n=0,1$ 得低次項條件，一般 $n$ 得下一步的遞迴式。

$$
2a_2=0
\Rightarrow
\boxed{a_2=0}.
$$

$x^1$ 項：

$$
6a_3+a_0=0
\Rightarrow
\boxed{a_3=-\frac16a_0}.
$$

**③ 一般遞迴式：** 對 $n\ge1$ 合併 $x^n$ 的係數並解出 $a_{n+2}$。

$$
(n+2)(n+1)a_{n+2}+(n-1)a_{n-1}+a_{n-1}=0.
$$

所以

$$
(n+2)(n+1)a_{n+2}+na_{n-1}=0,
$$

$$
\boxed{a_{n+2}=-\frac{n}{(n+2)(n+1)}a_{n-1}}.
$$

亦可令 $k=n-1$：

$$
\boxed{a_{k+3}=-\frac{k+1}{(k+3)(k+2)}a_k}.
$$

**④ 第一個解：** 取 $a_0=1,a_1=0$，遞迴式每次跳 3 格，只剩 $a_0,a_3,a_6,\dots$。

$$
a_0=1,\qquad a_1=0,\qquad a_2=0.
$$

$$
a_3=-\frac{1}{3\cdot2}a_0=-\frac16,
$$

$$
a_6=-\frac{4}{6\cdot5}a_3
=-\frac4{30}\left(-\frac16\right)
=\frac1{45}.
$$

$$
\boxed{y_1(x)=1-\frac16x^3+\frac1{45}x^6-\cdots}.
$$

**⑤ 第二個解：** 取 $a_0=0,a_1=1$，只剩 $a_1,a_4,a_7,\dots$。

$$
a_0=0,\qquad a_1=1,\qquad a_2=0.
$$

$$
a_4=-\frac{2}{4\cdot3}a_1=-\frac16,
$$

$$
a_7=-\frac{5}{7\cdot6}a_4
=-\frac5{42}\left(-\frac16\right)
=\frac5{252}.
$$

$$
\boxed{y_2(x)=x-\frac16x^4+\frac5{252}x^7-\cdots}.
$$

**⑥ 說明線性獨立並寫通解：** 用 $x=0$ 的初值算 Wronskian。

公式（Wronskian 判別）：$W(y_1,y_2)(x)=y_1y_2'-y_1'y_2$，若在某點 $x_0$ 有 $W(x_0)\ne0$，則 $y_1,y_2$ 線性獨立，其中 $y_1,y_2$ 為方程的兩個解、$y_1',y_2'$ 為其導數；本題取 $x_0=0$，$W(0)=1\cdot1-0\cdot0=1\ne0$。

$$
y_1(0)=1,\ y_1'(0)=0,
\qquad
y_2(0)=0,\ y_2'(0)=1,
$$

故兩者線性獨立，通解為

$$
\boxed{y=C_1y_1+C_2y_2}.
$$

符號：$C_1,C_2$：任意常數。

## 作業四第 2 題｜冪級數解：依提示取兩組初值

**原題：** Solve $y''+(x^3+1)y'-y=0$.

**中文：** 利用冪級數法解此方程，並依題目提示取兩組 $(a_0,a_1)$ 求兩個線性獨立解。

**① 代入冪級數：** 把方程拆成 $y''+x^3y'+y'-y=0$，只有 $x^3y'$ 需要平移。

公式（逐項微分）：$\dfrac{d}{dx}\sum_{n=0}^{\infty}a_nx^n=\sum_{n=1}^{\infty}na_nx^{n-1}=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n$，其中 $a_n$ 為 $x^n$ 的係數、$n$ 為非負整數索引，第二個等號是把 $n-1$ 改記為 $n$ 的指標平移；本題對 $y$ 用一次得 $y'$，對 $y'$ 再用一次得 $y''$。

$$
y=\sum_{n=0}^{\infty}a_nx^n,
\quad
y'=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n,
\quad
y''=\sum_{n=0}^{\infty}(n+2)(n+1)a_{n+2}x^n.
$$

符號：$y_1,y_2$：兩個線性獨立解（分別取 $a_0=1,a_1=0$ 與 $a_0=0,a_1=1$）。

$$
y''+x^3y'+y'-y=0.
$$

$$
x^3y'=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^{n+3}.
$$

令 $n+3\to n$：

公式（指標平移）：$\sum_{n=0}^{\infty}c_nx^{n+m}=\sum_{n=m}^{\infty}c_{n-m}x^n$，其中 $c_n$ 為第 $n$ 項的係數、$m$ 為正整數，做法是把 $n+m$ 改記為 $n$；本題 $c_n=(n+1)a_{n+1}$、$m=3$，故 $c_{n-3}=(n-2)a_{n-2}$。

$$
\boxed{x^3y'=\sum_{n=3}^{\infty}(n-2)a_{n-2}x^n}.
$$

所以

$$
\sum_{n=0}^{\infty}(n+2)(n+1)a_{n+2}x^n
+\sum_{n=3}^{\infty}(n-2)a_{n-2}x^n
+\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n
-\sum_{n=0}^{\infty}a_nx^n=0.
$$

**② 比較低次項：** $x^3y'$ 從 $x^3$ 才開始，所以 $x^0,x^1,x^2$ 要先分開比較。

$x^0$：

公式（係數比較）：若 $\sum_{n=0}^{\infty}c_nx^n=0$ 對 $x=0$ 附近所有 $x$ 都成立，則每個 $c_n=0$，其中 $c_n$ 為所有級數合併後 $x^n$ 的總係數；本題取 $n=0,1,2$ 得低次項條件，$n\ge3$ 得下一步的遞迴式。

$$
2a_2+a_1-a_0=0
\Rightarrow
\boxed{a_2=\frac{a_0-a_1}{2}}.
$$

$x^1$：

$$
6a_3+2a_2-a_1=0
\Rightarrow
\boxed{a_3=\frac{a_1-2a_2}{6}}.
$$

$x^2$：

$$
12a_4+3a_3-a_2=0
\Rightarrow
\boxed{a_4=\frac{a_2-3a_3}{12}}.
$$

**③ 一般遞迴式：** 對 $n\ge3$ 四個級數都有項，合併後解出 $a_{n+2}$。

$$
(n+2)(n+1)a_{n+2}
+(n-2)a_{n-2}
+(n+1)a_{n+1}
-a_n=0.
$$

$$
\boxed{
a_{n+2}
=
\frac{a_n-(n+1)a_{n+1}-(n-2)a_{n-2}}
{(n+2)(n+1)}
}.
$$

**④ 第一組 $a_0=1,a_1=0$：** 依序代入低次項公式。

$$
a_2=\frac{1-0}{2}=\frac12.
$$

$$
a_3=\frac{0-2(1/2)}6=-\frac16.
$$

$$
a_4=\frac{\frac12-3(-\frac16)}{12}
=\frac{1}{12}.
$$

$$
\boxed{y_1(x)=1+\frac12x^2-\frac16x^3+\frac1{12}x^4-\cdots}.
$$

**⑤ 第二組 $a_0=0,a_1=1$：** 同樣代入。

$$
a_2=\frac{0-1}{2}=-\frac12.
$$

$$
a_3=\frac{1-2(-1/2)}6=\frac13.
$$

$$
a_4=\frac{-\frac12-3(\frac13)}{12}=-\frac18.
$$

$$
\boxed{y_2(x)=x-\frac12x^2+\frac13x^3-\frac18x^4-\cdots}.
$$

**⑥ 說明線性獨立：** 用 $x=0$ 的初值算 Wronskian。

公式（Wronskian 判別）：$W(y_1,y_2)(x)=y_1y_2'-y_1'y_2$，若在某點 $x_0$ 有 $W(x_0)\ne0$，則 $y_1,y_2$ 線性獨立，其中 $y_1,y_2$ 為方程的兩個解、$y_1',y_2'$ 為其導數；本題取 $x_0=0$，$W(0)=1\cdot1-0\cdot0=1\ne0$。

$$
y_1(0)=1,\ y_1'(0)=0,
\qquad
y_2(0)=0,\ y_2'(0)=1,
$$

所以兩解線性獨立。

## 作業四第 3 題｜冪級數解：初值問題

**原題：** Solve $(x-1)y''-xy'+y=0$, with $y(0)=-2$, $y'(0)=6$.

**中文：** 利用冪級數法求滿足給定初始條件的解。

**① 初始條件先決定 $a_0,a_1$：** 冪級數在 $x=0$ 的前兩個係數就是 $y(0)$、$y'(0)$。

$$
y=\sum_{n=0}^{\infty}a_nx^n.
$$

符號：$y(0)$、$y'(0)$：$x=0$ 時的函數值與導數值。

公式（Taylor 係數）：$y=\sum_{n=0}^{\infty}a_nx^n$ 時 $a_n=\dfrac{y^{(n)}(0)}{n!}$，其中 $y^{(n)}(0)$ 為 $y$ 在 $x=0$ 的第 $n$ 階導數、$n!$ 為 $n$ 的階乘（$0!=1$）；本題 $n=0$ 得 $a_0=y(0)$，$n=1$ 得 $a_1=y'(0)$。

$$
y(0)=a_0,
$$

$$
\boxed{a_0=-2}.
$$

公式（逐項微分）：$\dfrac{d}{dx}\sum_{n=0}^{\infty}a_nx^n=\sum_{n=1}^{\infty}na_nx^{n-1}=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n$，其中 $a_n$ 為 $x^n$ 的係數、$n$ 為非負整數索引，第二個等號是把 $n-1$ 改記為 $n$ 的指標平移；本題用一次得 $y'$，再用一次得下文的 $y''$。

$$
y'=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^n,
$$

$$
y'(0)=a_1
\Rightarrow
\boxed{a_1=6}.
$$

**② 改寫原方程：** 把 $(x-1)y''$ 拆開，$xy''$ 與 $xy'$ 各平移一格。

$$
(x-1)y''-xy'+y=0
$$

寫成

$$
xy''-y''-xy'+y=0.
$$

其中

$$
y''=\sum_{n=0}^{\infty}(n+2)(n+1)a_{n+2}x^n.
$$

公式（指標平移）：$\sum_{n=0}^{\infty}c_nx^{n+m}=\sum_{n=m}^{\infty}c_{n-m}x^n$，其中 $c_n$ 為第 $n$ 項的係數、$m$ 為正整數，做法是把 $n+m$ 改記為 $n$；本題 $c_n=(n+2)(n+1)a_{n+2}$、$m=1$，故 $c_{n-1}=(n+1)na_{n+1}$；下方 $xy'$ 同理取 $c_n=(n+1)a_{n+1}$、$m=1$。

$$
xy''
=\sum_{n=0}^{\infty}(n+2)(n+1)a_{n+2}x^{n+1}
=\boxed{\sum_{n=1}^{\infty}n(n+1)a_{n+1}x^n}.
$$

$$
xy'
=\sum_{n=0}^{\infty}(n+1)a_{n+1}x^{n+1}
=\boxed{\sum_{n=1}^{\infty}na_nx^n}.
$$

代回：

$$
\sum_{n=1}^{\infty}n(n+1)a_{n+1}x^n
-\sum_{n=0}^{\infty}(n+2)(n+1)a_{n+2}x^n
-\sum_{n=1}^{\infty}na_nx^n
+\sum_{n=0}^{\infty}a_nx^n
=0.
$$

**③ 比較 $x^0$：** 只有 $-y''$ 與 $y$ 兩個級數有常數項。

公式（係數比較）：若 $\sum_{n=0}^{\infty}c_nx^n=0$ 對 $x=0$ 附近所有 $x$ 都成立，則每個 $c_n=0$，其中 $c_n$ 為所有級數合併後 $x^n$ 的總係數；本題取 $n=0$ 得 $a_2$，$n\ge1$ 得下一步的遞迴式。

$$
-2a_2+a_0=0.
$$

$$
a_2=\frac{a_0}{2}=-1.
$$

$$
\boxed{a_2=-1}.
$$

**④ 一般遞迴式：** 對 $n\ge1$ 合併 $x^n$ 係數，再解出 $a_{n+2}$。

$$
n(n+1)a_{n+1}
-(n+2)(n+1)a_{n+2}
-na_n+a_n=0.
$$

整理：

$$
n(n+1)a_{n+1}
-(n+2)(n+1)a_{n+2}
+(1-n)a_n=0.
$$

移項：

$$
(n+2)(n+1)a_{n+2}
=n(n+1)a_{n+1}-(n-1)a_n.
$$

$$
\boxed{
a_{n+2}
=
\frac{n}{n+2}a_{n+1}
-
\frac{n-1}{(n+2)(n+1)}a_n
}.
$$

**⑤ 算出前幾個係數：** 依序令 $n=1,2$。

令 $n=1$：

$$
a_3
=\frac13a_2-\frac0{6}a_1
=\frac13(-1)
=-\frac13.
$$

$$
\boxed{a_3=-\frac13}.
$$

令 $n=2$：

$$
a_4
=\frac24a_3-\frac1{12}a_2
=\frac12\left(-\frac13\right)-\frac1{12}(-1).
$$

$$
a_4=-\frac16+\frac1{12}=-\frac1{12}.
$$

$$
\boxed{a_4=-\frac1{12}}.
$$

**⑥ 寫出級數解：** 代回係數，並提出 $-2$ 整理成題目附答形式。

$$
y=-2+6x-x^2-\frac13x^3-\frac1{12}x^4-\cdots.
$$

提出 $-2$：

$$
y=-2\left(1+\frac12x^2+\frac16x^3+\frac1{24}x^4+\cdots\right)+6x.
$$

$$
\boxed{
y=-2\left(1+\frac12x^2+\frac16x^3+\cdots\right)+6x
}.
$$

**⑦ 辨認閉式（補充）：** 括號內的係數是 $1/n!$，正好是 $e^x$ 少了 $x$ 項。

公式（指數函數 Maclaurin 級數）：$e^x=\sum_{n=0}^{\infty}\dfrac{x^n}{n!}$，對所有實數 $x$ 收斂，其中 $n!$ 為 $n$ 的階乘（$0!=1$）；本題對照 $\dfrac1{2!}=\dfrac12$、$\dfrac1{3!}=\dfrac16$、$\dfrac1{4!}=\dfrac1{24}$，括號內正是 $e^x$ 少了 $x$ 項。

$$
e^x=1+x+\frac12x^2+\frac16x^3+\frac1{24}x^4+\cdots,
$$

括號內為 $e^x-x$，所以也可寫成

$$
\boxed{y=-2e^x+8x}.
$$

**注意：** 這個閉式是由級數辨認出的補充形式；題目本身列的是冪級數答案。

# 八、Frobenius 法

## 作業五｜共用符號

符號：$x$：自變數；$y,y',y''$：待求函數及其導數；$a_n$：級數係數；$n=0,1,\ldots$：非負整數索引；$r$：Frobenius 指數（不等同常數係數特徵根）。先在 $x>0$ 使用

$$
y=x^r\sum_{n=0}^{\infty}a_nx^n=\sum_{n=0}^{\infty}a_nx^{n+r},\quad a_0\ne0.
$$

求導：

公式（冪次微分）：$\dfrac{d}{dx}x^{s}=s\,x^{s-1}$，其中 $s$ 為實數常數、$x\gt0$；此處對每一項取 $s=n+r$ 得 $y'$，再取 $s=n+r-1$ 得 $y''$。

$$
y'=\sum_{n=0}^{\infty}(n+r)a_nx^{n+r-1},\qquad
y''=\sum_{n=0}^{\infty}(n+r)(n+r-1)a_nx^{n+r-2}.
$$

## 作業五第 1 題｜兩個非整數間距的 indicial roots

**原題：** Solve $2x^2y''+3xy'+(2x-1)y=0$.

**中文：** 使用 Frobenius 法求兩個線性獨立解。

**① 代入級數：** 把方程分成 $2x^2y''+3xy'-y+2xy=0$，前三項同次、$2xy$ 高一次。

公式（Frobenius 代入式）：$xy'=\sum_{n=0}^{\infty}(n+r)a_nx^{n+r}$、$x^2y''=\sum_{n=0}^{\infty}(n+r)(n+r-1)a_nx^{n+r}$，其中 $a_n$ 為級數係數、$r$ 為 Frobenius 指數，由上方共用的 $y',y''$ 分別乘上 $x$、$x^2$ 得到；本題 $2x^2y''+3xy'-y$ 三項因此同為 $x^{n+r}$ 次，$2xy$ 則為 $x^{n+r+1}$ 次。

$$
\sum_{n=0}^{\infty}[2(n+r)(n+r-1)+3(n+r)-1]a_nx^{n+r}
+\sum_{n=0}^{\infty}2a_nx^{n+r+1}=0.
$$

**② 平移第二項：** 令新索引 $k=n+1$（$n=k-1$），讓兩個級數都是 $x^{k+r}$。

公式（指標平移）：$\sum_{n=0}^{\infty}c_nx^{n+r+m}=\sum_{n=m}^{\infty}c_{n-m}x^{n+r}$，其中 $c_n$ 為第 $n$ 項的係數、$m$ 為正整數、$r$ 為 Frobenius 指數；本題 $c_n=2a_n$、$m=1$。

$$
\sum_{k=1}^{\infty}2a_{k-1}x^{k+r}.
$$

**③ 指標方程：** 虛索引改回 $n$，比較最低次 $x^r$ 的係數。

公式（係數比較）：若 $\sum_{n=0}^{\infty}c_nx^{n+s}=0$ 對 $x\gt0$ 附近所有 $x$ 都成立，則每個 $c_n=0$，其中 $c_n$ 為合併後 $x^{n+s}$ 的總係數、$s$ 為固定的冪次偏移；本題 $s=r$，$n=0$ 給下面的 indicial equation，$n\ge1$ 給遞迴式 (F1)。

公式（指標方程）：把方程寫成 $x^2y''+xp(x)y'+q(x)y=0$，則指標方程為 $r(r-1)+p_0r+q_0=0$，其中 $p_0=p(0)$、$q_0=q(0)$ 為 $p(x),q(x)$ 在 $x=0$ 的值、$r$ 為 Frobenius 指數；本題除以 2 得 $p(x)=\dfrac32$、$q(x)=x-\dfrac12$，故 $p_0=\dfrac32$、$q_0=-\dfrac12$，乘回 2 即 $2r(r-1)+3r-1=0$。

$$
[2r(r-1)+3r-1]a_0=0.
$$

符號：$r_1,r_2$：indicial equation（指標方程）的兩根；$s=n+r$：因式分解時的簡寫。

由 $a_0\ne0$：

$$
2r^2+r-1=(2r-1)(r+1)=0.
$$

公式（Frobenius 定理，根差非整數）：若指標方程兩根 $r_1,r_2$ 的差 $r_1-r_2$ 不是整數，則 $x^{r_1}\sum_{n=0}^{\infty}a_nx^n$ 與 $x^{r_2}\sum_{n=0}^{\infty}b_nx^n$（$a_0,b_0\ne0$）都是解且線性獨立，其中 $a_n,b_n$ 由同一遞迴式分別代入 $r=r_1$、$r=r_2$ 求得、$x\gt0$；本題兩根差 $\dfrac12-(-1)=\dfrac32$。

因此 $r_1=-1$、$r_2=1/2$，兩根之差 $3/2$ 不是整數，可以分別用同一遞迴式建兩個解。

**④ 遞迴式：** 對 $n\ge1$ 比較 $x^{n+r}$ 係數。

$$
[2(n+r)(n+r-1)+3(n+r)-1]a_n+2a_{n-1}=0.
$$

使用因式分解 $2s(s-1)+3s-1=(2s-1)(s+1)$，令 $s=n+r$：

$$
\boxed{a_n=-\frac{2a_{n-1}}{\left[2(n+r)-1\right]\,(n+r+1)}.}\tag{F1}
$$

**⑤ 第一根 $r=-1$：** 分母變成 $n(2n-3)$，取標準化 $a_0=1$。

$$
a_n=-\frac{2}{n(2n-3)}a_{n-1}.
$$

$$
a_1=-\frac2{1(-1)}=2,\qquad
a_2=-\frac2{2(1)}(2)=-2,
$$

$$
a_3=-\frac2{3(3)}(-2)=\frac49.
$$

$$
\boxed{y_1(x)=x^{-1}\left(1+2x-2x^2+\frac49x^3+\cdots\right).}
$$

**⑥ 第二根 $r=1/2$：** 分母變成 $n(2n+3)$，取 $a_0=1$。

$$
a_n=-\frac2{n(2n+3)}a_{n-1}.
$$

$$
a_1=-\frac2{1(5)}=-\frac25,
$$

$$
a_2=-\frac2{2(7)}\left(-\frac25\right)=\frac2{35},
$$

$$
a_3=-\frac2{3(9)}\left(\frac2{35}\right)=-\frac4{945}.
$$

$$
\boxed{y_2(x)=\sqrt{x}\left(1-\frac25x+\frac2{35}x^2-\frac4{945}x^3+\cdots\right).}
$$

**⑦ 獨立性與條件：** $y_1\sim x^{-1}$、$y_2\sim x^{1/2}$ 在 $x\to0^+$ 的最低次冪不同，不可能互為常數倍，故在 $x>0$ 是兩個線性獨立的實值解；兩者在 $x=0$ 呈奇異／分數次冪行為，不是原點的普通冪級數解。

## 作業五第 2 題｜指標根差整數：需要對數項

**原題：** Solve $xy''-xy'+y=0$.

**中文：** 在 $x>0$ 求兩個線性獨立解；題目附答是 $y_1=x$，以及 $y_2=x\ln x-1+x^2/2+x^3/12+x^4/72+\cdots$。

**① Frobenius 代入：** 設 $y=\sum_{n=0}^{\infty}a_nx^{n+r}$，把 $xy''$ 與 $-xy'+y$ 分別寫成級數。

公式（Frobenius 代入式）：$xy''=\sum_{n=0}^{\infty}(n+r)(n+r-1)a_nx^{n+r-1}$、$xy'=\sum_{n=0}^{\infty}(n+r)a_nx^{n+r}$，其中 $a_n$ 為級數係數、$r$ 為 Frobenius 指數，由共用的 $y'',y'$ 乘上 $x$ 得到；本題 $-xy'+y$ 合併為 $\sum_{n=0}^{\infty}(1-n-r)a_nx^{n+r}$。

$$
xy''=\sum_{n=0}^{\infty}(n+r)(n+r-1)a_nx^{n+r-1},
$$

$$
-xy'+y=\sum_{n=0}^{\infty}(1-n-r)a_nx^{n+r}.
$$

**② 指標方程：** 第二組平移到 $x^{n+r-1}$，比較最低次 $x^{r-1}$。

公式（指標平移）：$\sum_{n=0}^{\infty}c_nx^{n+r}=\sum_{n=1}^{\infty}c_{n-1}x^{n+r-1}$，其中 $c_n$ 為第 $n$ 項的係數、$r$ 為 Frobenius 指數，做法是把 $n+1$ 改記為 $n$；本題 $c_n=(1-n-r)a_n$，故 $c_{n-1}=(2-n-r)a_{n-1}$，且這組從 $x^{r}$ 才開始。

公式（係數比較）：若 $\sum_{n=0}^{\infty}c_nx^{n+s}=0$ 對 $x\gt0$ 附近所有 $x$ 都成立，則每個 $c_n=0$，其中 $c_n$ 為合併後 $x^{n+s}$ 的總係數、$s$ 為固定的冪次偏移；本題 $s=r-1$，$n=0$ 給 indicial equation，$n\ge1$ 給遞迴式 (F2)。

公式（指標方程）：把方程寫成 $x^2y''+xp(x)y'+q(x)y=0$，則指標方程為 $r(r-1)+p_0r+q_0=0$，其中 $p_0=p(0)$、$q_0=q(0)$ 為 $p(x),q(x)$ 在 $x=0$ 的值、$r$ 為 Frobenius 指數；本題原式乘以 $x$ 得 $x^2y''-x^2y'+xy=0$，即 $p(x)=-x$、$q(x)=x$，故 $p_0=q_0=0$。

$$
r(r-1)=0\quad\Rightarrow\quad r_1=1,\ r_2=0.
$$

**③ 遞迴式與第一解：** 對 $n\ge1$ 比較 $x^{n+r-1}$ 係數，再代 $r=1$。

$$
(n+r)(n+r-1)a_n+(2-n-r)a_{n-1}=0.
$$

$$
\boxed{a_n=\frac{n+r-2}{(n+r)(n+r-1)}a_{n-1}}\tag{F2}
$$

對 $r=1$，令 $n=1$：$a_1=(1+1-2)/(2\cdot1)a_0=0$；後續係數全為零，故

$$
\boxed{y_1=x.}
$$

**④ 較小根 $r=0$ 失效：** 根差為整數，普通級數可能做不出第二解。

公式（Frobenius 定理，根差為正整數）：若指標方程兩根滿足 $r_1-r_2=N$ 為正整數，則 $y_1=x^{r_1}\sum_{n=0}^{\infty}a_nx^n$（$a_0\ne0$），第二解形如 $y_2=Cy_1\ln x+x^{r_2}\sum_{n=0}^{\infty}b_nx^n$（$b_0\ne0$），其中 $C$ 為常數（可能為 0）、$a_n,b_n$ 為級數係數、$x\gt0$；本題 $r_1=1$、$r_2=0$、$N=1$，下面求得的 $y_2$ 對應 $C=1$。

對 $r=0$，令 $n=1$ 代係數方程：$1(0)a_1+(2-1)a_0=0\Rightarrow a_0=0$，與 $a_0\ne0$ 矛盾。所以第二解要帶對數項，改用降階法求。

**⑤ 降階法：** 除以 $x\neq0$ 得 $y''-y'+\frac1x y=0$，故 $P(x)=-1$，已知 $y_1=x$。

$$
y_2=y_1\int\frac{e^{-\int P(x)dx}}{y_1^2}dx
=x\int\frac{e^x}{x^2}dx.
$$

符號：$P(x)$：標準式 $y''+P(x)y'+Q(x)y=0$ 中 $y'$ 的係數。

**⑥ 展開後逐項積分：** 把 $e^x$ 在 $x=0$ 展開，除以 $x^2$ 再積分。

公式（指數函數 Maclaurin 級數）：$e^x=\sum_{n=0}^{\infty}\dfrac{x^n}{n!}$，對所有實數 $x$ 收斂，其中 $n!$ 為 $n$ 的階乘（$0!=1$）；本題用它展開 $e^x$，再逐項除以 $x^2$。

$$
e^x=1+x+\frac{x^2}{2}+\frac{x^3}{6}+\frac{x^4}{24}+\cdots.
$$

$$
\frac{e^x}{x^2}=x^{-2}+x^{-1}+\frac12+\frac{x}{6}+\frac{x^2}{24}+\frac{x^3}{120}+\cdots.
$$

公式（冪函數積分）：$\int x^m\,dx=\dfrac{x^{m+1}}{m+1}+C\ (m\ne-1)$，$\int x^{-1}\,dx=\ln|x|+C$，其中 $m$ 為實數常數、$C$ 為積分常數；本題 $x\gt0$ 故 $\ln|x|=\ln x$，例如 $\int x^{-2}dx=-x^{-1}+C$、$\int\dfrac{x}{6}dx=\dfrac{x^2}{12}+C$。

$$
\int\frac{e^x}{x^2}dx=-x^{-1}+\ln x+\frac{x}{2}+\frac{x^2}{12}+\frac{x^3}{72}+\frac{x^4}{480}+\cdots+C.
$$

**⑦ 第二解與通解：** 乘上外面的 $x$，丟掉只會重複 $y_1=Cx$ 的常數部分。

$$
\boxed{y_2=x\ln x-1+\frac12x^2+\frac1{12}x^3+\frac1{72}x^4+\cdots.}
$$

一般解 $y=C_1x+C_2y_2$。因 $W=y_1^2v'=e^x\neq0$，兩解在 $x>0$ 上線性獨立。

符號：$W$：Wronskian，$W=y_1y_2'-y_1'y_2$；$v$：降階法中 $y_2=vy_1$ 的倍數函數，此題 $v'=e^x/x^2$；$C,C_1,C_2$：任意常數。

**條件：** $x=0$ 是奇異點，$\ln x$ 在實數範圍須 $x>0$；負半軸可改用 $\ln|x|$。

# 九、Fourier 級數：實數、複數 Fourier 與功率頻譜

## 2025 年 10 月期中第 4 題｜Fourier 級數、複數 Fourier 級數與功率頻譜（25 分）

**原題：** Consider the $2\pi$-periodic function $f(t)=t+\pi/2$ for $-\pi<t<0$, and $f(t)=-t+\pi/2$ for $0<t<\pi$. (a) Expand it in a Fourier series. (b) Expand it in a complex Fourier series. (c) Plot the power spectrum for the three lowest-frequency components.

**中文：** 將題目給出的分段週期函數展開成實數、複數 Fourier 級數，並畫最低三個頻率的功率頻譜。

符號：$t$：自變數；$n$：整數諧波索引；$a_0,a_n,b_n$：實 Fourier 係數；$c_n$：複數係數；$i^2=-1$；功率採 $|c_n|^2$（不是 $|c_n|$）。

### (a) 實數 Fourier 級數

**① 看出對稱性：** 原函數等價於 $f(t)=\pi/2-|t|$（$-\pi<t<\pi$），是偶函數，所以 $b_n=0$。

$$
f(t)=\frac{a_0}{2}+\sum_{n=1}^{\infty}[a_n\cos(nt)+b_n\sin(nt)].
$$

**② 常數項 $a_0$：** 偶函數積分只算半區間再乘 2。

公式（Fourier 係數）：週期 $2\pi$ 時 $a_n=\dfrac1\pi\int_{-\pi}^{\pi}f(t)\cos(nt)\,dt\ (n=0,1,2,\dots)$、$b_n=\dfrac1\pi\int_{-\pi}^{\pi}f(t)\sin(nt)\,dt\ (n=1,2,\dots)$，其中 $f(t)$ 為週期 $2\pi$ 的函數、$n$ 為諧波序號，$a_0$ 是 $n=0$ 的情形（級數常數項為 $a_0/2$）；本題 $f(t)=\dfrac\pi2-|t|$。

公式（奇偶函數積分）：若 $g(-t)=g(t)$（偶函數）則 $\int_{-a}^{a}g(t)\,dt=2\int_0^{a}g(t)\,dt$，若 $g(-t)=-g(t)$（奇函數）則 $\int_{-a}^{a}g(t)\,dt=0$，其中 $a\gt0$ 為積分半區間長；本題 $a=\pi$，$f(t)$ 與 $f(t)\cos(nt)$ 為偶函數、$f(t)\sin(nt)$ 為奇函數。

$$
a_0=\frac2\pi\int_0^{\pi}\left(\frac\pi2-t\right)dt
=\frac2\pi\left[\frac{\pi t}{2}-\frac{t^2}{2}\right]_0^\pi=0.
$$

**③ 餘弦係數 $a_n$：** 分部積分，$u=\pi/2-t$、$dv=\cos(nt)dt$，得 $du=-dt$、$v=\sin(nt)/n$。

$$
a_n=\frac2\pi\int_0^\pi\left(\frac\pi2-t\right)\cos(nt)dt.
$$

公式（分部積分）：$\int_a^b u\,dv=\left[uv\right]_a^b-\int_a^b v\,du$，其中 $u,v$ 為積分變數的函數、$du,dv$ 為其微分、$a,b$ 為積分下、上限；本題 $u=\dfrac\pi2-t$、$v=\dfrac{\sin(nt)}n$、$a=0$、$b=\pi$。

公式（標準積分）：$\int\cos(nt)\,dt=\dfrac{\sin(nt)}{n}+C$、$\int\sin(nt)\,dt=-\dfrac{\cos(nt)}{n}+C$，其中 $n\ne0$ 為常數、$C$ 為積分常數；本題用前者求 $v$，用後者算餘項 $\dfrac1n\int_0^\pi\sin(nt)dt$。

$$
\int_0^\pi\left(\frac\pi2-t\right)\cos(nt)dt
=\left[\left(\frac\pi2-t\right)\frac{\sin(nt)}n\right]_0^\pi
+\frac1n\int_0^\pi\sin(nt)dt.
$$

邊界項為零，餘項積分為 $[ -\cos(nt)/n]_0^\pi=(1-(-1)^n)/n$，所以

公式（整數倍角三角值）：$\sin(n\pi)=0$、$\cos(n\pi)=(-1)^n$，其中 $n$ 為整數；本題邊界項因 $\sin(n\pi)=\sin0=0$ 為零，餘項 $\left[-\dfrac{\cos(nt)}{n}\right]_0^\pi=\dfrac{1-(-1)^n}{n}$。

$$
a_n=\frac{2[1-(-1)^n]}{\pi n^2}
=\begin{cases}4/(\pi n^2),&n\text{ 奇數},\\0,&n\text{ 偶數}.\end{cases}
$$

$$
\boxed{f(t)=\frac4\pi\sum_{n=1,3,5,\dots}^{\infty}\frac{\cos(nt)}{n^2}.}
$$

### (b) 複數 Fourier 級數

**① 由實係數換算：** 定義 $f(t)=\sum_{n=-\infty}^{\infty}c_ne^{int}$，$c_n=(2\pi)^{-1}\int_{-\pi}^{\pi}f(t)e^{-int}dt$；偶函數 $b_n=0$，所以 $c_0=a_0/2=0$、非零 $n$ 有 $c_n=a_{|n|}/2$。

公式（實、複 Fourier 係數關係）：由 Euler 公式 $e^{i\theta}=\cos\theta+i\sin\theta$ 得 $c_0=\dfrac{a_0}2$、$c_n=\dfrac{a_n-ib_n}2$、$c_{-n}=\dfrac{a_n+ib_n}2\ (n\ge1)$，其中 $a_n,b_n$ 為實 Fourier 係數、$c_n$ 為複數係數、$\theta$ 為任意實數；本題 $b_n=0$，故 $c_{\pm n}=\dfrac{a_n}2$，即 $c_n=\dfrac{a_{|n|}}2$。

$$
\boxed{c_n=\frac{1-(-1)^n}{\pi n^2}\quad(n\neq0),\qquad c_0=0.}
$$

**② 寫成級數：** 把 $(-1)^n$ 換成 $\cos(n\pi)$。

公式（整數倍角三角值）：$\cos(n\pi)=(-1)^n$，其中 $n$ 為整數；本題用它把 $1-(-1)^n$ 寫成 $1-\cos(n\pi)$。

$$
\boxed{f(t)=\sum_{\substack{n=-\infty\\n\neq0}}^{\infty}\frac{1-\cos(n\pi)}{\pi n^2}e^{int}.}
$$

### (c) 功率頻譜

**① 列出 $|c_n|^2$：** 最低三個正頻率如下（負頻率對稱）。

| 頻率索引 $n$ | $c_n$ | $|c_n|^2$ |
|---:|---:|---:|
| 1 | $2/\pi$ | $4/\pi^2$ |
| 2 | $0$ | $0$ |
| 3 | $2/(9\pi)$ | $4/(81\pi^2)$ |

**② 畫圖：** 橫軸取離散的 $n=\pm1,\pm2,\pm3$，縱軸 $|c_n|^2$：$\pm1$ 柱高 $4/\pi^2$、$\pm2$ 為零、$\pm3$ 為 $4/(81\pi^2)$；$n=0$ 的 DC 為零。

符號：DC：直流分量，即 $n=0$ 的常數項 $c_0$；$\pm n$：正、負頻率索引。

**注意：** 原卷附答印成 $|c_1|^2=4/\pi$、$|c_3|^2=4/(9\pi)$，與同頁的 $c_n=(1-\cos n\pi)/(n^2\pi)$ 不一致；照 $|c_n|^2$ 的定義平方，正確值是上表。

## 2023 年 11 月期中第 4 題｜Fourier 級數（6 分）

**原題：** Let $f(t)=t$ for $-\pi\le t\le\pi$, with $f(t+2\pi)=f(t)$. Find its Fourier series.

**中文：** 將鋸齒型週期函數 $f(t)=t$ 展開成 Fourier 級數。

符號：$a_n$：餘弦係數；$b_n$：正弦係數，$n=1,2,\ldots$。

**① 看出對稱性：** $f(t)=t$ 是奇函數，所以 $a_0=a_n=0$，只需算 $b_n$。

公式（Fourier 係數）：週期 $2\pi$ 時 $a_n=\dfrac1\pi\int_{-\pi}^{\pi}f(t)\cos(nt)\,dt\ (n=0,1,2,\dots)$、$b_n=\dfrac1\pi\int_{-\pi}^{\pi}f(t)\sin(nt)\,dt\ (n=1,2,\dots)$，其中 $f(t)$ 為週期 $2\pi$ 的函數、$n$ 為諧波序號，$a_0$ 是 $n=0$ 的情形（級數常數項為 $a_0/2$）；本題 $f(t)=t$。

公式（奇偶函數積分）：若 $g(-t)=g(t)$（偶函數）則 $\int_{-a}^{a}g(t)\,dt=2\int_0^{a}g(t)\,dt$，若 $g(-t)=-g(t)$（奇函數）則 $\int_{-a}^{a}g(t)\,dt=0$，其中 $a\gt0$ 為積分半區間長；本題 $a=\pi$，$t$ 與 $t\cos(nt)$ 為奇函數（故 $a_0=a_n=0$）、$t\sin(nt)$ 為偶函數。

$$
b_n=\frac1\pi\int_{-\pi}^{\pi}t\sin(nt)dt
=\frac2\pi\int_0^\pi t\sin(nt)dt.
$$

**② 分部積分求 $b_n$：** 令 $u=t$、$dv=\sin(nt)dt$，則 $du=dt$、$v=-\cos(nt)/n$。

公式（分部積分）：$\int_a^b u\,dv=\left[uv\right]_a^b-\int_a^b v\,du$，其中 $u,v$ 為積分變數的函數、$du,dv$ 為其微分、$a,b$ 為積分下、上限；本題 $u=t$、$v=-\dfrac{\cos(nt)}n$、$a=0$、$b=\pi$。

公式（標準積分）：$\int\cos(nt)\,dt=\dfrac{\sin(nt)}{n}+C$、$\int\sin(nt)\,dt=-\dfrac{\cos(nt)}{n}+C$，其中 $n\ne0$ 為常數、$C$ 為積分常數；本題用後者求 $v$，用前者算餘項 $\dfrac1n\int_0^\pi\cos(nt)dt$。

公式（整數倍角三角值）：$\sin(n\pi)=0$、$\cos(n\pi)=(-1)^n$，其中 $n$ 為整數；本題上限代入得 $-\dfrac{\pi\cos(n\pi)}{n}=-\dfrac{\pi(-1)^n}{n}$，而 $\sin(n\pi)=\sin0=0$ 使第二項為零。

$$
\int_0^\pi t\sin(nt)dt
=\left[-\frac{t\cos(nt)}n\right]_0^\pi
+\frac1n\left[\frac{\sin(nt)}n\right]_0^\pi
=-\frac{\pi(-1)^n}{n}.
$$

**③ 寫出級數：** $b_n=2(-1)^{n+1}/n$。

$$
\boxed{f(t)=2\sum_{n=1}^\infty\frac{(-1)^{n+1}}{n}\sin(nt),\qquad -\pi<t<\pi.}
$$

**④ 端點收斂值：** 週期延拓在 $t=\pm\pi$ 有跳躍。

公式（Dirichlet 收斂定理）：$f$ 分段平滑時，Fourier 級數在 $t_0$ 收斂到 $\dfrac{f(t_0^+)+f(t_0^-)}{2}$，其中 $f(t_0^+)$、$f(t_0^-)$ 為週期延拓後在 $t_0$ 的右、左極限，連續點即等於 $f(t_0)$；本題 $t_0=\pi$ 時 $f(\pi^-)=\pi$、$f(\pi^+)=f(-\pi^+)=-\pi$，平均為 $0$。

**條件：** 級數在 $t=\pm\pi$ 收斂到左右極限平均 $0$，不是 $\pm\pi$。

## 2022 年 11 月期中第 4 題｜Fourier、複數 Fourier 與功率頻譜（4+4+2 分）

**原題：** Let $f(t)=1+t$, $-\pi\le t\le\pi$, with period $2\pi$. (1) Expand in a Fourier series. (2) Expand in a complex Fourier series. (3) Plot the power spectrum.

**中文：** 將 $1+t$ 作週期延拓，求實 Fourier、複數 Fourier 係數及頻譜。

符號：$a_n,b_n$：餘弦、正弦係數；$c_n$：複數係數；$n$：整數諧波序號。

### (1) 實 Fourier 級數

**① 拆成偶＋奇：** $f$ 由偶函數常數 $1$ 與奇函數 $t$ 組成，$1$ 只貢獻 $a_0$，$t$ 只貢獻 $b_n$。

公式（Fourier 係數）：週期 $2\pi$ 時 $a_n=\dfrac1\pi\int_{-\pi}^{\pi}f(t)\cos(nt)\,dt\ (n=0,1,2,\dots)$、$b_n=\dfrac1\pi\int_{-\pi}^{\pi}f(t)\sin(nt)\,dt\ (n=1,2,\dots)$，其中 $f(t)$ 為週期 $2\pi$ 的函數、$n$ 為諧波序號，$a_0$ 是 $n=0$ 的情形（級數常數項為 $a_0/2$）；本題 $f(t)=1+t$。

公式（奇偶函數積分）：若 $g(-t)=g(t)$（偶函數）則 $\int_{-a}^{a}g(t)\,dt=2\int_0^{a}g(t)\,dt$，若 $g(-t)=-g(t)$（奇函數）則 $\int_{-a}^{a}g(t)\,dt=0$，其中 $a\gt0$ 為積分半區間長；本題 $a=\pi$，$t$、$t\cos nt$、$\sin nt$ 為奇函數，$1$、$\cos nt$、$t\sin nt$ 為偶函數（且 $n\ge1$ 時 $\int_0^\pi\cos nt\,dt=0$）。

$$
a_0=\frac1\pi\int_{-\pi}^{\pi}(1+t)dt=2,
\quad a_n=\frac1\pi\int_{-\pi}^{\pi}(1+t)\cos nt\,dt=0.
$$

**② 分部積分求 $b_n$：** 只剩 $t\sin nt$ 這一項。

$$
b_n=\frac1\pi\int_{-\pi}^{\pi}(1+t)\sin nt\,dt
=\frac2\pi\int_0^\pi t\sin nt\,dt.
$$

公式（分部積分）：$\int_a^b u\,dv=\left[uv\right]_a^b-\int_a^b v\,du$，其中 $u,v$ 為積分變數的函數、$du,dv$ 為其微分、$a,b$ 為積分下、上限；本題 $u=t$、$v=-\dfrac{\cos nt}{n}$、$a=0$、$b=\pi$。

公式（標準積分）：$\int\cos nt\,dt=\dfrac{\sin nt}{n}+C$、$\int\sin nt\,dt=-\dfrac{\cos nt}{n}+C$，其中 $n\ne0$ 為常數、$C$ 為積分常數；本題用後者求 $v$，用前者算 $-\int v\,du$ 得 $\dfrac{\sin nt}{n^2}$ 項。

公式（整數倍角三角值）：$\sin(n\pi)=0$、$\cos(n\pi)=(-1)^n$，其中 $n$ 為整數；本題上限 $\pi$ 代入得 $-\dfrac{\pi(-1)^n}{n}$，下限 $0$ 兩項皆為零。

$$
\int_0^\pi t\sin nt\,dt=\left[-\frac{t\cos nt}{n}+\frac{\sin nt}{n^2}\right]_0^\pi=-\frac{\pi(-1)^n}{n}.
$$

**③ 寫出級數：** $b_n=2(-1)^{n+1}/n$，常數項 $a_0/2=1$。

$$
\boxed{f(t)=1+2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}n\sin nt,\quad -\pi<t<\pi.}
$$

### (2) 複數 Fourier 級數

**① 由實係數換算：** 定義 $f(t)=\sum_{n\in\mathbb Z}c_ne^{int}$，則 $c_0=a_0/2=1$；$n>0$ 時用 $c_n=(a_n-ib_n)/2$。

$$
c_n=-i\frac{(-1)^{n+1}}n=i\frac{(-1)^n}{n}\quad(n>0).
$$

符號：$\mathbb Z$：全體整數；$i$：虛數單位（$i^2=-1$）；$\overline{c_n}$：$c_n$ 的共軛複數。

**② 負頻率：** 實值函數滿足 $c_{-n}=\overline{c_n}$，同一式 $c_n=i(-1)^n/n$ 對 $n<0$ 仍成立。

$$
\boxed{f(t)=1+\sum_{\substack{n=-\infty\\n\ne0}}^{\infty}\frac{i(-1)^n}{n}e^{int}.}
$$

### (3) 功率頻譜

**① 取模平方：** $c_n$ 是純虛數，$|i(-1)^n/n|^2=1/n^2$。

公式（複數模平方）：$|z|^2=z\bar z=x^2+y^2$，其中 $z=x+iy$ 為複數、$x,y$ 為其實部與虛部、$\bar z$ 為共軛複數；本題 $z=c_n=\dfrac{i(-1)^n}{n}$ 實部為 0、虛部為 $\dfrac{(-1)^n}{n}$，又 $c_0=1$。

$$
\boxed{|c_0|^2=1,\qquad |c_n|^2=\frac1{n^2}\quad(n\neq0).}
$$

**② 畫圖：** $n=\pm1$ 為 1、$\pm2$ 為 $1/4$、$\pm3$ 為 $1/9$，是對稱的離散梳狀頻譜，每個諧波畫一根柱；本題用雙側 $|c_n|^2$（若畫單側譜要註明是否把 $n,-n$ 合併）。

**③ 端點收斂值：** 週期延拓在 $t=\pm\pi$ 有跳躍。

公式（Dirichlet 收斂定理）：$f$ 分段平滑時，Fourier 級數在 $t_0$ 收斂到 $\dfrac{f(t_0^+)+f(t_0^-)}{2}$，其中 $f(t_0^+)$、$f(t_0^-)$ 為週期延拓後在 $t_0$ 的右、左極限，連續點即等於 $f(t_0)$；本題 $t_0=\pi$ 時 $f(\pi^-)=1+\pi$、$f(\pi^+)=f(-\pi^+)=1-\pi$，平均為 $1$。

**條件：** 級數在 $t=\pm\pi$ 收斂到左右平均值 1。

## 2021 年 11 月期中第 5 題｜週期二次函數的 Fourier 級數（20 分）

**原題：** Find the Fourier series of the periodic function $f(x)=(x-1)(x-3)$ for $1\le x\le3$, with $f(x+2)=f(x)$.

**中文：** 求週期為 2、基本區間 $[1,3]$ 的二次函數的 Fourier 級數。

**① 中心化：** 令 $u=x-2$，則 $-1\le u\le1$ 且 $f=u^2-1$ 是偶函數；半週期 $L=1$，基底為 $\cos(n\pi u)$，$b_n=0$。

$$
f(u)=\frac{a_0}2+\sum_{n=1}^\infty[a_n\cos(n\pi u)+b_n\sin(n\pi u)].
$$

符號：$a_0$：常數項係數（級數常數項是 $a_0/2$）；$a_n$：餘弦係數；$b_n$：正弦係數；$n=1,2,\ldots$：諧波序號。

**② 常數項 $a_0$：** 偶函數只積半區間再乘 2。

公式（Fourier 係數）：週期 $2L$ 時 $a_n=\dfrac1L\int_{-L}^{L}f(u)\cos\dfrac{n\pi u}{L}\,du\ (n=0,1,2,\dots)$、$b_n=\dfrac1L\int_{-L}^{L}f(u)\sin\dfrac{n\pi u}{L}\,du\ (n=1,2,\dots)$，其中 $L$ 為半週期、$f(u)$ 為週期 $2L$ 的函數、$n$ 為諧波序號；本題 $L=1$、$f(u)=u^2-1$。

公式（奇偶函數積分）：若 $g(-u)=g(u)$（偶函數）則 $\int_{-a}^{a}g(u)\,du=2\int_0^{a}g(u)\,du$，若 $g(-u)=-g(u)$（奇函數）則 $\int_{-a}^{a}g(u)\,du=0$，其中 $a\gt0$ 為積分半區間長；本題 $a=1$，$u^2-1$ 與 $(u^2-1)\cos(n\pi u)$ 為偶函數、$(u^2-1)\sin(n\pi u)$ 為奇函數。

$$
a_0=\int_{-1}^{1}(u^2-1)du
=2\left[\frac{u^3}{3}-u\right]_0^1=-\frac43,
\qquad \frac{a_0}{2}=-\frac23.
$$

**③ 第一次分部積分：** 令 $\omega=n\pi$，取 $U=u^2-1$、$dV=\cos(\omega u)du$；邊界項 $[(u^2-1)\sin(\omega u)/\omega]_0^1=0$。

$$
a_n=2\int_0^1(u^2-1)\cos(n\pi u)du.
$$

公式（分部積分）：$\int_a^b U\,dV=\left[UV\right]_a^b-\int_a^b V\,dU$，其中 $U,V$ 為 $u$ 的函數、$dU,dV$ 為其微分、$a,b$ 為積分下、上限；本題第一次取 $U=u^2-1$、$V=\dfrac{\sin(\omega u)}{\omega}$、$dU=2u\,du$、$a=0$、$b=1$。

公式（標準積分）：$\int\cos(\omega u)\,du=\dfrac{\sin(\omega u)}{\omega}+C$、$\int\sin(\omega u)\,du=-\dfrac{\cos(\omega u)}{\omega}+C$，其中 $\omega\ne0$ 為常數、$C$ 為積分常數；本題 $\omega=n\pi$，前者用於第一次求 $V$，兩者都用於第二次分部積分。

$$
a_n=-\frac4\omega\int_0^1u\sin(\omega u)du.
$$

**④ 第二次分部積分：** 對 $u\sin(\omega u)$ 再做一次。

公式（整數倍角三角值）：$\sin(n\pi)=0$、$\cos(n\pi)=(-1)^n$，其中 $n$ 為整數；本題 $\omega=n\pi$，上限代入得 $-\dfrac{\cos(n\pi)}{n\pi}+\dfrac{\sin(n\pi)}{(n\pi)^2}=-\dfrac{(-1)^n}{\omega}$。

$$
\int_0^1u\sin(\omega u)du
=\left[-\frac{u\cos(\omega u)}\omega+\frac{\sin(\omega u)}{\omega^2}\right]_0^1
=-\frac{(-1)^n}{\omega}.
$$

因此

$$
a_n=\frac{4(-1)^n}{n^2\pi^2}.
$$

**⑤ 寫出級數：** 代回 $u=x-2$。

$$
\boxed{f(x)=-\frac23+\frac4{\pi^2}\sum_{n=1}^\infty\frac{(-1)^n}{n^2}\cos[n\pi(x-2)].}
$$

再用 $\cos[n\pi(x-2)]=\cos(n\pi x)$ 化簡：

公式（餘弦週期性）：$\cos(\theta-2k\pi)=\cos\theta$，其中 $\theta$ 為任意角、$k$ 為整數；本題 $\theta=n\pi x$、$k=n$，因 $n\pi(x-2)=n\pi x-2n\pi$。

$$
\boxed{f(x)=-\frac23+\frac4{\pi^2}\sum_{n=1}^\infty\frac{(-1)^n}{n^2}\cos(n\pi x).}
$$

**⑥ 收斂性：** 兩端值相同，延拓後沒有跳躍。

公式（Dirichlet 收斂定理）：$f$ 分段平滑時，Fourier 級數在 $x_0$ 收斂到 $\dfrac{f(x_0^+)+f(x_0^-)}{2}$，其中 $f(x_0^+)$、$f(x_0^-)$ 為週期延拓後在 $x_0$ 的右、左極限，連續點即等於 $f(x_0)$；本題 $f(1)=f(3)=0$ 使週期延拓處處連續，故級數在每點收斂到 $f(x)$。

**條件：** $f(1)=f(3)=0$，週期延拓連續，級數在每點收斂到 $f$。
