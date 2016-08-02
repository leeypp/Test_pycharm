#!/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'leeypp'
import os
import commands
import time


def mem():
    sum = 0
    n = 1
    total = os.popen("free -m |grep Mem | awk '{print $2}'").read()
    free = int(os.popen("free -m |grep Mem | awk '{print $4}'").read()) + \
           int(os.popen("free -m |grep Mem | awk '{print $6}'").read()) + \
           int(os.popen("free -m |grep Mem | awk '{print $7}'").read())
    percent = free * 1.0 / int(total)
    print "你好，内存的空闲率为：", percent * 100
    while (percent < 0.15) and (sum < 10):
        # 因为此脚本是定时任务，当清理10次(5*10=50s)内存还有溢出时退出循环，等待下一分钟再次执行
        total = os.popen("free -m |grep Mem | awk '{print $2}'").read()
        free = int(os.popen("free -m |grep Mem | awk '{print $4}'").read()) + \
               int(os.popen("free -m |grep Mem | awk '{print $6}'").read()) + \
               int(os.popen("free -m |grep Mem | awk '{print $7}'").read())
        percent = free * 1.0 / int(total)
        print percent
        commands.getoutput('sync && echo 1 > /proc/sys/vm/drop_caches')
        print time.ctime(),"clean up memory success"
        time.sleep(5)
        sum = sum + n
    else:
        pass
        print "memfree.percent is ok"
mem()
