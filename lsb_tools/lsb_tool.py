import lsb_core
from PyQt5.QtGui import QImage


class Tool:

    def __init__(self):
        self.app = lsb_core.Core()

    """
    传入带水印的图片
    :return QImage类型的背景图片和水印图片
    """

    def get_extract_images(self, embed_path):
        # 传入图片路径
        self.app.set_embed_path(embed_path)

        bg_img, wt_img = self.app.get_extract_image()

        # 转换为QImage
        height, width, channel = bg_img.shape
        bytesPerLine = 3 * width
        bg_qImg = QImage(bg_img.data, width, height, bytesPerLine, QImage.Format_RGB888)

        height, width, channel = wt_img.shape
        bytesPerLine = 3 * width
        wt_qImg = QImage(wt_img.data, width, height, bytesPerLine, QImage.Format_RGB888)

        return bg_qImg, wt_qImg

    """
    传入背景图像和水印图像的路径
    :return QImage类型的合成图像
    """

    def get_embed_image(self, bg_path, wm_path):
        self.app.set_image_path(bg_path, wm_path)
        cvImg = self.app.get_mix_image()

        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)

        return qImg
