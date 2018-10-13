# !/usr/bin/env python
# -*- coding:utf-8 -*-
import random

post_headers = [{
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_Java?px=default&city=%E5%8C%97%E4%BA%AC',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lagou.com',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': None,
    'X-Requested-With': 'XMLHttpRequest'
}, {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
    'Referer': 'https://www.lagou.com/jobs/list_go?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lagou.com',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': None,
    'X-Requested-With': 'XMLHttpRequest'
}, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
    'Referer': 'https://www.lagou.com/jobs/list_Java?px=default&city=%E5%8C%97%E4%BA%AC',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lagou.com',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': None,
    'X-Requested-With': 'XMLHttpRequest'
}, {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
    'Referer': 'https://www.lagou.com/jobs/list_java%20web?oquery=java%E5%A4%A7%E6%95%B0%E6%8D%AE&fromSearch=true&labelWords=relative&city=%E5%8C%97%E4%BA%AC',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lagou.com',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': None,
    'X-Requested-With': 'XMLHttpRequest'
}, {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
    'Referer': 'https://www.lagou.com/jobs/list_java%E5%A4%A7%E6%95%B0%E6%8D%AE?oquery=Java&fromSearch=true&labelWords=relative',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lagou.com',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': None,
    'X-Requested-With': 'XMLHttpRequest'
}]


def post_header():
    return random.choice(post_headers)


post_cookies = {
    'cookies': "ga=GA1.2.429037355.1532907445; \
    user_trace_token=20180730073724-58ce1db1-9388-11e8-a082-5254005c3644; \
    LGUID=20180730073724-58ce2118-9388-11e8-a082-5254005c3644; index_location_city=%E6%9D%AD%E5%B7%9E; \
    _gid=GA1.2.977130810.1533126669; JSESSIONID=ABAAABAABEEAAJA1A75E33213A0384577266415B4511D3D; \
    _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533014821,1533020693,1533126669,1533171673; \
    LGSID=20180802090112-8cc880aa-95ef-11e8-ae7d-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; \
    PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_navigation; \
    LGRID=20180802090114-8e2beb3b-95ef-11e8-ae7d-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533171675; \
    SEARCH_ID=054844d5dc124332b162539f86eae6ea"
}

get_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br;',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_Java?px=default&gx=%E5%85%A8%E8%81%8C&gj=&isSchoolJob=1&city=%E5%B9%BF%E5%B7%9E',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
}
get_cookie = {
    'Cookie': '_ga=GA1.2.429037355.1532907445; user_trace_token=20180730073724-58ce1db1-9388-11e8-a082-5254005c3644; \
                LGUID=20180730073724-58ce2118-9388-11e8-a082-5254005c3644; \
                _gid=GA1.2.977130810.1533126669; index_location_city=%E5%85%A8%E5%9B%BD; \
                JSESSIONID=ABAAABAAAGFABEFA3F94FDD22786F642EDD0DB3ED13123E; \
                Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533020693,1533126669,1533171673,1533203842; \
                LGSID=20180802202858-a15df84e-964f-11e8-a0db-5254005c3644; PRE_UTM=; PRE_HOST=; \
                PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=search_code; \
                SEARCH_ID=3ca71c89a0e94a988a6fa71e930fabb6; LGRID=20180802203311-37aa6455-9650-11e8-aeb2-525400f775ce; \
                Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533213191'

}
