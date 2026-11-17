# 李孟恩近代光學｜112、114、115 級考古題完整教學

> **閱讀方式：** 相同題型放在一起逐年比較，每題依步驟寫出公式、代入與結果。本文為考卷題意整理及自行演算，不是老師原始解答逐字版。
>
> **來源與日期：** 112 級 2022-04-27、114 級 2024-04-23、115 級 2025-04-22。資料夾的「級」和實際考試年份不同，以下依資料夾名稱標示。

**三份原卷**：112 級｜114 級｜115 級｜114 級附帶的手寫解答

> **2026 年本次考試範圍：** 依老師逐字稿，範圍為第八～十章。原 D 組 TM 反射與透射（三年的第 4 題）**不在此次範圍，已刪除**。新增的舊題與課本補強見 [H 組](#h-組本次新增舊考古與課本第一輪補強不含駐波)：八道完整題解，含電磁波能量密度、球／圓柱波平均能流與都卜勒提醒。

## 一、老師逐字稿與考古題對照

| 分組 | 112 級 | 114 級 | 115 級 | 逐字稿中的說法 |
|---|---|---|---|---|
| **A：同頻率波的疊加** | 第 1 題、20 分 | 第 1 題、20 分 | 第 1 題、20 分 | **第九章：「一定會考」**；同頻率正弦波、相量、振幅和相位 |
| **B：平面電磁波** | 第 2 題、40 分 | 第 2 題、40 分 | 第 2 題、40 分 | **第八章：「一定會考」**；波的表示、Poynting 向量、照度 |
| **C：干涉** | 雙稜鏡、20 分 | 雙波長牛頓環、20 分 | 亮暗牛頓環、20 分 | 第十章**重點**；有點名楊氏干涉／虛擬光源，**沒特別保證牛頓環必考** |

**判斷：** 三份考卷的題序和配分固定，第 1、2 題合計 60 分，正好是老師說「一定會考」的題型。但老師另外提到**球面波、圓柱波的指數表示法、瞬時與平均 Poynting 向量**，也提醒都卜勒效應、相速度／群速度和干涉對比度，所以這三份試題**不等於今年全部範圍**。

**注意：** 112 級第 2 題原卷頻率為 $10^{14}\ \mathrm{Hz}$，不是 $3\times10^{14}\ \mathrm{Hz}$；本文的波長、波數、角頻率及完整相位已依原卷修正。

---

# A 組：第 1 題｜波的疊加（每份 20 分）

**老師逐字稿：** 第九章，明確說「一定會考」。三年都是把四個同頻率的正弦／餘弦波合成一個餘弦波，求**合成振幅**和**初始相位角**。

## A-1. 共同解法：為什麼把波分成 cos 和 sin？

符號：$E$：疊加後的波動量（無指定單位）；$E_0\ge0$：合成振幅；$\alpha$：合成相位（rad 或度）；$\omega$：角頻率（rad/s）；$t$：時間（s）；$A$、$B$：全部 $\cos\omega t$、$\sin\omega t$ 項的係數加總。

**① 每項拆成 cos、sin 兩部分：** 頻率相同，就能用和角公式把每一項展開，再把同類項相加：

$$
\boxed{E=A\cos\omega t+B\sin\omega t}.
$$

**② 對照目標形式：** 題目要求的最後形式是

$$
\boxed{E=E_0\cos(\alpha-\omega t)}.
$$

用 cos 減法公式展開：

$$
\cos(a-b)=\cos a\cos b+\sin a\sin b,
$$

$$
\begin{aligned}
E&=E_0\cos(\alpha-\omega t)\\
 &=E_0\cos\alpha\cos\omega t+E_0\sin\alpha\sin\omega t.
\end{aligned}
$$

與 ① 比較係數：

$$
\boxed{A=E_0\cos\alpha},\qquad
\boxed{B=E_0\sin\alpha}.
$$

**③ 求振幅：** 兩式平方相加，用 $\cos^2\alpha+\sin^2\alpha=1$：

$$
\begin{aligned}
A^2+B^2
&=E_0^2\cos^2\alpha+E_0^2\sin^2\alpha\\
&=E_0^2(\cos^2\alpha+\sin^2\alpha)\\
&=E_0^2.
\end{aligned}
$$

振幅不能為負：

$$
\boxed{E_0=\sqrt{A^2+B^2}}.
$$

**④ 求相位並判斷象限：** 兩式相除：

$$
\boxed{\tan\alpha=\frac{B}{A}}.
$$

$\tan\alpha$ 不能單獨決定象限，要看 $A=E_0\cos\alpha$、$B=E_0\sin\alpha$ 的正負號：

| $A$ | $B$ | $\alpha$ 所在象限 |
|---|---|---|
| 正 | 正 | 第一象限 |
| 負 | 正 | 第二象限 |
| 負 | 負 | 第三象限 |
| 正 | 負 | 第四象限 |

三年都是 $A<0,B>0$，在**第二象限**：

$$
\boxed{\alpha=\pi-\tan^{-1}\left(\frac{|B|}{|A|}\right)}.
$$

最後換到題目指定的相位範圍：112、114 級採 $-\pi<\alpha\le\pi$；115 級採 $0\le\alpha<2\pi$。

**展開用的三角函數：**

$$
\begin{aligned}
\cos(a+b)&=\cos a\cos b-\sin a\sin b,\\
\cos(a-b)&=\cos a\cos b+\sin a\sin b,\\
\sin(a+b)&=\sin a\cos b+\cos a\sin b,\\
\sin(a-b)&=\sin a\cos b-\cos a\sin b.
\end{aligned}
$$

---

## A-2. 112 級第 1 題（20 分）

**題目：**

$$
\begin{aligned}
E={}&-3\cos\left(\frac\pi6+\omega t\right)
+4\sin\left(\frac{2\pi}3+\omega t\right)\\
&+\cos\left(-\frac\pi4+\omega t\right)
-2\sin\left(\frac\pi3-\omega t\right).
\end{aligned}
$$

(a) 求合成振幅 $E_0$（非負）；(b) 求相位 $\alpha$，範圍 $-\pi<\alpha\le\pi$。

**① 展開第一項：** 用 cos 加法公式。

公式（cos 加法公式）：$\cos(a+b)=\cos a\cos b-\sin a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=\dfrac{\pi}{6}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
-3\cos\left(\frac\pi6+\omega t\right).
$$

$$
\begin{aligned}
&=-3\left[\cos\frac\pi6\cos\omega t-\sin\frac\pi6\sin\omega t\right]\\
&=-3\left[\frac{\sqrt3}{2}\cos\omega t-\frac12\sin\omega t\right]\\
&=\boxed{-\frac{3\sqrt3}{2}\cos\omega t+\frac32\sin\omega t}.
\end{aligned}
$$

**② 展開第二項：** 用 sin 加法公式。

公式（sin 加法公式）：$\sin(a+b)=\sin a\cos b+\cos a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=\dfrac{2\pi}{3}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
\begin{aligned}
4\sin\left(\frac{2\pi}3+\omega t\right)
&=4\left[\sin\frac{2\pi}3\cos\omega t+\cos\frac{2\pi}3\sin\omega t\right]\\
&=4\left[\frac{\sqrt3}2\cos\omega t-\frac12\sin\omega t\right]\\
&=\boxed{2\sqrt3\cos\omega t-2\sin\omega t}.
\end{aligned}
$$

**③ 展開第三項：** 負角度要注意：$\cos(-\pi/4)=+\sqrt2/2$，$\sin(-\pi/4)=-\sqrt2/2$。

公式（餘弦偶函數、正弦奇函數）：$\cos(-\theta)=\cos\theta$，$\sin(-\theta)=-\sin\theta$，其中 $\theta$ 為任意角（rad）；本題 $\theta=\dfrac{\pi}{4}$。

$$
\begin{aligned}
\cos\left(-\frac\pi4+\omega t\right)
&=\cos\left(-\frac\pi4\right)\cos\omega t
-\sin\left(-\frac\pi4\right)\sin\omega t\\
&=\boxed{\frac{\sqrt2}2\cos\omega t+\frac{\sqrt2}2\sin\omega t}.
\end{aligned}
$$

**④ 展開第四項：** 這項是 **sin 減法**，不是 sin 加法。

公式（sin 減法公式）：$\sin(a-b)=\sin a\cos b-\cos a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=\dfrac{\pi}{3}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
\begin{aligned}
-2\sin\left(\frac\pi3-\omega t\right)
&=-2\left[\sin\frac\pi3\cos\omega t-\cos\frac\pi3\sin\omega t\right]\\
&=-2\left[\frac{\sqrt3}2\cos\omega t-\frac12\sin\omega t\right]\\
&=\boxed{-\sqrt3\cos\omega t+\sin\omega t}.
\end{aligned}
$$

**⑤ cos 係數加總得 $A$：**

公式（同頻率波疊加）：$\sum_i\left(c_i\cos\omega t+s_i\sin\omega t\right)=A\cos\omega t+B\sin\omega t$，$A=\sum_i c_i$，$B=\sum_i s_i$，其中 $c_i,s_i$ 為第 $i$ 個波展開後 $\cos\omega t$、$\sin\omega t$ 的係數（與 $E$ 同單位），$\omega$ 為共同角頻率（rad/s），$t$ 為時間（s）；本題 ⑤ 的 $A$ 取 ①～④ 四項的 $\cos\omega t$ 係數，⑥ 的 $B$ 取它們的 $\sin\omega t$ 係數。

$$
\begin{aligned}
A&=-\frac{3\sqrt3}2+2\sqrt3+\frac{\sqrt2}2-\sqrt3\\
&=\left(-\frac32+2-1\right)\sqrt3+\frac{\sqrt2}2\\
&=\boxed{\frac{\sqrt2-\sqrt3}2\approx-0.158919}.
\end{aligned}
$$

**⑥ sin 係數加總得 $B$：**

$$
\begin{aligned}
B&=\frac32-2+\frac{\sqrt2}2+1\\
&=\boxed{\frac{1+\sqrt2}2\approx1.207107}.
\end{aligned}
$$

合成波的中間形式：

$$E=-0.158919\cos\omega t+1.207107\sin\omega t.$$

### (a) 合成振幅

**① 平方和開根號：**

$$
\begin{aligned}
E_0&=\sqrt{A^2+B^2}\\
&=\sqrt{(-0.158919)^2+(1.207107)^2}\\
&=\boxed{1.217523}.
\end{aligned}
$$

### (b) 相位

**① 求參考銳角 $\beta$：** $A<0,B>0$，在第二象限。

公式（第二象限相位）：若 $A\lt0$、$B\gt0$，先求參考銳角 $\beta=\tan^{-1}\left(\dfrac{|B|}{|A|}\right)$，再取 $\alpha=\pi-\beta$（以度計為 $180^\circ-\beta$），其中 $A,B$ 為 $\cos\omega t$、$\sin\omega t$ 的係數總和，$\beta$ 為參考銳角，$\alpha$ 為合成波 $E=E_0\cos(\alpha-\omega t)$ 的相位（rad 或度）；本題 $A=-0.158919$、$B=1.207107$。

$$
\beta=\tan^{-1}\left(\frac{1.207107}{0.158919}\right)\approx82.5^\circ.
$$

**② 取真正相位：**

$$
\begin{aligned}
\alpha&=180^\circ-\beta\\
&=97.5^\circ\\
&=\boxed{1.701696\ \mathrm{rad}}.
\end{aligned}
$$

**答案：**

$$
\boxed{E=1.217523\cos(1.701696-\omega t)}.
$$

---

## A-3. 114 級第 1 題（20 分）

**題目：**

$$
\begin{aligned}
E={}&-2\cos\left(\frac\pi6+\omega t\right)
-3\sin\left(\frac\pi3+\omega t\right)\\
&+4\cos\left(-\frac\pi3+\omega t\right)
+\sin\left(-\frac\pi4-\omega t\right).
\end{aligned}
$$

(a) 求合成振幅 $E_0\ge0$；(b) 求 $-\pi<\alpha\le\pi$ 的相位。

**① 展開第一項：** 用 cos 加法公式。

公式（cos 加法公式）：$\cos(a+b)=\cos a\cos b-\sin a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=\dfrac{\pi}{6}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
\begin{aligned}
-2\cos\left(\frac\pi6+\omega t\right)
&=-2\left[\frac{\sqrt3}2\cos\omega t-\frac12\sin\omega t\right]\\
&=\boxed{-\sqrt3\cos\omega t+\sin\omega t}.
\end{aligned}
$$

**② 展開第二項：** 用 sin 加法公式。

公式（sin 加法公式）：$\sin(a+b)=\sin a\cos b+\cos a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=\dfrac{\pi}{3}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
\begin{aligned}
-3\sin\left(\frac\pi3+\omega t\right)
&=-3\left[\frac{\sqrt3}2\cos\omega t+\frac12\sin\omega t\right]\\
&=\boxed{-\frac{3\sqrt3}2\cos\omega t-\frac32\sin\omega t}.
\end{aligned}
$$

**③ 展開第三項：** 負角度用偶／奇函數處理。

公式（餘弦偶函數、正弦奇函數）：$\cos(-\theta)=\cos\theta$，$\sin(-\theta)=-\sin\theta$，其中 $\theta$ 為任意角（rad）；本題 $\theta=\dfrac{\pi}{3}$。

$$
\begin{aligned}
4\cos\left(-\frac\pi3+\omega t\right)
&=4\left[\frac12\cos\omega t+\frac{\sqrt3}2\sin\omega t\right]\\
&=\boxed{2\cos\omega t+2\sqrt3\sin\omega t}.
\end{aligned}
$$

**④ 展開第四項：** 特別注意負角度和減號。

公式（sin 減法公式）：$\sin(a-b)=\sin a\cos b-\cos a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=-\dfrac{\pi}{4}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
\begin{aligned}
\sin\left(-\frac\pi4-\omega t\right)
&=\sin\left(-\frac\pi4\right)\cos\omega t
-\cos\left(-\frac\pi4\right)\sin\omega t\\
&=\boxed{-\frac{\sqrt2}2\cos\omega t-\frac{\sqrt2}2\sin\omega t}.
\end{aligned}
$$

**⑤ 加總得 $A$、$B$：**

公式（同頻率波疊加）：$\sum_i\left(c_i\cos\omega t+s_i\sin\omega t\right)=A\cos\omega t+B\sin\omega t$，$A=\sum_i c_i$，$B=\sum_i s_i$，其中 $c_i,s_i$ 為第 $i$ 個波展開後 $\cos\omega t$、$\sin\omega t$ 的係數（與 $E$ 同單位），$\omega$ 為共同角頻率（rad/s），$t$ 為時間（s）；本題 $A$ 取 ①～④ 四項的 $\cos\omega t$ 係數，$B$ 取它們的 $\sin\omega t$ 係數。

$$
\begin{aligned}
A&=-\sqrt3-\frac{3\sqrt3}2+2-\frac{\sqrt2}2\\
&=\boxed{2-\frac{5\sqrt3+\sqrt2}2\approx-3.037234},\\
B&=1-\frac32+2\sqrt3-\frac{\sqrt2}2\\
&=\boxed{2\sqrt3-\frac12-\frac{\sqrt2}2\approx2.256995}.
\end{aligned}
$$

### (a) 合成振幅

**① 平方和開根號：**

$$
\begin{aligned}
E_0&=\sqrt{A^2+B^2}\\
&=\sqrt{(-3.037234)^2+(2.256995)^2}\\
&=\boxed{3.784021}.
\end{aligned}
$$

### (b) 相位

**① 第二象限取角：** $A<0,B>0$，仍在第二象限。

公式（第二象限相位）：若 $A\lt0$、$B\gt0$，則 $\alpha=\pi-\tan^{-1}\left(\dfrac{|B|}{|A|}\right)$（以度計為 $180^\circ-\tan^{-1}(|B|/|A|)$），其中 $A,B$ 為 $\cos\omega t$、$\sin\omega t$ 的係數總和，$\alpha$ 為合成波 $E=E_0\cos(\alpha-\omega t)$ 的相位（rad 或度）；本題 $A=-3.037234$、$B=2.256995$。

$$
\begin{aligned}
\alpha&=180^\circ-\tan^{-1}\left(\frac{2.256995}{3.037234}\right)\\
&=143.3836^\circ\\
&=\boxed{2.502517\ \mathrm{rad}}.
\end{aligned}
$$

**答案：**

$$\boxed{E=3.784021\cos(2.502517-\omega t)}.$$

---

## A-4. 115 級第 1 題（20 分）

**題目：**

$$
\begin{aligned}
E={}&2\cos\left(\frac{5\pi}{6}+\omega t\right)
+\sin\left(\frac{3\pi}{4}+\omega t\right)\\
&-4\cos\left(\frac\pi3+\omega t\right)
-3\sin\left(\frac{4\pi}{3}-\omega t\right).
\end{aligned}
$$

求 $E_0$ 和 $\alpha$；相位範圍是 $0\le\alpha<2\pi$。

**① 展開第一項：** 用 cos 加法公式。

公式（cos 加法公式）：$\cos(a+b)=\cos a\cos b-\sin a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=\dfrac{5\pi}{6}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
\begin{aligned}
2\cos\left(\frac{5\pi}6+\omega t\right)
&=2\left[-\frac{\sqrt3}2\cos\omega t-\frac12\sin\omega t\right]\\
&=-\sqrt3\cos\omega t-\sin\omega t.
\end{aligned}
$$

**② 展開第二項：** 用 sin 加法公式。

公式（sin 加法公式）：$\sin(a+b)=\sin a\cos b+\cos a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=\dfrac{3\pi}{4}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
\begin{aligned}
\sin\left(\frac{3\pi}4+\omega t\right)
&=\frac{\sqrt2}2\cos\omega t-\frac{\sqrt2}2\sin\omega t.
\end{aligned}
$$

**③ 展開第三項：** 同樣用 cos 加法公式。

$$
\begin{aligned}
-4\cos\left(\frac\pi3+\omega t\right)
&=-4\left[\frac12\cos\omega t-\frac{\sqrt3}2\sin\omega t\right]\\
&=-2\cos\omega t+2\sqrt3\sin\omega t.
\end{aligned}
$$

**④ 展開第四項：** 用 sin 減法公式。

公式（sin 減法公式）：$\sin(a-b)=\sin a\cos b-\cos a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a=\dfrac{4\pi}{3}$、$b=\omega t$（$\omega$ 為角頻率，rad/s；$t$ 為時間，s）。

$$
\begin{aligned}
-3\sin\left(\frac{4\pi}3-\omega t\right)
&=-3\left[-\frac{\sqrt3}2\cos\omega t+\frac12\sin\omega t\right]\\
&=\frac{3\sqrt3}2\cos\omega t-\frac32\sin\omega t.
\end{aligned}
$$

**⑤ 加總得 $A$、$B$：**

公式（同頻率波疊加）：$\sum_i\left(c_i\cos\omega t+s_i\sin\omega t\right)=A\cos\omega t+B\sin\omega t$，$A=\sum_i c_i$，$B=\sum_i s_i$，其中 $c_i,s_i$ 為第 $i$ 個波展開後 $\cos\omega t$、$\sin\omega t$ 的係數（與 $E$ 同單位），$\omega$ 為共同角頻率（rad/s），$t$ 為時間（s）；本題 $A$ 取 ①～④ 四項的 $\cos\omega t$ 係數，$B$ 取它們的 $\sin\omega t$ 係數。

$$
\begin{aligned}
A&=-\sqrt3+\frac{\sqrt2}2-2+\frac{3\sqrt3}2\\
&=\boxed{-2+\frac{\sqrt2+\sqrt3}2\approx-0.426868},\\
B&=-1-\frac{\sqrt2}2+2\sqrt3-\frac32\\
&=\boxed{2\sqrt3-\frac52-\frac{\sqrt2}2\approx0.256995}.
\end{aligned}
$$

### (a) 合成振幅

**① 平方和開根號：**

公式（合成振幅）：$E_0=\sqrt{A^2+B^2}$，其中 $A,B$ 為 $\cos\omega t$、$\sin\omega t$ 的係數總和，$E_0\ge0$ 為合成振幅（與 $E$ 同單位）；本題 $A=-0.426868$、$B=0.256995$。

$$
\begin{aligned}
E_0&=\sqrt{(-0.426868)^2+(0.256995)^2}\\
&=\boxed{0.498259}.
\end{aligned}
$$

### (b) 相位

**① 第二象限取角：** $A<0,B>0$，在第二象限；結果已落在 $0\le\alpha<2\pi$。

公式（第二象限相位）：若 $A\lt0$、$B\gt0$，則 $\alpha=\pi-\tan^{-1}\left(\dfrac{|B|}{|A|}\right)$（以度計為 $180^\circ-\tan^{-1}(|B|/|A|)$），其中 $A,B$ 為 $\cos\omega t$、$\sin\omega t$ 的係數總和，$\alpha$ 為合成波 $E=E_0\cos(\alpha-\omega t)$ 的相位（rad 或度）；本題 $A=-0.426868$、$B=0.256995$。

$$
\begin{aligned}
\alpha&=180^\circ-\tan^{-1}\left(\frac{0.256995}{0.426868}\right)\\
&=148.950^\circ\\
&=\boxed{2.599669\ \mathrm{rad}}.
\end{aligned}
$$

**答案：**

$$\boxed{E=0.498259\cos(2.599669-\omega t)}.$$

**A 組三年份總表：**

| 數值 | 112 級 | 114 級 | 115 級 |
|---|---:|---:|---:|
| $A$ | -0.158919 | -3.037234 | -0.426868 |
| $B$ | +1.207107 | +2.256995 | +0.256995 |
| $E_0$ | 1.217523 | 3.784021 | 0.498259 |
| $\alpha$ | 97.500° | 143.384° | 148.950° |

---

# B 組：第 2 題｜平面電磁波（每份 40 分）

**老師逐字稿：** 第八章，明確說「一定會考」。三年都考相同四小題：(a) 電場；(b) 磁場；(c) 瞬時 Poynting 向量；(d) 輻射照度。

## B-1. 共同概念：解題順序

**符號表**（三年都給相對磁導率 $\mu_r=1$，後面的能流式用此簡化）：

| 符號 | 意義 | 單位 |
|---|---|---|
| $n$ | 介質折射率 | 無 |
| $c_0$ | 真空光速，題目取 $3\times10^8$ | m/s |
| $v$ | 光在介質中的速度 | m/s |
| $f$ | 頻率 | Hz |
| $\lambda$ | 介質中的波長 | m |
| $\omega$ | 角頻率 | rad/s |
| $k$ | 波數（大小） | rad/m |
| $\hat k$ | 傳播單位方向向量 | 無 |
| $\vec k=k\hat k$ | 波向量 | rad/m |
| $\hat e,\hat b$ | 電場與磁場的單位方向 | 無 |
| $E_0$ | 電場振幅 | V/m |
| $B_0$ | 磁通密度振幅 | T |
| $\vec r=x\hat x+y\hat y+z\hat z$ | 位置向量，$x,y,z$ 為座標 | m |
| $\Phi$ | 時空相位 | rad |
| $\vec S$ | 瞬時 Poynting 向量 | W/m² |
| $S_0$ | 瞬時能流的最大大小 | W/m² |
| $I$ | 瞬時能流的時間平均大小／輻射照度 | W/m² |
| $\varepsilon_0$ | 真空介電常數，$8.8542\times10^{-12}$ | F/m |
| $\mu_0$ | 真空磁導率 | H/m |

**① 判斷三個方向 $\hat k$、$\hat e$、$\hat b$：** 平面電磁波的三個方向兩兩垂直：

$$
\vec E\perp\vec B,\qquad\vec E\perp\vec k,\qquad\vec B\perp\vec k.
$$

能量傳播方向由電場叉乘磁場決定：

$$
\boxed{\hat e\times\hat b=\hat k}.
$$

叉積順序（$\hat x,\hat y,\hat z$ 為座標軸單位向量）如下，反過來要加負號，例如 $\hat x\times\hat z=-\hat y$，所以電場方向不能用猜的：

$$
\hat x\times\hat y=\hat z,\quad
\hat y\times\hat z=\hat x,\quad
\hat z\times\hat x=\hat y.
$$

**② 求波速、波長、角頻率、波數與另一個振幅：** 折射率是真空光速與介質相速度之比：

$$
\boxed{v=\frac{c_0}{n}}.
$$

由 $v=f\lambda$：

$$\boxed{\lambda=\frac vf}.$$

一個週期、一個波長都對應 $2\pi$ 的相位變化：

$$
\boxed{\omega=2\pi f},\qquad\boxed{k=\frac{2\pi}{\lambda}}.
$$

兩個場的振幅關係：

$$
\boxed{E_0=vB_0}.
$$

已知 $E_0$ 就用 $B_0=E_0/v$；已知 $B_0$ 就用 $E_0=vB_0$。

**③ 組合完整相位：** $\vec k\cdot\vec r$ 是空間相位，$-\omega t$ 是時間相位，$\phi_0$ 是初始相位（**三份考卷均為 $0$**）：

$$
\boxed{\Phi=\vec k\cdot\vec r-\omega t+\phi_0}.
$$

例如 $\vec k=k_x\hat x+k_y\hat y$（$k_x,k_y$：$\vec k$ 的 x、y 分量）時，$\vec k\cdot\vec r=k_xx+k_yy$；$\vec k$ 沒有 $z$ 分量，相位就不含 $z$。

**④ 寫出電場、磁場與指數表示：**

$$
\boxed{\vec E(x,y,z;t)=E_0\hat e\cos\Phi},\qquad
\boxed{\vec B(x,y,z;t)=B_0\hat b\cos\Phi}.
$$

指數表示來自歐拉公式（$i^2=-1$）：

$$e^{i\Phi}=\cos\Phi+i\sin\Phi.$$

實際的場是實數，所以取實部 $\operatorname{Re}\{\cdots\}$；複數只是計算工具：

$$
\boxed{\vec E=\operatorname{Re}\{E_0\hat e\,e^{i\Phi}\}},\qquad
\boxed{\vec B=\operatorname{Re}\{B_0\hat b\,e^{i\Phi}\}}.
$$

**⑤ 瞬時 Poynting 向量：** 定義為

$$\boxed{\vec S=\frac1{\mu_0}\vec E\times\vec B}.$$

代入兩個場，兩個 $\cos\Phi$ 相乘得到 $\cos^2\Phi$：

$$
\begin{aligned}
\vec S
&=\frac1{\mu_0}(E_0\hat e\cos\Phi)\times(B_0\hat b\cos\Phi)\\
&=\frac{E_0B_0}{\mu_0}\cos^2\Phi(\hat e\times\hat b)\\
&=\frac{E_0B_0}{\mu_0}\cos^2\Phi\,\hat k.
\end{aligned}
$$

用 $B_0=nE_0/c_0$、$1/\mu_0=\varepsilon_0c_0^2$ 化簡：

$$
\boxed{\vec S=\varepsilon_0nc_0E_0^2\cos^2\Phi\,\hat k}.
$$

令不含 $\cos^2\Phi$ 的係數為 $S_0$：

$$\boxed{S_0=\varepsilon_0nc_0E_0^2}.$$

所以 $\vec S=S_0\hat k\cos^2\Phi$。指數形式利用

$$
\cos^2\Phi=\frac{e^{2i\Phi}+2+e^{-2i\Phi}}4,
$$

得到：

$$
\boxed{\vec S=\frac{S_0}{4}\hat k
\left(e^{2i\Phi}+2+e^{-2i\Phi}\right)}.
$$

**⑥ 照度取時間平均：** 照度 $I$ 是瞬時能流大小在一個完整週期的平均（$\langle\cdots\rangle$：週期平均；$|\vec S|$：$\vec S$ 的大小），而

$$\langle\cos^2\Phi\rangle=\frac12.$$

所以：

$$
\boxed{I=\langle|\vec S|\rangle=\frac12S_0=\frac12\varepsilon_0nc_0E_0^2}.
$$

瞬時 $\vec S$ 有方向、隨時間以 $\cos^2\Phi$ 變化；照度 $I$ 是非負的平均純量。

---

## B-4. 112 級第 2 題（40 分）

**題目：** 平面電磁波在折射率 $n=3$ 的介質傳播，波向量在 $xy$ 平面、與 $+x$ 軸夾 $30^\circ$，向右上方傳播。已知磁場方向 $-\hat z$，電場振幅 $E_0=2\ \mathrm{V/m}$，**頻率 $f=10^{14}\ \mathrm{Hz}$**，初始相位 $0$。

求：(a) 完整電場；(b) 完整磁場；(c) 完整瞬時 Poynting 向量；(d) 輻射照度（各要有單位，前 3 小題需包含指數表示法）。

**① 傳播方向：** 由 $+x$ 軸往上轉 $30^\circ$。

公式（平面內方向單位向量）：與單位向量 $\hat u$ 夾角 $\theta$、往與它垂直的單位向量 $\hat w$ 那一側偏轉的方向為 $\hat k=\cos\theta\,\hat u+\sin\theta\,\hat w$，其中 $\hat u\perp\hat w$，$\theta$ 為夾角（度或 rad），$\hat k$ 為傳播方向單位向量；本題 $\hat u=\hat x$、$\hat w=\hat y$、$\theta=30^\circ$。

$$
\begin{aligned}
\hat k&=\cos30^\circ\hat x+\sin30^\circ\hat y\\
&=\boxed{\frac{\sqrt3}{2}\hat x+\frac12\hat y}.
\end{aligned}
$$

**② 磁場與電場方向：** 磁場題目已給：

$$\boxed{\hat b=-\hat z}.$$

電場必須滿足 $\hat e\times\hat b=\hat k$：

公式（電場方向）：$\hat e=\hat b\times\hat k$（由 $\hat e\times\hat b=\hat k$ 且 $\hat e,\hat b,\hat k$ 兩兩垂直、構成右手系得到），其中 $\hat e,\hat b,\hat k$ 分別為電場、磁場、傳播方向的單位向量；本題 $\hat b=-\hat z$、$\hat k=\frac{\sqrt3}{2}\hat x+\frac12\hat y$。

公式（單位向量叉積）：$\hat x\times\hat y=\hat z$，$\hat y\times\hat z=\hat x$，$\hat z\times\hat x=\hat y$，順序對調則加負號（如 $\hat x\times\hat z=-\hat y$），且 $(a\hat u)\times(b\hat w)=ab\,(\hat u\times\hat w)$，其中 $\hat x,\hat y,\hat z$ 為座標軸單位向量，$a,b$ 為純量，$\hat u,\hat w$ 為任意單位向量；本題用來算 $\hat e=\hat b\times\hat k$。

$$\boxed{\hat e=\frac12\hat x-\frac{\sqrt3}{2}\hat y}.$$

**③ 介質波速：**

$$
\begin{aligned}
v&=\frac{c_0}{n}=\frac{3\times10^8}{3}\\
&=\boxed{1.00\times10^8\ \mathrm{m/s}}.
\end{aligned}
$$

**④ 波長、角頻率、波數：**

$$
\begin{aligned}
\lambda&=\frac vf=\frac{1.00\times10^8}{10^{14}}\\
&=\boxed{10^{-6}\ \mathrm m=1000\ \mathrm{nm}}.
\end{aligned}
$$

$$\boxed{\omega=2\pi f=2\pi\times10^{14}\ \mathrm{rad/s}}.$$

$$
\boxed{k=\frac{2\pi}{\lambda}=\frac{2\pi}{10^{-6}}
=2\pi\times10^6\ \mathrm{rad/m}}.
$$

**⑤ 完整相位：** 先寫 $\vec k=k\hat k$：

$$
\vec k=2\pi\times10^6\left(\frac{\sqrt3}{2}\hat x+\frac12\hat y\right).
$$

與 $\vec r=x\hat x+y\hat y+z\hat z$ 取內積：

公式（內積）：$\vec k\cdot\vec r=k_xx+k_yy+k_zz$，其中 $k_x,k_y,k_z$ 為波向量 $\vec k$ 的分量（rad/m），$x,y,z$ 為位置座標（m）；本題 $k_x=\sqrt3\pi\times10^6$、$k_y=\pi\times10^6$、$k_z=0$（單位 rad/m）。

$$
\begin{aligned}
\vec k\cdot\vec r
&=2\pi\times10^6\left(\frac{\sqrt3}{2}x+\frac12y\right)\\
&=\pi\times10^6(\sqrt3x+y).
\end{aligned}
$$

再扣掉時間相位 $\omega t$：

公式（平面波完整相位）：$\Phi=\vec k\cdot\vec r-\omega t+\phi_0$，其中 $\vec k$ 為波向量（rad/m），$\vec r$ 為位置向量（m），$\omega$ 為角頻率（rad/s），$t$ 為時間（s），$\phi_0$ 為初始相位（rad）；本題 $\omega=2\pi\times10^{14}\ \mathrm{rad/s}$、$\phi_0=0$。

$$
\boxed{\Phi_{112}=\pi\times10^6(\sqrt3x+y)-2\pi\times10^{14}t}.
$$

符號：$\Phi_{112}$：本題完整相位（rad），下標只標示年級；不含 $z$，因為 $\vec k$ 沒有 $z$ 分量。

### (a) 完整電場

**① 實數形式：** 代入 $\vec E=E_0\hat e\cos\Phi_{112}$。

$$
\boxed{
\vec E(x,y,z;t)=2\left(\frac12\hat x-\frac{\sqrt3}{2}\hat y\right)
\cos\Phi_{112}\ \mathrm{V/m}
}.
$$

**② 指數表示：**

公式（指數表示）：$\vec E=\operatorname{Re}\{E_0\hat e\,e^{i\Phi}\}$，因為歐拉公式 $e^{i\Phi}=\cos\Phi+i\sin\Phi$ 的實部就是 $\cos\Phi$，其中 $E_0$ 為電場振幅（V/m），$\hat e$ 為電場方向單位向量，$\Phi$ 為完整相位（rad），$i^2=-1$；本題 $E_0=2\ \mathrm{V/m}$、$\hat e=\frac12\hat x-\frac{\sqrt3}{2}\hat y$、$\Phi=\Phi_{112}$。

$$
\boxed{
\vec E=\operatorname{Re}\left\{2\left(\frac12\hat x-\frac{\sqrt3}{2}\hat y\right)
e^{i\Phi_{112}}\right\}\ \mathrm{V/m}
}.
$$

### (b) 完整磁場

**① 磁場振幅：** 已知 $E_0$，用 $B_0=E_0/v$。

$$
\begin{aligned}
B_0&=\frac{E_0}{v}=\frac2{1.00\times10^8}\\
&=\boxed{2.00\times10^{-8}\ \mathrm T}.
\end{aligned}
$$

**② 寫出磁場：** 方向為 $-\hat z$。

公式（平面波磁場）：$\vec B=B_0\hat b\cos\Phi=\operatorname{Re}\{B_0\hat b\,e^{i\Phi}\}$，其中 $B_0$ 為磁場振幅（T），$\hat b$ 為磁場方向單位向量，$\Phi$ 為完整相位（rad），$\operatorname{Re}\{\cdots\}$ 表示取實部；本題 $B_0=2.00\times10^{-8}\ \mathrm{T}$、$\hat b=-\hat z$、$\Phi=\Phi_{112}$。

$$\boxed{\vec B=-2.00\times10^{-8}\hat z\cos\Phi_{112}\ \mathrm T}.$$

指數表示：

$$
\boxed{\vec B=\operatorname{Re}\left\{-2.00\times10^{-8}\hat z\,e^{i\Phi_{112}}\right\}\ \mathrm T}.
$$

### (c) 瞬時 Poynting 向量

**① 求 $S_0$：** 代入 $S_0=\varepsilon_0nc_0E_0^2$。

$$
\begin{aligned}
S_0
&=(8.8542\times10^{-12})(3)(3\times10^8)(2^2)\\
&=(8.8542\times10^{-12})(3)(3\times10^8)(4)\\
&=\boxed{0.03187512\ \mathrm{W/m^2}}.
\end{aligned}
$$

**② 補上方向 $\hat k$ 與 $\cos^2\Phi_{112}$：**

公式（瞬時 Poynting 向量）：$\vec S=\dfrac{1}{\mu_0}\vec E\times\vec B=S_0\hat k\cos^2\Phi$，其中 $\mu_0$ 為真空磁導率（H/m），$\vec E$ 為電場（V/m），$\vec B$ 為磁場（T），$S_0=\varepsilon_0nc_0E_0^2$ 為能流最大值（W/m²），$\hat k=\hat e\times\hat b$ 為傳播方向，$\Phi$ 為完整相位（rad）；本題 $S_0=0.03187512\ \mathrm{W/m^2}$、$\hat k=\frac{\sqrt3}{2}\hat x+\frac12\hat y$、$\Phi=\Phi_{112}$。

$$
\boxed{\vec S=0.03187512
\left(\frac{\sqrt3}{2}\hat x+\frac12\hat y\right)
\cos^2\Phi_{112}\ \mathrm{W/m^2}}.
$$

**③ 指數表示：** 用 B-1 ⑤ 的 $\cos^2\Phi$ 展開。

$$
\boxed{\vec S=\frac{0.03187512}{4}
\left(\frac{\sqrt3}{2}\hat x+\frac12\hat y\right)
\left(e^{2i\Phi_{112}}+2+e^{-2i\Phi_{112}}\right)\ \mathrm{W/m^2}}.
$$

### (d) 平均照度

**① 取時間平均：** $\cos^2\Phi_{112}$ 一週期平均為 $\frac12$，所以 $I=\frac12S_0$。

$$
\begin{aligned}
I&=\frac12S_0=\frac{0.03187512}{2}\\
&=\boxed{0.01593756\ \mathrm{W/m^2}}.
\end{aligned}
$$

**112 級第 2 題答案整理：**

| 小題 | 結果 |
|---|---|
| (a) | $\vec E=2(\frac12\hat x-\frac{\sqrt3}{2}\hat y)\cos\Phi_{112}$ V/m |
| (b) | $\vec B=-2.00\times10^{-8}\hat z\cos\Phi_{112}$ T |
| (c) | $\vec S=0.03187512\hat k\cos^2\Phi_{112}$ W/m² |
| (d) | $I=0.01593756$ W/m² |

---

## B-5. 114 級第 2 題（40 分）

**題目：** 折射率 $n=1.5$，波向量在 $yz$ 平面，朝 $+y,-z$ 方向（與 $-z$ 軸夾 $30^\circ$）。已知**磁場振幅** $B_0=2\times10^{-6}\ \mathrm T$，磁場指向 $-\hat x$，頻率 $f=5\times10^{13}\ \mathrm{Hz}$，初始相位 0。

同樣求 (a) 電場、(b) 磁場、(c) 瞬時能流、(d) 照度。與 112 級的差別：**這一年先給 $B_0$，要反過來算 $E_0$**。

**① 傳播方向與磁場方向：** 由 $-z$ 軸往 $+y$ 側偏 $30^\circ$。

公式（平面內方向單位向量）：與單位向量 $\hat u$ 夾角 $\theta$、往與它垂直的單位向量 $\hat w$ 那一側偏轉的方向為 $\hat k=\cos\theta\,\hat u+\sin\theta\,\hat w$，其中 $\hat u\perp\hat w$，$\theta$ 為夾角（度或 rad），$\hat k$ 為傳播方向單位向量；本題 $\hat u=-\hat z$、$\hat w=\hat y$、$\theta=30^\circ$。

$$
\begin{aligned}
\hat k&=\sin30^\circ\hat y-\cos30^\circ\hat z\\
&=\boxed{\frac12\hat y-\frac{\sqrt3}{2}\hat z}.
\end{aligned}
$$

題目給 $\boxed{\hat b=-\hat x}$。

**② 電場方向：** 由 $\hat e\times(-\hat x)=\hat k$：

公式（電場方向）：$\hat e=\hat b\times\hat k$（由 $\hat e\times\hat b=\hat k$ 且 $\hat e,\hat b,\hat k$ 兩兩垂直、構成右手系得到），其中 $\hat e,\hat b,\hat k$ 分別為電場、磁場、傳播方向的單位向量；本題 $\hat b=-\hat x$、$\hat k=\frac12\hat y-\frac{\sqrt3}{2}\hat z$。

公式（單位向量叉積）：$\hat x\times\hat y=\hat z$，$\hat y\times\hat z=\hat x$，$\hat z\times\hat x=\hat y$，順序對調則加負號（如 $\hat x\times\hat z=-\hat y$），且 $(a\hat u)\times(b\hat w)=ab\,(\hat u\times\hat w)$，其中 $\hat x,\hat y,\hat z$ 為座標軸單位向量，$a,b$ 為純量，$\hat u,\hat w$ 為任意單位向量；本題用來算 $\hat e=\hat b\times\hat k$。

$$\boxed{\hat e=-\frac{\sqrt3}{2}\hat y-\frac12\hat z}.$$

**③ 波速，再由磁場振幅反推電場振幅：**

$$
\boxed{v=\frac{3\times10^8}{1.5}=2.00\times10^8\ \mathrm{m/s}}.
$$

利用 $E_0=vB_0$：

$$
\begin{aligned}
E_0&=(2.00\times10^8)(2\times10^{-6})\\
&=4\times10^2\\
&=\boxed{400\ \mathrm{V/m}}.
\end{aligned}
$$

**④ 波長、角頻率、波數：**

公式（波長）：$\lambda=\dfrac{v}{f}$，其中 $v$ 為介質中波速（m/s），$f$ 為頻率（Hz），$\lambda$ 為介質中波長（m）；本題 $v=2.00\times10^8\ \mathrm{m/s}$、$f=5\times10^{13}\ \mathrm{Hz}$。

公式（角頻率）：$\omega=2\pi f$，其中 $f$ 為頻率（Hz），$\omega$ 為角頻率（rad/s）；本題 $f=5\times10^{13}\ \mathrm{Hz}$。

公式（波數）：$k=\dfrac{2\pi}{\lambda}$，其中 $\lambda$ 為介質中波長（m），$k$ 為波數（rad/m）；本題 $\lambda=4.00\times10^{-6}\ \mathrm{m}$。

$$
\begin{aligned}
\lambda&=\frac{2.00\times10^8}{5\times10^{13}}
=\boxed{4.00\times10^{-6}\ \mathrm m},\\
\omega&=2\pi(5\times10^{13})=\boxed{\pi\times10^{14}\ \mathrm{rad/s}},\\
k&=\frac{2\pi}{4.00\times10^{-6}}
=\boxed{5\pi\times10^5\ \mathrm{rad/m}}.
\end{aligned}
$$

**⑤ 完整相位：** 先寫波向量。

公式（波向量）：$\vec k=k\hat k$，其中 $k$ 為波數（rad/m），$\hat k$ 為傳播方向單位向量；本題 $k=5\pi\times10^5\ \mathrm{rad/m}$。

$$
\vec k=5\pi\times10^5\left(\frac12\hat y-\frac{\sqrt3}{2}\hat z\right).
$$

取內積：

公式（內積）：$\vec k\cdot\vec r=k_xx+k_yy+k_zz$，其中 $k_x,k_y,k_z$ 為波向量 $\vec k$ 的分量（rad/m），$x,y,z$ 為位置座標（m）；本題 $k_x=0$、$k_y=\frac{5\pi}{2}\times10^5$、$k_z=-\frac{5\sqrt3\pi}{2}\times10^5$（單位 rad/m）。

$$
\begin{aligned}
\vec k\cdot\vec r
&=5\pi\times10^5\left(\frac12y-\frac{\sqrt3}{2}z\right)\\
&=\frac{5\pi}{2}\times10^5(y-\sqrt3z).
\end{aligned}
$$

再扣掉 $\omega t$：

公式（平面波完整相位）：$\Phi=\vec k\cdot\vec r-\omega t+\phi_0$，其中 $\vec k$ 為波向量（rad/m），$\vec r$ 為位置向量（m），$\omega$ 為角頻率（rad/s），$t$ 為時間（s），$\phi_0$ 為初始相位（rad）；本題 $\omega=\pi\times10^{14}\ \mathrm{rad/s}$、$\phi_0=0$。

$$
\boxed{\Phi_{114}=\frac{5\pi}{2}\times10^5(y-\sqrt3z)
-\pi\times10^{14}t}.
$$

符號：$\Phi_{114}$：本題完整相位（rad）；不含 $x$，因為波沿 $yz$ 平面傳播。

### (a) 電場

**① 代入 $E_0=400$ V/m 與 $\hat e$：**

公式（平面波電場）：$\vec E=E_0\hat e\cos\Phi=\operatorname{Re}\{E_0\hat e\,e^{i\Phi}\}$，其中 $E_0$ 為電場振幅（V/m），$\hat e$ 為電場方向單位向量，$\Phi$ 為完整相位（rad），$\operatorname{Re}\{\cdots\}$ 表示取實部；本題 $E_0=400\ \mathrm{V/m}$、$\hat e=-\frac{\sqrt3}{2}\hat y-\frac12\hat z$、$\Phi=\Phi_{114}$。

$$
\boxed{
\vec E=400\left(-\frac{\sqrt3}{2}\hat y-\frac12\hat z\right)
\cos\Phi_{114}\ \mathrm{V/m}}.
$$

**② 指數表示：**

$$
\boxed{\vec E=\operatorname{Re}\left\{400
\left(-\frac{\sqrt3}{2}\hat y-\frac12\hat z\right)
e^{i\Phi_{114}}\right\}\ \mathrm{V/m}}.
$$

### (b) 磁場

**① 代入 $B_0=2\times10^{-6}$ T 與 $\hat b=-\hat x$：**

公式（平面波磁場）：$\vec B=B_0\hat b\cos\Phi=\operatorname{Re}\{B_0\hat b\,e^{i\Phi}\}$，其中 $B_0$ 為磁場振幅（T），$\hat b$ 為磁場方向單位向量，$\Phi$ 為完整相位（rad），$\operatorname{Re}\{\cdots\}$ 表示取實部；本題 $B_0=2\times10^{-6}\ \mathrm{T}$、$\hat b=-\hat x$、$\Phi=\Phi_{114}$。

$$\boxed{\vec B=-2\times10^{-6}\hat x\cos\Phi_{114}\ \mathrm T}.$$

**② 指數表示：**

$$
\boxed{\vec B=\operatorname{Re}\left\{-2\times10^{-6}\hat x\,e^{i\Phi_{114}}\right\}\ \mathrm T}.
$$

### (c) 瞬時 Poynting 向量

**① 求 $S_0$：**

$$
\begin{aligned}
S_0&=\varepsilon_0nc_0E_0^2\\
&=(8.8542\times10^{-12})(1.5)(3\times10^8)(400^2).
\end{aligned}
$$

先平方 $400^2=160000$，再算得：

$$\boxed{S_0=637.5024\ \mathrm{W/m^2}}.$$

**② 加入傳播方向：**

公式（瞬時 Poynting 向量）：$\vec S=\dfrac{1}{\mu_0}\vec E\times\vec B=S_0\hat k\cos^2\Phi$，其中 $\mu_0$ 為真空磁導率（H/m），$\vec E$ 為電場（V/m），$\vec B$ 為磁場（T），$S_0=\varepsilon_0nc_0E_0^2$ 為能流最大值（W/m²），$\hat k=\hat e\times\hat b$ 為傳播方向，$\Phi$ 為完整相位（rad）；本題 $S_0=637.5024\ \mathrm{W/m^2}$、$\hat k=\frac12\hat y-\frac{\sqrt3}{2}\hat z$、$\Phi=\Phi_{114}$。

$$
\boxed{\vec S=637.5024
\left(\frac12\hat y-\frac{\sqrt3}{2}\hat z\right)
\cos^2\Phi_{114}\ \mathrm{W/m^2}}.
$$

**③ 指數表示：**

$$
\vec S=\frac{637.5024}{4}
\left(\frac12\hat y-\frac{\sqrt3}{2}\hat z\right)
\left(e^{2i\Phi_{114}}+2+e^{-2i\Phi_{114}}\right)\ \mathrm{W/m^2}.
$$

### (d) 輻射照度

**① 取時間平均 $I=\frac12S_0$：**

$$
\boxed{I=\frac{637.5024}{2}=318.7512\ \mathrm{W/m^2}}.
$$

**114 級第 2 題答案整理：**

| 小題 | 結果 |
|---|---|
| (a) | $\vec E=400(-\frac{\sqrt3}{2}\hat y-\frac12\hat z)\cos\Phi_{114}$ V/m |
| (b) | $\vec B=-2\times10^{-6}\hat x\cos\Phi_{114}$ T |
| (c) | $\vec S=637.5024\hat k\cos^2\Phi_{114}$ W/m² |
| (d) | $I=318.7512$ W/m² |

---

## B-6. 115 級第 2 題（40 分）

**題目：** 折射率 $n=2.5$，電場振幅 $E_0=5\ \mathrm{V/m}$，頻率 $f=2\times10^{14}\ \mathrm{Hz}$，磁場朝 $+\hat z$。波向量在 $xy$ 平面朝左下方，與 $-y$ 軸夾 $30^\circ$；初始相位 $0$。

**① 傳播、磁場、電場方向：** 朝左下、靠近負 $y$ 軸。

公式（平面內方向單位向量）：與單位向量 $\hat u$ 夾角 $\theta$、往與它垂直的單位向量 $\hat w$ 那一側偏轉的方向為 $\hat k=\cos\theta\,\hat u+\sin\theta\,\hat w$，其中 $\hat u\perp\hat w$，$\theta$ 為夾角（度或 rad），$\hat k$ 為傳播方向單位向量；本題 $\hat u=-\hat y$、$\hat w=-\hat x$、$\theta=30^\circ$。

$$
\begin{aligned}
\hat k&=-\sin30^\circ\hat x-\cos30^\circ\hat y\\
&=\boxed{-\frac12\hat x-\frac{\sqrt3}{2}\hat y}.
\end{aligned}
$$

已知 $\hat b=+\hat z$，要讓 $\hat e\times\hat z=\hat k$：

公式（電場方向）：$\hat e=\hat b\times\hat k$（由 $\hat e\times\hat b=\hat k$ 且 $\hat e,\hat b,\hat k$ 兩兩垂直、構成右手系得到），其中 $\hat e,\hat b,\hat k$ 分別為電場、磁場、傳播方向的單位向量；本題 $\hat b=\hat z$、$\hat k=-\frac12\hat x-\frac{\sqrt3}{2}\hat y$。

公式（單位向量叉積）：$\hat x\times\hat y=\hat z$，$\hat y\times\hat z=\hat x$，$\hat z\times\hat x=\hat y$，順序對調則加負號（如 $\hat x\times\hat z=-\hat y$），且 $(a\hat u)\times(b\hat w)=ab\,(\hat u\times\hat w)$，其中 $\hat x,\hat y,\hat z$ 為座標軸單位向量，$a,b$ 為純量，$\hat u,\hat w$ 為任意單位向量；本題用來算 $\hat e=\hat b\times\hat k$。

$$\boxed{\hat e=\frac{\sqrt3}{2}\hat x-\frac12\hat y}.$$

**② 基本波動量：** 依序求 $v=c_0/n$、$\lambda$、$\omega$、$k$，再用 $B_0=E_0/v$。

公式（波長）：$\lambda=\dfrac{v}{f}$，其中 $v$ 為介質中波速（m/s），$f$ 為頻率（Hz），$\lambda$ 為介質中波長（m）；本題 $v=1.20\times10^8\ \mathrm{m/s}$、$f=2\times10^{14}\ \mathrm{Hz}$。

公式（角頻率）：$\omega=2\pi f$，其中 $f$ 為頻率（Hz），$\omega$ 為角頻率（rad/s）；本題 $f=2\times10^{14}\ \mathrm{Hz}$。

公式（波數）：$k=\dfrac{2\pi}{\lambda}$，其中 $\lambda$ 為介質中波長（m），$k$ 為波數（rad/m）；本題 $\lambda=6.00\times10^{-7}\ \mathrm{m}$。

$$
\begin{aligned}
v&=\frac{3\times10^8}{2.5}=\boxed{1.20\times10^8\ \mathrm{m/s}},\\
\lambda&=\frac{1.20\times10^8}{2\times10^{14}}
=\boxed{6.00\times10^{-7}\ \mathrm m},\\
\omega&=2\pi(2\times10^{14})=\boxed{4\pi\times10^{14}\ \mathrm{rad/s}},\\
k&=\frac{2\pi}{6.00\times10^{-7}}
=\boxed{\frac{10\pi}{3}\times10^6\ \mathrm{rad/m}},\\
B_0&=\frac{E_0}{v}=\frac{5}{1.20\times10^8}
=\boxed{4.16667\times10^{-8}\ \mathrm T}.
\end{aligned}
$$

**③ 完整相位：** 先寫波向量。

公式（波向量）：$\vec k=k\hat k$，其中 $k$ 為波數（rad/m），$\hat k$ 為傳播方向單位向量；本題 $k=\frac{10\pi}{3}\times10^6\ \mathrm{rad/m}$。

$$
\vec k=\frac{10\pi}{3}\times10^6
\left(-\frac12\hat x-\frac{\sqrt3}{2}\hat y\right).
$$

取內積：

公式（內積）：$\vec k\cdot\vec r=k_xx+k_yy+k_zz$，其中 $k_x,k_y,k_z$ 為波向量 $\vec k$ 的分量（rad/m），$x,y,z$ 為位置座標（m）；本題 $k_x=-\frac{5\pi}{3}\times10^6$、$k_y=-\frac{5\sqrt3\pi}{3}\times10^6$、$k_z=0$（單位 rad/m）。

$$
\vec k\cdot\vec r=-\frac{5\pi}{3}\times10^6(x+\sqrt3y).
$$

再扣掉 $\omega t$：

公式（平面波完整相位）：$\Phi=\vec k\cdot\vec r-\omega t+\phi_0$，其中 $\vec k$ 為波向量（rad/m），$\vec r$ 為位置向量（m），$\omega$ 為角頻率（rad/s），$t$ 為時間（s），$\phi_0$ 為初始相位（rad）；本題 $\omega=4\pi\times10^{14}\ \mathrm{rad/s}$、$\phi_0=0$。

$$
\boxed{\Phi_{115}=-\frac{5\pi}{3}\times10^6(x+\sqrt3y)-4\pi\times10^{14}t}.
$$

符號：$\Phi_{115}$：本題完整相位（rad）。

### (a) 電場

**① 代入 $E_0=5$ V/m 與 $\hat e$：**

公式（平面波電場）：$\vec E=E_0\hat e\cos\Phi=\operatorname{Re}\{E_0\hat e\,e^{i\Phi}\}$，其中 $E_0$ 為電場振幅（V/m），$\hat e$ 為電場方向單位向量，$\Phi$ 為完整相位（rad），$\operatorname{Re}\{\cdots\}$ 表示取實部；本題 $E_0=5\ \mathrm{V/m}$、$\hat e=\frac{\sqrt3}{2}\hat x-\frac12\hat y$、$\Phi=\Phi_{115}$。

$$
\boxed{\vec E=5\left(\frac{\sqrt3}{2}\hat x-\frac12\hat y\right)
\cos\Phi_{115}\ \mathrm{V/m}}.
$$

**② 指數表示：**

$$
\vec E=\operatorname{Re}\left\{5\left(\frac{\sqrt3}{2}\hat x-\frac12\hat y\right)e^{i\Phi_{115}}\right\}\ \mathrm{V/m}.
$$

### (b) 磁場

**① 代入 ② 求出的 $B_0$ 與 $\hat b=\hat z$：**

公式（平面波磁場）：$\vec B=B_0\hat b\cos\Phi=\operatorname{Re}\{B_0\hat b\,e^{i\Phi}\}$，其中 $B_0$ 為磁場振幅（T），$\hat b$ 為磁場方向單位向量，$\Phi$ 為完整相位（rad），$\operatorname{Re}\{\cdots\}$ 表示取實部；本題 $B_0=4.16667\times10^{-8}\ \mathrm{T}$、$\hat b=\hat z$、$\Phi=\Phi_{115}$。

$$\boxed{\vec B=4.16667\times10^{-8}\hat z\cos\Phi_{115}\ \mathrm T}.$$

**② 指數表示：**

$$
\vec B=\operatorname{Re}\left\{4.16667\times10^{-8}\hat z e^{i\Phi_{115}}\right\}\ \mathrm T.
$$

### (c) 瞬時 Poynting 向量

**① 求 $S_0=\varepsilon_0nc_0E_0^2$：**

$$
\begin{aligned}
S_0&=(8.8542\times10^{-12})(2.5)(3\times10^8)(5^2)\\
&=(8.8542\times10^{-12})(2.5)(3\times10^8)(25)\\
&=\boxed{0.16601625\ \mathrm{W/m^2}}.
\end{aligned}
$$

**② 加入傳播方向：**

公式（瞬時 Poynting 向量）：$\vec S=\dfrac{1}{\mu_0}\vec E\times\vec B=S_0\hat k\cos^2\Phi$，其中 $\mu_0$ 為真空磁導率（H/m），$\vec E$ 為電場（V/m），$\vec B$ 為磁場（T），$S_0=\varepsilon_0nc_0E_0^2$ 為能流最大值（W/m²），$\hat k=\hat e\times\hat b$ 為傳播方向，$\Phi$ 為完整相位（rad）；本題 $S_0=0.16601625\ \mathrm{W/m^2}$、$\hat k=-\frac12\hat x-\frac{\sqrt3}{2}\hat y$、$\Phi=\Phi_{115}$。

$$
\boxed{\vec S=0.16601625\left(-\frac12\hat x-\frac{\sqrt3}{2}\hat y\right)
\cos^2\Phi_{115}\ \mathrm{W/m^2}}.
$$

**③ 指數表示：**

$$
\vec S=\frac{0.16601625}{4}
\left(-\frac12\hat x-\frac{\sqrt3}{2}\hat y\right)
\left(e^{2i\Phi_{115}}+2+e^{-2i\Phi_{115}}\right)\ \mathrm{W/m^2}.
$$

### (d) 照度

**① 取時間平均 $I=\frac12S_0$：**

$$
\boxed{I=\frac12S_0=\frac{0.16601625}{2}=0.083008125\ \mathrm{W/m^2}}.
$$

**B 組三年份比較：**

| 物理量／條件 | 112 級 | 114 級 | 115 級 |
|---|---:|---:|---:|
| 折射率 $n$ | 3 | 1.5 | 2.5 |
| 題目給的振幅 | $E_0=2$ V/m | $B_0=2\times10^{-6}$ T | $E_0=5$ V/m |
| 頻率 $f$ | $10^{14}$ Hz | $5\times10^{13}$ Hz | $2\times10^{14}$ Hz |
| 傳播平面 | $xy$ | $yz$ | $xy$ |
| 磁場方向 | $-\hat z$ | $-\hat x$ | $+\hat z$ |
| 波長 $\lambda$ | $10^{-6}$ m | $4\times10^{-6}$ m | $6\times10^{-7}$ m |
| $B_0$ | $2\times10^{-8}$ T | $2\times10^{-6}$ T | $4.16667\times10^{-8}$ T |
| $S_0$ | $0.03187512$ | $637.5024$ | $0.16601625$ W/m² |
| 照度 $I$ | $0.01593756$ | $318.7512$ | $0.083008125$ W/m² |

---

# C 組：第 3 題｜干涉（每份 20 分）

112 級是雙稜鏡虛光源；114、115 級是兩種不同情況的牛頓環。三題共同點都是**兩束相干光的光程差**。

## C-1. 112 級第 3 題｜菲涅耳雙稜鏡（20 分）

**中文：** 一道波長 $\lambda=632.8\ \mathrm{nm}$ 的光經過狹縫 S，再入射菲涅耳（Fresnel）雙稜鏡。已知：

| 條件 | 數值 |
|---|---|
| 波長 $\lambda$ | 632.8 nm |
| 稜鏡折射率 $n$ | 1.6 |
| 狹縫到雙稜鏡距離 $d$ | 20 cm |
| 稜鏡到屏幕距離 | $3d=60$ cm |
| 屏幕相鄰亮紋間距 $\Delta y$ | 0.04 cm |

求：(a) 雙稜鏡的小角度 $\alpha$（rad）；(b) 兩虛光源間距 $a$（cm）。題目提示：$\alpha$ 很小時單側偏折角 $\delta\approx\alpha(n-1)$，且 $\tan\delta\approx\delta$。

**① 看出兩個虛光源：** 光穿過雙稜鏡上下兩側往不同方向偏折，把折射光往回延長得到兩個相干虛光源 S₁、S₂。做法是由亮紋間距先求虛光源間距 $a$，再由 $a$ 求稜鏡角 $\alpha$。

符號：$a$：兩虛光源間距；$D$：虛光源平面到屏幕的有效距離；$d$：狹縫到稜鏡距離；$\delta$：單側偏折角；$\alpha$：稜鏡小頂角；$y_m$：第 $m$ 條亮紋離中央的距離；$\Delta L$：兩束光的光程差。

**② 有效屏幕距離：** 虛光源約在真光源的平面上：

$$
D=d+3d=4d=4(20)=\boxed{80\ \mathrm{cm}}.
$$

**③ 推條紋間距 $\lambda D/a$：** $a\ll D$、條紋靠近中軸時，屏幕上距中央 $y$ 處的光程差：

$$\boxed{\Delta L\approx\frac{ay}{D}}.$$

亮紋條件是光程差為整數個波長：

$$\Delta L=m\lambda.$$

合併：

$$
\frac{ay_m}{D}=m\lambda.
$$

$$
\boxed{y_m=\frac{m\lambda D}{a}}.
$$

相鄰兩亮紋相減：

$$
\begin{aligned}
\Delta y&=\frac{(m+1)\lambda D}{a}-\frac{m\lambda D}{a}\\
&=\frac{[(m+1)-m]\lambda D}{a}\\
&=\boxed{\frac{\lambda D}{a}}.
\end{aligned}
$$

### (b) 虛光源間距 a（先算，因為 (a) 要用到 $a$）

**① 解出 $a$：**

$$\boxed{a=\frac{\lambda D}{\Delta y}}.$$

**② 統一單位：**

$$
\lambda=632.8\ \mathrm{nm}
=632.8\times10^{-7}\ \mathrm{cm}
=6.328\times10^{-5}\ \mathrm{cm}.
$$

**③ 代入** $D=80\ \mathrm{cm}$、$\Delta y=0.04\ \mathrm{cm}$：

$$
\begin{aligned}
a&=\frac{(6.328\times10^{-5})(80)}{0.04}\ \mathrm{cm}\\
&=\frac{0.0050624}{0.04}\ \mathrm{cm}\\
&=\boxed{0.12656\ \mathrm{cm}}.
\end{aligned}
$$

### (a) 稜鏡小角度 α

**① 虛光源幾何：** 單側虛光源偏離原軸 $d\tan\delta$，兩側對稱：

$$a=2d\tan\delta.$$

**② 小角度近似：** $\tan\delta\approx\delta$：

$$a\approx2d\delta.$$

**③ 代入偏折角** $\delta\approx(n-1)\alpha$：

$$
\begin{aligned}
a&\approx2d\delta\\
&\approx2d(n-1)\alpha.
\end{aligned}
$$

$$\boxed{\alpha\approx\frac{a}{2d(n-1)}}.$$

**④ 代數值** $a=0.12656$ cm、$d=20$ cm、$n=1.6$：

$$
\begin{aligned}
\alpha&=\frac{0.12656}{2(20)(1.6-1)}\\
&=\frac{0.12656}{2(20)(0.6)}\\
&=\frac{0.12656}{24}\\
&=\boxed{0.00527333\ \mathrm{rad}}.
\end{aligned}
$$

**最終答案：**

$$
\boxed{\text{(a) }\alpha=0.00527333\ \mathrm{rad}},\qquad
\boxed{\text{(b) }a=0.12656\ \mathrm{cm}}.
$$

---

## C-2. 牛頓環共同觀念（114、115 級都要會）

**① 同心圓的來源：** 平凸透鏡凸面放在平玻璃上，中間是中央最薄、向外漸厚的空氣膜；膜上下兩界面的反射光互相干涉，同半徑處膜厚相同，所以形成同心亮暗環。

**② 中央是暗點：** 空氣到玻璃的那次反射多一個 $\pi$ 相位反轉，所以反射光觀察時，中心膜厚接近 0 也會相消。

**③ 環半徑與膜厚的幾何關係：**

符號：$R$：凸面曲率半徑；$r$：離環中心的半徑；$t_f$：半徑 $r$ 處的空氣膜厚（寫成 $t_f$ 避免與時間混淆）；$\lambda$：空氣中波長；$m$：環的階數（中心暗點 $m=0$）；單位皆為 m。

公式（畢氏定理）：$c^2=a^2+b^2$，其中 $c$ 為直角三角形的斜邊長、$a,b$ 為兩股長（三者同單位，m）；本題以透鏡球心、球面上離中心軸 $r$ 的點、與該點同高度的中心軸上一點構成直角三角形，斜邊 $c=R$，兩股 $a=R-t_f$（沿中心軸）、$b=r$（水平）。

$$R^2=(R-t_f)^2+r^2.$$

展開平方：

$$R^2=R^2-2Rt_f+t_f^2+r^2.$$

兩邊減 $R^2$：

$$0=-2Rt_f+t_f^2+r^2.$$

$$r^2=2Rt_f-t_f^2.$$

膜很薄（$t_f\ll R$），忽略 $t_f^2$：

$$\boxed{r^2\approx2Rt_f}.$$

**④ 亮環用 $m-1/2$、暗環用 $m$：**

公式（薄膜反射干涉條件）：$\Delta L=2n_ft_f\cos\theta_t+\dfrac{\lambda}{2}$，亮紋 $\Delta L=m\lambda$、暗紋 $\Delta L=\left(m+\dfrac12\right)\lambda$，其中 $\Delta L$ 為兩束反射光的光程差（m）、$n_f$ 為薄膜折射率（無單位）、$t_f$ 為膜厚（m）、$\theta_t$ 為膜內光線與法線的夾角（rad）、$\lambda$ 為入射光在空氣中的波長（m）、$\dfrac{\lambda}{2}$ 是兩個反射界面中只有一個發生 $\pi$ 相位反轉所附加的光程、$m$ 為使 $t_f\ge0$ 的整數；本題空氣膜 $n_f=1$、近正向入射 $\theta_t=0$，得 $\Delta L=2t_f+\dfrac{\lambda}{2}$，代入亮暗條件即得下表。

| 反射光條件 | 薄膜光程差 | 第幾圈的 $m$ |
|---|---|---|
| 亮環 | $2t_f=(m-\frac12)\lambda$ | $m=1,2,3,\ldots$ |
| 暗環 | $2t_f=m\lambda$ | $m=0,1,2,\ldots$ |

把 $r^2\approx2Rt_f$ 代入亮環條件：

$$r^2=R\left(m-\frac12\right)\lambda.$$

$$\boxed{r_{m,\mathrm{亮}}=\sqrt{\left(m-\frac12\right)\lambda R}}.$$

暗環同理：

$$\boxed{r_{m,\mathrm{暗}}=\sqrt{m\lambda R}}.$$

**注意：** 暗中心是 $m=0$，第一圈暗環才是 $m=1$，別讓圈數整個偏一格。

---

## C-3. 114 級第 3 題｜兩種波長亮環重合（20 分）

**中文：** 兩種波長的光照射同一個牛頓環裝置。第一種光 $\lambda_1=589.2\ \mathrm{nm}$，它的**第 6 道亮環**與第二種光的**第 8 道亮環**重合；透鏡凸面曲率半徑 $R=50\ \mathrm{cm}$。求：(a) 第二種波長 $\lambda_2$（nm）；(b) 重合處的半徑 $r$（mm）。

**① 「重合」就是半徑相等：**

$$\boxed{r_{6,\lambda_1}=r_{8,\lambda_2}}.$$

符號：$r_{6,\lambda_1}$、$r_{8,\lambda_2}$：第一種光第 6 道、第二種光第 8 道亮環的半徑。

**② 兩邊都用亮環公式**（推導見 C-2 ④）：

$$r_m^2=\left(m-\frac12\right)\lambda R.$$

第 6 亮環：

$$
\begin{aligned}
r_{6,\lambda_1}^2
&=\left(6-\frac12\right)\lambda_1R\\
&=5.5\lambda_1R.
\end{aligned}
$$

第 8 亮環：

$$
\begin{aligned}
r_{8,\lambda_2}^2
&=\left(8-\frac12\right)\lambda_2R\\
&=7.5\lambda_2R.
\end{aligned}
$$

**③ 令兩者相等、約掉同一個 $R$：**

$$5.5\lambda_1R=7.5\lambda_2R.$$

$$\boxed{5.5\lambda_1=7.5\lambda_2}.$$

### (a) 第二種波長

**① 解出 $\lambda_2$ 並代入：**

$$\lambda_2=\frac{5.5\lambda_1}{7.5}.$$

$$
\begin{aligned}
\lambda_2&=\frac{5.5(589.2)}{7.5}\ \mathrm{nm}\\
&=\frac{3240.6}{7.5}\ \mathrm{nm}\\
&=\boxed{432.08\ \mathrm{nm}}.
\end{aligned}
$$

### (b) 共同半徑

**① 用已知的第一種光算第 6 亮環：**

$$r=\sqrt{5.5\lambda_1R}.$$

**② 換成公尺：**

$$
\lambda_1=589.2\times10^{-9}\ \mathrm m,
\qquad R=50\ \mathrm{cm}=0.50\ \mathrm m.
$$

**③ 代入：**

$$
\begin{aligned}
r&=\sqrt{5.5(589.2\times10^{-9})(0.50)}\ \mathrm m\\
&=\sqrt{1.6203\times10^{-6}}\ \mathrm m\\
&=1.272910\times10^{-3}\ \mathrm m\\
&=\boxed{1.27291\ \mathrm{mm}}.
\end{aligned}
$$

**最終答案：**

$$
\boxed{\text{(a) }\lambda_2=432.08\ \mathrm{nm}},\qquad
\boxed{\text{(b) }r=1.27291\ \mathrm{mm}}.
$$

---

## C-4. 115 級第 3 題｜第 2 亮環、第 4 暗環（20 分）

**中文：** 以平凸透鏡做牛頓環實驗，焦距 $f=6.00\ \mathrm m$、折射率 $n=1.7328$、波長 $\lambda=486.1\ \mathrm{nm}$。求：(a) 第 2 亮環半徑（mm）；(b) 第 4 暗環半徑（mm）。

**① 先把焦距換成曲率半徑：** 牛頓環公式要的是凸面曲率半徑 $R$，題目給的是焦距 $f$，兩者不同，不能直接拿 6.00 m 當 $R$。

**② 薄透鏡製鏡公式：** 空氣中、薄透鏡近似：

$$\frac1f=(n-1)\left(\frac1{R_1}-\frac1{R_2}\right).$$

$R_1,R_2$ 是前後表面的帶符號曲率半徑；平面那側 $1/R_2=0$，凸面取 $R\gt0$：

$$\frac1f=\frac{n-1}{R}.$$

$$\boxed{R=(n-1)f}.$$

$$
\begin{aligned}
R&=(1.7328-1)(6.00)\\
&=0.7328\times6.00\\
&=\boxed{4.3968\ \mathrm m}.
\end{aligned}
$$

### (a) 第 2 亮環半徑

**① 亮環公式取 $m=2$：**

$$r_{m,\mathrm{亮}}=\sqrt{\left(m-\frac12\right)\lambda R}.$$

$$
\begin{aligned}
r_{2,\mathrm{亮}}
&=\sqrt{\left(2-\frac12\right)\lambda R}\\
&=\sqrt{\frac32\lambda R}.
\end{aligned}
$$

**② 換單位：**

$$\lambda=486.1\ \mathrm{nm}=486.1\times10^{-9}\ \mathrm m.$$

**③ 代入：**

$$
\begin{aligned}
r_{2,\mathrm{亮}}
&=\sqrt{\frac32(486.1\times10^{-9})(4.3968)}\ \mathrm m\\
&=\sqrt{3.20592672\times10^{-6}}\ \mathrm m\\
&=1.790510\times10^{-3}\ \mathrm m\\
&=\boxed{1.79051\ \mathrm{mm}}.
\end{aligned}
$$

### (b) 第 4 暗環半徑

**① 暗環公式取 $m=4$**（中心暗點為 $m=0$）：

$$r_{m,\mathrm{暗}}=\sqrt{m\lambda R}.$$

$$
\begin{aligned}
r_{4,\mathrm{暗}}
&=\sqrt{4\lambda R}\\
&=\sqrt{4(486.1\times10^{-9})(4.3968)}\ \mathrm m\\
&=\sqrt{8.54913792\times10^{-6}}\ \mathrm m\\
&=2.923891\times10^{-3}\ \mathrm m\\
&=\boxed{2.92389\ \mathrm{mm}}.
\end{aligned}
$$

**最終答案：**

$$
\boxed{\text{(a) 第 2 亮環 }r=1.79051\ \mathrm{mm}},\qquad
\boxed{\text{(b) 第 4 暗環 }r=2.92389\ \mathrm{mm}}.
$$

### C 組三年比較

| 變化 | 112 級 | 114 級 | 115 級 |
|---|---|---|---|
| 干涉裝置 | 菲涅耳雙稜鏡 | 牛頓環 | 牛頓環 |
| 主要條件 | 屏幕條紋間距、狹縫稜鏡距離 | 第 6 和第 8 亮環重合、曲率半徑 | 焦距、折射率、第 2 亮環／第 4 暗環 |
| 解題核心 | $\Delta y=\lambda D/a$；$a\approx2d(n-1)\alpha$ | $r^2=(m-1/2)\lambda R$，兩半徑相等 | 先求 $R=(n-1)f$，再分亮環暗環 |

---

# E 組：三年份全部答案總整理

答案總表（D 組 TM 反射與透射不在此次範圍，已刪除）。向量題作答時仍要寫出方向與完整相位。

| 題目 | 112 級 | 114 級 | 115 級 |
|---|---|---|---|
| 1(a) 合成振幅 $E_0$ | $1.217523$ | $3.784021$ | $0.498259$ |
| 1(b) 相位 $\alpha$ | $1.701696$ rad | $2.502517$ rad | $2.599669$ rad |
| 2 電場振幅 $E_0$ | $2$ V/m | $400$ V/m | $5$ V/m |
| 2 磁場振幅 $B_0$ | $2.00\times10^{-8}$ T | $2.00\times10^{-6}$ T | $4.16667\times10^{-8}$ T |
| 2 最大瞬時能流 $S_0$ | $0.03187512$ W/m² | $637.5024$ W/m² | $0.16601625$ W/m² |
| 2(d) 輻射照度 $I$ | $0.01593756$ W/m² | $318.7512$ W/m² | $0.083008125$ W/m² |
| 3(a) | 稜鏡頂角 $0.00527333$ rad | 第二波長 $432.08$ nm | 第 2 亮環 $1.79051$ mm |
| 3(b) | 虛光源間距 $0.12656$ cm | 重合半徑 $1.27291$ mm | 第 4 暗環 $2.92389$ mm |

電磁波題共用相位與方向（$x,y,z$ 單位 m，$t$ 單位 s）：

$$
\begin{aligned}
\Phi_{112}&=\pi\times10^6(\sqrt3x+y)-2\pi\times10^{14}t,\\
\Phi_{114}&=\frac{5\pi}{2}\times10^5(y-\sqrt3z)-\pi\times10^{14}t,\\
\Phi_{115}&=-\frac{5\pi}{3}\times10^6(x+\sqrt3y)-4\pi\times10^{14}t.
\end{aligned}
$$

符號：$\Phi_{112},\Phi_{114},\Phi_{115}$：各年第 2 題的完整相位 $\vec k\cdot\vec r-\omega t$（rad），電場、磁場共用同一個相位。

$$
\begin{aligned}
\hat k_{112}&=\frac{\sqrt3}{2}\hat x+\frac12\hat y,\\
\hat k_{114}&=\frac12\hat y-\frac{\sqrt3}{2}\hat z,\\
\hat k_{115}&=-\frac12\hat x-\frac{\sqrt3}{2}\hat y.
\end{aligned}
$$

符號：$\hat k_{112},\hat k_{114},\hat k_{115}$：各年第 2 題的傳播方向單位向量；$\hat x,\hat y,\hat z$：座標軸單位向量。

---

# F 組：考試書寫版（讀完詳細教學後再看）

考卷上的必要步驟（D 組與第 4 題骨架不在此次範圍，已刪除）。

## 第 1 題：三年通用作答骨架

公式（和角公式）：$\cos(a\pm b)=\cos a\cos b\mp\sin a\sin b$，$\sin(a\pm b)=\sin a\cos b\pm\cos a\sin b$，其中 $a,b$ 為任意角（rad）；本題 $a$ 取各波的初相位常數（如 $\dfrac\pi6$）、$b$ 取 $\omega t$，展開後收集 $\cos\omega t$、$\sin\omega t$ 的係數。

1. 以 $\cos(a\pm b)$、$\sin(a\pm b)$ 展開所有波，逐項列出 cos、sin 係數。
2. 設 $E=A\cos\omega t+B\sin\omega t$，求 A、B。
3. 比較 $E=E_0\cos(\alpha-\omega t)$ 得 $A=E_0\cos\alpha$、$B=E_0\sin\alpha$。
4. 算 $E_0=\sqrt{A^2+B^2}$。依 A、B 正負判斷象限再求 $\alpha$。
5. 確認相位在題目要求的區間，並將最後的 $E$ 寫完整。

公式（合成振幅與相位）：由 $A=E_0\cos\alpha$、$B=E_0\sin\alpha$ 得 $E_0=\sqrt{A^2+B^2}$、$\tan\alpha=\dfrac{B}{A}$，其中 $A,B$ 為 $\cos\omega t$、$\sin\omega t$ 的係數加總（與 $E$ 同單位）、$E_0$ 為合成振幅、$\alpha$ 為合成相位（rad），象限由 $A,B$ 的正負決定，$A\lt0$、$B\gt0$ 時 $\alpha=\pi-\arctan\left|\dfrac{B}{A}\right|$；本題三年的 $A,B$ 都是 $A\lt0$、$B\gt0$（第二象限），數值見下。

**三年數值代入重點：**

- 112 級：$A=(\sqrt2-\sqrt3)/2$、$B=(1+\sqrt2)/2$，所以 $E_0=1.217523$、$\alpha=1.701696$ rad。
- 114 級：$A=2-(5\sqrt3+\sqrt2)/2$、$B=2\sqrt3-1/2-\sqrt2/2$，所以 $E_0=3.784021$、$\alpha=2.502517$ rad。
- 115 級：$A=-2+(\sqrt3+\sqrt2)/2$、$B=2\sqrt3-5/2-\sqrt2/2$，所以 $E_0=0.498259$、$\alpha=2.599669$ rad。

## 第 2 題：三年通用作答骨架

公式（外積）：$\vec a\times\vec b=(a_yb_z-a_zb_y)\hat x+(a_zb_x-a_xb_z)\hat y+(a_xb_y-a_yb_x)\hat z$，其中 $a_x,a_y,a_z$ 與 $b_x,b_y,b_z$ 為兩向量的直角座標分量；本題第 1 步取 $\vec a=\hat e$、$\vec b=\hat b$，外積必須等於傳播方向 $\hat k$。

公式（cos² 的指數式）：$\cos^2\Phi=\dfrac{e^{2i\Phi}+2+e^{-2i\Phi}}{4}$，由 Euler 公式 $\cos\Phi=\dfrac{e^{i\Phi}+e^{-i\Phi}}{2}$ 平方而得，其中 $\Phi$ 為完整相位（rad）、$i$ 為虛數單位；本題用在第 6 步把 $\vec S$ 改寫成指數式。

1. 依圖寫 $\hat k,\hat b$，利用 $\hat e\times\hat b=\hat k$ 求電場方向。
2. 列出 $v=c_0/n$、$\lambda=v/f$、$\omega=2\pi f$、$k=2\pi/\lambda$。
3. 已知 $E_0$ 就求 $B_0=E_0/v$；已知 $B_0$ 就求 $E_0=vB_0$。
4. 寫 $\Phi=\vec k\cdot\vec r-\omega t$，包含所有座標、正負號。
5. (a) $\vec E=E_0\hat e\cos\Phi$；(b) $\vec B=B_0\hat b\cos\Phi$；兩者各附 $\operatorname{Re}\{\cdots e^{i\Phi}\}$。
6. (c) $\vec S=\varepsilon_0nc_0E_0^2\cos^2\Phi\hat k$，若需指數式再替換 $\cos^2\Phi$。
7. (d) $I=\frac12\varepsilon_0nc_0E_0^2$；寫 W/m²。

符號：$\hat k,\hat e,\hat b$：傳播、電場、磁場方向的單位向量；$c_0$：真空光速；$\Phi$：完整相位；$\vec r$：位置向量；$\operatorname{Re}\{\cdots\}$：取實部（實際的場是實數，指數式只是計算工具）；$\vec S$：瞬時 Poynting 向量；$\varepsilon_0$：真空介電常數 $8.8542\times10^{-12}$ F/m；$I$：輻射照度（瞬時能流的時間平均）。

**必須寫出方向**，例如 112 級電場是 $\frac12\hat x-\frac{\sqrt3}2\hat y$，不是只寫 $2\ \mathrm{V/m}$。

## 第 3 題：三年分別作答

### 112 級雙稜鏡

$$
D=d+3d=4d=80\ \mathrm{cm},\qquad
\Delta y=\frac{\lambda D}{a}.
$$

$$
\begin{aligned}
a&=\frac{(6.328\times10^{-5})(80)}{0.04}=0.12656\ \mathrm{cm},\\
\alpha&=\frac{a}{2d(n-1)}
=\frac{0.12656}{2(20)(0.6)}=0.00527333\ \mathrm{rad}.
\end{aligned}
$$

符號：$d$：狹縫到雙稜鏡的距離（20 cm）；$D$：虛光源到屏幕的有效距離；$\Delta y$：相鄰亮紋間距（0.04 cm）；$\lambda$：波長（$632.8\ \mathrm{nm}=6.328\times10^{-5}$ cm）；$a$：兩虛光源間距；$\alpha$：稜鏡小頂角；$n$：稜鏡折射率（1.6）。

### 114 級牛頓亮環重合

公式（牛頓環亮環半徑）：$r_m^2=\left(m-\dfrac12\right)\lambda R$，其中 $r_m$ 為第 $m$ 道亮環的半徑（m）、$m=1,2,3,\ldots$ 為亮環階數、$\lambda$ 為波長（m）、$R$ 為透鏡凸面的曲率半徑（m）；本題 $\lambda_1$ 的 $m=6$ 亮環與 $\lambda_2$ 的 $m=8$ 亮環半徑相等。

$$
\begin{aligned}
(6-\tfrac12)\lambda_1R&=(8-\tfrac12)\lambda_2R,\\
\lambda_2&=\frac{5.5}{7.5}(589.2)=432.08\ \mathrm{nm},\\
r&=\sqrt{5.5(589.2\times10^{-9})(0.50)}=1.27291\ \mathrm{mm}.
\end{aligned}
$$

符號：$\lambda_1$：第一種光的波長（589.2 nm）；$\lambda_2$：第二種光的波長；$R$：凸面曲率半徑（0.50 m）；$r$：兩道亮環重合處的半徑；$\tfrac12$ 來自亮環條件 $2t_f=(m-\frac12)\lambda$。

### 115 級牛頓亮暗環

公式（薄透鏡製鏡公式）：$\dfrac1f=(n-1)\left(\dfrac1{R_1}-\dfrac1{R_2}\right)$，其中 $f$ 為透鏡在空氣中的焦距（m）、$n$ 為透鏡折射率（無單位）、$R_1,R_2$ 為前、後表面的帶符號曲率半徑（m）；本題平凸透鏡取凸面 $R_1=R\gt0$、平面 $R_2\to\infty$，得 $R=(n-1)f$。

$$R=(n-1)f=(1.7328-1)(6.00)=4.3968\ \mathrm m.$$

公式（牛頓環亮環半徑）：$r_{m,\mathrm{亮}}=\sqrt{\left(m-\dfrac12\right)\lambda R}$，其中 $r_{m,\mathrm{亮}}$ 為第 $m$ 道亮環的半徑（m）、$m=1,2,3,\ldots$ 為亮環階數、$\lambda$ 為波長（m）、$R$ 為透鏡凸面的曲率半徑（m）；本題 $m=2$、$\lambda=486.1\times10^{-9}$ m、$R=4.3968$ m。

公式（牛頓環暗環半徑）：$r_{m,\mathrm{暗}}=\sqrt{m\lambda R}$，其中 $r_{m,\mathrm{暗}}$ 為第 $m$ 道暗環的半徑（m）、$m=0,1,2,\ldots$ 為暗環階數（中心暗點 $m=0$）、$\lambda,R$ 同上；本題 $m=4$。

$$
\begin{aligned}
r_{2,\mathrm{亮}}&=\sqrt{(2-\tfrac12)(486.1\times10^{-9})(4.3968)}
=1.79051\ \mathrm{mm},\\
r_{4,\mathrm{暗}}&=\sqrt{4(486.1\times10^{-9})(4.3968)}
=2.92389\ \mathrm{mm}.
\end{aligned}
$$

符號：$f$：焦距（6.00 m）；$n$：透鏡折射率（1.7328）；$R$：凸面曲率半徑，由 $R=(n-1)f$ 求得；$r_{2,\mathrm{亮}}$：第 2 道亮環半徑；$r_{4,\mathrm{暗}}$：第 4 道暗環半徑（中心暗點算 $m=0$）；$486.1\times10^{-9}$ m 是波長 $\lambda$。

---

# G 組：老師明確提及、但三年試卷未完整覆蓋的內容

老師考前逐字稿中除了 A、B 組，還有以下提醒：

- **第八章**：球面波和圓柱波的電場、磁場振幅與指數表示；瞬時與時間平均 Poynting 向量；照度、能量密度、波長；**都卜勒效應**。
- **第九章**：**相位速度和群速度**。同頻率波疊加已由 A 組練習。
- **第十章**：**干涉後照度的最大、最小值與對比度**，以及楊氏干涉／虛擬光源；牛頓環雖然近兩份有考，老師沒有單獨說「牛頓環必考」。

本檔保留 9 道大題（原 12 道，D 組 3 道 TM 反射與透射題不在此次範圍），不等於已準備完所有考試範圍。

## 最後的複習順序

先做**A 組**（三角函數與相位象限）→ 用最多時間練**B 組**（每份 40 分）→ 整理**C 組**雙稜鏡、牛頓環。逐字稿的新提醒（球面波／圓柱波等）另外準備。

---

**注意：** 112 級第 2 題的頻率以掃描原卷 $10^{14}\ \mathrm{Hz}$ 為準。

---

# H 組：本次新增舊考古與課本第一輪補強（不含駐波）

> 依老師逐字稿（第八章球面波／圓柱波、場振幅與能流；第九章相位與群速度；第十章干涉對比度和楊氏干涉），額外解 **2018 年期中第 3、4 題，2020 年期中第 2、3 題，課本 4-18、4-19、7-1、7-6**；**不加入 2018 年第 5 題駐波**。「一定會考」指**波的表示與能流**、**同頻率波的疊加**；干涉對比度／楊氏干涉是重點；群速度、都卜勒只是「注意一下」。老師講義第八～十章與 Pedrotti 課本第 4、5、7 章**章號不同**。

## H-0. 題目來源、優先順序與本章符號

| 順序 | 題目 | 老師說法 | 與原三份考古題的差異 |
|---|---|---|---|
| 1 | **2020 期中第 2 題**（30 分） | 第八章波形／能流**一定會考的整組內容** | 從平面波改為**球面電磁波**，需用空間點的照度反求振幅 |
| 2 | **課本 4-19** | 同上，特別補**圓柱波** | 從能量守恆證明振幅隨距離變為 $1/\sqrt r$；歷屆三年沒練過 |
| 3 | **課本 4-18 (a)(b)** | 球面波照度、電磁場振幅 | 從**總功率與面積**計算照度和場振幅 |
| 4 | **2018 期中第 3 題**（20 分） | 第十章「對比度」是重點 | 不只求條紋位置，還須由**兩束照度比例**求可見度及反推比例 |
| 5 | **課本 7-1 (a)～(d)** | 同上 | 從兩個明確電場式、**光程差與初相位**求完整照度與可見度 |
| 6 | **2018 期中第 4 題**（20 分） | **楊氏干涉**可能會考 | 多出**覆蓋玻璃薄片使整組條紋平移**的小題 |
| 7 | **課本 7-6** | 楊氏干涉 | 同一屏幕上**不同波長的亮暗條紋重合**，不可直接套牛頓環公式 |
| 8 | **2020 期中第 3 題**（10 分） | 相位、群速度「注意一下」 | 考**從已知色散關係推導群速度**，且原卷式子的量綱有疑點 |

**來源：**

- 2018～2020 近代光學歷屆原卷：2018 年期中在 PDF **第 1 頁**；2020 年期中在 PDF **第 4 頁**。
- Pedrotti, *Introduction to Optics*, 3rd ed.：4-18、4-19 在**印刷第 112 頁／PDF 第 131 頁**；7-1、7-6 在**印刷第 189 頁／PDF 第 208 頁**。
- 老師考前逐字稿：第八章 00:38～02:39；第九章 02:42～04:21；第十章 04:37～05:31。

### 符號表

| 符號 | 意義 | 常用單位 |
|---|---|---|
| $c_0$ | 真空中的光速，取 $3.00\times10^8$ | m/s |
| $\varepsilon_0$ | 真空介電常數，取 $8.8542\times10^{-12}$ | F/m |
| $\mu_0$ | 真空磁導率，且 $\varepsilon_0\mu_0c_0^2=1$ | H/m |
| $E_0,B_0$ | 電場與磁通密度振幅 | V/m、T |
| $I$ | **時間平均**的輻射照度 | W/m² |
| $\vec S$ | **瞬時** Poynting 能流向量 | W/m² |
| $\overline{u}$ | **時間平均**的電磁能量密度 | J/m³ |
| $P$ | 通過表面之輻射功率 | W |
| $r,\rho$ | 離點源的距離、離柱軸的距離 | m |
| $\lambda,k,\omega$ | 波長、波數 $2\pi/\lambda$、角頻率 $2\pi f$ | m、rad/m、rad/s |
| $\vec r$ | 位置向量 $x\hat x+y\hat y+z\hat z$ | m |
| $\hat r,\hat\phi,\hat\rho$ | 球面徑向、方位角向、圓柱徑向單位向量 | 無 |
| $I_1,I_2$ | 兩束光各自的照度 | W/m² |
| $\delta$ | 兩束相干光在觀察點的**總相位差** | rad |
| $V$ | 干涉條紋可見度／對比度，介於 0 與 1 之間 | 無 |
| $d,L,\Delta y$ | 雙狹縫間距、狹縫到屏幕距離、亮紋間距 | m |
| $v_p,v_g$ | 相位速度、群速度 | m/s |

---

# H-1. 2020 年期中第 2 題：球面電磁波（30 分）

## 題目（依原卷）

**中文：** 真空中，原點的**點波源**發出球面電磁波；波長 $\lambda=2\ \mathrm m$，**電場沿球座標 $\hat\phi$ 方向**。在直角座標 $(x,y,z)=(2,1,3)\ \mathrm m$ 處測到輻射照度 $I=2\ \mathrm{W/m^2}$。以 $x,y,z$ 及 $\hat x,\hat y,\hat z$ 寫出：

- (a) 球面波**瞬時 Poynting 向量**的完整表示（振幅、方向、指數形式、單位）。
- (b) **電場向量**的完整表示（振幅、偏振方向、指數形式、單位）。
- (c) **磁場向量**的完整表示（振幅、偏振方向、指數形式、單位）。

**注意：** 題目未指定初相位，以下用 $\phi_0$ 保留（需要具體式子時可取 $\phi_0=0$），這是解題約定。

**① 觀察點與傳播方向：** 球面波從原點向外擴散，觀察點的傳播方向是原點指向觀察點的徑向。設 $\vec r_0=2\hat x+\hat y+3\hat z$：

$$
\begin{aligned}
r_0&=\sqrt{x_0^2+y_0^2+z_0^2}\\
&=\sqrt{2^2+1^2+3^2}\\
&=\boxed{\sqrt{14}\ \mathrm m}.
\end{aligned}
$$

位置向量除以長度得單位傳播方向（只對觀察點成立，換位置 $\hat r$ 就變）：

$$
\boxed{\hat r_0=\frac{2\hat x+\hat y+3\hat z}{\sqrt{14}}}.
$$

**② 把 $\hat\phi$ 換成直角座標：** 方位角在 $xy$ 平面內從 +x 轉向 +y：

$$
\hat\phi=-\sin\phi\,\hat x+\cos\phi\,\hat y.
$$

令 $\rho=\sqrt{x^2+y^2}$：

$$
\sin\phi=\frac y\rho,\qquad \cos\phi=\frac x\rho,
$$

$$
\boxed{\hat\phi=\frac{-y\hat x+x\hat y}{\sqrt{x^2+y^2}}}.
$$

觀察點 $\rho_0=\sqrt{2^2+1^2}=\sqrt5$，電場偏振方向：

$$
\boxed{\hat e_0=\hat\phi_0=\frac{-\hat x+2\hat y}{\sqrt5}}.
$$

**③ 由平均照度反推振幅：** 題目給的是平均照度，真空中：

$$
\boxed{I=\frac12\varepsilon_0c_0E_0^2}.
$$

解出 $E_0$：

$$
E_0^2=\frac{2I}{\varepsilon_0c_0}
\quad\Rightarrow\quad
E_0=\sqrt{\frac{2I}{\varepsilon_0c_0}}.
$$

代入 $I=2\ \mathrm{W/m^2}$：

$$
\begin{aligned}
E_0(r_0)
&=\sqrt{\frac{2(2)}{(8.8542\times10^{-12})(3.00\times10^8)}}\\
&=\boxed{38.8056\ \mathrm{V/m}}.
\end{aligned}
$$

真空中 $E_0=c_0B_0$：

$$
B_0(r_0)=\frac{E_0(r_0)}{c_0}
=\frac{38.8056}{3.00\times10^8}
=\boxed{1.29352\times10^{-7}\ \mathrm T}.
$$

這兩個值只是 $r=r_0$ 處的振幅，離開觀察點還要再乘 $1/r$ 的衰減（見 ⑤）。

**④ 波數、角頻率與相位：**

$$k=\frac{2\pi}{2}=\boxed{\pi\ \mathrm{rad/m}}.$$

真空中 $\omega=c_0k$：

$$\omega=(3\times10^8)\pi
=\boxed{3\pi\times10^8\ \mathrm{rad/s}}.$$

公式（球面波相位）：$\Phi(r,t)=kr-\omega t+\phi_0$，其中 $k$ 為波數（rad/m）、$r$ 為離點波源的距離（m）、$\omega$ 為角頻率（rad/s）、$t$ 為時間（s）、$\phi_0$ 為初相位（rad），$kr-\omega t$ 的寫法代表波往 $r$ 增加的方向（向外）傳播；本題 $k=\pi\ \mathrm{rad/m}$、$\omega=3\pi\times10^8\ \mathrm{rad/s}$。

相位裡的空間座標是離原點的距離 $r$：

$$
\boxed{\Phi(r,t)=\pi r-3\pi\times10^8 t+\phi_0},\qquad
r=\sqrt{x^2+y^2+z^2}.
$$

**⑤ 振幅隨 $1/r$ 衰減：** 忽略吸收時，總功率 $P$ 穿過任意半徑球面都相同：

$$I(r)=\frac{P}{4\pi r^2}\propto\frac1{r^2}.$$

又 $I\propto E_0^2$：

$$\boxed{E_0(r)\propto\frac1r,\qquad B_0(r)\propto\frac1r}.$$

用 $r_0=\sqrt{14}$ 處的已知振幅寫成（$r_0/r$ 無單位，長度皆以 m 計）：

$$
\boxed{E_0(r)=38.8056\frac{\sqrt{14}}r\ \mathrm{V/m}},
$$

$$
\boxed{B_0(r)=1.29352\times10^{-7}\frac{\sqrt{14}}r\ \mathrm T}.
$$

### (a) 瞬時 Poynting 向量

公式（Poynting 向量）：$\vec S=\dfrac{1}{\mu_0}\vec E\times\vec B$，對 $\vec E=E_0\hat e\cos\Phi$、$\vec B=B_0\hat b\cos\Phi$（$\hat e\times\hat b=\hat k$、$B_0=E_0/c_0$）得 $\vec S=\varepsilon_0c_0E_0^2\cos^2\Phi\,\hat k$，其中 $\mu_0$ 為真空磁導率（H/m）、$\varepsilon_0$ 為真空介電常數（F/m）、$c_0$ 為真空光速（m/s）、$E_0,B_0$ 為電場（V/m）與磁場（T）振幅、$\hat e,\hat b,\hat k$ 為電場、磁場、傳播方向的單位向量、$\Phi$ 為完整相位（rad）；本題 $\hat k=\hat r$，最大瞬時能流 $S_0=\varepsilon_0c_0E_0^2$。

**① 最大瞬時能流：** $\overline{\cos^2\Phi}=1/2$，所以最大值是平均照度的兩倍：

$$S_0(r_0)=2I(r_0)=\boxed{4\ \mathrm{W/m^2}}.$$

**② 觀察點的瞬時 Poynting 向量：**

$$
\boxed{\begin{aligned}
\vec S(2,1,3;t)
&=4\frac{2\hat x+\hat y+3\hat z}{\sqrt{14}}\\
&\quad\times\cos^2\!\left(\pi\sqrt{14}-3\pi\times10^8t+\phi_0\right)
\ \mathrm{W/m^2}
\end{aligned}}.
$$

**③ 任意位置：** 把球面擴散放進去：

$$
\boxed{\begin{aligned}
\vec S(x,y,z;t)
&=4\left(\frac{\sqrt{14}}r\right)^2
\frac{x\hat x+y\hat y+z\hat z}{r}\\
&\quad\times\cos^2\Phi(r,t)\ \mathrm{W/m^2}
\end{aligned}}.
$$

**④ 指數表示：** 把 $\cos^2\Phi$ 換成 $(e^{2i\Phi}+2+e^{-2i\Phi})/4$。$\vec S$ 來自真實場的叉積，不能把單一複數場 $e^{i\Phi}$ 直接平方當成瞬時能流。

### (b) 電場向量

公式（電場向量表示）：$\vec E=E_0\hat e\cos\Phi=\operatorname{Re}\{E_0\hat e\,e^{i\Phi}\}$，第二個等號來自 Euler 公式 $e^{i\Phi}=\cos\Phi+i\sin\Phi$，其中 $E_0$ 為電場振幅（V/m）、$\hat e$ 為偏振方向單位向量、$\Phi$ 為完整相位（rad）、$\operatorname{Re}\{\cdots\}$ 為取實部；本題 $E_0=38.8056\dfrac{\sqrt{14}}{r}$ V/m、$\hat e=\hat\phi$、$\Phi=\pi r-3\pi\times10^8t+\phi_0$。

**① 觀察點代入振幅與方向：**

$$
\boxed{\begin{aligned}
\vec E(2,1,3;t)&=38.8056\frac{-\hat x+2\hat y}{\sqrt5}\\
&\quad\times\cos(\pi\sqrt{14}-3\pi\times10^8t+\phi_0)\ \mathrm{V/m}
\end{aligned}}.
$$

**② 指數表示：**

$$
\boxed{\begin{aligned}
\vec E(2,1,3;t)
&=\operatorname{Re}\!\Big\{
38.8056\frac{-\hat x+2\hat y}{\sqrt5}\\
&\qquad\times e^{i(\pi\sqrt{14}-3\pi\times10^8t+\phi_0)}
\Big\}\ \mathrm{V/m}
\end{aligned}}.
$$

**③ 任意位置：** 振幅隨 $1/r$（排除 $x=y=0$，該處 $\hat\phi$ 未定義）：

$$
\boxed{
\vec E(x,y,z;t)
=38.8056\frac{\sqrt{14}}r
\frac{-y\hat x+x\hat y}{\sqrt{x^2+y^2}}
\cos\Phi(r,t)\ \mathrm{V/m}
}.
$$

### (c) 磁場向量

**① 磁場方向：** $\hat b$ 須與 $\hat e$、$\hat r$ 垂直且 $\hat e\times\hat b=\hat r$：

$$\boxed{\hat b=\hat r\times\hat e=\hat r\times\hat\phi}.$$

公式（外積）：$\vec a\times\vec b=(a_yb_z-a_zb_y)\hat x+(a_zb_x-a_xb_z)\hat y+(a_xb_y-a_yb_x)\hat z$，其中 $a_x,a_y,a_z$ 與 $b_x,b_y,b_z$ 為兩向量的直角座標分量；本題 $\vec a=\hat r_0=\dfrac{(2,1,3)}{\sqrt{14}}$、$\vec b=\hat e_0=\dfrac{(-1,2,0)}{\sqrt5}$，分子算得 $(-6,-3,5)$。

$$
\begin{aligned}
\hat b_0
&=\frac{2\hat x+\hat y+3\hat z}{\sqrt{14}}
\times\frac{-\hat x+2\hat y}{\sqrt5}\\
&=\boxed{\frac{-6\hat x-3\hat y+5\hat z}{\sqrt{70}}}.
\end{aligned}
$$

**② 觀察點的磁場：**

公式（磁場向量表示）：$\vec B=B_0\hat b\cos\Phi=\operatorname{Re}\{B_0\hat b\,e^{i\Phi}\}$，且真空中 $B_0=\dfrac{E_0}{c_0}$，其中 $B_0$ 為磁場振幅（T）、$\hat b$ 為磁場方向單位向量、$\Phi$ 為與電場相同的完整相位（rad）、$c_0$ 為真空光速（m/s）；本題 $B_0=1.29352\times10^{-7}\dfrac{\sqrt{14}}{r}$ T、$\hat b=\hat r\times\hat\phi$。

$$
\boxed{\begin{aligned}
\vec B(2,1,3;t)
&=1.29352\times10^{-7}
\frac{-6\hat x-3\hat y+5\hat z}{\sqrt{70}}\\
&\quad\times\cos(\pi\sqrt{14}-3\pi\times10^8t+\phi_0)\ \mathrm T
\end{aligned}}.
$$

**③ 指數表示：**

$$
\boxed{\begin{aligned}
\vec B(2,1,3;t)
&=\operatorname{Re}\!\Big\{
1.29352\times10^{-7}
\frac{-6\hat x-3\hat y+5\hat z}{\sqrt{70}}\\
&\qquad\times e^{i(\pi\sqrt{14}-3\pi\times10^8t+\phi_0)}
\Big\}\ \mathrm T
\end{aligned}}.
$$

**④ 任意位置：** 磁場方向展成直角座標：

$$
\hat b(x,y,z)=
-\frac{zx}{r\rho}\hat x
-\frac{zy}{r\rho}\hat y
+\frac{\rho}{r}\hat z,
\qquad \rho=\sqrt{x^2+y^2}.
$$

$$
\boxed{\begin{aligned}
\vec B(x,y,z;t)
&=1.29352\times10^{-7}\frac{\sqrt{14}}r\\
&\quad\times\left(-\frac{zx}{r\rho}\hat x-\frac{zy}{r\rho}\hat y+\frac\rho r\hat z\right)
\cos\Phi(r,t)\ \mathrm T
\end{aligned}}.
$$

---

# H-2. 課本第 4 章第 19 題：圓柱波為什麼是 $1/\sqrt r$？

**來源**：Pedrotti 第 4 章 Problem 19，印刷第 112 頁。

**中文：** 由**通量守恆（conservation of flux）**證明圓柱波振幅必須隨**距離平方根的倒數**而減小。

符號：$r$ 為離圓柱軸的垂直距離（m）；$L$ 為選定的線狀波源長度（m）；$P_L$ 為這段長度穿過圓柱側面的總功率（W）；$I(r)$ 為半徑 $r$ 處的平均照度（W/m²）；$E_0(r),B_0(r)$ 為對應位置的電、磁場振幅。

**① 取同軸圓柱側面：** 球面波的能量攤在 $4\pi r^2$ 上，所以 $I\propto1/r^2$；圓柱波由一條長線狀波源向外擴散，要改用包圍波源的同軸圓柱側面，面積是圓周長乘長度：

$$A(r)=2\pi rL.$$

**② 功率守恆求照度：** 沒有吸收時，不管側面半徑選多大，通過側面的總功率 $P_L$ 都相同：

$$P_L=I(r)\,A(r)=I(r)(2\pi rL).$$

把面積除過去：

$$
\boxed{I(r)=\frac{P_L}{2\pi rL}}.
$$

固定 $P_L$ 和 $L$，分母只有 $r$ 會變：

$$\boxed{I(r)\propto\frac1r}.$$

**③ 照度換成振幅：** 真空中平均照度與電場振幅平方成正比：

$$I(r)=\frac12\varepsilon_0c_0\big[E_0(r)\big]^2.$$

代入 ② 的 $I(r)=P_L/(2\pi rL)$：

$$\frac12\varepsilon_0c_0[E_0(r)]^2=\frac{P_L}{2\pi rL}.$$

左右同乘 $2$：

$$\varepsilon_0c_0[E_0(r)]^2=\frac{P_L}{\pi rL}.$$

除以 $\varepsilon_0c_0$：

$$[E_0(r)]^2=\frac{P_L}{\pi rL\varepsilon_0c_0}.$$

開平方根：

$$
\boxed{E_0(r)=\sqrt{\frac{P_L}{\pi L\varepsilon_0c_0}}\frac1{\sqrt r}}.
$$

根號內的因子與 $r$ 無關，因此得到題目要證明的結果：

$$\boxed{E_0(r)\propto\frac1{\sqrt r}}.$$

又真空中 $B_0(r)=E_0(r)/c_0$：

$$\boxed{B_0(r)\propto\frac1{\sqrt r}}.$$

**④ 指數表示（依老師逐字稿的延伸，非原題要求）：** 以遠離軸的理想向外圓柱波示範，選電場沿 $z$ 軸偏振；$\hat\rho$ 為向外的徑向單位向量、$\hat\phi$ 為方位角單位向量。

公式（Poynting 向量）：$\vec S=\dfrac{1}{\mu_0}\vec E\times\vec B$，其中 $\vec S$ 為瞬時 Poynting 向量（W/m²，方向即能流方向）、$\mu_0$ 為真空磁導率（H/m）、$\vec E$ 為電場（V/m）、$\vec B$ 為磁場（T）；本題要求能流朝 $+\hat\rho$，所以 $\vec E\times\vec B$ 必須指向 $+\hat\rho$。

公式（圓柱座標單位向量叉積）：$\hat\rho\times\hat\phi=\hat z,\quad\hat\phi\times\hat z=\hat\rho,\quad\hat z\times\hat\rho=\hat\phi$，交換次序則變號，其中 $\hat\rho,\hat\phi,\hat z$ 依序為徑向、方位角、軸向單位向量（右手系）；本題 $\hat z\times\hat\phi=-\hat\rho$，所以 $\hat z\times(-\hat\phi)=\hat\rho$。

電場 $\vec E\parallel\hat z$ 時，為讓能流朝 $+\hat\rho$，磁場要朝 $-\hat\phi$。設 $C$ 是決定振幅的常數、$\Phi=kr-\omega t+\phi_0$：

公式（Euler 公式）：$e^{i\Phi}=\cos\Phi+i\sin\Phi$，故對與相位無關的實振幅 $A$ 有 $\operatorname{Re}\{Ae^{i\Phi}\}=A\cos\Phi$，其中 $\Phi$ 為相位（rad）、$A$ 可含單位向量；本題 $A=\dfrac{C}{\sqrt r}\hat z$（電場）或 $-\dfrac{C}{c_0\sqrt r}\hat\phi$（磁場），$\Phi=kr-\omega t+\phi_0$。

$$
\boxed{
\vec E(r,t)=\frac{C}{\sqrt r}\hat z\cos\Phi
=\operatorname{Re}\left\{\frac{C}{\sqrt r}\hat z e^{i\Phi}\right\}
}.
$$

公式（電磁波 E、B 關係）：$\vec B=\dfrac{1}{c_0}\hat k\times\vec E$，其中 $\hat k$ 為傳播方向單位向量、$c_0$ 為真空光速（m/s）、$\vec E$ 為電場（V/m）、$\vec B$ 為磁場（T）；本題 $\hat k=\hat\rho$、$\vec E\parallel\hat z$，因 $\hat\rho\times\hat z=-\hat\phi$，$\vec B$ 振幅為 $\dfrac{C}{c_0\sqrt r}$、方向為 $-\hat\phi$。

$$
\boxed{
\vec B(r,t)=-\frac{C}{c_0\sqrt r}\hat\phi\cos\Phi
=\operatorname{Re}\left\{-\frac{C}{c_0\sqrt r}\hat\phi e^{i\Phi}\right\}
}.
$$

再求瞬時 Poynting 向量：

公式（真空光速）：$c_0=\dfrac{1}{\sqrt{\varepsilon_0\mu_0}}$，故 $\dfrac{1}{\mu_0c_0}=\varepsilon_0c_0$，其中 $\varepsilon_0$ 為真空介電常數（F/m）、$\mu_0$ 為真空磁導率（H/m）、$c_0$ 為真空光速（m/s）；本題 $\dfrac{1}{\mu_0}\cdot\dfrac{C}{\sqrt r}\cdot\dfrac{C}{c_0\sqrt r}=\dfrac{\varepsilon_0c_0C^2}{r}$，方向 $\hat z\times(-\hat\phi)=\hat\rho$。

$$
\boxed{\vec S(r,t)=\frac{\varepsilon_0c_0C^2}{r}\cos^2\Phi\ \hat\rho}.
$$

對一個完整週期取平均：

公式（餘弦平方的時間平均）：$\overline{\cos^2\Phi}=\dfrac{1}{T}\displaystyle\int_0^{T}\cos^2\Phi\,dt=\dfrac12$，其中 $T=2\pi/\omega$ 為週期（s）、$\Phi$ 為以角頻率 $\omega$ 隨時間變化的相位（rad）；本題 $\Phi=kr-\omega t+\phi_0$，固定 $r$ 對 $t$ 平均。

$$
\boxed{\overline{\vec S}(r)=\frac{\varepsilon_0c_0C^2}{2r}\hat\rho}.
$$

**注意：** 以上是圓柱波遠場的理想近似；嚴格解涉及 Hankel 函數，遠場相位可多一個與 $r$ 無關的常數，不影響 $1/\sqrt r$ 的振幅比例。

**三種波一眼分辨：**

| 波形（理想、無吸收） | 傳遞能量的幾何面積 | 振幅 $E_0$ | 平均照度 $I$ |
|---|---|---|---|
| 平面波 | 不隨距離增加 | 常數 | 常數 |
| **圓柱波** | $\propto r$ | $\propto r^{-1/2}$ | $\propto r^{-1}$ |
| **球面波** | $\propto r^2$ | $\propto r^{-1}$ | $\propto r^{-2}$ |

---
# H-3. 課本第 4 章第 18 題：由功率求照度，再求電場／磁場

**來源**：Pedrotti 第 4 章 Problem 18，印刷第 112 頁。

**中文：**

**(a)** 一盞**電功率 220 W** 的燈，假設只有 **5%** 轉為光，且光均勻向各方向傳播。求離燈 **10 m** 處的輻射照度與**電場振幅**。

**(b)** 一束 **2000 W** 的雷射光經透鏡集中到截面積約 **$1\times10^{-6}\ \mathrm{cm^2}$**，求照度和**電場、磁場振幅**。

**注意：** 題目未給介質折射率，以下以空氣近似真空、忽略損耗與聚焦的非理想效應，依課本標準估算。

### H-3(a) 燈泡：功率不等於全部光功率

符號：$P_\mathrm{in}=220\ \mathrm W$ 為耗電功率、$\eta=0.05$ 為光轉換效率、$P_\mathrm{light}$ 為向外輻射的光功率。

**① 先算真正變成光的功率：**

$$P_\mathrm{light}=\eta P_\mathrm{in}=0.05(220)=\boxed{11\ \mathrm W}.$$

**② 球面面積與照度：** 光均勻向四周傳播，$r=10\ \mathrm m$ 處的球面面積：

$$A=4\pi r^2=4\pi(10)^2=400\pi\ \mathrm{m^2}.$$

照度是單位面積上的平均功率：

$$
\begin{aligned}
I&=\frac{P_\mathrm{light}}{A}=\frac{11}{400\pi}\\
&=\boxed{8.75352\times10^{-3}\ \mathrm{W/m^2}}.
\end{aligned}
$$

**③ 照度轉電場振幅：** 由 $I=\tfrac12\varepsilon_0c_0E_0^2$ 移項：

$$E_0=\sqrt{\frac{2I}{\varepsilon_0c_0}}.$$

代入：

$$
\begin{aligned}
E_0&=\sqrt{\frac{2(8.75352\times10^{-3})}{(8.8542\times10^{-12})(3\times10^8)}}\\
&=\boxed{2.56727\ \mathrm{V/m}}.
\end{aligned}
$$

### H-3(b) 雷射：聚焦面積特別小，要先換單位

**① 換算截面積：** $1\ \mathrm{cm}=10^{-2}\ \mathrm m$，面積要**平方**：

$$1\ \mathrm{cm^2}=(10^{-2}\ \mathrm m)^2=10^{-4}\ \mathrm{m^2}.$$

因此：

$$A=10^{-6}\times10^{-4}=\boxed{10^{-10}\ \mathrm{m^2}}.$$

**② 求雷射照度：**

$$
I=\frac PA=\frac{2000}{10^{-10}}
=\boxed{2.00\times10^{13}\ \mathrm{W/m^2}}.
$$

**③ 求電場振幅：**

公式（照度與振幅）：$I=\dfrac12\varepsilon_0c_0E_0^2\ \Rightarrow\ E_0=\sqrt{\dfrac{2I}{\varepsilon_0c_0}}$，其中 $I$ 為平均照度（W/m²）、$\varepsilon_0$ 為真空介電常數（F/m）、$c_0$ 為真空光速（m/s）、$E_0$ 為電場振幅（V/m）；本題 $I=2.00\times10^{13}\ \mathrm{W/m^2}$。

$$
\begin{aligned}
E_0&=\sqrt{\frac{2I}{\varepsilon_0c_0}}\\
&=\sqrt{\frac{2(2\times10^{13})}{(8.8542\times10^{-12})(3\times10^8)}}\\
&=\boxed{1.22714\times10^8\ \mathrm{V/m}}.
\end{aligned}
$$

**④ 求磁場振幅：** 用 $B_0=E_0/c_0$：

$$
\begin{aligned}
B_0&=\frac{E_0}{c_0}\\
&=\frac{1.22714\times10^8}{3.00\times10^8}\\
&=\boxed{0.409047\ \mathrm T}.
\end{aligned}
$$

**4-18 答案小結：**

| 小題 | 輻射照度 $I$ | 電場振幅 $E_0$ | 磁場振幅 $B_0$ |
|---|---|---|---|
| (a) 燈泡 10 m 處 | $8.75352\times10^{-3}$ W/m² | $2.56727$ V/m | 非原題要求 |
| (b) 聚焦雷射 | $2.00\times10^{13}$ W/m² | $1.22714\times10^8$ V/m | $0.409047$ T |

解題主線：電功率還是光功率？→ 光通過哪個面積？→ $I=P/A$ → $I=\varepsilon_0c_0E_0^2/2$ → $B_0=E_0/c_0$。

---

# H-4. 2018 年期中第 3 題：干涉條紋對比度（20 分）

**來源**：2018 年 4 月 25 日期中考第 3 題。

**中文：** 兩道光發生干涉，形成干涉條紋：

- (a) 若其中一束照度為另一束的 $N$ 倍（$N>1$），求條紋**對比度（contrast / fringe visibility）**，以 $N$ 表示。
- (b) 若條紋對比度為 $3/4$，求照度較大的那道光是照度較小的幾倍。

**① 寫出對比度與亮暗照度：** $I_{\max}$ 為亮條紋最大照度、$I_{\min}$ 為暗條紋最小照度，對比度定義為：

$$
\boxed{V=\frac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}}.
$$

