import cv2
from PIL import Image

# image = Image.open('../outputs/predict1.png')
image = cv2.imread('../outputs/predict.png')
# print(image.shape)
# for x in range(image.shape[0]):
#     for y in range(image.shape[1]):
#         if image[x][y][0] != 0 or image[x][y][1] != 0 or image[x][y][2] != 0:
#             image[x][y] = 255
# cv2.imshow('1', image)
# cv2.waitKey(0)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


cont, hier = cv2.findContours(gray, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cont, hier = cv2.findContours(image,cv2.CHAIN_APPROX_SIMPLE)
print(len(cont))
print(cont[0][0][0][0])
print(image[cont[0][0][0][0], cont[0][0][0][1]][0])
# cv2.drawContours(image, cont, -1, (0, 0, 255), 3)
# cv2.imshow('1', image)
# cv2.waitKey(0)
