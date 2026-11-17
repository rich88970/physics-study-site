<!-- 力學公式表的來源。改完執行 python tools/build_mechanics_formulas.py，格式見該檔開頭。 -->
<p class="lead">力學 Lecture 1、2 用到的公式，依主題整理成十節。每條公式附一兩句說明：它在說什麼、什麼條件下能用、考試常怎麼用錯。右上角的「L1 §4.1」連回講義那一段，可以看完整推導和例題。</p>

<div class="box idea exam-style">
  <span class="box-title">怎麼用這一章</span>
  <p>前四節是 Lecture 1 的數學工具（向量、旋轉矩陣、曲線座標、梯度散度旋度），後六節是 Lecture 2 的牛頓力學（解運動方程、阻力、拋體、守恆律、平衡）。寫題目卡住時，先找「這題要的量」對應哪一條；說明裡的「條件」一定要對過一遍，例如 $\vec F=-\nabla U$ 只對保守力成立、$R=v_0^2\sin2\theta/g$ 只對起點終點同高成立。只想快速複習的話，兩章各自的「考前衝刺」頁有一頁式的必背公式：<a data-chapter="mechanics/ch01" href="#ex-formulas">Lecture 1 必背公式</a>、<a data-chapter="mechanics/ch02" href="#c2x-formulas">Lecture 2 必背公式</a>。</p>
</div>

<p class="small muted">記號照講義：向量用箭頭 $\vec F$（課本用粗體），點表示對時間微分 $\dot x=\mathrm dx/\mathrm dt$；Lecture 1 的位能寫 $V$ 或 $\phi$，Lecture 2 寫 $U$；動能寫 $T$、力矩寫 $\vec N$。</p>

<div data-section-list></div>

# s01 | 01-calculus-vectors.html | 微積分與向量運算 | Lecture 1 §1–5、§7 | 微分與積分的基本式、向量分量與長度、內積、外積、三重積、$\varepsilon_{ijk}$、向量的微分。

## 1.1 微分與積分 {#fx-calc}

### 微分的寫法 | ch01#c-differential
$$\mathrm df=f'(x)\,\mathrm dx,\qquad \mathrm dx^n=nx^{n-1}\,\mathrm dx,\qquad \mathrm d\sin x=\cos x\,\mathrm dx,\qquad \mathrm de^x=e^x\,\mathrm dx$$

講義習慣把導數寫成「微分」：$\mathrm df$ 是 $x$ 變一點點 $\mathrm dx$ 時 $f$ 跟著變的量。這種寫法在解運動方程時最好用，因為可以把 $\mathrm dv$、$\mathrm dt$ 分到等號兩邊再積分。

### 積分＝把微分表倒過來讀 | ch01#c-integral
$$\int x^n\,\mathrm dx=\frac{x^{n+1}}{n+1}+C\ (n\neq-1),\qquad \int\frac{\mathrm dx}{x}=\ln x+C,\qquad \int e^x\,\mathrm dx=e^x+C$$

$n=-1$ 是唯一不能用冪次公式的情況，答案是 $\ln$；阻力題裡 $\int\mathrm dv/v$、$\int\mathrm dv/(g+kv)$ 都屬於這一型。不定積分記得加常數 $C$，再用初始條件定它。

### 點記號 | ch01#c-dot
$$\dot x=\frac{\mathrm dx}{\mathrm dt}\iff\mathrm dx=\dot x\,\mathrm dt,\qquad \ddot x=\frac{\mathrm d\dot x}{\mathrm dt}$$

上面一點是速度、兩點是加速度，只用在「對時間」微分；對位置微分要寫 $\mathrm d/\mathrm dx$ 或 $'$。

### 乘積律、商數律 | ch01#c-product
$$\mathrm d(fg)=g\,\mathrm df+f\,\mathrm dg,\qquad \mathrm d\!\left(\frac fg\right)=\frac{g\,\mathrm df-f\,\mathrm dg}{g^2}$$

倒過來用就是分部積分：$\int f\,\mathrm dg=fg-\int g\,\mathrm df$，例如 $\int xe^x\,\mathrm dx=xe^x-e^x+C$（指數阻力的停止距離會用到）。

### 換元積分 | ch01#c-subst
$$\int f(kx+b)\,\mathrm dx=\frac1k\int f(y)\,\mathrm dy,\qquad y=kx+b$$

括號裡是一次式時，把整個括號當新變數，前面補 $1/k$。常見的錯是忘了 $1/k$，例如 $\int e^{-kt}\,\mathrm dt=-\tfrac1ke^{-kt}$。

## 1.2 向量的分量與長度 {#fx-vec}

### 分量、長度與單位向量 | ch01#sv-3d, ch01#sv-unit
$$\vec A=A_1\hat i+A_2\hat j+A_3\hat k,\qquad |\vec A|=\sqrt{A_1^2+A_2^2+A_3^2},\qquad \hat A=\frac{\vec A}{|\vec A|}$$

向量＝大小＋方向；單位向量只留方向（長度 1）。題目說「沿某方向的單位向量」就是把那個向量除以自己的長度。

### 二維的極座標表示 | ch01#sv-2d
$$A_1=r\cos\theta,\quad A_2=r\sin\theta;\qquad r=\sqrt{A_1^2+A_2^2},\quad \tan\theta=\frac{A_2}{A_1}$$

由分量求角度時，$\tan^{-1}$ 只給 $-90^\circ$ 到 $90^\circ$，要看 $A_1$、$A_2$ 的正負判斷象限。

### 加減與純量乘法 | ch01#va-comp, ch01#va-scale
$$\vec A\pm\vec B=(A_1\pm B_1,\ A_2\pm B_2,\ A_3\pm B_3),\qquad |c\vec A|=|c|\,|\vec A|$$

分量各自加減。乘上負數會反向，長度乘 $|c|$ 而不是 $c$。

## 1.3 內積 {#fx-dot}

### 內積的兩種算法 | ch01#dot-def
$$\vec A\cdot\vec B=A_1B_1+A_2B_2+A_3B_3=|\vec A|\,|\vec B|\cos\theta$$

結果是純量。左邊用分量算、右邊用夾角算，兩個一起用就能求夾角或求分量。$\vec A\cdot\vec A=|\vec A|^2$。

