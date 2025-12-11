### 1. Giả thiết Ma trận đầu vào (Input Image Patch)

Giả sử chúng ta có một vùng ảnh kích thước $3 \times 3$. Các giá trị bên trái thấp (tối) và bên phải cao (sáng). Đây là ví dụ điển hình của một **cạnh dọc (vertical edge)**.

$$A = \begin{bmatrix} 10 & 10 & 200 \\ 10 & 10 & 200 \\ 10 & 10 & 200 \end{bmatrix}$$

### 2. Tính Gradient theo phương ngang ($g_x$)

Ta sử dụng kernel $g_x$ từ hình ảnh bạn cung cấp để phát hiện sự thay đổi theo chiều ngang.

$$K_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

Áp dụng tích chập (nhân từng phần tử tương ứng rồi cộng lại) cho tâm ma trận:

$$g_x = (-1 \cdot 10) + (0 \cdot 10) + (1 \cdot 200) \\ \quad + (-2 \cdot 10) + (0 \cdot 10) + (2 \cdot 200) \\ \quad + (-1 \cdot 10) + (0 \cdot 10) + (1 \cdot 200)$$

$$g_x = (-10 + 0 + 200) + (-20 + 0 + 400) + (-10 + 0 + 200)$$

$$g_x = 190 + 380 + 190 = \mathbf{760}$$

### 3. Tính Gradient theo phương dọc ($g_y$)

Ta sử dụng kernel $g_y$ từ hình ảnh để phát hiện sự thay đổi theo chiều dọc.

$$K_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

Tính toán:

$$g_y = (-1 \cdot 10) + (-2 \cdot 10) + (-1 \cdot 200) \\ \quad + (0 \cdot 10) + (0 \cdot 10) + (0 \cdot 200) \\ \quad + (1 \cdot 10) + (2 \cdot 10) + (1 \cdot 200)$$

$$g_y = (-10 - 20 - 200) + 0 + (10 + 20 + 200)$$

$$g_y = -230 + 0 + 230 = \mathbf{0}$$

_(Kết quả bằng 0 là hợp lý vì nhìn từ trên xuống dưới, các giá trị pixel không thay đổi: $10 \to 10$ hay $200 \to 200$)._

### 4. Tính Độ lớn (Magnitude) và Hướng (Orientation)

Dựa trên công thức trong hình ảnh:

**Độ lớn (Magnitude - Cường độ cạnh):**

$$g = \sqrt{g_x^2 + g_y^2} = \sqrt{760^2 + 0^2} = \mathbf{760}$$

**Hướng (Orientation - Góc của gradient):**

$$\theta = \tan^{-1}\left(\frac{g_y}{g_x}\right) = \tan^{-1}\left(\frac{0}{760}\right) = \tan^{-1}(0) = \mathbf{0^{\circ}} \text{ (hoặc 0 radian)}$$

---

### 5. Phân tích ý nghĩa kết quả

Từ kết quả tính toán trên ($g = 760, \theta = 0^{\circ}$), ta có thể rút ra các ý nghĩa sau:

1. **Về Magnitude ($g=760$):**
    
    - Giá trị này rất lớn, cho thấy đây là một **cạnh mạnh (strong edge)**.
        
    - Sự chênh lệch giữa vùng tối (10) và vùng sáng (200) là rất rõ rệt. Nếu $g$ nhỏ (ví dụ $< 50$), đó có thể chỉ là nhiễu hoặc sự thay đổi ánh sáng nhẹ.
        
2. **Về Orientation ($\theta = 0^{\circ}$):**
    
    - Góc $0^{\circ}$ chỉ ra hướng của **Vector Gradient**.
        
    - Vector Gradient luôn chỉ theo hướng **tăng độ sáng nhanh nhất**. Trong ví dụ này, độ sáng tăng từ Trái sang Phải, nên mũi tên gradient nằm ngang hướng sang phải ($0^{\circ}$).
        
    - **Quan trọng:** Hướng của **cạnh (edge)** luôn vuông góc với hướng gradient. Vì gradient nằm ngang ($0^{\circ}$), nên **cạnh là đường thẳng đứng ($90^{\circ}$)**. Điều này hoàn toàn khớp với ma trận mẫu (cạnh dọc phân chia bên trái và bên phải).
        
3. **Về $g_x$ và $g_y$:**
    
    - $g_x > 0$: Có sự thay đổi cường độ theo chiều ngang.
        
    - $g_y = 0$: Không có sự thay đổi cường độ theo chiều dọc.
        
    - Nếu ta xoay ma trận đi, cả $g_x$ và $g_y$ đều sẽ khác 0, và góc $\theta$ sẽ thay đổi tương ứng (ví dụ $45^{\circ}$).




