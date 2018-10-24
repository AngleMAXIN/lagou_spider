# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import random
import re
import time

import gevent
import grequests
import requests
from gevent import monkey
from lxml import etree

from .config import get_header, post_headers, get_cookie, succeed_format
from .log import logger

monkey.patch_all()


class Spider(object):
    """docstring for  Spider"""

    def __init__(self, keyword='', city='', employment_type=None):
        self.keyword = keyword
        self.city = city
        # 工作性质,诸如 不限 / 实习
        self.employment_type = employment_type

        # 页数
        self.page = 5
        # 最终爬取的职位信息,元素类型为字典
        self._jobs_info_list = []
        # 所有职位的url
        self._jobs_url_list = []
        # 所有的职位技能信息
        self._jobs_limit_list = []

    def start_spider(self):
        '''
            开启爬虫
        '''
        pass

    def init_urls(self):
        '''
        初始化url,包括首页url以及每一个职位url
        :return:
        '''
        pass

    def _parse_index_data(self):
        '''
        解析首页数据,拉钩和智联属于解析json,实习僧属于解析html
        :return:
        '''

    def _parse_detail_html(self):
        '''
        解析每一页的职位信息
        '''
        pass

    def _get_index_jobs_list(self, url):
        '''
        根据首页的url,获取每一页所有职位的url以及职位名称,薪资,经验,学历
        '''
        pass

    def _grequests_urls(self, jobs_url_list):
        # 只对职位的url进行异步爬取,所以只用self._jobs_url_list
        task = [grequests.get(url) for url in jobs_url_list]
        return grequests.map(task, size=6)

    @property
    def jobs_info_list(self):
        # 返回最终职位数据
        return self._jobs_info_list

    # @property
    # def jobs_url_list(self):
    #     # 返回职位的url
    #     return self._jobs_url_list

    @property
    def jobs_limit_list(self):
        # 返回职位的技能要求数据
        return self._jobs_limit_list


class LaGou_Spider(Spider):
    """
    spider of LaGou
    """
    __page_num = 30
    SLEEP_TIME = [1, 2, 14, 4, 5, 5.5, 11, 8, 11, 10, 9, 7, 6]

    # spider_live = True

    def __init__(self, keyword='', cities='', work_year=''):
        super().__init__(keyword, cities)
        # self.keyword = keyword
        # self.cities = cities
        self.work_year = work_year

        self.urls_list = []
        self.__company_list = []
        self.__jobs_list = []
        self.__positionId = []
        self.__position_result = []

    def __post_index_data(self, url=None, pn=None):
        """post请求url,返回json格式数据,如果返回正确结果,则继续解析数据;"""
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


class ZhiLian_Spdier(Spider):
    """
    spider of zhilian
    """

    def __init__(self, keyword='', cityId=530, employment_type=-1):
        # 530默认北京
        super().__init__(keyword, cityId, employment_type)
        self.numfound = 0
        self.city = self.__city(cityId)
        self.job_info = []
        self._jobs_url_list = []

        self.xpath_list = [
            '//*[@id="divMain"]/div/div/div[1]/div[2]/div[2]/div/div/p',
            "//div[@class='pos-ul']/p/text()",
            "//div[@class='pos-ul']/p/span/text()",
            "//div[@class='pos-ul']/div/text()",
            "//p[@class='mt20']/text()"
        ]

    def start_spider(self):
        # 确定页数
        self._get_num_page()
        for page in range(2):
            r = self._get_index_jobs_list(page)
            if r is not None:
                urls_list = self._parse_index_data(r)
        html_list = self._grequests_urls(urls_list)
        if self._parse_detail_html(html_list):
            logger.info(succeed_format.format(
                self.keyword,
                self.city,
                self.employment_type,
                spider='ZhiLian_spider',
            ))
        return

    def __city(self,city):
        city_dict = {
            '全国':'489',
            '北京':'530',
            '上海':'538',
            '杭州':'653',
            '广州':'763',
            '深圳':'765'
        }
        return city_dict[city]

    def _get_num_page(self):
        res = self._get_index_jobs_list()
        self.numfound = res['data']['numFound']

    def _get_index_jobs_list(self, page=0):
        url = "https://fe-api.zhaopin.com/c/i/sou"
        payload = {
            'employmentType': self.employment_type,
            'pageSize': 60,
            'cityId': self.city,  # city id
            'education': -1,
            'kw': self.keyword,  # keyword
            'kt': 3,
            'start': 0 + 60 * page  # next page
        }

        r = requests.get(url, params=payload).text
        print("the --------- {0} --------".format(page + 1))

        r_json = json.loads(r)

        if r_json['code'] == 200:
            return r_json
        else:
            logger.warning("ZhiLian_spider request failed")
            return None

    def _parse_index_data(self, r_json):
        jobs_url_list = []
        jobs_results_list = r_json['data']['results']
        for job_info in jobs_results_list:
            # positionURL : 详情页
            # url salary : 薪酬
            # updateDate : 发布时间
            # workingexp : 经验要求
            # eduLevel : 学历
            # name : 职位名称
            # city : 城市
            # company_name : 公司名称
            url = job_info['positionURL']

            jobs_url_list.append(url)
            self._jobs_info_list.append({
                'positionurl': url,
                'salary': job_info['salary'],
                'jobname': job_info['jobName'],
                'city': job_info['city']['display'],
                'updatedate': job_info['updateDate'],
                'edulevel': job_info['eduLevel']['name'],
                'companyname': job_info['company']['name'],
                'company_url':job_info['company']['url'],
                'workingexp': job_info['workingExp']['name']    
            })
        return jobs_url_list

    def _parse_detail_html(self, html_list):
        # 使用xpath对html进行解析
        for html in html_list:
            selector = etree.HTML(html.text)
            for x_str in self.xpath_list:
                r = selector.xpath(x_str)
                if len(r) != 0:
                    self._jobs_limit_list.append(dict(data=r))
                    break
        del(self.xpath_list)
        return True

    @property
    def time_xpath_api(self):
        return self.numfound, self.city


