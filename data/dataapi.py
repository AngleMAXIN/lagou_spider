# !/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient


class DateStore(object):
    HOST = "localhost"
    POST = 27017
    i = 0
    SAVE_OVER = False

    def __init__(self, coll_name):
        self.client = MongoClient(host=self.HOST, port=self.POST)
        self.db = self.client['job_info']
        self.coll_job = self.db[coll_name + '_coll_job']
        self.coll_company = self.db[coll_name + '_coll_company']

    def let_save(self, com_document, job_document):

        for com in com_document:
            self.coll_company.insert(com)
            print("save com mongo -------", com)
        for job in job_document:
            self.coll_job.insert(job)
            print("save job mongo -------", job)
        # print("-------------successful-----------")
        self.SAVE_OVER = True

    @property
    def save_result(self):
        return self.SAVE_OVER
