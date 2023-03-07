import glob
import time
import PIL.Image
import PIL.ImageDraw
import cv2
import numpy as np
from skimage import morphology
from PIL import Image, ImageStat
import matplotlib.pyplot as plt
from skimage import io


def cnt_area(cnt):
    area = cv2.contourArea(cnt)
    return area


def cnt_props(prop):
    return prop.area


def contoursCv(th1):
    contours = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[1]
    contours.sort(key=cnt_area, reverse=True)  # 轮廓排序
    return contours


def sift_kp(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d_SIFT.create()
    kp, des = sift.detectAndCompute(image, None)
    return kp, des


def get_good_match(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return good


def siftImageAlignment(im0, im1, im2, im3, im4, im5):
    size = (im0.shape[1], im0.shape[0])
    size1 = (2000, 2000)
    im = cv2.resize(im0, size1, interpolation=cv2.INTER_LINEAR)
    im1 = cv2.resize(im1, size1, interpolation=cv2.INTER_LINEAR)
    im2 = cv2.resize(im2, size1, interpolation=cv2.INTER_LINEAR)
    im3 = cv2.resize(im3, size1, interpolation=cv2.INTER_LINEAR)
    im4 = cv2.resize(im4, size1, interpolation=cv2.INTER_LINEAR)
    im5 = cv2.resize(im5, size1, interpolation=cv2.INTER_LINEAR)
    kp1, des1 = sift_kp(im)
    kp2, des2 = sift_kp(im1)
    goodMatch = get_good_match(des1, des2)
    if len(goodMatch) > 4:
       ptsA = np.float32([kp1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
       ptsB = np.float32([kp2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
       H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 4)
       im1 = cv2.warpPerspective(im1, H, size1, flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
       im2 = cv2.warpPerspective(im2, H, size1, flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
       im3 = cv2.warpPerspective(im3, H, size1, flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
       im4 = cv2.warpPerspective(im4, H, size1, flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
       im5 = cv2.warpPerspective(im5, H, size1, flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    im1 = cv2.resize(im1, size, interpolation=cv2.INTER_LINEAR)
    im2 = cv2.resize(im2, size, interpolation=cv2.INTER_LINEAR)
    im3 = cv2.resize(im3, size, interpolation=cv2.INTER_LINEAR)
    im4 = cv2.resize(im4, size, interpolation=cv2.INTER_LINEAR)
    im5 = cv2.resize(im5, size, interpolation=cv2.INTER_LINEAR)
    return im1, im2, im3, im4, im5


def get_background(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([98, 43, 46])
    high_hsv = np.array([124, 255, 255])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    return mask


def get_background_b(image):
    im = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([98, 43, 46])
    high_hsv = np.array([124, 255, 255])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    im[mask != 0] = 0
    im[im != 0] = 255
    mask = im[:, :, 0]
    mask = mask.astype(np.bool_)
    mask = morphology.remove_small_objects(mask, 10000) * 255
    mask = mask.astype(np.bool_)
    mask = morphology.remove_small_holes(mask, 1000) * 255
    image[mask == 0] = 0
    return image


def prop_measure_new(all_seg, counters, cnt_s, mask):
    c = []
    for cnt in cnt_s:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 500 and h < 500:
            counters.append([cnt])
            c.append(cnt)
        elif w < 1000 and h < 1000:
            area0 = cv2.contourArea(cnt)
            area1 = cnt_area(np.array(cv2.convexHull(cnt)))
            if area0 / area1 > 0.7:
                counters.append([cnt])
                c.append(cnt)
        elif w < 2000 and h < 2000:
            area0 = cv2.contourArea(cnt)
            area1 = cnt_area(np.array(cv2.convexHull(cnt)))
            if area0 / area1 > 0.8:
                counters.append([cnt])
                c.append(cnt)
        else:
            area0 = cv2.contourArea(cnt)
            area1 = cnt_area(np.array(cv2.convexHull(cnt)))
            if area0 / area1 > 0.9:
                counters.append([cnt])
                c.append(cnt)
    # 返回True， False, np.unit8: 0, 1
    cnt_mask = shape_to_mask(mask.shape, c).astype(np.uint8)
    all_seg[cnt_mask == 1] = 0
    return all_seg, counters


def brightness_img(img, all_seg):
    im = Image.fromarray(img).convert('L')
    stat = ImageStat.Stat(im)
    rms = stat.rms[0]
    im1 = img.copy()
    im1[im1 < rms] = 0
    im1[all_seg == 0] = 0
    im1[im1 != 0] = 255
    mask = im1[:, :, 0]
    mask = morphology.remove_small_objects(mask.astype(np.bool_), 10000) * 255
    mask = morphology.remove_small_holes(mask.astype(np.bool_), 1000) * 255
    img[mask == 0] = 0
    return img


def shape_to_mask(img_shape, counters):
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    for points in counters:
        xy = [(point[0][0], point[0][1]) for point in points]
        draw.polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


def extract_prop_test(image, all_seg, counters):
    image[all_seg == 0] = 0
    image = morphology.remove_small_objects(image.astype(np.bool_), 10000) * 255
    cnts = cv2.findContours(image.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    cnts = list(filter(lambda x: len(x) > 100, cnts))
    all_seg, counters = prop_measure_new(all_seg, counters, cnts, image)
    return all_seg, counters


def mask_light(image, all_seg, counters):
    mask = image.copy()
    mask[mask != 0] = 255
    mask = mask[:, :, 0]
    mask[all_seg == 0] = 0
    mask = morphology.remove_small_objects(mask.astype(np.bool_), 50000) * 255

    cnts = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    cnts = list(filter(lambda x: len(x) > 100, cnts))
    all_seg, counters = prop_measure_new(all_seg, counters, cnts, mask)

    all_seg = morphology.remove_small_objects(all_seg.astype(np.bool_), 50000) * 255
    return all_seg, counters


def get_background_b_zhimi(image):
    im = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([98, 43, 46])
    high_hsv = np.array([124, 255, 255])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    im[mask != 0] = 0
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([11, 43, 46])
    high_hsv = np.array([43, 255, 255])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    im[mask != 0] = 0
    return im


def new_seg(pA, pB):

    im0 = io.imread(pA)
    im0 = im0[:, :, ::-1]

    # 制作counter和标准模版
    im0 = get_background_b_zhimi(im0)
    all_seg = im0.copy()
    all_seg = all_seg[:, :, 0]
    all_seg[all_seg != 0] = 255
    counters = []

    # 去蓝色背景和黄色杂质
    for im_path in pB:
        im = io.imread(im_path)
        im = im[:, :, ::-1]
        im = get_background_b_zhimi(im)
        im[all_seg == 0] = 0
        im = brightness_img(im, all_seg)
        all_seg, counters = mask_light(im, all_seg, counters)

    return counters
