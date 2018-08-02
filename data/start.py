# !/usr/bin/env python
# -*- coding:utf-8 -*-

from lagou_spider.data import dataapi
from lagou_spider.data import spider


def spider_start(key_word, cities=None):
    print("----" * 10, 2)
    small_spider = spider.Spider(key_word, cities)
    small_spider.start()
    data_api = dataapi.DateStore(key_word)
    data_api.let_save(small_spider.company_result, small_spider.jobs_result)
    if data_api.save_result:
        print("---" * 10, "ok")
