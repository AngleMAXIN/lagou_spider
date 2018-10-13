# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import time
import json
import random

import requests
from lagou_spider.conf import get_header, post_headers, get_cookie, logger
from lxml import etree


class LaGou_Spider(object):
    """
    spider of LaGou
    """
    __page_num = 30

    urls_list = []

    __company_list = []
    __jobs_list = []
    __positionId = []
    __position_result = []
    SLEEP_TIME = [1, 2, 14, 4, 5, 5.5, 11, 8, 11, 10, 9, 7, 6]

    # spider_live = True

    def __init__(self, keyword=None, cities=None, work_year=''):
        self.keyword = keyword
        self.cities = cities
        self.work_year = work_year

    def __post_index_data(self, url=None, pn=None):
        """请求url,返回json格式数据,如果返回正确结果,则继续解析数据;"""
        OVER = 2
        data = {'first': 'true', 'pn': pn, 'kd': self.keyword}
        while OVER > 0:
            result = requests.post(
                url, data=data, headers=post_headers()).json()
            OVER -= 1

            time.sleep(random.choice(self.SLEEP_TIME))
            if result['success'] is True:
                self.__data_parser(result)
                break
            else:
                print("lagou---------拒绝访问了-------------")

    def __get_detail_data(self, position_id=None):

        url = "https://www.lagou.com/jobs/{}.html".format(str(position_id))
        result = requests.get(
            url, headers=get_header, cookies=get_cookie)
        time.sleep(1)
        if result.status_code == 200:
            selector = etree.HTML(result.text)
            r = selector.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()', )
            requests_list = dict(data=r)
            return requests_list
        return None

    def __init_url(self):
        """
        根据有无提供城市选项,构造请求的url,如果没有提供,就默认在全国范围;
        如果有,就具体构造出请求的url
        """
        if self.cities[0] == "全国":
            if self.work_year == '':
                url = "https://www.lagou.com/jobs/positionAjax.json? \
                        px=default"
            else:
                url = "https://www.lagou.com/jobs/positionAjax.json? \
                        px=default&gx={0}&isSchoolJob=1".format(self.work_year)
            self.urls_list.append(url)
        else:
            for city in self.cities:
                if self.work_year == '':
                    url = "https://www.lagou.com/jobs/positionAjax.json? \
                            px=default&city={0}".format(city)
                else:
                    url = "https://www.lagou.com/jobs/positionAjax.json? \
                    px=default&gx={0}city={1}&isSchoolJob=1".format(self.work_year, city)
                self.urls_list.append(url)

    def __info_list(self):

        comy_list = ['financeStage', 'industryField']
        jobs_list = ['positionName', 'firstType',
                     'salary', 'education']
        # print(self.cities[0], self.work_year)

        if self.cities[0] == "全国":
            if self.work_year == '':
                # 全国 经验不限
                # print("全国 经验不限")
                comy_list.append('city')
                jobs_list.append('workYear')
            else:
                # 全国 应届或实习
                # print("全国 应届或实习")
                comy_list.append('city')

        else:
            if self.work_year == '':
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

    def get_post_id_data(self):
        posts_len = len(self.__positionId)
        i = 1
        print(" ")
        for post_id in self.__positionId:
            i += 1
            info = self.__get_detail_data(post_id)
            self.__position_result.append(info)
            print("\r" + "had download  {:.2%}".format(i / posts_len), end="")

    def get_urls_data(self):
        for url in self.urls_list:
            for pn in range(1, self.__page_num + 1):
                print(url, pn)
                self.__post_index_data(url, pn)

    def start(self):
        self.__init_url()
        self.get_urls_data()
        self.get_post_id_data()

    @property
    def company_result(self):
        return self.__company_list

    @property
    def jobs_result(self):
        return self.__jobs_list

    @property
    def job_requests_list(self):
        return self.__position_result


