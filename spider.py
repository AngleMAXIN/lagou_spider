# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import config


class Spider():
    urls_list = []
    company_list = []
    jobs_list = []

    def __init__(self, data=None, citys=None):
        self.data = data
        self.citys = citys

    def __init_url(self):
        for city in self.citys:
            url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city={0}".format(city)
            self.urls_list.append(url)

    def __get_index_data(self, url=None, cookies=None):
        '''
        :argument url
        :argument cookies
        :return r.json()
        '''

        r = requests.post(url, data=self.data, headers=config.headers, cookies=cookies,)
        if r.status_code == 200:
            self.__data_parser(r.json())
        else:
            print("---------拒绝访问了-------------")
            return None

    def __data_parser(self, data):
        count = 0
        print(data)
        result = data['content']['positionResult']['result']

        for i in result:
            comy = dict(companyShortName=i['companyShortName'],
                        positionAdvantage=i['positionAdvantage'],
                        industryField=i['industryField'],
                        financeStage=i['financeStage'],
                        companySize=i['companySize'],
                        district=i['district'])

            jobs = dict(firstType=i['firstType'],
                        salary=i['salary'],
                        workYear=i['workYear'],
                        education=i['education'],
                        positionId=i['positionId'])

            print("this is ----- {0} ".format(count))
            count = count + 1
            self.company_list.append(comy)
            self.jobs_list.append(jobs)

    @property
    def company_result(self):
        return self.company_list

    @property
    def jobs_result(self):
        return self.jobs_list

    def start(self):
        self.__init_url()
        for url in self.urls_list:
            self.__get_index_data(url)
        print("-------爬取结束------")



