# !/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request, render_template

from lagou_spider.FlyJob.main import main
from lagou_spider.data import start


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/search', methods=['POST'])
def search_api():
    key = request.form.get('keyword')
    print("---"*10,"searching")
    cities = [u"北京"]
    is_ok = start.spider_start(key, cities)
    if is_ok:
        return "ok"
    return "sorry fialed"



z