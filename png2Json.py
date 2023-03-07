import numpy as np
import cv2

img = cv2.imread('融合/BZ282S1006-5X-A-1.png')

img_arr = np.asarray(img, dtype=np.double)

r_img = img_arr[:, :, 0].copy()
# g_img = img_arr[:, :, 1].copy()
# b_img = img_arr[:, :, 2].copy()

# img = r_img * 256 * 256 + g_img * 256 + b_img
img = r_img

n = 1
for n in range(2, 23):
    r_img[img != n] = 0
    r_img[img == n] = 255
    # g_img[img == n*256] = 255
    # b_img[img == n] = 255

    # dst_img = np.array([r_img, r_img, r_img], dtype=np.uint8)
    dst_img = np.array(r_img, dtype=np.uint8)
    # dst_img = dst_img.transpose(1, 2, 0)

    # print(dst_img)
    contours, hierarchy = cv2.findContours(dst_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('1', dst_img)
    cv2.waitKey(0)
    # cv2.imwrite('融合/B.png', dst_img)
