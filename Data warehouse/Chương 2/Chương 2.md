

### 1. Giới thiệu chung và Khái niệm cơ bản về Kho dữ liệu

Kho dữ liệu (Data Warehouse - DW) là một thành phần thiết yếu trong môi trường dữ liệu hiện đại, đóng vai trò là nền tảng cho các hệ thống Hỗ trợ quyết định (DSS) và Tình báo kinh doanh (BI). Định nghĩa cốt lõi của Inmon Wiley nêu rõ: **“Kho dữ liệu là một tập hợp dữ liệu có định hướng theo chủ đề, được tích hợp, không biến đổi và có tính biến thiên theo thời gian, nhằm hỗ trợ cho quá trình ra quyết định của nhà quản lý.”**

**Vai trò chính của DW và DSS:** Cung cấp "một phiên bản duy nhất của sự thật" (single version of the truth) cho doanh nghiệp, tạo nền tảng cho BI/Analytics và khả năng phân tích dài hạn, đa chiều. Đây là bước chuyển từ "Dữ liệu → Thông tin → Kiến thức → Quyết định".

### 2. Bốn đặc trưng cốt lõi của Kho dữ liệu (Theo Inmon)

1. **Subject-oriented (Định hướng theo chủ đề):** Dữ liệu được tổ chức xoay quanh các chủ đề phân tích chính (ví dụ: khách hàng, sản phẩm, bán hàng), thay vì theo chức năng nghiệp vụ như các hệ thống tác nghiệp (OLTP). Điều này giúp quản lý dễ dàng phân tích theo đối tượng quan tâm.

- _Ví dụ:_ Thay vì dữ liệu phân tán theo chức năng "bán hàng" hay "nhân sự", kho dữ liệu sẽ tập trung vào "khách hàng" hoặc "sản phẩm".

1. **Integrated (Tích hợp):** Đây là đặc trưng quan trọng nhất. Dữ liệu từ nhiều nguồn khác nhau (ERP, CRM, POS, file Excel, web logs,...) được trích xuất, chuyển đổi (reformat), chuẩn hóa (standardize), tổng hợp (summarize) và đồng nhất mã hóa (naming conventions, coding schemes) để tạo thành **“một bức tranh dữ liệu thống nhất của toàn công ty”** (single corporate image).
2. **Nonvolatile (Không biến đổi):** Dữ liệu trong kho dữ liệu chủ yếu chỉ được nạp (load) và truy vấn (access). Không có các thao tác cập nhật (update) hay xóa (delete) thường xuyên như trong hệ thống giao dịch. Điều này giúp tăng tính ổn định, đáng tin cậy và đảm bảo phân tích lịch sử không bị sai lệch.
3. **Time-variant (Biến thiên theo thời gian):** Dữ liệu luôn gắn liền với yếu tố thời gian (timestamp, ngày hiệu lực, kỳ báo cáo). Kho dữ liệu lưu trữ dữ liệu lịch sử trong nhiều năm, cho phép phân tích xu hướng, dự báo và hỗ trợ ra quyết định chiến lược.

- _Ví dụ:_ "Báo cáo doanh thu quý 3 trong 5 năm gần nhất" hoặc "Phân tích xu hướng hành vi khách hàng từ 2019–2024".

### 3. Các đặc tính mở rộng khác của Kho dữ liệu

Bên cạnh bốn đặc trưng cốt lõi của Inmon, kho dữ liệu còn có các đặc tính mở rộng sau để phục vụ phân tích và ra quyết định:

- **Granularity (Độ chi tiết dữ liệu):** Quyết định mức độ chi tiết hoặc tổng hợp của dữ liệu. Dữ liệu càng chi tiết càng linh hoạt cho phân tích nhưng dung lượng lớn, ngược lại dữ liệu tổng hợp tiết kiệm không gian và cải thiện hiệu suất.
- **Partitioning (Phân vùng dữ liệu):** Chia nhỏ dữ liệu (theo thời gian, địa lý, sản phẩm) để tối ưu quản lý và hiệu suất truy vấn.
- **Homogeneity vs. Heterogeneity (Tính đồng nhất/dị thể):** Kho dữ liệu phải xử lý cả dữ liệu đồng nhất (cùng cấu trúc) và dị thể (khác cấu trúc, nguồn gốc).
- **Auditing (Kiểm toán dữ liệu):** Theo dõi nguồn gốc và quá trình biến đổi của dữ liệu để đảm bảo minh bạch, tin cậy và tuân thủ.

### 4. Kiến trúc kho dữ liệu: Mô hình đa chiều

Để tối ưu cho phân tích (OLAP), dữ liệu trong kho dữ liệu thường được mô hình hóa theo các kiến trúc đa chiều, dựa trên hai loại bảng cốt lõi:

- **Fact Table (Bảng sự kiện):** Lưu trữ các giá trị định lượng (measures/facts) có thể đo lường, tổng hợp, tính toán (ví dụ: doanh thu, số lượng bán). Khóa chính thường là khóa tổng hợp bao gồm các khóa ngoại từ bảng Dimension.
- **Dimension Table (Bảng chiều):** Cung cấp ngữ cảnh mô tả (descriptive attributes) cho các sự kiện trong bảng Fact (ví dụ: Thời gian, Khách hàng, Sản phẩm). Được thiết kế phi chuẩn hóa (denormalized) để thuận tiện cho truy vấn OLAP và có thể có cấu trúc phân cấp.

Ba kiến trúc phổ biến nhất bao gồm:

#### 4.1. Star Schema (Sơ đồ Ngôi sao)

