# import redis
# import time, json
# from collections import OrderedDict
# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
# rds = redis.Redis(connection_pool=pool)


# data = {
#     "keyword": "python",
#             "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
#             "salary_data": [('a',4),('b',7),("5","7")],
#             "work_year": ['self.__work_year',6,'789'],
#             "education": "__education",
#             "city": 5,
#             "requests": [('a',4),('b',7),("5","7")],
# }


# # re = rds.set("key",json.dumps(data))
# # print(re)

# result = rds.get("key")
# t = json.loads(result,object_pairs_hook=OrderedDict)
# print(t['work_year'],type(t))
# # for i in t:
# #     print(type(i),"-->",i)

# from spider import dataapi
# from spider import DateStore

# da = DateStore()

import sys

print(sys.path)