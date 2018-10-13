# !/usr/bin/env python
# -*- coding:utf-8 -*-

from data_show.data import keywords
from data_show.show import EchartsApi
from flask import render_template

from ..main import main


@main.route('/')
def index():

    context = {
        "keyword_list": keywords()
    }
    return render_template('index.html', **context)


# @main.route('/search', methods=['POST'])
# def search_api():
#     key = request.form.get('keyword')
#     print("---" * 10, "searching")
#     cities = [u"北京"]
#     # is_ok = start.spider_start(key, cities)
#     # if is_ok:
#     return redirect(url_for('main.data_show'))
#     # return "sorry fialed"


@main.route('/data_show/<keyword>')
def data_show(keyword):
    key_words = ['salary', 'workYear', 'education', 'city', 'data']
    # print(keyword)
    echarts = EchartsApi(key_words, keyword)
    render_list = echarts.echarts_list
    # print("---------",render_list)
    content = {
        "keyword": keyword,
        "render_list": render_list

    }
    return render_template('result.html', **content)
