#!/usr/bin/python
# -*- coding: UTF-8 -*-
from hashlib import md5
import requests
import json


# 通过超级鹰识别验证码
def recognition_captcha(filename, code_type):
    im = open(filename, 'rb').read()
    params = {
        'user': 'morethink',
        'pass2': md5('123456789'.encode('utf8')).hexdigest(),
        'softid': '898005',
        'codetype': code_type
    }
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    }
    files = {'userfile': ('ccc.jpg', im)}
    resp = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                         headers=headers).json()
    return resp


# 调用代码
if __name__ == '__main__':
    print(json.dumps(recognition_captcha('/Users/liwenhao/Desktop/rec/douban-captcha-example1.jpeg', 1006)))
