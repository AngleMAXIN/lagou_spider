# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests

from . import config


class Spider(object):
    count = 0
    urls_list = []
    __company_list = []
    __jobs_list = []
    __page_num = 10

    def __init__(self, keyword=None, cities=None):
        self.keyword = keyword
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

    def __post_index_data(self, url=None, pn=None):
        """
        请求url,返回json格式数据,如果返回正确结果,则继续解析数据;
        否则就拒绝访问
        """

        #     proxies = {
        #     'http': 'http://114.222.24.111:808',
        #
        # }
        data = {'first': 'true', 'pn': pn, 'kd': self.keyword}
        result = requests.post(url, data=data, headers=config.headers).json()
        time.sleep(1)
        if result['success'] is True:
            self.__data_parser(result)
        else:
            print("---------拒绝访问了-------------")
            return None

    def __data_parser(self, data):
        """
        接受请求返回的正确格式的数据,并一步步获取需要的数据
        """
        result = data['content']['positionResult']['result']
        for i in result:
            comy = dict(
                companyShortName=i['companyShortName'],
                positionAdvantage=i['positionAdvantage'],
                industryField=i['industryField'],
                financeStage=i['financeStage'],
                companySize=i['companySize'],
                district=i['district']
            )

            jobs = dict(
                positionName=i['positionName'],
                firstType=i['firstType'],
                salary=i['salary'],
                workYear=i['workYear'],
                education=i['education'],
                positionId=i['positionId']
            )

            print("this is ----- {0} ".format(self.count))
            self.count += 1
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
        # print("----" * 10, 3)
        for url in self.urls_list:
            for pn in range(1, self.__page_num + 1):
                self.__post_index_data(url, pn)
        # print("-------爬取结束------")
