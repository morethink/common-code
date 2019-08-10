# -*- coding: UTF-8 -*-
import json
import threading
import time

import pymongo as pymongo
import requests
import re

import sys

reload(sys)
sys.setdefaultencoding('utf8')


def find_product_id(key_word):
    jd_url = 'https://search.jd.com/Search'
    product_ids = []
    # 爬前3页的商品
    for i in range(1, 4):
        param = {'keyword': key_word, 'enc': 'utf-8', 'page': i}
        headers = {'User-Agent':
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        response = requests.get(jd_url, params=param, headers=headers)
        # 商品id
        ids = re.findall('data-pid="(.*?)"', response.text, re.S)
        product_ids += ids
    return product_ids


"""
获取评论内容
"""


def get_comment_message(product_id):
    urls = ['https://sclub.jd.com/comment/productPageComments.action?' \
            'callback=fetchJSON_comment98vv21&' \
            'productId={}' \
            '&score=0&sortType=5&' \
            'page={}' \
            '&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(product_id, page) for page in range(1, 11)]
    for url in urls:
        headers = {'Referer': 'https://item.jd.com/' + product_id + '.html',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                   'cookie': '__jdu=15582763997996387168; shshshfpb=1cb7b06261b1042249141f311bee5ef3181c2cfbb9fbca2ab5ad5f6736; shshshfpa=7e1dcff0-5c9c-55a2-36cb-ab3c4d6ff16f-1558276402; pinId=L5tgEyENOgJKilrJ2ray5g; qrsc=3; TrackID=1IHaEYXAmUoFDzt96M1pKQ-CAMFklczcZqBWboVR_C9cVWsm-UcqnVhUOhbNnl4m0Yx0_M2ak-O0SlV2pG5y3dtyEpL8SyjD_c3uGz-ADecotfptjQ2JJx9doe0a67M6w; PCSYCityID=CN_310000_310100_310114; xtest=3908.cf6b6759; UM_distinctid=16c5192dfaba9-015f4cbe58c848-37637c02-fa000-16c5192dfac56; rkv=V0100; areaId=2; __jdv=76161171|click.linktech.cn|t_4_A100221402|tuiguang|10fbbdf0333f43979703b8830d303f51|1564837418811; __jda=122270672.15582763997996387168.1558276400.1564736654.1564837419.9; __jdc=122270672; 3AB9D23F7A4B3C9B=KWWCLKC24Z4UBYAC6W3IDIUUBSB2K3L3Q4GW7TW5NH4ZTQ52V3CXMJHYERPEKGBTZOPZMWSFQMDTFJ5UUWXVNLLSTA; CNZZDATA1256793290=1822694398-1559896179-https%253A%252F%252Fwww.google.com%252F%7C1564833272; shshshfp=18bfad6b353b5e5ddf75966cfa5d3b08; ipLoc-djd=2-2826-51941-0; shshshsID=2f12c64bc687e5adeb446330f6a704e5_9_1564838815634; __jdb=122270672.9.15582763997996387168|9.1564837419'
                   }
        print(url)
        response = requests.get(url, headers=headers)
        html = response.text
        # 删除无用字符
        print('ll' + html)
        html = html.replace('fetchJSON_comment98vv21(', '').replace(');', '')
        data = json.loads(html)
        comments = data['comments']
        time.sleep(3)
        t = threading.Thread(target=save_mongo, args=(comments,))
        t.start()


def flush_data(data):
    if '肤' in data:
        return '肤色'
    if '黑' in data:
        return '黑色'
    if '紫' in data:
        return '紫色'
    if '粉' in data:
        return '粉色'
    if '蓝' in data:
        return '蓝色'
    if '白' in data:
        return '白色'
    if '灰' in data:
        return '灰色'
    if '槟' in data:
        return '香槟色'
    if '琥' in data:
        return '琥珀色'
    if '红' in data:
        return '红色'
    if '紫' in data:
        return '紫色'
    if 'A' in data:
        return 'A'
    if 'B' in data:
        return 'B'
    if 'C' in data:
        return 'C'
    if 'D' in data:
        return 'D'


#  保存mongo
def save_mongo(comments):
    # mongo服务
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    # jd数据库
    db = client.jd
    # product表,没有自动创建
    product_db = db.product
    for comment in comments:
        product_data = {}
        # 颜色
        # flush_data清洗数据的方法
        product_data['product_color'] = flush_data(comment['productColor'])
        # size
        product_data['product_size'] = flush_data(comment['productSize'])
        # 评论内容
        product_data['comment_content'] = comment['content']
        # create_time
        product_data['create_time'] = comment['creationTime']
        # 插入mongo
        product_db.insert(product_data)


# 获取评论线程
def spider_jd(ids):
    while ids:
        # 加锁
        lock.acquire()
        # 取出第一个元素
        id = ids[0]
        # 将取出的元素从列表中删除，避免重复加载
        del ids[0]
        # 释放锁
        lock.release()
        # 获取评论内容
        get_comment_message(id)


if __name__ == '__main__':
    # 创建一个线程锁
    lock = threading.Lock()

    product_ids = find_product_id('胸罩')
    print(product_ids)
    for i in (1, 5):
        # 增加一个获取评论的线程
        t = threading.Thread(target=spider_jd, args=(product_ids,))
        # 启动线程
        t.start()