亮暗差異大時 $V$ 接近 1，幾乎分不出時接近 0。兩束相干、**平行偏振**、完全重疊的光（照度 $I_1,I_2$），在總相位差 $\delta$ 處的總照度（第三項來自展開 $|E_1+E_2|^2$ 的交叉項）：

$$
\boxed{I(\delta)=I_1+I_2+2\sqrt{I_1I_2}\cos\delta}.
$$

$\cos\delta=+1$ 時最亮：

$$\boxed{I_{\max}=I_1+I_2+2\sqrt{I_1I_2}=(\sqrt{I_1}+\sqrt{I_2})^2}.$$

$\cos\delta=-1$ 時最暗：

$$\boxed{I_{\min}=I_1+I_2-2\sqrt{I_1I_2}=(\sqrt{I_1}-\sqrt{I_2})^2}.$$

### (a) 由照度比 $N$ 推導可見度

**① 設照度比：** 設照度較小的一束為 $I_2$：

$$I_1=NI_2.$$

**② 代入亮暗照度：**

$$
\begin{aligned}
I_{\max}&=(N+1+2\sqrt N)I_2,\\
I_{\min}&=(N+1-2\sqrt N)I_2.
\end{aligned}
$$

**③ 代入對比度定義：**

$$
\begin{aligned}
V&=\frac{(N+1+2\sqrt N)I_2-(N+1-2\sqrt N)I_2}
{(N+1+2\sqrt N)I_2+(N+1-2\sqrt N)I_2}\\
&=\frac{4\sqrt NI_2}{2(N+1)I_2}.
\end{aligned}
$$

