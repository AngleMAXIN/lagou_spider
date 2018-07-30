# !/usr/bin/env python
# -*- coding:utf-8 -*-

from spider import Spider
from dataapi import DateStore

def spider_start(key_word,end_page):
    citys = [u"北京", u"上海", u"杭州", u"广州", u"深圳"]
    for i in range(1,end_page):
        data = {'first':'true','pn': i, 'kd': key_word}
        spider = Spider(data, citys)
        spider.start()
    data_api = DateStore()
    data_api.let_save(spider.company_list,spider.jobs_list)


if __name__ == '__main__':
    key_word = "docker"
    end_page = 2
    spider_start(key_word,end_page)
    print("------ok--------")