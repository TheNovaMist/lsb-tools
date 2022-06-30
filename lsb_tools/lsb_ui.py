import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QTabWidget, QDesktopWidget)

from lsb_ui_decrypt import Decrypt
from lsb_ui_encrypt import Encrypt


class Tab(QWidget):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        self.tabWidget = QTabWidget()

        # 两个tab
        encrypt = Encrypt()
        decrypt = Decrypt()

        self.tabWidget.addTab(encrypt, "添加水印")
        self.tabWidget.addTab(decrypt, "提取水印")

        vbox.addWidget(self.tabWidget)

        # 获取显示器长宽
        cp = QDesktopWidget().availableGeometry()
        width = cp.width() / 2
        height = cp.height() / 2

        # 固定窗口大小
        self.setFixedSize(int(width), int(height))
        self.setWindowTitle('lsb tool')
        self.setLayout(vbox)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tab = Tab()
    sys.exit(app.exec_())
