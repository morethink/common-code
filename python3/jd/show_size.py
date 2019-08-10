# -*- coding: UTF-8 -*-
import pymongo
from pylab import *


if __name__ == '__main__':
    index = ["A", "B", "C", "D"]

    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.jd
    product_db = db.product

    value = []
    for i in index:
        num = product_db.count({'product_size': i})
        value.append(num)

    plt.bar(index, height=value, color="green", width=0.5)

    plt.show()
