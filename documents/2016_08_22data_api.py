#!/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'leeypp'
import requests
import time
import json

end = int(time.time()) # 起始时间戳
start = end - 3600*24*int(raw_input("请输入你要查询过去几天的数据："))  # 截至时间戳

print "请输入你要查询的主机名和counter"
d = {
        "start": start,
        "end": end,
        "cf": "AVERAGE",
        "endpoint_counters": [
            {
                "endpoint": raw_input("please input hostname:"),
                "counter":  raw_input("please input counter:"),
            },
        ],
}

query_api = "http://127.0.0.1:9966/graph/history"
r = requests.post(query_api, data=json.dumps(d))
print r.text
'''
start: 要查询的历史数据起始时间点（为UNIX时间戳形式）
end: 要查询的历史数据结束时间点（为UNIX时间戳形式）
cf: 指定的采样方式，可以选择的有：AVERAGE、MAX、MIN
endpoint_counters: 数组，其中每个元素为 endpoint和counter组成的键值对, 其中counter是由metric/sorted(tags)构成的，没有tags的话就是metric本身。
query_api: query组件的监听地址 + api
'''