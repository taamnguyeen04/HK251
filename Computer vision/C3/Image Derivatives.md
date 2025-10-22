

Tài liệu này tổng hợp các khái niệm và kỹ thuật cốt lõi liên quan đến đạo hàm ảnh, một công cụ toán học cơ bản trong xử lý ảnh và thị giác máy tính. Mục tiêu chính của việc sử dụng đạo hàm là để phát hiện và định lượng sự thay đổi về cường độ điểm ảnh, từ đó xác định các đặc trưng quan trọng như biên và chi tiết.

**Các điểm chính bao gồm:**

• **Đạo hàm cấp một (Gradient):** Được sử dụng để đo lường tốc độ và hướng thay đổi cường độ. Độ lớn của vector gradient cho biết "sức mạnh" của một biên, trong khi hướng của nó chỉ ra chiều của sự thay đổi lớn nhất. Các toán tử như Sobel, Prewitt và Robert là những bộ lọc phổ biến để xấp xỉ giá trị đạo hàm cấp một.

• **Đạo hàm cấp hai (Toán tử Laplacian):** Nhạy cảm hơn với các chi tiết nhỏ, đường mảnh và nhiễu. Nó được sử dụng để xác định vị trí chính xác của biên thông qua việc phát hiện các điểm "vượt qua không" (zero-crossing). Đặc tính này làm cho nó trở thành một công cụ hiệu quả để tinh chỉnh các đặc trưng ảnh.

• **Ứng dụng làm sắc nét ảnh:** Toán tử Laplacian là nền tảng cho các kỹ thuật làm sắc nét ảnh. Bằng cách cộng hoặc trừ kết quả của bộ lọc Laplacian vào ảnh gốc, các biên và chi tiết sẽ được nhấn mạnh, tạo ra một hình ảnh rõ nét hơn.

• **Kỹ thuật nâng cao:** Các phương pháp như **Unsharp Masking** (làm sắc nét bằng cách trừ đi một phiên bản mờ của ảnh) và **High-boost Filtering** (một dạng tổng quát của Unsharp Masking) cung cấp các cơ chế linh hoạt để tăng cường chi tiết. High-boost Filtering không chỉ làm sắc nét mà còn có khả năng làm sáng các vùng ảnh tối.

Tóm lại, đạo hàm cấp một và cấp hai cung cấp một bộ công cụ mạnh mẽ để trích xuất đặc trưng và nâng cao chất lượng ảnh. Việc hiểu và áp dụng các kỹ thuật này là nền tảng cho nhiều tác vụ phức tạp trong thị giác máy tính, từ nhận dạng đối tượng đến phân tích hình ảnh y tế.

--------------------------------------------------------------------------------

1. Mô Hình Ảnh và Nguyên Tắc Đạo Hàm

1.1. Mô Hình Ảnh Dưới Dạng Hàm Số

Trong xử lý ảnh, một ảnh kỹ thuật số được mô hình hóa như một hàm hai biến `f(x, y)`, trong đó `x` và `y` là tọa độ không gian, và giá trị của hàm tại mỗi điểm là cường độ sáng (ví dụ: mức xám). Dưới góc độ này, ảnh có thể được xem như một bề mặt ba chiều trên không gian hai chiều.

1.2. Nguyên Tắc Toán Học của Đạo Hàm

Đạo hàm của một hàm số đo lường tốc độ thay đổi của hàm đó. Trong xử lý ảnh, đạo hàm được sử dụng để phát hiện những nơi có sự thay đổi đột ngột về cường độ, thường tương ứng với các biên của đối tượng.

Dựa trên khai triển Taylor, đạo hàm cấp một có thể được xấp xỉ bằng các phương pháp sau trong miền rời rạc:

• **Xấp xỉ tiến (Forward Approximation):** `f'(x) ≈ f(x+1) - f(x)`

• **Xấp xỉ lùi (Backward Approximation):** `f'(x) ≈ f(x) - f(x-1)`

• **Xấp xỉ trung tâm (Central Approximation):** `f'(x) ≈ (f(x+1) - f(x-1)) / 2`

2. Đạo Hàm Cấp Một: Phát Hiện Biên và Hướng

Đạo hàm cấp một được sử dụng để phát hiện sự tồn tại của các biên trong ảnh.

2.1. Phép Toán Gradient

Gradient tại một điểm ảnh là một vector `∇f` chứa các đạo hàm riêng theo hai hướng `x` và `y`:

`∇f = [ fx; fy ]`

Vector gradient có hai thuộc tính quan trọng:

• **Độ lớn (Magnitude):** Cho biết tốc độ thay đổi cường độ tại một điểm, hay "sức mạnh" của biên. Nó được tính bằng công thức `|∇f| = √(fx² + fy²)`, hoặc xấp xỉ bằng `|∇f| ≈ |fx| + |fy|`. Giá trị độ lớn càng cao, biên càng rõ nét.

• **Hướng (Angle):** Cho biết hướng của sự thay đổi cường độ lớn nhất. Nó được tính bằng công thức `θ(∇f) = tan⁻¹(fy / fx)`. Vector gradient luôn vuông góc với hướng của biên tại điểm đó.

2.2. Triển Khai Bằng Bộ Lọc Tuyến Tính (Kernel)

Trong thực tế, đạo hàm cấp một được tính toán bằng cách áp dụng phép tích chập (convolution) giữa ảnh và một ma trận nhỏ gọi là kernel (nhân). Các kernel khác nhau nhấn mạnh các đặc điểm khác nhau.

