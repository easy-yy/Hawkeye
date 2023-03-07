import PIL.Image
import PIL.ImageEnhance
from qtpy.QtCore import Qt
from qtpy import QtGui
from qtpy import QtWidgets

import utils
import requests


class BrightnessContrastDialog(QtWidgets.QDialog):
    def __init__(self, img, callback, is_server, f_name, parent=None):
        super(BrightnessContrastDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Brightness/Contrast")

        self.slider_brightness = self._create_slider()
        self.slider_contrast = self._create_slider()

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(self.tr("Brightness"), self.slider_brightness)
        formLayout.addRow(self.tr("Contrast"), self.slider_contrast)
        self.setLayout(formLayout)

        assert isinstance(img, PIL.Image.Image)
        self.img = img
        self.callback = callback
        self.f_name = f_name
        self.IsServer = is_server

    def onNewValue(self, value):
        brightness = self.slider_brightness.value() / 50.0
        contrast = self.slider_contrast.value() / 50.0

        img = self.img
        img = PIL.ImageEnhance.Brightness(img).enhance(brightness)
        img = PIL.ImageEnhance.Contrast(img).enhance(contrast)

        img_data = utils.img_pil_to_data(img)
        # --------------------------------------------------------------------------- #
        #  修改
        # 保存亮度和对比度图片，并上传服务器
        # 新增传值 is_server（是否连接服务器） 和 f_name（当前图片的文件名）
        if self.IsServer:
            server_path = 'http://125.64.98.246:8333'
            imgp = 'ResultsImage/source.jpg'
            with open(imgp, 'wb') as f:
                img.save(f)
            url = '/DataManagementSystem/OriPicAdd'
            files = {
                'file': (self.f_name, open(imgp, 'rb')),
            }
            data = {
                'typeId': 2,
            }
            res = requests.post(
                url=server_path + url,
                data=data,
                files=files
            )
        # --------------------------------------------------------------------------- #
        qimage = QtGui.QImage.fromData(img_data)
        self.callback(qimage)

    def _create_slider(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(0, 150)
        slider.setValue(50)
        slider.valueChanged.connect(self.onNewValue)
        return slider
