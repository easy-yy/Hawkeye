from qtpy.QtCore import Qt
from qtpy.QtWidgets import QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget, QListView
from widgets.image_zoom_widget import ImageView


class ImageItem(QListWidgetItem):

    def __init__(self, filetype, pixmap):
        super(ImageItem, self).__init__()
        self.image = pixmap
        self.title = filetype
        self.initUI()

    def initUI(self):
        self.widget = QWidget()

        self.nameLabel = QLabel()
        self.nameLabel.setText(self.title)
        self.nameLabel.setAlignment(Qt.AlignCenter)

        self.imgLabel = QLabel()
        self.imgLabel.setScaledContents(True)
        img = self.image.scaled(200, 200)
        self.imgLabel.setPixmap(img)

        vbox = QVBoxLayout()
        vbox.addWidget(self.nameLabel)
        vbox.addWidget(self.imgLabel)
        vbox.addStretch(1)
        # 设置widget的布局
        self.widget.setLayout(vbox)
        # 设置自定义的QListWidgetItem的sizeHint，不然无法显示
        self.setSizeHint(self.widget.sizeHint())


class ImageList(QListWidget):

    def __init__(self):
        super(ImageList, self).__init__()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setFlow(QListView.LeftToRight)
        self.setFlow(QListView.TopToBottom)

    def loadImages(self, images, list_=None):
        self.clear()
        if list_ is not None:
            names = list_
        else:
            names = ['单偏光', '正交偏光', '对齐后图片', '融合后图片']
        for i, pixmap in enumerate(images):
            item = ImageItem(names[i], pixmap)
            self.addItem(item)
            self.setItemWidget(item, item.widget)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        item = self.currentItem()
        self.imgWidget = ImageView(item.title, item.image)
        self.imgWidget.show()


class ImageWidget(QWidget):

    def __init__(self, title, pixmap):
        super(ImageWidget, self).__init__()
        self.img = pixmap
        self.imgWidth = self.img.width()
        self.imgHeight = self.img.height()

        self.initUI()
        self.setWindowTitle(title)
        print(self.imgHeight, self.imgWidth)

    def initUI(self):

        self.resize(self.imgHeight/5, self.imgWidth/5)
        # self.resize(self.imgHeight, self.imgWidth)
        self.imgLabel = QLabel(self)
        self.imgLabel.setGeometry(0, 0, self.width(), self.height())
        self.imgLabel.setScaledContents(True)

        # vbox = QVBoxLayout()
        # vbox.addWidget(self.nameLabel)
        # vbox.addWidget(self.imgLabel)
        # vbox.addStretch()
        # # 设置widget的布局
        # self.widget.setLayout(vbox)
        # # 设置自定义的QListWidgetItem的sizeHint，不然无法显示
        # self.setSizeHint(self.widget.sizeHint())

    def resizeEvent(self, a0) -> None:
        self.imgLabel.setGeometry(0, 0, self.width(), self.height())
        if self.isMaximized():
            img = self.img.scaled(self.imgWidth, self.imgHeight)
            self.imgLabel.setPixmap(img)
        else:
            min = self.width() / self.imgWidth if self.width() / self.imgWidth > self.height() / self.imgHeight \
                else self.height() / self.imgHeight
            img = self.img.scaled(self.imgWidth * min, self.imgHeight * min)
            self.imgLabel.setPixmap(img)
