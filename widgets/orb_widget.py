import glob
import cv2
import os
import numpy as np
from skimage import io
from qtpy.QtCore import QThread, Signal, Slot
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QPushButton
from qtpy.QtGui import Qt
from qtpy.QtWidgets import QLabel
from qtpy.QtWidgets import QWidget, QTextEdit, QTextBrowser


class TestThread(QThread):
    signal = Signal(str)

    def __init__(self, t1):
        super(TestThread, self).__init__()
        self.t1 = t1
        # self.t2 = t2
        # self.t3 = t3

    def run(self) -> None:
        self.start1()

    def start1(self):
        for path in glob.glob(os.path.join(self.t1, '*.JPG')):
            basename = os.path.basename(path)
            dir = os.path.dirname(path)
            pa = dir + '/对齐'
            pb = dir + '/融合'
            if not os.path.exists(pa):
                os.makedirs(pa)
            if not os.path.exists(pb):
                os.makedirs(pb)
            save1 = os.path.join(pa, basename)
            save2 = os.path.join(pb, basename)
            s = basename.split('_')
            prefix = '_'.join(s[:5])
            suffix = '_'.join(s[6:])
            if s[5] == 'A':
                b = os.path.join(dir, prefix + '_B_' + suffix)
                if not os.path.exists(b):
                    self.signal.emit(basename + '：转换失败！未找到对应的正交偏光图像！')
                    continue
                self.signal.emit(basename + ': 寻找成功！开始进行对齐：')
                print(path, b)
                img1 = io.imread(path)
                img2 = io.imread(b)

                size = (img1.shape[1], img2.shape[0])
                im1 = cv2.resize(img1, (1000, 1000), interpolation=cv2.INTER_AREA)
                im2 = cv2.resize(img2, (1000, 1000), interpolation=cv2.INTER_AREA)
                result, image = self.ORB(im1, im2)
                result = result[:, :, ::-1]
                result = cv2.resize(result, size, interpolation=cv2.INTER_AREA)

                cv2.imencode(save1, result)[1].tofile(save1)
                cv2.imencode(save2, image)[1].tofile(save2)
                self.signal.emit('融合成功，保存完成！')
                self.signal.emit(basename + '转换完成')
        self.signal.emit('该目录已经全部转换完成！')

    # 对齐
    def sift_kp(self, image):
        gary = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d_SIFT.create()
        kp, des = sift.detectAndCompute(gary, None)
        return kp, des

    def get_good_match(self, des1, des2):
        bf = cv2.BFMatcher()
        # matches = bf.knnMatch(des1, des2, k=2)
        matches = bf.match(des1,des2)
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)
        return good

    def siftImageAlignment(self, img1, img2):
        kp1, des1 = self.sift_kp(img1)
        kp2, des2 = self.sift_kp(img2)
        goodMatch = self.get_good_match(des1, des2)
        if len(goodMatch) > 4:
            ptsA = np.float32([kp1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
            ptsB = np.float32([kp2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
            ransacReprojThreshold = 4
            H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, ransacReprojThreshold)
            imgOut = cv2.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]),
                                         flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        return imgOut, H, status

    def ORB(self, img1, img2):
        result, _, _ = self.siftImageAlignment(img1, img2)
        self.signal.emit('对齐成功！开始融合：')
        image = np.maximum(img1, result)
        return result, image


class ORBWidget(QWidget):

    def __init__(self):
        super(ORBWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 700)
        self.setWindowTitle('对齐工具')

        label = QLabel('对齐工具', self)
        label.setStyleSheet('QLabel{font-family:Microsoft YaHei;font-size: 30px}')
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, 400, 100)

        # 输入路
        label = QLabel('图片路径:', self)
        label.setStyleSheet('QLabel{font-family:Microsoft YaHei;font-size: 15px}')
        label.setAlignment(Qt.AlignRight)
        label.setGeometry(5, 100, 80, 30)

        self.s_path = QTextEdit(self)
        self.s_path.setEnabled(False)
        self.s_path.setGeometry(90, 95, 230, 30)

        self.s_btn = QPushButton('浏览', self)
        self.s_btn.setStyleSheet('QPushButton{font-family:Microsoft YaHei;font: 15px}')
        self.s_btn.setGeometry(330, 95, 50, 30)
        self.s_btn.clicked.connect(self.openS)

        # 开始转换
        self.start_btn = QPushButton('开始转换', self)
        self.start_btn.setStyleSheet('QPushButton{font-family:Microsoft YaHei;font-size:20px;color:black;}')
        self.start_btn.setGeometry(10, 140, 380, 50)
        self.start_btn.clicked.connect(self.start)

        # 执行状态
        self.log = QTextBrowser(self)
        self.log.setGeometry(10, 200, 380, 400)

    def openS(self):
        dir = QFileDialog.getExistingDirectory(self, '选取文件夹', './')
        self.s_path.setText(dir)

    def start(self):
        if self.s_path.toPlainText() != '':
            self.log.append('开始转换')
            self.start_btn.setEnabled(False)
            t1 = self.s_path.toPlainText()
            self.thread = TestThread(t1)
            self.thread.signal.connect(self.appendLog)
            self.thread.start()

    @Slot(str)
    def appendLog(self, result):
        self.log.append(result)

