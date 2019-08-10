# -*- coding: UTF-8 -*-


# 使用 蘑菇代理
import requests

if __name__ == '__main__':
    appKey = "a0hQT1p1U3BmTENVd2ZIRTphTWZYajliNlNNQ2l0VHdW"
    ip_port = 'transfer.mogumiao.com:9001'
    proxies = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {"Proxy-Authorization": 'Basic ' + appKey,
               'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
               }
    flag = True
    while flag:
        try:
            resp = requests.get("https://baidu.com", proxies=proxies, headers=headers, verify=False)
            # if resp.status_code != 502:
            flag = False
            print(resp.text)
        except Exception as e:
            print(e)
