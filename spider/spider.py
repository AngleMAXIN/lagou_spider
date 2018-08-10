# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time

import requests

from . import config
from lxml import etree


class Spider(object):
    # count = 0
    __page_num = 2
    urls_list = []
    __company_list = []
    __jobs_list = []
    __positionId = []
    __positionresult = []
    spider_live = True

    def __init__(self, keyword=None, cities=None, workyear=None):
        self.keyword = keyword
        self.cities = cities
        self.work_year = workyear

    def __post_index_data(self, url=None, pn=None):
        """
        请求url,返回json格式数据,如果返回正确结果,则继续解析数据;
        否则就拒绝访问
        """
        OVER = 2
        data = {'first': 'true', 'pn': pn, 'kd': self.keyword}
        while OVER > 0:
            result = requests.post(
                url, data=data, headers=config.get_header()).json()
            OVER -= 1
            time.sleep(2)
            if result['success'] is True:
                self.__data_parser(result)
                break
            else:
                print("---------拒绝访问了-------------")

    def __get_detail_data(self, position_id=None):

        url = "https://www.lagou.com/jobs/{}.html".format(str(position_id))
        result = requests.get(
            url, headers=config.get_headers, cookies=config.get_cookies)
        time.sleep(1)
        if result.status_code == 200:
            selector = etree.HTML(result.text)
            r = selector.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
            requests_list = dict(data=r)

            return requests_list

        return None

    def __init_url(self):
        """
        根据有无提供城市选项,构造请求的url,如果没有提供,就默认在全国范围;
        如果有,就具体构造出请求的url
        """
        if self.cities[0] == "全国":
            url = "https://www.lagou.com/jobs/positionAjax.json? \
                                            px=default"
            self.urls_list.append(url)
        else:
            for city in self.cities:
                if self.work_year is "不限":
                    url = "https://www.lagou.com/jobs/positionAjax.json? \
                            px=default&city={0}".format(city)
                else:
                    url = "https://www.lagou.com/jobs/positionAjax.json? \
                    px=default&gx={0}ity={1}isSchoolJob=1".format(self.work_year, city)
                self.urls_list.append(url)

    def __info_list(self):
        """"""
        comy_list = ['financeStage', 'industryField']
        jobs_list = ['positionName', 'firstType',
                     'salary', 'education']
        print("-----",self.work_year,self.cities)
        if self.cities[0] == "全国":
            if self.work_year == "不限":
                # 全国 经验不限
                print("全国 经验不限")
                comy_list.append('city')
                jobs_list.append('workYear')
            else:
                # 全国 应届或实习
                print("全国 应届或实习")
                comy_list.append('city')

        else:
            if self.work_year == "不限":
                # 指定地区 经验不限
                jobs_list.append('workYear')
            # else:
            # 指定地区 应届或实习

        return comy_list, jobs_list

    def __data_parser(self, data):
        """
        接受请求返回的正确格式的数据,并一步获取需要的数据
        """
        result = data['content']['positionResult']['result']
        comy_list, jobs_list = self.__info_list()
        for r in result:
            comy = {key: r[key] for key in comy_list}
            jobs = {key: r[key] for key in jobs_list}
            position_id = r['positionId']

            self.__positionId.append(position_id)
            self.__company_list.append(comy)
            self.__jobs_list.append(jobs)

    def get_postId_data(self):

        for post_id in self.__positionId:
            print("---" * 10, post_id)
            info = self.__get_detail_data(post_id)
            self.__positionresult.append(info)

    def get_urls_data(self):
        for url in self.urls_list:
            for pn in range(1, self.__page_num + 1):
                print("----" * 10, url, pn)
                self.__post_index_data(url, pn)

    def start(self):
        self.__init_url()
        self.get_urls_data()
        self.get_postId_data()

    @property
    def company_result(self):
        return self.__company_list

    @property
    def jobs_result(self):
        return self.__jobs_list

    @property
    def job_requests_list(self):
        return self.__positionresult

    