class ZhiLian_Spdier(object):
    """
    spider of zhilian
    """

    def __init__(self, keyword='', cityId=530, page=0):
        self.numfound = 120

        self.keyword = keyword
        self.cityId = cityId
        self.page = page
        self.job_info = []

    def start_spider(self):
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
        print("the --------- {0} --------".format(page + 1))
        r_json = json.loads(r)
        if r_json['code'] == 200:
            # self.numfound = r_json['data']['numFound']
            # print("******************",self.numfound)
            jobs_results_list = r_json['data']['results']
            for job_info in jobs_results_list:
                # positionURL : 详情页 / url salary : 薪酬 / updateDate : 发布时间
                # job_info['workingExp']['name'] : 经验要求 / eduLevel : 学历 / name : 职位名称
                self.job_info.append({
                    'jobName': job_info['jobName'],
                    'salary': job_info['salary'],
                    'city': job_info['city']['display'],
                    'updateDate': job_info['updateDate'],
                    'positionURL': job_info['positionURL'],
                    'eduLevel': job_info['eduLevel']['name'],
                    'workingExp': job_info['workingExp']['name']
                })
                print(
                    job_info['positionURL'],
                    job_info['salary'],
                    job_info['updateDate'],
                    job_info['workingExp']['name'],
                    job_info['eduLevel']['name'],
                    job_info['city']['display']
                )
        else:
            print("zhilian---------拒绝访问了-------------")


import grequests


class ShiXi_Spider(object):
    """
    Spider about Shixiseng
    """
    page = 2

    def __init__(self, keyword='', city=''):
        self.k = keyword
        self.city = city
        self.job_urls = []
        self.index_job_html = []
        self.res = []
        self.every_job_info = []

    def _get_jobs_list(self):
        try:
            url = "http://www.shixiseng.com/interns/st-intern_?k={0}&t=zj&p={1}"
            index_urls = [url.format(self.k, p) for p in range(1, self.page)]
            self.index_job_html = self.__grequests_api(index_urls)
            # print(self.index_job_urls[0].text)
            return True
        except Exception as e:
            logger.error("_get_jobs_list {0}".format(e))
            return False

    def __grequests_api(self, url_list):
        tasks = [grequests.get(url) for url in url_list]
        return grequests.map(tasks, size=6)

    def _parse_job_url_html(self):
        for html in self.index_job_html:
            pattern = r'<a class="name" href="(.*?)" target="_blank"'
            result = re.findall(pattern, html.text, re.S)
            url = "http://www.shixiseng.com"
            for suffix_url in result:
                parse_url = url + suffix_url
                self.job_urls.append(parse_url)
        return True

    def _parse_job_info(self):
        for html in self.res:
            try:
                # if html.status_code == 200:
                reg = r'<div class="new_job_name" title="(.*?)">'
                job_name = re.findall(reg, html.text)[0]
                reg = r'<span title="(.*?)" class="job_position">'
                job_city = re.findall(reg, html.text)[0]
                reg = r'<span class="job_academic">(.*?)</span>'
                job_edu = re.findall(reg, html.text)[0]
                self.every_job_info.append({
                    'job_name': job_name,
                    'job_city': job_city,
                    'job_limit': job_edu
                })
            except Exception as e:
                logger.error("__parse_job_info {0}".format(e))
                return False
        return True

    # def Save_Mongo(result):
    #     client = pymongo.MongoClient(MongoUrl, connect=False)
    #     db = client[MongoDB]
    #     if db[MongoTable].insert(result):
    #         print("数据存储成功")

    def start_spider(self):
        if self._get_jobs_list() and self._parse_job_url_html():
            self.res = self.__grequests_api(self.job_urls)
            if self._parse_job_info():
                logger.info(
                    "Shixiseng_spider  have pull {0} pages ,data len is {1}".format(self.page - 1,
                                                                                    len(self.every_job_info)))
                print(self.every_job_info)
                print(self.job_urls)
            return True
        return False


if __name__ == '__main__':
    spider = ShiXi_Spider("python")
    spider.start_spider()
