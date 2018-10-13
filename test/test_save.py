# # !/usr/bin/env python
# # -*- coding:utf-8 -*-
# import jieba
# from data_show.data import GetData
# from collections import Counter

# def main():
#     jieba.enable_parallel(3)
#     key = ['data']
#     g = GetData()
#     g.filed_api(key)
#     word_string = ''
#     for data in g.requests_data:
#         word_string += ''.join(data)
#     # print(word_string)
#     result_01 = [w for w in jieba.cut(word_string, cut_all=True) if len(w) >= 3]
#     result_02 = [w for w in jieba.cut(word_string) if len(w) >= 3]
#     result_03 = [w for w in jieba.cut_for_search(word_string) if len(w) >= 3]
#     # print(result)
#     count_1_test = Counter(result_01).most_common(50)
#     # count_2 = Counter(result_02).most_common(50)
#     # count_3 = Counter(result_03).most_common(50)
#     def filter_bed_words(data):
#         words = ['岗位职责','熟练掌握','解决方案','以上学历']
#         return data[0] not in words
#     count_1 = filter(filter_bed_words, count_1_test)
#     print("精确模式:", list(count_1))
#     # for i in count_1:
#     #     print(i)
#     # print("全模式:",count_2)
#     # print("搜索引擎模式",count_3)
# main()

# from spider import dataapi
import os.path

print(os.path.dirname(os.getcwd())+"/log/")
