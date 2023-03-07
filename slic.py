import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from skimage.feature import greycomatrix, greycoprops
from skimage import color, img_as_ubyte, segmentation, measure


# 提取图像纹理特征，灰度共生矩阵
from skimage.morphology import dilation
from skimage.segmentation import find_boundaries


def GLCM_K(img):
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
    K = (T[0][0] + T[0][1] + T[0][2] + T[0][3]) / (4*10)
    K1 = math.ceil(abs(K))
    return K1


def SLIC(img, K):
    seg_map =segmentation.slic(img, compactness=16, n_segments=K, max_size_factor=5, min_size_factor=0.5)

    res = cv2.equalizeHist(cv2.convertScaleAbs(seg_map))
    print(res)
    cv2.imshow('ret', np.hstack((img, res)))
    cv2.waitKey(0)

    # contours = cv2.findContours(seg_map, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    # show1 = segmentation.find_boundaries(seg_map)
    # print(show1)
    # list = []
    # List = []
    # for props in measure.regionprops(seg_map):
    #     print(props.label)
    #     for i in range(len(props.coords)):
    #         x = props.coords[i][0]
    #         y = props.coords[i][1]
    #         if show1[x][y] == True:
    #             list.apend(props.coords[i])
    #             img[x][y] = [0, 0, 0]
    #     List.append(list)
    #     if props.label == 1:
    #         break
    #
    # plt.imshow(seg_map)
    # plt.show()


if __name__ == '__main__':
    image = cv2.imread('re1/BZ282S1006-5X-A-1.JPG')
    K = GLCM_K(image)
    image1 = SLIC(image, K)
    # cv2.imwrite('re1/resultA.jpg', image1)


