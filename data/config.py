# !/usr/bin/env python
# -*- coding:utf-8 -*-

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    # 'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?px=default&city=%E6%9D%AD%E5%B7%9E',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lagou.com',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': None,
    'X-Requested-With': 'XMLHttpRequest'
}
# Cookie= 'JSESSIONID=ABAAABAAADEAAFI6D8D57BCA8CF1E9A7ED03144441CC87C; _ga=GA1.2.429037355.1532907445; _gid=GA1.2.1657994839.1532907445; user_trace_token=20180730073724-58ce1db1-9388-11e8-a082-5254005c3644; LGSID=20180730073724-58ce1f65-9388-11e8-a082-5254005c3644; LGUID=20180730073724-58ce2118-9388-11e8-a082-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532907445; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=search_code; LGRID=20180730090345-68c4b904-9394-11e8-a082-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532912626; SEARCH_ID=5fcb93102ac846909b61a0aabfd3e843',
cookies = {
    'user_trace_token': '20171011085044-36afc724-ae1e-11e7-947d-5254005c3644',
    'LGUID': '20171011085044-36afc9e6-ae1e-11e7-947d-5254005c3644',
    '_ga': 'GA1.2.1411877279.1507683044',
    'index_location_city': '%E5%B9%BF%E5%B7%9E',
    'JSESSIONID': 'ABAAABAAADEAAFI2466B2149D4B3E406932CAEA37FDF471',
    '_gid': 'GA1.2.1604143331.1517585155',
    'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1515000882,1515252738,1516984463,1517585156',
    'LGSID': '20180202232556-5ce93c91-082d-11e8-abfa-5254005c3644', 'PRE_UTM': '',
    'PRE_HOST': '',
    'PRE_SITE': '',
    'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
    'TG-TRACK-CODE': 'index_navigation',
    'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1517585322',
    'LGRID': '20180202232842-c0095589-082d-11e8-abfa-5254005c3644',
    'SEARCH_ID': '0a887843a48a49c7bb6dae915dabdcc1'
}
# headers = {
#     'Host': 'www.lagou.com',
#     'Connection': 'keep-alive',
#     'Content-Length': '23',
#     'Origin': 'https://www.lagou.com',
#     'X-Anit-Forge-Code': '0',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'X-Requested-With': 'XMLHttpRequest',
#     'X-Anit-Forge-Token': 'None',
#     # 'Referer': 'https://www.lagou.com/jobs/list_java?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
# }