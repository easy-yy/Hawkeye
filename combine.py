import cv2
import numpy as np
import time


# 提取RGB，融合图像
def getRGB(img1,img2):
    # img3 = img1.copy()
    # b1, g1, r1 = cv2.split(img1)
    # b2, g2, r2 = cv2.split(img2)
    # b3, g3, r3 = cv2.split(img3)
    # rows, cols = b1.shape
    # for i in range(0, rows):
    #     for j in range(0, cols):
    #         b3[i, j] = max(b1[i, j], b2[i, j])
    #         g3[i, j] = max(g1[i, j], g2[i, j])
    #         r3[i, j] = max(r1[i, j], r2[i, j])
    # merge = cv2.merge([b3, g3, r3])
    # return merge
    return np.maximum(img1, img2)


img1 = cv2.imread("aligned.jpg")
img2 = cv2.imread("re1/BZ282S1006-5X-A-1.JPG")
# t = time.time()
image = getRGB(img2, img1)
# print(time.time() - t)
cv2.imwrite('re1/LX.jpg', image)
