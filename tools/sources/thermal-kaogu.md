<!-- 熱學考古章（subjects/thermal/kaogu）各卡的精簡解題；每張卡以「## 卡片 id」開頭。改完執行 python tools/build_thermal_kaogu.py -->

## tk1-115-1

符號：咖啡 $M=100\ \text{g}$，滾燙取 $100^\circ\text{C}$，比熱當成水 $c_w=1\ \text{cal/(g·°C)}$；末溫 $T_f=60^\circ\text{C}$；冰初溫 $-15^\circ\text{C}$、比熱 $c_{\text{冰}}=0.5\ \text{cal/(g·°C)}$；熔化熱 $l_f=80\ \text{cal/g}$（題目沒給，要背）；求冰的質量 $m$。

**① 咖啡放出的熱：** 這是習題 1.47 換數字，做法相同：咖啡放的熱＝冰「升到 0°C＋熔化＋升到 60°C」三段吸的熱，全程用 cal。

公式（比熱）：$Q=mc\,\Delta T$，其中 $m$ 為質量、$c$ 為比熱、$\Delta T$ 為溫度變化；本題咖啡 $m=M=100\ \text{g}$、$c=c_w$、$\Delta T=100-60=40^\circ\text{C}$。

$$Q_{\text{咖啡}}=Mc_w\,(100^\circ\text{C}-T_f)=(100)(1)(40)\ \text{cal}=4000\ \text{cal}$$

**② 每克冰吸收的熱：** 冰先從 $-15^\circ\text{C}$ 升到 $0^\circ\text{C}$，再熔化，最後當水升到 $60^\circ\text{C}$。

公式（潛熱）：$Q=m\,l_f$，其中 $m$ 為熔化的質量、$l_f$ 為每克的熔化熱；本題 $l_f=80\ \text{cal/g}$。

代入 $c_{\text{冰}}=0.5$、$l_f=80$、$T_f=60^\circ\text{C}$：

$$\frac{Q_{\text{冰}}}{m}=c_{\text{冰}}(15^\circ\text{C})+l_f+c_w\,(T_f-0)=7.5+80+60=147.5\ \text{cal/g}$$

**③ 解出冰的質量：** 咖啡放的熱全部給冰，用 ① 的 $Q_{\text{咖啡}}$ 除以 ② 的每克吸熱。

$$m=\frac{Q_{\text{咖啡}}}{Q_{\text{冰}}/m}=\frac{4000\ \text{cal}}{147.5\ \text{cal/g}}=27.1\ \text{g}$$

$$\boxed{m\approx27\ \text{g}}$$

## sc-1-8

符號：線膨脹係數 $\alpha\equiv\dfrac{\Delta L/L}{\Delta T}$；鋼 $\alpha=1.1\times10^{-5}\ \text{K}^{-1}$，橋長 $L=1\ \text{km}=1000\ \text{m}$；溫差自己估計 $\Delta T\approx25\ \text{K}$（台灣冬夜 $10^\circ\text{C}$、夏日 $35^\circ\text{C}$）。考卷只考 (a) 與 (c)（考卷上 (c) 編為 (b)）。

### (a) 鋼橋冬夏的長度變化

**① 把定義移項：** 題目給的是「每度的長度變化比例」，移項後直接代入；溫差是估計值，答案只要數量級。

公式（線膨脹係數定義）：$\alpha=\dfrac{\Delta L/L}{\Delta T}$，其中 $L$ 為原長、$\Delta L$ 為長度變化、$\Delta T$ 為溫度變化；本題 $L=1000\ \text{m}$、$\Delta T=25\ \text{K}$。

$$\alpha=\frac{\Delta L/L}{\Delta T}\ \Longrightarrow\ \Delta L=\alpha\,L\,\Delta T$$

**② 代入數值：** 代入 $\alpha=1.1\times10^{-5}\ \text{K}^{-1}$、$L=1000\ \text{m}$、$\Delta T=25\ \text{K}$：

$$\Delta L=(1.1\times10^{-5}\ \text{K}^{-1})(1000\ \text{m})(25\ \text{K})=0.275\ \text{m}\approx28\ \text{cm}$$

**③ 溫差估計不同時：** $\Delta L$ 正比於 $\Delta T$，每 1 K 是 1.1 cm：115 級期中一份滿分答案卷取 $\Delta T=15\ \text{K}$ 得 16.5 cm；解答手冊取溫帶 $-30\to+40^\circ\text{C}$（70 K）得 77 cm。都是「數十公分」，所以橋上必須留伸縮縫。

$$\boxed{\Delta L=\alpha L\Delta T\approx0.3\ \text{m}\ \ (\Delta T=25\ \text{K}\text{；溫帶 }70\ \text{K}\text{ 時約 }0.8\ \text{m})}$$

### (c) 證明 $\beta=\alpha_x+\alpha_y+\alpha_z$

**① 升溫後的體積：** 體積是三個邊長的乘積，先寫出升溫後的體積，展開後略去 $(\Delta T)^2$ 以上的小量，再和 $\beta$ 的定義比較。

取邊長 $L_x,L_y,L_z$ 的長方體，$V=L_xL_yL_z$。由 $\alpha$ 的定義，每個方向 $L_i\to L_i+\Delta L_i=L_i(1+\alpha_i\Delta T)$，所以

$$V+\Delta V=L_xL_yL_z(1+\alpha_x\Delta T)(1+\alpha_y\Delta T)(1+\alpha_z\Delta T)$$

**② 展開三個括號：**

$$\begin{aligned}&(1+\alpha_x\Delta T)(1+\alpha_y\Delta T)(1+\alpha_z\Delta T)\\&=1+(\alpha_x+\alpha_y+\alpha_z)\Delta T\\&\quad+(\alpha_x\alpha_y+\alpha_y\alpha_z+\alpha_z\alpha_x)(\Delta T)^2\\&\quad+\alpha_x\alpha_y\alpha_z(\Delta T)^3\end{aligned}$$

**③ 略去高次小量：** $\alpha_i\Delta T\sim10^{-5}\times10=10^{-4}$，平方是 $10^{-8}$，可略（定義中的 $\Delta T$ 本來就應取無窮小）：

$$V+\Delta V\approx V\,[1+(\alpha_x+\alpha_y+\alpha_z)\Delta T]\ \Longrightarrow\ \frac{\Delta V}{V}=(\alpha_x+\alpha_y+\alpha_z)\Delta T$$

**④ 和 $\beta$ 的定義比較：**

公式（體膨脹係數定義）：$\beta=\dfrac{\Delta V/V}{\Delta T}$，其中 $V$ 為原體積、$\Delta V$ 為體積變化；本題 $\Delta V/V$ 用上一步的結果。

$$\beta=\frac{\Delta V/V}{\Delta T}=\alpha_x+\alpha_y+\alpha_z$$

幾何意義：$\Delta V$ 是貼在三個面上的三塊薄板 $\Delta L_x\,L_yL_z+\Delta L_y\,L_xL_z+\Delta L_z\,L_xL_y$，略去的是邊上與角上的細條。各向同性時 $\alpha_x=\alpha_y=\alpha_z=\alpha$，$\beta=3\alpha$。

**⑤ 另一種寫法（微分）：** $\alpha_i=\dfrac1{L_i}\dfrac{dL_i}{dT}$、$\beta=\dfrac1V\dfrac{dV}{dT}$（定壓），用乘積法則：

$$\begin{aligned}\beta&=\frac1{L_xL_yL_z}\Big(\frac{dL_x}{dT}L_yL_z+L_x\frac{dL_y}{dT}L_z\\&\qquad+L_xL_y\frac{dL_z}{dT}\Big)\\&=\alpha_x+\alpha_y+\alpha_z\end{aligned}$$

（等價於 $\ln V=\ln L_x+\ln L_y+\ln L_z$ 兩邊對 $T$ 微分。）

$$\boxed{\begin{gathered}\frac{\Delta V}{V}=(\alpha_x+\alpha_y+\alpha_z)\Delta T\\ \Longrightarrow\ \beta=\alpha_x+\alpha_y+\alpha_z\\ \text{各向同性：}\beta=3\alpha\end{gathered}}$$

## tk-115-3

符號：$N=10$ 枚公正硬幣，每枚 H、T 各 $\tfrac12$、互相獨立；巨觀態用正面數 $n$ 區分。（原卷前兩小題都標成 (a)。）

### (a) 微觀態與巨觀態的個數

**① 微觀態個數：** 每枚 2 種結果、互相獨立，用乘法原理。

公式（乘法原理）：$N$ 個獨立物件各有 $k$ 種結果時，總排列數為 $k^N$，其中 $N$ 為物件數、$k$ 為每個物件的結果數；本題 $N=10$、$k=2$。

$$\Omega(\text{all})=2^N=2^{10}=1024$$

**② 巨觀態個數：** 巨觀態只看正面數 $n$，$n$ 只能是 $0,1,\dots,N$ 的整數，共 $N+1$ 個（不是 $2^{10}$）。代入 $N=10$：

$$\text{巨觀態數}=10+1=11$$

$$\boxed{\text{微觀態 }1024\text{ 個，巨觀態 }11\text{ 個}}$$

### (b) 特定序列 HTHHTTTHTH 的機率

**① 一個微觀態的機率：** 指定序列把每一枚都定好了，是 1024 個等機率微觀態中的一個。代入 (a) 的 $\Omega(\text{all})=1024$：

$$P(\text{序列})=\frac1{\Omega(\text{all})}=\frac1{1024}=9.77\times10^{-4}$$

$$\boxed{P=\frac1{1024}\approx9.77\times10^{-4}}$$

### (c) 7 正 3 反（任意順序）的機率

**① 數「7 正 3 反」的排法：** 「任意順序」是一個巨觀態，要算它的多重度，也就是從 10 枚裡選哪 7 枚是正面。

公式（二項式多重度）：$\Omega(n)=\dbinom{N}{n}=\dfrac{N!}{n!\,(N-n)!}$，其中 $N$ 為硬幣數、$n$ 為正面數；本題 $N=10$、$n=7$。

選 7 個正面等於選 3 個反面，$\binom{10}7=\binom{10}3$，分子只剩 3 個因子比較好算：

$$\Omega(7)=\binom{10}{7}=\frac{10!}{7!\,3!}=\frac{10\cdot9\cdot8}{3\cdot2\cdot1}=\frac{720}{6}=120$$

**② 巨觀態的機率：** 微觀態等機率，機率＝這個巨觀態的微觀態數 ÷ 總數。代入上一步的 $\Omega(7)=120$ 與 (a) 的 $\Omega(\text{all})=1024$：

$$P(7)=\frac{\Omega(7)}{\Omega(\text{all})}=\frac{120}{1024}=0.117$$

$$\boxed{P=\frac{120}{1024}\approx0.117=11.7\%}$$

## tk-115-4

符號：愛因斯坦固體，$N$ 個振子、$q$ 份能量（$E_q\simeq q\epsilon$），$N\gg1$、$q\gg1$；$k$ 為波茲曼常數。

### (a) 用 Stirling 證明多重度近似式

**① 改寫成完整的階乘：** Stirling 只能代入完整的 $n!$，而多重度裡是 $(q+N-1)!$ 與 $(N-1)!$，所以先照課本提示改寫；題目要的式子含根號，$\sqrt{2\pi n}$ 一個都不能丟。

公式（愛因斯坦固體多重度 (2.9)）：$\Omega(N,q)=\dfrac{(q+N-1)!}{q!\,(N-1)!}$，其中 $N$ 為振子數、$q$ 為能量份數。

