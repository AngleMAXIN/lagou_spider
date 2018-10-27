# !/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os.path
import time

# 第一步，创建一个logger

logger = logging.getLogger()

# Log等级总开关
logger.setLevel(logging.INFO)

# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/flyjob/log/'
log_name = "spider.log"
fh = logging.FileHandler(log_path + log_name, mode='a')

# 输出到file的log等级的开关
fh.setLevel(logging.INFO)  

# 第三步，定义handler的输出格式
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)

# 第四步，将logger添加到handler里面
logger.addHandler(fh)

