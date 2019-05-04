# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib3


urllib3.disable_warnings()


if __name__ == '__main__':

    # 蘑菇代理的隧道订单
    appKey = "a0hQT1p1U3BmTENVd2ZIRTphTWZYajliNlNNQ2l0VHdW"

    # 蘑菇隧道代理服务器地址
    ip_port = 'transfer.mogumiao.com:9001'

    # 准备去爬的 URL 链接
    # url = 'https://ip.cn'
    url = 'https://www.liaoxuefeng.com/wiki/1016959663602400'

    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {"Proxy-Authorization": 'Basic ' + appKey,
               'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
               }
    r = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup)
    # print(soup.select(".well p")[0].text)
    # if r.status_code == 302 or r.status_code == 301:
    #     loc = r.headers['Location']
    #     url_f = "https://ip.cn" + loc
    #     print(loc)
    #     r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    #     print(r.status_code)
    #     print(r.text)
