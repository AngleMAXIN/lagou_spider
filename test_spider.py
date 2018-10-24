from spider import ZhiLian_Spdier,ShiXi_Spider



def printf(daat):
    for i in daat:
        print(i)

def test():

    keyword = 'python'
    city = '北京'
    # 实习 4
    # 不限 -1

    shixi = ShiXi_Spider(keyword,city)
    shixi.start_spider()
    # zhilian = ZhiLian_Spdier(keyword,city)
    # zhilian.start_spider()

    printf(shixi.jobs_info_list)
    # printf(zhilian.jobs_info_list)

if __name__ == '__main__':
    test()


    self._jobs_info_list.append({
                    'companyname': job_com_name,
                    'company_url': com_base_url + job_com_url,
                    'positionurl': base_url + job_url,
                    'jobname': job_name,
                    'city': job_city,
                    'edulevel': job_edu,
                    'limit': limit ,
                    'com_logo':com_logo
                })