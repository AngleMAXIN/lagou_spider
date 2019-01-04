# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from threading import Thread,currentThread
from spider import ZhiLian_Spdier, LaGou_Spider, ShiXi_Spider
from data_api import DateStore

data_api = None

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.setDaemon(True)
        thr.start()
    return wrapper


def spider_start(key_word=None, city=None, emplo_type=''):
    '''
        key_word 职位关键字
        emplo_type　职位性质，包括实习或是非实习（不限）
        city　工作城市，包括　全国，北京，上海，杭州，深圳
    '''
    print("----" * 10, "the small spider is start!")

    start_time = time.time()
    # 初始化存储实例
    global data_api
    data_api = DateStore(key_word, emplo_type, city)
    spider_status = _spider_train(key_word, city, emplo_type)
    if spider_status:
        end_time = time.time() - start_time
        print(
            "\n -------- \n the {0} spider is over time spend {1} s \n".format(key_word, end_time))
        return True
    return False


@async
def _save_to_mongo(spider=None):
    # for spider in spider_list:
    global data_api
    print('mongo thread name is:%s\r' % currentThread().getName())

    if spider is not None:
        ok = data_api.let_save(spider.jobs_info_list, spider.jobs_limit_list)
        if ok:
            return True
        return False


def _spider_train(keyword, city, employment_type):
    _spiders = [ShiXi_Spider, ZhiLian_Spdier, LaGou_Spider]
    for spider in _spiders:
        print("{} start ...".format(spider.name))
        my_spider = spider(keyword, city, employment_type)
        ok = my_spider.start_spider()
        if ok:
            _save_to_mongo(my_spider)
    return True


if __name__ == '__main__':
    # keyword = input("input your keyword:")
    # city = input("input your ares:")
    # emplo_type = input("input your emploment type:")
    keyword = "区块链"
    city = "全国"
    emplo_type = "不限"
    spider_start(keyword, city, emplo_type)
