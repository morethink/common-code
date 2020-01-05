# -*- coding: UTF-8 -*-
import os

if __name__ == '__main__':
    nowtime = os.popen("ifconfig |grep 'inet '|awk {'print $2'}|grep -v '127.0.0.1'|cut -d: -f2")
    print(nowtime.read())
