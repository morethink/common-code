import time
import pdfkit
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()


# 使用 蘑菇代理
def get_soup(target_url):
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
            resp = requests.get(target_url, proxies=proxies, headers=headers, verify=False, allow_redirects=False,
                                timeout=1)
            flag = False
        except Exception as e:
            print(e)

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
    title = soup.select(".x-content h4")[0]
    new_title = BeautifulSoup('<h' + depth + '>' + title.string + '</h' + depth + '>', 'html.parser')
    print(new_title)
    # 加载图片
    images = soup.find_all('img')
    for x in images:
        x['src'] = x['data-src']

    div_content = soup.find('div', class_='x-wiki-content')
    return new_title, div_content


def convert_pdf(template):
    html_file = "python-tutorial-pdf.html"
    with open(html_file, mode="w", encoding="utf8") as code:
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
