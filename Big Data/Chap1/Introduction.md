## 1. Định nghĩa Dữ liệu lớn (Big Data)

Dữ liệu lớn được xác định thông qua hai định nghĩa chính, nhấn mạnh vào giới hạn của các công nghệ truyền thống và sự cần thiết của các kiến trúc mới:

- "Dữ liệu quá lớn và phức tạp để có thể được xử lý hiệu quả bởi các công nghệ cơ sở dữ liệu tiêu chuẩn hiện có ở hầu hết các tổ chức."
- "Dữ liệu có quy mô, sự đa dạng và độ phức tạp đòi hỏi các kiến trúc, kỹ thuật, thuật toán và phương pháp phân tích mới để quản lý và trích xuất giá trị cũng như kiến thức ẩn giấu từ nó."

## 2. Các Đặc Trưng Cốt Lõi của Dữ liệu lớn

Các đặc tính của Dữ liệu lớn thường được tóm tắt qua mô hình 4V hoặc 5V.

### 2.1. Volume (Khối lượng)

Khối lượng đề cập đến quy mô khổng lồ của dữ liệu được tạo ra và thu thập từ nhiều nguồn khác nhau.

- **Dự án khoa học:**
    - Máy gia tốc hạt lớn (LHC) của CERN tạo ra 15 petabyte (PB) dữ liệu mỗi năm.
    - Dự án Earthscope, theo dõi sự tiến hóa địa chất của Bắc Mỹ, tích lũy 67 terabyte (TB) dữ liệu.
- **Internet và Mạng xã hội:**
    - Hơn 12 TB dữ liệu tweet được tạo ra mỗi ngày.
    - Hơn 25 TB dữ liệu log được tạo ra mỗi ngày.
    - Hơn 2 tỷ người dùng web tính đến cuối năm 2011.
- **Thiết bị và Cảm biến (IoT):**
    - 30 tỷ thẻ RFID vào năm 2024 (so với 1.3 tỷ vào năm 2005).
    - 4.6 tỷ điện thoại có camera trên toàn thế giới.
    - Hàng trăm triệu thiết bị hỗ trợ GPS được bán ra hàng năm.
    - 76 triệu đồng hồ thông minh vào năm 2009, dự kiến đạt 200 triệu vào năm 2014.

### 2.2. Variety (Tính đa dạng)

Tính đa dạng đề cập đến các định dạng, loại hình và cấu trúc khác nhau của dữ liệu. Một ứng dụng duy nhất có thể tạo ra nhiều loại dữ liệu không đồng nhất.

- **Các loại dữ liệu:** Dữ liệu số, hình ảnh, âm thanh, video, văn bản, chuỗi thời gian.
- **Các cấu trúc dữ liệu:**
    - Dữ liệu quan hệ (Bảng/Giao dịch).
    - Dữ liệu văn bản (Web).
    - Dữ liệu bán cấu trúc (XML).
    - Dữ liệu đồ thị (Mạng xã hội, Web ngữ nghĩa).

Để trích xuất kiến thức, tất cả các loại dữ liệu này cần được liên kết với nhau. Một ví dụ điển hình là việc xây dựng **"Góc nhìn Toàn diện về Khách hàng" (Single Customer View)**, là một "sự biểu diễn tổng hợp, nhất quán và toàn diện về dữ liệu mà một tổ chức biết về khách hàng của mình" từ các nguồn như mạng xã hội, lịch sử mua hàng, tài chính, giải trí.

### 2.3. Velocity (Tốc độ)

Tốc độ đề cập đến việc dữ liệu được tạo ra và cần được xử lý một cách nhanh chóng. Việc ra quyết định muộn có thể dẫn đến bỏ lỡ các cơ hội kinh doanh.

- **Ví dụ ứng dụng:**
    - **Khuyến mãi điện tử (E-Promotions):** Gửi các chương trình khuyến mãi ngay lập tức dựa trên vị trí hiện tại, lịch sử mua hàng và sở thích của khách hàng.
    - **Giám sát sức khỏe:** Các cảm biến theo dõi hoạt động và chỉ số cơ thể, đòi hỏi phản ứng ngay lập tức khi có các phép đo bất thường.

