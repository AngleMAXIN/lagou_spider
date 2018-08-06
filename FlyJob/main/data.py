from pymongo import MongoClient

from collections import Counter


class GetData(object):
    __salary = []

    def __init__(self):
        MONGO_URL = '127.0.0.1:27017'
        client = MongoClient(MONGO_URL)
        self.db = client['job_info']

        self.colle = self.db['php_coll_job']

    def salary(self):
        fileds = {'_id': False, 'salary': True}
        result_list = self.colle.find(projection=fileds)
        result = []
        for i in result_list:
            result.append(i['salary'])
        self.count_data(result)

    def count_data(self, datas=None):
        count_min = 0
        data_dict = Counter(datas)
        # print(data_dict.most_common())
        for value in data_dict.values():
            if value < 5:
                count_min += 1
        self.__salary = data_dict.most_common()[:-count_min]
        print("---",self.__salary)
    @property
    def salary_data(self):
        return self.__salary
        # for d in data_dict.items():
        #     if d[1] < 3:
        #         del d