由 $N!=N\cdot(N-1)!$ 得 $(N-1)!=\dfrac{N!}N$；同理 $(q+N-1)!=\dfrac{(q+N)!}{q+N}$。代入：

$$\Omega=\frac{(q+N-1)!}{q!\,(N-1)!}=\frac{(q+N)!/(q+N)}{q!\,N!/N}=\frac N{q+N}\cdot\frac{(q+N)!}{q!\,N!}$$

**② 代入 Stirling：** 三個階乘各代一次，$n$ 分別取 $q+N$、$q$、$N$。

公式（Stirling 近似）：$n!\simeq n^ne^{-n}\sqrt{2\pi n}$，其中 $n\gg1$；本題 $n=q+N,\ q,\ N$。

$$\Omega\approx\frac N{q+N}\cdot\frac{(q+N)^{q+N}e^{-(q+N)}\sqrt{2\pi(q+N)}}{q^qe^{-q}\sqrt{2\pi q}\cdot N^Ne^{-N}\sqrt{2\pi N}}$$

**③ 冪次與 $e$：** $e$ 的次方 $-(q+N)-(-q)-(-N)=0$，完全抵消。把 $(q+N)^{q+N}=(q+N)^q(q+N)^N$ 分給兩個分母：

$$\frac{(q+N)^{q+N}}{q^q\,N^N}=\left(\frac{q+N}q\right)^q\left(\frac{q+N}N\right)^N$$

**④ 根號部分化簡：** 剩下的是前面的 $\frac N{q+N}$ 乘上三個根號：

$$\frac N{q+N}\cdot\frac{\sqrt{2\pi(q+N)}}{\sqrt{2\pi q}\sqrt{2\pi N}}=\sqrt{\frac{N^2}{(q+N)^2}\cdot\frac{q+N}{2\pi qN}}=\sqrt{\frac{N}{2\pi q(q+N)}}$$

和上一步的冪次部分合起來：

$$\boxed{\Omega(N,q)\approx\frac{\left(\frac{q+N}q\right)^q\left(\frac{q+N}N\right)^N}{\sqrt{2\pi q(q+N)/N}}}$$

### (b) 熵 $S(N,q)$，以及省略的因子為何不影響

**① 取對數：** 用題目指定的（無根號）多重度，$\ln$ 把乘積變和、冪次變係數。

公式（熵的定義）：$S=k\ln\Omega$，其中 $k$ 為波茲曼常數、$\Omega$ 為多重度；本題 $\Omega=\left(\frac{q+N}q\right)^q\left(\frac{q+N}N\right)^N$。

$$S=k\left[q\ln\frac{q+N}q+N\ln\frac{q+N}N\right]$$

**② 展開合併：** 用 $\ln\frac{a}{b}=\ln a-\ln b$ 展開，兩個 $\ln(q+N)$ 合併：

$$S=k\Big[(q+N)\ln(q+N)-q\ln q-N\ln N\Big]$$

**③ 省略的因子：** 被省略的是 $-\tfrac k2\ln\frac{2\pi q(q+N)}N$。以 $N\sim q\sim10^{23}$ 估計，$\tfrac12\ln(2\pi\cdot2\times10^{23})\approx28$；保留的項卻是 $10^{23}$ 等級，所以在熵裡完全可以忽略：「只是大」的因子取對數後變成「小」的數。

$$\boxed{\begin{gathered}S=k\big[(q+N)\ln(q+N)-q\ln q-N\ln N\big]\\ \text{省略的根號只貢獻 }\ln\text{ 等級的小量}\end{gathered}}$$

### (c) 高溫極限 $q\gg N$

**① 第一個因子：** $N/q$ 是小數，把它寫成指數再用對數近似。

公式（小量的對數）：$\ln(1+x)\approx x$，其中 $|x|\ll1$；本題 $x=N/q$。

$$\left(1+\frac Nq\right)^q=e^{q\ln(1+N/q)}\approx e^{q\cdot N/q}=e^N$$

**② 第二個因子：** $q+N\approx q$（$N$ 相對 $q$ 可忽略），$\frac{q+N}N\approx\frac qN$。兩個合起來：

$$\Omega\approx e^N\left(\frac qN\right)^N=\left(\frac{eq}N\right)^N$$

**③ 為什麼叫「高溫」極限：** $q\gg N$ 表示平均每個振子有 $q/N\gg1$ 份能量，$U/N=(q/N)\epsilon\gg\epsilon$：能階間隔 $\epsilon$ 相對於每個振子的平均能量很小，量子化看不出來。溫度越高、能量越多才會這樣，對應 $kT\gg\epsilon$（第 3 章會證明此時 $U=NkT$）。

$$\boxed{\Omega\simeq\left(\frac{eq}N\right)^N\text{；每個振子平均很多份能量（}kT\gg\epsilon\text{），故稱高溫}}$$

### (d) 低溫極限 $q\ll N$

**① 第一個因子：** 角色對調，這次 $x=q/N\ll1$。$q+N\approx N$：

$$\left(\frac{q+N}q\right)^q\approx\left(\frac Nq\right)^q$$

**② 第二個因子：** 寫成指數，用 $\ln(1+x)\approx x$：

$$\left(1+\frac qN\right)^N=e^{N\ln(1+q/N)}\approx e^{N\cdot q/N}=e^q$$

**③ 合起來：**

$$\Omega\approx\left(\frac Nq\right)^qe^q=\left(\frac{eN}q\right)^q$$

論證：(a) 的式子對 $q\leftrightarrow N$ 對稱（除了根號），所以把 (c) 的 $q$、$N$ 對調即得。

$$\boxed{\Omega\simeq\left(\frac{eN}q\right)^q\qquad(q\ll N)}$$

## tk-115-5

符號：A、B 兩個愛因斯坦固體，$N_A=10$、$N_B=20$；共 $q=q_A+q_B=60$ 份能量且固定；弱耦合，熱平衡時微觀態等機率；答案可寫成組合數。

### (a) 巨觀態數

**① 數 $q_A$ 的可能值：** 巨觀態由 $q_A$ 指定，$q_A=0,1,\dots,60$（$q_B=60-q_A$）。

$$60+1=61$$

$$\boxed{61\text{ 個巨觀態}}$$

### (b) 微觀態數

**① 30 個振子分 60 份能量：** 長時間可及的是整個系統所有的排法，等於 $N_A+N_B=30$ 個振子分 60 份。

公式（愛因斯坦固體多重度）：$\Omega(N,q)=\dbinom{q+N-1}{q}$，其中 $N$ 為振子數、$q$ 為能量份數；本題 $N=N_A+N_B=30$、$q=60$。

代入 $q=60$、$N=30$，$q+N-1=89$：

$$\Omega(\text{all})=\binom{89}{60}=\frac{89!}{60!\,29!}\approx2.24\times10^{23}$$

$$\boxed{\Omega(\text{all})=\frac{89!}{60!\,29!}\approx2.24\times10^{23}}$$

### (c) 能量全在 A 的機率

**① 數這個巨觀態的微觀態：** 微觀態等機率，機率＝$\Omega_A\Omega_B$ ÷ 總數。A 的 10 個振子分 60 份，$\binom{60+9}{60}=\binom{69}{60}$；B 沒有能量只有 1 種。

$$P=\frac{\binom{69}{60}\cdot1}{\binom{89}{60}}=\frac{69!/(60!\,9!)}{89!/(60!\,29!)}=\frac{69!\,29!}{89!\,9!}$$

**② 算出數值：** 用計算機 $\binom{69}{60}=\binom{69}9=5.67\times10^{10}$，代入 (b) 的 $2.24\times10^{23}$：

$$P=\frac{5.67\times10^{10}}{2.24\times10^{23}}=2.5\times10^{-13}$$

$$\boxed{P=\frac{69!\,29!}{89!\,9!}\approx2.5\times10^{-13}}$$

### (d) 處在最可能巨觀態的機率

**① 相鄰兩個巨觀態的比：** 不知道峰在哪個 $q_A$，小系統用「照振子數分」不精確，所以比較相鄰兩個巨觀態的多重度，比值 $\ge1$ 表示還在上升。

由多重度公式，A 多一份時 $\dfrac{\Omega(N_A,q_A+1)}{\Omega(N_A,q_A)}=\dfrac{q_A+N_A}{q_A+1}$；B 同時少一份時 $\dfrac{\Omega(N_B,q_B-1)}{\Omega(N_B,q_B)}=\dfrac{q_B}{q_B+N_B-1}$。$\Omega_{\text{total}}$ 繼續增加的條件是兩者相乘 $\ge1$：

$$(q_A+N_A)\,q_B\ \ge\ (q_A+1)(q_B+N_B-1)$$

代入 $N_A=10$、$N_B=20$ 與 $q_B=60-q_A$：

$$(q_A+10)(60-q_A)\ \ge\ (q_A+1)(79-q_A)$$

**② 解不等式找峰：** 兩邊展開，$-q_A^2$ 互相消掉：

$$-q_A^2+50q_A+600\ \ge\ -q_A^2+78q_A+79$$

$$521\ \ge\ 28\,q_A\quad\Longleftrightarrow\quad q_A\le18.6$$

所以 $q_A=18$ 時比值 $\gt1$（$\Omega(19)\gt\Omega(18)$），$q_A=19$ 時比值 $\lt1$（$\Omega(20)\lt\Omega(19)$）：最可能的巨觀態是 $q_A=19,\ q_B=41$。

**③ 最可能巨觀態的機率：** $\Omega_A(10,19)=\binom{19+9}{19}=\binom{28}{19}$，$\Omega_B(20,41)=\binom{41+19}{41}=\binom{60}{41}$：

$$P=\frac{\binom{28}{19}\binom{60}{41}}{\binom{89}{60}}$$

用計算機 $\binom{28}{19}=6.91\times10^{6}$、$\binom{60}{41}=2.04\times10^{15}$，代入 (b) 的 $2.24\times10^{23}$：

$$P=\frac{(6.91\times10^{6})(2.04\times10^{15})}{2.24\times10^{23}}=\frac{1.41\times10^{22}}{2.24\times10^{23}}=0.063$$

$$\boxed{q_A=19\text{，}P=\frac{\binom{28}{19}\binom{60}{41}}{\binom{89}{60}}\approx6.3\%}$$

## tk-115-6

符號：兩態順磁體，$N$ 個偶極、$N\gg1$；$N_\downarrow=N-N_\uparrow$；峰在 $N_\uparrow=N/2$；$x\equiv N_\uparrow-N/2$，即 $N_{\uparrow,\downarrow}=\frac N2\pm x$，峰附近 $|x|\ll N$；寬度用課文 (2.28) 的定義：降到峰值的 $1/e$。

### (a) 峰的高度

**① 多重度代入 Stirling：** 問的是峰的高度（一個具體的數），$2^N$ 前面的根號因子會影響高度，所以必須用含根號的 Stirling。

公式（兩態順磁體多重度）：$\Omega=\dfrac{N!}{N_\uparrow!\,N_\downarrow!}$，其中 $N$ 為偶極總數、$N_\uparrow$、$N_\downarrow$ 為朝上、朝下的個數。

公式（Stirling 近似）：$n!\approx n^ne^{-n}\sqrt{2\pi n}$，其中 $n\gg1$；本題 $n=N,\ N_\uparrow,\ N_\downarrow$。

指數部分：分子 $e^{-N}$，分母 $e^{-N_\uparrow}e^{-N_\downarrow}=e^{-N}$，約掉。剩下

