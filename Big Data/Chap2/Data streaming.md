### 1. Tổng quan về Hệ thống Luồng Dữ liệu

#### 1.1. Phân loại Hệ thống Thời gian thực

Hệ thống thời gian thực được phân loại dựa trên độ trễ có thể chấp nhận được và mức độ chịu đựng đối với sự chậm trễ. Mỗi loại phù hợp với các ứng dụng khác nhau, từ các hệ thống quan trọng đến tính mạng đến các ứng dụng tiêu dùng.

|   |   |   |   |
|---|---|---|---|
|Phân loại|Ví dụ|Độ trễ đo được|Mức độ chịu đựng chậm trễ|
|**Hard**|Máy tạo nhịp tim, phanh chống bó cứng|Micro giây – mili giây|Không—lỗi hệ thống toàn bộ, có nguy cơ mất mát sinh mạng|
|**Soft**|Hệ thống đặt vé máy bay, báo giá chứng khoán trực tuyến, VoIP (Skype)|Mili giây – giây|Thấp—không gây lỗi hệ thống, không có nguy cơ đến tính mạng|
|**Near**|Video Skype, tự động hóa nhà thông minh|Giây – phút|Cao—không gây lỗi hệ thống, không có nguy cơ đến tính mạng|

#### 1.2. Kiến trúc Luồng Dữ liệu

Một kiến trúc luồng dữ liệu điển hình được cấu thành từ nhiều tầng, mỗi tầng thực hiện một chức năng riêng biệt để xử lý dữ liệu từ nguồn đến ứng dụng.

- **Tầng Thu thập (Collection tier):** Tiếp nhận dữ liệu từ các nguồn khác nhau.
- **Tầng Hàng đợi Tin nhắn (Message queuing tier):** Hoạt động như một bộ đệm, tách biệt tầng thu thập và tầng phân tích. Kafka là một công cụ chính trong tầng này.
- **Tầng Phân tích (Analysis tier):** Xử lý và phân tích dữ liệu luồng. Apache Spark là một ví dụ.
- **Tầng Truy cập Dữ liệu (Data access tier):** Cung cấp dữ liệu đã được phân tích cho các ứng dụng. Tầng này có thể bao gồm kho dữ liệu trong bộ nhớ (in-memory data store) để truy cập nhanh và kho lưu trữ dài hạn (long term store) cho mục đích lưu trữ.

### 2. Tầng Thu thập và Hàng đợi Tin nhắn

#### 2.1. Các Mẫu Thu thập Dữ liệu (Data Ingestion)

Có nhiều mẫu khác nhau để thu thập dữ liệu, tùy thuộc vào yêu cầu của hệ thống.

- **Request/response:** Một client gửi yêu cầu và đợi phản hồi. Các biến thể bao gồm: đồng bộ (Sync RR), bán-bất đồng bộ (Half-async RR), và hoàn toàn bất đồng bộ (Full-async RR).

|Biến thể|Đặc điểm|Ví dụ|
|---|---|---|
|**Sync RR (Synchronous Request/Response)**|Client gửi yêu cầu, **chặn** (blocking) cho đến khi có phản hồi.|Trình duyệt gửi yêu cầu HTTP GET đến server và đợi trả về trang HTML.|
|**Half-async RR (Bán bất đồng bộ)**|Client gửi yêu cầu, có thể xử lý song song, nhưng vẫn **đợi phản hồi** trong thời gian nhất định.|Một ứng dụng gửi yêu cầu tới API và xử lý các tác vụ khác trong khi chờ callback.|
|**Full-async RR (Hoàn toàn bất đồng bộ)**|Client gửi yêu cầu và **không cần đợi phản hồi**; phản hồi được xử lý qua **callback hoặc event**.|Gửi yêu cầu đăng ký dịch vụ qua API; khi hoàn thành, server gửi webhook hoặc email xác nhận.|

