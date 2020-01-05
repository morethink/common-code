# -*- coding: UTF-8 -*-
import random
import time

import requests

if __name__ == '__main__':
    num = random.randint(0, 100)
    if num < 10:
        time.sleep(random.randint(0, 60) * 60)
        bark = "https://api.day.app/5jTdNbL57SDHfjk7SMJ7GK/做一个四有青年/你背单词时，阿拉斯加的鳕鱼正跃出水面，你算数学时，太平洋彼岸的海鸥振翅掠过城市上空，你晚自习时，极图中夜空散漫了五彩斑斓，但是少年你别着急，在你为自己未来踏踏实实地努力时，那些你感觉从来不会看到的景色，那些你觉得终身不会遇到的人，正一步步向你走来。"
        resp = requests.get(bark)
