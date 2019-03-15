# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    # 蘑菇代理的隧道订单
    appKey = "Njd5NmpLQzVnQmhKMEhjczowWGZwdTlxY2dWU29UVTFr"

    # 蘑菇隧道代理服务器地址
    ip_port = 'transfer.mogumiao.com:9001'

    # 准备去爬的 URL 链接
    url = 'https://ip.cn'

    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {"Proxy-Authorization": 'Basic ' + appKey}
    r = requests.get("https://ip.cn", headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.select(".well p")[0].text)
    # if r.status_code == 302 or r.status_code == 301:
    #     loc = r.headers['Location']
    #     url_f = "https://ip.cn" + loc
    #     print(loc)
    #     r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
    #     print(r.status_code)
    #     print(r.text)
