
import pymongo
import cProfile
from collections import Counter


MONGO_URL = '127.0.0.1:27017'
client = pymongo.MongoClient(MONGO_URL)
db = client['job_info']
colle = db['php_coll_job']

fileds = {'_id': False, 'salary': True}
result_list = colle.find(projection=fileds)
result = []
for i in result_list:
    result.append(i['salary'])


def count_3(datas=None):
    data_dict = Counter(datas)
    for d in data_dict.items():
        if d[1] < 3:
            del d

    data_list = list(data_dict.keys())
    data_count = list(data_dict.values())
    print(data_list, data_count)


cProfile.run('count_3(result)')