$$\Omega\approx\frac{N^N}{N_\uparrow^{N_\uparrow}N_\downarrow^{N_\downarrow}}\sqrt{\frac{2\pi N}{2\pi N_\uparrow\cdot2\pi N_\downarrow}}=\frac{N^N}{N_\uparrow^{N_\uparrow}N_\downarrow^{N_\downarrow}}\sqrt{\frac N{2\pi N_\uparrow N_\downarrow}}$$

**② 代入峰的位置：** 代入 $N_\uparrow=N_\downarrow=N/2$。主要部分：

$$\frac{N^N}{(N/2)^{N/2}(N/2)^{N/2}}=\frac{N^N}{(N/2)^N}=2^N$$

根號部分：

$$\sqrt{\frac N{2\pi(N/2)(N/2)}}=\sqrt{\frac N{\pi N^2/2}}=\sqrt{\frac2{\pi N}}$$

$$\boxed{\Omega_{\max}\approx2^N\sqrt{\frac2{\pi N}}}$$

### (b) 峰附近的公式，證明是高斯函數

**① 取對數，代 $N_{\uparrow,\downarrow}=\frac N2\pm x$：** $\Omega$ 太大不好直接展開，照課文 (2.25)–(2.27)：先取 $\ln\Omega$，在 $x\ll N$ 展開到 $x^2$，再取指數。

對 (a) ① 的結果取 $\ln$，把兩個含 $x$ 的對數項合稱 $f(x)$：

$$\ln\Omega=N\ln N-f(x)+\frac12\ln\frac N{2\pi N_\uparrow N_\downarrow}$$

$$f(x)=\left(\tfrac N2+x\right)\ln\left(\tfrac N2+x\right)+\left(\tfrac N2-x\right)\ln\left(\tfrac N2-x\right)$$

根號裡 $N_\uparrow N_\downarrow=(\frac N2+x)(\frac N2-x)=(\frac N2)^2-x^2$。

**② 把 $f(x)$ 重排：** 係數本身也含 $x$，直接把對數只展開到一次會漏掉一半的 $x^2$，所以先把係數拆成 $\frac N2$ 與 $\pm x$ 兩部分分別收集：

$$\begin{aligned}f={}&\tfrac N2\Big[\ln\left(\tfrac N2+x\right)+\ln\left(\tfrac N2-x\right)\Big]\\&+x\Big[\ln\left(\tfrac N2+x\right)-\ln\left(\tfrac N2-x\right)\Big]\end{aligned}$$

對數相加變乘、相減變除：

$$f=\frac N2\ln\left[\left(\tfrac N2\right)^2-x^2\right]+x\ln\frac{N/2+x}{N/2-x}$$

**③ 兩項各自展開到 $x^2$：** 第一項提出 $(N/2)^2$，用小量的對數近似。

公式（小量的對數）：$\ln(1+\epsilon)\approx\epsilon$，其中 $|\epsilon|\ll1$；本題第一項 $\epsilon=-(2x/N)^2$，第二項 $\epsilon=\pm2x/N$。

$$\ln\left[\left(\tfrac N2\right)^2\left(1-\tfrac{4x^2}{N^2}\right)\right]\approx2\ln\frac N2-\frac{4x^2}{N^2}$$

乘上 $\frac N2$：$N\ln\frac N2-\frac{2x^2}N$。

第二項分子分母各除以 $N/2$：

$$\ln\frac{1+2x/N}{1-2x/N}\approx\frac{2x}N-\left(-\frac{2x}N\right)=\frac{4x}N$$

乘上 $x$：$\frac{4x^2}N$。兩項相加：

$$f(x)\approx N\ln\frac N2-\frac{2x^2}N+\frac{4x^2}N=N\ln\frac N2+\frac{2x^2}N$$

（第二項前面已經乘了 $x$，對數展開到一次就給出 $x^2$；兩項的下一階都是 $x^4/N^3$，可忽略。）

**④ 根號那一項：** $(\frac N2)^2-x^2=(\frac N2)^2[1-(2x/N)^2]$，修正是 $x^2/N^2$ 的量級，比指數裡的 $2x^2/N$ 小了 $N$ 倍，丟掉：

$$\frac12\ln\frac N{2\pi[(N/2)^2-x^2]}\approx\frac12\ln\frac N{2\pi N^2/4}=\ln\sqrt{\frac2{\pi N}}$$

**⑤ 合起來：** 把 ③ 的 $f(x)$ 和 ④ 的根號項代回 ① 的 $\ln\Omega$：

$$\ln\Omega\approx N\ln N-N\ln\frac N2-\frac{2x^2}N+\ln\sqrt{\frac2{\pi N}}$$

$N\ln N-N\ln\frac N2=N\ln2$。取指數：

$$\Omega(x)\approx2^N\sqrt{\frac2{\pi N}}\;e^{-2x^2/N}$$

指數是 $-(\text{正常數})\times x^2$，所以是以 $x=0$ 為中心的高斯函數。

**⑥ 檢查 $x=0$：** $x=0$ 時 $e^0=1$，回到 (a) 的 $2^N\sqrt{2/(\pi N)}$。

$$\boxed{\Omega(x)\approx2^N\sqrt{\frac2{\pi N}}\,e^{-2x^2/N}\text{（高斯函數，}x=0\text{ 時回到 (a)）}}$$

### (c) 峰的寬度

**① 令 $\Omega$ 降到峰值的 $1/e$：** 高斯函數沒有明確邊界，用課文的 $1/e$ 定義寬度。

$$e^{-2x^2/N}=e^{-1}\ \Longrightarrow\ \frac{2x^2}N=1\ \Longrightarrow\ x=\pm\sqrt{\frac N2}$$

**② 全寬：**

$$\text{全寬}=2\sqrt{\frac N2}=\sqrt{2N}$$

相對於整個範圍 $N$（$N_\uparrow$ 從 0 到 $N$），寬度只佔 $\sqrt{2N}/N=\sqrt{2/N}$；例如 $N=10^{20}$ 時是 $1.4\times10^{-10}$。

$$\boxed{1/e\text{ 半寬 }\sqrt{N/2}\text{，全寬 }\sqrt{2N}}$$

## tk-115-7

符號：二維單原子理想氣體，$N$ 個不可分辨的分子、面積 $A$、總能量 $U=\sum_i\frac{p_{ix}^2+p_{iy}^2}{2m}$；題目給三維範本 $\Omega_N\simeq\frac1{N!}\frac{V^N}{h^{3N}}\frac{\pi^{3N/2}}{(3N/2)!}(\sqrt{2mU})^{3N}$；答案以 $U,m,N,A$ 表示。

**① 一個分子：** 照三維的推導逐項改成二維：位置空間由 $V$ 變成 $A$，動量只有兩個分量，每個方向貢獻一個 $1/h$。

公式（相空間狀態數 (2.33)）：一維時獨立狀態數為 $\dfrac{L\,L_p}{h}$，其中 $L$ 為位置範圍長度、$L_p$ 為動量範圍長度、$h$ 為普朗克常數；本題二維有 $x$、$y$ 兩個方向，各給一個 $h$。

$$\Omega_1=\frac{A\,A_p}{h^2}$$

$A_p$ 是動量空間中可用的「面積」：能量 $U=\frac{p_x^2+p_y^2}{2m}$ 固定，就是動量平面上 $p_x^2+p_y^2=2mU$ 這個半徑 $\sqrt{2mU}$ 的圓周。

**② $N$ 個不可分辨的分子：** 每個分子各給一個 $A/h^2$，$N$ 個是 $A^N/h^{2N}$；不可分辨，互換的 $N!$ 種只算一次；只有總能量受限：

$$p_{1x}^2+p_{1y}^2+\cdots+p_{Nx}^2+p_{Ny}^2=2mU$$

這是 $2N$ 個平方和，即 $2N$ 維動量空間中半徑 $\sqrt{2mU}$ 的超球面：

$$\Omega_N=\frac1{N!}\frac{A^N}{h^{2N}}\times(2N\text{ 維超球面面積})$$

**③ 代入超球面面積公式：** 用考卷給的公式，取 $d=2N$、$r=\sqrt{2mU}$。

公式（$d$ 維超球面面積 (2.39)）：$\dfrac{2\pi^{d/2}}{(d/2-1)!}r^{d-1}$，其中 $d$ 為維度、$r$ 為半徑；本題 $d=2N$、$r=\sqrt{2mU}$、$d/2-1=N-1$。

$$\text{面積}=\frac{2\pi^N}{(N-1)!}\left(\sqrt{2mU}\right)^{2N-1}$$

和三維一樣，用 $(N-1)!=N!/N$ 與 $r^{2N-1}=r^{2N}/r$ 把階乘補成 $N!$、次方補成 $2N$：

$$\text{面積}=\frac{2N}{\sqrt{2mU}}\cdot\frac{\pi^N}{N!}\left(\sqrt{2mU}\right)^{2N}$$

前面的 $2N/\sqrt{2mU}$ 只是「大的數」，和後面「很大的數」相比可以丟掉（三維時丟掉的是同類的 $3N/\sqrt{2mU}$）：

$$\text{面積}\approx\frac{\pi^N}{N!}(2mU)^N$$

**④ 結果：** 把上一步的面積代回 ② 的式子：

$$\Omega_N\approx\frac1{N!}\frac{A^N}{h^{2N}}\frac{\pi^N}{N!}(2mU)^N$$

$A^N$、$\pi^N$、$(2mU)^N$、$h^{-2N}$ 都是 $N$ 次方，可以合併：

$$\Omega_N\approx\frac{1}{(N!)^2}\left(\frac{2\pi mUA}{h^2}\right)^N$$

$$\boxed{\Omega_N\approx\frac1{N!}\frac{A^N}{h^{2N}}\frac{\pi^N}{N!}(2mU)^N=\frac1{(N!)^2}\left(\frac{2\pi mUA}{h^2}\right)^N}$$


## tk1-114-2

符號：$m$ 為分子質量，$T$ 為溫度，$k=1.381\times10^{-23}\ \text{J/K}$；室溫取 $T=300\ \text{K}$；分子量 H$_2$ 為 2.016、O$_2$ 為 32.00，$1\ \text{u}=1.6605\times10^{-27}\ \text{kg}$（題目沒給，查表）。

### (a) 方均根速率的公式

**① 三個平移自由度：** 速率只和平移動能有關，三維平移有三個平方項，各分到 $\tfrac12kT$；雙原子分子的轉動自由度不影響速率，不算進去。

公式（均分定理）：每個二次自由度的平均能量為 $\tfrac12kT$，其中 $k$ 為波茲曼常數、$T$ 為溫度；本題三維平移有 $\tfrac12mv_x^2$、$\tfrac12mv_y^2$、$\tfrac12mv_z^2$ 三項。

$$\tfrac12m\overline{v^2}=\tfrac12m\overline{v_x^2}+\tfrac12m\overline{v_y^2}+\tfrac12m\overline{v_z^2}=3\cdot\tfrac12kT$$

**② 解出 $v_{\text{rms}}$：** 兩邊乘 $2/m$ 再開根號。

$$v_{\text{rms}}\equiv\sqrt{\overline{v^2}}=\sqrt{\frac{3kT}m}$$

$$\boxed{v_{\text{rms}}=\sqrt{\frac{3kT}m}}$$

### (b) 室溫下氫分子的 $v_{\text{rms}}$

**① 氫分子的質量：** 代入分子量 2.016 與 $1\ \text{u}=1.6605\times10^{-27}\ \text{kg}$：

$$m_{\text{H}_2}=2.016\times1.6605\times10^{-27}\ \text{kg}=3.348\times10^{-27}\ \text{kg}$$

