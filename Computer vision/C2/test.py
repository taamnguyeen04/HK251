import cv2
import matplotlib.pyplot as plt

path = r"C:\Users\tam\Documents\GitHub\HK251\Computer vision\landscape-photography_1645.jpg"  # thay bằng ảnh của bạn

img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)  # Sobel X
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)  # Sobel Y

plt.figure(figsize=(12,4))
plt.subplot(1,3,1); plt.imshow(img, cmap='gray'); plt.title("Original")
plt.subplot(1,3,2); plt.imshow(sobelx, cmap='gray'); plt.title("Sobel X")
plt.subplot(1,3,3); plt.imshow(sobely, cmap='gray'); plt.title("Sobel Y")
plt.show()