符號：$\theta$＝兩向量夾角（$0\le\theta\le\pi$）。

### 投影（沿某方向的分量） | ch01#dot-proj
$$A_B=\vec A\cdot\hat B=\frac{\vec A\cdot\vec B}{|\vec B|}$$

$\vec A$ 在 $\vec B$ 方向上「有多長」。斜面上重力沿斜面的分量 $mg\sin\theta$ 就是這樣來的（$\vec F_g\cdot\hat x$）。

### 夾角與垂直 | ch01#dot-angle, ch01#dot-orth
$$\cos\theta=\frac{\vec A\cdot\vec B}{|\vec A|\,|\vec B|},\qquad \vec A\perp\vec B\iff\vec A\cdot\vec B=0$$

判斷垂直不用算角度，內積為零就是垂直（兩向量都不是零向量時）。

## 1.4 外積與三重積 {#fx-cross}

### 外積的大小與方向 | ch01#cr-def
$$|\vec A\times\vec B|=|\vec A|\,|\vec B|\sin\theta,\qquad \vec A\times\vec B=-\vec B\times\vec A$$

結果是向量，方向用右手定則（四指從 $\vec A$ 轉向 $\vec B$，拇指方向），同時垂直 $\vec A$ 和 $\vec B$。大小＝兩向量張成的平行四邊形面積；三角形面積再除以 2。次序對調會變號。

### 外積的分量（行列式） | ch01#cr-comp
$$\vec A\times\vec B=\begin{vmatrix}\hat i&\hat j&\hat k\\ A_1&A_2&A_3\\ B_1&B_2&B_3\end{vmatrix}=\begin{pmatrix}A_2B_3-A_3B_2\\ A_3B_1-A_1B_3\\ A_1B_2-A_2B_1\end{pmatrix}$$

中間 $\hat j$ 那一項最容易漏負號；寫成 $A_3B_1-A_1B_3$ 的循環形式就不會錯（下標 $1\to2\to3\to1$ 輪換）。$\hat i\times\hat j=\hat k$，$\hat j\times\hat k=\hat i$，$\hat k\times\hat i=\hat j$。

### $\varepsilon_{ijk}$ 記號 | ch01#cr-eps
$$(\vec A\times\vec B)_i=\sum_{j,k}\varepsilon_{ijk}A_jB_k,\qquad \sum_k\varepsilon_{ijk}\varepsilon_{lmk}=\delta_{il}\delta_{jm}-\delta_{im}\delta_{jl}$$

$\varepsilon_{ijk}$：$ijk$ 是 123 的偶排列為 $+1$、奇排列為 $-1$、有重複下標為 $0$。證明向量恆等式（例如 $\vec A\times(\vec B\times\vec C)$）時用右邊的縮併公式最快。

符號：$\delta_{ij}$＝Kronecker delta，$i=j$ 時為 1，否則為 0。

### 純量三重積 | ch01#cr-proof
$$\vec A\cdot(\vec B\times\vec C)=\begin{vmatrix}A_1&A_2&A_3\\ B_1&B_2&B_3\\ C_1&C_2&C_3\end{vmatrix}=\vec B\cdot(\vec C\times\vec A)=\vec C\cdot(\vec A\times\vec B)$$

三個向量張成的平行六面體的有號體積；循環輪換不變，對調兩個會變號。等於零 ⟺ 三向量共面。

### 向量三重積（BAC−CAB） | ch01#cr-proof
$$\vec A\times(\vec B\times\vec C)=\vec B(\vec A\cdot\vec C)-\vec C(\vec A\cdot\vec B)$$

口訣「BAC 減 CAB」。外積沒有結合律：$(\vec A\times\vec B)\times\vec C\neq\vec A\times(\vec B\times\vec C)$。角動量 $\vec r\times(\vec\omega\times\vec r)$ 就用這條展開。

## 1.5 向量的微分 {#fx-dvec}

### 逐分量微分與乘積律 | ch01#dv-what, ch01#dv-rules
$$\frac{\mathrm d}{\mathrm dt}(\vec A\cdot\vec B)=\dot{\vec A}\cdot\vec B+\vec A\cdot\dot{\vec B},\qquad \frac{\mathrm d}{\mathrm dt}(\vec A\times\vec B)=\dot{\vec A}\times\vec B+\vec A\times\dot{\vec B}$$

直角座標的 $\hat i,\hat j,\hat k$ 不隨時間變，所以向量的導數就是各分量分別微分。外積的乘積律**次序不能換**。

### 長度固定的向量 | ch01#dv-rules
$$|\vec A|=\text{常數}\ \Longrightarrow\ \vec A\cdot\dot{\vec A}=0$$

長度不變的向量只能轉向，變化量一定垂直它自己。等速率圓周運動的加速度垂直速度、極座標的 $\dot{\hat r}\perp\hat r$ 都是這個原因。

# s02 | 02-angular-rotation.html | 角速度、矩陣與座標旋轉 | Lecture 1 §6、§8、§9 | $\vec v=\vec\omega\times\vec r$、矩陣乘法與行列式、二維與三維旋轉矩陣、正交條件、連續旋轉的次序。

## 2.1 角速度 {#fx-omega}

### 角速度與線速度 | ch01#ang-scalar
$$\omega=\dot\theta,\qquad v=R\omega$$

$R$ 是到轉軸的距離（不是到原點的距離），$\theta$ 用弧度。

### 角速度向量 | ch01#ang-vector
$$\vec v=\vec\omega\times\vec r,\qquad v=r\omega\sin\alpha$$

$\vec\omega$ 沿轉軸、方向用右手定則（四指沿轉動方向，拇指指 $\vec\omega$）。次序是 $\vec\omega\times\vec r$，寫反會差一個負號。$r\sin\alpha$ 就是到轉軸的距離 $R$。

符號：$\alpha$＝$\vec r$ 與轉軸的夾角。

## 2.2 矩陣 {#fx-matrix}

### 矩陣乘法 | ch01#mx-mult, ch01#mx-noncomm
$$(AB)_{ij}=\sum_kA_{ik}B_{kj},\qquad AB\neq BA\ \text{（一般而言）}$$

