


def decode_word(content, spe=False):
    # 解析加密字符串
    words = {
        'xf31a': '0',
        'xf548': '1',
        'xf25d': '2',
        'xe96b': '3',
        'xf825': '4',
        'xf22f': '5',
        'xe9b1': '6',
        'xee63': '7',
        'xe95d': '8',
        'xe951': '9',
    }
    res = ""
    try:
        if spe:
            content = content.split('-')
            pre_words = content[0].split('&#')
            next_word = content[1].split('&#')

            for char in pre_words[1:]:
                res += words[char]
            res = res + '-'
            for char in next_word[1:]:
                res += words[char]
        else:
            words = content.split('&#')

            for char in words[1:]:
                res += words[char]
    except KeyError as e:
        pass
    else:
        pass

        return res


import time
for i in range(6):
    start = time.time()
    content = '&#xf25d&#xf31a&#xf31a-&#xf25d&#xf22f&#xf31a'
    print(decode_word(content, True))
    # content = '&#xf25d&#xf31a&#xf548&#xe95d-&#xf548&#xf31a-&#xf25d&#xe96b'
    # print(decode_word(content, True))
    # content = '&#xf3we1a-&#xf31a'
    # print(decode_word(content, True))
    end = time.time() - start
    print(end)

# # 1.0251998901367188e-05
# # 6.67572021484375e-06
# # 5.7220458984375e-06
# # 5.7220458984375e-06
# # 5.245208740234375e-06
# # 5.245208740234375e-06


# # 1.2159347534179688e-05
# # 7.867813110351562e-06
# # 6.4373016357421875e-06
# # 6.4373016357421875e-06
# # 6.198883056640625e-06
# # 6.198883056640625e-06

# self._jobs_info_list.append({
#                 'jobname': job_info['jobName'],
#                 'salary': job_info['salary'],
#                 'city': job_info['city']['display'],
#                 'updatedate': job_info['updateDate'],
#                 'positionurl': url,
#                 'company_name': job_info['company']['name'],
#                 'edulevel': job_info['eduLevel']['name'],
#                 'workingexp': job_info['workingExp']['name']
#             })
/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div