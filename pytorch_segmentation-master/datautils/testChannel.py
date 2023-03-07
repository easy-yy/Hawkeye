from PIL import Image
import cv2
from torchvision import transforms


file = '../testimg/4444.png'
to_tensor = transforms.ToTensor()
MEAN = [0.45734706, 0.43338275, 0.40058118]
STD = [0.23965294, 0.23532275, 0.2398498]
normalize = transforms.Normalize(MEAN, STD)

image1 = Image.open(file)
print(image1)
image1 = image1.convert('RGB')
print(image1)
image1 = transforms.Normalize(transforms.ToTensor(image1)).unsqueeze(0)
print(image1)
image2 = cv2.imread(file)
print(image2)