第 $i$ 列乘第 $j$ 行。$A$ 的行數要等於 $B$ 的列數才能乘；$(m\times n)(n\times p)=(m\times p)$。

### 轉置、反矩陣、行列式 | ch01#mx-tm
$$(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T},\qquad (AB)^{-1}=B^{-1}A^{-1},\qquad \det(AB)=\det A\,\det B$$

轉置和反矩陣都會讓次序顛倒。三階行列式沿第一列展開：$a(ei-fh)-b(di-fg)+c(dh-eg)$。

## 2.3 座標旋轉 {#fx-rot}

### 二維旋轉矩陣 | ch01#rot-2d
$$\begin{bmatrix}x'\\y'\end{bmatrix}=\begin{bmatrix}\cos\theta&\sin\theta\\-\sin\theta&\cos\theta\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix}$$

這是「座標軸逆時針轉 $\theta$」後，同一個點的新座標（點沒動、軸在動）。若是點本身轉 $\theta$，$\sin$ 的正負號對調。

### 三維：繞單一軸旋轉 | ch01#rot-3d
$$\lambda_z=\begin{bmatrix}\cos\theta&\sin\theta&0\\-\sin\theta&\cos\theta&0\\0&0&1\end{bmatrix},\qquad \lambda_x=\begin{bmatrix}1&0&0\\0&\cos\theta&\sin\theta\\0&-\sin\theta&\cos\theta\end{bmatrix}$$

$$\lambda_y=\begin{bmatrix}\cos\theta&0&-\sin\theta\\0&1&0\\\sin\theta&0&\cos\theta\end{bmatrix}$$

繞哪一軸，那一軸的座標不變（對應的列與行是 1、0）。$\lambda_y$ 的 $\sin$ 正負位置和另外兩個相反，因為 $z\to x$ 才是右手循環的次序。

### 旋轉矩陣的意義 | ch01#rot-proof
$$x_i'=\sum_j\lambda_{ij}x_j,\qquad \lambda_{ij}=\cos(x_i',x_j)=\hat x_i'\cdot\hat x_j$$

第 $i$ 列就是新軸 $\hat x_i'$ 在舊座標裡的分量（方向餘弦）。求旋轉矩陣時，把每個新軸寫成舊軸的組合，照列填進去即可。

### 正交條件 | ch01#rot-proof
$$\lambda^{\mathsf T}\lambda=I\iff\sum_i\lambda_{ij}\lambda_{ik}=\delta_{jk},\qquad \lambda^{-1}=\lambda^{\mathsf T},\qquad \det\lambda=\pm1$$

旋轉不改變長度和夾角，所以各列（各行）互相垂直且長度 1。轉回去的矩陣就是轉置，不用算反矩陣。$\det=+1$ 是真正的旋轉，$-1$ 含鏡射（左右手座標互換）。

### 連續旋轉的次序 | ch01#rot-tbex
$$\text{先 }\lambda_1\text{ 再 }\lambda_2:\qquad \vec x''=\lambda_2\lambda_1\,\vec x$$

後做的寫在左邊。有限角度的旋轉一般不可交換（$\lambda_2\lambda_1\neq\lambda_1\lambda_2$），所以有限旋轉不是向量；無限小旋轉才可交換。

# s03 | 03-coordinates.html | 曲線座標：極、柱、球 | Lecture 1 §10–11 | 單位向量隨時間的變化、極座標的速度與加速度、線元素、面積與體積元素、轉動慣量。

## 3.1 極座標 {#fx-polar}

### 單位向量與它的時間導數 | ch01#po-unit
$$\hat r=\cos\theta\,\hat i+\sin\theta\,\hat j,\qquad \hat\theta=-\sin\theta\,\hat i+\cos\theta\,\hat j$$

$$\dot{\hat r}=\dot\theta\,\hat\theta,\qquad \dot{\hat\theta}=-\dot\theta\,\hat r$$

極座標的單位向量會跟著粒子轉，對時間微分不是零——這是和直角座標最大的不同，速度、加速度多出來的項都從這裡來。

### 極座標的速度 | ch01#po-va
$$\vec r=r\hat r,\qquad \vec v=\dot r\,\hat r+r\dot\theta\,\hat\theta$$

徑向是「離原點多快」，切向是「繞多快」（$r\dot\theta=r\omega$）。

### 極座標的加速度 | ch01#po-va
$$\vec a=(\ddot r-r\dot\theta^2)\,\hat r+(2\dot r\dot\theta+r\ddot\theta)\,\hat\theta$$

$-r\dot\theta^2$ 是向心加速度，$2\dot r\dot\theta$ 是科氏項。等速圓周運動（$\dot r=\ddot r=\ddot\theta=0$）剩 $-r\omega^2\hat r$。切向那一項等於 $\frac1r\frac{\mathrm d}{\mathrm dt}(r^2\dot\theta)$，連心力時為零 ⟹ $r^2\dot\theta$ 守恆（角動量）。

### 線元素與面積元素 | ch01#po-def
$$\mathrm d\vec s=\mathrm dr\,\hat r+r\,\mathrm d\theta\,\hat\theta,\qquad \mathrm dA=r\,\mathrm dr\,\mathrm d\theta$$

角度方向走 $\mathrm d\theta$ 的長度是 $r\,\mathrm d\theta$，所以面積元素多一個 $r$。積圓形區域時最常漏掉這個 $r$。

## 3.2 柱座標與球座標 {#fx-cylsph}

### 柱座標 | ch01#cs-cyl
$$\mathrm d\vec s=\mathrm dr\,\hat r+r\,\mathrm d\phi\,\hat\phi+\mathrm dz\,\hat z,\qquad \mathrm dV=r\,\mathrm dr\,\mathrm d\phi\,\mathrm dz$$

就是極座標加上 $z$：速度、加速度照極座標再加 $\dot z\hat z$、$\ddot z\hat z$。側面面積元素 $r\,\mathrm d\phi\,\mathrm dz$。

### 球座標 | ch01#cs-sph
$$x=r\sin\theta\cos\phi,\quad y=r\sin\theta\sin\phi,\quad z=r\cos\theta$$

$$\mathrm d\vec s=\mathrm dr\,\hat r+r\,\mathrm d\theta\,\hat\theta+r\sin\theta\,\mathrm d\phi\,\hat\phi,\qquad \mathrm dV=r^2\sin\theta\,\mathrm dr\,\mathrm d\theta\,\mathrm d\phi$$

