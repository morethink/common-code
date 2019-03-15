#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tesserocr

from PIL import Image

if __name__ == '__main__':
    captcha_path = "/Users/liwenhao/Desktop/douban-captcha-example1.jpeg"

    # # 新建Image对象
    image = Image.open(captcha_path)

    # 调用tesserocr的image_to_text()方法，传入image对象完成识别
    result = tesserocr.image_to_text(image)

    print(result)

    # 图片处理便于识别文字：彩色转灰度，灰度转二值，二值图像识别
    im = Image.open(captcha_path)
    w, h = im.size
    im = im.convert('L')  # convert()用于不同模式图像之间的转换
    threshold = 100  # 图片降噪处理
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.point(table, '1')
    w_new, h_new = w * 2, h * 2
    im = im.resize((w_new, h_new), Image.ANTIALIAS)  # 图片放大
    path = "/Users/liwenhao/Desktop/rec/captcha-example3.jpg"
    im.save(path)

    print(tesserocr.image_to_text(Image.open(path)))
