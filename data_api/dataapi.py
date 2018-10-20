# !/usr/bin/env python
# -*- coding:utf-8 -*-

import gevent
from gevent import monkey
from pymongo import MongoClient

monkey.patch_all()


class LaGouDateStore(object):

    HOST = "localhost"
    PORT = 27017
    SAVE_OVER = False
    KET_WORDS_DB = 'keyword_list'
    KET_WORDS_COLL = 'coll_keyword'
    DB = 'job_info'

    def __init__(self, coll_name, gx='', cities=None):
        self.coll_name = coll_name
        self.workyear = gx
        self.cities = cities

        self.client = MongoClient(host=self.HOST, port=self.PORT)
        self.keyword_db = self.client[self.KET_WORDS_DB]
        self.coll_keywords = self.keyword_db[self.KET_WORDS_COLL]
        self.db = self.client[self.DB]
        self.coll_job = self.db[gx + coll_name + '_coll_job']
        self.coll_company = self.db[gx + coll_name + '_coll_company']
        self.coll_requests = self.db[gx + coll_name + '_coll_requests']
        self.__save_keywords()

    def __save_keywords(self):
        keyword = {
            'keyword': self.coll_name,
            'city': self.cities[0],
            'workyear': self.workyear
        }
        self.coll_keywords.insert(keyword)

    def __save_com(self, com_doc):
        if len(com_doc) == 0:
            return False
        for com in com_doc:
            self.coll_company.insert(com)

    def __save_job(self, job_doc):
        if len(job_doc) == 0:
            return False
        for job in job_doc:
            self.coll_job.insert(job)

    def __save_requests(self, request_doc):
        if len(request_doc) == 0:
            return False
        for req in request_doc:
            self.coll_requests.insert(req)

    def let_save(self, com_doc, job_doc, request_doc):
        # self.__save_keywords(self.coll_name)
        try:
            gevent.joinall([
                gevent.spawn(self.__save_com, com_doc),
                gevent.spawn(self.__save_job, job_doc),
                gevent.spawn(self.__save_requests, request_doc)
            ])
        except Exception as e:
            raise e
        else:
            self.SAVE_OVER = True

    @property
    def save_result(self):
        return self.SAVE_OVER




#
# if __name__ == '__main__':
#     key = ['python', 'java', "C++","PHP", "docker","golang","web前端"]
#     city = "全国"
#     gx = "不限"
#     for k in key:
#         ex = DateStore(k,gx,city)


