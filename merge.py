import cv2
import numpy as np

image1 = cv2.imread('merge/CB2045A-5X-A-1.JPG')
image2 = cv2.imread('merge/CB2045A-5X-B-1.JPG')


def merge():
    img1 = np.maximum(image1, image2)
    img2 = cv2.addWeighted(image1, 0.7, image2, 0.3, 0)
    cv2.imshow('1', img1)
    cv2.imshow('2', img2)
    cv2.waitKey(0)


image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
ret, th1 = cv2.threshold(image1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
th2 = cv2.adaptiveThreshold(image1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
kernel = np.ones((5, 5), np.uint8)
th2 = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, kernel)

cv2.imshow('1', th1)
cv2.imshow('2', th2)
cv2.waitKey(0)