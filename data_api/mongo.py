# !/usr/bin/env python
# -*- coding:utf-8 -*-

import gevent,time
from gevent import monkey
from pymongo import MongoClient

monkey.patch_all()


class LaGouDateStore(object):

    HOST = "localhost"
    PORT = 27017
    SAVE_OVER = False
    JOB_INFO_DB = 'jobs_info'
    JOB_LIMIT_DB = 'jobs_limit'
    DB = 'notes'

    def __init__(self, coll_name, emp_type='', citiy=None):
        self.coll_name = coll_name
        self.emp_type = 'fw' if emp_type == '实习' else ''
        self.city = city

        self.client = MongoClient(host=self.HOST, port=self.PORT)
        self.jobs_info_db = self.client[self.JOB_INFO_DB]
        self.jobs_limit_db = self.client[self.JOB_LIMIT_DB]
        self.other_db = self.client[self.DB]

        self.jobs_info_coll = self.jobs_info_db[gx + coll_name]
        self.jobs_limit_coll = self.jobs_limit_db[gx + coll_name]
        self.keywords_coll = self.other_db['keywords']

        self.__save_keywords()

    def __save_keywords(self):
        keyword = {
            'keyword': self.coll_name,
            'city': self.city,
            'workyear': "实习" if self.emp_type == 'fw' else "不限"
            'time': time.strftime("%Y-%m-%d %X", time.localtime())
        }
        self.keywords_coll.insert(keyword)

    def _save_com(self, com_doc):
        if len(com_doc) == 0:
            return False
        for com in com_doc:
            self.coll_company.insert(com)

    def _save_job(self, job_doc):
        if len(job_doc) == 0:
            return False
        for job in job_doc:
            self.coll_job.insert(job)

    def _save_requests(self, request_doc):
        if len(request_doc) == 0:
            return False
        for req in request_doc:
            self.coll_requests.insert(req)

    def let_save(self, job_doc, request_doc):
        # self.__save_keywords(self.coll_name)
        try:
            gevent.joinall([
                gevent.spawn(self._save_job, job_doc),
                gevent.spawn(self._save_requests, request_doc)
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


