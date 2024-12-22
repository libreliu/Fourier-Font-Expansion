# Fourier-Font-Expansion

## Setup

### Windows

### Linux


## 文件

## 解释

### Bezier 样条曲线

给定控制点 $ P_0, P_1, P_2, P_3 $，那么 Bezier 曲线可以表示成如下的参数形式：

$$
B(t) = (1-t)^3 P_0 + 3 (1-t)^2 t P_1 + 3 (1-t) t^2 P_2 + t^3 P_3 \quad \text{where}\ t \in [0, 1] 
$$

现在如果有多段 Bezier 样条曲线 $ B_1, .., B_n $，且满足 $ C_0 $ 连续，即 $ B_i(1) = B_{i+1}(0) $，那么可以重参数化

$$
B_c (t) = \left\{
\begin{aligned}
& B_1(nt) & t \in [0, 1 / n] \\
& B_2(nt - 1) & t \in [1 / n, 2 / n] \\
& \cdots &  \\
& B_i(nt - (i-1)) & t \in [(i-1) / n, i / n] \\
& \cdots &  \\
& B_n(nt - (n-1)) & t \in [(n-1)/n, 1] \\
\end{aligned}
\right.
$$

使得合并后的曲线 $ B_c(t) $ 满足 $ t \in [0, 1] $，且满足 $ C_0 $ 连续，则可以进行傅里叶展开

自然，曲线也可以重参数化到 $ [0, 2\pi] $，令 $ t = {t_r} / {2\pi} $，得到

$$
B_{c} (t_r / 2\pi) = \left\{
\begin{aligned}
& B_1(n (t_r / 2\pi)) & t_r \in [0, 2\pi / n] \\
& B_2(n (t_r / 2\pi) - 1) & t \in [2\pi / n, 4\pi / n] \\
& \cdots &  \\
& B_i(n (t_r / 2\pi) - (i-1)) & t \in [2\pi (i-1) / n, 2\pi (i / n)] \\
& \cdots &  \\
& B_n(n (t_r / 2\pi) - (n-1)) & t \in [2\pi (n-1)/n, 2\pi] \\
\end{aligned}
\right.
$$

把 $ B_i(n (t_r / 2\pi) - (i-1)) $ 写开可以得到

$$
\begin{aligned}
B_i \left( n \frac{t_r}{2\pi} - (i-1) \right) &= \left( 1 - n \frac{t_r}{2\pi} + (i-1) \right)^3 P_{i_0} \\
&+ 3 \left( 1 - n \frac{t_r}{2\pi} + (i-1) \right)^2 \left( n \frac{t_r}{2\pi} - (i-1) \right) P_{i_1} \\
&+ 3 \left( 1 - n \frac{t_r}{2\pi} + (i-1) \right) \left( n \frac{t_r}{2\pi} - (i-1) \right)^2 P_{i_2} \\
&+ \left( n \frac{t_r}{2\pi} - (i-1) \right)^3 P_{i_3}
\end{aligned}
$$

### Fourier 展开

二维参数曲线 $ B_i(t) $ 定义在 $ [0, 2\pi] $ 上，现在我们希望将其可视化。

鉴于 $ B_i(t) $ 的结果是一个二维向量，一个自然的想法是将其 $ x(t) $ 和 $ y(t) $ 分量作为两个独立的函数，分别进行 Fourier 展开。

Fourier 展开后，会产生下面的形式

$$
\left\{
\begin{aligned}
x(t) &= a_0 + \sum_{i=1}^{\infty} a_n \cos{(nt)} + b_n \sin{(nt)} \\
y(t) &= c_0 + \sum_{i=1}^{\infty} c_n \cos{(nt)} + d_n \sin{(nt)} \\
\end{aligned}
\right.
$$

而我们的目标是把他们表示成一些圆形轨迹旋转的向量的集合。集合中的向量 $ v_i $ 可以逆时针旋转

$$
v_i(t) = M_i (\cos{(k_i t + \phi_i)} \cdot \mathbf{\vec {e_1}} + \sin{(k_i t + \phi_i)} \cdot \mathbf{\vec {e_2}})
$$

或者顺时针旋转
$$
v_{-i}(t) = M_{-i} (\cos{(k_i t + \phi_{-i})} \cdot \mathbf{\vec {e_1}} - \sin{(k_i t + \phi_{-i})} \cdot \mathbf{\vec {e_2}})
$$

这样可以用 $ \{ \dots, v_{-i}(t), \dots, v_0(t), \dots, v_{i}(t), \dots \} $ 的运动的线性叠加来凑整个可视化的效果。

那么，应该如何凑呢？考虑到

$$
M_i e^{\phi} e^{ikt} = M_i (\cos{(kt + \phi)} - i\sin{(kt + \phi)})
$$

所以，其实可以采用复 Fourier 展开的结果，并将其相应的复系数拆分为模和辐角，以此来进行可视化。

> See also: 
> - 3B1B 的视频 [【官方双语】微分方程概论-第四章：但什么是傅立叶级数呢？-从热流到画圈圈 (bilibili)](https://www.bilibili.com/video/BV1vt411N7Ti)

### 复 Fourier 展开

考虑对值域在复平面的函数 $ F(t) \in \mathbb{C} $ 的复 Fourier 展开
$$
F(t) = \sum_{k=-\infty}^{\infty} c_k e^{ik t}
$$

其中，
$$
c_k = \frac{1}{2\pi} \int_{0}^{2 \pi} F(t) e^{-ik t} dt
$$

这里直接采用数值积分的方式来进行计算会比较方便，不需要求出解析解；虽然，作为次数不超过二次的多项式，求出解析的积分解是相对平凡的。



### 相关链接


https://www.bilibili.com/video/BV1vt411N7Ti 3b1b 指出可以用复表示很方便的做，sin/cos 表示会比较费劲

可视化一个可以这样：https://www.bilibili.com/video/BV1xb411y7EL

https://www.youtube.com/watch?v=Mm2eYfj0SgA
  