**② 代入 (a) 的公式：** 代入 $k=1.381\times10^{-23}\ \text{J/K}$、$T=300\ \text{K}$ 和上一步的 $m_{\text{H}_2}$：

$$\begin{aligned}v_{\text{rms}}&=\sqrt{\frac{3(1.381\times10^{-23})(300)}{3.348\times10^{-27}}}\ \text{m/s}\\&=\sqrt{3.71\times10^6}\ \text{m/s}=1.93\times10^3\ \text{m/s}\end{aligned}$$

$$\boxed{v_{\text{rms}}\approx1.93\times10^3\ \text{m/s}\approx1.9\times10^3\ \text{m/s}}$$

### (c) 氫與氧誰快、快幾倍

**① 同溫度下比較：** 熱平衡表示同溫度，兩種分子平均平移動能相同，所以 $v_{\text{rms}}\propto m^{-1/2}$；兩式相除，$3kT$ 消掉，只需要質量比。

$$\frac{v_{\text{rms,H}_2}}{v_{\text{rms,O}_2}}=\sqrt{\frac{m_{\text{O}_2}}{m_{\text{H}_2}}}$$

**② 代入分子量：** 代入 32.00 與 2.016：

$$\sqrt{\frac{32.00}{2.016}}=\sqrt{15.9}=3.98\approx4$$

$$\boxed{\text{氫分子較快，約 }4\text{ 倍}}$$

## tk-114-3

符號：$N$ 個粒子的單原子理想氣體，$PV=NkT$；單原子只有 3 個平移二次自由度，$U=\tfrac32NkT$；$\gamma=C_P/C_V$。

### (a) 熱力學第一定律

**① 寫出定律：** 把熱也算成一種能量傳遞之後的能量守恆。

$$\Delta U=Q+W$$

系統內能的變化，等於流入系統的熱 $Q$ 加上外界對系統做的功 $W$。

$$\boxed{\Delta U=Q+W}$$

### (b) $C_V$ 與 $C_P$ 的關係

**① 定容熱容量：** 理想氣體的 $U$ 只和 $T$ 有關；定容時外界不做功 $W=0$，第一定律給 $Q=\Delta U$。

公式（熱容量定義）：$C=\dfrac{Q}{\Delta T}$，即每升高 1 K 要吸的熱，其中 $Q$ 為吸收的熱、$\Delta T$ 為溫度變化；本題定容時 $Q=\Delta U$。

$$C_V=\left(\frac{\partial U}{\partial T}\right)_V$$

代入 $U=\tfrac32NkT$：

$$C_V=\frac32Nk$$

**② 定壓熱容量：** 定壓時氣體膨脹，外界做的功 $W=-P\Delta V$，所以 $Q=\Delta U-W=\Delta U+P\Delta V$；多出來的就是對外做功那一份。

$$C_P=\left(\frac{\partial U}{\partial T}\right)_P+P\left(\frac{\partial V}{\partial T}\right)_P$$

**③ 用 $PV=NkT$ 算第二項：** $U$ 只和 $T$ 有關，第一項就是 $C_V$。

公式（理想氣體方程）：$PV=NkT$，其中 $P$ 為壓力、$V$ 為體積、$N$ 為粒子數、$k$ 為波茲曼常數、$T$ 為溫度；本題 $P$ 固定時 $V=NkT/P$。

$$\left(\frac{\partial V}{\partial T}\right)_P=\frac{Nk}P\quad\Longrightarrow\quad P\left(\frac{\partial V}{\partial T}\right)_P=Nk$$

$$C_P=C_V+Nk=\frac52Nk$$

$$\boxed{C_P=C_V+Nk\quad\left(C_V=\tfrac32Nk,\ C_P=\tfrac52Nk\right)}$$

### (c) 證明準靜態絕熱過程 $PV^\gamma=$ 常數

**① 寫出微分方程：** 絕熱 $Q=0$，第一定律變成 $dU=-P\,dV$；代入 $dU=C_V\,dT$、$P=NkT/V$ 後，變數可以分離。

$$C_V\,dT=-\frac{NkT}V\,dV$$

**② 分離變數：** 兩邊除以 $C_VT$。由 (b)，$Nk=C_P-C_V$，所以 $\dfrac{Nk}{C_V}=\dfrac{C_P}{C_V}-1=\gamma-1$：

$$\frac{dT}T=-\frac{Nk}{C_V}\frac{dV}V=-(\gamma-1)\frac{dV}V$$

**③ 積分：** $\int dT/T=\ln T$，$\int dV/V=\ln V$：

$$\ln T=-(\gamma-1)\ln V+\text{常數}$$

$$\ln T+\ln V^{\gamma-1}=\text{常數}\ \Longrightarrow\ TV^{\gamma-1}=\text{常數}$$

**④ 換成 $P$、$V$：** 由 $PV=NkT$，$T=PV/(Nk)$；$Nk$ 是常數，併進右邊：

$$\frac{PV}{Nk}V^{\gamma-1}=\text{常數}\ \Longrightarrow\ PV^\gamma=\text{常數}$$

代入 (b) 的 $C_V$、$C_P$（單原子）：

$$\gamma=\frac{C_P}{C_V}=\frac{5/2}{3/2}=\frac53$$

$$\boxed{PV^\gamma=\text{常數}\text{（得證）},\quad\gamma=\tfrac53}$$

### (d) 理想氣體的熵

**① 取對數並用 Stirling：** 熵是多重度的對數；把 $(\sqrt{2mU})^{3N}=(2mU)^{3N/2}$ 和 $\pi$、$h$ 的次方合併，兩個階乘用 Stirling 近似。

公式（熵的定義）：$S=k\ln\Omega$，其中 $k$ 為波茲曼常數、$\Omega$ 為多重度；本題 $\Omega=\Omega_N$。

公式（Stirling 近似）：$\ln n!\approx n\ln n-n$，其中 $n$ 為大整數；本題 $n=N$ 與 $n=\tfrac{3N}2$。

$$\begin{aligned}\frac Sk\approx{}&N\ln V+\tfrac{3N}2\ln\tfrac{2\pi mU}{h^2}\\&-(N\ln N-N)-\left(\tfrac{3N}2\ln\tfrac{3N}2-\tfrac{3N}2\right)\end{aligned}$$

**② 整理成 Sackur–Tetrode：** $N\ln V-N\ln N=N\ln\frac VN$；$\frac{3N}2\big[\ln\frac{2\pi mU}{h^2}-\ln\frac{3N}2\big]=\frac{3N}2\ln\frac{4\pi mU}{3Nh^2}$；常數 $N+\frac{3N}2=\frac52N$：

$$S=Nk\left[\ln\left(\frac VN\left(\frac{4\pi mU}{3Nh^2}\right)^{3/2}\right)+\frac52\right]$$

$$\boxed{S=Nk\left[\ln\left(\frac VN\left(\frac{4\pi mU}{3Nh^2}\right)^{3/2}\right)+\frac52\right]\ \text{（Sackur–Tetrode）}}$$

### (e) 溫度 $T$ 表示成 $U$、$k$、$N$

**① 只有含 $U$ 的項有貢獻：** 偏微分時 $V$、$N$ 固定，只有 $\frac{3N}2k\ln U$ 含 $U$，不必整個式子都微分。把對數裡的 $U^{3/2}$ 拆出來：

$$S=\frac32Nk\ln U+C(V,N)$$

其中 $C(V,N)$ 不含 $U$。

**② 對 $U$ 偏微分：** 代入題目給的溫度定義 $\dfrac1T=\dfrac{\partial S}{\partial U}$：

$$\frac1T=\left(\frac{\partial S}{\partial U}\right)_{V,N}=\frac32\frac{Nk}U\quad\Longrightarrow\quad T=\frac{2U}{3Nk}$$

$$\boxed{T=\frac{2U}{3Nk}\quad\left(\text{即 }U=\tfrac32NkT\right)}$$

## tk-114-4

符號：A 有 $N_A=3$ 個振子、B 有 $N_B=2$ 個振子，$q_A+q_B=5$ 固定（能量單位 $\epsilon$）；所有微觀態等機率。

### (a) $q_A=1$ 時的 $\Omega_A$

**① 示意圖：** 用圓圈代表一份能量、直線代表振子之間的隔板。A 有 3 個振子，需要 $N_A-1=2$ 條隔線；$q_A=1$ 是 1 個圓圈，可以放在三個位置之一：

$$\circ\,|\,|\qquad|\,\circ\,|\qquad|\,|\,\circ$$

**② 用多重度公式：** 代入 $N_A=3$、$q_A=1$。

公式（愛因斯坦固體多重度）：$\Omega(N,q)=\dbinom{q+N-1}{q}$，其中 $N$ 為振子數、$q$ 為能量單位數；本題 $N=N_A=3$、$q=q_A=1$。

$$\Omega_A=\binom{1+3-1}{1}=\binom31=3$$

那一份能量可以在三個振子中的任一個。

$$\boxed{\Omega_A=3}$$

### (b) 列出所有 $q_A$、$q_B$ 與多重度

**① 兩個固體各自的多重度公式：** 代入 $N_A=3$ 與 $N_B=2$：

$$\Omega_A=\binom{q_A+2}{q_A}=\frac{(q_A+2)(q_A+1)}2$$

$$\Omega_B=\binom{q_B+1}{q_B}=q_B+1$$

**② 代入各個 $q$：** 代入 $q_A=0,\dots,5$ 得 $\Omega_A=1,3,6,10,15,21$；代入 $q_B=5-q_A=5,\dots,0$ 得 $\Omega_B=6,5,4,3,2,1$。

**③ 相乘列表：** A 的每個微觀態可以配 B 的任一個，所以 $\Omega_{\text{total}}=\Omega_A\Omega_B$，例如 $q_A=2$：$6\times4=24$。

$$\begin{array}{c|cccccc}q_A&0&1&2&3&4&5\\\hline q_B&5&4&3&2&1&0\\\Omega_A&1&3&6&10&15&21\\\Omega_B&6&5&4&3&2&1\\\Omega_{\text{total}}&6&15&24&30&30&21\end{array}$$

總和：

$$6+15+24+30+30+21=126$$

$$\boxed{\Omega_{\text{total}}=6,15,24,30,30,21\ \text{（共 }126\text{）}}$$

### (c) 長條圖

**① 畫圖：** 橫軸 $q_A=0,\dots,5$，縱軸 $\Omega_{\text{total}}$。六根長條高度 6、15、24、30、30、21：由左往右上升，在 $q_A=3,4$ 最高，$q_A=5$ 再降下來。

$$\boxed{\text{先升後降，}q_A=3,4\text{ 最高的長條圖}}$$

### (d) 圖的意義

**① 巨觀態機率正比於 $\Omega_{\text{total}}$：** 所有微觀態等機率，所以長條圖的形狀就是能量分配的機率分布。

$$P(q_A)=\frac{\Omega_{\text{total}}(q_A)}{126}$$

**② 代入最高與最低的長條：** 代入 (b) 表中 $q_A=3,4$ 的 30 與 $q_A=0$ 的 6：

$$P(3)=P(4)=\frac{30}{126}=24\%$$

$$P(0)=\frac6{126}=4.8\%$$

**③ 解讀：** 最可能的是 $q_A=3$ 或 4，也就是能量大致依振子數 $3:2$ 分配；能量全集中在一邊（$q_A=0$ 或 5）的機率小得多。所以能量會自發地往「分散」的巨觀態流，這就是熱流方向與第二定律的機率解釋。

