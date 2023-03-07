import numpy as np
import math
from skimage.feature import greycomatrix, greycoprops
from skimage import io, color, img_as_ubyte

img = io.imread('image/t.jpg')
x, y, z = img.shape

gray = color.rgb2gray(img)
image = img_as_ubyte(gray)

bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255]) #16-bit
inds = np.digitize(image, bins)
max_value = inds.max()+1
'''
    image:正值图像，[1]：距离
    [0, np.pi/4, np.pi/2, 3*np.pi/4]:0度,45度,90度，135度
    levels:灰度数
    symmetric=False（默认false）
    normed=False（默认false）
'''
matrix_coocurrence = greycomatrix(inds, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=max_value)
'''
    GLCM properties
    prop:{'contrast' 对比度, 'dissimilarity' 差异性, 'homogeneity' 逆差矩
    'energy' 熵, 'correlation' 相关性, 'ASM' 二阶矩(能量)    
'''
contrast = greycoprops(matrix_coocurrence, 'contrast')
dissimilarity = greycoprops(matrix_coocurrence, 'dissimilarity')
homogeneity = greycoprops(matrix_coocurrence, 'homogeneity')
energy = greycoprops(matrix_coocurrence, 'energy')
correlation = greycoprops(matrix_coocurrence, 'correlation')
asm = greycoprops(matrix_coocurrence, 'ASM')

print(contrast)
print(dissimilarity)
print(homogeneity)
print(energy)
print(correlation)
print(asm)

Tk = energy + contrast - asm - correlation
print(Tk)
T = (x + y) / Tk
print(T)
K = (T[0][0]+T[0][1]+T[0][2]+T[0][3])/4
print(K)
K1 = math.ceil(abs(K))
print(K1)