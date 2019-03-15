# -*- coding: UTF-8 -*-
import random

import requests
from bs4 import BeautifulSoup


def is_available(proxy):
    url = 'https://www.baidu.com/'
    proxies = {
        "http": proxy,
        "https": proxy
    }
    try:
        s = requests.get(url, proxies=proxies, timeout=5)
        print(s)
        return True
    except Exception as e:
        print(e)
    return False


def get_ip():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
    url = 'https://www.kuaidaili.com/free/intr/'
    s = requests.get(url, headers=headers)
    soup = BeautifulSoup(s.text, 'html.parser')
    proxys = list()
    for i in soup.select('#list tr')[1:]:
        ip = i.select('td')
        proxy = 'https://' + ip[0].text + ':' + ip[1].text
        if is_available(proxy):
            proxys.append(proxy)
    return proxys


if __name__ == "__main__":
    # proxys = get_ip()
    # print(proxys)
    #
    #
    # print(random.sample(proxys, 1)[0])
    # print(random.sample(proxys, 1))
    # print(random.sample(proxys, 1)[0])
    # print(random.sample(proxys, 1)[0])
    # print(random.sample(proxys, 1)[0])
    # print(random.sample(proxys, 1)[0])
    # proxies = {
    #       "http": random.sample(proxys, 1)[0],
    #       "https": random.sample(proxys, 1)[0]
    #   }
    proxies = {
        "http": 'http://115.223.118.185:25331',
        "https": 'http://115.223.118.185:25331'
    }
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    # proxies = {'proxy ': 'http://119.101.112.57:9999'}
    r = requests.get('https://www.morethink.cn', proxies=proxies, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup)
    print(soup.select(".well p")[0].text)
