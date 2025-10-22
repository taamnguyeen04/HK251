import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import correlate2d

def apply_correlation(image_path, Hcorr, title="Filtered"):
    """Áp dụng phép tương quan giữa ảnh xám và kernel Hcorr(i,j)."""
    print(Hcorr)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = img.astype(np.float32) / 255.0

    result = correlate2d(img, Hcorr, mode='same', boundary='symm')

    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.imshow(img, cmap='gray')
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.imshow(result, cmap='gray')
    plt.title(title)
    plt.axis("off")
    plt.show()

    return result

# ==== Một số ma trận Hcorr(i,j) phổ biến ====

# 1. Mean filter 5x5 (làm mờ)
H_mean = np.ones((16,16), dtype=np.float32) / 25.0

# 2. Sobel edge detector theo trục X và Y
H_sobel_x = np.array([[1,0,-1],
                      [5,0,-5],
                      [1,0,-1]], dtype=np.float32)

H_sobel_y = np.array([[1, 5, 1],
                      [0, 0, 0],
                      [-1,-5,-1]], dtype=np.float32)

# 3. Gaussian 3x3 (làm mượt nhẹ)
H_gaussian = np.array([[1,2,1],
                       [2,4,2],
                       [1,2,1]], dtype=np.float32) / 16.0

# 4. Shift filter (dịch 1 pixel sang phải)
H_shift = np.zeros((300,300), dtype=np.float32)
H_shift[1,2] = 10.0  # pixel giữa hàng 2, cột 3

# === Ví dụ chạy thử ===
if __name__ == "__main__":
    path = r"C:\Users\tam\Documents\GitHub\HK251\Computer vision\landscape-photography_1645.jpg"  # thay bằng ảnh của bạn
    # apply_correlation(path, H_mean, "Mean blur 5x5")
    # apply_correlation(path, H_sobel_x, "Sobel X")
    # apply_correlation(path, H_sobel_y, "Sobel Y")
    # apply_correlation(path, H_gaussian, "Gaussian blur")
    apply_correlation(path, H_shift, "Shift right")
