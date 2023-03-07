import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
img = cv2.imread('re1/324-1.jpg')
print(img.shape)
# 灰度化处理图像
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Roberts算子
kernelx = np.array([[-1, 0], [0, 1]], dtype=int)
kernely = np.array([[0, -1], [1, 0]], dtype=int)
x = cv2.filter2D(grayImage, cv2.CV_16S, kernelx)
y = cv2.filter2D(grayImage, cv2.CV_16S, kernely)
# 转uint8
absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)
Roberts = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
print(Roberts)
x = np.mean(Roberts)
print(x)
y = np.var(Roberts)
print(y)
T = x + 4*y
print(T)
cv2.imwrite('result-image/result2.jpg', Roberts*5)
for i in range(Roberts.shape[0]):
    for j in range(Roberts.shape[1]):
        if Roberts[i][j] <= 20 and Roberts[i][j] >= 30:
            Roberts[i][j] = 0
plt.rcParams['font.sans-serif'] = ['SimHei']

# 显示图形
plt.imshow(Roberts*10, 'gray')
plt.show()