from lagou_spider.spider import ZhiLian_Spdier


def printf(daat):
    for i in daat:
        print(i)

def test():
    zhilian = ZhiLian_Spdier('python')
    zhilian.start_spider()
    # printf(zhilian.jobs_limit_list)
    print(zhilian.time_xpath_api)
    # printf(zhilian.jobs_url_list)
    # printf(zhilian.jobs_info_list)

if __name__ == '__main__':
    test()