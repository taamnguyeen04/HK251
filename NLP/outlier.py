import numpy as np
import pandas as pd
data = pd.read_csv(r'C:\Users\tam\Documents\data\house\train.csv')
col = "GrLivArea"
mean = data[col].mean()
std = data[col].std()

# Tính Z-score cho từng giá trị
data['Z_score'] = (data[col] - mean) / std

# Ngưỡng thường dùng: |Z| > 3
outliers_z = data[np.abs(data['Z_score']) > 3]

print(f"Số lượng outlier (Z-score > 3) trong {col}: {len(outliers_z)}")
print(outliers_z[[col, 'SalePrice', 'Z_score']])
