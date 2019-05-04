# -*- coding: UTF-8 -*-
import re
import time
import pdfkit
import requests
from bs4 import BeautifulSoup


# 使用 阿布云代理
def get_soup(target_url):
    proxy_host = "http-dyn.abuyun.com"
    proxy_port = "9020"
    proxy_user = "HKQL6V46321071VD"
    proxy_pass = "1759D9C2F6DE34B3"
    proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_user,
        "pass": proxy_pass,
    }

    proxies = {
        "http": proxy_meta,
        "https": proxy_meta,
    }
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    flag = True
    while flag:
        try:
            resp = requests.get(target_url, proxies=proxies, headers=headers)
            flag = False
        except Exception as e:
            print(e)
            time.sleep(0.4)

    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def get_toc(url):
    soup = get_soup(url)
    toc = soup.select("#x-wiki-index a")
    print(toc[0]['href'])
    return toc


# ⬇️教程html
def download_html(url, depth):
    soup = get_soup(url)
    # 处理目录
    if int(depth) <= 1:
        depth = '1'
    elif int(depth) >= 2:
        depth = '2'
    title = soup.select("#x-content h4")[0]
    new_a = soup.new_tag('a', href=url)
    new_a.string = title.string
    new_title = soup.new_tag('h' + depth)
    new_title.append(new_a)
    print(new_title)
    # 加载图片
    images = soup.find_all('img')
    for x in images:
        x['src'] = 'https://static.liaoxuefeng.com/' + x['data-src']
    # 将bilibili iframe 视频更换为链接地址
    iframes = soup.find_all('iframe', src=re.compile("bilibili"))
    for x in iframes:
        x['src'] = "http:" + x['src']
        a_tag = soup.new_tag("a", href=x['src'])
        a_tag.string = "vide play:" + x['src']
        x.replace_with(a_tag)

    div_content = soup.find('div', class_='x-wiki-content')
    return new_title, div_content


def convert_pdf(template):
    html_file = "python-tutorial-pdf.html"
    with open(html_file, mode="w") as code:
        code.write(str(template))
    pdfkit.from_file(html_file, 'python-tutorial-pdf.pdf')


if __name__ == '__main__':
    # html 模板
    template = BeautifulSoup(
        '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <link rel="stylesheet" href="https://cdn.liaoxuefeng.com/cdn/static/themes/default/css/all.css?v=bc43d83"> <script src="https://cdn.liaoxuefeng.com/cdn/static/themes/default/js/all.js?v=bc43d83"></script> </head> <body> </body> </html>',
        'html.parser')
    # 教程目录
    toc = get_toc('https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000')
    for i, x in enumerate(toc):
        url = 'https://www.liaoxuefeng.com' + x['href']
        # ⬇️教程html
        content = download_html(url, x.parent['depth'])
        # 往template添加新的教程
        new_div = template.new_tag('div', id=i)
        template.body.insert(3 + i, new_div)
        new_div.insert(3, content[0])
        new_div.insert(3, content[1])
        time.sleep(0.4)
    convert_pdf(template)
