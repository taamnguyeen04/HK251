import cv2
import numpy as np
from matplotlib import pyplot as plt

path = r"C:\Users\tam\Documents\GitHub\HK251\Computer vision\landscape-photography_1645.jpg"  # thay bằng ảnh của bạn
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

img_blur = cv2.GaussianBlur(img, (3,3), 0)

# 2️⃣ Đạo hàm bậc nhất (Sobel)
fx = cv2.Sobel(img_blur, cv2.CV_64F, 1, 0, ksize=3)
fy = cv2.Sobel(img_blur, cv2.CV_64F, 0, 1, ksize=3)
grad = np.sqrt(fx**2 + fy**2)
grad = cv2.convertScaleAbs(grad)   # scale về 0–255

# 3️⃣ Đạo hàm bậc hai (Laplacian)
lap = cv2.Laplacian(img_blur, cv2.CV_64F, ksize=3)
lap_abs = cv2.convertScaleAbs(lap)

# 4️⃣ Hiển thị 3 ảnh trong 1 figure
plt.figure(figsize=(15,5))

plt.subplot(1,3,1)
plt.imshow(img, cmap='gray')
plt.title("Ảnh gốc")
plt.axis('off')

plt.subplot(1,3,2)
plt.imshow(grad, cmap='gray')
plt.title("Đạo hàm bậc 1 (Sobel Gradient)")
plt.axis('off')

plt.subplot(1,3,3)
plt.imshow(lap_abs, cmap='gray')
plt.title("Đạo hàm bậc 2 (Laplacian)")
plt.axis('off')

plt.tight_layout()
plt.show()
