# !/usr/bin/env python
# -*- coding:utf-8 -*-


from lagou_spider.data.start import spider_start

if __name__ == '__main__':
    keyword = input("input keyword:")
    cities = input("inptu cities:")
    if cities == "全国":
        cities_list = None
    else:
        cities_list = cities.split(" ")
    for city in cities_list:
        print(city)
    spider_start(keyword, cities_list)