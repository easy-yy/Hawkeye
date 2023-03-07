from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QLabel, QFrame, QComboBox, QTextEdit, QPushButton
import featureOpt
import widgets.feature_widget


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
        self.featureTitle.setStyleSheet('QLabel{font-size: 18px;}')

        self.featureBox = QComboBox(self)
        self.featureBox.setGeometry(120, 15, 200, 30)
        self.featureBox.setStyleSheet('QComboBox{font-size: 16px;}')

    def loadData(self, features):
        for feature in features:
            self.featureBox.addItem(feature)


class FeatureWidget(QWidget):

    def __init__(self):
        super(FeatureWidget, self).__init__()
        self.initUI()
        self.shape = None
        self.save.clicked.connect(self.saveFeatures)
        self.feature_id = None

    def initUI(self):
        self.labelName = QLabel(self)
        self.labelName.setGeometry(130, 10, 350, 50)
        self.labelName.setStyleSheet('QLabel{font-size: 20px}')

        label = self.labelName
        if label in ['石英', ]:
            # 解理
            self.jl = BoxWidget(self, '解理：', ['无'])
            self.jl.setGeometry(10, 70, 350, 50)
            # 风化特征
            self.fh = BoxWidget(self, '风化特征：', ['无', '不易风化，表面无色透明'])
            self.fh.setGeometry(10, 130, 350, 50)
            # 双晶特征
            self.sj = BoxWidget(self, '双晶特征：', ['无'])
            self.sj.setGeometry(10, 190, 350, 50)
            # 干涉色
            self.gss = BoxWidget(self, '干涉色：', ['无', '一级灰、一级灰白、一级黄白'])
            self.gss.setGeometry(10, 250, 350, 50)
            # 消光
            self.xg = BoxWidget(self, '消光：', ['无', '波状消光(受作用力石英)', '平均消光'])
            self.xg.setGeometry(10, 310, 350, 50)
            # 保存
            self.save = QPushButton(self)
            self.save.setText('保存')
            self.save.setGeometry(130, 370, 200, 40)
        elif label in ['燧石']:
            # 解理
            self.jl = BoxWidget(self, '解理：', ['无'])
            self.jl.setGeometry(10, 70, 350, 50)
            # 风化特征
            self.fh = BoxWidget(self, '风化特征：', ['无', '不易风化，表面无色透明'])
            self.fh.setGeometry(10, 130, 350, 50)
            # 干涉色
            self.gss = BoxWidget(self, '干涉色：', ['无', '一级灰白'])
            self.gss.setGeometry(10, 190, 350, 50)
            # 消光
            self.xg = BoxWidget(self, '消光：', ['无', '平行消光'])
            self.xg.setGeometry(10, 250, 350, 50)
            # 双晶特征
            self.sj = BoxWidget(self, '双晶特征：', ['无'])
            self.sj.setGeometry(10, 310, 350, 50)
            # 其他
            self.qt = BoxWidget(self, '其他：', ['无', '纤维状、放射状集合体'])
            self.qt.setGeometry(10, 370, 350, 50)
            # 保存
            self.save = QPushButton(self)
            self.save.setText('保存')
            self.save.setGeometry(130, 430, 200, 40)
        elif label in ['微斜长石']:
            # 解理
            self.jl = BoxWidget(self, '解理：', ['无', '两组完全解理'])
            self.jl.setGeometry(10, 70, 350, 50)
            # 风化特征
            self.fh = BoxWidget(self, '风化特征：', ['无', '表面浑浊，浅土褐色'])
            self.fh.setGeometry(10, 130, 350, 50)
            # 干涉色
            self.gss = BoxWidget(self, '干涉色：', ['无', '一级灰白'])
            self.gss.setGeometry(10, 190, 350, 50)
            # 双晶特征
            self.sj = BoxWidget(self, '双晶特征：', ['无', '格子双晶'])
            self.sj.setGeometry(10, 250, 350, 50)
            # 其他
            self.qt = BoxWidget(self, '其他：', ['无'])
            self.qt.setGeometry(10, 310, 350, 50)
            # 保存
            self.save = QPushButton(self)
            self.save.setText('保存')
            self.save.setGeometry(130, 370, 200, 40)
        elif label in ['正长石']:
            # 晶形
            self.jx = BoxWidget(self, '晶形：', ['无', '板状、粒状'])
            self.jx.setGeometry(10, 70, 350, 50)
            # 风化特征
            self.fh = BoxWidget(self, '风化特征：', ['无', '具高岭土化，浅土褐色'])
            self.fh.setGeometry(10, 130, 350, 50)
            # 干涉色
            self.gss = BoxWidget(self, '干涉色：', ['无', '一级灰、一级灰白'])
            self.gss.setGeometry(10, 190, 350, 50)
            # 双晶特征
            self.sj = BoxWidget(self, '双晶特征：', ['无'])
            self.sj.setGeometry(10, 250, 350, 50)
            # 其他
            self.qt = BoxWidget(self, '其他：', ['无'])
            self.qt.setGeometry(10, 310, 350, 50)
            # 保存
            self.save = QPushButton(self)
            self.save.setText('保存')
            self.save.setGeometry(130, 370, 200, 40)
        elif label in ['条纹长石']:
            # 组成特征
            self.zc = BoxWidget(self, '组成特征：', ['无', '钾长石（主晶）和纳质长石（客晶）'])
            self.zc.setGeometry(10, 70, 350, 50)
            # 晶形
            self.jx = BoxWidget(self, '晶形：', ['无', '正交光下具条纹结构'])
            self.jx.setGeometry(10, 130, 350, 50)
            # 风化特征
            self.fh = BoxWidget(self, '风化特征：', ['无', '具高岭土化，浅土褐色'])
            self.fh.setGeometry(10, 190, 350, 50)
            # 保存
            self.save = QPushButton(self)
            self.save.setText('保存')
            self.save.setGeometry(130, 250, 200, 40)
        elif label in ['斜长石']:
            pass
        elif label in ['泥岩岩屑']:
            pass
        elif label in ['砂岩岩屑']:
            pass
        elif label in ['碳酸盐岩岩屑']:
            pass
        elif label in ['石英岩岩屑']:
            pass
        elif label in ['变质石英岩岩屑']:
            pass
        elif label in ['片麻岩岩屑']:
            pass
        elif label in ['千枚岩岩屑']:
            pass
        elif label in ['片岩岩屑']:
            pass
        elif label in ['花岗岩岩屑']:
            pass
        elif label in ['安山岩岩屑']:
            pass
        elif label in ['玄武岩岩屑']:
            pass
        elif label in ['酸性喷出岩岩屑']:
            pass
        elif label in ['火山碎屑岩岩屑']:
            pass
        elif label in ['黑云母']:
            pass
        elif label in ['白云母']:
            pass
        elif label in ['绿泥石']:
            pass
        elif label in ['重矿物']:
            pass
        elif label in ['泥质']:
            pass
        elif label in ['黄铁矿']:
            pass
        elif label in ['菱铁矿']:
            pass
        elif label in ['方解石']:
            pass
        elif label in ['白云石']:
            pass
        elif label in ['铁方解石']:
            pass
        elif label in ['铁白云石']:
            pass
        elif label in ['高领石']:
            pass
        else:
            self.save = QPushButton(self)
            self.save.setText('保存')
            self.save.setGeometry(10, 570, 80, 30)


            # self.xg.featureBox.setCurrentText(features['消光'])
            # self.jx.featureBox.setCurrentText(features['晶形'])
            # self.ys.featureBox.setCurrentText(features['颜色'])
            # self.lx.featureBox.setCurrentText(features['类型'])
            # self.tz.featureBox.setCurrentText(features['特征'])
            # self.tq.featureBox.setCurrentText(features['突起'])
            # self.qt.featureBox.setCurrentText(features['其他'])
            # self.gss.featureBox.setCurrentText(features['干涉色'])
            # self.fh.featureBox.setCurrentText(features['风化特征'])
            # self.sj.featureBox.setCurrentText(features['双晶特征'])
            # self.zc.featureBox.setCurrentText(features['组成特征'])
            # self.jxt.featureBox.setCurrentText(features['镜下特征'])
            # self.jg.featureBox.setCurrentText(features['结构特征'])
            # self.cf.featureBox.setCurrentText(features['成分特征'])
            # self.gz.featureBox.setCurrentText(features['构造特征'])

        # # 解理
        # self.jl = BoxWidget(self, '解理：', ['无', '两组完全解理', '完全', '极完全一组解理', '一组完全解理'])
        # self.jl.setGeometry(10, 70, 350, 50)
        # # 风化特征
        # self.fh = BoxWidget(self, '风化特征：', ['无', '不易风化，表面无色透明', '表面浑浊，浅土褐色', '具高岭土化，浅土褐色', '部分绢云母化，表面浑浊'])
        # self.fh.setGeometry(10, 130, 350, 50)
        #
        # self.sj = BoxWidget(self, '双晶特征：', ['无', '格子双晶', '聚片双晶', '卡斯巴双晶'])
        # self.sj.setGeometry(10, 190, 350, 50)
        #
        # self.gss = BoxWidget(self, '干涉色：', ['无', '一级灰', '一级灰白', '一级黄白', '靛蓝等异常干涉色', '具鲜艳的二至三级干涉色'])
        # self.gss.setGeometry(10, 250, 350, 50)
        #
        # self.xg = BoxWidget(self, '消光：', ['无', '波状消光', '斜消光', '平行消光', '近平等消光', '近平行消光', '平均消光'])
        # self.xg.setGeometry(10, 310, 350, 50)
        #
        # self.jx = BoxWidget(self, '晶型：', ['无', '板状', '粒状', '条纹结构', '叶片状', '等轴粒状', '片状', '鳞片状、玫瑰花形集合体产出'])
        # self.jx.setGeometry(10, 370, 350, 50)

        # line3 = self.drawLine()
        # line3.setGeometry(20, 5, 2, 190)

        # self.qtT = QLabel(self)
        # self.qtT.setText('其他特征：')
        # self.qtT.setGeometry(30, 430, 100, 50)
        # self.qtT.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # self.qtT.setStyleSheet('QLabel{font-size: 20px;}')
        #
        # self.qt = QTextEdit(self)
        # self.qt.setGeometry(130, 440, 200, 120)
        # self.qt.setStyleSheet('QTextEdit{font-size: 20px;}')



    def drawLine(self):
        line = QFrame(self)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet('QFrame{border: 1px solid gray}')
        return line

    def loadData(self, shape):
        # if shape.features['解理'] == '无':
        feature = featureOpt.readFeatures(shape.label)
        self.copyFeatures(shape, feature)
        features = shape.features
        label = shape.label
        self.initUI()
        if shape.label in ['石英']:
            self.jl.featureBox.setCurrentText(features['解理'])
            self.xg.featureBox.setCurrentText(features['消光'])
            self.gss.featureBox.setCurrentText(features['干涉色'])
            self.fh.featureBox.setCurrentText(features['风化特征'])
            self.sj.featureBox.setCurrentText(features['双晶特征'])
            self.labelName.setText(shape.label)
        elif shape.label in ['燧石']:
            self.jl.featureBox.setCurrentText(features['解理'])
            self.xg.featureBox.setCurrentText(features['消光'])
            self.gss.featureBox.setCurrentText(features['干涉色'])
            self.fh.featureBox.setCurrentText(features['风化特征'])
            self.sj.featureBox.setCurrentText(features['双晶特征'])
            self.qt.featureBox.setCurrentText(features['其他'])
            self.labelName.setText(shape.label)
        elif label in ['微斜长石']:
            self.jl.featureBox.setCurrentText(features['解理'])
            self.gss.featureBox.setCurrentText(features['干涉色'])
            self.fh.featureBox.setCurrentText(features['风化特征'])
            self.sj.featureBox.setCurrentText(features['双晶特征'])
            self.qt.featureBox.setCurrentText(features['其他'])
            self.labelName.setText(shape.label)
        elif label in ['正长石']:
            pass
        elif label in ['条纹长石']:
            pass
        elif label in ['斜长石']:
            pass
        elif label in ['泥岩岩屑']:
            pass
        elif label in ['砂岩岩屑']:
            pass
        elif label in ['碳酸盐岩岩屑']:
            pass
        elif label in ['石英岩岩屑']:
            pass
        elif label in ['变质石英岩岩屑']:
            pass
        elif label in ['片麻岩岩屑']:
            pass
        elif label in ['千枚岩岩屑']:
            pass
        elif label in ['片岩岩屑']:
            pass
        elif label in ['花岗岩岩屑']:
            pass
        elif label in ['安山岩岩屑']:
            pass
        elif label in ['玄武岩岩屑']:
            pass
        elif label in ['酸性喷出岩岩屑']:
            pass
        elif label in ['火山碎屑岩岩屑']:
            pass
        elif label in ['黑云母']:
            pass
        elif label in ['白云母']:
            pass
        elif label in ['绿泥石']:
            pass
        elif label in ['重矿物']:
            pass
        elif label in ['泥质']:
            pass
        elif label in ['黄铁矿']:
            pass
        elif label in ['菱铁矿']:
            pass
        elif label in ['方解石']:
            pass
        elif label in ['白云石']:
            pass
        elif label in ['铁方解石']:
            pass
        elif label in ['铁白云石']:
            pass
        elif label in ['高领石']:
            pass
        else:
            self.jl.featureBox.setCurrentText(features['解理'])
            self.xg.featureBox.setCurrentText(features['消光'])
            self.jx.featureBox.setCurrentText(features['晶形'])
            self.ys.featureBox.setCurrentText(features['颜色'])
            self.lx.featureBox.setCurrentText(features['类型'])
            self.tz.featureBox.setCurrentText(features['特征'])
            self.tq.featureBox.setCurrentText(features['突起'])
            self.qt.featureBox.setCurrentText(features['其他'])
            self.gss.featureBox.setCurrentText(features['干涉色'])
            self.fh.featureBox.setCurrentText(features['风化特征'])
            self.sj.featureBox.setCurrentText(features['双晶特征'])
            self.zc.featureBox.setCurrentText(features['组成特征'])
            self.jxt.featureBox.setCurrentText(features['镜下特征'])
            self.jg.featureBox.setCurrentText(features['结构特征'])
            self.cf.featureBox.setCurrentText(features['成分特征'])
            self.gz.featureBox.setCurrentText(features['构造特征'])

        labelName = shape.label
        self.labelName.setText(labelName)
        self.feature_id = features['feature_id']
        self.shape = shape

    def getData(self):
        features = {
            '解理': self.jl.featureBox.currentText(),
            '消光': self.xg.featureBox.currentText(),
            '晶形': self.jx.featureBox.currentText(),
            '颜色': self.ys.featureBox.currentText(),
            '类型': self.lx.featureBox.currentText(),
            '特征': self.tz.featureBox.currentText(),
            '突起': self.tq.featureBox.currentText(),
            '其他': self.qt.featureBox.currentText(),
            '干涉色': self.gss.featureBox.currentText(),
            '风化特征': self.fh.featureBox.currentText(),
            '双晶特征': self.sj.featureBox.currentText(),
            '组成特征': self.zc.featureBox.currentText(),
            '镜下特征': self.jxt.featureBox.currentText(),
            '结构特征': self.jg.featureBox.currentText(),
            '成分特征': self.cf.featureBox.currentText(),
            '构造特征': self.gz.featureBox.currentText(),
            'feature_id': self.feature_id,
            'labelName': self.labelName.text()
        }
        return features

    def saveFeatures(self):
        feature = self.getData()
        self.copyFeatures(self.shape, feature)
        featureOpt.writeFeatures(self.shape.features)

    def copyFeatures(self, shape, feature):
        shape.features['解理'] = feature['解理']
        shape.features['消光'] = feature['消光']
        shape.features['晶形'] = feature['晶形']
        shape.features['颜色'] = feature['颜色']
        shape.features['类型'] = feature['类型']
        shape.features['特征'] = feature['特征']
        shape.features['突起'] = feature['突起']
        shape.features['其他'] = feature['其他']
        shape.features['干涉色'] = feature['干涉色']
        shape.features['风化特征'] = feature['风化特征']
        shape.features['双晶特征'] = feature['双晶特征']
        shape.features['组成特征'] = feature['组成特征']
        shape.features['镜下特征'] = feature['镜下特征']
        shape.features['结构特征'] = feature['结构特征']
        shape.features['成分特征'] = feature['成分特征']
        shape.features['构造特征'] = feature['构造特征']
        shape.features['labelName'] = shape.label

