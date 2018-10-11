# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json


class Spdier(object):
    """docstring for Spdier"""

    def __init__(self):
        self.numfound = 120

    def spider_start_api(self, keyword='', cityId=530, page=0):
        self.keyword = keyword
        self.cityId = cityId
        self.page = page

        for page_number in range(4):
            # print("===============",self.numfound//60)
            self.__get_jobs_list(page_number)

    def __get_jobs_list(self, page=0):

        url = "https://fe-api.zhaopin.com/c/i/sou"
        payload = {'pageSize': 60,
                   'cityId': self.cityId,  # city id
                   'education': -1,
                   'kw': self.keyword,  # keyword
                   'kt': 3,
                   'start': 0 + 60 * page}  # next page

        r = requests.get(url, params=payload).text
        print("the --------- {0} --------".format(page))
        r_json = json.loads(r)
        if r_json['code'] == 200:
            # self.numfound = r_json['data']['numFound']
            # print("******************",self.numfound)
            jobs_results_list = r_json['data']['results']
            for job_info in jobs_results_list:
                print(job_info['positionURL'], job_info['salary'], job_info['updateDate'],
                      job_info['workingExp']['name'], job_info['eduLevel']['name'])
        else:
            print("zhilian---------拒绝访问了-------------")


if __name__ == '__main__':
    spider = Spdier()
    spider.spider_start_api('java开发工程师')