分子分母約去 $2I_2$：

$$\boxed{V=\frac{2\sqrt N}{N+1}}.$$

### (b) 已知 $V=3/4$，反求照度比

**① 列方程：**

$$\frac{2\sqrt N}{N+1}=\frac34.$$

交叉相乘：

$$8\sqrt N=3(N+1).$$

**② 換元：** 同時有 $N$ 與 $\sqrt N$，令

$$x=\sqrt N\quad\Rightarrow\quad N=x^2,\quad x>1.$$

代入：

$$8x=3(x^2+1).$$

移到同一側：

$$3x^2-8x+3=0.$$

**③ 二次公式求 $x$：**

公式（二次公式）：$ax^2+bx+c=0\ (a\ne0)\ \Rightarrow\ x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$，其中 $a,b,c$ 為實係數、$x$ 為未知數；本題 $a=3$、$b=-8$、$c=3$。

$$
\begin{aligned}
x&=\frac{8\pm\sqrt{(-8)^2-4(3)(3)}}{2(3)}\\
&=\frac{8\pm\sqrt{28}}6
=\frac{4\pm\sqrt7}{3}.
\end{aligned}
$$

因 $x=\sqrt N>1$，取正號：

$$x=\frac{4+\sqrt7}{3}\approx2.21525.$$

