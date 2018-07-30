# !/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient


class DateStore():
    HOST = "localhost"
    POST = 27017
    i = 0
    def __init__(self):
        self.client = MongoClient(host=self.HOST, port=self.POST)
        self.db = self.client['job_info']
        self.coll_job = self.db['coll_job']
        self.coll_company = self.db['coll_company']

    def let_save(self, com_document, job_document):
        for com in com_document:
            self.coll_company.insert(com)
            print("save com mongo -------", com)
        for job in job_document:
            self.coll_job.insert(job)
            print("save job mongo -------", job)
        print("-------------successful-----------")

