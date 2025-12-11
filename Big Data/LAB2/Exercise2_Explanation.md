# Exercise 2: Which Genres Are Hot Right Now? 🔥

## 📋 Yêu Cầu Bài Tập

Theo tài liệu PDF, Exercise 2 yêu cầu:
- **Hint**: Static-stream join và per-genre aggregation
- **Join** ratings với movies để lấy genres
- **Write** to console every 5 seconds

## ⚠️ Vấn Đề Với Code Hiện Tại

Code trong `LAB2.ipynb` có một **lỗi nghiêm trọng**:

```python
# ❌ SAI: Movies được đọc dưới dạng STREAM
df_movies = read_and_parse_kafka(spark, "Lab1_movies", movies_schema)
```

**Vấn đề**: 
- Yêu cầu đề bài là **"Static-stream join"** (movies phải là STATIC)
- Nhưng code đang dùng `spark.readStream` → movies thành STREAMING DataFrame
- Điều này vi phạm yêu cầu của bài tập!

## ✅ Giải Pháp Đúng

### 1. Đọc Movies Dưới Dạng STATIC

```python
# ✓ ĐÚNG: Đọc movies dưới dạng STATIC (batch mode)
df_movies_raw = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVERS) \
    .option("subscribe", "Lab1_movies") \
    .option("startingOffsets", "earliest") \
    .option("endingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

df_movies = df_movies_raw.select(
    from_json(col("value").cast("string"), movies_schema).alias("data")
).select("data.*").cache()  # Cache để tối ưu
```

**Điểm quan trọng:**
- Dùng `spark.read` (không phải `readStream`)
- Set `endingOffsets = "latest"` để đọc tất cả dữ liệu có sẵn
- `.cache()` để tối ưu performance vì sẽ join nhiều lần

### 2. Đọc Ratings Dưới Dạng STREAM

```python
# ✓ Ratings là STREAMING với rate limit 100 rows/trigger
df_ratings_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVERS) \
    .option("subscribe", "Lab1_ratings") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", 100) \
    .option("failOnDataLoss", "false") \
    .load()

df_ratings = df_ratings_raw.select(
    from_json(col("value").cast("string"), ratings_schema).alias("data")
).select("data.*") \
    .withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss"))
```

### 3. Static-Stream Join

```python
# Join STREAM ratings với STATIC movies
df_joined = df_ratings.join(df_movies, on="movieId", how="inner")
```

**Lưu ý về Static-Stream Join:**
- Spark cho phép join streaming DataFrame với static DataFrame
- Static DataFrame sẽ được broadcast đến các node (hiệu quả)
- Không cần watermark cho loại join này

### 4. Explode Genres

```python
# Tách "Action|Comedy|Drama" thành nhiều dòng riêng biệt
df_exploded = df_joined.withColumn("genre", explode(split(col("genres"), "\\|")))
```

**Tại sao cần explode?**

Dữ liệu genres có dạng:
```
movieId: 1, genres: "Action|Comedy|Drama"
```

Sau khi explode, mỗi genre trở thành 1 dòng riêng:
```
movieId: 1, genre: "Action"
movieId: 1, genre: "Comedy"
movieId: 1, genre: "Drama"
```

Điều này đảm bảo khi đếm, mỗi genre được tính riêng biệt.

### 5. Per-Genre Aggregation

```python
# Đếm số ratings cho mỗi genre
genre_counts = df_exploded.groupBy("genre").count()

# Sắp xếp để thể loại HOT nhất lên đầu
hot_genres = genre_counts.orderBy(desc("count"))
```

### 6. Write to Console Every 5 Seconds

```python
query_ex2 = hot_genres.writeStream \
    .outputMode("complete") \
    .format("console") \
    .trigger(processingTime="5 seconds") \
    .option("truncate", "false") \
    .option("numRows", 20) \
    .start()
```

**Tại sao dùng "complete" mode?**
- Với aggregation không có watermark, chỉ có thể dùng "complete"
- Mode này xuất toàn bộ bảng kết quả mỗi trigger
- Phù hợp để xem ranking thể loại HOT nhất

## 📊 Kết Quả Mong Đợi

Output sẽ hiển thị mỗi 5 giây dạng:

```
-------------------------------------------
Batch: 1
-------------------------------------------
+------------+-----+
|genre       |count|
+------------+-----+
|Drama       |3420 |
|Comedy      |2891 |
|Action      |2456 |
|Thriller    |1823 |
|Romance     |1567 |
...
+------------+-----+
```

## 🎯 Tổng Kết Điểm Chính

1. **Static-Stream Join**: Movies = STATIC, Ratings = STREAM
2. **Explode Genres**: Tách chuỗi thành nhiều dòng để đếm chính xác
3. **Complete Mode**: Cần thiết cho aggregation không có watermark
4. **Trigger 5s**: Xuất kết quả mỗi 5 giây
5. **Cache Static DF**: Tối ưu performance cho join

## 🚀 Cách Chạy

### Option 1: Chạy file Python
```bash
python Exercise2_Solution.py
```

### Option 2: Copy code vào Jupyter Notebook
- Mở `LAB2.ipynb`
- Thay thế phần Exercise 2 bằng code đã sửa
- Chạy từng cell

## 📝 Checklist Hoàn Thành

- [x] Movies được đọc dưới dạng STATIC (batch read)
- [x] Ratings được đọc dưới dạng STREAM với rate limit 100
- [x] Thực hiện static-stream join
- [x] Explode genres để tách thành nhiều dòng
- [x] Group by genre và count
- [x] Order by count descending
- [x] Write to console mỗi 5 giây
- [x] Output mode = "complete"

## 💡 Tips

1. **Kiểm tra topics**: Đảm bảo topics đúng tên ("Lab1_movies", "Lab1_ratings")
2. **Kafka servers**: Xác nhận địa chỉ Kafka servers đang hoạt động
3. **Cache**: Luôn cache static DataFrame để tối ưu
4. **Debugging**: Dùng `df_movies.printSchema()` để kiểm tra cấu trúc dữ liệu
