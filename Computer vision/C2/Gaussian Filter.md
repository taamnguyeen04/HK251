### 1. Bản chất Toán học (Slide 34)

Hàm Gaussian 2 chiều được biểu diễn bằng hình dáng một "quả chuông" hoặc một ngọn đồi (như hình vẽ trong slide 1).

Công thức:

$$G(x,y,\sigma)=\frac{1}{2\pi\sigma^{2}}exp(-\frac{x^{2}+y^{2}}{2\sigma^{2}})$$


**Giải thích các thành phần:**

- **$x, y$**: Là tọa độ khoảng cách tính từ tâm của bộ lọc. Tâm bộ lọc có tọa độ $(0,0)$. Càng xa tâm ($x, y$ lớn), giá trị hàm càng nhỏ.
- **$\sigma$ (Sigma)**: Đây là độ lệch chuẩn (Standard Deviation). Nó quyết định độ "bè" của ngọn đồi:
    - $\sigma$ lớn: Ngọn đồi thoải, rộng $\rightarrow$ Làm mờ ảnh nhiều hơn.
    - $\sigma$ nhỏ: Ngọn đồi nhọn, hẹp $\rightarrow$ Làm mờ ít, chỉ ảnh hưởng cục bộ gần tâm.
- **Hàm $exp$ (mũ âm)**: Đảm bảo giá trị lớn nhất nằm ở tâm và giảm dần về 0 khi ra xa tâm.

---

### 2. Từ Công thức đến Ma trận số (Slide 35)

Làm sao máy tính hiểu được hàm số liên tục trên? Người ta phải "lấy mẫu" (sampling) hàm số đó vào một lưới rời rạc (ma trận).
Hãy xem ví dụ **Kernel $3 \times 3$** với $\sigma = 0.5$ trong tài liệu3:

$$H = \begin{bmatrix} 0.0113 & 0.0838 & 0.0113 \\ 0.0838 & 0.6193 & 0.0838 \\ 0.0113 & 0.0838 & 0.0113 \end{bmatrix}$$

**Tại sao lại ra các số này?**

Để tạo ma trận $3 \times 3$, ta coi vị trí trung tâm ma trận là gốc tọa độ $(0,0)$. Khi đó các tọa độ $(x, y)$ sẽ phân bố như sau:

$$\begin{bmatrix} (-1, -1) & (0, -1) & (1, -1) \\ (-1, 0) & (0, 0) & (1, 0) \\ (-1, 1) & (0, 1) & (1, 1) \end{bmatrix}$$

Thử tính toán nháp một vài vị trí với công thức trên (với $\sigma = 0.5$):

1. **Tại tâm $(0,0)$:**
    - $x=0, y=0 \Rightarrow x^2+y^2 = 0$.
    - $exp(0) = 1$.
    - Hệ số đầu = $\frac{1}{2\pi(0.5)^2} \approx 0.636$.
    - (Lưu ý: Giá trị trong slide là $0.6193$, có thể do tác giả dùng phương pháp chuẩn hóa tổng bằng 1 hoặc sai số làm tròn, nhưng về độ lớn thì nó luôn là số lớn nhất).
        
2. **Tại lân cận gần nhất $(1,0)$ hoặc $(0,1)$:**
    - Khoảng cách đến tâm là 1. Giá trị giảm xuống đáng kể ($0.0838$).
        
3. **Tại góc chéo $(1,1)$:**
    - Khoảng cách đến tâm là $\sqrt{2} \approx 1.41$. Giá trị giảm cực mạnh xuống còn $0.0113$.
        

**Quy luật quan trọng:**

> Trong bộ lọc Gaussian, pixel ở trung tâm luôn có **trọng số cao nhất** (ảnh hưởng lớn nhất đến kết quả), các pixel càng xa tâm thì trọng số càng giảm. Điều này giúp ảnh được làm mượt nhưng vẫn giữ được cấu trúc tốt hơn so với bộ lọc trung bình (Mean filter - nơi mọi pixel có quyền lực như nhau).

---

### 3. Tại sao Ma trận $5 \times 5$ lại có nhiều số 0? (Slide 35 - Phần dưới)

Tài liệu đưa ra ví dụ thứ 2: Kernel $5 \times 5$ nhưng vẫn giữ nguyên $\sigma = 0.5$4.

Kết quả ma trận $H$ là5:

$$H = \begin{bmatrix} 0.0 & 0.0 & 0.0 & 0.0 & 0.0 \\ 0.0 & 0.0113 & 0.0837 & 0.0113 & 0.0 \\ 0.0 & 0.0837 & 0.6187 & 0.0837 & 0.0 \\ 0.0 & 0.0113 & 0.0837 & 0.0113 & 0.0 \\ 0.0 & 0.0 & 0.0 & 0.0 & 0.0 \end{bmatrix}$$

**Phân tích:**

- Bạn thấy rằng vùng lõi $3 \times 3$ ở giữa vẫn y hệt như ví dụ trước.
- Nhưng lớp viền bên ngoài (hàng 1, hàng 5, cột 1, cột 5) toàn là số `0.0000` hoặc `0.0002`.
    

Lý do:

Với $\sigma = 0.5$ (độ lệch chuẩn rất nhỏ), cái "chuông" Gaussian rất hẹp. Khi bạn đi ra xa tâm đến khoảng cách $x=2$ (vị trí ngoài cùng của ma trận $5 \times 5$), giá trị hàm số đã tiệm cận về 0.

**Bài học rút ra:**

- Nếu chọn $\sigma$ nhỏ, việc dùng kích thước Kernel lớn (như $5 \times 5$, $7 \times 7$) là **lãng phí tính toán**, vì các phần tử rìa đều xấp xỉ bằng 0, nhân vào không có tác dụng gì.
    
- Kích thước Kernel (thường gọi là window size) phải tương ứng với $\sigma$. Quy tắc ngón tay cái thường dùng là kích thước kernel nên khoảng $6\sigma$ (tức là $3\sigma$ về mỗi phía) để bao phủ hết phần "chuông" có giá trị đáng kể.