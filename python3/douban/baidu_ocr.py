#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

from aip import AipOcr

if __name__ == '__main__':
    APP_ID = '15306981'
    API_KEY = '5ZDzsFGj6cl6wa3QQSbF2xrn'
    SECRET_KEY = 'VUiYSYg12yImNROMaXG8LITDDG3O1SiT'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    def get_file_content(file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()


    image = get_file_content('/Users/liwenhao/Desktop/douban-captcha-example2.jpg')
    """ 调用通用文字识别(高精度), 图片参数为本地图片 """
    result = json.dumps(client.basicAccurate(image))
    print(result)
