import cv2
import numpy as np
from matplotlib import pyplot as plt

path = r"C:\Users\tam\Documents\GitHub\HK251\Computer vision\landscape-photography_1645.jpg"  # thay bằng ảnh của bạn
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

# Làm mờ ảnh (Gaussian blur)
blur = cv2.GaussianBlur(img, (21,21), 0)

# Hệ số A
A = 1.5   # thử các giá trị: 1.0, 1.5, 2.0

# High-boost filtering
high_boost = cv2.addWeighted(img, A, blur, -1, 0)

# Hiển thị
plt.figure(figsize=(15,5))
plt.subplot(1,3,1), plt.imshow(img, cmap='gray'), plt.title("Ảnh gốc")
plt.subplot(1,3,2), plt.imshow(blur, cmap='gray'), plt.title("Ảnh mờ (blur)")
plt.subplot(1,3,3), plt.imshow(high_boost, cmap='gray'), plt.title(f"High-boost A={A}")
plt.show()