**④ 換回 $N$：** 題目問的是照度比 $N$，不能停在 $x$：

$$
\boxed{N=x^2=\left(\frac{4+\sqrt7}{3}\right)^2\approx4.90733}.
$$

**2018 第 3 題最終答案：**

$$\boxed{\text{(a) }V=\frac{2\sqrt N}{N+1}\qquad
\text{(b) }N\approx4.90733.}$$

---

# H-5. 課本第 7 章第 1 題：完整干涉照度與可見度

**來源**：Pedrotti 第 7 章 Problem 1，印刷第 189 頁，PDF 第 208 頁。

**原題：** Two mutually coherent beams with parallel electric fields are described by

$$
E_1=3\cos\left(ks_1-\omega t+\frac\pi5\right),\quad
E_2=4\cos\left(ks_2-\omega t+\frac\pi6\right).
$$

The amplitudes are in **kV/m**. At point $P$, the phase difference due to optical paths is $\pi/3$, with the **first beam having the longer path**. Find (a) individual irradiances $I_1,I_2$; (b) interference irradiance $I_{12}$; (c) net irradiance; (d) fringe visibility.

**中文：** 兩束互相相干、電場偏振方向平行的光，電場式如上，振幅單位 **kV/m**。在觀察點 $P$，**由路徑長短造成的相位差是 $\pi/3$，且第一束的路徑較長**。求兩束各自照度、干涉交叉項、總照度及條紋對比度。

