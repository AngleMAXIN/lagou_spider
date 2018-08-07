# !/usr/bin/env python
# -*- coding:utf-8 -*-

from pyecharts import Bar, Pie
from .data import GetData


def salary_show():
    g = GetData()
    keyword = ['salary']
    g.filed_api(keyword)
    bar = Bar("薪资统计",title_pos='center', width=1200, height=500)
    salary_name, salary_count = bar.cast(g.salary_data)
    bar.add("", salary_name, salary_count,
            xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30, is_more_utils=True)
    return bar


def work_year_show():
    g = GetData()
    keyword = ['workYear']
    g.filed_api(keyword)
    pie = Pie("工作经验", title_pos='center')
    attr_name, attr_value = pie.cast(g.work_year_data)
    pie.add("", attr_name, attr_value, radius=[40, 80], title_pos='center', is_label_show=True,
            legend_orient='vertical',
            legend_pos='left')
    return pie
