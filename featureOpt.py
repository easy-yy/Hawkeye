import os
import json


def readFeatures(class_):
    defaultFile = './feature/feature.json'
    file = './feature/' + class_ + '.json'
    if not os.path.exists(file):
        with open(defaultFile, 'r', encoding='utf-8') as f:
            with open(file, 'w', encoding='utf-8') as ff:
                features = json.load(f)
                # features['labelName'] = class_
                json.dump(features, ff, ensure_ascii=False)
    else:
        with open(file, 'r', encoding='utf-8') as f:
            features = json.load(f)
            # features['labelName'] = class_
    return features


def writeFeatures(shape):
    class_ = shape.label
    file = './feature/' + class_ + '.json'
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(shape.features, f, ensure_ascii=False)
