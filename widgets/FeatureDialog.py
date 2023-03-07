from PySide2.QtWidgets import QDialog, QLabel, QFrame, QWidget, QComboBox, QTextEdit, QPushButton
from PySide2.QtCore import Qt

import featureOpt


class BoxWidget(QWidget):

    def __init__(self, parent, featureTitle: str, featureItem):
        super().__init__()
        self.setParent(parent)
        self.initUI()
        self.featureTitle.setText(featureTitle)
        self.loadData(featureItem)

    def initUI(self):
        self.resize(600, 50)
        self.featureTitle = QLabel(self)
        self.featureTitle.setGeometry(20, 5, 100, 50)
        self.featureTitle.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.featureTitle.setStyleSheet('QLabel{font-size: 20px;}')

        self.featureBox = QComboBox(self)
        self.featureBox.setGeometry(120, 15, 250, 30)
        self.featureBox.setStyleSheet('QComboBox{font-size: 20px;}')

    def loadData(self, features):
        for feature in features:
            self.featureBox.addItem(feature)


class FeatureDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.shape = None
        self.save.clicked.connect(self.saveFeatures)
        self.feature_id = None

    def initUI(self):
        self.setWindowTitle('特征')
        self.resize(400, 640)
        self.setMaximumSize(400, 640)
        self.setMinimumSize(400, 640)

        # 标签名
        self.labelName = QLabel(self)
        self.labelName.setGeometry(20, 10, 200, 50)
        self.labelName.setStyleSheet('QLabel{font-size: 24px}')

        # 水平线
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setGeometry(0, 60, 720, 2)
        self.line.setStyleSheet('QFrame{border: 2px solid gray}')

        # 解理
        self.jl = BoxWidget(self, '解理：', ['无', '两组完全解理', '完全'])
        self.jl.setGeometry(0, 70, 800, 50)

        # 风化特征
        self.fh = BoxWidget(self, '风化特征：', ['无', '不易风化，表面无色透明', '表面浑浊，浅土褐色', '具高岭土化，浅土褐色'])
        self.fh.setGeometry(0, 120, 800, 50)

        self.sj = BoxWidget(self, '双晶特征：', ['无', '格子双晶', '聚片双晶'])
        self.sj.setGeometry(0, 170, 800, 50)

        self.gss = BoxWidget(self, '干涉色：', ['无', '一级灰', '一级灰白', '一级黄白'])
        self.gss.setGeometry(0, 220, 800, 50)

        self.xg = BoxWidget(self, '消光：', ['无', '波状消光', '斜消光', '平行消光'])
        self.xg.setGeometry(0, 270, 800, 50)

        self.jx = BoxWidget(self, '晶型：', ['无', '板状', '粒状', '条纹', '叶片状', '等轴粒状'])
        self.jx.setGeometry(0, 320, 800, 50)

        self.qtT = QLabel(self)
        self.qtT.setText('其他：')
        self.qtT.setGeometry(20, 370, 100, 50)
        self.qtT.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.qtT.setStyleSheet('QLabel{font-size: 20px;}')

        self.qt = QTextEdit(self)
        self.qt.setGeometry(120, 380, 250, 150)
        self.qt.setStyleSheet('QTextEdit{font-size: 20px;}')

        self.save = QPushButton(self)
        self.save.setText('保存')
        self.save.setGeometry(290, 570, 80, 30)

    def loadData(self, shape):
        if shape.features['jl'] == '无':
            feature = featureOpt.readFeatures(shape.label)
            self.copyFeatures(shape, feature)
        features = shape.features
        self.jl.featureBox.setCurrentText(features['jl'])
        self.fh.featureBox.setCurrentText(features['fh'])
        self.sj.featureBox.setCurrentText(features['sj'])
        self.gss.featureBox.setCurrentText(features['gss'])
        self.xg.featureBox.setCurrentText(features['xg'])
        self.jx.featureBox.setCurrentText(features['jx'])
        self.qt.setText(features['qt'])
        self.labelName.setText(shape.label)

        self.feature_id = features['feature_id']

        self.shape = shape

    def getData(self):
        features = {
            'jl': self.jl.featureBox.currentText(),
            'fh': self.fh.featureBox.currentText(),
            'sj': self.sj.featureBox.currentText(),
            'gss': self.gss.featureBox.currentText(),
            'xg': self.xg.featureBox.currentText(),
            'jx': self.jx.featureBox.currentText(),
            'qt': self.qt.toPlainText(),
            'feature_id': self.feature_id,
            # 'labelName': self.labelName.text()
        }
        return features

    def saveFeatures(self):
        feature = self.getData()
        self.copyFeatures(self.shape, feature)
        featureOpt.writeFeatures(self.shape.features)

    def copyFeatures(self, shape, feature):
        shape.features['jl'] = feature['jl']
        shape.features['fh'] = feature['fh']
        shape.features['sj'] = feature['sj']
        shape.features['gss'] = feature['gss']
        shape.features['xg'] = feature['xg']
        shape.features['jx'] = feature['jx']
        shape.features['qt'] = feature['qt']


