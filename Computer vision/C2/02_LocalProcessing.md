A increases pass 1 the contribution of sharpening process becomes less and less important 
# Xử lý cục bộ trên ảnh

## 1. Khái niệm xử lý cục bộ

- **Định nghĩa:** Xử lý cục bộ là phép toán trên ảnh trong đó giá trị điểm ảnh I(u, v) được thay đổi dựa trên một hàm của các điểm ảnh nằm trong vùng lân cận của nó.
- **Ví dụ:**
    - Ảnh đầu vào I(u,v) với một điểm ảnh và vùng lân cận 3×3.
    - Các loại hàm:
        - **Hàm tuyến tính:** trung bình, dịch chuyển, Gaussian, phát hiện biên.
        - **Hàm phi tuyến:** median, min, max.

Ví dụ:
- Hàm trung bình 3×3:

$I'(u,v) = \frac{1}{9}\sum_{i=-1}^{1}\sum_{j=-1}^{1} I(u+i, v+j)$

→ ảnh đầu ra bị mờ, làm trơn.
- Hàm median 3×3: loại bỏ nhiễu trong ảnh.

---

## 2. Xử lý tuyến tính

- **Hàm trung bình tổng quát:**

$I'(u,v) = \frac{1}{(2r+1)\times(2r+1)} \sum_{i=-r}^{r} \sum_{j=-r}^{r} I(u+i, v+j)$

- Có thể biểu diễn qua ma trận $H_{corr}$.
- Nếu thay đổi ma trận $H_{corr}$, ta có thể xây dựng các phép biến đổi khác:
    - Phát hiện biên (Sobel).
    - Dịch chuyển điểm ảnh.

---

## 3. Tương quan (Correlation)

- **Định nghĩa:**

$I'_{corr}(u,v) = \sum_{i=-r}^{r} \sum_{j=-r}^{r} I(u+i, v+j) \cdot H_{corr}(i,j)$

- **Cách tính:**
    1. Đặt ma trận $H_{corr}$ tại vị trí điểm ảnh (u,v)(u,v).
    2. Nhân từng hệ số của $H_{corr}$ với điểm ảnh tương ứng.
    3. Cộng các giá trị này.
    4. Gán vào I'(u,v).

---

## 4. Tích chập (Convolution)

- **Định nghĩa:**

$I'_{conv}(u,v) = \sum_{i=-r}^{r} \sum_{j=-r}^{r} I(u-i, v-j) \cdot H_{conv}(i,j)$

- Ký hiệu:

$I'_{conv}(u,v) = I \ast H_{conv}$

- **Khác biệt với tương quan:** chỉ khác dấu của chỉ số trong công thức.
- Có thể chuyển đổi giữa hai phép bằng cách xoay ma trận 180° hoặc lật theo trục.

---

## 5. Lọc tuyến tính (Linear Filtering)

- **Định nghĩa:** áp dụng phép tương quan hoặc tích chập giữa ảnh và một ma trận HH (kernel).
- **Tên gọi khác của kernel:** cửa sổ, mặt nạ, template, vùng cục bộ.

---

## 6. Các bộ lọc tuyến tính phổ biến

- **Bộ lọc trung bình (Mean filter):** làm mờ ảnh, giảm nhiễu ngẫu nhiên.
- **Bộ lọc Gaussian:** làm mượt ảnh bằng hàm phân phối chuẩn 2D.
- **Bộ lọc dịch chuyển (Shifting filter):** dịch điểm ảnh sang vị trí khác dựa vào kernel.

---

## 7. Tính chất của tích chập

- **Giao hoán:** $I \ast H = H \ast I$.
- **Kết hợp:** $(I \ast H_1) \ast H_2 = I \ast (H_1 \ast H_2)$.
- **Tuyến tính:**
    $(\alpha I) \ast H = \alpha (I \ast H), \quad (I_1 + I_2)\ast H = I_1\ast H + I_2\ast H$
- **Bất biến dịch chuyển (Shift-invariance).**
- **Khả tách (Separability):** kernel có thể tách thành nhiều kernel nhỏ hơn → giảm chi phí tính toán.
    

---

## 8. Xử lý tại biên ảnh

Các phương pháp khi kernel vượt khỏi biên ảnh:
1. **Cắt bớt (Cropping):** bỏ qua biên.
2. **Đệm (Padding):** thêm dải 0.
3. **Mở rộng (Extending):** sao chép giá trị biên ra ngoài.
4. **Phản chiếu (Wrapping):** phản chiếu giá trị biên.

---

## 9. Cài đặt tích chập

- **Trong miền không gian:**
    - Dùng kỹ thuật cửa sổ trượt.
    - Có thể tối ưu cho các trường hợp đặc biệt.
- **Trong miền tần số:**
    - Giảm độ phức tạp, không phụ thuộc kích thước kernel (sẽ học trong chương sau).
- **Độ phức tạp tính toán:**
    - Phụ thuộc trực tiếp kích thước kernel.
    - Kernel lớn → tốn nhiều phép nhân/cộng hơn.
        

Ví dụ:

- Dịch ảnh 10 pixel sang trái: dùng 1 kernel 21×21 tốn nhiều hơn so với áp dụng 10 lần kernel 3×3.
    

---

## 10. Các kỹ thuật tối ưu

- **Khả tách kernel (Separability):** áp dụng lần lượt hai kernel nhỏ thay vì kernel lớn.
- **Box filter và Integral image:** tận dụng tổng tích lũy để tính nhanh hơn.

Ví dụ 1D và 2D Integral image cho phép tính tổng trong một vùng bất kỳ bằng vài phép cộng/trừ đơn giản.