$\theta$ 從 $+z$ 軸量（$0$ 到 $\pi$），$\phi$ 繞 $z$ 軸（$0$ 到 $2\pi$）。繞 $\phi$ 的圓半徑是 $r\sin\theta$，所以 $\phi$ 方向的長度是 $r\sin\theta\,\mathrm d\phi$。球面面積元素 $r^2\sin\theta\,\mathrm d\theta\,\mathrm d\phi$，積滿得 $4\pi r^2$。

### 球座標的速度 | ch01#cs-sph
$$\vec v=\dot r\,\hat r+r\dot\theta\,\hat\theta+r\sin\theta\,\dot\phi\,\hat\phi$$

把 $\mathrm d\vec s$ 除以 $\mathrm dt$ 就是速度——三種座標都可以這樣記。

### 記法：元素＝各方向長度相乘 | ch01#cs-table
$$\mathrm dV=(\mathrm dr)(r\,\mathrm d\theta)(r\sin\theta\,\mathrm d\phi)$$

$\mathrm d\vec s$ 的每一項是「沿那個方向走的長度」，角度前面一定乘上轉動的半徑（$r$ 或 $r\sin\theta$）；體積元素就是三項長度相乘，面積元素是兩項相乘。

## 3.3 轉動慣量 {#fx-inertia}

### 轉動慣量的定義與常用值 | ch01#cs-tm, ch02#c2m-inertia
$$I=\int(\text{到轉軸的距離})^2\,\mathrm dm$$

$$\begin{gathered}\text{圓環 }MR^2,\qquad\text{圓盤 }\tfrac12MR^2\\ \text{實心球 }\tfrac25MR^2,\qquad\text{圓管 }\tfrac M2(R_1^2+R_2^2)\end{gathered}$$

用柱、球座標的體積元素積分；距離是到**轉軸**的距離（球座標裡是 $r\sin\theta$，不是 $r$）。密度不均勻時 $\mathrm dm=\rho\,\mathrm dV$，$\rho$ 跟著座標變。

# s04 | 04-vector-calculus.html | 梯度、散度、旋度與積分定理 | Lecture 1 §12–15 | $\nabla$ 運算子、梯度與方向導數、散度與 Gauss 定理、旋度與 Stokes 定理、保守力的三種等價說法。

## 4.1 梯度 {#fx-grad}

### $\nabla$ 運算子 | ch01#gr-del
$$\nabla=\hat i\frac{\partial}{\partial x}+\hat j\frac{\partial}{\partial y}+\hat k\frac{\partial}{\partial z}$$

本身不是數，要作用在函數上：作用在純量是梯度 $\nabla\phi$、和向量內積是散度 $\nabla\cdot\vec A$、和向量外積是旋度 $\nabla\times\vec A$。

### 梯度與全微分 | ch01#gr-def
$$\nabla\phi=\Big(\frac{\partial\phi}{\partial x},\frac{\partial\phi}{\partial y},\frac{\partial\phi}{\partial z}\Big),\qquad \mathrm d\phi=\nabla\phi\cdot\mathrm d\vec s$$

梯度指向 $\phi$ 增加最快的方向，大小是最大變化率，並且垂直等值面（等高線）。求曲面的法向量：把曲面寫成 $\phi(x,y,z)=$ 常數，$\nabla\phi$ 就是法向量。

### 方向導數 | ch01#gr-def
$$\frac{\mathrm d\phi}{\mathrm ds}\Big|_{\hat n}=\hat n\cdot\nabla\phi$$

沿單位向量 $\hat n$ 走時 $\phi$ 的變化率。題目給的方向不是單位向量時要先除以長度。

### 位能與力 | ch01#gr-force
$$\vec F=-\nabla V$$

力指向位能下降最快的方向。只對保守力成立（見 4.4）。

### 只和 $r$ 有關的函數 | ch01#dv-r
$$\nabla f(r)=f'(r)\,\hat r,\qquad \nabla r=\hat r,\qquad \nabla\frac1r=-\frac{\hat r}{r^2}$$

連心力、萬有引力都屬於這一型：梯度一定沿徑向。

符號：$r=\sqrt{x^2+y^2+z^2}$，$\hat r=\vec r/r$。

## 4.2 散度 {#fx-div}

### 散度的定義與意義 | ch01#dv-def, ch01#dv-sign
$$\nabla\cdot\vec f=\frac{\partial f_x}{\partial x}+\frac{\partial f_y}{\partial y}+\frac{\partial f_z}{\partial z}=\frac{\text{淨流出通量}}{\text{體積}}$$

結果是純量。正的是「源」（往外流出）、負的是「匯」（往內流入）、零表示流進等於流出。

### $\nabla$ 作用在 $\vec r$ 上 | ch01#dv-r
$$\nabla\cdot\vec r=3,\qquad \nabla\cdot\big(g(r)\,\vec r\big)=3g+rg',\qquad \nabla\cdot\frac{\hat r}{r^2}=0\ (r\neq0)$$

$\nabla^2=\nabla\cdot\nabla=\partial_x^2+\partial_y^2+\partial_z^2$ 是拉普拉斯算子。平方反比場在原點以外散度為零，所以通量只由原點的「源」決定。

### Gauss 散度定理 | ch01#dv-gauss
$$\oint_S\vec A\cdot\mathrm d\vec a=\int_V\nabla\cdot\vec A\,\mathrm dv$$

封閉曲面的總通量＝裡面散度的體積分。哪邊好算就算哪邊：散度簡單（例如常數）就算體積分。$\mathrm d\vec a$ 指向曲面外側。

## 4.3 旋度 {#fx-curl}

### 旋度的行列式 | ch01#cu-def
$$\nabla\times\vec V=\begin{vmatrix}\hat i&\hat j&\hat k\\ \partial_x&\partial_y&\partial_z\\ V_x&V_y&V_z\end{vmatrix},\qquad (\nabla\times\vec V)_z=\frac{\partial V_y}{\partial x}-\frac{\partial V_x}{\partial y}$$

展開方式和外積一樣，中間項同樣要小心負號。

