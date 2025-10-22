import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 19267.91883
# --- 1. Đọc dữ liệu ---
data = pd.read_csv(r"C:/Users/tam/Documents/data/titanic/train.csv")

# --- 2. Phân loại biến ---
numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = data.select_dtypes(include=['object']).columns.tolist()

print("Số biến số:", len(numeric_cols))
print("Số biến dạng text:", len(categorical_cols))

# --- 3. Xử lý giá trị thiếu ---
# Với biến số: thay bằng trung bình
for col in numeric_cols:
    data[col] = data[col].fillna(data[col].mean())

# Với biến phân loại: thay bằng 'None'
for col in categorical_cols:
    data[col] = data[col].fillna('None')

# --- 4. One-Hot Encoding cho biến text ---
data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

print("Kích thước dữ liệu sau khi mã hóa:", data_encoded.shape)

# --- 5. Tính tương quan với SalePrice ---
corr = data_encoded.corr()['Survived'].sort_values(ascending=False)

# --- 6. In ra kết quả ---
print("/nTop 20 biến (bao gồm cả biến mã hóa) tương quan mạnh nhất với Survived:")
print(corr.head(20))

print("/nTop 10 biến tương quan thấp hoặc ngược chiều:")
print(corr.tail(10))

# --- 7. Vẽ biểu đồ top 15 biến mạnh nhất ---
plt.figure(figsize=(10,6))
(corr.drop('Survived') * 100).abs().sort_values(ascending=False).head(15).plot(kind='bar')
plt.title("Mức độ ảnh hưởng (%) của các biến (sau khi mã hóa) đến SalePrice")
plt.ylabel("Mức độ tương quan tuyệt đối (%)")
plt.xlabel("Tên biến")
plt.grid(axis='y')
plt.show()
