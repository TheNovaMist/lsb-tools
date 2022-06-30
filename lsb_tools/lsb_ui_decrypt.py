import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, QDesktopWidget, \
    QMessageBox

from lsb_tool import Tool


class ExtractThread(QThread):
    err = pyqtSignal(str)
    """
    提取水印的线程
    """

    def __init__(self, decrypt):
        super().__init__()
        self.tool = Tool()
        self.decrypt = decrypt  # 关联组件 让子线程能够操作

        # 关联信号和槽
        self.err.connect(self.decrypt.handle_err)

    def run(self):
        embed_path = self.decrypt.mix

        # 输入为空则跳过
        if not os.path.isfile(embed_path):
            self.err.emit('请先选择图片')
            return

        bg_img, wt_img = self.tool.get_extract_images(embed_path)

        # 变为 QPixmap
        bg_pixmap = QPixmap(bg_img)
        wm_pixmap = QPixmap(wt_img)

        self.decrypt.bg_lbl.setPixmap(bg_pixmap)
        self.decrypt.wm_lbl.setPixmap(wm_pixmap)


"""
提取水印
"""


class Decrypt(QWidget):
    bg = ''
    wm = ''
    mix = ''

    def __init__(self):
        super(Decrypt, self).__init__()

        self.initUI()

    def initUI(self):
        # 固定窗口大小
        # 获取显示器长宽
        cp = QDesktopWidget().availableGeometry()
        width = cp.width() / 2
        height = cp.height() / 2
        box_width = int(width / 3.3)

        self.bg = ''
        self.wm = ''
        self.mix = ''

        # 带水印的图片
        self.mix_btn = QPushButton('提取')  # 显示生成的图片
        self.mix_btn.clicked.connect(self.extract_image)

        self.choose_embed_btn = QPushButton('选择图片')
        self.choose_embed_btn.clicked.connect(self.choose_embed_file)

        self.mix_pixmap = QPixmap(self.mix)
        self.mix_lbl = QLabel(self)

        self.mix_lbl.setFixedSize(box_width, box_width)
        self.mix_lbl.setScaledContents(True)
        self.mix_lbl.setPixmap(self.mix_pixmap)

        # 背景图片
        self.bg_pixmap = QPixmap(self.bg)
        self.bg_lbl = QLabel(self)

        self.bg_lbl.setFixedSize(box_width, box_width)
        self.bg_lbl.setScaledContents(True)  # 图像自适应大小
        self.bg_lbl.setPixmap(self.bg_pixmap)

        # 水印图片
        self.wm_pixmap = QPixmap(self.wm)
        self.wm_lbl = QLabel(self)

        self.wm_lbl.setFixedSize(box_width, box_width)
        self.wm_lbl.setScaledContents(True)
        self.wm_lbl.setPixmap(self.wm_pixmap)

        # 输入的图片
        vbox3 = QVBoxLayout()
        vbox3.addStretch(1)
        vbox3.addWidget(self.mix_lbl)
        vbox3.addStretch(1)
        vbox3.addWidget(self.choose_embed_btn)
        vbox3.addWidget(self.mix_btn)

        # 提取的背景图片
        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addWidget(self.bg_lbl)
        vbox1.addStretch(2)

        # 提取的水印图片
        vbox2 = QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.wm_lbl)
        vbox2.addStretch(2)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox3)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)
        self.setWindowTitle('lsb')
        self.show()

        # 创建子线程的时候绑定窗口组件
        self.work = ExtractThread(self)

    def choose_embed_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            self.mix = fname[0]
            self.mix_lbl.setPixmap(QPixmap(fname[0]))

    def extract_image(self):
        self.work.start()

    # 提示错误的弹窗
    def handle_err(self, err):
        reply = QMessageBox.warning(self, 'error', err, QMessageBox.Ok)
