# !/usr/bin/env python
# -*- coding:utf-8 -*-


from lagou_spider.data.start import spider_start

if __name__ == '__main__':
    keyword = input("input keyword:")
    cities = input("inptu cities:").split(" ")

    for city in cities:
        print(city)
    # spider_start()