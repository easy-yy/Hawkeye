from qtpy.QtGui import Qt
from qtpy.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton


class LoginDialog(QDialog):

    def __init__(self):
        super(LoginDialog, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录')
        self.setFixedSize(400, 300)

        label = QLabel('岩石薄片智能识别系统', self)
        label.setStyleSheet('QLabel{font-size: 30px}')
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 30, 400, 60)

        label1 = QLabel('用户名:', self)
        label1.setStyleSheet('QLabel{font-size: 20px}')
        label1.setAlignment(Qt.AlignRight)
        label1.setGeometry(10, 120, 100, 30)
        self.username = QLineEdit(self)
        self.username.setGeometry(130, 115, 200, 30)

        label2 = QLabel('密码:', self)
        label2.setAlignment(Qt.AlignRight)
        label2.setStyleSheet('QLabel{font-size: 20px}')
        label2.setGeometry(10, 170, 100, 30)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(130, 165, 200, 30)

        self.loginBtn = QPushButton('登录', self)
        self.loginBtn.setGeometry(230, 225, 100, 30)