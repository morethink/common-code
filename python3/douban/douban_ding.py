#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

import requests
import urllib3
import re
from hashlib import md5
import random
from lxml import html
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
urllib3.disable_warnings()


# 下载验证码图片
def download_captcha(captcha_url, agent):
    # findall返回的是一个列表
    captcha_name = re.findall("id=(.*?):", captcha_url)
    filename = "douban_%s.jpg" % (str(captcha_name[0]))
    logging.info("文件名为: " + filename)
    with open(filename, 'wb') as f:
        # 以二进制写入的模式在本地构建新文件
        header = {
            'User-Agent': agent,
            'Referer': captcha_url
        }
        f.write(requests.get(captcha_url, headers=header).content)
        logging.info("%s 下载完成" % filename)
    return filename


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
    # 错误处理
    if resp.get('err_no', 0) == 0:
        return resp.get('pic_str')


def result_verification(response):
    if response.status_code == 302:
        logging.info("豆瓣ding成功")
    else:
        logging.info(response.status_code)
        logging.info(response)
        url = "https://sc.ftqq.com/SCU37167T460e639bc3f6f62ab90c3a551460553d5c090f360cef6.send?text=douban失败" + \
              str(random.randint(0, 1000))
        requests.post(url)
        logging.info("豆瓣ding失败，发送失败信息到微信")


# 豆瓣顶帖
def douban_ding():
    # 豆瓣具体帖子
    url = "https://www.douban.com/group/topic/129122199/"
    # 豆瓣具体帖子回复的接口，格式是帖子链接+/add_comment
    comment_url = url + "/add_comment"
    cookie = 'll="108296"; bid=A15UCrHkbU4; _ga=GA1.2.1646425546.1520868371; _vwo_uuid_v2=D9259AAD7CAD23C91CF5B0925770B2D45|bfcc908c735a139e1738583d2e90b2de; gr_user_id=9c1d1d6b-87ec-4ff4-81c4-0a779721a18f; OUTFOX_SEARCH_USER_ID_NCOO=328889871.89926124; douban-fav-remind=1; __yadk_uid=JflylLEQXpoB2MAKaVY29uSc5suFHgDx; viewed="27032786_30155726_26786719_3369600_6538430"; __utmz=30149280.1543833505.24.17.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); push_noty_num=0; push_doumail_num=0; ps=y; ct=y; __utmc=30149280; ue="lwhyx9@qq.com"; dbcl2="14660354:JdguK/eRZ8Q"; ck=NjRh; __utmv=30149280.1466; __ads_session=lH9Oek1GNQkx9egsRwA=; ap_v=0,6.0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1544953613%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; _pk_id.100001.8cb4=653f1061c8391114.1527506463.183.1544953613.1544865998.; _pk_ses.100001.8cb4=*; __utma=30149280.1646425546.1520868371.1544865995.1544953615.43; __utmt=1; __utmb=30149280.5.7.1544953615'
    referer = url
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    headers = {
        "Host": "www.douban.com",
        "Referer": referer,
        'User-Agent': agent,
        "Cookie": cookie
    }
    params = {
        "rv_comment": '🆙',
        "ck": re.findall("ck=(.*?);", headers["Cookie"])[-1],
        'start': '0',
        'submit_btn': '发送'
    }
    response = requests.get(url, headers=headers, verify=False).content.decode('utf-8')
    selector = html.fromstring(response)
    captcha_image = selector.xpath("//img[@id=\"captcha_image\"]/@src")
    if captcha_image:
        logging.info("发现验证码，下载验证码")
        captcha_id = selector.xpath("//input[@name=\"captcha-id\"]/@value")
        filename = download_captcha(captcha_image[0], agent)
        captcha_solution = recognition_captcha(filename, 1006)
        os.remove(filename)
        params['captcha-solution'] = captcha_solution
        params['captcha-id'] = captcha_id
    else:
        logging.info("没有验证码")
    response = requests.post(comment_url, headers=headers, allow_redirects=False,
                             data=params, verify=False)
    result_verification(response)


if __name__ == '__main__':
    douban_ding()
