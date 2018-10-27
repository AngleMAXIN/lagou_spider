from spider import LaGou_Spider


def printf(daat):
    for i in daat:
        print(i)


def test():

    keyword = 'python'
    city = '北京'
    # 实习 4
    # 不限 -1

    shixi = LaGou_Spider(keyword, city)
    shixi.start_spider()

    # printf(shixi.jobs_info_list)
    printf(shixi._jobs_limit_list)
    # printf(zhilian.jobs_info_list)


if __name__ == '__main__':
    test()
