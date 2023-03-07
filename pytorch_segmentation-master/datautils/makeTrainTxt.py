import os

image = os.listdir('../data/trainImages/')
with open('../data/train.txt', 'w', encoding='utf-8') as f:
    for file in image:
        file = file.split('.')[0]
        f.write(file + '\n')


# labels = os.listdir('../data/trainLabels3/')
# with open('../data/val.txt', 'w', encoding='utf-8') as f:
#     for file in labels:
#         file.split('.')[0]
#         f.write(file + '\n')