- **Publish/subscribe:** Các Publishers gửi tin nhắn đến các Topics mà không cần biết về Subscribers. Subscribers đăng ký các **chủ đề** để nhận tin nhắn.
- **One-way:** Còn được gọi là mẫu "fire and forget". Hệ thống gửi yêu cầu không cần phản hồi và thậm chí không biết liệu yêu cầu có được nhận hay không. Ví dụ: cảm biến môi trường, máy chủ gửi dữ liệu đến hệ thống giám sát.
- **Request/acknowledge:** Client gửi yêu cầu và nhận lại một xác nhận (thường là một mã định danh duy nhất) thay vì dữ liệu đầy đủ. Mã định danh này có thể được sử dụng trong các yêu cầu tiếp theo.
- **Stream:** Dịch vụ trở thành client. Một yêu cầu duy nhất có thể không trả về dữ liệu nào hoặc trả về một luồng dữ liệu liên tục.

#### 2.2. Hệ thống Hàng đợi Tin nhắn

Hệ thống hàng đợi tin nhắn có ba thành phần cốt lõi:

- **Producer:** Gửi tin nhắn đến một broker.
- **Broker:** Đặt tin nhắn vào một hàng đợi.
- **Consumer:** Đọc tin nhắn từ broker.

Mục đích chính của tầng này là **tách biệt producers và consumers**, cho phép chúng hoạt động độc lập. Điều này giúp quản lý **áp lực ngược (backpressure)**—tình huống mà consumer không thể xử lý dữ liệu nhanh bằng tốc độ producer gửi đến—ngăn ngừa mất dữ liệu.

#### 2.3. Ngữ nghĩa Phân phối Tin nhắn (Message Delivery Semantics)

Đây là các đảm bảo về cách tin nhắn được gửi và xử lý.

- **At most once (Tối đa một lần):** Một tin nhắn có thể bị mất nhưng sẽ không bao giờ được đọc lại. Ví dụ: offset được cập nhật ngay khi tin nhắn được lấy về, nếu xử lý sau đó thất bại, tin nhắn sẽ bị mất.
- **At least once (Ít nhất một lần):** Một tin nhắn sẽ không bao giờ bị mất nhưng có thể được đọc lại. Ví dụ: offset được cập nhật sau khi xử lý thành công. Nếu có lỗi, tin nhắn sẽ được đọc lại, có thể dẫn đến xử lý trùng lặp. Đây là tùy chọn được ưu tiên trong nhiều trường hợp.
- **Exactly-once (Chính xác một lần):** Một tin nhắn không bao giờ bị mất và chỉ được xử lý một lần duy nhất. Trong Kafka, điều này chỉ có thể thực hiện được thông qua Streams API. Với các API khác, cần có sự phối hợp giữa producer và consumer để đạt được điều này, ví dụ như lưu trữ metadata về tin nhắn cuối cùng đã đọc.

### 3. Phân tích Chuyên sâu về Apache Kafka

#### 3.1. Giới thiệu và Đặc điểm

Kafka là một dự án mã nguồn mở do LinkedIn tạo ra, hiện được duy trì bởi Confluent. Nó được định nghĩa là một **"hệ thống nhắn tin publish-subscribe được tái cấu trúc như một commit log phân tán"**.

- **Đặc điểm chính:** Nhanh, có khả năng mở rộng, bền bỉ, và phân tán.
- **Độ phổ biến:** Được sử dụng bởi hàng ngàn công ty, bao gồm hơn 60% trong danh sách Fortune 100.
- **Kiến trúc:** Chịu lỗi, có khả năng mở rộng đến hàng trăm broker và xử lý hàng triệu tin nhắn mỗi giây.

#### 3.2. Hiệu năng và Tốc độ

Kafka nổi tiếng về hiệu năng cao, có thể đạt **"tới 2 triệu lượt ghi/giây trên 3 máy tính giá rẻ"**. Tốc độ này đạt được nhờ hai yếu tố chính:

