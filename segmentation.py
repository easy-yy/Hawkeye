import cv2
import numpy as np
import math

import skimage
from skimage.feature import greycomatrix, greycoprops
from skimage import color, img_as_ubyte, segmentation, io, restoration, filters
from skimage.future import graph
import matplotlib.pyplot as plt


# 提取RGB，融合图像
def GetRGB(img1, img2):
    return np.maximum(img1, img2)


# 提取图像纹理特征，灰度共生矩阵
def GLCM_K(img):
    x, y, z = img.shape
    gray = color.rgb2gray(img)
    image = img_as_ubyte(gray)
    bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255])  # 16-bit
    inds = np.digitize(image, bins)
    max_value = inds.max() + 1
    '''
        image:正值图像，[1]：距离
        [0, np.pi/4, np.pi/2, 3*np.pi/4]:0度,45度,90度，135度
        levels:灰度数
        symmetric=False（默认false）
        normed=False（默认false）
    '''
    matrix_coocurrence = greycomatrix(inds, [1], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=max_value)
    '''
        GLCM properties
        prop:{'contrast' 对比度, 'dissimilarity' 差异性, 'homogeneity' 逆差矩
        'energy' 熵, 'correlation' 相关性, 'ASM' 二阶矩(能量)    
    '''
    contrast = greycoprops(matrix_coocurrence, 'contrast')
    # dissimilarity = greycoprops(matrix_coocurrence, 'dissimilarity')
    # homogeneity = greycoprops(matrix_coocurrence, 'homogeneity')
    energy = greycoprops(matrix_coocurrence, 'energy')
    correlation = greycoprops(matrix_coocurrence, 'correlation')
    asm = greycoprops(matrix_coocurrence, 'ASM')
    Tk = energy + contrast - asm - correlation
    # print(Tk)
    T = (x + y) / Tk
    # print(T)
    K = (T[0][0] + T[0][1] + T[0][2] + T[0][3]) / (4*10)
    # print(K)
    K1 = math.ceil(abs(K))
    # print(K1)
    return K1


def SLIC(img, K):
    labels = segmentation.slic(img, compactness=20, n_segments=K, max_size_factor=5, convert2lab=True)
    # labels = segmentation.watershed(img, connectivity=2, compactness=20)

    # g = graph.rag_mean_color(img, labels, mode='similarity')

    # 展示RAG区域邻接图
    # lc = graph.show_rag(labels, g, img)
    # cbar = plt.colorbar(lc)
    # plt.show()

    # 区域邻接图上执行归一化图切割
    # labels = graph.cut_normalized(labels, g)
    show = segmentation.mark_boundaries(img, labels, color=(0, 0, 255))
    cv2.imwrite('re1/result2.jpg', show*255)

    # label = graph.cut_threshold(seg_map, g, 22)
    # show = segmentation.mark_boundaries(image, label, color=(0, 0, 255))
    # return show*255


def WaterShed(img):
    # Step1. 加载图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Step2.阈值分割，将图像分为黑白两部分
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Step3. 对图像进行“开运算”，先腐蚀再膨胀
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # Step4. 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    # Step5.通过distanceTransform获取前景区域
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    # DIST_L1 DIST_C只能 对应掩膜为3    DIST_L2 可以为3或者5
    ret, sure_fg = cv2.threshold(dist_transform, 0.1 * dist_transform.max(), 255, 0)
    # Step6. sure_bg与sure_fg相减,得到既有前景又有背景的重合区域   #此区域和轮廓区域的关系未知
    sure_fg = np.uint8(sure_fg)
    unknow = cv2.subtract(sure_bg, sure_fg)
    # Step7. 连通区域处理
    ret, markers = cv2.connectedComponents(sure_fg, connectivity=8)
    # 对连通区域进行标号  序号为 0 - N-1
    markers = markers + 1
    # OpenCV 分水岭算法对物体做的标注必须都大于1,背景为标号为0,因此对所有markers加1变成了1-N
    # 去掉属于背景区域的部分（即让其变为0，成为背景）
    # 此语句的Python语法 类似于if ，“unknow == 255” 返回的是图像矩阵的真值表。
    markers[unknow == 255] = 0
    # Step8.分水岭算法
    markers = cv2.watershed(img, markers)
    # 分水岭算法后，所有轮廓的像素点被标注为  -1
    # print(markers)
    img[markers == -1] = [0, 0, 255]  # 标注为-1 的像素点标 红黑,轮廓线
    # img[markers == 1] = [255, 255, 255]
    # img[markers >= 2] = [0, 0, 0]
    th1 = skimage.morphology.remove_small_holes(thresh, area_threshold=2000, connectivity=1) * 255
    th1 = 255 - th1
    th1 = np.array(th1, dtype=np.uint8)
    th1 = skimage.morphology.remove_small_holes(th1, area_threshold=2000, connectivity=1) * 255
    th1 = np.array(th1, dtype=np.uint8)
    return th1