$$\boxed{\text{能量傾向依振子數分配，最可能 }q_A=3\text{ 或 }4\text{（各 }24\%\text{）}}$$

## tk-114-5

符號：$V_i=1\ \text{L}=1.0\times10^{-3}\ \text{m}^3$，$T_i=300\ \text{K}$（室溫），$P=1.013\times10^5\ \text{N/m}^2$ 全程不變，$V_f=2V_i$；空氣當理想氣體，雙原子 $f=5$（3 平移＋2 轉動）。

**① 熵怎麼隨 $V$、$U$ 變：** 熵是狀態函數，只看初、末狀態；多重度的位置部分給 $V^N$，動量部分是 $fN$ 維球面（$fN$ 很大時面積 $\propto U^{(fN-1)/2}\approx U^{fN/2}$）給 $U^{fN/2}$，空氣是雙原子所以用 $f=5$，不能直接套單原子的 Sackur–Tetrode。

$$\Omega=C(N)\,V^NU^{fN/2}$$

**② 取對數求熵：** $\ln$ 把乘積變成相加。

公式（熵的定義）：$S=k\ln\Omega$，其中 $k$ 為波茲曼常數、$\Omega$ 為多重度；本題 $\Omega=C(N)\,V^NU^{fN/2}$。

$$S=k\ln\Omega=Nk\ln V+\frac f2Nk\ln U+k\ln C(N)$$

$C(N)$ 包含 $N!$、$h$、$\pi$、質量等，粒子數不變時是常數。

**③ 熵的變化：** 末狀態減初狀態，$k\ln C(N)$ 消掉；$\ln a-\ln b=\ln\frac ab$：

$$\Delta S=Nk\ln\frac{V_f}{V_i}+\frac f2Nk\ln\frac{U_f}{U_i}$$

第一項來自體積變大，第二項來自能量增加。

**④ 定壓下溫度與內能也變兩倍：** $P$、$N$ 固定，$T\propto V$。

公式（理想氣體方程）：$PV=NkT$，其中 $P$ 為壓力、$V$ 為體積、$N$ 為粒子數、$T$ 為溫度；本題 $T=\dfrac{PV}{Nk}$，$P$、$N$ 固定。

$$\frac{T_f}{T_i}=\frac{V_f}{V_i}=2$$

公式（均分定理）：$U=\frac f2NkT$，其中 $f$ 為每個分子的二次自由度數；本題 $f=5$、$N$ 不變。

$$\frac{U_f}{U_i}=\frac{T_f}{T_i}=2$$

**⑤ 代回 $\Delta S$：** 代入 $V_f/V_i=2$、上一步的 $U_f/U_i=2$、$f=5$：

$$\Delta S=Nk\ln2+\frac52Nk\ln2=\frac72Nk\ln2$$

**⑥ 用初狀態算 $Nk$：** $N$ 沒給，但 $PV=NkT$ 直接給出 $Nk$。代入 $P=1.013\times10^5\ \text{N/m}^2$、$V_i=1.0\times10^{-3}\ \text{m}^3$、$T_i=300\ \text{K}$：

$$Nk=\frac{PV_i}{T_i}=\frac{(1.013\times10^5\ \text{N/m}^2)(1.0\times10^{-3}\ \text{m}^3)}{300\ \text{K}}=\frac{101.3\ \text{J}}{300\ \text{K}}=0.338\ \text{J/K}$$

**⑦ 求數值：** 代入上一步的 $Nk$ 與 $\ln2=0.693$：

$$\Delta S=\frac72(0.338\ \text{J/K})(0.693)=0.82\ \text{J/K}$$

換成純數：

$$\frac{\Delta S}k=\frac{0.82}{1.38\times10^{-23}}=5.9\times10^{22}$$

$$\boxed{\Delta S=\frac72Nk\ln2=\frac72\frac{PV_i}{T_i}\ln2\approx0.82\ \text{J/K}}$$

若取 $P=10^5\ \text{N/m}^2$，結果為 $0.81\ \text{J/K}$，與課本解答相同。

## tk-114-6

符號：$N=20$ 枚公正硬幣，每枚 H、T 機率各 $\tfrac12$、互相獨立；$n$ 為正面數。

### (a) 微觀態總數

**① 乘法原理：** 每枚 2 種結果、彼此獨立。

公式（乘法原理）：$N$ 個獨立物件各有 $k$ 種結果時，總排列數為 $k^N$，其中 $N$ 為物件數、$k$ 為每個物件的結果數；本題 $N=20$、$k=2$。

$$\Omega(\text{all})=2^N$$

代入 $N=20$，$2^{10}=1024$：

$$\Omega(\text{all})=2^{20}=\left(2^{10}\right)^2=1024^2=1\,048\,576$$

$$\boxed{\Omega(\text{all})=2^{20}=1\,048\,576}$$

### (b) 特定序列的機率

**① 一個微觀態的機率：** 「完全照這個順序」把每一枚都指定了，是 $1\,048\,576$ 個等機率微觀態中的一個；也可以想成每一枚都要剛好對，機率各 $\tfrac12$，20 枚相乘。

$$P(\text{序列})=\frac{1}{\Omega(\text{all})}=\left(\frac12\right)^{20}$$

**② 代入 (a) 的結果：** 代入 $\Omega(\text{all})=1\,048\,576$：

$$P(\text{序列})=\frac1{1\,048\,576}=9.54\times10^{-7}$$

$$\boxed{P(\text{序列})=\frac1{2^{20}}\approx9.5\times10^{-7}}$$

### (c) 12 正 8 反的機率

**① 數排法數：** 「任意順序」只指定正面個數，是一個巨觀態，裡面包含很多種排法；從 20 個位置中選 12 個放正面。

公式（二態系統多重度）：$\Omega(N,n)=\dbinom{N}{n}=\dfrac{N!}{n!\,(N-n)!}$，其中 $N$ 為硬幣數、$n$ 為正面數；本題 $N=20$、$n=12$。

$$\Omega(12)=\binom{20}{12}=\frac{20!}{12!\,8!}$$

**② 約分計算：** 分子分母約掉 $12!$，剩下 8 個因子除以 $8!=40\,320$：

$$\Omega(12)=\frac{20\cdot19\cdot18\cdot17\cdot16\cdot15\cdot14\cdot13}{8!}=\frac{5\,079\,110\,400}{40\,320}=125\,970$$

**③ 巨觀態的機率：** 排法數除以總數，代入上一步的 $\Omega(12)=125\,970$ 與 (a) 的 $\Omega(\text{all})=1\,048\,576$：

$$P(12)=\frac{\Omega(12)}{\Omega(\text{all})}=\frac{125\,970}{1\,048\,576}=0.120$$

$$\boxed{P(12)=\frac{125\,970}{2^{20}}\approx0.120=12.0\%}$$

## tk1-114-7

符號：$V_i=1\ \text{L}=10^{-3}\ \text{m}^3$，$P_i=1\ \text{atm}\approx10^5\ \text{Pa}$，$V_f=4\ \text{L}=4\times10^{-3}\ \text{m}^3$；路徑 $P=cV$（$c=P_i/V_i$），所以 $P_f=4\ \text{atm}=4\times10^5\ \text{Pa}$；氦為單原子理想氣體。

**注意：** 原卷把 1 公升寫成 $10^{-3}\,m$，應為 $10^{-3}\ \text{m}^3$。

### (a) PV 圖

**① 畫直線：** $P=cV$ 是通過原點的直線，由 $(1\ \text{L},1\ \text{atm})$ 到 $(4\ \text{L},4\ \text{atm})$，箭頭向右上；底下到 $V$ 軸是梯形，面積就是 $|W|$。

$$\boxed{\text{過原點的直線 }(1\ \text{L},1\ \text{atm})\to(4\ \text{L},4\ \text{atm})}$$

### (b) 對氣體做的功

**① 積分求功：** 壓力隨體積線性上升，直接積分；題目指定焦耳並給了 $1\ \text{atm}\approx10^5\ \text{N/m}^2$，所以用 $10^5$（不是 $1.013\times10^5$）。

公式（準靜態功）：$W=-\displaystyle\int_{V_i}^{V_f}P\,dV$，其中 $W$ 為外界對氣體做的功、$P$ 為壓力、$V$ 為體積；本題 $P=cV$。

$$W=-\int_{V_i}^{V_f}cV\,dV=-\frac c2\left(V_f^2-V_i^2\right)=-\tfrac12\left(P_fV_f-P_iV_i\right)$$

最後一步用 $cV_f^2=P_fV_f$、$cV_i^2=P_iV_i$。

**② 代入數值：** 代入 $P_fV_f=(4\times10^5)(4\times10^{-3})=1600\ \text{J}$、$P_iV_i=(10^5)(10^{-3})=100\ \text{J}$：

$$W=-\tfrac12(1600-100)\ \text{J}=-750\ \text{J}$$

$$\boxed{W=-750\ \text{J}\ \text{（氣體對外做 }750\ \text{J）}}$$

### (c) 氦的能量變化

**① 內能只看初末的 $PV$：** 單原子理想氣體 $U=\tfrac32NkT=\tfrac32PV$。

公式（均分定理）：$U=\frac f2NkT$，其中 $f$ 為每個分子的二次自由度數；本題氦 $f=3$，再用 $PV=NkT$ 得 $U=\tfrac32PV$。

$$\Delta U=\tfrac32\left(P_fV_f-P_iV_i\right)$$

**② 代入數值：** 代入同樣的 $P_fV_f=1600\ \text{J}$、$P_iV_i=100\ \text{J}$：

$$\Delta U=\tfrac32(1500\ \text{J})=2250\ \text{J}$$

$$\boxed{\Delta U=+2250\ \text{J}}$$


## tk1x-1a

符號：容器為長 $L$、活塞面積 $A$ 的圓筒，$V=LA$（任何形狀結果相同）；分子質量 $m$、共 $N$ 個，彼此不交互作用，與器壁做彈性碰撞（撞後 $v_x\to-v_x$，$v_y,v_z$ 不變）；題目允許直接使用 $PV=NkT$。

**① 一個分子對活塞的平均壓力：** 題目只給巨觀的 $PV=NkT$，要的卻是微觀動能，所以先用牛頓定律把 $PV$ 寫成分子速度的函數。單一分子的力是一陣一陣的脈衝，要取時間平均。

公式（牛頓第二、第三定律）：$F=m\,\dfrac{\Delta v}{\Delta t}$，其中 $F$ 為物體受的力、$m$ 為質量、$\Delta v$ 為速度變化、$\Delta t$ 為經過的時間；第三定律：分子施於活塞的力與活塞施於分子的力等大反向。本題取 $x$ 方向。

壓力＝分子施於活塞的力 ÷ 面積，換成活塞施於分子的力（變號）：

$$\overline P=\frac{\overline F_{x,\text{活塞受}}}{A}=\frac{-\overline F_{x,\text{分子受}}}{A}=-\frac{m\,\overline{\left(\Delta v_x/\Delta t\right)}}{A}$$

**② 取一個來回當平均時間：** 分子往返一次走 $2L$，這段時間剛好撞活塞一次（撞側壁不改變 $v_x$）。

$$\Delta t=\frac{2L}{v_x},\qquad \Delta v_x=v_{x,\text{末}}-v_{x,\text{初}}=(-v_x)-v_x=-2v_x$$

**③ 一個分子的 $\overline P$：** 代入上一步的 $\Delta v_x$、$\Delta t$ 與 $V=LA$：

