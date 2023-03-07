from qtpy.QtWidgets import QTextBrowser, QDialog, QWidget
from qtpy.QtCore import QThread, Signal, Slot


class TestThread(QThread):
    signal = Signal(str)
    clear = Signal()

    def __init__(self):
        super(TestThread, self).__init__()

    def setFunc(self, func, *args):
        self.func = func
        self.args = args

    def run(self):
        self.func(self.args)


class TqdmDialog(QWidget):

    def __init__(self, title='进度展示'):
        super(TqdmDialog, self).__init__()
        self.setWindowTitle(title)
        self.initUI()
        self.setFixedSize(self.log.width() + 20, self.log.height() + 20)

    def initUI(self):
        self.log = QTextBrowser(self)
        self.log.setGeometry(10, 10, 550, 200)

    def start(self):
        self.log.append('开始转换')

    @Slot(str)
    def appendLog(self, result):
        self.log.append(result)

    @Slot()
    def clearLog(self):
        self.log.clear()
