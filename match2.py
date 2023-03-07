import cv2
# import Utility
import numpy as np


# 这里使用的Python 3
def sift_kp(image):
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d_SIFT.create()
    kp, des = sift.detectAndCompute(image, None)
    # kp, des = sift.detectAndCompute(gray_image, None)
    # kp_image = cv2.drawKeypoints(gray_image, kp, None)
    # return kp_image, kp, des
    return kp, des


def get_good_match(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    print(3)
    # index_params = dict(algorithm=0, trees=5)
    # search_params = dict(checks=50)
    # flann = cv2.FlannBasedMatcher(index_params, search_params)
    # matches = flann.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return good


def siftImageAlignment(img1, img2):
   kp1, des1 = sift_kp(img1)
   kp2, des2 = sift_kp(img2)
   print(1)
   goodMatch = get_good_match(des1, des2)
   print(2)
   # if len(goodMatch) > 4:
   ptsA = np.float32([kp1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
   ptsB = np.float32([kp2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
   ransacReprojThreshold = 4
   H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, ransacReprojThreshold)
   imgOut = cv2.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
   return imgOut, H, status


img1 = cv2.imread('re1/CB2045A-5X-A-1.JPG')
img2 = cv2.imread('re1/CB2045A-5X-B-1.JPG')
# img1 = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')
# img2 = cv2.imread('re1/BZ282S1006-5X-B-1.JPG')
# img1 = cv2.imread('re1/X85001A-5X-A-1.JPG')
# img2 = cv2.imread('re1/X85001A-5X-B-1.JPG')
img1 = img1.copy()
img2 = img2.copy()
print(1)
result, _, _ = siftImageAlignment(img1, img2)
print(2)
img = np.maximum(img1, result)
print(3)
allImg = np.concatenate((img1, img2, result, img), axis=1)
cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
cv2.imshow('Result', allImg)
cv2.waitKey(0)
# cv2.imshow('1', img)
# cv2.waitKey(0)