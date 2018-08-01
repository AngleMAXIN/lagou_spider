# !/usr/bin/env python
# -*- coding:utf-8 -*-


from lagou_spider.data import spider
from lagou_spider.data import dataapi


def spider_start(key_word, cities=None):
    print("----"*10,2)
    for i in range(1, 3):
        data = {'first': 'true', 'pn': i, 'kd': key_word}
        small_spider = spider.Spider(data, cities)
        small_spider.start()
    data_api = dataapi.DateStore(key_word)
    data_api.let_save(small_spider.company_result, small_spider.jobs_result)


if __name__ == '__main__':
    cities = [u"北京", u"上海"]
    key = "c#"
    spider_start(key,cities)