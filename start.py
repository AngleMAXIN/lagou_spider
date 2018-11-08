# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from spider import ZhiLian_Spdier, LaGou_Spider, ShiXi_Spider ,Spider
from data_api import DateStore


def spider_start(key_word=None, city=None, emplo_type=''):
    '''
    Function: spider_start
    Summary:   start spider then save data to MongoDB
    Examples: InsertHere
    Attributes: 
        @param (key_word) default=None: InsertHere
        @param (cities) default=None: InsertHere
        @param (work_year) default='': InsertHere
    Returns: InsertHere
    '''
    print("----" * 10, "the small spider is start!")

    start_time = time.time()

    data_api = DateStore(key_word, emplo_type, city)
    spider_list = _spider_train(key_word, city, emplo_type)
    ok = _save_to_mongo(data_api, spider_list)
    if ok:
        end_time = time.time() - start_time
        print(
            "\n -------- \n the {0} spider is over time spend {1} s \n".format(key_word, end_time))
        return True
    return False


def _save_to_mongo(mongo, spider_list):
    _succeed = 0
    for spider in spider_list:
        ok = mongo.let_save(spider.jobs_info_list, spider.jobs_limit_list)
        if ok:
            _succeed += 1
    if _succeed == 3:
        return True
    return False


def _spider_train(keyword, city, employment_type):
    _spiders = [LaGou_Spider, ZhiLian_Spdier, ShiXi_Spider]
    my_spider  = Spider()
    spider_list = []
    i = 0
    for spider in _spiders:
        print("spider start ",i)
        my_spider = spider(keyword, city, employment_type)
        my_spider.start_spider()
        spider_list.append(my_spider)
    return spider_list


if __name__ == '__main__':
    keyword = input("input your keyword:")
    city = input("input your ares:")
    emplo_type = input("input your emploment type:")

    spider_start(keyword, city, emplo_type)
