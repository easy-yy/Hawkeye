import PySide2
from PySide2.QtCore import QPoint, Qt, Signal
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QWidget, QScrollArea


class ImageZoom(QWidget):

    def __init__(self, parent, title, pixmap):
        super(ImageZoom, self).__init__()
        self.setParent(parent)
        self.scale = 1.0
        self.pixmap = pixmap
        self._painter = QPainter()
        self.setWindowTitle(title)

    def offsetToCenter(self):
        s = self.scale
        area = super().size()
        w, h = self.pixmap.width() * s, self.pixmap.height() * s
        aw, ah = area.width(), area.height()
        x = (aw - w) / (2 * s) if aw > w else 0
        y = (ah - h) / (2 * s) if ah > h else 0
        return QPoint(x, y)

    def paintEvent(self, event) -> None:
        if not self.pixmap:
            return super().paintEvent(event)
        p = self._painter
        s = self.scale

        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.scale(s, s)
        p.translate(self.offsetToCenter())
        p.drawPixmap(0, 0, self.pixmap)
        p.end()

    def wheelEvent(self, ev):

        mods = ev.modifiers()
        delta = ev.angleDelta()
        if Qt.ControlModifier == int(mods):
            if delta.y() < 0:
                if self.scale > 0.05:
                    self.scale -= 0.01
            else:
                self.scale += 0.01
            s = self.scale
            pw = self.pixmap.width() * s
            ph = self.pixmap.height() * s
            w = self.parent().width()
            h = self.parent().height()
            if pw > w or ph > h:
                self.resize(pw if pw > w else w, ph if ph > h else h)
            else:
                self.resize(w, h)
                self.update()

    def resizeEvent(self, event) -> None:
        self.scale = self.width() / self.pixmap.width() if self.width() / self.pixmap.width() < self.height() / self.pixmap.height()\
            else self.height() / self.pixmap.height()
        self.repaint()


class ImageView(QWidget):

    def __init__(self, title, pixmap):
        super(ImageView, self).__init__()
        self.image = ImageZoom(self, title, pixmap)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidget(self.image)
        self.resize(800, 600)

    def resizeEvent(self, event: PySide2.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.scrollArea.resize(self.width(), self.height())
        self.image.resize(self.width(), self.height())
