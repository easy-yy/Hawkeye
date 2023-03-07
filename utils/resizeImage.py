import numpy as np
import glob
from PIL import Image
import cv2
import os


def Crop(filename, imagePath):
    SavePath = './Net/temp/'
    image = Image.open(imagePath)
    width, height = image.size
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    CropSize = 512
    x = height // CropSize
    y = width // CropSize

    for i in range(x):
        for j in range(y):
            img = image.copy()
            cropped1 = img[int(i * CropSize): int(i * CropSize) + CropSize,
                           int(j * CropSize): int(j * CropSize) + CropSize]
            cv2.imwrite(SavePath + filename + '1-%d-' % i + '%d.jpg' % j, cropped1)
            # cv2.imwrite(SavePath + '1-%d-' % i + '%d.jpg' % j, cropped1)
    #  向前裁剪最后一列
    for i in range(x):
        img = image.copy()
        cropped1 = img[int(i * CropSize): int(i * CropSize) + CropSize, (width - CropSize): width]
        cv2.imwrite(SavePath + filename + '2-%d-' % i + '%d.jpg' % j, cropped1)
        # cv2.imwrite(SavePath + '2-%d-' % i + '%d.jpg' % j, cropped1)
    #  向前裁剪最后一行
    for j in range(y):
        img = image.copy()
        cropped1 = img[(height - CropSize): height, int(j * CropSize): int(j * CropSize) + CropSize]
        cv2.imwrite(SavePath + filename + '3-%d-' % i + '%d.jpg' % j, cropped1)
        # cv2.imwrite(SavePath + '3-%d-' % i + '%d.jpg' % j, cropped1)
    #  裁剪右下角
    cropped1 = img[(height - CropSize): height, (width - CropSize): width]
    cv2.imwrite(SavePath + filename + '4-1.jpg', cropped1)
    # cv2.imwrite(SavePath + '4-1.jpg', cropped1)


def cat(src_path='./4444.png', path='./test512/4444', size=512, out='./icons/predict.jpg'):
    width, height = Image.open(src_path).size
    # area1 = sorted(glob.glob(f'{path}1*.jpg'))
    col = int(width / size)
    row = int(height / size)
    w = size - (width - size * col)
    h = size - (height - size * row)

    # 区域一
    image = None
    img_row = None
    for r in range(row):
        for c in range(col):
            if img_row is None:
                img_row = np.array(Image.open(f'{path}1-{r}-{c}.jpg'))
            else:
                img = np.array(Image.open(f'{path}1-{r}-{c}.jpg'))
                img_row = np.hstack((img_row, img))
        if image is None:
            image = img_row
        else:
            image = np.vstack((image, img_row))
        img_row = None

    # 区域二
    area2 = sorted(glob.glob(f'{path}2*.jpg'))
    img_col = None
    for p in area2:
        if img_col is None:
            img_col = np.array(Image.open(p))
        else:
            img = np.array(Image.open(p))
            img_col = np.vstack((img_col, img))
    image = np.hstack((image, img_col[:, w:]))

    # 区域三
    area3 = sorted(glob.glob(f'{path}3*.jpg'))
    for p in area3:
        if img_row is None:
            img_row = np.array(Image.open(p))
        else:
            img = np.array(Image.open(p))
            img_row = np.hstack((img_row, img))

    # 区域四
    area4 = np.array(Image.open(f'{path}4-1.jpg'))
    img_row = np.hstack((img_row, area4[:, w:]))

    # 总
    image = np.vstack((image, img_row[h:, :]))

    # 保存
    Image.fromarray(image).save(out)

    image_files = glob.glob(path + '*.jpg')
    for imgf in image_files:
        os.remove(imgf)
    # return np.array(image)