**① (a) 兩束各自的照度：** 先把振幅換成 V/m：

$$E_{01}=3\ \mathrm{kV/m}=3000\ \mathrm{V/m},$$

$$E_{02}=4\ \mathrm{kV/m}=4000\ \mathrm{V/m}.$$

公式（照度與振幅）：$I=\dfrac12\varepsilon_0c_0E_0^2$，其中 $I$ 為平均照度（W/m²）、$\varepsilon_0$ 為真空介電常數（F/m）、$c_0$ 為真空光速（m/s）、$E_0$ 為電場振幅（V/m）；本題兩束分別代入 $E_{01}=3000\ \mathrm{V/m}$、$E_{02}=4000\ \mathrm{V/m}$。

空氣近似真空，令共同常數 $K=\tfrac12\varepsilon_0c_0$：

$$K=\frac12(8.8542\times10^{-12})(3\times10^8)
=0.00132813.$$

因此：

$$
\begin{aligned}
I_1&=KE_{01}^2\\
&=0.00132813(3000)^2\\
&=\boxed{11953.17\ \mathrm{W/m^2}}.
\end{aligned}
$$

同樣：

$$
\begin{aligned}
I_2&=KE_{02}^2\\
&=0.00132813(4000)^2\\
&=\boxed{21250.08\ \mathrm{W/m^2}}.
\end{aligned}
$$

