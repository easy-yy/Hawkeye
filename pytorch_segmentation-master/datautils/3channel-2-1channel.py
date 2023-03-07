import cv2
from PIL import Image
import os
import numpy as np


def sigleChannel():
    path = "../data/trainLabels3/"  # 原始路径
    save_path = '../data/trainLabels/'  # 保存路径
    all_images = os.listdir(path)

    for image in all_images:
        image_path = os.path.join(path, image)
        img = Image.open(image_path)  # 打开图片
        r, g, b = img.split()
        img = r
        img.save(save_path + image)


def convertImage():
    image_path = '../outputs/predict 2.png'
    image = Image.open(image_path)  # 打开图片
    img_arr = np.asarray(image, dtype=np.double)
    img_arr1 = cv2.imread('../outputs/predict 2.png')
    colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
              (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0), (192, 128, 0),
              (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128), (0, 64, 0), (128, 64, 0),
              (0, 192, 0), (128, 192, 0), (0, 64, 128), (128, 64, 12), (0, 192, 128)]
    seg_img = img_arr.copy()
    for x in range(seg_img.shape[0]):
        for y in range(seg_img.shape[1]):
            c = int(seg_img[x][y])
            img_arr1[x][y][0] = colors[c][0]
            img_arr1[x][y][1] = colors[c][1]
            img_arr1[x][y][2] = colors[c][2]
    cv2.imwrite('../outputs/result1.png', img_arr1)
    # cv2.imshow('1', img_arr1)
    # cv2.waitKey(0)


def splitImage():
    image_path = '../outputs/re.png'
    image = Image.open(image_path)  # 打开图片
    img_arr = np.asarray(image, dtype=np.double)
    img = img_arr

    n = 1
    for n in range(1, 23):
        r_img = img_arr.copy()
        r_img[img != n] = 0
        r_img[img == n] = 255
        dst_img = np.array(r_img, dtype=np.uint8)
        contours, hierarchy = cv2.findContours(dst_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.imshow('1', dst_img)
        # cv2.waitKey(0)
        cv2.imwrite('../data/' + str(n) + '.png', dst_img)


convertImage()
# splitImage()
# sigleChannel()
