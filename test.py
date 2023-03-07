import cv2
import numpy as np
import math
from skimage.feature import greycomatrix, greycoprops
from skimage import color, img_as_ubyte, segmentation, measure

img = cv2.imread('MIOu/A.jpg')

class tt:
    x = 0
    y = 0
    color = 0

    def on_EVENT_LBUTTONDOWN(self, event, x, y, flags, param):
        colors = [
            [0, 0, 0],
            [0, 50, 0],
            [1, 0, 0],
            [150, 150, 150],
            [0, 0, 200],
            [255, 255, 0]
        ]
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x = x
            self.y = y
            Z = seg_map[y][x]
            for props in measure.regionprops(seg_map):
                if props.label == Z:
                    for p in props.coords:
                        img[p[0]][p[1]] = colors[self.color]
            cv2.imshow('1', img)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.color += 1
            if self.color >= len(colors):
                self.color = 0
        # for a in range(len(seg_map)):
        #     for b in range(len(seg_map[a])):
        #         if seg_map[a][b] == Z:
        #             img[a][b] = [0, 0, 0]

    def GLCM_K(self, img):
        x, y, z = img.shape
        gray = color.rgb2gray(img)
        image = img_as_ubyte(gray)
        bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255])  # 16-bit
        inds = np.digitize(image, bins)
        max_value = inds.max() + 1
        matrix_coocurrence = greycomatrix(inds, [1], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=max_value)
        contrast = greycoprops(matrix_coocurrence, 'contrast')
        energy = greycoprops(matrix_coocurrence, 'energy')
        correlation = greycoprops(matrix_coocurrence, 'correlation')
        asm = greycoprops(matrix_coocurrence, 'ASM')
        Tk = energy + contrast - asm - correlation
        T = (x + y) / Tk
        K = (T[0][0] + T[0][1] + T[0][2] + T[0][3]) / (4 * 10)
        K1 = math.ceil(abs(K))
        return K1

    def SLIC(self, img, K):
        seg_map = segmentation.slic(img, compactness=16, n_segments=K, max_size_factor=5,
                                    min_size_factor=0.5, enforce_connectivity=True, convert2lab=True)
        show = segmentation.mark_boundaries(img, seg_map, color=(255, 255, 0))
        return show, seg_map

t = tt()
K = t.GLCM_K(img)
img, seg_map = t.SLIC(img, K)
t.img = seg_map
cv2.namedWindow("1")
cv2.setMouseCallback("1", t.on_EVENT_LBUTTONDOWN)
cv2.imshow('1', img)
cv2.waitKey()