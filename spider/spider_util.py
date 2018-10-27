# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import random
import re
import time

import grequests
import requests
from gevent import monkey
from lxml import etree

from .config import get_header, post_header, get_cookie, succeed_format
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
        # self.page = 5
        # 最终爬取的职位信息,元素类型为字典
        self._jobs_info_list = []
        # # 所有职位的url
        # self._jobs_url_list = []
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

    @property
    def jobs_limit_list(self):
        # 返回职位的技能要求数据
        return self._jobs_limit_list

    # @property
    # def jobs_url_list(self):
    #     # 返回职位的url
    #     return self._jobs_url_list


class LaGou_Spider(Spider):
    """
    spider of LaGou
    """
    SLEEP_TIME = [1, 2, 14, 4, 5, 5.5, 11, 8, 11, 10, 9, 7, 6]

    # spider_live = True

    def __init__(self, keyword='', cities='', employment_type="不限"):
        super().__init__(keyword, cities, employment_type)
        # self.keyword = keyword
        # self.cities = citiesn
        # self.work_year = work_year
        self.numpage = 1
        self.post_url = ""
        self.__positionId = []

    def start_spider(self):
        # 初始化url
        self.__init_url()
        # 获取数据量
        self.__get_num_page()
        for pn in range(self.numpage // 15 + 1):

            r = self._get_index_jobs_list(pn)
            self._parse_index_data(r)
            self._parse_detail_data()
        logger.info(succeed_format.format(
            self.keyword,
            self.city,
            self.employment_type,
            spider='LaGou_spider',
        ))

    def __init_url(self):
        # 根据是否实习和诚实构造post url
        base = "https://www.lagou.com/jobs/positionAjax.json?px=new"
        if self.employment_type == "实习":
            url = base + "&gx={0}&city={1}&isSchoolJob=1".format(
                self.employment_type,
                self.city)
        else:
            # 非实习
            url = base + "&city={0}".format(self.city)
        self.post_url = url

   
    def __get_num_page(self):
        res = self._get_index_jobs_list()
        number = res['content']['positionResult']['totalCount']
        self.numpage = number if number < 1000 else 1000

    def _get_index_jobs_list(self, pn=1):
        """post请求url,返回json格式数据,如果返回正确结果,则继续解析数据;"""
        OVER = 3
        data = {'first': 'true', 'pn': pn, 'kd': self.keyword}
        while OVER > 0:
            result = requests.post(
                self.post_url, data=data, headers=post_header()).json()
            OVER -= 1
            time.sleep(random.choice(self.SLEEP_TIME))
            if result['success'] is True:
                return result
            else:
                logger.warning(
                    "LaGou_Spider request failed at page {0}".format(pn))

    def _parse_index_data(self, data):
        # 解析json数据,获取每一个职位的url_id,以及每一个职位的信息
        potstion_url = "https://www.lagou.com/jobs/{0}.html"
        company_url = "https://www.lagou.com/gongsi/{0}.html"
        com_logo_url = "https://www.lgstatic.com/thumbnail_120x120/{0}"

        try:
            result = data['content']['positionResult']['result']
            for r in result:
                self.__positionId.append(r['positionId'])
                self._jobs_info_list.append(
                    'salary': r['salary'],
                    'workYear': r['workYear'],
                    'education': r['education'],
                    'jobname': r['positionName'],
                    'company_type': r['financeStage'],
                    'company_size': r['companySize'],
                    'company_name': r['companyFullName'],
                    'company_url': , company_url.format(r['companyId']),
                    'position_url': potstion_url.format(r['companyId']),
                    'companyLogo': com_logo_url.format(r['companyLogo']),
                )
        except KeyError as e:
            logger.error("Lagou_Spider _parse_index_data failed ", e)

    def _get_detail_html(self, url_list):
        html_list = []
        for url in url_list:
            html = requests.get(url, headers=get_header, cookies=get_cookie)
            if html.status_code == 200:
                html_list.append(html)
        return html_list

    def _parse_detail_data(self):
        url_list = []
        for id in self.__positionId:
            url = "https://www.lagou.com/jobs/{0}.html".format(str(id))
            url_list.append(url)
        # print(url_list)
        html_list = self._get_detail_html(url_list)

        try:
            for html in html_list:
                selector = etree.HTML(html.text)
                r = selector.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
                self._jobs_limit_list.append(dict(data=r))
        except KeyError as e:
            logger.error("Lagou_Spider __get_detail_data failed ", e)
            pass
        return None


class ZhiLian_Spdier(Spider):
    """
    spider of zhilian
    """

    def __init__(self, keyword='', cityId=530, employment_type=-1):
        # 530默认北京
        super().__init__(keyword, cityId)
        self.numfound = 2
        # -1 代表不限; 4 代表实习
        self.employment_type = -1 if employment_type == "不限" else 4
        self.city = self.__city(cityId)
        self.xpath_list = [
            '//*[@id="divMain"]/div/div/div[1]/div[2]/div[2]/div/div/p/text()',
            "//div[@class='pos-ul']/p/text()",
            "//div[@class='pos-ul']/p/span/text()",
            "//div[@class='pos-ul']/div/text()",
            "//p[@class='mt20']/text()"
        ]

    def start_spider(self):
        # 确定页数
        self._get_num_page()
        for page in range(self.numfound // 60 + 1):
            # 根据输入的页数,进行请求,并返回json结果
            r = self._get_index_jobs_list(page)
            if r is not None:
                # 如果数据不为空,解析数据,并返回没一个职位的url,再进行异步请求
                urls_list = self._parse_index_data(r)
                html_list = self._grequests_urls(urls_list)
                # 解析其中的职位要求
                self._parse_detail_html(html_list)
        # 记录日志
        logger.info(succeed_format.format(
            self.keyword,
            self.city,
            self.employment_type,
            spider='ZhiLian_spider'
        ))
        return True

    def __city(self, city):
        city_dict = {
            '全国': '489',
            '北京': '530',
            '上海': '538',
            '杭州': '653',
            '广州': '763',
            '深圳': '765'
        }
        return city_dict[city]

    def _get_num_page(self):
        res = self._get_index_jobs_list()
        number = res['data']['numFound']
        self.numfound = number if number <= 2000 else 2000

    def _get_index_jobs_list(self, page=0):
        # 使用POST方法请求
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
        r_json = json.loads(r)
        if r_json['code'] == 200:
            return r_json
        else:
            logger.warning(
                "ZhiLian_spider request failed at page {}".format(page))
            return None

    def _parse_index_data(self, r_json):
        # 解析需要的数据,并返回每一个职位信息的url
        jobs_url_list = []
        jobs_results_list = r_json['data']['results']
        try:
            for job_info in jobs_results_list:
            url = job_info['positionURL']
            jobs_url_list.append(url)
            self._jobs_info_list.append({
                'position_url': url,
                'salary': job_info['salary'],
                'jobname': job_info['jobName'],
                'city': job_info['city']['display'],
                'education': job_info['eduLevel']['name'],
                'company_name': job_info['company']['name'],
                'company_url': job_info['company']['url'],
                'company_size': job_info['company']['size']['name']
                'company_type': job_info['company']['type']['name']
                'workYear': job_info['workingExp']['name']
            })
        except KeyError as e:
            logger.error(
                "ZhiLian_Spider _parse_index_data failed {0}".format(e))
            pass
        finally:
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
        return True


class ShiXi_Spider(Spider):
    """
    Spider about Shixiseng
    """

    def __init__(self, keyword='', city='', employment_type='实习'):
        super().__init__(keyword, city, employment_type)
        self.page = 8

    def start_spider(self):

        # 获取每一个职位主页的HTML,并返回一个列表
        html_list = self._get_index_jobs_list()

        # 解析每一个html文本, 获取每一个职位信息的url,并返回一个列表
        urls_list = self._parse_index_data(html_list)

        if urls_list is not None:

            # 列表非空,使用异步请求,返回一个html的列表
            html_list = self._grequests_urls(urls_list)

            # 解析HTML中的数据,返回是否成功
            ok = self._parse_detail_html(html_list)

            if ok:

                # 整个过程成功,记录日志信息
                logger.info(succeed_format.format(
                    self.keyword,
                    self.city,
                    self.employment_type,
                    spider='Shixi_spider',
                ))
                return True

    def __init_urls(self):
        # 根据城市和关键字构造baseurl,最后通过列表推导式,生成完整的url列表
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
        # 获得职位主页url,最后进行异步请求
        index_urls = self.__init_urls()
        return self._grequests_urls(index_urls)

    def _parse_index_data(self, index_job_html):
        # 从主页职位列表中解析得每一个职位详情页的url
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
                limit = re.findall(reg, html.text, re.S)
                reg = r'"bdPic":"(.*?)"'
                com_logo = re.findall(reg, html.text)[0]
                self._jobs_info_list.append({
                    'company_name': job_com_name,
                    'company_url': com_base_url + job_com_url,
                    'position_url': base_url + job_url,
                    'jobname': job_name,
                    'city': job_city,
                    'education': job_edu,
                    'companyLogo': com_logo
                })
                self._jobs_limit_list.append(dict(data=limit))
            except Exception as e:
                logger.error("ShiXiSeng_spider parse html {0}".format(e))
                pass
        return True
