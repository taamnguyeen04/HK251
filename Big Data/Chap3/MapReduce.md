## 1. Mô hình Lập trình MapReduce

MapReduce là một mô hình lập trình, một khung thực thi và một triển khai cụ thể được thiết kế để xử lý và tạo ra các tập dữ liệu lớn một cách **song song, phân tán**.

### 1.1. Khái niệm Cốt lõi: Tách biệt "Cái gì" và "Như thế nào"

Điểm mạnh chính của MapReduce nằm ở mức độ trừu tượng mà nó cung cấp. Nó cho phép các nhà phát triển tập trung vào logic tính toán cần thực hiện mà không cần phải quản lý các chi tiết cấp thấp của việc thực thi phân tán.

- **"Cái gì":** Lập trình viên chỉ định phép tính cần thực hiện thông qua hai hàm chính là `map` và `reduce`.
- **"Như thế nào":** Khung thực thi (runtime) tự động xử lý mọi thứ khác, bao gồm lập lịch tác vụ, phân phối dữ liệu, đồng bộ hóa và xử lý lỗi. Điều này giúp loại bỏ các vấn đề phức tạp như điều kiện tranh đua (race conditions) và tranh chấp khóa (lock contention).

### 1.2. Các Hàm Chính

Lập trình viên xác định các hàm sau để định nghĩa một công việc MapReduce:

|          |                                          |                                                                                                                                                                                                                                |
| -------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Hàm      | Chữ ký                                   | Mô tả                                                                                                                                                                                                                          |
| `map`    | `map (k1, v1) → list(<k2, v2>)`          | Xử lý một cặp khóa/giá trị đầu vào (`k1`, `v1`) và tạo ra một danh sách các cặp khóa/giá trị trung gian (`k2`, `v2`).                                                                                                          |
| `reduce` | `reduce (k2, list(v2)) → list(<k3, v3>)` | Xử lý một khóa `k2` và một danh sách tất cả các giá trị trung gian `v2` được liên kết với khóa đó, sau đó tạo ra danh sách các cặp khóa/giá trị đầu ra. Tất cả các giá trị có cùng khóa `k2` sẽ được gửi đến cùng một reducer. |
|          |                                          |                                                                                                                                                                                                                                |

Ngoài ra, hai hàm tối ưu hóa tùy chọn thường được sử dụng:

|             |                                                 |                                                                                                                                                                              |
| ----------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hàm         | Chữ ký                                          | Mô tả                                                                                                                                                                        |
| `partition` | `partition (k2, num_partitions) → partition_id` | Xác định reducer nào sẽ nhận cặp khóa/giá trị trung gian. Thường là một hàm băm đơn giản (`hash(k2) mod n`) để phân chia không gian khóa cho các hoạt động reduce song song. |
| `combine`   | `combine (k2, v2) → <k2, v2>`                   | Thực hiện tổng hợp cục bộ trên các đầu ra của mapper trước khi chúng được gửi qua mạng. Chúng hoạt động như các "mini-reducers" để giảm lưu lượng mạng.                      |

### 1.3. Ví dụ Tương tự: Đếm Tiền Xu

Một cách tương tự trong thế giới thực để hiểu MapReduce là quá trình đếm một lượng lớn tiền xu hỗn hợp:

- **Mapper:** Phân loại tiền xu theo mệnh giá của chúng (ví dụ: nhóm tất cả đồng 1 xu, 5 xu, 10 xu lại với nhau).
- **Reducer:** Đếm số lượng tiền xu trong mỗi nhóm mệnh giá một cách song song.

## 2. Khung Thực thi MapReduce ("Runtime")

Khung thực thi, hay "runtime", là nền tảng quản lý toàn bộ vòng đời của một công việc MapReduce trên một hệ thống tệp phân tán.

### 2.1. Các Trách nhiệm Chính

- **Lập lịch (Scheduling):** Phân công các worker cho các tác vụ map và reduce.
- **Phân phối Dữ liệu (Data Distribution):** Di chuyển các quy trình đến gần dữ liệu để giảm thiểu chi phí truyền dữ liệu qua mạng.
- **Đồng bộ hóa (Synchronization):** Thu thập, sắp xếp và xáo trộn (shuffle) dữ liệu trung gian từ các mapper để chuẩn bị cho các reducer.
- **Xử lý Lỗi và Sự cố (Errors and Faults):** Phát hiện các worker bị lỗi và khởi động lại các tác vụ thất bại.

### 2.2. Luồng Thực thi và Đồng bộ hóa

