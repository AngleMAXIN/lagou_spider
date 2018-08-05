# !/usr/bin/env python
# -*- coding:utf-8 -*-
import gevent
from pymongo import MongoClient


class DateStore(object):
    HOST = "localhost"
    PORT = 27017
    i = 0
    SAVE_OVER = False

    def __init__(self, coll_name):
        self.coll_name = coll_name
        self.client = MongoClient(host=self.HOST, port=self.PORT)
        self.keyword_list = self.client['keyword_list']
        self.coll_keywords = self.keyword_list['coll_keywords']
        self.db = self.client['job_info']
        self.coll_job = self.db[coll_name + '_coll_job']
        self.coll_company = self.db[coll_name + '_coll_company']
        self.coll_requests = self.db[coll_name + '_coll_coll_requests']
        self.test_company = self.db['test_coll_company']

    def __save_keywords(self, key):
        keyword = {
            "keyword": key
        }
        if self.coll_keywords.find(keyword):
            pass
        self.coll_keywords.insert(keyword)

    def __save_com(self, com_doc):
        for com in com_doc:
            self.coll_company.insert(com)
            print("com")

    def __save_job(self, job_doc):
        for job in job_doc:
            self.coll_job.insert(job)
            print("job")

    def __save_requests(self, request_doc):
        for req in request_doc:
            self.coll_requests.insert(req)
            print("req")

    def let_save(self, com_doc, job_doc, request_doc):
        self.__save_keywords(self.coll_name)

        gevent.joinall([
            gevent.spawn(self.__save_com, com_doc),
            gevent.spawn(self.__save_job, job_doc),
            gevent.spawn(self.__save_requests, request_doc)
        ])

    def insert_requests(self, data):
        print(data)
        self.test_company.insert(data)

    @property
    def save_result(self):
        return self.SAVE_OVER
