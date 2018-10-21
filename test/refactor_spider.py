# !/usr/bin/env python
# -*- coding:utf-8 -*-

#
# import gevent.monkey
#
# gevent.monkey.patch_socket()
# import gevent
# import requests
# import simplejson as json
#
#
#
# def fetch(pid):
#     response = requests.get('http://json-time.appspot.com/time.json')
#     result = response.text
#     json_result = json.loads(result)
#     datetime = json_result['datetime']
#     print('Process %s: %s' % (pid, datetime))
#
#     return json_result['datetime']
#
#
# def synchronous():
#     for i in range(1, 10):
#         fetch(i)
#
#
# def asynchronous():
#     threads = []
#     for i in range(1, 10):
#         threads.append(gevent.spawn(fetch, i))
#     gevent.joinall(threads)
#
#
# print('Synchronous:')
# synchronous()
# print('Asynchronous:')
# asynchronous()
import gevent
import time
import random
from gevent import monkey; monkey.patch_all()
l = [i for i in range(500)]

uuuu = []
def prin(i):
    # gevent.sleep(2)
    time.sleep(random.random()*0.004)
    uuuu.append(i)

def gevent_test(l):
    th = []
    for i in l:
        th.append(gevent.spawn(prin,i))
    gevent.joinall(th)
    #     prin(i)
uu = []
def prinl(i):
    # gevent.sleep(2)
    time.sleep(random.random()*0.004)
    uu.append(i)
def no_gevent(l):
    for i in l:
        prinl(i)

u = time.time()
gevent_test(l)
print(uuuu)
print("gevent",time.time() - u)

u1 = time.time()
no_gevent(l)
print(uu)
print("no_gevent",time.time() - u1)