**② 組合總相位差：** 不能直接拿 $\pi/3$ 當總相位差，電場式本身還有初相位 $\pi/5$、$\pi/6$。兩束相位：

$$\Phi_1=ks_1-\omega t+\frac\pi5.$$

$$\Phi_2=ks_2-\omega t+\frac\pi6.$$

第一束減第二束：

$$
\begin{aligned}
\delta&=\Phi_1-\Phi_2\\
&=k(s_1-s_2)+\left(\frac\pi5-\frac\pi6\right).
\end{aligned}
$$

第一束路徑較長，路徑造成的相位差為：

$$k(s_1-s_2)=\frac\pi3.$$

初相位差：

$$\frac\pi5-\frac\pi6=\frac{6\pi-5\pi}{30}=\frac\pi{30}.$$

總相位差：

$$
\boxed{\delta=\frac\pi3+\frac\pi{30}=\frac{11\pi}{30}=66^\circ}.
$$

**③ (b) 干涉交叉項 $I_{12}$：** 相干光要加上交叉項：

$$\boxed{I_{12}=2\sqrt{I_1I_2}\cos\delta}.$$

由 $I_j=\tfrac12\varepsilon_0c_0E_{0j}^2$ 改用振幅計算：

$$2\sqrt{I_1I_2}=\varepsilon_0c_0E_{01}E_{02}.$$

