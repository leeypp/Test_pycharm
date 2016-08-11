#!/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import MySQLdb
from threading import Thread

path = '/data/work/open-falcon/plugin/Aliyun11'


class pingThread(Thread):

    def __init__(self, ip):
        Thread.__init__(self)
        self.eth1 = ip[0]
        self.eth0 = ip[1]
        self.name = ip[2]

    def run(self):
        db = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='aC2Ia',
            db='falcon_portal',
            port=3306)
        cursor = db.cursor()
        print self.eth0
        sql = "select hostname from host where ip='%s';" % self.eth0
        print sql
        cursor.execute(sql)
        results = cursor.fetchall()
        hostname = str(results)
        # hostname=hostname.replace('-','_').replace(',),)','').replace('((','').replace("'","")
        hostname = hostname.replace(',),)', '').replace('((', '').replace("'", "")  # 处理hostname
        if hostname == '()':
            hostname = self.name
            from1 = 'local_file'
        else:
            hostname = hostname
            from1 = 'open_falcon'
        print hostname, from1, self.eth0, self.eth1
        if from1 != 'open_falcon':
            return None
        return1 = os.popen(
            "nmap -n -p T:1-65535 -sS %s| grep tcp" %
            (self.eth1))
        m = return1.readlines()
        for line in m:
            rows = line.strip('\n')
            port = rows.split("/")[0]
            if port == '53' or port == '80' or port == '5666' or port == 111:  # 将正常开启的端口过滤掉
                continue
            else:
                port = port
            print port, type(port)
            # doc = {"hostname":"%s"%hostname,"eth1":"%s"%eth1,"eth0":"%s"%eth0,"@timestamp":day_yestoday,"port":"%s"%port}
            doc = hostname + " " + eth1 + " " + eth0 + " " + port
            f = open('out.csv', 'a+')
            print >> f, doc
        db.close()


T_thread = []
for line in open(path):  # 打开path文件
    val = line.split()
    eth1 = val[0]
    eth0 = val[1]
    name = val[2]
    list = [eth1, eth0, name]
    print list
    t = pingThread(list)
    ll = T_thread.append(t)
for ip in range(len(T_thread)):
    T_thread[ip].start()

'''
path文件格式
外网ip 内网ip 注释
'''