### 旋度的意義 | ch01#cu-meaning
$$\oint_C\vec V\cdot\mathrm d\vec\lambda\approx(\nabla\times\vec V)\cdot\hat n\,\Delta\sigma$$

在那一點放一個小槳輪，旋度描述它會不會轉、繞哪個軸轉。剛體轉動的速度場 $\vec v=\vec\omega\times\vec r$ 的旋度是 $2\vec\omega$。

### 一定為零的兩個組合 | ch01#cu-cons
$$\nabla\times(\nabla\phi)=0,\qquad \nabla\cdot(\nabla\times\vec A)=0,\qquad \nabla\times\big[\vec r\,f(r)\big]=0$$

梯度場沒有旋度（所以 $\vec F=-\nabla U$ 的力旋度為零）；旋度場沒有散度。連心力 $f(r)\vec r$ 旋度為零 ⟹ 連心力都是保守力。

## 4.4 Stokes 定理與保守力 {#fx-stokes}

### Stokes 定理 | ch01#st-thm
$$\oint_C\vec V\cdot\mathrm d\vec\lambda=\int_S(\nabla\times\vec V)\cdot\mathrm d\vec\sigma$$

封閉曲線的環量＝曲線圍起來的曲面上旋度的通量。方向用右手定則：四指沿 $C$ 走的方向，拇指是 $\mathrm d\vec\sigma$ 的方向。曲面可以任選（只要邊界是 $C$），選最好積的那個。

### 用線積分求面積 | ch01#st-thm
$$A=\frac12\oint_C(x\,\mathrm dy-y\,\mathrm dx)$$

Stokes 定理在平面上的應用（取 $\vec V=\tfrac12(-y,x,0)$，旋度為 $\hat k$）。曲線要逆時針走。

### 純量位能 | ch01#st-pot
$$\vec F=-\nabla\phi\iff\phi(\vec r)=-\int_{\vec r_0}^{\vec r}\vec F\cdot\mathrm d\vec r$$

給力求位能：沿任一條路徑積分（通常選沿座標軸的折線），加負號；參考點 $\vec r_0$ 任選，只差一個常數。

### 保守力的三種等價說法 | ch01#st-equiv, ch02#c2c-curl
$$\vec F=-\nabla\phi\iff\nabla\times\vec F=0\iff\oint\vec F\cdot\mathrm d\vec r=0$$

三者任一成立就是保守力，功和路徑無關。考試判斷保守力最快的方法是算旋度。條件：區域要單連通（中間沒有挖洞）。

# s05 | 05-newton.html | 牛頓定律與解運動方程 | Lecture 2 §1–4 | 牛頓三定律、伽利略轉換、用第三定律定義質量、地球的加速度、$\ddot x$ 的三種寫法與依力的形式選寫法。

## 5.1 牛頓三定律 {#fx-laws}

### 第二定律 | ch02#c2s-second
$$\vec F=\frac{\mathrm d\vec p}{\mathrm dt},\qquad \vec p=m\vec v;\qquad m\text{ 不變時 }\vec F=m\ddot{\vec r}$$

$\vec F$ 是所有外力的合力。向量式要拆成各軸分別寫：$F_x=m\ddot x$、$F_y=m\ddot y$、$F_z=m\ddot z$。質量會變（火箭、繩子）或相對論時要回到 $\mathrm d\vec p/\mathrm dt$。

### 第三定律與動量守恆 | ch02#c2s-third
$$\vec F_{12}=-\vec F_{21}\ \Longrightarrow\ \frac{\mathrm d}{\mathrm dt}(\vec p_1+\vec p_2)=0$$

作用力與反作用力作用在**不同**物體上，所以不會互相抵消；兩個物體合起來看，內力抵消，總動量守恆（沒有外力時）。

### 用第三定律定義質量 | ch02#c2s-mass
$$m_1\vec a_1=-m_2\vec a_2\ \Longrightarrow\ \frac{m_2}{m_1}=-\frac{a_1}{a_2}$$

兩物體只互相作用時，量加速度的比就能得到質量比（選一個當標準質量），不必先知道力。

## 5.2 座標系 {#fx-frames}

### 伽利略轉換 | ch02#c2l-sym
$$\vec r\,'=\vec r-\vec Vt\ \Longrightarrow\ \dot{\vec r}\,'=\dot{\vec r}-\vec V,\qquad \ddot{\vec r}\,'=\ddot{\vec r}$$

等速度相對運動的兩個座標系量到的加速度相同，所以 $F=ma$ 在兩邊形式一樣（伽利略不變性）。只要座標系有加速度，就不再是慣性座標系。

### 地球自轉的向心加速度 | ch02#c2f-earth
$$a=\omega^2R\cos\lambda,\qquad \text{赤道 }a=\frac{v^2}R\approx3.4\times10^{-2}\ \text{m/s}^2$$

約為 $g$ 的 0.3%，所以一般問題把地面當慣性座標系。赤道上體重計讀數 $F_{\text{scale}}=mg-mv^2/R$，比真正的重力小一點。

符號：$\lambda$＝緯度，$R$＝地球半徑，$\omega=2\pi/(1\ \text{天})$。

## 5.3 解 $F=m\ddot x$ 的策略 {#fx-strategy}

### $\ddot x$ 的三種寫法 | ch02#c2st-tips
$$\ddot x=\frac{\mathrm dv}{\mathrm dt}=v\frac{\mathrm dv}{\mathrm dx}=\frac12\frac{\mathrm d(v^2)}{\mathrm dx}$$

題目要 $v(t)$ 就用第一種；要 $v(x)$（距離、速率和位置的關係）就用後兩種，時間會消失。這是本章最重要的一條。

### 依力的形式選寫法 | ch02#c2st-form
$$F(t):\ v=v_0+\frac1m\int_0^tF\,\mathrm dt;\qquad F(v):\ t=\int\frac{m\,\mathrm dv}{F(v)},\ \ x=\int\frac{mv\,\mathrm dv}{F(v)};\qquad F(x):\ \tfrac12mv^2=\int F\,\mathrm dx+C$$

原則：讓方程式一邊只有一個變數就能積分。力和兩個以上的量有關（例如 $F(x,v)$）一般不能直接分離變數。

