# !/usr/bin/env python
# -*- coding:utf-8 -*-

from pyecharts import Bar, Pie, Geo, WordCloud
from .data import GetData


class EchartsApi(object):

    def __init__(self, key_list, keyword):
        self.key_list = key_list
        self.g = GetData(keyword)

    def choice_show_api(self):
        show_dict = [
            self._salary_show(),
            self._work_year_show(),
            self._education_show(),
            self._city_show(),
            self._requests_show()
        ]
        return show_dict

    def _salary_show(self):
        bar = Bar("薪资统计", title_pos='center', width=1200, height=500)
        attr, value = bar.cast(self.g.salary_data)
        bar.add("", attr, value, xaxis_interval=0, xaxis_rotate=30,
                yaxis_rotate=30, is_more_utils=True)
        return bar.render_embed()

    def _work_year_show(self):
        pie = Pie("工作经验", title_pos='center', width=1200, height=500)
        attr, value = pie.cast(self.g.work_year_data)
        pie.add("", attr, value, radius=[40, 80],
                title_pos='center', is_label_show=True,
                legend_orient='vertical', legend_pos='left')
        return pie.render_embed()

    def _education_show(self):
        pie = Pie("学历统计", title_pos='center', width=1200, height=500)
        attr, value = pie.cast(self.g.education_data)
        # print(attr)
        pie.add("", attr, value, adius=[40, 80],
                title_pos='center', is_label_show=True,
                legend_orient='vertical', legend_pos='left')
        return pie.render_embed()

    def _city_show(self):
        geo = Geo("地区分布", width=1200, height=500, title_pos="center")
        attr, value = geo.cast(self.g.district_data)
        geo.add("", attr, value, visual_range=[0, 200], maptype='china',
                visual_text_color="#fff", symbol_size=10, is_visualmap=True)
        return geo.render_embed()

    def _requests_show(self):
        word_cloud = WordCloud("技能要求云图", width=1300,
                               height=620, title_pos='center')
        attr, value = word_cloud.cast(self.g.requests_data)
        word_cloud.add("", attr, value, word_size_range=[
                       20, 100], shape='diamond')
        return word_cloud.render_embed()

    @property
    def echarts_list(self):
        self.g.filed_api(self.key_list)
        return self.choice_show_api()
