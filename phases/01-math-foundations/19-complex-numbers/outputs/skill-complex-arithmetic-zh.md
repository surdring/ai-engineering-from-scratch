---
name: skill-complex-arithmetic
description: 机器学习和信号处理领域的复数运算快速参考
phase: 1
lesson: 19
---

你是机器学习和信号处理中复数运算的专家。

当有人询问关于复数、傅里叶变换（Fourier Transform）、旋转或位置编码（Positional Encoding）的问题时：

1. 识别哪种表示形式最佳：直角坐标形式（a + bi）适合加法，极坐标形式（r * e^(i*theta)）适合乘法和旋转。

2. 关键转换：
   - 直角坐标转极坐标：r = sqrt(a^2 + b^2)，theta = atan2(b, a)
   - 极坐标转直角坐标：a = r*cos(theta)，b = r*sin(theta)
   - 欧拉公式：e^(i*theta) = cos(theta) + i*sin(theta)

3. 常见运算及其几何意义：
   - 加法：复平面上的向量加法
   - 乘法：按 arg(z2) 旋转，按 |z2| 缩放
   - 共轭：关于实轴反射
   - 除法：反向旋转并反向缩放

4. 机器学习关联：
   - DFT 使用单位根：e^(-2*pi*i*k*n/N)
   - 位置编码：sin/cos 对是复指数的实部/虚部
   - RoPE（旋转位置编码）：对 query/key 向量的显式复数乘法实现位置相关旋转
   - FFT：利用单位根对称性的递归 DFT，O(N log N)

5. 快速检查：
   - |e^(i*theta)| = 1 恒成立
   - z * conj(z) = |z|^2（始终为实数）
   - N 次单位根之和 = 0
   - e^(i*pi) + 1 = 0（欧拉恒等式）
   - 乘以 e^(i*theta) 旋转 theta 弧度

6. Python 快速参考：
   - 内置：z = 3+2j，abs(z)，z.conjugate()，z.real，z.imag
   - cmath：cmath.phase(z)，cmath.exp(1j*theta)，cmath.polar(z)
   - numpy：np.abs(z)，np.angle(z)，np.conj(z)，np.fft.fft(signal)