- Có một rào cản (barrier) giữa giai đoạn map và reduce. Tuy nhiên, dữ liệu trung gian có thể được sao chép đến các reducer ngay khi các mapper hoàn thành.
- Các khóa (keys) đến mỗi reducer theo thứ tự được sắp xếp. Không có thứ tự bắt buộc nào được áp đặt trên các reducer khác nhau.
- Lập trình viên có quyền kiểm soát hạn chế đối với luồng dữ liệu và thực thi. Họ không biết mapper và reducer chạy ở đâu, khi nào chúng bắt đầu hoặc kết thúc, hoặc chúng đang xử lý đầu vào hoặc khóa trung gian cụ thể nào.

## 3. Apache Hadoop

Hadoop là một hệ thống phân tán chịu lỗi, có khả năng mở rộng dành cho Dữ liệu Lớn, và là triển khai mã nguồn mở phổ biến nhất của mô hình MapReduce.

### 3.1. Nguồn gốc và Lịch sử

Hadoop được lấy cảm hứng từ các hệ thống được thiết kế tại Google (Google File System và MapReduce).

- **Tháng 12/2004:** Google công bố bài báo về GFS.
- **Tháng 2/2006:** Hadoop trở thành một dự án con của Lucene.
- **Tháng 4/2007:** Yahoo! chạy Hadoop trên một cụm 1000 nút.
- **Tháng 1/2008:** Hadoop trở thành một Dự án Cấp cao của Apache.
- **Năm 2010:** Facebook tuyên bố sở hữu cụm Hadoop lớn nhất thế giới với 21 PB dung lượng lưu trữ, sau đó tăng lên 30 PB vào năm 2011.

Hadoop đã trở thành nền tảng xử lý dữ liệu lớn de facto, được sử dụng rộng rãi bởi các công ty như Yahoo, Facebook, Twitter, LinkedIn và Netflix.

### 3.2. Động lực cho Dữ liệu Lớn: Ví dụ của Google

Nhu cầu về các hệ thống như Hadoop được thúc đẩy bởi khối lượng dữ liệu khổng lồ.

- **Bài toán:** Phân tích 10 tỷ trang web.
- **Kích thước bộ sưu tập:** 10 tỷ trang × 20KB/trang = 200TB.
- **Thời gian đọc:**
    - Với ổ cứng HDD (150MB/giây): hơn 15 ngày.
    - Với ổ cứng SSD (550MB/giây): hơn 4 ngày.
- **Kết luận:** Kiến trúc một nút đơn là không đủ cho các tác vụ như vậy.

### 3.3. So sánh Hadoop và HPC

|   |   |   |
|---|---|---|
|Đặc điểm|Hadoop|High-Performance Computing (HPC)|
|**Mục đích thiết kế**|Khối lượng công việc chuyên sâu về dữ liệu (Data intensive).|Các tác vụ chuyên sâu về CPU (CPU intensive).|
|**Đặc điểm tác vụ**|Thường không yêu cầu tính toán CPU cao.|Hiệu năng được đo bằng FLOPS.|
|**Kích thước dữ liệu**|Xử lý các tập dữ liệu rất lớn.|Thường xử lý các tập dữ liệu "nhỏ".|

## 4. Hệ thống Tệp Phân tán Hadoop (HDFS)

HDFS là thành phần lưu trữ chính cho các ứng dụng Hadoop. Nó là một hệ thống tệp phân tán được thiết kế để chịu lỗi, có khả năng mở rộng và dễ dàng mở rộng.

### 4.1. Kiến trúc HDFS

HDFS có hai loại máy chính:

- **NameNode:** Là trung tâm của hệ thống tệp, duy trì và quản lý siêu dữ liệu của hệ thống tệp (ví dụ: khối nào tạo thành một tệp, các khối đó được lưu trữ trên DataNode nào).
- **DataNode:** Nơi HDFS lưu trữ dữ liệu thực tế. Thường có rất nhiều DataNode trong một cụm.

### 4.2. Tổ chức Dữ liệu và Sao chép

- Mỗi tệp được ghi vào HDFS được chia thành các khối dữ liệu (data blocks).
- Mỗi khối được lưu trữ trên một hoặc nhiều nút. Mỗi bản sao của một khối được gọi là một **bản sao (replica)**.
- **Chính sách đặt khối:**
    1. Bản sao đầu tiên được đặt trên nút cục bộ.
    2. Bản sao thứ hai được đặt trong một rack khác.
    3. Bản sao thứ ba được đặt trong cùng rack với bản sao thứ hai.

### 4.3. Các Tính năng Chính

