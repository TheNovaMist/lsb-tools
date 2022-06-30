import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget, QDesktopWidget, \
    QMessageBox

from lsb_tool import Tool


class WorkerThread(QThread):
    """
    嵌入水印的线程
    """

    err = pyqtSignal(str)

    def __init__(self, decrypt):
        super().__init__()
        self.tool = Tool()
        self.encrypt = decrypt

        # 关联信号和槽
        self.err.connect(self.encrypt.handle_err)

    def run(self):

        bg_path = self.encrypt.bg
        wm_path = self.encrypt.wm
        # 输入为空则跳过
        if not os.path.isfile(bg_path) & os.path.isfile(wm_path):
            self.err.emit('请先选择背景和水印图片')
            return

        # catch assert error
        try:
            img = self.tool.get_embed_image(bg_path, wm_path)
        except Exception as err:
            print(err)
            # 弹出错误对话
            self.err.emit(str(err))

            return

        # 变为 QPixmap
        image = QPixmap(img)

        self.encrypt.mix_lbl.setPixmap(image)


class Encrypt(QWidget):
    bg = ''
    wm = ''
    mix = ''

    def __init__(self):
        super(Encrypt, self).__init__()

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

        self.choose_bg_btn = QPushButton('选择背景图')
        # 绑定选择文件action
        self.choose_bg_btn.clicked.connect(self.choose_bg_file)
        self.bg_pixmap = QPixmap(self.bg)
        self.bg_lbl = QLabel(self)

        # 正方形
        self.bg_lbl.setFixedSize(box_width, box_width)
        self.bg_lbl.setScaledContents(True)  # 图像自适应大小
        self.bg_lbl.setPixmap(self.bg_pixmap)

        self.choose_wm_btn = QPushButton('选择水印')
        # 绑定选择文件action
        self.choose_wm_btn.clicked.connect(self.choose_wm_file)
        self.wm_pixmap = QPixmap(self.wm)
        self.wm_lbl = QLabel(self)

        # 正方形
        self.wm_lbl.setFixedSize(box_width, box_width)
        self.wm_lbl.setScaledContents(True)
        self.wm_lbl.setPixmap(self.wm_pixmap)

        self.mix_btn = QPushButton('合成')
        # 显示生成的图片
        self.mix_btn.clicked.connect(self.show_embed_image)
        self.mix_pixmap = QPixmap(self.mix)
        self.mix_lbl = QLabel(self)

        # 正方形
        self.mix_lbl.setFixedSize(box_width, box_width)
        self.mix_lbl.setScaledContents(True)
        self.mix_lbl.setPixmap(self.mix_pixmap)

        # 保存生成的带水印图片
        self.save_btn = QPushButton('保存')
        self.save_btn.clicked.connect(self.save_embed_image)

        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addWidget(self.bg_lbl)
        vbox1.addStretch(1)
        vbox1.addWidget(self.choose_bg_btn)

        vbox2 = QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.wm_lbl)
        vbox2.addStretch(1)
        vbox2.addWidget(self.choose_wm_btn)

        vbox3 = QVBoxLayout()
        vbox3.addStretch(1)
        vbox3.addWidget(self.mix_lbl)
        vbox3.addStretch(1)
        vbox3.addWidget(self.mix_btn)
        vbox3.addWidget(self.save_btn)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)

        self.setLayout(hbox)
        self.setWindowTitle('lsb')
        self.show()

        # 创建子线程的时候绑定窗口组件
        self.work = WorkerThread(self)

    def choose_bg_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            self.bg = fname[0]
            self.bg_lbl.setPixmap(QPixmap(fname[0]))

    def choose_wm_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            self.wm = fname[0]
            self.wm_lbl.setPixmap(QPixmap(fname[0]))

    def show_embed_image(self):

        self.work.start()

    """
    保存生成的含有水印的图片
    """

    def save_embed_image(self):
        # 对话框保存 传递路径
        image_path = QFileDialog.getSaveFileName(self, '保存图片', './', '*.png')
        self.mix_lbl.pixmap().save(image_path[0])

    # 提示错误的弹窗
    def handle_err(self, err):
        reply = QMessageBox.warning(self, 'error', err, QMessageBox.Ok)
