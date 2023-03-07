import cv2
import skimage
from skimage import filters, io, morphology
from matplotlib import pyplot as plt
import numpy as np

# image = cv2.imread('re1/CB2045A-5X-A-1.JPG')
image = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')

# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# f1, f2 = filters.gabor(image, frequency=0.1)

# f1 = filters.laplace(image, ksize=3)
# f1 = filters.prewitt(image)
# f1 = filters.scharr(image)
f1 = filters.sobel(image)
io.imsave('f1.JPG', f1)

f1 = cv2.imread('f1.JPG')
f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
ret, f1 = cv2.threshold(f1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# contours, h = cv2.findContours(f1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# print(contours)
# f1 = cv2.drawContours(image, contours, -1, color=(255, 0, 0))
f1 = f1.astype(np.bool)
f1 = morphology.remove_small_holes(f1, area_threshold=2000, connectivity=1) * 255
f1 = (255 - f1).astype(np.bool)
f1 = morphology.remove_small_holes(f1, area_threshold=1000, connectivity=1) * 255
f1 = np.array(f1, dtype=np.uint8)

plt.figure()
io.imshow(f1)
io.show()
