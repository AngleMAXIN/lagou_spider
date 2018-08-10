# # !/usr/bin/env python
# # -*- coding:utf-8 -*-
from spider import start

# # from lagou_spider.spider.spider import Spider
# # from lagou_spider.spider.dataapi import DateStore


# # def run(id=None):
# #     spider = Spider()
# #     data = spider.get__detail_data(id)
# #     store = DateStore('example')
# #     store.insert_requests(data)

# # def test():
# #     index_list = ["industryField","financeStage"]
# #     result = {
# #     # "_id" : ObjectId("5b62d85bba88bc0dd8389f56"),
# #     "positionId" : 4942990,
# #     "salary" : "15k-25k",
# #     "firstType" : "开发|测试|运维类",
# #     "positionName" : "C++开发工程师",
# #     "education" : "本科",
# #     "workYear" : "3-5年"
# # }
# #     for i in result.items():
# #         # print(i[1])
# #         comy = {p :i[0] for p  in index_list}
# #         print(comy)

if __name__ == '__main__':
    keyword = "golang"
    cities = "全国"
    workyear = "不限"
    cities_list = cities.split(" ")
    for city in cities_list:
        print(city)
    start.spider_start(keyword, cities_list, workyear)
#     # run(4942990)
#     # test()