1. **Ghi nhanh (Fast writes):** Mặc dù Kafka lưu trữ tất cả dữ liệu trên đĩa, nhưng hầu hết các thao tác ghi đều được thực hiện vào **bộ đệm trang (page cache)** của hệ điều hành, tức là RAM.
2. **Đọc nhanh (Fast reads):** Việc truyền dữ liệu từ page cache đến một socket mạng rất hiệu quả. Trên Linux, Kafka sử dụng lời gọi hệ thống `sendfile()` để tối ưu hóa quá trình này.

Khi consumer bắt kịp producer, hầu hết dữ liệu được phục vụ hoàn toàn từ bộ đệm mà không cần đọc từ đĩa.

#### 3.3. Các Khái niệm Cốt lõi

|                    |                                                                                                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Thuật ngữ          | Định nghĩa                                                                                                                                                                   |
| **Broker**         | Một máy chủ Kafka. Một cụm Kafka (Kafka cluster) bao gồm một hoặc nhiều broker.                                                                                              |
| **Topic**          | Một danh mục hoặc tên nguồn cấp dữ liệu mà các bản ghi (tin nhắn) được xuất bản vào. Topics được chia thành các partitions.                                                  |
| **Partition**      | Một chuỗi các bản ghi có thứ tự, không thể thay đổi và liên tục được nối thêm vào. Thứ tự chỉ được đảm bảo trong phạm vi một partition.                                      |
| **Offset**         | Một số nguyên tăng dần, là mã định danh duy nhất cho mỗi bản ghi trong một partition.                                                                                        |
| **Replica**        | Một bản sao (backup) của một partition, được lưu trữ trên một broker khác để ngăn ngừa mất dữ liệu. Replicas không bao giờ được đọc hoặc ghi vào.                            |
| **Producer**       | Một ứng dụng client gửi (ghi) dữ liệu vào các topic của Kafka.                                                                                                               |
| **Consumer**       | Một ứng dụng client đọc dữ liệu từ các topic của Kafka.                                                                                                                      |
| **Consumer Group** | Một nhóm các consumer cùng đọc từ một topic. Mỗi consumer trong nhóm sẽ đọc từ một tập hợp các partition riêng biệt, đảm bảo mỗi tin nhắn chỉ được xử lý một lần trong nhóm. |

#### 3.4. Vai trò của ZooKeeper

**Kafka không thể hoạt động nếu không có ZooKeeper.** ZooKeeper là một dịch vụ tập trung để duy trì dữ liệu cấu hình, đặt tên và cung cấp sự đồng bộ hóa mạnh mẽ trong các hệ thống phân tán.

- **Quản lý trạng thái Broker:** Theo dõi các broker đang hoạt động trong cụm.
- **Cấu hình Topic:** Lưu trữ thông tin về các topic, số lượng partition, vị trí của các replica.
- **Bầu chọn Controller:** Chọn một broker làm leader cho một partition khi leader hiện tại bị lỗi.
- **Quản lý thành viên cụm:** Duy trì danh sách các broker đang hoạt động.
- **Danh sách kiểm soát truy cập (ACLs):** Lưu trữ quyền truy cập cho các topic.
- **Quản lý Consumer Offsets:** Theo dõi vị trí (offset) mà mỗi consumer group đã đọc đến trong mỗi partition.

#### 3.5. Chi tiết về Producer và Consumer

- **Producer:**
    - Có thể sử dụng **khóa tin nhắn (message key)**. Tất cả các tin nhắn có cùng khóa sẽ được gửi đến cùng một partition, đảm bảo thứ tự cho một trường dữ liệu cụ thể (ví dụ: `user_id`).
    - Có thể cấu hình mức độ xác nhận (`ack`):
        - `ack=0`: Producer không chờ xác nhận.
        - `ack=1`: Producer chờ xác nhận từ leader của partition.
        - `ack=2`: Producer chờ xác nhận từ cả leader và tất cả các replica.
- **Consumer:**
    - Đọc các bản ghi theo thứ tự trong mỗi partition.
    - Có thể bắt đầu đọc từ bất kỳ offset nào.
    - Nếu số lượng consumer trong một group vượt quá số lượng partition, một số consumer sẽ không nhận được tin nhắn nào.

### 4. Phân tích Dữ liệu Luồng