Điểm mấu chốt là: "Sự tiến bộ và đổi mới không còn bị cản trở bởi khả năng thu thập dữ liệu, mà bởi khả năng quản lý, phân tích, tóm tắt, trực quan hóa và khám phá kiến thức từ dữ liệu thu thập được một cách kịp thời và có khả năng mở rộng."

### 2.4. Veracity (Tính xác thực)

Đặc tính này đề cập đến chất lượng và độ tin cậy của dữ liệu.

### 2.5. Value (Giá trị)

Đây là mục tiêu cuối cùng của việc khai thác Dữ liệu lớn: biến dữ liệu thành lợi thế kinh doanh. Quá trình này được minh họa qua ví dụ về doanh số bán kẹo mút sụt giảm:

|   |   |
|---|---|
|Giai đoạn|Mô tả|
|**Vấn đề**|Doanh số bán kẹo mút đang giảm.|
|**Dữ liệu**|Tất cả dữ liệu bán hàng theo khách hàng, khu vực, thời gian, v.v.|
|**Thông tin**|Kẹo mút được mua bởi những người trên 25 tuổi (nhưng được ăn bởi những người dưới 10 tuổi).|
|**Kiến thức**|Các bà mẹ tin rằng kẹo mút gây sâu răng.|
|**Giá trị**|Để các nha sĩ quảng cáo cho sản phẩm kẹo mút của bạn.|

## 3. Ba Góc nhìn về Dữ liệu lớn

Dữ liệu lớn có thể được tiếp cận từ ba góc độ khác nhau: triết học, kinh doanh và kỹ thuật.

### 3.1. Góc nhìn Triết học: Một Mô thức Khoa học Mới

Dữ liệu lớn đại diện cho một sự thay đổi từ khoa học truyền thống sang một phương pháp tiếp cận mới, thường được gọi là "Mô thức thứ 4" hay Khoa học Dữ liệu.

- **Khoa học truyền thống (Dựa trên logic/trí tuệ):** Hiểu vấn đề -> Xây dựng mô hình/thuật toán -> Trả lời câu hỏi từ mô hình đã triển khai.
- **Khoa học mới (Dựa trên thống kê/kinh nghiệm):** Thu thập dữ liệu -> Trả lời câu hỏi từ dữ liệu (người khác đã làm gì?).

**Lớn hơn có đồng nghĩa với thông minh hơn không?**

- **Có:** Vì dữ liệu lớn hơn giúp chịu lỗi tốt hơn, khám phá được các trường hợp hiếm (long tail) và các trường hợp góc (corner cases), và giúp học máy hoạt động hiệu quả hơn nhiều.
- **Nhưng:** Nhiều dữ liệu hơn cũng có thể mang lại nhiều lỗi hơn (ví dụ, không đồng nhất về ngữ nghĩa). Với đủ dữ liệu, người ta có thể chứng minh bất cứ điều gì, và vẫn cần con người để đặt ra những câu hỏi đúng đắn.

### 3.2. Góc nhìn Kinh doanh: Dữ liệu như một Mô hình Kinh doanh

Dưới góc độ kinh doanh, Dữ liệu lớn là một mô hình kinh doanh mới.

- **Người dùng trả tiền bằng dữ liệu:**
    - **Ví dụ:** Facebook, Google, Twitter. Người dùng sử dụng dịch vụ và cung cấp dữ liệu. Google bán dữ liệu của bạn cho các nhà quảng cáo.
    - **Ví dụ:** Amazon. Người dùng vừa trả tiền cho dịch vụ, vừa cung cấp dữ liệu. Amazon bán dữ liệu và sử dụng nó để cải thiện dịch vụ.
- **Tương tự "Ngân hàng dữ liệu" (Databank):**
    - Giống như một ngân hàng giữ tiền của bạn và cho vay để sinh lời, một "ngân hàng dữ liệu" giữ dữ liệu của bạn an toàn và đưa dữ liệu đó vào hoạt động để tạo ra lợi ích hoặc dịch vụ tốt hơn.

