# !/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request, render_template, redirect, url_for

from ..main import main
from .show import EchartsApi
from .data import keywords


@main.route('/')
def index():

    context  = {
        "keyword_list": keywords()
    }
    return render_template('index.html', **context)


@main.route('/search', methods=['POST'])
def search_api():
    key = request.form.get('keyword')
    print("---" * 10, "searching")
    cities = [u"北京"]
    # is_ok = start.spider_start(key, cities)
    # if is_ok:
    return redirect(url_for('main.data_show'))
    # return "sorry fialed"


@main.route('/data_show')
def data_show():
    key_words = ['salary', 'workYear', 'education', 'city', 'data']
    key = 'golang'
    echarts = EchartsApi(key_words, key)
    render_list = echarts.echarts_list
    content = {
        "keyword": key,
        "render_list": render_list

    }
    return render_template('result.html', **content)
