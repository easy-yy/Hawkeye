from PySide2.QtCore import Qt
from qtpy.QtWidgets import QTabWidget, QApplication


class TabWidget(QTabWidget):

    def __init__(self, parent, horizontal=True):
        super(TabWidget, self).__init__()
        self.setParent(parent)

        w = QApplication.desktop().width()
        if w > 1920:
            self.w = 450
            self.h = 350
        elif 1366 < w <= 1920:
            self.w = 350
            self.h = 250
        else:
            self.w = 250
            self.h = 200

        self.mousePressPos = None
        if horizontal:
            self.setMaximumWidth(self.w)
            self.tabBarClicked['int'].connect(self.horizontalBarClickedEvent)
        else:
            self.setMaximumHeight(self.h)
            self.tabBarClicked['int'].connect(self.verticalBarClickedEvent)

    def horizontalBarClickedEvent(self, index):
        if index == self.currentIndex():
            if self.width() == self.w:
                self.setMaximumSize(self.tabBar().width(), self.parent().maximumHeight())
            else:
                self.setMaximumSize(self.w, self.parent().maximumHeight())
        else:
            self.setMaximumSize(self.w, self.parent().maximumHeight())

    def verticalBarClickedEvent(self, index):
        if index == self.currentIndex():
            if self.height() == self.h:
                self.setMaximumSize(self.parent().maximumWidth(), self.tabBar().height())
            else:
                self.setMaximumSize(self.parent().maximumWidth(), self.h)
        else:
            self.setMaximumSize(self.parent().maximumWidth(), self.h)

    def mouseMoveEvent(self, event) -> None:
        super().mouseMoveEvent(event)

        w = self.w
        h = self.h
        step = 40
        self.setCursor(Qt.SizeHorCursor)
        if event.buttons() == Qt.LeftButton:
            if self.mousePressPos and (self.mousePressPos.x() >= w - step or self.mousePressPos.y() >= h - step):
                if w - step <= event.x() <= w + step:
                    self.w = event.x()
                    self.setMaximumWidth(self.w)
                    self.mousePressPos = event.pos()
        self.setCursor(Qt.CustomCursor)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.mousePressPos = event.pos()