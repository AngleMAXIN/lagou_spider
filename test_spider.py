from spider import ZhiLian_Spdier



def printf(daat):
    for i in daat:
        print(i)

def test():

    keyword = 'python'
    city = 530
    # 实习 4
    # 不限 -1
    employment_type = -1

    zhilian = ZhiLian_Spdier('python')
    zhilian.start_spider()
    print(zhilian.time_xpath_api)
    print(len(zhilian.jobs_url_list),len(zhilian.jobs_limit_list))
    printf(zhilian.jobs_limit_list)
    printf(zhilian.jobs_url_list)

    # printf(zhilian.jobs_url_list)
    # printf(zhilian.jobs_info_list)

if __name__ == '__main__':
    test()