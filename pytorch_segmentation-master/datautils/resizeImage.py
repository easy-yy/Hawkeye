import os
import cv2


def Crop(image, label, filename, SavePath):
    width = image.shape[1]
    height = image.shape[0]
    print(width, height)
    CropSize = 512

    x = height // CropSize
    y = width // CropSize
    print(x, y)
    #  裁剪图片,重复率为RepetitionRate

    for i in range(x):
        for j in range(y):
            img = image.copy()
            lab = label.copy()
            cropped1 = img[
                      int(i * CropSize): int(i * CropSize) + CropSize,
                      int(j * CropSize): int(j * CropSize) + CropSize]
            cropped2 = lab[
                      int(i * CropSize): int(i * CropSize) + CropSize,
                      int(j * CropSize): int(j * CropSize) + CropSize]
            #  写图像
            cv2.imwrite(SavePath + 'trainImages/' + filename + '1-%d-' % i + '%d.jpg' % j, cropped1)
            cv2.imwrite(SavePath + 'trainLabels3/' + filename + '1-%d-' % i + '%d.png' % j, cropped2)
    #  向前裁剪最后一列
    for i in range(x):
        img = image.copy()
        lab = label.copy()
        cropped1 = img[
                      int(i * CropSize): int(i * CropSize) + CropSize,
                      (width - 512): width]
        cropped2 = lab[
                      int(i * CropSize): int(i * CropSize) + CropSize,
                      (width - 512): width]
        #  写图像
        cv2.imwrite(SavePath + 'trainImages/' + filename + '2-%d-' % i + '%d.jpg' % j, cropped1)
        cv2.imwrite(SavePath + 'trainLabels3/' + filename + '2-%d-' % i + '%d.png' % j, cropped2)
    #  向前裁剪最后一行
    for j in range(y):
        img = image.copy()
        lab = label.copy()
        cropped1 = img[
                      (height - 512): height,
                      int(j * CropSize): int(j * CropSize) + CropSize]
        cropped2 = lab[
                      (height - 512): height,
                      int(j * CropSize): int(j * CropSize) + CropSize]
        cv2.imwrite(SavePath + 'trainImages/' + filename + '3-%d-' % i + '%d.jpg' % j, cropped1)
        cv2.imwrite(SavePath + 'trainLabels3/' + filename + '3-%d-' % i + '%d.png' % j, cropped2)
    #  裁剪右下角
    cropped1 = img[(height - 512): height, (width - 512): width]
    cropped2 = lab[(height - 512): height, (width - 512): width]
    cv2.imwrite(SavePath + 'trainImages/' + filename + '4-1.jpg', cropped1)
    cv2.imwrite(SavePath + 'trainLabels3/' + filename + '4-1.png', cropped2)


label_dir = os.path.join('../sybp/dataset/labels/')
image_dir = os.path.join('../sybp/dataset/images/')

savePath = 'data/'
labels = os.listdir(label_dir)
images = os.listdir(image_dir)

for file in labels:
    if os.path.isfile(label_dir + file):
        label = cv2.imread(label_dir + file)
        image = cv2.imread(image_dir + file)
        file = file.split('.')[0]
        Crop(image, label, file, savePath)


# image = cv2.imread('sybp/dataset/images/BZ282S1006-5X-A-1.png')
# label = cv2.imread('sybp/dataset/masks/BZ282S1006-5X-A-1.png')
# filename = 'BZ.jpg'
# filename= filename.split('.')[0]
# print(filename)

# Crop(image, label, filename, savePath)
