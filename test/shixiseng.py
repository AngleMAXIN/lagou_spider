# !/usr/bin/env python
import requests
import re
import pymongo

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
MongoUrl= 'localhost'
MongoDB = 'Shixiceng'
MongoTable = 'shixiceng'

def Gethtml(url):

    try:
        html = requests.get(url,headers=headers)
        if html.status_code == 200:
            # print(html.text)
            return html.text
    except Exception as e:
        print(e,"1")
def parse_html(html):
    job_url = []
    pattern = r'<a class="name" href="(.*?)" target="_blank"'
    result = re.findall(pattern,html,re.S)
    Url = "http://www.shixiseng.com"
    for i in result:
        parse_url = Url + i
        job_url.append(parse_url)
    return job_url

def Get_jobInfo(url):
    try:
        html = requests.get(url, headers=headers)
        if html.status_code == 200:
            reg = r'<div class="new_job_name" title="(.*?)">'
            job_name = re.findall(reg, html.text)[0]
            reg = r'<span title=".*?" class="job_position">(.*?)</span>'
            job_city = re.findall(reg, html.text)[0]
            reg = r'<div class="job_detail">(.*?)</div>'
            job_limit = re.findall(reg,html.text)[0]
            return {
                'job_name' : job_name,
                'job_city' : job_city,
                'job_limit' : job_limit
            }
    except Exception as e:
        print(e,"2")
def Save_Mongo(result):
    client = pymongo.MongoClient(MongoUrl,connect=False)
    db = client[MongoDB]
    if db[MongoTable].insert(result):
        print("数据存储成功")



def main():
    # for page in range(1,20):
    try:
        url = "https://www.shixiseng.com/interns/st-intern_?k=Android"
        html = Gethtml(url)
        job_url = parse_html(html)
        for i in job_url:
            print(i)
            # Result = Get_jobInfo(i)
            # Save_Mongo(Result)

    except Exception as e:
        print(e, "3")

if __name__ == '__main__':
    main()

# https://www.shixiseng.com/interns/st-intern_c-120100_ch-noentry_?k=Android&p=1
# https://www.shixiseng.com/interns/st-intern_c-120100_ch-entry_?k=Android&p=1
# https://www.shixiseng.com/interns/st-intern_c-120100_?k=Android&p=1
# https://www.shixiseng.com/interns/st-intern_c-120100_?k=Android&p=1&t=zj