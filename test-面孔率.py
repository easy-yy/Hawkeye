import cv2
import numpy as np
from collections import Counter
from matplotlib import pyplot as plt
from skimage import io, morphology
from numpy import mask_indices

image1 = cv2.imread('re1/CB2045A-5X-A-1.JPG')
# image1 = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')
# image1 = cv2.imread('re1/test22.JPG')

# image2 = io.imread('re1/CB2045A-5X-A-1.JPG')
# image2 = io.imread('re1/BZ282S1006-5X-A-1.JPG')
# image2 = io.imread('re1/test22.JPG')



# # 计算面孔率
# def getColor1():
#     # 获取蓝色的颜色值范围
#     lower_blue = np.array([100, 43, 46])
#     upper_blue = np.array([124, 255, 255])
#     list = []
#     list.append(lower_blue)
#     list.append(upper_blue)
#     dict = {'blue': list}
#     return dict
#
#
# def getColor(img):
#     # 采取HSV方式获取
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     # maxsum = -100
#     # color = None
#     color_dict = getColor1()
#     for d in color_dict:
#         # 将超出范围的变为0，变成黑色部分
#         mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
#
#         # 阈值处理，变成只有黑白的图，返回ret,thersh利用返回的thersh
#         binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
#         th1 = morphology.remove_small_holes(binary, area_threshold=1000000, connectivity=1) * 255
#
#         cv2.imwrite(d + '.jpg', th1)
#         # th1 = 255 - th1
#         # th1 = morphology.remove_small_holes(th1, area_threshold=2000, connectivity=1) * 255
#         binary = np.array(th1, dtype=np.uint8)
#         # binary = cv2.dilate(binary, None, iterations=2)
#         # 要读取黑白的图,python2只返回两个值
#         cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         sum = 0
#         for c in cnts:
#             sum += cv2.contourArea(c)
#         # if sum > maxsum:
#         # maxsum = sum
#         # color = d
#         print('image', '该图像中蓝色区域比例是：', sum / binary.size)
#         # return (sum / binary.size)
#
# getColor(image1)
"""
# 提取图中的红色部分
"""
hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
low_hsv = np.array([98, 43, 46])
high_hsv = np.array([124, 255, 255])
mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)

# 阈值处理，变成只有黑白的图，返回ret,thersh利用返回的thersh
binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
# 要读取黑白的图,python2只返回两个值
print(Counter(binary.flatten()))
print(Counter(binary.flatten())[255])
print(Counter(binary.flatten())[0])
a = Counter(binary.flatten())[255]
b = a + Counter(binary.flatten())[0]
x2 = a / b
print(x2)

cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
sum = 0
for c in cnts:
    sum += cv2.contourArea(c)
# if sum > maxsum:
# maxsum = sum
# color = d
x = sum / binary.size
print('image', '该图像中蓝色区域比例是：', x)
x1 = '%.3f%%' % (x * 100)
print(x1)

cv2.imshow('1', binary)
cv2.waitKey(0)
# return (sum / binary.size)


# # r = image2[:, :, 0] < 3
# # b = image2[:, :, 2] > 200
#
# r = image2.reshape(-1, 3)[:, 0] < 3
#
# pixel_count1 = ((image2.reshape(-1, 3)[:, 0] < 3) and (image2.reshape(-1, 3)[:, 2] > 200)).all()
# # pixel_count2 = (image2.reshape(-1, 3)[:, 0] < 50).sum()
# # pixel_count3 = (image2.reshape(-1, 3)[:, 0] < 70).sum()
# # pixel_count1 = len(image2[r, b])
# # and image2[b]).all()
# # pixel_count3 = (image2.reshape(-1, 3)[:, 0] < 70).sum()
#
# # pixel_count = pixel_count1 + pixel_count3 - pixel_count2
# pixel_count = pixel_count1
# print(pixel_count)
# pixels_count = image2.shape[0] * image2.shape[1]
# print(image2.shape)
# print(pixels_count)
#
# m_ratio = pixel_count/pixels_count
# print(m_ratio)
# # cv2.imshow('1',image2)
# # cv2.waitKey()
# plt.imshow(image2)
# plt.show()
# # print(image)