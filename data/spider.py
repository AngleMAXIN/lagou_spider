# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
from . import config

class Spider(object):
    count = 0
    urls_list = []
    __company_list = []
    __jobs_list = []

    def __init__(self, data=None, cities=None):
        self.data = data
        self.cities = cities

    def __init_url(self):
        """
        根据有无提供城市选项,构造请求的url,如果没有提供,就默认在全国范围;
        如果有,就具体构造出请求的url
        """
        if self.cities is None:
            url = "https://www.lagou.com/jobs/positionAjax.json? \
                                            px=default"
            self.urls_list.append(url)
        else:
            for city in self.cities:
                url = "https://www.lagou.com/jobs/positionAjax.json? \
                        px=default&city={0}".format(city)
                self.urls_list.append(url)

    def __get_index_data(self, url=None, cookies=None):
        """
        内部方法,请求url,
        """

        proxies = {
        'http': 'http://110.73.10.186:8123',

    }
        r = requests.post(url, data=self.data,
                          headers=config.headers,
                          proxies=proxies)
        time.sleep(1)
        print(r.json())
        if r.status_code == 200:
            if r.json()['success'] is True:
                self.__data_parser(r)
            else:
                print("---------拒绝访问了-------------")
                return None

    def __data_parser(self, data):

        result = data['content']['positionResult']['result']
        for i in result:
            comy = dict(companyShortName=i['companyShortName'],
                        positionAdvantage=i['positionAdvantage'],
                        industryField=i['industryField'],
                        financeStage=i['financeStage'],
                        companySize=i['companySize'],
                        district=i['district'])

            jobs = dict(positionName=i['positionName'],
                        firstType=i['firstType'],
                        salary=i['salary'],
                        workYear=i['workYear'],
                        education=i['education'],
                        positionId=i['positionId'])

            # print("this is ----- {0} ".format(self.count))
            self.count = self.count + 1
            self.__company_list.append(comy)
            self.__jobs_list.append(jobs)

    @property
    def company_result(self):
        return self.__company_list

    @property
    def jobs_result(self):
        return self.__jobs_list

    def start(self):
        self.__init_url()
        print("----"*10,3)
        for url in self.urls_list:
            self.__get_index_data(url)
        print("-------爬取结束------")
