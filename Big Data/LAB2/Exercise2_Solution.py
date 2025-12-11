# ============================================================
# EXERCISE 2: Which genres are hot right now?
# Yêu cầu: Static-stream join và per-genre aggregation
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import from_json, col, to_timestamp, split, explode, desc
import findspark

# Khởi tạo findspark
findspark.init()

# ============================================================
# BƯỚC 1: Khởi tạo SparkSession
# ============================================================
kafka_package = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"

spark = SparkSession.builder \
    .appName("Lab02_Exercise2_HotGenres") \
    .master("local[*]") \
    .config("spark.jars.packages", kafka_package) \
    .config("spark.sql.shuffle.partitions", "20") \
    .getOrCreate()

print("✓ SparkSession đã sẵn sàng!")

# ============================================================
# BƯỚC 2: Định nghĩa Schema
# ============================================================
movies_schema = StructType([
    StructField("movieId", StringType(), True),
    StructField("title", StringType(), True),
    StructField("genres", StringType(), True)
])

ratings_schema = StructType([
    StructField("userId", StringType(), True),
    StructField("movieId", StringType(), True),
    StructField("rating", DoubleType(), True),
    StructField("timestamp", StringType(), True)
])

# ============================================================
# BƯỚC 3: Đọc STATIC Movies DataFrame
# ============================================================
# Quan trọng: Movies phải là STATIC để thực hiện static-stream join
# Đọc TẤT CẢ dữ liệu từ Kafka một lần (batch mode)
KAFKA_SERVERS = "203.205.33.134:29090,203.205.33.134:29091,203.205.33.134:29092"

print("\n1. Đang đọc Movies (STATIC)...")

df_movies_raw = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVERS) \
    .option("subscribe", "Lab1_movies") \
    .option("startingOffsets", "earliest") \
    .option("endingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

# Parse JSON và cache để tối ưu performance
df_movies = df_movies_raw.select(
    from_json(col("value").cast("string"), movies_schema).alias("data")
).select("data.*").cache()

# Trigger action để cache thực sự được thực thi
movies_count = df_movies.count()
print(f"✓ Đã load {movies_count} movies (STATIC)")

# ============================================================
# BƯỚC 4: Đọc STREAMING Ratings DataFrame
# ============================================================
print("\n2. Đang đọc Ratings (STREAMING với rate limit 100 rows)...")

df_ratings_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVERS) \
    .option("subscribe", "Lab1_ratings") \
    .option("startingOffsets", "earliest") \
    .option("maxOffsetsPerTrigger", 100) \
    .option("failOnDataLoss", "false") \
    .load()

# Parse JSON và convert timestamp
df_ratings = df_ratings_raw.select(
    from_json(col("value").cast("string"), ratings_schema).alias("data")
).select("data.*") \
    .withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss"))

print("✓ Ratings stream đã sẵn sàng")

# ============================================================
# BƯỚC 5: Static-Stream Join
# ============================================================
print("\n3. Thực hiện Static-Stream Join...")

# Join ratings (STREAM) với movies (STATIC)
df_joined = df_ratings.join(df_movies, on="movieId", how="inner")

# ============================================================
# BƯỚC 6: Explode Genres
# ============================================================
# Tách chuỗi "Action|Comedy|Drama" thành nhiều dòng
# Ví dụ: "Action|Comedy" → ["Action"], ["Comedy"]
# Điều này đảm bảo mỗi genre được đếm riêng biệt
df_exploded = df_joined.withColumn("genre", explode(split(col("genres"), "\\|")))

# ============================================================
# BƯỚC 7: Per-Genre Aggregation
# ============================================================
# Đếm số lượng ratings cho mỗi genre
genre_counts = df_exploded.groupBy("genre").count()

# Sắp xếp theo count giảm dần để thể loại HOT nhất lên đầu
hot_genres = genre_counts.orderBy(desc("count"))

# ============================================================
# BƯỚC 8: Write to Console Every 5 Seconds
# ============================================================
print("\n4. Khởi động Streaming Query (xuất console mỗi 5 giây)...\n")

query_ex2 = hot_genres.writeStream \
    .outputMode("complete") \
    .format("console") \
    .trigger(processingTime="5 seconds") \
    .option("truncate", "false") \
    .option("numRows", 20) \
    .start()

print("=" * 60)
print("EXERCISE 2: Hot Genres Tracker đã khởi động!")
print("=" * 60)
print("Output sẽ hiển thị mỗi 5 giây")
print("Nhấn Ctrl+C để dừng stream")
print("=" * 60)

# Chờ stream kết thúc (hoặc Ctrl+C)
try:
    query_ex2.awaitTermination()
except KeyboardInterrupt:
    print("\n\n✓ Đã dừng stream thành công!")
    query_ex2.stop()
