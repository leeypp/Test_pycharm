#!/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'leeypp'
import time
import os
import urllib2
import json
from threading import Thread
path = '/data/work/open-falcon/plugin/ping/config_all'
start_Time = int(time.time())  # 记录开始时间
# 多线程ping，将结果通过open-falcon agent上传

class pingThread(Thread):

    def __init__(self, ip):
        Thread.__init__(self)
        self.ip = ip[0]
        self.link = ip[1]
        self.add = ip[2]

    def run(self):
        count_True, count_False = 0, 0
        ping = os.popen("ping -c 5 -i 0.1 -w 1 %s| grep loss|awk '{print $6}'" % (self.ip))
        m = ping.read()
        n = int(m.replace('%', ''))
        if (n == 100):
            h, min1, avg1, max1 = 0, 0, 0, 0
            count_False += 1
        else:
            return2 = os.popen("ping -c 5 -i 0.1 -w 1 %s| grep rtt|awk '{print $4}'" % (self.ip))
            hh = return2.read().replace('/', ' ')
            h = hh.replace('\n', '')
            val2 = h.split()
            min1 = float(val2[0])
            avg1 = float(val2[1])
            max1 = float(val2[2])
            count_True += 1
        a = loss(self.link, self.add, n)
        b = Time1(self.link, self.add, min1)
        c = Time2(self.link, self.add, avg1)
        d = Time3(self.link, self.add, max1)
        str_list = a + b + c + d
        post_url(str_list)
        end_Time = int(time.time())  # 记录结束时间
        print "time(秒)：", end_Time - start_Time, "s"  # 打印并计算用的时间
        print "ping通数：", count_True, "   ping不通的ip数：", count_False  # 结果计数


def loss(tag1, tag2, value):
    step = 60
    metric = 'pkt.loss.percent'
    p = []
    m = {
        'Metric': metric,
        'Endpoint': 'aliyun-bgp',
        'Timestamp': int(time.time()),
        'step': step,
        'Value': value,
        'CounterType': "GAUGE",
        'TAGS': 'add=%s,link=%s' % (tag2, tag1)
    }
    p.append(m)
    print p
    return p


def Time1(tag1, tag2, value):
    step = 60
    metric = 'Round-Trip.Time.min'
    p = []
    m = {
        'Metric': metric,
        'Endpoint': 'aliyun-bgp',
        'Timestamp': int(time.time()),
        'step': step,
        'Value': value,
        'CounterType': "GAUGE",
        'TAGS': 'add=%s,link=%s' % (tag2, tag1)
    }
    p.append(m)
    print p
    return p


def Time2(tag1, tag2, value):
    step = 60
    metric = 'Round-Trip.Time.avg'
    p = []
    m = {
        'Metric': metric,
        'Endpoint': 'aliyun-bgp',
        'Timestamp': int(time.time()),
        'step': step,
        'Value': value,
        'CounterType': "GAUGE",
        'TAGS': 'add=%s,link=%s' % (tag2, tag1)
    }
    p.append(m)
    print p
    return p


def Time3(tag1, tag2, value):
    step = 60
    metric = 'Round-Trip.Time.max'
    p = []
    m = {
        'Metric': metric,
        'Endpoint': 'aliyun-bgp',
        'Timestamp': int(time.time()),
        'step': step,
        'Value': value,
        'CounterType': "GAUGE",
        'TAGS': 'add=%s,link=%s' % (tag2, tag1)
    }
    p.append(m)
    print p
    return p


def post_url(content):
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = 'http://127.0.0.1:1988/v1/push'
    request = urllib2.Request(url, data=json.dumps(content))
    request.add_header("Content-Type", 'application/json')
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
    except urllib2.HTTPError as e:
        connection = e

    # check. Substitute with appropriate HTTP code
    if connection.code == 200:
        print connection.read()
    else:
        print '{"err":1,"msg":"%s"}' % connection


T_thread = []
for line in open(path):  # 打开path文件
    val = line.split()
    ip = val[2]
    link = val[1]
    add = val[0]
    print ip, link, add
    list = [ip, link, add]
    t = pingThread(list)  # 创建线程
    ll = T_thread.append(t)  # 添加线程到线程列表
for ip in range(len(T_thread)):  #len(T_thread)--开启的线程数
    T_thread[ip].start()  # 开启新线程
T_thread[ip].join()  # 等待所有线程完成
print "Exiting Main Thread"

'''
path 文件格式
haerbin dxin 219.150.32.132
shenyang dxin 219.148.204.66
guangzhou dxin 183.59.4.178
'''
