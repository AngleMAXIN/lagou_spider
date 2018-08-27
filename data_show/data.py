# !/usr/bin/env python
# -*- coding:utf-8 -*-

import jieba
import time
import json
import redis

from pymongo import MongoClient

from collections import Counter, OrderedDict

MONGO_URL = '127.0.0.1:27017'


def keywords():
    '''
    Function: keywords
    Summary: find all keyword from MongoDB 
    Examples: InsertHere
    Returns: InsertHere
    '''
    client = MongoClient(MONGO_URL)
    db_keys = client['keyword_list']
    colle_keyword = db_keys['coll_keyword']
    filed = {
        '_id': False,
        "keyword": True,
        "city": True,
        "workyear": True
    }
    result = colle_keyword.find(projection=filed)
    key_words = list()
    for key in result:
        key_words.append([key['keyword'], key['city'], key['workyear']])

    return key_words


class GetData(object):
    word_string = ''
    __salary = []
    __work_year = []
    __education = []
    __district = []
    __req_data = []
    __keywords = []
    KET_WORDS_DB = 'keyword_list'
    KET_WORDS_COLL = 'coll_keyword'
    FILE_NAME = "keyword.json"
    __comp_keys = ['city']
    __jobs_keys = ['salary', 'workYear', 'education']
    words = ['岗位职责', '熟练掌握', '解决方案', '以上学历', '岗位要求', '计算机相关'
             'java', 'Java', 'python', 'Python', 'C++', 'PHP', 'c++', '计算机', '软件开发', 'Docker', 'docker']

    def __init__(self, keyword, filed_list):
        self.keyword = keyword
        self.filed_list = filed_list

        # Mongo 
        client = MongoClient(MONGO_URL)
        self.db = client[self.KET_WORDS_DB]
        self.coll_key = self.db[self.KET_WORDS_COLL]

        # Redis 
        pool = redis.ConnectionPool(
            host='localhost', port=6379, decode_responses=True)
        self.rds = redis.Redis(connection_pool=pool)


        if not self.__check_key_exit():
            # if redis had not this data. get data from database and sava to redis
            # if hava , just get dat from redis
            self.keyword_json = {}
            self.db = client['job_info']
            self.colle = self.db[keyword + '_coll_job']
            self.colle_com = self.db[keyword + '_coll_company']
            self.colle_req = self.db[keyword + '_coll_requests']
            self._filed_api()
            self._write_json_to_file()

    def _filed_api(self):
        for filed in self.filed_list:
            self.__count_data(self.__get_data(filed), filed)

    def _write_json_to_file(self):
        self.keyword_json = {
            "keyword": self.keyword,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "salary_data": self.__salary,
            "work_year": self.__work_year,
            "education": self.__education,
            "city": self.__district,
            "requests": self.__req_data
        }
        # self.__openfile("a+")
        self._save_to_redis()

    def __check_key_exit(self):

        # if self.__openfile("r"):
        #     return True
        # return False

        result = self.rds.get(self.keyword)
        if result:
            self.__get_from_io(json.loads(result))
            return True
        return False

    def _save_to_redis(self):
        try:
            self.rds.set(self.keyword, json.dumps(self.keyword_json))
        except Exception as e:
            return False
        return True

    def __get_from_io(self, result):
        self.__salary = [tuple(r) for r in result['salary_data']]
        self.__work_year = result['work_year']
        self.__education = result['education']
        self.__district = result['city']
        self.__req_data = [tuple(r) for r in result['requests']]
        return True

    # def __openfile(self, open_model):
    #     with open(self.FILE_NAME, open_model, encoding="utf-8") as f:
    #         if open_model == "a+":
    #             f.write(json.dumps(self.keyword_json, sort_keys=True) + '\n')
    #             # f.write(strself.keyword_json)
    #         else:
    #             result = f.readlines()
    #             if len(result) == 0:
    #                 return False
    #             for line in result:
    #                 result = json.loads(line)
    #                 if result['keyword'] == self.keyword:
    #                     self.__get_from_io(result)
    #                     return True
    #             return False

    def __get_data(self, key):
        '''
        Function: __get_data
        Summary:  get data from mongodb by keyword and parse data
        Examples: InsertHere
        Attributes: 
            @param (self):InsertHere
            @param (key): filedname
        Returns: InsertHere
        '''
        filed = {'_id': False, key: True}
        if key in self.__comp_keys:
            collect = self.colle_com
        elif key in self.__jobs_keys:
            collect = self.colle
        else:
            collect = self.colle_req
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
        '''
        Function: __count_data
        Summary:  data count, if filed is 'data', need Chinese word segmentation
        Examples: InsertHere
        Attributes: 
            @param (self):InsertHere
            @param (data) default=None: InsertHere
            @param (filed) default=None: InsertHere
        Returns: InsertHere
        '''
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
                # take the top 60
                data_dict.most_common(60))
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
