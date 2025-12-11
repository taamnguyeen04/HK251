
<audio controls>
  <source src="audio/Chương 1 Tổng quan.m4a" type="audio/mpeg">
  Trình duyệt của bạn không hỗ trợ phát audio.
</audio>

# 1. Khái niệm Kho dữ liệu (Data Warehouse - DW)

Kho dữ liệu được định nghĩa bởi Bill Inmon (Building the Data Warehouse, 4th Edition – Bill Inmon, 2005) là:

"một tập hợp dữ liệu có định hướng theo chủ đề, được tích hợp từ nhiều nguồn, có tính lịch sử và không thay đổi, nhằm hỗ trợ quá trình ra quyết định trong tổ chức."

**Các đặc điểm chính của Kho dữ liệu:**

- **Chủ đề (Subject-oriented):** Tập trung vào các chủ đề kinh doanh cụ thể (khách hàng, sản phẩm, doanh thu...) thay vì các giao dịch hàng ngày.
- **Tích hợp (Integrated):** Dữ liệu được hợp nhất từ nhiều nguồn khác nhau, đảm bảo tính đồng nhất.
- **Có tính lịch sử (Time-variant):** Lưu giữ dữ liệu trong quá khứ để phân tích xu hướng và sự thay đổi theo thời gian.
- **Không thay đổi (Non-volatile):** Dữ liệu trong DW không bị ghi đè hay xóa thường xuyên, chỉ được thêm mới.

**Granularity (Độ chi tiết dữ liệu):** Đây là mức độ chi tiết hoặc tổng hợp của dữ liệu trong DW, ảnh hưởng trực tiếp đến kích thước lưu trữ, tốc độ truy vấn và khả năng phân tích.

- **Fine Granularity (Độ chi tiết cao):** Lưu dữ liệu ở mức chi tiết nhất (transaction-level), ví dụ: mỗi hóa đơn bán hàng.
- **Ưu điểm:** Phân tích chi tiết, linh hoạt.
- **Nhược điểm:** Tốn dung lượng, truy vấn chậm hơn.
- **Coarse Granularity (Độ chi tiết thấp – dữ liệu tổng hợp):** Lưu dữ liệu đã được tổng hợp (summary-level), ví dụ: doanh số theo ngày, doanh thu theo tháng.
- **Ưu điểm:** Tiết kiệm dung lượng, truy vấn nhanh.
- **Nhược điểm:** Mất chi tiết, không drill-down được sâu.

**Nguyên tắc thiết kế Granularity:** Thường thì DW ưu tiên lưu dữ liệu chi tiết (fine-grained), sau đó tạo các bảng/tầng dữ liệu tổng hợp (summary tables) để tối ưu hiệu suất truy vấn. Cách tiếp cận này giúp cân bằng giữa việc lưu giữ dữ liệu gốc để phân tích khi cần và sử dụng dữ liệu tổng hợp cho báo cáo nhanh.

**ETL (Extract – Transform – Load):** Là quy trình cốt lõi trong việc xây dựng Kho dữ liệu, có nhiệm vụ thu thập, xử lý và nạp dữ liệu vào DW.

- **Extract (Trích rút dữ liệu):** Thu thập dữ liệu từ nhiều nguồn khác nhau (OLTP, ERP, CRM, POS, Excel, log web...).
- **Transform (Biến đổi dữ liệu):** Giai đoạn xử lý quan trọng nhất, bao gồm chuẩn hóa định dạng, làm sạch dữ liệu (xử lý trùng, thiếu, sai), tích hợp, tính toán, tổng hợp, mã hóa... Mục tiêu là biến dữ liệu thô thành dữ liệu chính xác, nhất quán, phù hợp để phân tích.
- **Load (Nạp dữ liệu):** Nạp dữ liệu đã xử lý vào DW hoặc Data Mart, có thể là Full Load (nạp toàn bộ) hoặc Incremental Load (chỉ nạp dữ liệu mới/thay đổi). 

**Ý nghĩa của ETL:** "Là cầu nối giúp dữ liệu từ nhiều hệ thống khác nhau trở nên nhất quán và đáng tin cậy. Đảm bảo kho dữ liệu luôn cập nhật, chính xác, đầy đủ. Giúp cho việc phân tích, báo cáo và ra quyết định trong BI (Business Intelligence) và DSS (Decision Support System) trở nên hiệu quả."

**Data Mart:** Là một phân vùng nhỏ của Kho dữ liệu, được thiết kế để phục vụ một bộ phận, lĩnh vực kinh doanh hoặc nhóm người dùng cụ thể. "Nếu Data Warehouse là “thư viện tổng hợp” của doanh nghiệp, thì Data Mart giống như “tủ sách chuyên ngành” cho từng phòng ban."

- **Đặc điểm:** Phạm vi hẹp (Marketing, Tài chính, Nhân sự), nguồn dữ liệu có thể từ DW hoặc OLTP, dễ triển khai, tối ưu cho người dùng cụ thể.
- **Các loại:** Dependent Data Mart (trích xuất từ DW trung tâm), Independent Data Mart (xây dựng trực tiếp từ nguồn giao dịch), Hybrid Data Mart (kết hợp cả hai).
- **Ý nghĩa:** Giúp các bộ phận nhanh chóng truy cập dữ liệu phù hợp, giảm tải cho DW trung tâm, thúc đẩy ra quyết định nhanh và chuyên sâu.

