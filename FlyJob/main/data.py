# !/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

from collections import Counter


class GetData(object):
    __salary = []
    __work_year = []
    __education = []
    __district = []
    __comp_keys = ['city']
    __jobs_keys = ['salary', 'workYear', 'education']

    def __init__(self):
        MONGO_URL = '127.0.0.1:27017'
        client = MongoClient(MONGO_URL)
        self.db = client['job_info']
        self.colle = self.db['golang_coll_job']
        self.colle_com = self.db['golang_coll_company']

    def filed_api(self, filed_list):
        for filed in filed_list:
            self.__count_data(self.__get_data(filed), filed)

    def __get_data(self, key):
        filed = {'_id': False, key: True}
        collect = None
        if key in self.__comp_keys:
            collect = self.colle_com
        elif key in self.__jobs_keys:
            collect = self.colle
        result_list = collect.find(projection=filed)
        result = []
        for i in result_list:
            try:
                result.append(i[key])
            except Exception as e:
                pass
        return result

    def __count_data(self, data=None, filed=None):
        count_min = 0
        data_dict = Counter(data)
        # print(data_dict.most_common())
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
        # print("---"*10,self.__district)
        return self.__district
