import cv2
import numpy as np
import skimage
import skimage.morphology
from matplotlib import pyplot as plt
from scipy import ndimage as ndi
# from skimage import filters


def cnt_area(cnt):
    area = cv2.contourArea(cnt)
    return area

def watershed():
    # Step1. 加载图像
    # img = cv2.imread('re1/CB2045A-5X-A-1.JPG')
    img = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')
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
    img[markers == -1] = [255, 255, 255]   # 标注为-1 的像素点标 红
    img[markers == 1] = [255, 255, 255]
    img[markers >= 2] = [0, 0, 0]
    # 变为单通道
    th1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh1 = skimage.morphology.remove_small_holes(thresh, area_threshold=2000, connectivity=1) * 255
    plt.subplot(242), plt.imshow(thresh, cmap='gray'),
    plt.title('Threshold'), plt.axis('off')
    plt.subplot(243), plt.imshow(thresh1, cmap='gray'),
    plt.title('Threshold'), plt.axis('off')
    plt.subplot(243), plt.imshow(opening, cmap='gray'),
    plt.title('Dilate'), plt.axis('off')
    plt.subplot(244), plt.imshow(dist_transform, cmap='gray'),
    plt.title('Dist Transform'), plt.axis('off')
    plt.subplot(245), plt.imshow(sure_fg, cmap='gray'),
    plt.title('Threshold'), plt.axis('off')
    plt.subplot(246), plt.imshow(unknow, cmap='gray'),
    plt.title('Unknow'), plt.axis('off')
    plt.subplot(247), plt.imshow(np.abs(markers), cmap='jet'),
    plt.title('Markers'), plt.axis('off')
    plt.imshow(th1)
    plt.show()
watershed()

def w2():
    np.set_printoptions(threshold=np.inf)
    img = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow('thresh', thresh)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    cv2.imshow('opening', opening)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    cv2.imshow('sure_bg', sure_bg)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
    cv2.imshow('sure_fg', sure_fg)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    cv2.imshow('unknown', unknown)

    ret, markers1 = cv2.connectedComponents(sure_fg)
    markers = markers1 + 1
    markers[unknown == 255] = 0
    markers3 = cv2.watershed(img, markers)
    img[markers3 == -1] = [255, 255, 0]
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def water_demo(img):
    print(img.shape)
    blurred = cv2.pyrMeanShiftFiltering(img,10,100)
    gray = cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)
    ret, binnary = cv2.threshold(gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    cv2.imshow("binnary",binnary)
    kerhel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    mb = cv2.morphologyEx(binnary,cv2.MORPH_OPEN,kerhel,iterations=2)
    sure_bg = cv2.dilate(mb,kerhel,iterations=3)
    cv2.imshow("sure_bg",sure_bg)

    dist = cv2.distanceTransform(mb,cv2.DIST_L2,3)
    dist_optput = cv2.normalize(dist,0,1.0,cv2.NORM_MINMAX)
    cv2.imshow("dist",dist_optput*50)
    ret, surface = cv2.threshold(dist,dist.max()*0.6,255,cv2.THRESH_BINARY)
    cv2.imshow("surface",surface)

    surface_fg = np.uint8(surface)
    unknown = cv2.subtract(sure_bg,surface_fg)
    ret,markers=cv2.connectedComponents(surface_fg)
    print(ret)

    markers = markers+1
    markers[unknown == 255]=0
    markers =cv2.watershed(img,markers = markers)
    img[markers ==-1]=[0,0,255]
    cv2.imshow("return",img)

    img = cv2.imread('re1/BZ282S1006-5X-A-1.JPG', 1)
    cv2.namedWindow('img', 0)
    cv2.namedWindow('binnary', 0)
    cv2.namedWindow('sure_bg', 0)
    cv2.namedWindow('dist', 0)
    cv2.namedWindow('surface', 0)
    cv2.namedWindow('return', 0)
    cv2.resizeWindow('img', 400, 320)
    cv2.resizeWindow('binnary',400, 320)
    cv2.resizeWindow('sure_bg',400, 320)
    cv2.resizeWindow('dist',400, 320)
    cv2.resizeWindow('surface',400, 320)
    cv2.resizeWindow('return',400, 320)
    cv2.imshow('img', img)
    water_demo(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def w4():
    image = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # 现在我们用分水岭算法分离两个圆
    denoised = skimage.filters.rank.median(image, skimage.morphology.disk(2))  # 过滤噪声

    # 将梯度值低于10的作为开始标记点
    markers = skimage.filters.rank.gradient(denoised, skimage.morphology.disk(5)) < 10
    markers = ndi.label(markers)[0]

    gradient = skimage.filters.rank.gradient(denoised, skimage.morphology.disk(2))  # 计算梯度
    labels = skimage.morphology.watershed(gradient, markers, mask=image)  # 基于梯度的分水岭算法

    cv2.imshow('or', image)
    cv2.imshow('gr', gradient)
    # cv2.imshow('ma', markers)
    cv2.imshow('la', labels)
    cv2.waitKey(0)