**So sánh OLTP (Online Transaction Processing) và OLAP (Online Analytical Processing) DW:**

- **OLTP:** Tập trung vào vận hành, xử lý giao dịch tức thì (ví dụ: ghi nhận hóa đơn bán hàng).
- **OLAP/DW:** Tập trung vào phân tích, hỗ trợ quyết định, xử lý khối lượng dữ liệu lớn, thường là dữ liệu lịch sử (ví dụ: phân tích xu hướng doanh thu theo tháng).

# 2. Ý nghĩa của Kho dữ liệu

- **Nền tảng cho BI, DSS, Data Mining:** DW cung cấp dữ liệu đáng tin cậy cho các hệ thống này.
- **Cái nhìn toàn diện:** Giúp doanh nghiệp có cái nhìn tổng thể thay vì dữ liệu phân tán, rời rạc.
- **Tăng tính chính xác và tin cậy:** Cung cấp thông tin chất lượng cao để ra quyết định.
- **Lợi ích cụ thể:** Hỗ trợ phân tích xu hướng (dự báo nhu cầu), tích hợp dữ liệu từ nhiều nguồn (tránh trùng lặp, mâu thuẫn), nâng cao hiệu quả quản trị điều hành và ra quyết định chiến lược.
- **Ví dụ:** Một công ty bán lẻ dùng DW để tổng hợp và phân tích xu hướng mua hàng, từ đó quyết định nhập kho trong tháng tới. Các doanh nghiệp lớn như Amazon, Walmart minh họa sức mạnh của DW trong dự báo tồn kho và cá nhân hóa dịch vụ.

# 3. Vai trò của Kho dữ liệu

- **Trong hệ thống thông tin doanh nghiệp:** Là "Cầu nối giữa dữ liệu vận hành và dữ liệu cho ra quyết định."
- **Trong quản lý:Ban giám đốc:** Hoạch định chiến lược dài hạn.
- **Bộ phận tài chính:** Phân tích lợi nhuận, chi phí.
- **Marketing:** Phân khúc khách hàng, đánh giá hiệu quả chiến dịch.
- **Sản xuất:** Tối ưu quy trình, dự báo nhu cầu.
- **Trong DSS (Decision Support System):** "Cung cấp dữ liệu nền để DSS hoạt động. Biến dữ liệu thô thành tri thức phục vụ phân tích." Nhấn mạnh rằng "DSS không thể hoạt động hiệu quả nếu thiếu DW."
- **Vai trò chiến lược:** Biến dữ liệu thô thành tri thức để phục vụ phân tích và ra quyết định.

# 4. Ứng dụng trong việc hỗ trợ ra quyết định ở các mức quản lý khác nhau

DW hỗ trợ ra quyết định ở ba cấp độ chính trong một tổ chức:

- **Cấp tác nghiệp (Operational):**
- **Đặc điểm thông tin:** Chi tiết, thời gian thực.
- **Hỗ trợ:** Quyết định trong công việc hàng ngày.
- **Ví dụ:** Xác định sản phẩm nào bán chạy nhất trong tuần để bổ sung hàng ngay lập tức; Báo cáo bán hàng ngày.
- **Cấp quản lý trung gian (Tactical):**
- **Đặc điểm thông tin:** Tổng hợp theo chu kỳ (tuần/tháng).
- **Hỗ trợ:** Quyết định ngắn hạn, quản lý bộ phận.
- **Ví dụ:** Phân tích hiệu quả chương trình khuyến mãi theo khu vực; Đánh giá hiệu quả marketing.
- **Cấp chiến lược (Strategic):**
- **Đặc điểm thông tin:** Dữ liệu lịch sử, xu hướng dài hạn.
- **Hỗ trợ:** Hoạch định dài hạn, định hướng toàn công ty.
- **Ví dụ:** Phân tích xu hướng thị trường 5 năm để định hướng phát triển sản phẩm mới; Dự báo nhu cầu 5 năm.

Dù cùng một kho dữ liệu, cách sử dụng và mức độ chi tiết thông tin sẽ khác nhau tùy theo cấp độ quản lý để phù hợp với nhu cầu ra quyết định của từng cấp.

**Tóm tắt các ý chính đã học:**

- **Khái niệm:** DW theo Bill Inmon (định hướng chủ đề, tích hợp, có lịch sử, không thay đổi, hỗ trợ ra quyết định). Phân biệt OLTP và DW/OLAP. Quy trình ETL (Extract – Transform – Load). Data Mart (phân vùng nhỏ của DW).
- **Ý nghĩa:** DW là nền tảng cho BI, DSS, Data Mining, cung cấp cái nhìn toàn diện, dữ liệu chính xác, đáng tin cậy, hỗ trợ phân tích xu hướng và tích hợp dữ liệu.
- **Vai trò:** Cầu nối giữa dữ liệu vận hành và phân tích, hỗ trợ các bộ phận quản lý từ ban giám đốc đến sản xuất, biến dữ liệu thô thành tri thức cho DSS.
- **Ứng dụng:** Hỗ trợ ra quyết định ở ba cấp độ: tác nghiệp (chi tiết, hàng ngày), quản lý trung gian (tổng hợp, ngắn hạn), chiến lược (lịch sử, dài hạn).

