# !/usr/bin/env python
# -*- coding:utf-8 -*-

# from ..spider import spider, dataapi
from spider import DateStore
from spider import Spider


def spider_start(key_word=None, cities=None, work_year=''):
    print("----" * 10, "let's start!")
    small_spider = Spider(key_word, cities, work_year)
    small_spider.start()
    data_api = DateStore(key_word, work_year, cities)
    data_api.let_save(
        small_spider.company_result,
        small_spider.jobs_result,
        small_spider.job_requests_list
    )
    if data_api.save_result:
        print("---" * 10, "ok")
        return True
    return False


if __name__ == '__main__':
    keyword = "运维"
    cities = "全国"
    workyear = ''
    cities_list = cities.split(" ")
    for city in cities_list:
        print(city)
    spider_start(keyword, cities_list, workyear)