所以：

$$
\begin{aligned}
I_{12}&=(8.8542\times10^{-12})(3\times10^8)(3000)(4000)
\cos66^\circ\\
&=31875.12\cos66^\circ\\
&=\boxed{12964.78\ \mathrm{W/m^2}}.
\end{aligned}
$$

交叉項為正，表示此觀察點是部分**建設性干涉**。

**④ (c) 總照度：** 兩束照度加上交叉項：

$$
\begin{aligned}
I_{\mathrm{net}}&=I_1+I_2+I_{12}\\
&=11953.17+21250.08+12964.78\\
&=\boxed{46168.03\ \mathrm{W/m^2}}.
\end{aligned}
$$

**⑤ (d) 條紋可見度：** 亮、暗條紋的最大與最小照度：

$$
I_{\max}=(\sqrt{I_1}+\sqrt{I_2})^2,\quad
I_{\min}=(\sqrt{I_1}-\sqrt{I_2})^2.
$$

代入定義：

$$
V=\frac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}
=\frac{2\sqrt{I_1I_2}}{I_1+I_2}.
$$

$I_1:I_2=3^2:4^2=9:16$，直接用振幅比：

$$
V=\frac{2(3)(4)}{3^2+4^2}
=\frac{24}{25}
=\boxed{0.96}.
$$

**7-1 最終答案：**

| 小題 | 結果 |
|---|---|
| (a) $I_1,I_2$ | $11953.17,\ 21250.08$ W/m² |
| (b) $I_{12}$ | $12964.78$ W/m² |
| (c) $I_{\mathrm{net}}$ | $46168.03$ W/m² |
| (d) $V$ | $0.96$ |

---
# H-6. 2018 年期中第 4 題：楊氏雙狹縫＋薄片造成條紋平移（20 分）

**來源**：2018 年 4 月 25 日期中第 4 題。

**中文：**

- 兩狹縫距離 $d=0.6\ \mathrm{mm}$。
- 入射光波長 $\lambda=550\ \mathrm{nm}$。
- (a) 若希望相鄰亮紋距離為 $\Delta y=1\ \mathrm{mm}$，屏幕距離 $L$ 應為多少？
- (b) 在其中一個狹縫放厚度 $t=200\ \mathrm{\mu m}$、折射率 $n=1.5$ 的玻璃片，沿用 (a) 的屏幕位置，求**整組干涉條紋平移多遠**。

### (a) 屏幕應放多遠？

符號：$d$ 為兩狹縫間隔、$L$ 為雙狹縫到屏幕距離、$\Delta y$ 為相鄰亮紋距離、$\lambda$ 為波長。

**① 亮紋間隔公式：** 小角度遠場下光程差 $d\sin\theta\simeq dy/L$，亮紋要求 $m\lambda$，得 $y_m=m\lambda L/d$，相鄰兩級相差：

$$\boxed{\Delta y=\frac{\lambda L}{d}}.$$

**② 移項解 $L$：**

$$L=\frac{\Delta y\,d}{\lambda}.$$

**③ 換成公尺代入：**

$$
\begin{aligned}
\Delta y&=1\ \mathrm{mm}=1\times10^{-3}\ \mathrm m,\\
d&=0.6\ \mathrm{mm}=0.6\times10^{-3}\ \mathrm m,\\
\lambda&=550\ \mathrm{nm}=550\times10^{-9}\ \mathrm m.
\end{aligned}
$$

$$
\begin{aligned}
L&=\frac{(1\times10^{-3})(0.6\times10^{-3})}{550\times10^{-9}}\\
&=\boxed{1.09091\ \mathrm m}.
\end{aligned}
$$

### (b) 為什麼加玻璃片會讓**全部條紋**平移？

**① 玻璃片額外增加的光程：** 同樣厚度 $t$ 原本走空氣，換成折射率 $n$ 的玻璃後光程由 $t$ 變 $nt$：

$$\boxed{\Delta_\mathrm{glass}=(n-1)t}.$$

代入：

$$
\begin{aligned}
\Delta_\mathrm{glass}&=(1.5-1)(200\ \mathrm{\mu m})\\
&=0.5(200)=\boxed{100\ \mathrm{\mu m}}.
\end{aligned}
$$

**② 換算成幾個波長：**

$$
\begin{aligned}
\frac{\Delta_\mathrm{glass}}\lambda
&=\frac{100\times10^{-6}}{550\times10^{-9}}\\
&=\boxed{181.818}.
\end{aligned}
$$

額外光程差約 181.8 個波長，整組條紋就移動約 181.8 個條紋間距。

**③ 轉成屏幕上的距離：** (a) 的條紋間距是 $1\ \mathrm{mm}$：

$$
\begin{aligned}
|\Delta y_\mathrm{shift}|
&=\frac{\Delta_\mathrm{glass}}\lambda\,\Delta y\\
&=(181.818)(1\ \mathrm{mm})\\
&=\boxed{181.818\ \mathrm{mm}}.
\end{aligned}
$$

**注意：** 條紋往被玻璃片覆蓋的狹縫一側移動；原題沒指定哪一個狹縫，只能給平移量大小，不要自行補 +y 或 −y。

**2018 第 4 題答案：**

$$\boxed{\text{(a) }L=1.09091\ \mathrm m\qquad
\text{(b) }|\Delta y_\mathrm{shift}|=181.818\ \mathrm{mm}.}$$

---

# H-7. 課本第 7 章第 6 題：兩種波長的暗紋與亮紋重合

**來源**：Pedrotti 第 7 章 Problem 6，印刷第 189 頁／PDF 第 208 頁。

**原題：** Two slits are illuminated by light with two wavelengths. One is known to be 436 nm. On a screen, the **fourth minimum** of the 436-nm light coincides with the **third maximum** of the other light. Find the other wavelength.

**中文：** 雙狹縫同時受到兩種波長的光照射，其中一種波長為 436 nm。屏幕上，此光的**第 4 個暗紋**，剛好與另一種光的**第 3 個亮紋**重合。求另一光的波長。

符號：$d$ 為雙狹縫間隔、$L$ 為到屏幕距離、$y$ 為條紋相對中央亮紋的位置、$\lambda$ 為光波長。

**① 亮紋與暗紋位置公式：** 亮紋光程差是整數倍波長：

$$d\sin\theta=m\lambda,\qquad m=0,1,2,3,\ldots$$

小角度 $y\approx L\sin\theta$：

$$\boxed{y_{m,\mathrm{亮}}=\frac{m\lambda L}{d}}.$$

暗紋光程差是半整數倍波長，第 1、2、3、4 暗紋依序為 $\lambda/2$、$3\lambda/2$、$5\lambda/2$、$7\lambda/2$。用 $j=1,2,3,\ldots$ 表示第幾暗紋：

$$\boxed{y_{j,\mathrm{暗}}=\frac{(j-\tfrac12)\lambda L}{d}}.$$

所以第 4 暗紋不是 $4\lambda L/d$，也不是 $4.5\lambda L/d$。

**② 寫出兩條紋位置並令其相等：** 第一種光 $\lambda_1=436\ \mathrm{nm}$，第 4 暗紋 $j=4$：

$$
\begin{aligned}
y_{4,\mathrm{暗}}^{(1)}
&=\frac{(4-\frac12)\lambda_1L}{d}\\
&=\frac{3.5\lambda_1L}{d}.
\end{aligned}
$$

第二種光 $\lambda_2$，第 3 亮紋 $m=3$：

$$y_{3,\mathrm{亮}}^{(2)}=\frac{3\lambda_2L}{d}.$$

兩條紋重合，$y$ 相同：

$$\frac{3.5\lambda_1L}{d}=\frac{3\lambda_2L}{d}.$$

同一組狹縫和屏幕，$L/d$ 可約掉：

$$3.5\lambda_1=3\lambda_2.$$

**③ 求另一波長：**

$$\lambda_2=\frac{3.5}{3}\lambda_1.$$

代入：

$$
\begin{aligned}
\lambda_2&=\frac{3.5}{3}(436\ \mathrm{nm})\\
&=\boxed{508.667\ \mathrm{nm}}.
\end{aligned}
$$

**7-6 最後答案：**

$$\boxed{\lambda_2\approx508.7\ \mathrm{nm}}.$$

---

# H-8. 2020 年期中第 3 題：相位速度推導群速度（10 分）

**來源**：2020 年 4 月 21 日期中第 3 題。

**中文：** 原卷給

$$\boxed{v_p=\left(\frac{g\lambda}{2\pi}\right)^{1/3}},$$

其中 $g$ 為重力加速度，求**群速度是相位速度的幾倍**。

**注意：** 原卷印成 $1/3$ 次方，但 $g\lambda$ 單位是 m²/s²，取 $1/3$ 次方不是速度單位，題目量綱不自洽。以下按原卷的數學關係求比值，不擅自改成 $1/2$；深水重力波的平方根版本另列在最後。

符號：$k$ 為波數、$\lambda$ 為波長、$\omega$ 為角頻率、$v_p$ 為相位速度、$v_g$ 為群速度。

**① 群速度定義：** 知道 $v_p$ 與 $k$ 的關係後，先求 $\omega=kv_p$ 再對 $k$ 微分：

$$v_p=\frac\omega k,\qquad\boxed{v_g=\frac{d\omega}{dk}}.$$

**② 把波長改成波數：**

$$k=\frac{2\pi}{\lambda}\quad\Rightarrow\quad\lambda=\frac{2\pi}{k}.$$

代入原卷公式：

$$
\begin{aligned}
v_p&=\left(\frac{g(2\pi/k)}{2\pi}\right)^{1/3}\\
&=\left(\frac gk\right)^{1/3}\\
&=\boxed{g^{1/3}k^{-1/3}}.
\end{aligned}
$$

**③ 求 $\omega(k)$：** 由 $v_p=\omega/k$：

$$\omega=kv_p.$$

代入：

$$
\begin{aligned}
\omega&=k\cdot g^{1/3}k^{-1/3}\\
&=g^{1/3}k^{1-1/3}\\
&=\boxed{g^{1/3}k^{2/3}}.
\end{aligned}
$$

**④ 對 $k$ 微分：** $g^{1/3}$ 是常數，用冪次法則 $\dfrac{d}{dk}k^a=ak^{a-1}$：

$$
\begin{aligned}
v_g&=\frac{d\omega}{dk}\\
&=g^{1/3}\frac{d}{dk}k^{2/3}\\
&=g^{1/3}\left(\frac23k^{-1/3}\right)\\
&=\frac23g^{1/3}k^{-1/3}.
\end{aligned}
$$

由 ② 的 $v_p=g^{1/3}k^{-1/3}$：

$$\boxed{v_g=\frac23v_p}.$$

**按原卷印出的 $1/3$ 次方：**

$$\boxed{\frac{v_g}{v_p}=\frac23}.$$

**注意（平方根版本，不是修改原題）：** 若原意是深水重力波：

$$v_p=\sqrt{\frac{g\lambda}{2\pi}}=\sqrt{\frac gk},$$

同樣 $\omega=kv_p=g^{1/2}k^{1/2}$，微分得：

$$v_g=\frac12g^{1/2}k^{-1/2}=\boxed{\frac12v_p}.$$

原卷 $1/3$ → 數學答案 $2/3$；深水波 $1/2$ → 物理答案 $1/2$，作答時不要混用。

---
# H-9. 老師額外點名：電磁波能量密度、時間平均 Poynting 向量

> 這是老師逐字稿第八章（約 00:44、01:25～02:05）點名的內容，不是八題中某一題的原文。

## H-9.1 能量密度和照度到底有什麼不同？

- **能量密度 $u$（J/m³）**：每**單位體積**包含多少電磁能量。
- **Poynting 向量 $\vec S$（W/m²）**：瞬間每**單位面積、單位時間**向哪個方向輸送多少能量。
- **照度 $I$（W/m²）**：沿傳播方向的 Poynting 向量大小經過**時間平均**。

$u$ 和 $I$ 單位不同，要乘上傳播速度才能連結。

## H-9.2 從電場、磁場分別算能量密度

符號：$\varepsilon$ 為介質介電常數、$\mu$ 為介質磁導率，$E=|\vec E|$、$B=|\vec B|$ 為瞬時電場與磁通密度大小。

**① 電、磁能量密度：** 瞬時**電場**能量密度：

$$\boxed{u_E=\frac12\varepsilon E^2}.$$

瞬時**磁場**能量密度：

$$\boxed{u_B=\frac{B^2}{2\mu}}.$$

相加得總瞬時能量密度：

$$\boxed{u=u_E+u_B=\frac12\varepsilon E^2+\frac{B^2}{2\mu}}.$$

**② 平面波中兩者相等：** 理想、非色散、均勻介質中的平面正弦波：

$$v=\frac1{\sqrt{\varepsilon\mu}},\qquad B=\frac Ev.$$

把 $B=E/v$ 代入 $u_B$，並用 $1/(\mu v^2)=\varepsilon$：

$$
\begin{aligned}
u_B&=\frac{(E/v)^2}{2\mu}\\
&=\frac{E^2}{2\mu v^2}\\
&=\frac12\varepsilon E^2=u_E,
\end{aligned}
$$

所以總能量密度簡化為：

$$\boxed{u=\varepsilon E^2}.$$

**③ 時間平均：** 若 $E=E_0\cos\Phi$：

$$\boxed{u(t)=\varepsilon E_0^2\cos^2\Phi}.$$

$\overline{\cos^2\Phi}=1/2$：

$$\boxed{\overline u=\frac12\varepsilon E_0^2}.$$

**④ 乘傳播速度得照度：**

$$\boxed{I=v\overline u=\frac12\varepsilon v E_0^2}.$$

在 $\mu_r=1$ 的非磁性介質中，它就是 $I=\varepsilon_0nc_0E_0^2/2$：

$$\varepsilon=n^2\varepsilon_0,\qquad v=\frac{c_0}{n},\quad \varepsilon v=n\varepsilon_0c_0.$$

## H-9.4 套用到球面波與圓柱波

$I=v\overline u$ 是局部關係，所以 $\overline u$ 與 $I$ 隨距離的比例相同：

- **球面波**：$I\propto r^{-2}$，平均能量密度同樣 $\overline u\propto r^{-2}$。
- **圓柱波**：$I\propto r^{-1}$，平均能量密度同樣 $\overline u\propto r^{-1}$。

2020 年第 2 題在觀察點給 $I=2\ \mathrm{W/m^2}$，當地平均能量密度：

$$\boxed{\overline u=\frac I{c_0}=\frac2{3\times10^8}=6.66667\times10^{-9}\ \mathrm{J/m^3}}.$$

---

# H-10. 老師「提醒注意」的都卜勒效應：最少要記哪些？

> 老師只說「注意一下」、「公式要自己記」，沒有承諾必考；這裡只留考前必要觀念。

都卜勒效應（Doppler effect）：波源與觀察者有**徑向相對運動**時，觀察到的頻率或波長改變。

- **互相靠近**：觀察到的光波長變**短**，頻率變**高**（藍移）。
- **互相遠離**：觀察到的光波長變**長**，頻率變**低**（紅移）。

符號：波源沿視線方向**遠離**的速率 $v>0$，$\beta=v/c_0$，$\lambda_\mathrm{em}$ 為發射波長、$\lambda_\mathrm{obs}$ 為接收波長。

**① 相對論性都卜勒公式：**

