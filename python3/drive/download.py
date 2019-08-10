# -*- coding: UTF-8 -*-
import time
import requests
from bs4 import BeautifulSoup


def get_soup(target_url):
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    flag = True
    while flag:
        try:
            resp = requests.get(target_url, headers=headers)
            flag = False
        except Exception as e:
            print(e)
            time.sleep(0.4)
    resp.encoding = 'gb18030'
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.find('h4')
    print(title)

    for x in soup.select('.tpc_content input'):
        print(x['data-src'])


if __name__ == '__main__':
    get_soup('http://xn--5uw.ml/htm_data/1902/16/3440135.html')
