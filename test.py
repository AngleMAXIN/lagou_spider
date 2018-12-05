# !/usr/bin/env python
# -*- coding:utf-8 -*-

from spider.spider_util import LaGou_Spider


def test(kw,city,job_type):
    spider = LaGou_Spider(kw,city,job_type)
    spider.start_spider()
    print("-------------------------------")
    print("job number is: ",spider._get_job_number)
    print("-------------------------------")


if __name__ == '__main__':
    kw = "php"
    city = "全国"
    job_type = "不限"
    test(kw,city,job_type)