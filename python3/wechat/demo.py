# -*- coding: UTF-8 -*-

import itchat

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)  # 登录，会下载二维码给手机扫描登录，hotReload设置为True表示以后自动登录
    itchat.send('hello my love', toUserName='filehelper')  # 发送信息给微信文件助手

    friends = itchat.search_friends(name='好友昵称')  # 获取微信好友列表
    userName = friends[0]['UserName']
    itchat.send('hello my love', toUserName=userName)  # 发送信息给指定好友

    itchat.run()  # 让itchat一直运行
