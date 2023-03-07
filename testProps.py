import cv2
import numpy as np
from skimage import measure, morphology
from matplotlib import pyplot as plt


def cnt_area(cnt):
    area = cv2.contourArea(cnt)
    return area


def contoursCv(img):
    contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[1]
    contours.sort(key=cnt_area, reverse=True)  # 轮廓排序
    for i in range(len(contours)):
        cnt = cv2.approxPolyDP(contours[i], 1, True)
        hull = cv2.convexHull(cnt, returnPoints=False)
        print(hull)
        defects = cv2.convexityDefects(cnt, hull)
        print(defects)
        break
    return contours


def watershed():
    img = cv2.imread('re1/CB2045A-5X-A-1.JPG')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    th1 = morphology.remove_small_holes(thresh, area_threshold=2000, connectivity=1) * 255
    th1 = 255 - th1
    th1 = morphology.remove_small_holes(th1, area_threshold=1000, connectivity=1) * 255
    th1 = np.array(th1, dtype=np.uint8)
    return th1


# def regionProps(th1):
#     props = measure.regionprops(th1)
#     for prop in props:
#         label = prop.label
#         print(label)
#         # 质心坐标
#         x = prop.centroid
#         print(x)
#         # 短径
#         y = prop.minor_axis_length
#         # 长径
#         z = prop.major_axis_length
#         print(z)


if __name__ == '__main__':
    th1 = watershed()
    contoursCv(th1)
    # plt.imshow(th1)
    # plt.show()
    # for contour in contours:
    #     rect = cv2.minAreaRect(contour)
    #     print(rect)