---
### 1. Giả thiết Ma trận đầu vào

Để tạo một cạnh chéo mượt mà (độ sáng tăng dần từ góc trên-trái xuống góc dưới-phải), ta dùng ma trận sau:

$$A = \begin{bmatrix} 50 & 100 & 150 \\ 100 & 150 & 200 \\ 150 & 200 & 250 \end{bmatrix}$$

- **Nhận xét:** Bạn có thể thấy các đường chéo phụ (từ góc dưới-trái lên trên-phải) có giá trị bằng nhau ($100-100$, $150-150-150$, $200-200$). Điều này tạo ra một "dốc" độ sáng đi chéo xuống góc dưới phải.
    

### 2. Tính Gradient theo phương ngang ($g_x$)

Áp dụng kernel $g_x$:

$$K_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

Tính toán:

$$g_x = (-1 \cdot 50) + (0 \cdot 100) + (1 \cdot 150) \\ \quad + (-2 \cdot 100) + (0 \cdot 150) + (2 \cdot 200) \\ \quad + (-1 \cdot 150) + (0 \cdot 200) + (1 \cdot 250)$$

$$g_x = (-50 + 0 + 150) + (-200 + 0 + 400) + (-150 + 0 + 250)$$

$$g_x = 100 + 200 + 100 = \mathbf{400}$$

_(Dương: Có sự tăng độ sáng từ trái sang phải)_

### 3. Tính Gradient theo phương dọc ($g_y$)

Áp dụng kernel $g_y$:

$$K_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

Tính toán:

$$g_y = (-1 \cdot 50) + (-2 \cdot 100) + (-1 \cdot 150) \\ \quad + (0 \cdot 100) + (0 \cdot 150) + (0 \cdot 200) \\ \quad + (1 \cdot 150) + (2 \cdot 200) + (1 \cdot 250)$$

$$g_y = (-50 - 200 - 150) + 0 + (150 + 400 + 250)$$

$$g_y = -400 + 0 + 800 = \mathbf{400}$$

_(Dương: Có sự tăng độ sáng từ trên xuống dưới)_

### 4. Tính Độ lớn và Hướng

**Độ lớn (Magnitude):**

$$g = \sqrt{400^2 + 400^2} = \sqrt{320000} \approx \mathbf{565.7}$$

**Hướng (Orientation):**

$$\theta = \tan^{-1}\left(\frac{g_y}{g_x}\right) = \tan^{-1}\left(\frac{400}{400}\right) = \tan^{-1}(1) = \mathbf{45^{\circ}} \text{ (hoặc } \frac{\pi}{4} \text{ radian)}$$

---

### 5. Phân tích ý nghĩa kết quả

Đây là phần quan trọng nhất để hiểu bản chất của Sobel:

1. **Tại sao $g_x$ và $g_y$ bằng nhau?**
    
    - Vì sự thay đổi độ sáng theo chiều ngang ($50 \to 100 \to 150$) mạnh tương đương với sự thay đổi theo chiều dọc ($50 \to 100 \to 150$). Điều này chứng tỏ gradient không thiên về trục hoành hay trục tung, mà nằm ở giữa.
        
2. **Ý nghĩa của góc $\theta = 45^{\circ}$:**
    
    - Góc này cho biết hướng của **Vector Gradient**.
        
    - Trong hệ tọa độ ảnh (gốc $(0,0)$ ở trên cùng bên trái, trục $y$ hướng xuống), vector $(g_x, g_y) = (400, 400)$ sẽ hướng về phía **Đông Nam** (chéo xuống dưới bên phải).
        
    - Điều này đúng với thực tế: Góc dưới bên phải là vùng sáng nhất (250), góc trên bên trái tối nhất (50). Gradient luôn chỉ về hướng sáng nhất.
        
3. **Hướng của Cạnh (Edge Direction):**
    
    - Như đã biết, cạnh luôn **vuông góc** với gradient.
        
    - Nếu Gradient là $45^{\circ}$ (chéo xuống phải), thì **Cạnh sẽ nằm ở góc $-45^{\circ}$ (hoặc $135^{\circ}$)**.
        
    - Tức là cạnh chạy từ **góc dưới-trái lên góc trên-phải**. Nhìn vào ma trận, bạn sẽ thấy các số $150$ nằm trên đường chéo này, tạo thành ranh giới phân chia vùng tối hơn và vùng sáng hơn.