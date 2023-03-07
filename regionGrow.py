import numpy as np
import cv2
from skimage import segmentation
from skimage.measure import regionprops


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y


def getGrayDiff(img, currentPoint, tmpPoint):
    print(tmpPoint)
    currentPoint = Point(currentPoint[0], currentPoint[1])
    return abs(int(img[currentPoint.x, currentPoint.y]) - int(img[tmpPoint.x, tmpPoint.y]))


def selectConnects(p):
    if p != 0:
        connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1),
                    Point(0, 1), Point(-1, 1), Point(-1, 0)]
    else:
        connects = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
    return connects


def regionGrow(img, seeds, thresh, p=1):
    height = img.shape[0]
    weight = img.shape[1]
    seedMark = np.zeros(img.shape)
    seedList = []
    for seed in seeds:
        seedList.append(seed)
    label = 1
    connects = selectConnects(p)
    while (len(seedList) > 0):
        currentPoint = seedList.pop(0)
        seedMark[currentPoint[0], currentPoint[1]] = label
        for i in range(8):
            tmpX = currentPoint[0] + connects[i].x
            tmpY = currentPoint[1] + connects[i].y
            if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:
                continue
            grayDiff = getGrayDiff(img, currentPoint, Point(tmpX, tmpY))
            if grayDiff < thresh and seedMark[tmpX, tmpY] == 0:
                seedMark[tmpX, tmpY] = label
                seedList.append(Point(tmpX, tmpY))
    return seedMark


img = cv2.imread('re1/test22.JPG')
seg_map = segmentation.slic(img, compactness=16, n_segments=1000, max_size_factor=5, min_size_factor=0.5,
                            enforce_connectivity=True, convert2lab=True)
# print(seg_map)
for props in regionprops(seg_map):
    binaryImg = regionGrow(img, props.coords, 10)
    cv2.imshow(' ', binaryImg)
    cv2.waitKey(0)