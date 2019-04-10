# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    proxies = {
        "http": 'http://127.0.0.1:1081',
        "https": 'http://127.0.0.1:1081'
    }
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    r = requests.get('https://d.ishadowx.com/', headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.select(".hover-text")[0])
    print(soup.select(".hover-text")[1])
    # print(soup.select(".well p")[0].text)