$$\boxed{\lambda_\mathrm{obs}=\lambda_\mathrm{em}\sqrt{\frac{1+\beta}{1-\beta}}}.$$

**② 低速近似：** $v\ll c_0$ 時：

$$\boxed{\frac{\Delta\lambda}{\lambda_\mathrm{em}}\approx\frac v{c_0}},\qquad\Delta\lambda=\lambda_\mathrm{obs}-\lambda_\mathrm{em}.
$$

互相靠近時把速度改成負值，就得到藍移。套公式前先確認正負號定義，以及題目給的是波源還是觀察者的運動。

---

# H-11. 新增八道題的考試書寫版（詳細推導見 H-1～H-8）

> 考前複習用；某一步不懂就回到前面對應的完整題解。

## ① 2020 期中第 2 題：球面電磁波

已知 $r_0=\sqrt{2^2+1^2+3^2}=\sqrt{14}\ \mathrm m$、$\hat r_0=(2\hat x+\hat y+3\hat z)/\sqrt{14}$、$\hat\phi_0=(-\hat x+2\hat y)/\sqrt5$、$\lambda=2\ \mathrm m$、$I(r_0)=2\ \mathrm{W/m^2}$。

公式（照度與振幅）：$I=\dfrac12\varepsilon_0c_0E_0^2$，其中 $I$ 為平均照度（W/m²）、$\varepsilon_0$ 為真空介電常數（F/m）、$c_0$ 為真空光速（m/s）、$E_0$ 為電場振幅（V/m）；本題 $I(r_0)=2\ \mathrm{W/m^2}$，移項得 $E_0=\sqrt{2I/(\varepsilon_0c_0)}$。

公式（電磁波 E、B 關係）：$\vec B=\dfrac{1}{c_0}\hat k\times\vec E$，其中 $\hat k$ 為傳播方向單位向量、$c_0$ 為真空光速（m/s）、$\vec E$ 為電場（V/m）、$\vec B$ 為磁場（T）；本題球面波 $\hat k=\hat r_0$、$\vec E\parallel\hat\phi_0$，所以 $B_0=E_0/c_0$、方向 $\hat b_0=\hat r_0\times\hat\phi_0$。

$$
\begin{aligned}
k&=2\pi/\lambda=\pi\ \mathrm{rad/m},\quad\omega=c_0k=3\pi\times10^8\ \mathrm{rad/s},\\
E_0(r_0)&=\sqrt{2I/(\varepsilon_0c_0)}=38.8056\ \mathrm{V/m},\\
B_0(r_0)&=E_0(r_0)/c_0=1.29352\times10^{-7}\ \mathrm T,\\
\hat b_0&=\hat r_0\times\hat\phi_0=(-6\hat x-3\hat y+5\hat z)/\sqrt{70},\\
\Phi_0(t)&=\pi\sqrt{14}-3\pi\times10^8t+\phi_0.
\end{aligned}
$$

公式（Poynting 向量）：$\vec S=\dfrac{1}{\mu_0}\vec E\times\vec B$，其中 $\vec S$ 為瞬時 Poynting 向量（W/m²）、$\mu_0$ 為真空磁導率（H/m）、$\vec E$ 為電場（V/m）、$\vec B$ 為磁場（T）；本題大小 $\dfrac{E_0B_0}{\mu_0}=\varepsilon_0c_0E_0^2=2I(r_0)=4\ \mathrm{W/m^2}$，方向 $\hat\phi_0\times\hat b_0=\hat r_0$。

$$
\begin{aligned}
\vec S(r_0,t)&=4\hat r_0\cos^2\Phi_0(t)\ \mathrm{W/m^2},\\
\vec E(r_0,t)&=38.8056\hat\phi_0\cos\Phi_0(t)\ \mathrm{V/m},\\
\vec B(r_0,t)&=1.29352\times10^{-7}\hat b_0\cos\Phi_0(t)\ \mathrm T.
\end{aligned}
$$

公式（球面波距離關係）：$E_0(r)=E_0(r_0)\dfrac{r_0}{r},\quad I(r)=I(r_0)\left(\dfrac{r_0}{r}\right)^2$，由總功率 $P=4\pi r^2I$ 不隨 $r$ 改變而來，其中 $r$ 為到點波源的距離（m）、$r_0$ 為參考距離（m）、$E_0$ 為電場振幅（V/m）、$I$ 為平均照度（W/m²）、$P$ 為總功率（W）；本題 $r_0=\sqrt{14}\ \mathrm m$，$B_0$ 與 $E_0$ 同比例、$\vec S$ 與 $I$ 同比例。

公式（Euler 公式）：$\cos\Phi=\operatorname{Re}\{e^{i\Phi}\}=\dfrac{e^{i\Phi}+e^{-i\Phi}}{2}$，平方得 $\cos^2\Phi=\dfrac{e^{2i\Phi}+2+e^{-2i\Phi}}{4}$，其中 $\Phi$ 為相位（rad）；本題 $\Phi=\pi r-3\pi\times10^8t+\phi_0$。

任意半徑時，各式再乘 $r_0/r$（E、B）或 $(r_0/r)^2$（S），並將相位換為 $\pi r-3\pi\times10^8t+\phi_0$。指數寫法：電磁場用 $\operatorname{Re}\{\cdots e^{i\Phi}\}$，S 用 $(e^{2i\Phi}+2+e^{-2i\Phi})/4$。

## ② 課本 4-19：圓柱波振幅

公式（能量通量守恆）：$P=IA$，其中 $P$ 為穿過某曲面的總平均功率（W）、$I$ 為該面上的平均照度（W/m²）、$A$ 為曲面面積（m²）；本題曲面是半徑 $r$、長 $L$ 的同軸圓柱側面 $A=2\pi rL$，$P=P_L$ 與 $r$ 無關。

$$P_L=I(r)\,2\pi rL\quad\Rightarrow\quad I(r)=\frac{P_L}{2\pi rL}\propto r^{-1}.$$

公式（電磁波 E、B 關係）：$\vec B=\dfrac{1}{c_0}\hat k\times\vec E$，故振幅 $B_0=E_0/c_0$，其中 $\hat k$ 為傳播方向單位向量、$c_0$ 為真空光速（m/s）、$\vec E$ 為電場（V/m）、$\vec B$ 為磁場（T）；本題 $\hat k=\hat\rho$、$\vec E\parallel\hat z$，因 $\hat\rho\times\hat z=-\hat\phi$，$\vec B$ 沿 $-\hat\phi$。

$$I(r)=\tfrac12\varepsilon_0c_0E_0(r)^2
\quad\Rightarrow\quad
\boxed{E_0(r)\propto r^{-1/2}},\quad
\boxed{B_0(r)\propto r^{-1/2}}.$$

公式（Euler 公式）：$e^{i\Phi}=\cos\Phi+i\sin\Phi$，故對實振幅 $A$ 有 $\operatorname{Re}\{Ae^{i\Phi}\}=A\cos\Phi$，其中 $\Phi$ 為相位（rad）、$A$ 可含單位向量；本題 $\Phi=kr-\omega t$。

示範指數形式：$\vec E=\operatorname{Re}\{C\hat z e^{i(kr-\omega t)}/\sqrt r\}$、$\vec B=\operatorname{Re}\{-C\hat\phi e^{i(kr-\omega t)}/(c_0\sqrt r)\}$。

## ③ 課本 4-18：燈泡與雷射

公式（光轉換效率）：$P_\mathrm{light}=\eta P_\mathrm{in}$，其中 $P_\mathrm{in}$ 為耗電功率（W）、$\eta$ 為轉為光的比例（無單位）、$P_\mathrm{light}$ 為光功率（W）；本題 $\eta=0.05$、$P_\mathrm{in}=220\ \mathrm W$。

公式（照度定義）：$I=\dfrac{P}{A}$，其中 $P$ 為通過受光面的平均功率（W）、$A$ 為受光面積（m²）、$I$ 為平均照度（W/m²）；本題 (a) 光均勻向四周傳播，取球面 $A=4\pi r^2$、$r=10\ \mathrm m$，(b) $A$ 為聚焦截面積 $10^{-10}\ \mathrm{m^2}$、$P=2000\ \mathrm W$。

公式（照度與振幅）：$I=\dfrac12\varepsilon_0c_0E_0^2$，其中 $I$ 為平均照度（W/m²）、$\varepsilon_0$ 為真空介電常數（F/m）、$c_0$ 為真空光速（m/s）、$E_0$ 為電場振幅（V/m）；本題移項得 $E_0=\sqrt{2I/(\varepsilon_0c_0)}$，(a)(b) 各代入 $I_a$、$I_b$。

$$
\begin{aligned}
P_\mathrm{light}&=0.05(220)=11\ \mathrm W,\\
I_a&=\frac{11}{4\pi(10)^2}=8.75352\times10^{-3}\ \mathrm{W/m^2},\\
E_{0a}&=\sqrt{\frac{2I_a}{\varepsilon_0c_0}}=2.56727\ \mathrm{V/m},\\
A_b&=10^{-6}\ \mathrm{cm^2}=10^{-10}\ \mathrm{m^2},\\
I_b&=\frac{2000}{10^{-10}}=2.00\times10^{13}\ \mathrm{W/m^2},\\
E_{0b}&=\sqrt{\frac{2I_b}{\varepsilon_0c_0}}=1.22714\times10^8\ \mathrm{V/m},\\
B_{0b}&=E_{0b}/c_0=0.409047\ \mathrm T.
\end{aligned}
$$

## ④ 2018 期中第 3 題：可見度

公式（雙光束干涉照度）：$I(\delta)=I_1+I_2+2\sqrt{I_1I_2}\cos\delta$，其中 $I_1,I_2$ 為兩束相干、平行偏振光各自的照度（W/m²）、$\delta$ 為觀察點的總相位差（rad）；$\cos\delta=+1$ 得 $I_{\max}$、$\cos\delta=-1$ 得 $I_{\min}$，本題 $I_1=NI_2$。

$$
I_{\max}=(\sqrt{I_1}+\sqrt{I_2})^2,\quad
I_{\min}=(\sqrt{I_1}-\sqrt{I_2})^2.
$$

$$I_1=NI_2\quad\Rightarrow\quad
\boxed{V=\frac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}=\frac{2\sqrt N}{N+1}}.$$

$$V=3/4,\ x=\sqrt N\ \Rightarrow\ 8x=3(x^2+1)
\ \Rightarrow\ 3x^2-8x+3=0.$$

公式（二次公式）：$ax^2+bx+c=0\ (a\ne0)\ \Rightarrow\ x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$，其中 $a,b,c$ 為實係數、$x$ 為未知數；本題 $a=3$、$b=-8$、$c=3$，因 $x=\sqrt N\gt1$ 取正號。

$$x=(4+\sqrt7)/3>1\quad\Rightarrow\quad\boxed{N=4.90733}.$$

## ⑤ 課本 7-1：完整照度與對比度

公式（總相位差）：若 $E_j=E_{0j}\cos(ks_j-\omega t+\alpha_j)$，則 $\delta=\Phi_1-\Phi_2=k(s_1-s_2)+(\alpha_1-\alpha_2)$，其中 $E_{0j}$ 為第 $j$ 束振幅（V/m）、$k$ 為波數（rad/m）、$s_j$ 為路徑長（m）、$\omega$ 為角頻率（rad/s）、$\alpha_j$ 為初相位（rad）、$\Phi_j$ 為第 $j$ 束的總相位；本題 $k(s_1-s_2)=\pi/3$、$\alpha_1=\pi/5$、$\alpha_2=\pi/6$。

公式（雙光束干涉照度）：$I_\mathrm{net}=I_1+I_2+I_{12}$，$I_{12}=2\sqrt{I_1I_2}\cos\delta$，其中 $I_1,I_2$ 為兩束各自照度（W/m²）、$I_{12}$ 為干涉交叉項（W/m²）、$\delta$ 為總相位差（rad）；本題由 $I_j=\tfrac12\varepsilon_0c_0E_{0j}^2$ 得 $2\sqrt{I_1I_2}=\varepsilon_0c_0E_{01}E_{02}$。

公式（可見度）：$V=\dfrac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}$，$I_{\max}=(\sqrt{I_1}+\sqrt{I_2})^2$、$I_{\min}=(\sqrt{I_1}-\sqrt{I_2})^2$，其中 $I_{\max},I_{\min}$ 為亮、暗紋照度（W/m²）、$V$ 為可見度（無單位）；本題代入得 $V=\dfrac{2\sqrt{I_1I_2}}{I_1+I_2}$，再用 $I_j\propto E_{0j}^2$ 寫成振幅形式。

$$
\begin{aligned}
E_{01}&=3000\ \mathrm{V/m},\quad E_{02}=4000\ \mathrm{V/m},\\
\delta&=\pi/3+\pi/5-\pi/6=11\pi/30,\\
I_1&=\tfrac12\varepsilon_0c_0E_{01}^2=11953.17\ \mathrm{W/m^2},\\
I_2&=\tfrac12\varepsilon_0c_0E_{02}^2=21250.08\ \mathrm{W/m^2},\\
I_{12}&=\varepsilon_0c_0E_{01}E_{02}\cos\delta=12964.78\ \mathrm{W/m^2},\\
I_\mathrm{net}&=I_1+I_2+I_{12}=46168.03\ \mathrm{W/m^2},\\
V&=\frac{2E_{01}E_{02}}{E_{01}^2+E_{02}^2}=\boxed{0.96}.
\end{aligned}
$$

## ⑥ 2018 期中第 4 題：楊氏雙狹縫＋薄片

公式（楊氏亮紋位置）：$d\sin\theta=m\lambda$，小角度 $\sin\theta\approx y/L$ 得 $y_m=\dfrac{m\lambda L}{d}$，相鄰間距 $\Delta y=\dfrac{\lambda L}{d}$，其中 $d$ 為雙狹縫間距（m）、$\theta$ 為觀察方向與中軸的夾角、$m$ 為整數級次、$\lambda$ 為波長（m）、$L$ 為狹縫到屏幕距離（m）、$y_m$ 為第 $m$ 亮紋到中央亮紋的距離（m）；本題 $\Delta y=1\ \mathrm{mm}$、$d=0.6\ \mathrm{mm}$、$\lambda=550\ \mathrm{nm}$。

公式（薄片造成的條紋平移）：$\Delta_\mathrm{glass}=(n-1)t$，整組條紋移動 $\Delta_\mathrm{glass}/\lambda$ 個間距，即 $|\Delta y_\mathrm{shift}|=\dfrac{\Delta_\mathrm{glass}}{\lambda}\Delta y=\dfrac{(n-1)tL}{d}$，其中 $n$ 為薄片折射率、$t$ 為薄片厚度（m）、$\Delta_\mathrm{glass}$ 為額外光程差（m）；本題 $n=1.5$、$t=200\ \mathrm{\mu m}$、$L=1.09091\ \mathrm m$。

$$
\begin{aligned}
\Delta y&=\frac{\lambda L}{d}\quad\Rightarrow\quad
L=\frac{(1\times10^{-3})(0.6\times10^{-3})}{550\times10^{-9}}\\
&=\boxed{1.09091\ \mathrm m},\\
\Delta_\mathrm{glass}&=(n-1)t=0.5(200\ \mathrm{\mu m})=100\ \mathrm{\mu m},\\
|\Delta y_\mathrm{shift}|&=\frac{(n-1)tL}{d}=\boxed{181.818\ \mathrm{mm}}.
\end{aligned}
$$

## ⑦ 課本 7-6：兩波長條紋重合

公式（雙狹縫亮紋與暗紋位置）：$y_{m,\mathrm{亮}}=\dfrac{m\lambda L}{d}\ (m=0,1,2,\ldots)$，$y_{j,\mathrm{暗}}=\dfrac{(j-\tfrac12)\lambda L}{d}\ (j=1,2,3,\ldots)$，其中 $d$ 為狹縫間距（m）、$L$ 為到屏幕距離（m）、$\lambda$ 為波長（m）、$m$ 為亮紋級次、$j$ 表示第 $j$ 個暗紋；本題第一光 $\lambda_1=436\ \mathrm{nm}$ 取 $j=4$，第二光 $\lambda_2$ 取 $m=3$。

$$
y_{4,\mathrm{暗}}^{(1)}=(4-\tfrac12)\frac{\lambda_1L}{d},\quad
y_{3,\mathrm{亮}}^{(2)}=3\frac{\lambda_2L}{d}.
$$

$$3.5\lambda_1=3\lambda_2\quad\Rightarrow\quad
\boxed{\lambda_2=\frac{3.5}{3}(436)=508.667\ \mathrm{nm}}.$$

## ⑧ 2020 期中第 3 題：群速度

公式（相速度與群速度）：$k=\dfrac{2\pi}{\lambda}$，$v_p=\dfrac{\omega}{k}$，$v_g=\dfrac{d\omega}{dk}$，其中 $\lambda$ 為波長（m）、$k$ 為波數（rad/m）、$\omega$ 為角頻率（rad/s）、$v_p$ 為相速度、$v_g$ 為群速度；本題先把 $v_p$ 寫成 $k$ 的函數，求 $\omega=kv_p$ 再對 $k$ 微分。

公式（冪次微分）：$\dfrac{d}{dk}k^a=ak^{a-1}$，其中 $a$ 為常數指數、$k$ 為自變數；本題 $a=2/3$，$g^{1/3}$ 視為常數提出。

$$
\begin{aligned}
v_p&=(g\lambda/(2\pi))^{1/3}=(g/k)^{1/3}=g^{1/3}k^{-1/3},\\
\omega&=kv_p=g^{1/3}k^{2/3},\\
v_g&=d\omega/dk=\tfrac23g^{1/3}k^{-1/3}=\boxed{\tfrac23v_p}.
\end{aligned}
$$

**注意：** 原卷 $1/3$ 冪次與「$g$ 為重力加速度」的速度量綱不合；以原卷數學形式作答是 $2/3$，若老師另外說明是深水波平方根關係，才會得到 $1/2$。

---

# H-12. 考前一頁總表：哪些「新補」最重要？

| 要練的題目 | 直接考點 | 最後答案或解題關鍵 | 本次重要程度 |
|---|---|---|---|
| **2020 第 2 題** | 球面波 $\vec E,\vec B,\vec S$ | $r_0=\sqrt{14}$ m，$E_0=38.8056$ V/m，$B_0=1.29352\times10^{-7}$ T；球面振幅 $\propto1/r$ | **最高** |
| **課本 4-19** | 圓柱波能量守恆 | $E_0\propto1/\sqrt r$；$I\propto1/r$ | **最高** |
| **課本 4-18** | 由功率求照度與場振幅 | 燈泡 $I=8.75352\times10^{-3}$；雷射 $I=2\times10^{13}$ W/m² | **最高** |
| **2018 第 3 題** | 對比度與光強比例 | $V=2\sqrt N/(N+1)$；$V=3/4\Rightarrow N=4.90733$ | **高** |
| **課本 7-1** | 初相位、光程差、干涉照度 | $\delta=11\pi/30$；$I_\mathrm{net}=46168.03$ W/m²；$V=0.96$ | **高** |
| **2018 第 4 題** | 楊氏干涉＋薄片移紋 | $L=1.09091$ m；平移 $181.818$ mm | **高** |
| **課本 7-6** | 不同波長亮暗紋重合 | $\lambda_2=508.667$ nm | **高** |
| **2020 第 3 題** | 相位／群速度推導 | 原卷印 $1/3$ 時 $v_g/v_p=2/3$（注意量綱疑點） | 中 |
| **能量密度延伸** | $u(t)$、$\overline u$、$I=v\overline u$ | 見 H-9.2 | **最高** |
| 都卜勒提醒 | 頻移方向與公式 | 靠近藍移，遠離紅移；老師說「注意一下」 | 中 |

**範圍收尾**：以老師第八～十章為優先；A 組（同頻率疊加）和 B 組（電磁波）仍是核心。D 組 TM 反射與透射不在此次範圍，已刪除。
