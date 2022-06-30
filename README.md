# lsb-tools
A python-based lsb image encryption and decryption tool using PyQT5.

![gui](https://github.com/TheNovaMist/lsb-tools/blob/main/gui.png)

The lsb digital watermarking algorithm is used to embed digital watermarks into images.

Dividing the color image into 8 bit planes, the lower bit planes contain little information about the image, and the watermark image can be embedded into the lower planes without affecting the appearance features of the image.

😊See this. [Image Steganography using Python| by Rupali Roy | Towards Data Science](https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372)

## Requirements

It is not limited to this dependency, but is only developed based on this dependency version.

- numpy==1.22.4
- opencv-python==4.6.0.66
- PyQt5==5.15.6
- PyQt5-Qt5==5.15.2
- PyQt5-sip==12.10.1

(Development on windows platform, so there maybe bugs on other platforms.)

## Usage

1. Configure python requirements
2. Run `lsb_ui.py`
3. Select image files and Click run button



## Description

![structure](https://github.com/TheNovaMist/lsb-tools/blob/main/structure.png)

> lsb_ui模块是程序的主界面，负责窗口的创建。
>
> lsb_ui_decrypt和lsb_ui_encrypt模块分别对应着加密和解密的界面模块，处理图片的选择和组件的布局。
>
> lsb_tool是工具模块，负责从上层ui模块向lsb_core模块传递选择的图片信息，并从lsb_core模块向上层组件传递处理后的图像。
>
> lsb_core是程序的核心模块，含有处理图像的逻辑，用来为图像添加水印、从图像提取水印。