- **Khái niệm:** Bảng Fact nằm ở trung tâm, được bao quanh bởi các bảng Dimension. Quan hệ giữa Fact và Dimension là một-nhiều (1-n).
- **Đặc điểm:** Đơn giản, dễ hiểu, hiệu suất truy vấn cao (do các Dimension được phi chuẩn hóa), nhưng có thể dư thừa dữ liệu.
- **Ứng dụng:** Rất phù hợp cho các hệ thống OLAP và báo cáo doanh nghiệp.
- _Ví dụ:_ Fact_Sales ở trung tâm, kết nối với Dim_Date, Dim_Product, Dim_Customer, Dim_Store.

#### 4.2. Snowflake Schema (Sơ đồ Bông tuyết)

- **Khái niệm:** Các bảng Dimension được chuẩn hóa thành nhiều bảng con liên kết với nhau, tạo thành hình dạng giống bông tuyết.
- **Đặc điểm:** Giảm dư thừa dữ liệu, tăng tính toàn vẹn dữ liệu, tiết kiệm dung lượng lưu trữ. Tuy nhiên, cấu trúc phức tạp hơn Star Schema, hiệu suất truy vấn chậm hơn do phải join nhiều bảng.
- **Ứng dụng:** Phù hợp khi dữ liệu chiều có tính phân cấp phức tạp và cần tối ưu dung lượng lưu trữ.
- _Ví dụ:_ Dim_Product được tách thành Dim_Product, Dim_Brand, Dim_Category.

#### 4.3. Galaxy Schema (Sơ đồ Ngân hà / Fact Constellation)

- **Khái niệm:** Nhiều bảng Fact cùng chia sẻ các bảng Dimension chung, tạo thành một mạng lưới phức tạp.
- **Đặc điểm:** Hỗ trợ nhiều quy trình kinh doanh cùng lúc, giảm trùng lặp Dimension, cho phép phân tích liên miền (cross-functional analysis). Cấu trúc rất phức tạp, khó thiết kế và bảo trì.
- **Ứng dụng:** Mạnh mẽ trong phân tích dữ liệu đa chiều và toàn diện cho các hệ thống lớn.
- _Ví dụ:_ Fact_Sales, Fact_Inventory, Fact_Shipping cùng chia sẻ Dim_Time, Dim_Product, Dim_Store, Dim_Customer.

### 5. Chất lượng dữ liệu (Data Quality Dimensions)

Các đặc tính chất lượng dữ liệu **khác với các đặc tính cốt lõi của kho dữ liệu (Subject-Oriented, Integrated, Nonvolatile, Time-Variant)**. Đây là tập hợp tiêu chuẩn để đánh giá dữ liệu có đủ tin cậy, chính xác và hữu ích cho quá trình ra quyết định, áp dụng cho bất kỳ hệ thống thông tin nào.

Các chiều chất lượng dữ liệu bao gồm:

1. **Độ chính xác (Accuracy):** Dữ liệu phản ánh đúng thực tế khách quan.
2. **Tính đầy đủ (Completeness):** Dữ liệu không bị thiếu trường hoặc giá trị quan trọng.
3. **Tính nhất quán (Consistency):** Dữ liệu phải thống nhất trong toàn bộ hệ thống.
4. **Tính hợp lệ (Validity):** Dữ liệu tuân theo chuẩn mực, quy tắc hoặc miền giá trị.
5. **Tính kịp thời (Timeliness):** Dữ liệu phải được cập nhật đúng lúc để phục vụ ra quyết định.
6. **Tính duy nhất (Uniqueness):** Không có dữ liệu trùng lặp gây dư thừa hoặc sai lệch.
7. **Tính dễ truy cập và khả dụng (Accessibility & Availability):** Người dùng có quyền và công cụ để truy cập dữ liệu khi cần.

### 6. Vấn đề về độ mịn dữ liệu (Data Granularity)

Độ mịn dữ liệu là mức độ chi tiết hay tổng hợp của dữ liệu được lưu trữ. Quyết định về độ mịn ảnh hưởng trực tiếp đến khả năng phân tích, dung lượng lưu trữ và hiệu suất truy vấn.

- **Lợi ích:Độ mịn chi tiết cao (fine-grained):** Cho phép phân tích sâu, drill-down, trả lời nhiều câu hỏi khác nhau.
- **Độ mịn tổng hợp (coarse-grained):** Tiết kiệm không gian lưu trữ, cải thiện tốc độ truy vấn, phù hợp với báo cáo quản trị cấp cao.
- **Thách thức:**Mức chi tiết cao đòi hỏi nhiều dung lượng và phức tạp trong quản lý.
- Mức tổng hợp hạn chế khả năng phân tích chi tiết.
- **Mô hình hai cấp độ (Dual Levels of Granularity - Inmon):** Kho dữ liệu thường cần kết hợp cả **Atomic data (dữ liệu chi tiết nhất)** và **Summary data (dữ liệu tóm tắt)** để cân bằng giữa khả năng phân tích sâu và hiệu quả tài nguyên.
- **Ý nghĩa:** Đây là quyết định cốt lõi trong thiết kế kho dữ liệu, đòi hỏi cân nhắc kỹ lưỡng giữa nhu cầu phân tích chi tiết và khả năng tối ưu tài nguyên.

**Các vấn đề khác được đề cập nhưng chưa được trình bày chi tiết trong tài liệu nguồn, sẽ được thảo luận trong các buổi học tiếp theo:**

- Vấn đề về chuyển đổi dữ liệu
- Vấn đề về dữ liệu dẫn xuất
- Vấn đề về siêu dữ liệu
- Các vấn đề khác về kho dữ liệu