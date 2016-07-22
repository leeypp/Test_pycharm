#!/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'leeypp'
import time
import commands
import socket
import urllib2
import json
# 一分钟内文件变化，过滤，再进行处理


def tvengine():
    n = commands.getoutput(''' cat /data/log/tvengine/tv0.log /data/log/tvengine/tv1.log /data/log/tvengine/tv2.log /data/log/tvengine/tv3.log /data/log/tvengine/tv4.log /data/log/tvengine/tv5.log /data/log/tvengine/tv6.log /data/log/tvengine/tv7.log |grep `date +"%Y-%m-%d"`|grep `date +"%H:%M:"`|grep '3rd'|wc -l ''' ).split('\n')
    print n
    n = n[0]
    n = int(n)
    list = loss(n)
    post_url(list)


def loss(value):
    step = 60
    hostname = socket.gethostname()
    metric = 'tvengine.post.3rd'
    p = []
    m = {
        'Metric': metric,
        'Endpoint': hostname,
        'Timestamp': int(time.time()),
        'step': step,
        'Value': value,
        'CounterType': "GAUGE",
        'TAGS': ''
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
tvengine()