$$\overline P=-\frac mA\cdot\frac{(-2v_x)}{(2L/v_x)}=\frac{mv_x^2}{AL}=\frac{mv_x^2}{V}$$

**④ $N$ 個分子相加：** 分子彼此不交互作用，總壓力是各分子貢獻相加；$N$ 很大時碰撞極頻繁，壓力近似連續，不必再寫平均符號。

$$PV=mv_{1x}^2+mv_{2x}^2+\cdots+mv_{Nx}^2=Nm\,\overline{v_x^2}$$

其中 $\overline{v_x^2}$ 是對所有分子的平均：$\sum_iv_{ix}^2=N\overline{v_x^2}$。

**⑤ 代入理想氣體定律：** 

公式（理想氣體定律）：$PV=NkT$，其中 $P$ 為壓力、$V$ 為體積、$N$ 為粒子數、$k$ 為波茲曼常數、$T$ 為溫度；本題由題目直接給定。

代入 $PV=NkT$，兩邊消去 $N$：

$$NkT=Nm\overline{v_x^2}\ \Longrightarrow\ \frac12m\overline{v_x^2}=\frac12kT$$

**⑥ 三個方向相加：** 分子運動方向隨機，三個方向對等，$\tfrac12m\overline{v_y^2}=\tfrac12m\overline{v_z^2}=\tfrac12kT$；和的平均等於平均的和。

$$\frac12m\langle v^2\rangle=\frac12m\left(\overline{v_x^2}+\overline{v_y^2}+\overline{v_z^2}\right)=\frac12kT+\frac12kT+\frac12kT=\frac32kT\qquad\blacksquare$$

$$\boxed{PV=Nm\overline{v_x^2}=NkT\ \Longrightarrow\ \tfrac12m\langle v^2\rangle=\tfrac32kT}$$

## tk1x-1b

符號：1(a) 的結果 $\tfrac12m\overline{v^2}=\tfrac32kT$（三維單原子理想氣體，只有平移運動）；$v^2=v_x^2+v_y^2+v_z^2$；平衡的氣體沒有特別的方向，$\overline{v_x^2}=\overline{v_y^2}=\overline{v_z^2}$。

**① 把 1(a) 的結果拆成三個方向：** 題目要「以這個結果為例」，所以先把 $\tfrac32kT$ 拆成每個平方項各 $\tfrac12kT$，再推廣。三個方向等價，平均值各占三分之一：

$$\tfrac12m\overline{v_x^2}=\tfrac12m\overline{v_y^2}=\tfrac12m\overline{v_z^2}=\frac13\cdot\frac32kT=\frac12kT$$

每一個平方項 $\tfrac12mv_x^2$ 平均分到 $\tfrac12kT$；三項加起來就是 $\tfrac32kT$。

**② 推廣：均分定理。** 把「平方項」推廣到所有二次形式的能量：

**在溫度 $T$ 的熱平衡中，能量中每一個「座標或速度分量的二次項」（每個二次自由度），平均能量都是 $\tfrac12kT$。** 例如轉動動能 $\tfrac12I\omega_x^2$、彈性位能 $\tfrac12k_sx^2$ 也各分到 $\tfrac12kT$。

$N$ 個分子、每個 $f$ 個二次自由度：

$$U_{\text{thermal}}=Nf\cdot\tfrac12kT$$

1(a) 就是 $f=3$（只有三個平移自由度）的情形：$U=\tfrac32NkT$。

$$\boxed{\begin{gathered}\text{每個二次自由度平均 }\tfrac12kT\\ \tfrac12m\overline{v^2}=3\times\tfrac12kT=\tfrac32kT\\ U_{\text{thermal}}=Nf\cdot\tfrac12kT\end{gathered}}$$

## tk1x-1cd

符號：$PV=NkT$，粒子數 $N$ 固定；單原子 $f=3$；原子間交互作用可忽略，$U$ 只有動能、只和 $T$ 有關；功的慣例 $W$ 為外界對氣體做的功，準靜態時 $W=-P\,dV$。

### (c) 熱力學第一定律

**① 寫出式子與意義：** 題目只問「說明」，寫出式子、各符號意義與正負號慣例即可。

$$\Delta U=Q+W$$

系統內能的變化＝流入系統的熱 $Q$（因溫差而傳入的能量）＋外界對系統做的功 $W$。這是能量守恆用在熱力學系統上。$U$ 是狀態量（只看初末狀態），$Q$ 和 $W$ 是過程量（看路徑），但兩者之和只看初末。對準靜態壓縮，$W=-\int P\,dV$，微小變化寫成 $dU=dQ-P\,dV$。

$$\boxed{\begin{gathered}\Delta U=Q+W\\ \text{內能變化＝吸收的熱＋外界做的功（能量守恆）}\end{gathered}}$$

### (d) $C_P$ 與 $C_V$ 的關係

**① 定容加熱：** 題目指定用第一定律，所以分別寫出定容與定壓的 $dQ$，再用熱容量的定義。體積不變，$dV=0$，沒有壓縮功。

公式（熱容量定義）：$C=\dfrac{dQ}{dT}$，其中 $dQ$ 為吸收的熱、$dT$ 為溫度變化；下標 $V$、$P$ 表示定容、定壓。

$$dQ_V=dU\ \Rightarrow\ C_V=\left(\frac{dQ}{dT}\right)_V=\frac{dU}{dT}$$

公式（均分定理）：每個二次自由度平均能量 $\tfrac12kT$，$U=Nf\cdot\tfrac12kT$，其中 $N$ 為粒子數、$f$ 為每個粒子的二次自由度數；本題單原子 $f=3$。

代入單原子 $U=\tfrac32NkT$：

$$C_V=\frac{d}{dT}\left(\frac32NkT\right)=\frac32Nk$$

**② 定壓加熱：** 壓力不變時氣體膨脹，第一定律移項：

$$dQ_P=dU+P\,dV$$

$U$ 只和 $T$ 有關，所以 $dU=C_V\,dT$（和定容時相同）。定壓下對 $PV=NkT$ 取微分：$P\,dV=Nk\,dT$。代入：

$$dQ_P=C_V\,dT+Nk\,dT\ \Rightarrow\ C_P=\left(\frac{dQ}{dT}\right)_P=C_V+Nk$$

**③ 單原子的數值：** 代入 ① 的 $C_V=\tfrac32Nk$：

$$C_P=\frac32Nk+Nk=\frac52Nk,\qquad\gamma=\frac{C_P}{C_V}=\frac53$$

$$\boxed{C_P=C_V+Nk;\ \text{單原子 }C_V=\tfrac32Nk,\ C_P=\tfrac52Nk}$$

## tk1x-1e

符號：$PV=NkT$；絕熱 $Q=0$；準靜態 $W=-P\,dV$；理想氣體 $U$ 只和 $T$ 有關，$dU=C_V\,dT$；(d) 的結果 $C_P=C_V+Nk$；$\gamma=C_P/C_V$。

**① 第一定律（無限小一段）：** 題目的 $\gamma$ 定義成 $C_P/C_V$，所以證明裡不用自由度，而用 $dU=C_V\,dT$，最後靠 (d) 的 $C_P-C_V=Nk$ 把係數變成 $\gamma-1$。$P$、$V$、$T$ 都在變，先寫無限小一段。

公式（熱力學第一定律）：$dU=dQ+dW$，其中 $dU$ 為內能變化、$dQ$ 為吸收的熱、$dW$ 為外界做的功；本題 $dQ=0$、$dW=-P\,dV$、$dU=C_V\,dT$。

$$C_V\,dT=-P\,dV$$

**② 消去 $P$，係數變成 $\gamma-1$：** 

公式（理想氣體定律）：$PV=NkT$，其中 $P$ 為壓力、$V$ 為體積、$N$ 為粒子數、$k$ 為波茲曼常數、$T$ 為溫度；本題用來寫 $P=NkT/V$。

代入 $P=NkT/V$，兩邊除以 $C_VT$：

$$\frac{dT}T=-\frac{Nk}{C_V}\,\frac{dV}V$$

由 (d) $Nk=C_P-C_V$，所以 $\dfrac{Nk}{C_V}=\dfrac{C_P}{C_V}-1=\gamma-1$：

$$\frac{dT}T=-(\gamma-1)\frac{dV}V$$

**③ 積分：** $C_V$ 不隨溫度變（單原子 $\tfrac32Nk$），$\gamma$ 是常數：

$$\ln T=-(\gamma-1)\ln V+\text{常數}\ \Longrightarrow\ TV^{\gamma-1}=\text{常數}$$

**④ 換回 $P$、$V$：** $T=PV/(Nk)$，$Nk$ 併進常數：

$$\frac{PV}{Nk}V^{\gamma-1}=\text{常數}\ \Longrightarrow\ PV^\gamma=\text{常數}$$

單原子：$C_V=\tfrac32Nk$、$C_P=\tfrac52Nk$（(d)），$\gamma=\tfrac53$。

$$\boxed{PV^\gamma=\text{常數},\ \gamma=C_P/C_V\ (\text{單原子 }\tfrac53)}$$

## sc-1-17

符號：維里展開 $PV=nRT\left(1+\dfrac{B(T)}{(V/n)}+\dfrac{C(T)}{(V/n)^2}+\cdots\right)$，$B$、$C$ 為第二、第三維里係數；凡得瓦方程式 $\left(P+\dfrac{an^2}{V^2}\right)(V-nb)=nRT$，$a$、$b$ 為依氣體而定的常數；低密度 $nb/V\ll1$。求以 $a$、$b$ 表示的 $B$、$C$。

**① 把凡得瓦方程式寫成維里形式：** 維里展開是「$PV/nRT$ 對 $n/V$ 的冪級數」，所以先解出 $P$、寫成 $PV=nRT\times[\cdots]$，再把 $[\cdots]$ 展開到 $(n/V)^2$ 對照係數。解出 $P$，再提出 $nRT/V$：

$$P=\frac{nRT}{V-nb}-\frac{an^2}{V^2}\ \Longrightarrow\ PV=nRT\left[\frac{1}{1-nb/V}-\frac{an}{RTV}\right]$$

**② 二項式展開：** 

公式（二項式展開）：$(1+x)^p\approx1+px+\tfrac12p(p-1)x^2$，條件 $|px|\ll1$，其中 $x$ 為小量、$p$ 為指數；本題 $x=-nb/V$、$p=-1$。

$$\Big[1-\frac{nb}{V}\Big]^{-1}\approx1+(-1)\Big(-\frac{nb}V\Big)+\frac12(-1)(-2)\Big(\frac{nb}V\Big)^2=1+\frac{b}{V/n}+\frac{b^2}{(V/n)^2}$$

**③ 代回、對照係數：** 把 $\dfrac{an}{RTV}$ 寫成 $\dfrac{a/RT}{V/n}$：

$$PV\approx nRT\left[1+\frac{b-a/RT}{V/n}+\frac{b^2}{(V/n)^2}\right]$$

對照維里展開的各項：

$$B(T)=b-\frac{a}{RT},\qquad C(T)=b^2$$

$a,b\gt0$：低溫 $a/RT$ 大，$B\lt0$；高溫 $B\to b\gt0$。

$$\boxed{B=b-\frac a{RT},\qquad C=b^2}$$

## tkx-1j

符號：$\Omega_N\simeq\dfrac1{N!}\dfrac{V^N}{h^{3N}}\dfrac{\pi^{3N/2}}{(3N/2)!}\left(\sqrt{2mU}\right)^{3N}$，$U$ 只有動能；$V$、$N$ 固定；$N$ 很大。