|   |   |   |
|---|---|---|
|Tên Toán Tử|Kernel Đạo Hàm theo trục X|Kernel Đạo Hàm theo trục Y|
|**Đơn giản**|`[-1 0 1]`|`[-1; 0; 1]`|
|**Robert**|`[-1 0; 0 1]`|`[0 -1; 1 0]`|
|**Prewitt**|`[-1 0 1; -1 0 1; -1 0 1]`|`[-1 -1 -1; 0 0 0; 1 1 1]`|
|**Sobel**|`[-1 0 1; -2 0 2; -1 0 1]`|`[-1 -2 -1; 0 0 0; 1 2 1]`|

2.3. Đặc Điểm

• **Phát hiện biến đổi:** Đạo hàm cấp một làm nổi bật sự thay đổi cường độ theo các trục tọa độ.

• **Giá trị âm và dương:** Kết quả có thể là giá trị dương hoặc âm.

• **Biên dày:** Thường tạo ra các đường biên dày hơn so với đạo hàm cấp hai.

• **Phản ứng với bước nhảy:** Phản ứng mạnh mẽ với các thay đổi đột ngột về mức xám (step edges).

3. Đạo Hàm Cấp Hai: Tinh Chỉnh và Làm Sắc Nét

Đạo hàm cấp hai đo lường sự thay đổi của đạo hàm cấp một, giúp xác định các chi tiết tinh vi và vị trí chính xác của biên.

3.1. Toán Tử Laplacian

Toán tử Laplacian `∇²f` là tổng của các đạo hàm riêng cấp hai theo hai trục `x` và `y`:

`∇²f = (∂²f / ∂x²) + (∂²f / ∂y²)`

Nó được triển khai bằng các kernel, trong đó hệ số trung tâm có thể là dương hoặc âm.

|   |   |   |
|---|---|---|
|Đặc điểm Kernel|Kernel 4 lân cận|Kernel 8 lân cận|
|**Hệ số trung tâm dương**|`[0 -1 0; -1 4 -1; 0 -1 0]`|`[-1 -1 -1; -1 8 -1; -1 -1 -1]`|
|**Hệ số trung tâm âm**|`[0 1 0; 1 -4 1; 0 1 0]`|`[1 1 1; 1 -8 1; 1 1 1]`|

3.2. So Sánh Đạo Hàm Cấp Một và Cấp Hai

|   |   |   |
|---|---|---|
|Đặc điểm|Đạo hàm Cấp Một (Gradient)|Đạo hàm Cấp Hai (Laplacian)|
|**Phản ứng với biên**|Tạo ra biên dày, phản ứng mạnh tại các bước nhảy cường độ.|Tạo ra phản ứng kép (một dương, một âm) tại biên.|
|**Phát hiện biên**|Dựa trên độ lớn của gradient.|Dựa trên điểm "vượt qua không" (zero-crossing), cho vị trí biên chính xác hơn.|
|**Phản ứng với chi tiết**|Kém nhạy hơn với các chi tiết nhỏ.|Rất nhạy với các chi tiết nhỏ, đường mảnh và nhiễu.|

4. Các Ứng Dụng Nâng Cao

4.1. Làm Sắc Nét Ảnh bằng Laplacian

Toán tử Laplacian có đặc tính làm nổi bật các điểm thay đổi đột ngột (biên) và làm mờ các vùng có cường độ thay đổi chậm. Dựa vào đặc tính này, ta có thể làm sắc nét ảnh gốc.

Phương pháp được định nghĩa như sau: `g(x, y) = f(x, y) + c * ∇²f(x, y)`

Trong đó:

• `f(x, y)` là ảnh gốc.

• `g(x, y)` là ảnh đã được làm sắc nét.

• `c` là -1 nếu hệ số trung tâm của kernel Laplacian là âm, và `c` là +1 nếu hệ số trung tâm là dương.

Quá trình này có thể được thực hiện bằng một bộ lọc tuyến tính duy nhất, ví dụ, kernel `[0 -1 0; -1 5 -1; 0 -1 0]` là kết hợp của ảnh gốc và toán tử Laplacian.

4.2. Lọc Unsharp Masking và High-Boost

Đây là những kỹ thuật làm sắc nét phổ biến và hiệu quả.

**Unsharp Masking:**

• **Nguyên lý:** Một ảnh được làm sắc nét bằng cách trừ đi một phiên bản làm mờ của chính nó.

• **Công thức:** `fs(x, y) = f(x, y) - f̄(x, y)`, trong đó `f̄(x, y)` là phiên bản mờ của ảnh gốc `f(x, y)`.

**High-Boost Filtering:**

• **Nguyên lý:** Là một dạng tổng quát hóa của Unsharp Masking.

• **Công thức:** `fhb(x, y) = A * f(x, y) - f̄(x, y)`, với `A ≥ 1`.

    ◦ Khi `A = 1`, nó trở thành Unsharp Masking.

    ◦ Khi `A > 1`, một phần của ảnh gốc được cộng trở lại, giúp giữ lại các chi tiết nền.

• **Ứng dụng:** Kỹ thuật này không chỉ làm sắc nét hình ảnh mà còn có thể được sử dụng để làm sáng các hình ảnh tối.

Kỹ thuật High-boost cũng có thể được triển khai bằng một bộ lọc tuyến tính duy nhất với các kernel như:

• `Hhb4 = [0 -1 0; -1 A+4 -1; 0 -1 0]`

• `Hhb8 = [-1 -1 -1; -1 A+8 -1; -1 -1 -1]`