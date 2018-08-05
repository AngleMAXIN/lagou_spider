# !/usr/bin/env python
# -*- coding:utf-8 -*-

from lagou_spider.spider import dataapi
from lagou_spider.spider import spider


def spider_start(key_word, cities=None, work_year=None):
    print("----" * 10, 2)
    small_spider = spider.Spider(key_word, cities, work_year)
    small_spider.start()
    data_api = dataapi.DateStore(key_word)
    data_api.let_save(small_spider.company_result,
                      small_spider.jobs_result, small_spider.job_requests_list)
    if data_api.save_result:
        print("---" * 10, "ok")
        return True
    return False