**① 熵：** 本小題只有 3 分，熵寫到 Sackur–Tetrode 式即可；而且 $\Omega$ 對 $U$ 的依賴只有 $(2mU)^{3N/2}$ 一個因子，取對數後對 $U$ 微分只剩一項。

公式（熵的定義）：$S=k\ln\Omega$，其中 $S$ 為熵、$k$ 為波茲曼常數、$\Omega$ 為多重度；本題 $\Omega=\Omega_N$。

公式（Stirling 近似）：$\ln n!\approx n\ln n-n$，其中 $n$ 為大的正整數；本題 $n=N$ 與 $n=3N/2$。

取 $\ln$，兩個階乘用 Stirling，整理後（代數同習題 2.31）：

$$S=k\ln\Omega_N\approx Nk\left[\ln\left(\frac VN\left(\frac{4\pi mU}{3Nh^2}\right)^{3/2}\right)+\frac52\right]$$

**② 找出含 $U$ 的項：** 對數裡的 $U^{3/2}$ 拆出來，$Nk\ln U^{3/2}=\tfrac32Nk\ln U$，其餘都不含 $U$：

$$S=\frac32Nk\ln U+C(V,N)$$

$C(V,N)$ 包含 $\ln\frac VN$、$m$、$h$、$\frac52$ 等，$V$、$N$ 固定時是常數。

**③ 溫度：** 

公式（溫度的熱力學定義）：$\dfrac1T=\left(\dfrac{\partial S}{\partial U}\right)_{V,N}$，其中 $T$ 為溫度、$S$ 為熵、$U$ 為內能，偏微分時 $V$、$N$ 固定。

用 $\frac d{dU}\ln U=\frac1U$：

$$\frac1T=\left(\frac{\partial S}{\partial U}\right)_{V,N}=\frac{3Nk}{2U}$$

取倒數：

$$T=\frac{2U}{3Nk}$$

$$\boxed{S\approx Nk\left[\ln\left(\frac VN\left(\frac{4\pi mU}{3Nh^2}\right)^{3/2}\right)+\frac52\right],\qquad T=\frac{2U}{3Nk}}$$

## tkx-2

符號：$N$ 為振子數、$q$ 為能量量子數，$N,q\gg1$；$U=q\epsilon$；精確多重度 $\Omega(N,q)=\dfrac{(q+N-1)!}{q!\,(N-1)!}$。

### (a) 用 Stirling 證明多重度近似式

**① 改寫成完整階乘：** Stirling 只能代入完整的階乘，所以先改寫 $(N-1)!$、$(q+N-1)!$。

公式（愛因斯坦固體多重度）：$\Omega(N,q)=\dfrac{(q+N-1)!}{q!\,(N-1)!}$，其中 $N$ 為振子數、$q$ 為能量單位數。

$(N-1)!=\dfrac{N!}N$、$(q+N-1)!=\dfrac{(q+N)!}{q+N}$，所以

$$\Omega=\frac N{q+N}\cdot\frac{(q+N)!}{q!\,N!}$$

**② 三個階乘代入 Stirling：** 

公式（Stirling 近似）：$n!\simeq n^ne^{-n}\sqrt{2\pi n}$，其中 $n$ 為大的正整數；本題 $n$ 依序為 $q+N$、$q$、$N$。

$$\begin{aligned}\Omega&\approx\frac N{q+N}\cdot\frac{(q+N)^{q+N}e^{-(q+N)}\sqrt{2\pi(q+N)}}{q^qe^{-q}\sqrt{2\pi q}\cdot N^Ne^{-N}\sqrt{2\pi N}}\\&=\frac{(q+N)^{q+N}}{q^q\,N^N}\sqrt{\frac N{2\pi q(q+N)}}\end{aligned}$$

$e$ 的次方 $-(q+N)+q+N=0$ 抵消；根號是 $\dfrac N{q+N}\sqrt{\dfrac{q+N}{2\pi qN}}=\sqrt{\dfrac{N}{2\pi q(q+N)}}$。

**③ 分配次方：** 把 $(q+N)^{q+N}=(q+N)^q(q+N)^N$ 分給兩個分母：

$$\Omega\approx\frac{\left(\frac{q+N}q\right)^q\left(\frac{q+N}N\right)^N}{\sqrt{2\pi q(q+N)/N}}$$

$$\boxed{\Omega(N,q)\simeq\frac{\left(\frac{q+N}q\right)^q\left(\frac{q+N}N\right)^N}{\sqrt{2\pi q(q+N)/N}}}$$

### (b) 化學勢

**① 熵：** $\mu$ 要在 $U$ 固定（也就是 $q$ 固定）時對 $N$ 微分。根號因子只是 $\ln$ 等級，對熵和它的微分都沒有影響，所以熵用

公式（熵的定義）：$S=k\ln\Omega$，其中 $k$ 為波茲曼常數、$\Omega$ 為多重度；本題用 (a) 去掉根號後的 $\Omega$。

$$S=k\big[(q+N)\ln(q+N)-q\ln q-N\ln N\big]$$

**② 對 $N$ 微分：** $q$ 固定時 $-q\ln q$ 是常數；用 $\frac{d}{dx}(x\ln x)=\ln x+1$：

$$\frac{\partial S}{\partial N}=k\Big[\ln(q+N)+1-\ln N-1\Big]=k\ln\frac{q+N}N$$

**③ 代入化學勢定義：** 

公式（化學勢的定義）：$\mu=-T\left(\dfrac{\partial S}{\partial N}\right)_{U,V}$，其中 $\mu$ 為化學勢、$T$ 為溫度，偏微分時 $U$、$V$ 固定；本題 $U$ 固定即 $q$ 固定。

$$\mu=-T\frac{\partial S}{\partial N}=-kT\ln\left(1+\frac qN\right)$$

$$\boxed{\mu=-kT\ln\left(1+\frac qN\right)}$$

### (c) 高溫極限 $q\gg N$

**① 取極限：** 極限中 $N/q$ 是小數，用 $\ln(1+x)\approx x$。令 $x=N/q\ll1$：

$$\left(1+\frac Nq\right)^q=e^{q\ln(1+N/q)}\approx e^{q\cdot N/q}=e^N$$

又 $\frac{q+N}N\approx\frac qN$；根號只是大的因子，可丟：

$$\Omega\approx e^N\left(\frac qN\right)^N=\left(\frac{eq}N\right)^N$$

**② 為什麼叫高溫：** 每個振子平均有 $q/N\gg1$ 份能量，$U/N\gg\epsilon$，能階間隔相對很小、量子化看不出來（$kT\gg\epsilon$）。

$$\boxed{\Omega\simeq\left(\frac{eq}N\right)^N;\ \text{每個振子平均能量遠大於 }\epsilon\ (kT\gg\epsilon)}$$

### (d) 低溫極限 $q\ll N$

**① 取極限：** 令 $x=q/N\ll1$，同樣用 $\ln(1+x)\approx x$：

$$\left(1+\frac qN\right)^N=e^{N\ln(1+q/N)}\approx e^q$$

又 $\frac{q+N}q\approx\frac Nq$：

$$\Omega\approx\left(\frac Nq\right)^qe^q=\left(\frac{eN}q\right)^q$$

(a) 的式子對 $q\leftrightarrow N$ 對稱，結果等於把 (c) 的 $q$、$N$ 對調。

$$\boxed{\Omega\simeq\left(\frac{eN}q\right)^q}$$

### (e) 高溫的 $U(T)$、$C_V$ 與均分定理

**① 由 $1/T$ 求 $U$：** 高溫與低溫的 $S$ 形式不同，這裡代入 (c) 的多重度。由 (c)，$S=k\ln\left(\frac{eq}N\right)^N=Nk\left[\ln q-\ln N+1\right]$。

公式（溫度的熱力學定義）：$\dfrac1T=\left(\dfrac{\partial S}{\partial U}\right)_{N,V}$，其中 $T$ 為溫度、$S$ 為熵、$U$ 為內能；本題 $U=q\epsilon$，所以 $\partial/\partial U=\frac1\epsilon\,\partial/\partial q$。

$$\frac1T=\frac{\partial S}{\partial U}=\frac1\epsilon\frac{\partial S}{\partial q}=\frac1\epsilon\cdot\frac{Nk}q=\frac{Nk}{q\epsilon}=\frac{Nk}U$$

**② 熱容量：** 取倒數再乘 $Nk$，對 $T$ 微分：

$$U=NkT,\qquad C_V=\frac{\partial U}{\partial T}=Nk$$

**③ 和均分定理比較：** 

公式（均分定理）：每個二次自由度平均能量 $\tfrac12kT$；本題每個一維振子有動能、位能兩個二次自由度。

每個振子共 $kT$，$N$ 個振子 $U=NkT$，與上面一致。

$$\boxed{U=NkT,\quad C_V=Nk,\quad \text{與均分定理一致}}$$

### (f) 低溫的 $U(T)$、$C_V$ 與均分定理

**① 由 $1/T$ 求 $U$：** 代入 (d) 的多重度，$S=k\,q\ln\frac{eN}q=k[q\ln N-q\ln q+q]$。對 $q$ 微分（$\frac{d}{dq}q\ln q=\ln q+1$）：

$$\frac{\partial S}{\partial q}=k\big[\ln N-(\ln q+1)+1\big]=k\ln\frac Nq$$

$$\frac1T=\frac1\epsilon\frac{\partial S}{\partial q}=\frac k\epsilon\ln\frac Nq\quad\Longrightarrow\quad\frac Nq=e^{\epsilon/kT}$$

解出 $q=Ne^{-\epsilon/kT}$，乘上 $\epsilon$：

$$U=q\epsilon=N\epsilon\,e^{-\epsilon/kT}$$

**② 熱容量：** 對 $T$ 微分，連鎖律 $\frac{d}{dT}\left(-\frac\epsilon{kT}\right)=\frac\epsilon{kT^2}$：

$$C_V=\frac{\mathrm dU}{\mathrm dT}=N\epsilon\,e^{-\epsilon/kT}\cdot\frac\epsilon{kT^2}=Nk\left(\frac\epsilon{kT}\right)^2e^{-\epsilon/kT}$$

**③ 和均分定理比較：** 不一致。$T\to0$ 時 $C_V\to0$（指數式地），遠小於 $Nk$。原因是 $kT\ll\epsilon$，熱擾動連一份能量都給不起，振動自由度被「凍結」；均分定理只在能量單位遠小於 $kT$（古典極限）時成立。

$$\boxed{\begin{gathered}U=N\epsilon\,e^{-\epsilon/kT},\quad C_V=Nk\left(\frac\epsilon{kT}\right)^2e^{-\epsilon/kT}\\ \text{不符合均分定理（自由度凍結）}\end{gathered}}$$

## tkx-3

符號：$N$ 個偶極，$N_\uparrow$ 個向上、$N_\downarrow=N-N_\uparrow$ 個向下；$U=\mu B(N-2N_\uparrow)$。原卷 (b) 的式子沒有 $k$，其實是 $S/k$。

### (a) 多重度

**① 組合數：** 每個偶極只有上、下兩態，一個微觀態就是「哪 $N_\uparrow$ 個偶極向上」的一種選法。

公式（組合數）：$\binom{N}{n}=\dfrac{N!}{n!\,(N-n)!}$，表示從 $N$ 個物件選 $n$ 個的方法數；本題 $n=N_\uparrow$。

$$\Omega(N,N_\uparrow)=\binom N{N_\uparrow}=\frac{N!}{N_\uparrow!\,(N-N_\uparrow)!}$$

