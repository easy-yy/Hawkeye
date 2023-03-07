import cv2
from PIL import Image
import numpy as np

image = Image.open('MIOu/123.jpg')
from skimage import morphology

image1 = cv2.imread('MIOu/123.jpg')
# image1 = cv2.imread('MIOu/re.jpg')
pix = image.load()
width = image.size[0]
height = image.size[1]
for x in range(width):
    for y in range(height):
        r, g, b = pix[x, y]
        # if b != 255:
        #     image[x][y] == [255, 255, 255]
        rgb = (r, g, b)
        # print(rgb)
        if r <= 200 and g > 43 and b>  35:
            image1[y][x] = 255
cv2.imwrite('MIOu/re.jpg', image1)
# # cv2.imshow('new', image1)
# # cv2.waitKey()

# hsv = cv2.cvtColor(image1, cv2.COLOR_RGB2HSV)
# H, S, V = cv2.split(HSV)
# red = np.array([200, 0, 0])
# red1 = np.array([255, 0, 0])
# mask = cv2.inRange(HSV, red, red1)
# res = cv2.bitwise_and(image1, image1, mask=mask)


# h, w, c = hsv.shape
# new_img = np.zeros((h, w))
# lower_red1 = np.array([156, 43, 35])
# upper_red1 = np.array([180, 255, 255])
# lower_red2 = np.array([0, 43, 35])
# upper_red2 = np.array([10, 255, 255])
#
#
# mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
#
#
# mask_red = morphology.remove_small_objects(mask_red == 255, 0) * 1
#
# new_img[mask_red == 1] = 255
#
# cv2.imshow('new', new_img)
# cv2.waitKey()