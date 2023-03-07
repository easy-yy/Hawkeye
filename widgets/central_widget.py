from PySide2.QtWidgets import QWidget, QListWidget, QTabWidget, QHBoxLayout, QVBoxLayout

from widgets.tab_widget import TabWidget


class CentralWidget(QWidget):

    def __init__(self, parent, canvas):
        super(CentralWidget, self).__init__()
        self.setParent(parent)
        self.initUI(canvas)

    def initUI(self, canvas):

        self.leftTab = TabWidget(self, True)
        self.leftTab.setTabPosition(QTabWidget.West)

        self.rightTab = TabWidget(self, True)
        self.rightTab.setTabPosition(QTabWidget.East)

        # self.bottomTab = TabWidget(self, False)
        # self.bottomTab.setTabPosition(QTabWidget.South)

        # 中间canvas
        self.canvas = canvas

        hBox = QHBoxLayout()
        hBox.setContentsMargins(0, 0, 0, 0)
        hBox.addWidget(self.leftTab)
        hBox.addWidget(self.canvas)
        hBox.addWidget(self.rightTab)

        # hBox2 = QHBoxLayout()
        # hBox2.setContentsMargins(20, 0, 20, 0)
        # hBox2.addWidget(self.bottomTab)

        vBox = QVBoxLayout()
        vBox.setContentsMargins(0, 0, 0, 0)
        vBox.addLayout(hBox)
        # vBox.addLayout(hBox2)

        self.setLayout(vBox)

    def addLeftWidget(self, widget, title):
        self.leftTab.addTab(widget, title)

    def addLeftLayout(self, layout, title):
        widget = QWidget()
        widget.setLayout(layout)
        self.leftTab.addTab(widget, title)

    def addRightWidget(self, widget, title):
        self.rightTab.addTab(widget, title)

    def addRightLayout(self, layout, title):
        widget = QWidget()
        widget.setLayout(layout)
        self.rightTab.addTab(widget, title)

    # def addBottomWidget(self, widget, title):
    #     self.bottomTab.addTab(widget, title)
    #
    # def addBottomLayout(self, layout, title):
    #     widget = QWidget()
    #     widget.setLayout(layout)
    #     self.bottomTab.addTab(widget, title)