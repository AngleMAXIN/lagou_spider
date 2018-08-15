# !/usr/bin/env python
# -*- coding:utf-8 -*-

import jieba

from pymongo import MongoClient

from collections import Counter


class GetData(object):

    word_string = ''
    __salary = []
    __work_year = []
    __education = []
    __district = []
    __req_data = []
    __comp_keys = ['city']
    __jobs_keys = ['salary', 'workYear', 'education']
    words = ['岗位职责', '熟练掌握', '解决方案', '以上学历', '岗位要求']

    def __init__(self, keyword):
        MONGO_URL = '127.0.0.1:27017'
        client = MongoClient(MONGO_URL)
        self.db = client['job_info']
        self.colle = self.db[keyword + '_coll_job']
        self.colle_com = self.db[keyword + '_coll_company']
        self.colle_req = self.db[keyword + '_coll_requests']

    def filed_api(self, filed_list):
        for filed in filed_list:
            self.__count_data(self.__get_data(filed), filed)

    def __get_data(self, key):
        filed = {'_id': False, key: True}
        # collect = None
        if key in self.__comp_keys:
            collect = self.colle_com
        elif key in self.__jobs_keys:
            collect = self.colle
        else:
            collect = self.colle_req
        # print("-------------------",key)
        result_list = collect.find(projection=filed)
        if key == 'data':
            return self._words_collcet(result_list)
        result = []
        for i in result_list:
            try:
                result.append(i[key])
            except KeyError:
                pass
        return result

    def __count_data(self, data=None, filed=None):
        count_min = 0
        data_dict = Counter(data)
        if filed == 'salary':
            for value in data_dict.values():
                if value < 5:
                    count_min += 1
            self.__salary = data_dict.most_common()[:-count_min]
        elif filed == 'workYear':
            self.__work_year = data_dict
        elif filed == 'education':
            self.__education = data_dict
        elif filed == 'city':
            self.__district = data_dict
        elif filed == 'data':
            self.__req_data = list(filter(
                self.__filter_bed_words,
                data_dict.most_common(50))
            )

    def _words_collcet(self, word_result):
        for d in word_result:
            self.word_string += ''.join(d['data'])
        result = [w for w in jieba.cut(
            self.word_string, cut_all=True) if len(w) >= 3]
        return result

    def __filter_bed_words(self, d):
        return d[0] not in self.words

    @property
    def salary_data(self):
        return self.__salary

    @property
    def work_year_data(self):
        return self.__work_year

    @property
    def education_data(self):
        return self.__education

    @property
    def district_data(self):
        return self.__district

    @property
    def requests_data(self):
        return self.__req_data
