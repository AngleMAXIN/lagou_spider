# !/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request, render_template, redirect, url_for

from lagou_spider.FlyJob.main import main
from lagou_spider.spider import start
from .show import salary_show, work_year_show


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/search', methods=['POST'])
def search_api():
    key = request.form.get('keyword')
    print("---" * 10, "searching")
    cities = [u"北京"]
    # is_ok = start.spider_start(key, cities)
    # if is_ok:
    return redirect(url_for('main.data_show'))
    # return "sorry fialed"


@main.route('/datashow')
def data_show():
    salary_bar = salary_show()
    work_year_pie = work_year_show()
    content = {
        "salary_bar": salary_bar.render_embed(),
        "work_year_show": work_year_pie.render_embed()

    }
    return render_template('result.html', **content)