### 等加速度 | ch02#c2i-friction
$$v=v_0+at,\qquad x=x_0+v_0t+\tfrac12at^2,\qquad v^2=v_0^2+2a(x-x_0)$$

只有加速度是常數時才能用（斜面、無阻力拋體）；有阻力時加速度隨速度變，不能用。

# s06 | 06-incline-drag.html | 斜面、阻力與由速度求力 | Lecture 2 §5–7 | 斜面的座標與正向力、靜摩擦與動摩擦、阻力的一般形式、線性與 $v^2$ 阻力的完整解、終端速度、指數阻力、已知 $v(x)$ 求力、相對論定力。

## 6.1 斜面與摩擦 {#fx-incline}

### 斜面的分力與正向力 | ch02#c2i-axes
$$F_x=mg\sin\theta,\qquad N=mg\cos\theta$$

$x$ 軸沿斜面向下、$y$ 軸垂直斜面：這樣運動只在 $x$ 方向，$y$ 方向直接得到 $N$。$N=mg\cos\theta$ 只在垂直斜面沒有其他力時成立；有斜拉的力要重算。

符號：$\theta$＝斜面傾角。

### 靜摩擦與開始滑的角度 | ch02#c2i-friction
$$f_s\le\mu_sN,\qquad \tan\theta_c=\mu_s$$

靜摩擦是「需要多少給多少」，最大才到 $\mu_sN$；只有在「剛好要滑」時才寫等號。

### 動摩擦與滑動的加速度 | ch02#c2i-friction
$$f_k=\mu_kN,\qquad \ddot x=g(\sin\theta-\mu_k\cos\theta)\ \text{（下滑）}$$

方向和相對運動相反。往上滑時摩擦向下，加速度變 $-g(\sin\theta+\mu_k\cos\theta)$，上滑和下滑要分開寫。

## 6.2 阻力 {#fx-drag}

### 阻力的一般形式 | ch02#c2d-law
$$\vec F_r=-mk\,v^n\,\frac{\vec v}{v}$$

方向永遠和速度相反（$-\vec v/v$）。低速小物體 $n\approx1$、一般空氣中 $n\approx2$。$n$ 為奇數時可以寫成帶號的 $-mkv$ 一條式子管上升和下降；$n=2$ 時不行，要分段。

### 水平運動的線性阻力 | ch02#c2d-hor
$$v=v_0e^{-kt},\qquad x=\frac{v_0}k\big(1-e^{-kt}\big),\qquad v=v_0-kx$$

速度指數衰減、永遠不會真正停下，但走的總距離有限 $v_0/k$。

符號：阻力 $F_r=-kmv$，$k$ 的單位是 $\text{s}^{-1}$。

### 鉛直運動的線性阻力與終端速度 | ch02#c2d-vert
$$\dot z=-\frac gk+\Big(v_0+\frac gk\Big)e^{-kt},\qquad v_t=\frac gk$$

$z$ 向上為正、$v_0$ 帶號。時間夠長時指數項消失，速度趨近終端速度 $g/k$（重力＝阻力）。$k\to0$ 時要退回 $\dot z=v_0-gt$，可以用來檢查答案。

### 線性阻力上拋的最高點 | ch02#c2d-vert
$$t_{\text{top}}=\frac1k\ln\!\Big(1+\frac{kv_0}g\Big),\qquad y_{\max}=\frac{v_0}k-\frac g{k^2}\ln\!\Big(1+\frac{kv_0}g\Big)$$

令 $\dot z=0$ 得時間，再代回位置。

### $v^2$ 阻力：終端速度與由靜止下落 | ch02#c2d-more
$$v_t=\sqrt{\frac gk},\qquad v=v_t\tanh\!\big(\sqrt{gk}\,t\big),\qquad v^2=v_t^2\big(1-e^{-2ky}\big)$$

阻力 $kmv^2$。要時間用 $\mathrm dv/(g-kv^2)$ 積出 $\tanh$；要距離用 $\tfrac12\mathrm d(v^2)/(g-kv^2)$，比較好積。

符號：$y$＝下落的距離（向下為正）。

### $v^2$ 阻力：上升的最大高度 | ch02#c2d-more
$$x_{\max}=\frac1{2k}\ln\frac{g+kv_0^2}g,\qquad \text{回到原處的速率 }v=\frac{v_0v_t}{\sqrt{v_0^2+v_t^2}}$$

上升時重力和阻力同向（$g+kv^2$），下降時反向（$g-kv^2$），一定要在最高點分成兩段。回到原處的速率比 $v_0$ 小。

## 6.3 其他形式的力 {#fx-otherforce}

### 指數阻力的停止時間與距離 | ch02#c2v-exp
$$F=-\alpha e^{\beta v}:\qquad t_{\text{stop}}=\frac m{\alpha\beta}\big(1-e^{-\beta v_0}\big),\qquad x_{\text{stop}}=\frac m{\alpha\beta^2}\big[1-(1+\beta v_0)e^{-\beta v_0}\big]$$

時間用 $m\,\mathrm dv/\mathrm dt=F$、距離用 $mv\,\mathrm dv/\mathrm dx=F$，令 $v=0$；距離要分部積分 $\int ve^{-\beta v}\,\mathrm dv$。

### 已知 $v(x)$ 求力 | ch02#c2v-force
$$F(x)=m\,v\frac{\mathrm dv}{\mathrm dx}=\frac12m\frac{\mathrm d(v^2)}{\mathrm dx}$$

不必先求 $x(t)$。要 $F(t)$ 時再由 $\mathrm dx/\mathrm dt=v(x)$ 分離變數求 $x(t)$，代進 $F(x)$。

### 動量不是 $mv$：相對論的定力 | ch02#c2v-rel
$$p=\frac{mv}{\sqrt{1-v^2/c^2}}=Ft\ \Longrightarrow\ v=\frac{Ft/m}{\sqrt{1+(Ft/mc)^2}}$$

由 $F=\mathrm dp/\mathrm dt$ 直接積出 $p=Ft$（從靜止開始）再解 $v$。$t\to\infty$ 時 $v\to c$，不會超過光速；$Ft\ll mc$ 時退回 $v=Ft/m$。

