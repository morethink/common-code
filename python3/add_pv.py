# -*- coding: UTF-8 -*-
import time

import requests
from selenium import webdriver

if __name__ == '__main__':
    # 要访问的目标页面
    targetUrl = "https://juejin.im/post/5c37506ee51d455023417d0d"
    # headers = {'User-Agent':
    #                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    # requests.get(targetUrl, headers=headers)

    options = webdriver.ChromeOptions()
    # 设置成中文
    options.add_argument('lang=zh_CN.UTF-8')
    # 添加头部
    options.add_argument(
        '"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"')
    driver = webdriver.PhantomJS(chrome_options=options)

    # driver = webdriver.Chrome()
    # driver.get("https://httpbin.org/user-agent")
    driver.get(targetUrl)
    time.sleep(7)
    driver.page_source.encode("utf-8")
    print(driver.title)
    print(driver.current_url)
    driver.quit()