class ShiXi_Spider(Spider):
    """
    Spider about Shixiseng
    """

    def __init__(self, keyword='', city='', employment_type='实习'):
        self.k = keyword
        super().__init__(keyword, city, employment_type)
        self.page = 2

    def start_spider(self):
        html_list = self._get_index_jobs_list()
        urls_list = self._parse_index_data(html_list)
        if urls_list is not None:
            html_list = self._grequests_urls(urls_list)
            print(len(html_list))
            ok = self._parse_detail_html(html_list)
            if ok:
                logger.info(succeed_format.format(
                    self.keyword,
                    self.city,
                    self.employment_type,
                    spider='Shixi_spider',
                ))
                return True

    def __init_urls(self):
        city_dict = {
            "不限": "",
            "北京": "110100",
            "上海": "310100",
            "广州": "440100",
            "深圳": "440300",
            "杭州": "330100"
        }
        url = "http://www.shixiseng.com/interns/st-intern_c-" + \
            city_dict[self.city] + "?k=" + self.keyword + "&t=zj&p={0}&t=zj"
        return [url.format(p) for p in range(1, self.page)]

    def _get_index_jobs_list(self):
        index_urls = self.__init_urls()
        return self._grequests_urls(index_urls)

    def _parse_index_data(self, index_job_html):
        jobs_url_list = []
        if index_job_html is not None:
            for html in index_job_html:
                pattern = r'<a class="name" href="(.*?)" target="_blank"'
                result = re.findall(pattern, html.text, re.S)
                base_url = "http://www.shixiseng.com"
                if len(result) != 0:
                    for url in result:
                        jobs_url_list.append(base_url + url)
                else:
                    break
            return jobs_url_list
        return None

    def _parse_detail_html(self, res):
        base_url = "http://www.shixiseng.com"
        com_base_url = "https://www.shixiseng.com/com/"
        for html in res:
            try:
                reg = r'<a href="/company/detail/(.*?)" target="_blank" class="com-con">'
                job_com_url = re.findall(reg, html.text)[0]
                reg = r'<div class="job_com_name">(.*?)</div>'
                job_com_name = re.findall(reg, html.text)[0]
                reg = r'next=(.*?)" target="_blank" data-sa="click"'
                job_url = re.findall(reg, html.text)[0]
                reg = r'<div class="new_job_name" title="(.*?)">'
                job_name = re.findall(reg, html.text)[0]
                reg = r'<span title="(.*?)" class="job_position">'
                job_city = re.findall(reg, html.text)[0]
                reg = r'<span class="job_academic">(.*?)</span>'
                job_edu = re.findall(reg, html.text)[0]
                reg = r'<div class="job_detail">(.*?)</div>'
                limit = re.findall(reg, html.text,re.S)[0]
                reg = r'"bdPic":"(.*?)"'
                com_logo = re.findall(reg,html.text)[0]
                self._jobs_info_list.append({
                    'companyname': job_com_name,
                    'company_url': com_base_url + job_com_url,
                    'positionurl': base_url + job_url,
                    'jobname': job_name,
                    'city': job_city,
                    'edulevel': job_edu,
                    'limit': limit ,
                    'com_logo':com_logo
                })
            except Exception as e:
                logger.error("ShiXiSeng_spider parse html {0}".format(e))
                return False
        return True