# s07 | 07-projectile.html | 拋體（含空氣阻力） | Lecture 2 §8–9 | 無阻力拋體的時間、射程、最大高度與軌跡、斜坡上的射程、線性阻力拋體與微擾法、$v^2$ 阻力拋體為什麼要數值解。

## 7.1 無阻力的拋體 {#fx-proj}

### 各方向分開解 | ch02#c2p-comp
$$x=v_0\cos\theta\,t,\qquad y=v_0\sin\theta\,t-\tfrac12gt^2$$

水平無力、等速；鉛直只有重力、等加速。兩方向只透過時間 $t$ 連起來。

### 飛行時間、射程、最大高度 | ch02#c2p-comp
$$T=\frac{2v_0\sin\theta}g,\qquad R=\frac{v_0^2\sin2\theta}g,\qquad y_{\max}=\frac{v_0^2\sin^2\theta}{2g}$$

只在**起點和終點同高**時成立。最大射程在 $\theta=45^\circ$，且 $\theta$ 和 $90^\circ-\theta$ 射程相同。起終點不同高（從懸崖拋出）要回到 $y(t)$ 解二次方程。

### 軌跡方程式 | ch02#c2p-comp
$$y=x\tan\theta-\frac{gx^2}{2v_0^2\cos^2\theta}$$

消去 $t$ 得到拋物線。問「能不能打中某點 $(x,y)$」或「要用什麼角度」時用這條，把 $1/\cos^2\theta=1+\tan^2\theta$ 代進去變成 $\tan\theta$ 的二次方程。

### 斜坡上的射程 | ch02#c2p-more
$$d_{\max}=\frac{v_0^2}{g(1+\sin\beta)},\qquad \alpha=\frac\pi4+\frac\beta2$$

往傾角 $\beta$ 的斜坡上方發射時，沿坡面的最大射程與對應的仰角（從水平量）。往下坡發射時把 $\beta$ 換成 $-\beta$。

## 7.2 有空氣阻力的拋體 {#fx-airproj}

### 線性阻力的拋體 | ch02#c2a-linear
$$x=\frac Uk\big(1-e^{-kt}\big),\qquad y=-\frac{gt}k+\frac{kV+g}{k^2}\big(1-e^{-kt}\big)$$

阻力 $-km\vec v$ 時 $x$、$y$ 兩方向各自獨立，可以分開解（水平就是 6.2 的水平阻力、鉛直就是鉛直阻力）。水平距離有上限 $U/k$。

符號：$U=v_0\cos\theta$、$V=v_0\sin\theta$ 為初速的水平、鉛直分量。

### 微擾法：阻力很小時的修正 | ch02#c2a-linear
$$T\approx\frac{2V}g\Big(1-\frac{kV}{3g}\Big),\qquad R'\approx R\Big(1-\frac{4kV}{3g}\Big)$$

$kV/g\ll1$ 時把指數展開到一階。阻力讓飛行時間和射程都變短；最佳角度也略小於 $45^\circ$。

### $v^2$ 阻力的拋體 | ch02#c2a-updown
$$m\ddot x=-kmv\,\dot x,\qquad m\ddot y=-mg-kmv\,\dot y,\qquad v=\sqrt{\dot x^2+\dot y^2}$$

$v$ 同時含 $\dot x$、$\dot y$，兩方向耦合在一起，沒有解析解，只能數值計算。一維的 $v^2$ 阻力（鉛直上拋）才有解析解，且上升、下降要分開寫。

# s08 | 08-atwood-em.html | Atwood 機與帶電粒子 | Lecture 2 §10 | Atwood 機（含加速電梯）、Lorentz 力、均勻磁場中的圓周與螺旋運動、$\vec E\times\vec B$ 漂移。

## 8.1 Atwood 機 {#fx-atwood}

### Atwood 機的加速度與張力 | ch02#c2w-atwood
$$a=\frac{m_1-m_2}{m_1+m_2}\,g,\qquad T=\frac{2m_1m_2}{m_1+m_2}\,g$$

兩物體各寫一條 $F=ma$，用「繩長固定」連起兩者的加速度（一個上、一個下，大小相同），再消去張力。滑輪無質量、繩不可伸長時才成立。

### 在加速的電梯裡 | ch02#c2w-atwood
$$a'=\frac{(m_1-m_2)(g-\alpha)}{m_1+m_2},\qquad T=\frac{2m_1m_2(g-\alpha)}{m_1+m_2}$$

電梯以 $\alpha$ 向下加速時，等效重力變成 $g-\alpha$（向上加速則 $g+\alpha$）。$a'$ 是相對電梯的加速度；問對地加速度要再加上電梯的。最容易犯的錯是在電梯（非慣性系）裡直接寫 $F=ma$。

## 8.2 電磁場中的帶電粒子 {#fx-em}

### Lorentz 力 | ch02#c2w-em
$$\vec F=q\big(\vec E+\vec v\times\vec B\big)$$

磁力永遠垂直速度，所以**不做功**，只改變方向、不改變速率。

### 均勻磁場中的圓周運動 | ch02#c2w-em
$$\omega_c=\frac{qB}m,\qquad r=\frac{mv_\perp}{qB},\qquad T=\frac{2\pi m}{qB}$$

由 $qv_\perp B=mv_\perp^2/r$ 得到。週期和速率無關（迴旋加速器的原理）。速度有平行 $\vec B$ 的分量 $v_\parallel$ 時，平行方向等速，合起來是螺旋，螺距 $v_\parallel T$。

### $\vec E\times\vec B$ 漂移 | ch02#c2w-em
$$\vec v_d=\frac{\vec E\times\vec B}{B^2},\qquad v_d=\frac{E_\perp}B$$

電場和磁場互相垂直時，粒子一邊繞圈一邊以固定速度漂移，軌跡是擺線（由靜止出發時）。漂移速度和電荷、質量都無關。

# s09 | 09-conservation.html | 動量、角動量與能量守恆 | Lecture 2 §11–14 | 線動量與角動量守恆、力矩、轉動慣量、功與功能定理、保守力與位能、能量守恆、圓周運動與迴圈軌道。

## 9.1 線動量 {#fx-momentum}

### 沒有力的方向動量守恆 | ch02#c2m-lin
$$F_s=\frac{\mathrm dp_s}{\mathrm dt}=0\ \Longrightarrow\ p_s=\text{常數}$$

