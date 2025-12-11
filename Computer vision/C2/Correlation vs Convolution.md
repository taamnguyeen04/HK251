
### 1. Tính Correlation (Tương quan)

Dựa vào công thức (Slide 22)1, ta giữ nguyên Kernel $H$ và nhân chồng lên vùng ảnh tương ứng.

Ma trận ảnh $3 \times 3$ (góc trái trên):

$$\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}$$

Kernel $H$:

$$\begin{bmatrix} 1 & 0 & 2 \\ -1 & 1 & 3 \\ 0 & -2 & 4 \end{bmatrix}$$

Phép tính:

$$\begin{aligned} Result &= (1 \times 1) + (2 \times 0) + (3 \times 2) \\ &+ (4 \times -1) + (5 \times 1) + (6 \times 3) \\ &+ (7 \times 0) + (8 \times -2) + (9 \times 4) \\ &= 1 + 0 + 6 - 4 + 5 + 18 + 0 - 16 + 36 \\ &= \mathbf{46} \end{aligned}$$

### 2. Tính Convolution (Tích chập)

Theo định nghĩa (Slide 20, 24)2222, trước khi nhân, ta phải xoay Kernel $H$ một góc 180 độ quanh tâm.

Bước 1: Lật Kernel ($H \rightarrow H_{flipped}$)

Kernel gốc:

$$\begin{bmatrix} 1 & 0 & 2 \\ -1 & 1 & 3 \\ 0 & -2 & 4 \end{bmatrix}$$

Kernel đã lật 180 độ (phần tử cuối lên đầu, đầu xuống cuối):

$$H_{flipped} = \begin{bmatrix} 4 & -2 & 0 \\ 3 & 1 & -1 \\ 2 & 0 & 1 \end{bmatrix}$$

**Bước 2: Nhân Kernel đã lật với vùng ảnh**

$$\begin{aligned} Result &= (1 \times 4) + (2 \times -2) + (3 \times 0) \\ &+ (4 \times 3) + (5 \times 1) + (6 \times -1) \\ &+ (7 \times 2) + (8 \times 0) + (9 \times 1) \\ &= 4 - 4 + 0 + 12 + 5 - 6 + 14 + 0 + 9 \\ &= \mathbf{34} \end{aligned}$$
---
**Kết luận:**
- Kết quả Correlation: **46**
- Kết quả Convolution: **34**