### 3.3. Góc nhìn Kỹ thuật: Thu thập Trước, Phân tích Sau

Cách tiếp cận kỹ thuật của Dữ liệu lớn có sự khác biệt rất lớn so với các hệ thống thông tin truyền thống.

- **Thu thập tất cả dữ liệu:** Phương pháp này cho rằng việc giữ lại tất cả dữ liệu rẻ hơn việc quyết định dữ liệu nào nên giữ. Dữ liệu càng nhiều càng tốt để có ý nghĩa thống kê.
- **Quyết định phân tích sau:** Các thí nghiệm trên dữ liệu chỉ được thực hiện khi có câu hỏi phát sinh.
- **Khác biệt với truyền thống:** Các hệ thống truyền thống (ví dụ, mô hình thác nước trong kỹ thuật phần mềm) yêu cầu phải thiết kế trước để xác định dữ liệu nào cần giữ và tại sao.

## 4. Chuỗi Giá trị Dữ liệu lớn

Quá trình khai thác Dữ liệu lớn bao gồm bốn giai đoạn chính:

1. **Generation (Tạo ra):**
    - **Ghi lại thụ động (Passive recording):** Dữ liệu có cấu trúc điển hình (giao dịch ngân hàng, hồ sơ mua sắm).
    - **Tạo ra chủ động (Active generation):** Dữ liệu bán cấu trúc hoặc phi cấu trúc (nội dung do người dùng tạo trên mạng xã hội).
    - **Sản xuất tự động (Automatic production):** Dữ liệu nhận biết vị trí, phụ thuộc vào ngữ cảnh từ các thiết bị cảm biến kết nối Internet.
2. **Acquisition (Thu thập):**
    - **Tập hợp (Collection):** Dựa trên cơ chế kéo (pull-based, ví dụ: web crawler) hoặc đẩy (push-based, ví dụ: giám sát video, luồng nhấp chuột).
    - **Truyền tải (Transmission):** Chuyển đến trung tâm dữ liệu qua các liên kết dung lượng cao.
    - **Tiền xử lý (Preprocessing):** Tích hợp, làm sạch, loại bỏ dư thừa.
3. **Storage (Lưu trữ):**
    - **Hạ tầng lưu trữ (Storage infrastructure):** Công nghệ lưu trữ (HDD, SSD), kiến trúc mạng (DAS, NAS, SAN).
    - **Quản lý dữ liệu (Data management):** Hệ thống tệp (HDFS), kho lưu trữ khóa-giá trị (Memcached), cơ sở dữ liệu hướng cột (Cassandra), cơ sở dữ liệu tài liệu (MongoDB).
    - **Mô hình lập trình (Programming models):** MapReduce, xử lý luồng, xử lý đồ thị.
4. **Analysis (Phân tích):**
    - **Mục tiêu (Objectives):** Phân tích mô tả, phân tích dự đoán, phân tích đề xuất.
    - **Phương pháp (Methods):** Phân tích thống kê, khai phá dữ liệu, khai phá văn bản, khai phá dữ liệu mạng và đồ thị (phân cụm, phân loại, hồi quy).

## 5. Thách thức và Giải pháp Kỹ thuật Cốt lõi

### 5.1. Nút thắt cổ chai

Vấn đề cơ bản trong việc xử lý dữ liệu quy mô lớn là sự chênh lệch tốc độ giữa các thành phần phần cứng.

- Bộ xử lý (Processors) xử lý dữ liệu.
- Ổ cứng (Hard drives) lưu trữ dữ liệu.
- Nút thắt cổ chai nằm ở khâu **truyền dữ liệu từ đĩa cứng đến bộ xử lý**.

### 5.2. Giải pháp

Giải pháp nền tảng là đảo ngược quy trình truyền thống: **chuyển sức mạnh xử lý đến nơi có dữ liệu.**

- **Sử dụng nhiều đĩa phân tán:** Mỗi đĩa chứa một phần của bộ dữ liệu lớn.
- **Xử lý song song:** Xử lý đồng thời các phần tệp khác nhau từ các đĩa khác nhau.