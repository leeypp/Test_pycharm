#!/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'leeypp'


print "hello world!"
sum = n = 1
name = " "
sum1 = i = 0
# 两种方法计算汇率，本金10000，汇率3.25%，何时翻番
while n <= 2:
    print n
    print "time is over", n
    print n
    n = 1.0325 * n
    sum = sum + 1
print sum
year = 0
mon = 10000
while mon < 20000:
    mon = mon + mon * 0.0325
    year = year + 1
print year
while name != "":  # 输入数字，当直接按回车的时候循环退出并打印结果
    name = raw_input("please input your number")
    if name!='':
        name = int(name)
        i = i + 1
        sum1 = sum1 + name
print "最终的结果是：", sum1 * 1.0 / i
print "sucess"