不需要整個合力為零：只要某個**固定**方向 $\hat s$ 上沒有外力，那個方向的動量就守恆。例如拋體的水平動量、斜面上滑塊與可動斜面系統的水平動量。

### 衝量 | ch02#c2s-second
$$\Delta\vec p=\int\vec F\,\mathrm dt$$

碰撞、爆炸這種時間很短的過程，內力遠大於外力，所以碰撞前後總動量守恆，但動能一般不守恆。

## 9.2 角動量 {#fx-angmom}

### 角動量與力矩 | ch02#c2m-ang
$$\vec L=\vec r\times\vec p,\qquad \vec N=\vec r\times\vec F=\frac{\mathrm d\vec L}{\mathrm dt}$$

$\vec r$ 從同一個參考點量起。力矩為零（例如連心力，$\vec F\parallel\vec r$）⟹ 角動量守恆，這就是克卜勒第二定律（等面積）。

### 轉動慣量與角動量 | ch02#c2m-inertia
$$L=I\omega,\qquad I=\sum_im_ir_i^2$$

$r_i$ 是到轉軸的距離。轉動慣量變了（例如老鼠跳上吊扇）而沒有外力矩時，$I\omega$ 守恆，角速度跟著變。

## 9.3 功與能量 {#fx-work}

### 功 | ch02#c2k-work
$$W_{12}=\int_1^2\vec F\cdot\mathrm d\vec r$$

只有沿位移方向的分量做功。正向力、磁力垂直位移不做功；動摩擦做負功 $-f_k\,s$（$s$ 是路徑長，不是位移）。

### 功能定理 | ch02#c2k-theorem
$$W_{12}=T_2-T_1,\qquad T=\tfrac12mv^2$$

由 $F=m\ddot x$ 乘 $\dot x$ 積分得到，所以對任何力都成立——$\vec F$ 是**合力**。不需要知道時間，只看起點、終點的速率。

### 保守力與位能 | ch02#c2c-pot, ch02#c2c-grad
$$\int_1^2\vec F\cdot\mathrm d\vec r=U_1-U_2,\qquad \vec F=-\nabla U$$

功和路徑無關的力才能定義位能。重力 $U=mgz$、彈簧 $U=\tfrac12kx^2$。摩擦力的功和路徑有關，沒有位能。

### 力學能守恆 | ch02#c2c-energy
$$E=T+U,\qquad \frac{\mathrm dE}{\mathrm dt}=\frac{\partial U}{\partial t}$$

只有保守力做功、且 $U$ 不顯含時間時，$E$ 守恆。有非保守力時 $E_2-E_1=W_{\text{非保守}}$（例如摩擦讓 $E$ 減少）。

### 判斷保守力 | ch02#c2c-curl
$$\nabla\times\vec F=0\iff\oint\vec F\cdot\mathrm d\vec r=0$$

和 4.4 同一件事。和速度有關的力（阻力）、和時間有關的力都不是保守力。

## 9.4 圓周運動與迴圈軌道 {#fx-circle}

### 圓周運動的徑向方程 | ch02#c2s-second, ch02#c2-exam5-2=L2 考古 第 5 章第 2 題
$$\sum F_{\text{向心}}=\frac{mv^2}R=mR\omega^2$$

指向圓心的合力提供向心加速度；它不是另外一種力，是重力、張力、正向力等的合成。

### 迴圈軌道：何時離開軌道 | ch02#c2-tm-2-25=L2 課本 2-25
$$N=\frac{mv^2}R-mg\cos\phi\ \ (\text{軌道內側}),\qquad \text{離開軌道}\iff N=0$$

能量守恆給出每一點的 $v^2$，代進徑向方程求 $N$；$N$ 降到零的位置就是脫離點。過頂點不掉的條件是頂點 $v^2\ge gR$。

符號：$\phi$＝從迴圈頂點量起、半徑和鉛直線的夾角（頂點 $\phi=0$）。

# s10 | 10-equilibrium.html | 位能圖、平衡與穩定 | Lecture 2 §15 | 由能量守恆求速度與時間、轉折點、平衡點與穩定性判斷、平衡點附近的小振動。

## 10.1 讀位能圖 {#fx-diagram}

### 由能量守恆求速度與時間 | ch02#c2q-diagram
$$v=\pm\sqrt{\frac2m\big[E-U(x)\big]},\qquad t-t_0=\int_{x_0}^x\frac{\mathrm dx}{\pm\sqrt{\frac2m\big[E-U(x)\big]}}$$

一維保守系統不必解 $F=ma$：直接由 $E$ 和 $U(x)$ 得到速度，再積分得到時間。$E\ge U$ 的區域才能到達。

### 轉折點 | ch02#c2q-diagram
$$E=U(x_{\text{轉折}})$$

速度為零、要掉頭的位置。兩個轉折點之間是束縛運動（來回振動）；只有一邊有轉折點則會跑到無窮遠。

## 10.2 平衡與穩定 {#fx-stability}

### 平衡點與穩定性 | ch02#c2q-taylor
$$\Big(\frac{\mathrm dU}{\mathrm dx}\Big)_{x_0}=0;\qquad \Big(\frac{\mathrm d^2U}{\mathrm dx^2}\Big)_{x_0}>0\ \text{穩定},\quad <0\ \text{不穩定}$$

平衡＝合力為零＝位能圖的水平切線。穩定是谷底（偏離後被拉回），不穩定是山頂（偏離後越跑越遠）。

### 二階導數為零時 | ch02#c2q-taylor
$$U''(x_0)=0:\ \text{看第一個不為零的導數 }U^{(n)}(x_0)$$

$n$ 為偶數且 $U^{(n)}>0$ 才穩定；$n$ 為奇數一定不穩定（一邊推得回來、另一邊推不回來）。

### 平衡點附近的小振動 | ch02#c2q-taylor
$$U(x)\approx U(x_0)+\tfrac12U''(x_0)(x-x_0)^2,\qquad \omega=\sqrt{\frac{U''(x_0)}m},\qquad T=\frac{2\pi}\omega$$

在穩定平衡點附近把位能泰勒展開到二次，就是彈簧（等效彈力常數 $k=U''(x_0)$），做簡諧振動。