def Orb(img1, img2):
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(500)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)
    # Remove not so good matches
    numGoodMatches = int(len(matches) * 0.15)
    matches = matches[:numGoodMatches]
    # Draw top matches
    imMatches = cv2.drawMatches(img2, keypoints1, img1, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", imMatches)
    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
    # Use homography
    height, width, channels = img1.shape
    im1Reg = cv2.warpPerspective(img2, h, (width, height))
    return img1, im1Reg

def Smooth_denoising(img):
    B, G, R = cv2.split(img)  # get single 8-bits channel
    EB = cv2.equalizeHist(B)
    EG = cv2.equalizeHist(G)
    ER = cv2.equalizeHist(R)
    equal_test = cv2.merge((EB, EG, ER))  # merge it back

    bilateral_filter_img1 = cv2.bilateralFilter(equal_test, 9, 100, 100)
    return bilateral_filter_img1


def RGB2GBR(img):
    return img[:, :, ::-1]


if __name__ == '__main__':
    # 读取单偏光和正交偏光图片
    # img1 = io.imread("LX53/LX-53，1557.30，25X-，单偏全貌.jpg")
    # img2 = io.imread("LX53/LX-53，1557.30，25X+，加试板.jpg")
    # img3 = io.imread("LX53/LX-53，1557.30，25X+，正交.jpg")
    # img1 = RGB2GBR(img1)
    # img2 = RGB2GBR(img2)
    # img3 = RGB2GBR(img3)
    # img1 = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')
    # img2 = cv2.imread('re2/test.png')
    # img3 = cv2.imread('re2/test1.png')
    # 融合图片
    # img1, img3 = Orb(img1, img3)
    # cv2.imwrite('LX53/img3.jpg', img3)
    # cv2.imwrite('LX53/img1.jpg', img1)
    # image1 = GetRGB(img1, img3)
    # image1 = GetRGB(img1, img3)

    # image1 = GetRGB(image1, img3)

    # 滤波
    # image2 = cv2.medianBlur(image1, 5)
    # 高斯双边滤波
    # dst = cv2.bilateralFilter(image1, d=5, sigmaColor=100, sigmaSpace=15)
    # 均值迁移滤波
    # dst = cv2.pyrMeanShiftFiltering(image1, sp=15, sr=60)
    # 光照均衡
    # B, G, R = cv2.split(img1)  # get single 8-bits channel
    # EB = cv2.equalizeHist(B)
    # EG = cv2.equalizeHist(G)
    # ER = cv2.equalizeHist(R)
    # image1 = cv2.merge((EB, EG, ER))  # merge it back

    # 增强图像，具有立体感
    # kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    # image1 = cv2.filter2D(img1, ddepth=-1, kernel=kernel)


    # 分水岭分割
    # image = cv2.imread('re1/CB2045A-5X-A-1.JPG')
    image = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')
    # imageA, imageB, imageC = WaterShed(image)
    imageB = WaterShed(image)
    cv2.imwrite('re1/result2.jpg', imageB)
    # contours = cv2.findContours(imageA, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # SLIC
    # imageA = SLIC(image, GLCM_K(image))

    # 保存结果
    # cv2.imwrite('融合/A.png', imageA)
    # cv2.imwrite('融合/B.png', imageB)
    # cv2.imwrite('融合/C.png', imageC)
    # cv2.imshow('0', imageA)
    # cv2.imshow('1', imageB)
    # cv2.waitKey(0)