#### 4.1. So sánh Hệ thống Luồng và DBMS Truyền thống

|   |   |   |
|---|---|---|
|Tiêu chí|DBMS Truyền thống (Hadoop, RDBMS)|Hệ thống Luồng (Spark Streaming, Storm)|
|**Dữ liệu**|Dữ liệu ở trạng thái nghỉ (at rest).|Dữ liệu đang di chuyển (in-flight).|
|**Mô hình truy vấn**|Mô hình **kéo (pull)**. Người dùng thực thi một truy vấn một lần và nhận được câu trả lời.|Mô hình **đẩy (push)**. Truy vấn được đăng ký một lần và được thực thi liên tục khi có dữ liệu mới.|
|**Trạng thái truy vấn**|Nếu hệ thống gặp sự cố, truy vấn sẽ bị quên. Người dùng phải thực thi lại.|Truy vấn liên tục có thể cần tiếp tục từ nơi nó đã dừng lại sau khi hệ thống khôi phục.|

#### 4.2. Các Công cụ Xử lý Luồng Phân tán

- **Kiến trúc chung:** Bao gồm một trình điều khiển ứng dụng (application driver), một trình quản lý luồng (streaming manager) để phân phối công việc và các bộ xử lý luồng (stream processors) nơi công việc thực sự được thực thi.
- **Các công cụ phổ biến:** Apache Spark Streaming, Storm, Flink, và Samza.
- **Apache Spark:**
    - Được coi là nền tảng **de facto** cho tính toán phân tán mục đích chung.
    - Hỗ trợ các ngôn ngữ Java, Scala, Python và R.
    - Bao gồm các module như Spark Streaming, MLlib (học máy) và GraphX (xử lý đồ thị).

### 5. Ưu điểm, Nhược điểm và Ứng dụng của Kafka

#### 5.1. Ưu điểm

- **Thông lượng cao (High-throughput)**
- **Độ trễ thấp (Low latency)**
- **Chịu lỗi (Fault-Tolerant)**
- **Bền bỉ (Durability)**: Dữ liệu được lưu trữ trên đĩa.
- **Khả năng mở rộng (Scalability)**: Kiến trúc phân tán.
- **Đồng thời cao (High concurrency)**
- **Thân thiện với Consumer**: Cho phép consumer đọc lại hoặc bỏ qua dữ liệu.

#### 5.2. Nhược điểm

- **Thiếu công cụ giám sát toàn diện.**
- **Hiệu suất giảm** khi broker và consumer phải nén và giải nén tin nhắn có kích thước lớn.
- **Không hỗ trợ chọn topic theo ký tự đại diện (wildcard).**
- **Hoạt động thiếu linh hoạt** khi số lượng hàng đợi trong một cụm tăng lên.
- **Thiếu một số mô hình nhắn tin** như request/reply hoặc hàng đợi point-to-point.

#### 5.3. Ứng dụng Thực tế

- **Số liệu (Metrics):** Tổng hợp số liệu thống kê từ các ứng dụng phân tán để tạo ra các nguồn cấp dữ liệu hoạt động tập trung.
- **Giải pháp Tổng hợp Log (Log Aggregation):** Thu thập log từ nhiều dịch vụ và cung cấp chúng ở định dạng chuẩn cho nhiều consumer.
- **Xử lý Luồng (Stream Processing):** Các framework như Spark Streaming và Storm đọc dữ liệu từ một topic, xử lý nó và ghi kết quả vào một topic mới.

### 6. Giải pháp Thay thế: ThingsBoard

- ThingsBoard được trình bày như một **giải pháp quy mô nhỏ**.
- Nó tích hợp các chức năng như một **nút thu thập dữ liệu**, hỗ trợ nhiều giao thức, một **công cụ quy tắc (rule engine)** để tiền xử lý (lấy mẫu, lọc, tích hợp) và một hàng đợi tin nhắn.
- Đây là một lựa chọn phù hợp cho các trường hợp không yêu cầu quy mô và sự phức tạp của một hệ thống Kafka và Spark đầy đủ.