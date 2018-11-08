# !/usr/bin/env python
# -*- coding:utf-8 -*-

import gevent
import time
from gevent import monkey
from pymongo import MongoClient
from .log import logger
monkey.patch_all()


class DateStore(object):

    HOST = "localhost"
    PORT = 27017
    JOB_INFO_DB = 'jobs_info'
    JOB_LIMIT_DB = 'jobs_limit'
    DB = 'notes'

    def __init__(self, coll_name, emp_type='', city=None):
        self.coll_name = coll_name
        self.emp_type = 'fw' if emp_type == '实习' else ''
        self.city = city

        self.client = MongoClient(host=self.HOST, port=self.PORT)
        self.jobs_info_db = self.client[self.JOB_INFO_DB]
        self.jobs_limit_db = self.client[self.JOB_LIMIT_DB]
        self.other_db = self.client[self.DB]

        self.jobs_info_coll = self.jobs_info_db[self.emp_type + coll_name]
        self.jobs_limit_coll = self.jobs_limit_db[self.emp_type + coll_name]
        self.keywords_coll = self.other_db['keywords']

        self.__save_keywords()

    def __save_keywords(self):
        keyword = {
            'keyword': self.coll_name,
            'city': self.city,
            'workyear': "实习" if self.emp_type == 'fw' else "不限",
            'time': time.strftime("%Y-%m-%d %X", time.localtime())
        }
        self.keywords_coll.insert(keyword)
        logger.info("save note keyword:{0} succeed".format(self.coll_name))

    def _save_job(self, job_doc):
        number = len(job_doc)
        if number == 0:
            return False
        for job in job_doc:
            self.jobs_info_coll.insert(job)
        logger.info("succeed inserty job info {0}:{1}:{2} number:{3}".format(
            self.coll_name, self.city, self.emp_type, number))

    def _save_requests(self, request_doc):
        number = len(request_doc)
        if number == 0:
            return False
        for req in request_doc:
            self.jobs_limit_coll.insert(req)
        logger.info("succeed inserty job limit {0}:{1}:{2} number:{3}".format(
            self.coll_name, self.city, self.emp_type, number))

    def let_save(self, job_doc, request_doc):
        # self.__save_keywords(self.coll_name)
        try:
            print("-----start ave to mongo-----")
            gevent.joinall([
                gevent.spawn(self._save_job, job_doc),
                gevent.spawn(self._save_requests, request_doc)
            ])
        except Exception as e:
            logger.error("save to mongo failed {0}".format(e))
            pass
        else:
            return True


#
# if __name__ == '__main__':
#     key = ['python', 'java', "C++","PHP", "docker","golang","web前端"]
#     city = "全国"
#     gx = "不限"
#     for k in key:
#         ex = DateStore(k,gx,city)
