#!/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'leeypp'

import json
import time
import socket
import os
import re
import sys
import commands
import urllib2
path = './redis_file'

#需要修改的地方：redis-cli路径，连接的host，redis配置文件路径
class RedisStats: #该类实现与redis连接，返回info信息
    # 如果你是自己编译部署到redis，请将下面的值替换为你到redis-cli路径
    _redis_cli = '/usr/bin/redis-cli'
    _stat_regex = re.compile(ur'(\w+):([0-9]+\.?[0-9]*)\r')

    def __init__(self, port='', passwd=None, host='10.135.17.188'):
        self._cmd = '%s -h %s -p %s info' % (self._redis_cli, host, port)
        if passwd not in ['', None]:
            self._cmd = "%s -a %s" % (self._cmd, passwd)

    def stats(self):
        ' Return a dict containing redis stats '
        info = commands.getoutput(self._cmd)
        return dict(self._stat_regex.findall(info))


class Redislatency: #该类实现返回redis各实例的延迟时间
    # 如果你是自己编译部署到redis，请将下面的值替换为你到redis-cli路径
    _redis_cli = '/usr/bin/redis-cli'
    _stat_regex = re.compile(ur'(\w+):([0-9]+\.?[0-9]*)\r')

    def __init__(self, port='', passwd=None, host='10.135.17.188'):
        self._latency = '%s -h %s -p %s --latency' % (self._redis_cli, host, port)
        if passwd not in ['', None]:
            self._latency = "%s -a %s" % (self._latency, passwd)

    def latency_time(self):
        cmd = "%s > redis_file &" % (self._latency)
        os.popen(cmd)
        time.sleep(5)
        os.popen("ps -ef | grep latency | grep -v grep | awk '{print $2}'|xargs kill -9")
        for line in open(path):  # 打开path文件
            val = line.split()
            value = float(val[-3])
            print val[-2].replace('(', '')
            os.popen('rm -fr redis_file')
            return value
    #实现过程：命令行打入后台执行，且将结果输出到文件中，延时5秒（redis在插入数据），kill该进程，读取文件中的结果，最后将临时文件删除


def main():
    # inst_list中保存了redis配置文件列表，程序将从这些配置中读取port和password，建议使用动态发现的方法获得，如：
    insts_list = [i for i in commands.getoutput("find /data/redis/conf/ -name 'redis*.conf'").split('\n')]
    key1 = 'connect.status'
    vtype1 = vtype2 = 'GAUGE'
    key2 = 'latency.time'
    monit_keys = [
        ('connected_clients', 'GAUGE'),
        ('blocked_clients', 'GAUGE'),
        ('used_memory', 'GAUGE'),
        ('used_memory_rss', 'GAUGE'),
        ('mem_fragmentation_ratio', 'GAUGE'),
        ('total_commands_processed', 'COUNTER'),
        ('rejected_connections', 'COUNTER'),
        ('expired_keys', 'COUNTER'),
        ('evicted_keys', 'COUNTER'),
        ('keyspace_hits', 'COUNTER'),
        ('keyspace_misses', 'COUNTER'),
        ('keyspace_hit_ratio', 'GAUGE'),
    ]

    for inst in insts_list:
        port = commands.getoutput(
            "sed -n 's/^port *\([0-9]\{4,5\}\)/\\1/p' %s" %
            inst)
        passwd = commands.getoutput(
            "sed -n 's/^requirepass *\([^ ]*\)/\\1/p' %s" %
            inst)
        print port, passwd

        try:
            conn = RedisStats(port, passwd)
            stats = conn.stats()
            print len(stats), conn
            # print "连接的状态是：：：：：：：", stats
        except Exception as e:
            print '连接异常，程序退出'
            continue
        if int(len(stats)) == 0:
            for key, vtype in monit_keys:
                value = value1 = value2 = -1
                one = redis_value(key, vtype, value, port)
                post_url(one)
            status = redis_value(key1, vtype1, value1, port)
            latencytime = redis_value(key2, vtype2, value2, port)
            post_url(status + latencytime)

        else:
            for key, vtype in monit_keys:
                if key == 'keyspace_hit_ratio':
                    try:
                        value = float(stats['keyspace_hits']) / (
                            int(stats['keyspace_hits']) + int(stats['keyspace_misses']))
                    except ZeroDivisionError:
                        value = 0
                elif key == 'mem_fragmentation_ratio':
                    value = float(stats[key])
                else:
                    try:
                        value = int(stats[key])
                    except:
                        continue
                one = redis_value(key, vtype, value, port)
                post_url(one)
            value1 = 1
            status = redis_value(key1, vtype1, value1, port)
            value2 = Redislatency(port, passwd).latency_time()
            latencytime = redis_value(key2, vtype2, value2, port)
            post_url(status + latencytime)


def redis_value(key, vtype, value, port):
    step = 60
    ip = socket.gethostname()
    timestamp = int(time.time())
    metric = "redis"
    endpoint = ip
    tags = 'port=%s' % port
    p = []
    i = {
        'Metric': '%s.%s' % (metric, key),
        'Endpoint': endpoint,
        'Timestamp': timestamp,
        'Step': step,
        'Value': value,
        'CounterType': vtype,
        'TAGS': tags
    }
    p.append(i)
    print i
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
