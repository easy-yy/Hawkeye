import yaml
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QPushButton, QListWidget, QListWidgetItem, QLabel, QComboBox, QHBoxLayout, QWidget


class FeatureItem(QListWidgetItem):

    def __init__(self, feature, option):
        super(FeatureItem, self).__init__()

        self.title = QLabel(feature)
        self.title.setAlignment(Qt.AlignRight)
        font = QFont('Microsoft YaHei', 12, 70)
        self.title.setFont(font)
        self.title.setFixedSize(70, 30)

        self.option = QComboBox()
        self.option.setFixedSize(230, 40)
        self.option.setStyleSheet(''
                                  'QComboBox{font-family:Microsoft YaHei;'
                                  'font-size:20px;'
                                  'color:black;'
                                  'selection-background-color:blue;'
                                  'outline:0px;}')
        self.option.setEditable(True)
        self.option.setCurrentIndex(-1)
        for opt in option:
            # self.option.setStyleSheet('QAbstractItemView{min-width:' + str(len(opt)) + 'px;}')
            self.option.addItem(opt)

        layout = QHBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.option)
        layout.addStretch(1)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        # self.widget.setBaseSize(200, 200)
        self.setSizeHint(self.widget.sizeHint())


class FeatureWidget(QListWidget):

    def __init__(self):
        super(FeatureWidget, self).__init__()
        self.shape = None
        self.labelName = None
        # 读取配置文件
        with open('config/feature_config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        # 所有的颗粒
        self.granule = self.config['granule']

    def loadDataFromShape(self, shape):
        self.labelName = shape.label
        self.shape = shape
        self.features = self.granule[self.labelName]
        self.clear()
        item = QListWidgetItem()
        item.setSizeHint(QSize(40, 40))
        qlabel = QLabel(self.labelName)
        font = QFont('Microsoft YaHei', 18, 60)
        qlabel.setFont(font)
        qlabel.setAlignment(Qt.AlignCenter)
        self.addItem(item)
        self.setItemWidget(item, qlabel)
        ff = {}
        if len(shape.features) != 20:
            ff = shape.features
        if self.features:
            for feature in self.features:
                item = FeatureItem(feature, self.features[feature])
                self.addItem(item)
                self.setItemWidget(item, item.widget)
                if len(ff) > 0:
                    item.option.setCurrentText(ff[feature])
        item = QListWidgetItem()
        item.setSizeHint(QSize(50, 50))
        btn = QPushButton('保存')
        btn.setStyleSheet('QPushButton{font-size: 25px}')
        btn.setBaseSize(200, 200)
        self.addItem(item)
        self.setItemWidget(item, btn)
        btn.clicked.connect(self.saveFeatureOfShape)

    def saveFeatureOfShape(self):
        feature = {}
        for i in range(1, self.count()-1):
            key = self.item(i).title.text()
            value = self.item(i).option.currentText()
            feature[key] = value
        self.shape.features = feature
        self.__saveConfig(self.labelName)

    def __saveConfig(self, label):
        granule = {}
        for i in range(1, self.count() - 1):
            key = self.item(i).title.text()
            opt = self.item(i).option
            features = [self.item(i).option.currentText()]
            for j in range(opt.count()):
                value = opt.itemText(j)
                if value not in features:
                    features.append(value)
            granule[key] = features
        self.config['granule'][label] = granule
        with open('config/feature_config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)





