import os
import cv2
import numpy as np


label_dir = os.path.join('../data/trainLabels3/')

labels = os.listdir(label_dir)
for file in labels:
    if os.path.isfile(label_dir + file):
        image = cv2.imread(label_dir+file)
        if np.max(image) > 22:
            print(file)
