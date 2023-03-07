from qtpy.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from qtpy.QtGui import QPixmap, QResizeEvent, QMouseEvent
from qtpy.QtCore import Qt

import os
import requests


class ImageDialog(QWidget):

    def __init__(self, imagePath):
        super(ImageDialog, self).__init__()
        self.initUI(imagePath)
        self.img = QPixmap(imagePath)
        self.imgWidth = self.img.width()
        self.imgHeight = self.img.height()


    def initUI(self, fileName):
        self.setWindowTitle(fileName)
        # self.resize(800, 600)

        self.imgLabel = QLabel(self)
        self.imgLabel.setGeometry(0, 0, self.width(), self.height())
        self.imgLabel.setScaledContents(True)

    # def resizeEvent(self, a0: QResizeEvent) -> None:
    #     self.imgLabel.setGeometry(0, 0, self.width(), self.height())
    #     if self.isMaximized():
    #         img = self.img.scaled(self.width(), self.height())
    #         self.imgLabel.setPixmap(img)
    #     else:
    #         min = self.width() / self.imgWidth if self.width() / self.imgWidth > self.height() / self.imgHeight \
    #             else self.height() / self.imgHeight
    #         img = self.img.scaled(self.imgWidth * min, self.imgHeight * min)
    #         self.imgLabel.setPixmap(img)


class TextLabelWidget(QLabel):

    def __init__(self, text=None):
        super().__init__()
        fileNameStyle = 'QLabel{font-size:20px;font-family:Arial;}'
        self.setStyleSheet(fileNameStyle)
        self.setAlignment(Qt.AlignCenter)
        if text is not None:
            self.setText(text)


class ImageLabelWidget(QLabel):

    def __init__(self):
        super().__init__()
        self.clickedEnabled = False
        self.imagePath = os.path.abspath('./icons/404.jpg')

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.clickedEnabled:
            self.imgWindow = ImageDialog(self.imagePath)
            self.imgWindow.show()

    def loadImage(self, imagePath):
        if not os.path.exists(imagePath):
            pass
        else:
            self.imagePath = imagePath
            self.clickedEnabled = True

        img = QPixmap(self.imagePath)
        img = img.scaled(360, 270)
        self.setPixmap(img)

    def loadServerImage(self, fileName):
        # url = 'http://172.23.252.215:8333/DataManagementSystem/isExit'
        url = 'http://125.64.98.246:8333/DataManagementSystem/isExit'
        path = './icons/source'
        res = requests.post(
            url,
            data={
                'fileName': fileName,
                'typeId': 1
            }
        )
        if res.json():
            # url = 'http://172.23.252.215:8333/DataManagementSystem/download'
            url = 'http://125.64.98.246:8333/DataManagementSystem/download'
            res = requests.get(
                url,
                params={
                    'fileName': fileName,
                    'typeId': 1
                },
            )
            with open(path + fileName[-7:], 'wb') as f:
                f.write(res.content)
            self.clickedEnabled = True
            self.imagePath = os.path.abspath(path + fileName[-7:])
        img = QPixmap(self.imagePath)
        img = img.scaled(360, 270)
        self.setPixmap(img)


class ImageContrastWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()
        # imagePath = os.path.abspath(imagePath)
        # self.loadImage(imagePath)

    def initUi(self):
        self.setWindowTitle('偏光图像对比')
        self.resize(800, 600)

        titleStyle = 'QLabel{font-size:30px;font-weight:normal;font-family:Arial;}'

        textA = QLabel('单偏光：')
        textA.setStyleSheet(titleStyle)

        hBoxATitle = QHBoxLayout()
        hBoxATitle.addWidget(textA)

        textB = QLabel('正交偏光：')
        textB.setStyleSheet(titleStyle)

        hBoxBTitle = QHBoxLayout()
        hBoxBTitle.addWidget(textB)

        self.imgA1 = ImageLabelWidget()
        self.imgA2 = ImageLabelWidget()
        self.imgA3 = ImageLabelWidget()
        self.imgA4 = ImageLabelWidget()
        self.imgA5 = ImageLabelWidget()

        hBoxA = QHBoxLayout()
        hBoxA.addWidget(self.imgA1)
        hBoxA.addWidget(self.imgA2)
        hBoxA.addWidget(self.imgA3)
        hBoxA.addWidget(self.imgA4)
        hBoxA.addWidget(self.imgA5)

        self.imgB1 = ImageLabelWidget()
        self.imgB2 = ImageLabelWidget()
        self.imgB3 = ImageLabelWidget()
        self.imgB4 = ImageLabelWidget()
        self.imgB5 = ImageLabelWidget()

        hBoxB = QHBoxLayout()
        hBoxB.addWidget(self.imgB1)
        hBoxB.addWidget(self.imgB2)
        hBoxB.addWidget(self.imgB3)
        hBoxB.addWidget(self.imgB4)
        hBoxB.addWidget(self.imgB5)

        self.textA1 = TextLabelWidget()
        self.textA2 = TextLabelWidget()
        self.textA3 = TextLabelWidget()
        self.textA4 = TextLabelWidget()
        self.textA5 = TextLabelWidget()

        hBoxAT = QHBoxLayout()
        hBoxAT.addWidget(self.textA1)
        hBoxAT.addWidget(self.textA2)
        hBoxAT.addWidget(self.textA3)
        hBoxAT.addWidget(self.textA4)
        hBoxAT.addWidget(self.textA5)

        self.textB1 = TextLabelWidget()
        self.textB2 = TextLabelWidget()
        self.textB3 = TextLabelWidget()
        self.textB4 = TextLabelWidget()
        self.textB5 = TextLabelWidget()

        hBoxBT = QHBoxLayout()
        hBoxBT.addWidget(self.textB1)
        hBoxBT.addWidget(self.textB2)
        hBoxBT.addWidget(self.textB3)
        hBoxBT.addWidget(self.textB4)
        hBoxBT.addWidget(self.textB5)

        vBox = QVBoxLayout()
        vBox.addLayout(hBoxATitle)
        vBox.addLayout(hBoxA)
        vBox.addLayout(hBoxAT)
        vBox.addLayout(hBoxBTitle)
        vBox.addLayout(hBoxB)
        vBox.addLayout(hBoxBT)

        self.setLayout(vBox)

    def loadImage(self, imagePath):

        fileName = imagePath.split('/')[-1][:-7]
        path = '/'.join(imagePath.split('/')[:-1]) + '/'

        self.imgA1.loadImage(path + fileName + 'A-1.jpg')
        self.imgA2.loadImage(path + fileName + 'A-2.jpg')
        self.imgA3.loadImage(path + fileName + 'A-3.jpg')
        self.imgA4.loadImage(path + fileName + 'A-4.jpg')
        self.imgA5.loadImage(path + fileName + 'A-5.jpg')

        self.imgB1.loadImage(path + fileName + 'B-1.jpg')
        self.imgB2.loadImage(path + fileName + 'B-2.jpg')
        self.imgB3.loadImage(path + fileName + 'B-3.jpg')
        self.imgB4.loadImage(path + fileName + 'B-4.jpg')
        self.imgB5.loadImage(path + fileName + 'B-5.jpg')

        self.textA1.setText(fileName + 'A-1.jpg')
        self.textA2.setText(fileName + 'A-2.jpg')
        self.textA3.setText(fileName + 'A-3.jpg')
        self.textA4.setText(fileName + 'A-4.jpg')
        self.textA5.setText(fileName + 'A-5.jpg')

        self.textB1.setText(fileName + 'B-1.jpg')
        self.textB2.setText(fileName + 'B-2.jpg')
        self.textB3.setText(fileName + 'B-3.jpg')
        self.textB4.setText(fileName + 'B-4.jpg')
        self.textB5.setText(fileName + 'B-5.jpg')

    def loadServerImage(self, fileName: str):

        fileName = fileName[:-7]

        self.imgA1.loadServerImage(fileName + 'A-1.jpg')
        self.imgA2.loadServerImage(fileName + 'A-2.jpg')
        self.imgA3.loadServerImage(fileName + 'A-3.jpg')
        self.imgA4.loadServerImage(fileName + 'A-4.jpg')
        self.imgA5.loadServerImage(fileName + 'A-5.jpg')

        self.imgB1.loadServerImage(fileName + 'B-1.jpg')
        self.imgB2.loadServerImage(fileName + 'B-2.jpg')
        self.imgB3.loadServerImage(fileName + 'B-3.jpg')
        self.imgB4.loadServerImage(fileName + 'B-4.jpg')
        self.imgB5.loadServerImage(fileName + 'B-5.jpg')

        self.textA1.setText(fileName + 'A-1.jpg')
        self.textA2.setText(fileName + 'A-2.jpg')
        self.textA3.setText(fileName + 'A-3.jpg')
        self.textA4.setText(fileName + 'A-4.jpg')
        self.textA5.setText(fileName + 'A-5.jpg')

        self.textB1.setText(fileName + 'B-1.jpg')
        self.textB2.setText(fileName + 'B-2.jpg')
        self.textB3.setText(fileName + 'B-3.jpg')
        self.textB4.setText(fileName + 'B-4.jpg')
        self.textB5.setText(fileName + 'B-5.jpg')