'''
   **area** : int
        区域像素点数量.
    **bbox** : tuple
        Bounding box ``(min_row, min_col, max_row, max_col)``.
        属于边界框的像素处于半开区间
        ``[min_row; max_row)`` and ``[min_col; max_col)``.
    **bbox_area** : int
        Number of pixels of bounding box.
        边框的像素数。
    **centroid** : array
        Centroid coordinate tuple ``(row, col)``.
        质心坐标
    **convex_area** : int
        Number of pixels of convex hull image, which is the smallest convex
        polygon that encloses the region.
        凸包图像的像素数，包围该区域的最小多边形。
    **convex_image** : (H, J) ndarray
        Binary convex hull image which has the same size as bounding box.
        和bbox大小相同的二值图凸包
    **coords** : (N, 2) ndarray
        Coordinate list ``(row, col)`` of the region.
        区域坐标list
    **eccentricity** : float
        Eccentricity of the ellipse that has the same second-moments as the
        region. The eccentricity is the ratio of the focal distance
        (distance between focal points) over the major axis length.
        The value is in the interval [0, 1).
        When it is 0, the ellipse becomes a circle.
        与区域具有相同二阶矩的椭圆的偏心率。
        偏心率是焦距(焦点之间的距离)除以长轴长度的比率。
        取值范围为[0,1)，当取值为0时，椭圆变为圆。
    **equivalent_diameter** : float
        The diameter of a circle with the same area as the region.
        与区域面积相同的圆的直径
    **euler_number** : int
        Euler characteristic of region. Computed as number of objects (= 1)
        subtracted by number of holes (8-connectivity).
        区域的欧拉数
    **extent** : float
        Ratio of pixels in the region to pixels in the total bounding box.
        Computed as ``area / (rows * cols)``
        区域面积和边界外界框的面积比率
    **filled_area** : int
        Number of pixels of the region will all the holes filled in. Describes
        the area of the filled_image.
    **filled_image** : (H, J) ndarray
        Binary region image with filled holes which has the same size as
        bounding box.
    **image** : (H, J) ndarray
        Sliced binary region image which has the same size as bounding box.
        与bbox大小相同的切片二值图
    **inertia_tensor** : ndarray
        Inertia tensor of the region for the rotation around its mass.
        绕其质量旋转区域的惯性张量。
    **inertia_tensor_eigvals** : tuple
        The eigenvalues of the inertia tensor in decreasing order.
        惯性张量的特征值按递减顺序排列。
    **intensity_image** : ndarray
        Image inside region bounding box.
        图像内部区域边界框。
    **label** : int
        The label in the labeled input image.
        输入图像中的标签。
    **local_centroid** : array
        Centroid coordinate tuple ``(row, col)``, relative to region bounding
        box.
        质心坐标元组' ' (row, col) ' '，相对于区域边界
    **major_axis_length** : float
        The length of the major axis of the ellipse that has the same
        normalized second central moments as the region.
        椭圆长轴的长度，与区域具有相同的归一化二阶中心矩。
    **max_intensity** : float
        Value with the greatest intensity in the region.
        在该地区强度最大的值。
    **mean_intensity** : float
        Value with the mean intensity in the region.
        该区域的平均强度。
    **min_intensity** : float
        Value with the least intensity in the region.
        该区域强度最小的值
    **minor_axis_length** : float
        The length of the minor axis of the ellipse that has the same
        normalized second central moments as the region.
        短径
    **moments** : (3, 3) ndarray
        Spatial moments up to 3rd order::

            m_ij = sum{ array(row, col) * row^i * col^j }

        where the sum is over the `row`, `col` coordinates of the region.
    **moments_central** : (3, 3) ndarray
        Central moments (translation invariant) up to 3rd order::

            mu_ij = sum{ array(row, col) * (row - row_c)^i * (col - col_c)^j }

        where the sum is over the `row`, `col` coordinates of the region,
        and `row_c` and `col_c` are the coordinates of the region's centroid.
    **moments_hu** : tuple
        Hu moments (translation, scale and rotation invariant).
    **moments_normalized** : (3, 3) ndarray
        Normalized moments (translation and scale invariant) up to 3rd order::

            nu_ij = mu_ij / m_00^[(i+j)/2 + 1]

        where `m_00` is the zeroth spatial moment.
    **orientation** : float
        Angle between the 0th axis (rows) and the major
        axis of the ellipse that has the same second moments as the region,
        ranging from `-pi/2` to `pi/2` counter-clockwise.
    **perimeter** : float
        Perimeter of object which approximates the contour as a line
        through the centers of border pixels using a 4-connectivity.
        物体的周长，它近似于轮廓线，通过使用4连通性的边界像素中心的一条线。
    **slice** : tuple of slices
        A slice to extract the object from the source image.
        从源图像中提取对象的切片。
    **solidity** : float
        Ratio of pixels in the region to pixels of the convex hull image.
        区域内像素与凸包图像像素的比率。
    **weighted_centroid** : array
        Centroid coordinate tuple ``(row, col)`` weighted with intensity
        image.
    **weighted_local_centroid** : array
        Centroid coordinate tuple ``(row, col)``, relative to region bounding
        box, weighted with intensity image.
    **weighted_moments** : (3, 3) ndarray
        Spatial moments of intensity image up to 3rd order::

            wm_ij = sum{ array(row, col) * row^i * col^j }

        where the sum is over the `row`, `col` coordinates of the region.
    **weighted_moments_central** : (3, 3) ndarray
        Central moments (translation invariant) of intensity image up to
        3rd order::

            wmu_ij = sum{ array(row, col) * (row - row_c)^i * (col - col_c)^j }

        where the sum is over the `row`, `col` coordinates of the region,
        and `row_c` and `col_c` are the coordinates of the region's weighted
        centroid.
    **weighted_moments_hu** : tuple
        Hu moments (translation, scale and rotation invariant) of intensity
        image.
    **weighted_moments_normalized** : (3, 3) ndarray
        Normalized moments (translation and scale invariant) of intensity
        image up to 3rd order::
'''
