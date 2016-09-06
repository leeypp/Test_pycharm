#!/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'leeypp'
import json
import time
import socket
import os
import urllib2
import commands

file = (
    '/usr/bin/chfn',
    '/usr/bin/chsh',
    '/bin/login',
    '/bin/ls',
    '/usr/bin/passwd',
    '/bin/ps',
    '/usr/bin/top',
    '/bin/netstat',
    '/sbin/ifconfig',
    '/usr/bin/killall',
    '/sbin/pidof',
    '/usr/bin/find')


def main():
    sum1 = 0
    for line in file:
        return1 = os.popen("cd / && rpm -Vf %s" % line)
        m = return1.read()
        n = len(m)
        if n == 0:
            val = 0
        else:
            val = 1
        falcon(line, val)  # 此处调用falcon函数，打印详细的输出信息，用于查看哪个文件发生变化。值为1就说明该文件发生变化
        sum1 = sum1 + val
    line = ""
    print '最终上报的值为：', sum1
    fina = falcon(line, sum1)  # 此处为真正上报的结果，这样处理方便templates的配置
    post_url(fina)


def falcon(tag, value):
    step = 60
    host = socket.gethostname()
    metric = 'secure.binshell'
    p = []
    m = {
        'Metric': metric,
        'Endpoint': host,
        'Timestamp': int(time.time()),
        'step': step,
        'Value': value,
        'CounterType': "GAUGE",
        'TAGS': tag  # 'file=%s'%tag
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
if __name__ == '__main__':
    proc = commands.getoutput(' ps -ef|grep %s|grep -v grep|wc -l ' %os.path.basename(sys.argv[0]))
    if int(proc) < 5:
        main()