$$\boxed{\Omega(N,N_\uparrow)=\frac{N!}{N_\uparrow!\,(N-N_\uparrow)!}}$$

### (b) 證明熵的式子

**① 取對數：** 要證的式子沒有 $\sqrt{2\pi n}$ 項，所以只需要 $\ln n!\approx n\ln n-n$。

公式（熵的定義）：$S=k\ln\Omega$，其中 $k$ 為波茲曼常數、$\Omega$ 為多重度；本題 $\Omega$ 為 (a) 的結果。

對數把除法變減法：

$$\frac Sk=\ln N!-\ln N_\uparrow!-\ln(N-N_\uparrow)!$$

**② 三個階乘用 Stirling：** 

公式（Stirling 近似）：$\ln n!\approx n\ln n-n$，其中 $n$ 為大的正整數；本題 $n$ 依序是 $N$、$N_\uparrow$、$N-N_\uparrow$。

$$\begin{aligned}\frac Sk\approx{}&(N\ln N-N)-(N_\uparrow\ln N_\uparrow-N_\uparrow)\\&-\big[(N-N_\uparrow)\ln(N-N_\uparrow)-(N-N_\uparrow)\big]\end{aligned}$$

**③ 線性項抵消：** $-N+N_\uparrow+(N-N_\uparrow)=0$：

$$\frac Sk\simeq N\ln N-N_\uparrow\ln N_\uparrow-(N-N_\uparrow)\ln(N-N_\uparrow)$$

就是原卷要證的式子（原卷的 $S$ 以 $k$ 為單位）。

$$\boxed{\frac Sk\simeq N\ln N-N_\uparrow\ln N_\uparrow-(N-N_\uparrow)\ln(N-N_\uparrow)}$$

### (c) 峰附近是高斯函數

**① 代 $N_{\uparrow,\downarrow}=\frac N2\pm x$：** 題目只要求證明形狀是高斯，所以直接從 (b) 的 $\ln\Omega$ 出發（少了根號項只影響峰高，不影響形狀）。由 (b)，$\ln\Omega=S/k\approx N\ln N-f(x)$，其中

$$f(x)=\left(\tfrac N2+x\right)\ln\left(\tfrac N2+x\right)+\left(\tfrac N2-x\right)\ln\left(\tfrac N2-x\right)$$

**② 展開到 $x^2$：** 重排成對稱與反對稱兩部分，在 $x\ll N$ 時用 $\ln(1+\delta)\approx\delta$ 展開：第一項的 $\ln\left[1-\left(\tfrac{2x}N\right)^2\right]\approx-\tfrac{4x^2}{N^2}$，第二項的 $\ln\dfrac{1+2x/N}{1-2x/N}\approx\tfrac{4x}N$。

$$\begin{aligned}f(x)&=\frac N2\ln\left[\left(\tfrac N2\right)^2-x^2\right]+x\ln\frac{N/2+x}{N/2-x}\\&\approx\left(N\ln\frac N2-\frac{2x^2}N\right)+\frac{4x^2}N\end{aligned}$$

**③ 取指數：** 把 $f(x)\approx N\ln\frac N2+\frac{2x^2}N$ 代回 $\ln\Omega$：

$$\ln\Omega\approx N\ln N-N\ln\frac N2-\frac{2x^2}N=N\ln2-\frac{2x^2}N$$

$$\Omega\approx2^Ne^{-2x^2/N}=2^N\exp\left[-\frac{2(N_\uparrow-N/2)^2}N\right]$$

這是以 $N_\uparrow=N/2$ 為中心、$1/e$ 半寬 $\sqrt{N/2}$ 的高斯函數。峰高少了 $\sqrt{2/(\pi N)}$，因為 (b) 的 Stirling 沒有根號項；題目只問形狀，不影響。

$$\boxed{\Omega\approx2^Ne^{-2x^2/N},\ \text{以 }N_\uparrow=N/2\text{ 為中心的高斯}}$$

### (d) $S(U)$ 圖與負溫度區

**① 把 $S$ 寫成 $U$ 的函數：** 題目的 $U$ 和 $N_\uparrow$ 是一次關係，可以把 (b) 換成 $S(U)$。由 $U=\mu B(N-2N_\uparrow)$ 解出 $N_\uparrow=\frac12\left(N-\frac U{\mu B}\right)$，$U$ 和 $N_\uparrow$ 一一對應。看三個點：

- $N_\uparrow=N$（全部向上）：$U=-N\mu B$，只有 1 個微觀態，$S=0$。
- $N_\uparrow=0$（全部向下）：$U=+N\mu B$，$S=0$。
- $N_\uparrow=N/2$：$U=0$，(b) 給 $S/k=N\ln N-2\cdot\frac N2\ln\frac N2=N\ln2$，最大。

所以 $S(U)$ 是 $-N\mu B\le U\le N\mu B$ 上、對 $U=0$ 對稱的拱形。

**② 斜率的正負＝溫度的正負：** 

公式（溫度的熱力學定義）：$\dfrac1T=\dfrac{\partial S}{\partial U}$，其中 $T$ 為溫度、$S$ 為熵、$U$ 為內能；溫度的正負就是 $S(U)$ 斜率的正負。

連鎖律 $\frac{\partial S}{\partial U}=\frac{\partial S}{\partial N_\uparrow}\frac{dN_\uparrow}{dU}$。對 (b) 微分（$\frac d{dn}(n\ln n)=\ln n+1$）：

$$\frac1k\frac{\partial S}{\partial N_\uparrow}=-\ln N_\uparrow-1+\ln(N-N_\uparrow)+1=\ln\frac{N_\downarrow}{N_\uparrow}$$

而 $dN_\uparrow/dU=-1/(2\mu B)$，相乘：

$$\frac1T=\frac{\partial S}{\partial U}=\frac k{2\mu B}\ln\frac{N_\uparrow}{N_\downarrow}$$

- $U\lt0$：$N_\uparrow\gt N_\downarrow$，對數為正，$T\gt0$。
- $U\gt0$：$N_\uparrow\lt N_\downarrow$（多數偶極反平行於磁場），對數為負，$T\lt0$，即圖的右半邊。
- $U=0$：$1/T=0$，$T=\pm\infty$。

$$\boxed{\begin{gathered}S(U)\text{ 為對 }U=0\text{ 對稱的拱形}\\ 0\lt U\le N\mu B\text{ 為負溫度區}\\ \left(\frac1T=\frac k{2\mu B}\ln\frac{N_\uparrow}{N_\downarrow}\lt0\right)\end{gathered}}$$

## tk1x-4

符號：(a) 兩粒子質量 $m$、各距質心 $r$、相距 $2r$；(b) $N$ 個粒子、每個平均動能 $\tfrac32kT$；(c) 均勻密度 $\rho=\dfrac{M}{\frac43\pi R^3}$；(d) 太陽 $M=2\times10^{30}\ \text{kg}$、$R=7\times10^8\ \text{m}$，粒子數 $N=2M/m_p$（質子與電子，電子質量可忽略）；常數 $G=6.674\times10^{-11}$、$m_p=1.673\times10^{-27}\ \text{kg}$、$k=1.381\times10^{-23}\ \text{J/K}$（題目沒給，用標準值）。

### (a) 位能與動能的比值

**① 圓周運動條件：** 向心力由兩粒子間的重力提供。

公式（萬有引力與向心力）：$F=\dfrac{Gm_1m_2}{d^2}=\dfrac{mv^2}{r}$，其中 $G$ 為重力常數、$m_1,m_2$ 為兩質量、$d$ 為兩者距離、$v$ 為速率、$r$ 為圓周半徑；本題 $m_1=m_2=m$、$d=2r$。

$$\frac{Gm^2}{(2r)^2}=\frac{mv^2}{r}\ \Rightarrow\ mv^2=\frac{Gm^2}{4r}$$

**② 比值：** 

公式（重力位能）：$U_{\text{pot}}=-\dfrac{Gm_1m_2}{d}$，其中符號同上；本題 $d=2r$。

代入 $U_{\text{kin}}=2\cdot\tfrac12mv^2$、$U_{\text{pot}}=-\dfrac{Gm^2}{2r}$：

$$\frac{U_{\text{pot}}}{U_{\text{kin}}}=\frac{-Gm^2/(2r)}{Gm^2/(4r)}=-2$$

$$\boxed{\frac{U_{\text{pot}}}{U_{\text{kin}}}=-2}$$

### (b) 恆星的熱容量

**① 總能量：** 由均位定理，$U_{\text{pot}}=-2U_{\text{kin}}$：

$$U=U_{\text{kin}}+U_{\text{pot}}=U_{\text{kin}}-2U_{\text{kin}}=-U_{\text{kin}}$$

**② 熱容量：** 

公式（均分定理）：每個二次自由度平均能量 $\tfrac12kT$；本題每個粒子三個平移自由度，平均動能 $\tfrac32kT$。

代入 $U_{\text{kin}}=N\cdot\tfrac32kT$：

$$U=-\frac32NkT,\qquad C=\frac{dU}{dT}=-\frac32Nk\lt0$$

$$\boxed{C=-\tfrac32Nk\ (\text{負值})}$$

### (c) 均勻球的重力位能

**① 一層薄殼的位能：** 密度均勻，想像把恆星一層一層從中心堆起來：每次從無限遠搬來一層薄殼，殼只受內部球的吸引。半徑 $r$ 以內的質量與厚度 $dr$ 的殼質量：

$$m(r)=\rho\cdot\tfrac43\pi r^3=M\frac{r^3}{R^3},\qquad dm=\rho\cdot4\pi r^2dr=\frac{3Mr^2}{R^3}dr$$

公式（球殼定理）：均勻球殼外的質量對殼內物體沒有淨重力，球內質量 $m(r)$ 對半徑 $r$ 處的作用如同集中在球心；本題這層殼的位能為 $-G\,m(r)\,dm/r$。

$$dU_{\text{pot}}=-\frac{G}{r}\cdot\frac{Mr^3}{R^3}\cdot\frac{3Mr^2}{R^3}dr=-\frac{3GM^2}{R^6}r^4\,dr$$

**② 積分到 $R$：** 

$$U_{\text{pot}}=-\frac{3GM^2}{R^6}\int_0^Rr^4\,dr=-\frac{3GM^2}{R^6}\cdot\frac{R^5}{5}=-\frac{3GM^2}{5R}$$

$$\boxed{U_{\text{pot}}=-\frac{3GM^2}{5R}}$$

### (d) 太陽的平均溫度

**① 用均位定理解 $T$：** 把位能換成動能：$U_{\text{kin}}=-\tfrac12U_{\text{pot}}$，左邊用 (b)，右邊用 (c)，$N=2M/m_p$：

$$\frac32\cdot\frac{2M}{m_p}\cdot kT=\frac{3GM^2}{10R}\ \Rightarrow\ T=\frac{GMm_p}{10kR}$$

**② 代入數值：** 代入 $G=6.674\times10^{-11}$、$M=2\times10^{30}\ \text{kg}$、$R=7\times10^8\ \text{m}$、$m_p=1.673\times10^{-27}\ \text{kg}$、$k=1.381\times10^{-23}\ \text{J/K}$：

$$\begin{aligned}T&=\frac{(6.674\times10^{-11})(2\times10^{30})(1.673\times10^{-27})}{10(1.381\times10^{-23})(7\times10^8)}\\&=\frac{2.233\times10^{-7}}{9.667\times10^{-14}}\ \text{K}=2.3\times10^6\ \text{K}\end{aligned}$$

$$\boxed{T\approx2.3\times10^6\ \text{K}}$$