- **Chịu lỗi (Failure tolerant):** Dữ liệu được sao chép trên nhiều DataNode (mặc định là 3 bản sao) để bảo vệ khỏi lỗi máy.
- **Khả năng mở rộng (Scalability):** Việc truyền dữ liệu diễn ra trực tiếp với các DataNode, do đó dung lượng đọc/ghi tăng lên cùng với số lượng DataNode.
- **Không gian (Space):** Để thêm dung lượng đĩa, chỉ cần thêm DataNode và cân bằng lại.
- **Tiêu chuẩn công nghiệp:** Các ứng dụng phân tán khác như HBase được xây dựng trên HDFS.

**Lưu ý:** HDFS được thiết kế để xử lý các tập dữ liệu lớn với mẫu truy cập ghi một lần, đọc nhiều lần (write-once-read-many), không phù hợp cho truy cập có độ trễ thấp.

## 5. Thiết kế Thuật toán với MapReduce

Phần này minh họa cách biểu diễn các thuật toán khác nhau bằng mô hình MapReduce.

### 5.1. Ví dụ Kinh điển: Đếm từ (Word Count)

Đây là ví dụ "Hello, World!" của MapReduce.

- **Input:** Một văn bản.
- **Map:** Đối với mỗi từ, xuất ra một cặp `(từ, 1)`.
- **Shuffle/Sort:** Nhóm tất cả các cặp có cùng khóa (từ).
- **Reduce:** Đối với mỗi từ, tính tổng các số 1 để có được tổng số lần xuất hiện.
- **Output:** Một danh sách các cặp `(từ, tổng số lần xuất hiện)`.

### 5.2. Tối ưu hóa với Combiner và "In-Mapper Combining"

- **Combiner:** Một combiner có thể được sử dụng để thực hiện tổng hợp cục bộ trên mỗi mapper, giảm đáng kể lưu lượng mạng. Đối với Word Count, combiner sẽ tính tổng số lần xuất hiện của các từ trên một mapper trước khi gửi kết quả đến reducer.
- **"In-mapper combining":** Một kỹ thuật tối ưu hóa hơn nữa, trong đó chức năng của combiner được tích hợp vào mapper bằng cách duy trì trạng thái qua nhiều lần gọi hàm `map`. Điều này nhanh hơn nhưng đòi hỏi quản lý bộ nhớ một cách tường minh.

### 5.3. Các Hàm Phân phối và Không Phân phối

Khả năng sử dụng combiner phụ thuộc vào bản chất của phép toán tổng hợp.

- **Các hàm phân phối (Distributive):** Có thể sử dụng Reducer làm Combiner. Ví dụ: `Min()`, `Max()`, `Sum()`, `Count()`, `TopK()`.
- **Các hàm không phân phối (Non-distributive):** Không thể sử dụng Reducer làm Combiner. Ví dụ: `Mean()`, `Median()`, `Rank()`.

Để tính trung bình (Mean), không thể chỉ đơn giản tính trung bình của các giá trị trung bình cục bộ. Thay vào đó, mapper phải xuất ra một cặp `(năm, <tổng_nhiệt_độ, số_lượng_bản_ghi>)`, và reducer sẽ tính tổng cuối cùng và chia để có được giá trị trung bình chính xác.

### 5.4. Các Bài toán Ứng dụng

|   |   |   |
|---|---|---|
|Bài toán|Hàm Map|Hàm Reduce|
|**Sắp xếp/Top K từ**|Thực hiện Word Count, sau đó chạy vòng MapReduce thứ hai, hoán đổi khóa và giá trị (số lần xuất hiện, từ) để tận dụng khả năng sắp xếp của giai đoạn shuffle.|(Tùy thuộc vào giai đoạn)|
|**Phân phối Độ dài Từ**|`Emit(length(w), w)`|`Emit(key, size_of(values))`|
|**Lập chỉ mục & PageRank**|`Emit(word, <page_id, page_rank>)`|`Emit(key, sort(values, page_rank))`|
|**Tìm Bạn chung**|Đối với mỗi người, `Emit(<person_id, friend_id>, friend_list)`|`Emit(key, intersection(v1, v2))`|

## 6. Các Triển khai MapReduce

MapReduce có thể đề cập đến mô hình lập trình, khung thực thi, hoặc một triển khai cụ thể.

- **Google:** Triển khai độc quyền bằng C++, với các binding cho Java và Python.
- **Hadoop:** Triển khai mã nguồn mở bằng Java, do Yahoo dẫn đầu và hiện là một dự án của Apache.
- **Các triển khai nghiên cứu:** Nhiều triển khai tùy chỉnh cho các kiến trúc cụ thể như GPU, bộ xử lý Cell, v.v.