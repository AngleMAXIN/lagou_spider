# !/usr/bin/env python
# -*- coding:utf-8 -*-

from pyecharts import Bar, Pie, Geo
from .data import GetData


def salary_show():
    g = GetData()
    keyword = ['salary']
    g.filed_api(keyword)
    bar = Bar("薪资统计", title_pos='center', width=1200, height=500)
    attr, value = bar.cast(g.salary_data)
    bar.add("", attr, value,xaxis_interval=0, xaxis_rotate=30,
            yaxis_rotate=30, is_more_utils=True)
    return bar.render_embed()


def work_year_show():
    g = GetData()
    keyword = ['workYear']
    g.filed_api(keyword)
    pie = Pie("工作经验", title_pos='center',width=1200, height=500)
    attr, attr = pie.cast(g.work_year_data)
    pie.add("", attr, attr, radius=[40, 80],
            title_pos='center', is_label_show=True,
            legend_orient='vertical',legend_pos='left')
    return pie.render_embed()


def education_show():
    g = GetData()
    keyword = ['education'] 
    g.filed_api(keyword)
    pie = Pie("education",title_pos='center',width=1200, height=500)
    attr, value = pie.cast(g.education_data)
    # print(attr)
    pie.add("", attr, value, adius=[40, 80],
            title_pos='center', is_label_show=True,
            legend_orient='vertical',legend_pos='left')
    return pie.render_embed()


def district_show():
    g = GetData()
    keyword = ['city']
    g.filed_api(keyword)
    geo = Geo("citys", title_color="#fff",width=1200,height=500,
              title_pos="center",background_color='#404a59')
    attr, value = geo.cast(g.district_data)
    # print(attr,value)
    geo.add("", attr, value, visual_range=[0, 200], maptype='china',visual_text_color="#fff",
            symbol_size=10, is_visualmap=True)
    geo.render("ndex.html")
    return geo.render_embed()
    