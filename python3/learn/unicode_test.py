# -*- coding: UTF-8 -*-
import chardet

if __name__ == '__main__':
    s = "我爱我的祖国"
    # print chardet.detect(s)
    s1 = u"我不是乱码"
    # s2 = unicode("我不是乱码", "utf-8")
    print(chardet.detect(s))
    print(chardet.detect(s))
