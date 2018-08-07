# !/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

from collections import Counter


class GetData(object):
    __salary = []
    __work_year = []

    def __init__(self):
        MONGO_URL = '127.0.0.1:27017'
        client = MongoClient(MONGO_URL)
        self.db = client['job_info']
        self.colle = self.db['php_coll_job']

    def filed_api(self, filed_list):
        for filed in filed_list:
            self.__count_data(self.__get_data(filed), filed)

    def __get_data(self, key):
        filed = {'_id': False, key: True}
        result_list = self.colle.find(projection=filed)
        result = []
        for i in result_list:
            result.append(i[key])
        return result

    def __count_data(self, data=None, filed=None):
        count_min = 0
        data_dict = Counter(data)
        # print(data_dict.most_common())
        for value in data_dict.values():
            if value < 5:
                count_min += 1
        if filed == "salary":
            self.__salary = data_dict.most_common()[:-count_min]
        elif filed == 'workYear':
            self.__work_year = data_dict

    @property
    def salary_data(self):
        print(self.__salary)
        return self.__salary

    @property
    def work_year_data(self):
        print(self.__work_year)
        return self.__work_year
