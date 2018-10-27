# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from spider import ZhiLian_Spdier, LaGou_Spider, ShiXi_Spider
from data_api import LaGouDateStore


def spider_start(key_word=None, cities=None, work_year=''):
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

    small_spider = Spider(key_word, cities, work_year)
    small_spider.start()

    data_api = DateStore(key_word, work_year, cities)
    data_api.let_save(
        small_spider.company_result,
        small_spider.jobs_result,
        small_spider.job_requests_list
    )

    if data_api.save_result:
        end_time = time.time() - start_time
        print(
            "\n -------- \n the {0} spider is over time consuming {1} s \n --------".format(key_word, end_time))
        return True
    return False

def _save_to_mongo(spider_list):
    for spider in spider_list:
        

def _spider_train(keyword,city,employment_type):
    _spiders = [LaGou_Spider,ZhiLian_Spdier,ShiXi_Spider]

    for spider in _spiders:
        spider(keyword,city, employment_type)
        spider.start_spider()

    return _spiders

if __name__ == '__main__':
    keyword = input("input your keyword:")
    cities = input("input your ares:")
    work_year = '不限'
    cities_list = cities.split(" ")
    # for city in cities_list:
    #     print(city)
    spider_start(keyword, cities_list, work_year)
