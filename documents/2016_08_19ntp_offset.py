#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 时间同步监控脚本

from subprocess import Popen, PIPE
import json
import urllib2
import os
import time
import commands
import sys
import socket

data = []


def main():
    offset = 0
    try:
        raw_data = Popen(['ntpq', '-pn'], stdout=PIPE,stderr=PIPE).communicate()[0]  # 运行“ntpq -pn” 命令
        for line in raw_data.splitlines():  # 遍历每一行
            if line.startswith('*'):  # 选择以*开头的这一行
                offset = line.split()[8]  # 选择第九个字段的数据，以0开始
    except OSError:
        pass

    list = create_record(offset)  # 调用方法，将offset作为上传的value
    post_value(list)


def create_record(value):
    record = {}
    record['metric'] = 'sys.ntp.offset'
    record['endpoint'] = socket.gethostname()
    record['timestamp'] = int(time.time())
    record['step'] = 600
    record['value'] = abs(float(value))  # abs-返回绝对值
    record['counterType'] = 'GAUGE'
    record['tags'] = ''
    data.append(record)
    print record


def post_value(content):
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
    proc = commands.getoutput(' ps -ef|grep %s|grep -v grep|wc -l ' % os.path.basename(sys.argv[0]))
    if int(proc) < 5:
        main()
# 检测服务器时间偏移量