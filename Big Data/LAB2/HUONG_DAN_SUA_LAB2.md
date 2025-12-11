# 🔧 Hướng Dẫn Sửa LAB2.ipynb Cho Exercise 2

## ⚠️ Vấn Đề Cần Sửa

Code hiện tại trong `LAB2.ipynb` đang đọc **movies dưới dạng STREAM**, nhưng yêu cầu Exercise 2 là **Static-stream join** (movies phải là STATIC).

## ✅ Cách Sửa Nhanh

### Bước 1: Sửa phần đọc Movies (Exercise 1)

**TÌM đoạn code này:**
```python
print("1. Đang đọc Movies...")
# Topic: Lab1_movies 
df_movies = read_and_parse_kafka(spark, "Lab1_movies", movies_schema)
```

**THAY BẰNG:**
```python
print("1. Đang đọc Movies (STATIC DataFrame)...")

# QUAN TRỌNG: Movies phải là STATIC để thực hiện static-stream join
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
).select("data.*").cache()

movies_count = df_movies.count()
print(f"✓ Đã load {movies_count} movies (STATIC)")
```

### Bước 2: Phần Exercise 2 giữ nguyên

Phần Exercise 2 hiện tại trong notebook đã đúng về cơ bản, chỉ cần đảm bảo `df_movies` là static (sau khi sửa Bước 1).

## 🚀 Hoặc Sử Dụng File Có Sẵn

Tôi đã tạo file **`Exercise2_Solution.py`** có code hoàn chỉnh, bạn có thể:

### Option 1: Chạy trực tiếp file Python
```bash
cd "Big Data/LAB2"
python Exercise2_Solution.py
```

### Option 2: Copy từng cell vào Notebook
- Mở `Exercise2_Solution.py`
- Copy từng section vào các cell mới trong notebook
- Chạy tuần tự

## 📚 Đọc Thêm

Xem file **`Exercise2_Explanation.md`** để hiểu chi tiết:
- Tại sao cần static-stream join
- Cách hoạt động của explode genres
- Giải thích về output mode "complete"
- Kết quả mong đợi

## 🎯 Checklist Hoàn Thành

- [ ] Sửa phần đọc movies thành STATIC (spark.read thay vì spark.readStream)
- [ ] Thêm cache() cho df_movies
- [ ] Verify movies là static bằng: `print(df_movies.isStreaming)` → phải là False
- [ ] Chạy Exercise 2 và kiểm tra output mỗi 5 giây
- [ ] Kết quả hiển thị ranking genres theo count giảm dần

## 💡 Kiểm Tra Nhanh

Sau khi sửa, chạy dòng này để verify:
```python
print(f"df_movies is streaming: {df_movies.isStreaming}")  # Phải là False
print(f"df_ratings is streaming: {df_ratings.isStreaming}")  # Phải là True
```

---
**Lưu ý:** Nếu gặp khó khăn, hãy sử dụng file `Exercise2_Solution.py` đã được test kỹ!
