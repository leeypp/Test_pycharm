#!/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'leeypp'
#!/bin/env python
# -*- coding: utf-8 -*-
import time
import os
import MySQLdb
path = '/data/work/open-falcon/plugin/Aliyun'
# path的格式为--外网ip 内网ip 主机名 创建时间
# from elasticsearch import Elasticsearch  用于上传到elk日志系统


def main(day):

    i = day
    print 'The day before yestodday: ', i
    for line in open(path):  # 处理path文件
        val = line.split()
        eth1 = val[0]
        eth0 = val[1]
        name = val[2]
        print name, type(name)
        db = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='abcdef',
            db='falcon_portal',
            port=3306)  # 连接数据库
        cursor = db.cursor()
        print eth0
        sql = "select hostname from host where ip='%s';" % eth0  #同open-falcon中的数据对比
        print sql
        cursor.execute(sql)
        results = cursor.fetchall()
        hostname = str(results)
        # hostname=hostname.replace('-','_').replace(',),)','').replace('((','').replace("'","")
        hostname = hostname.replace(',),)', '').replace('((', '').replace("'", "")  # 处理hostname
        if hostname == '()':  # 判断该ip是否存在于open-falcon表中
            hostname = name
            from1 = 'local_file'
        else:
            hostname = hostname
            from1 = 'open_falcon'
        print eth1, eth0, hostname, from1
        if from1 == 'open_falcon':  # 如果主机信息存在于falcon表中，则进行扫描端口处理，否则退出本次循环
            pass
        else:
            continue  # 退出本次循环
        return1 = os.popen("nmap -n -p T:1-65535 -sS %s| grep tcp" % eth1)
        m = return1.readlines()
        for line in m:
            rows = line.strip('\n')
            port = rows.split("/")[0]
            if port == '53' or port == '80' or port == '5666' or port == 111:  # 过滤正常开启的端口
                continue
            else:
                port = port
            print port, type(port)
            # doc = {"hostname":"%s"%hostname,"eth1":"%s"%eth1,"eth0":"%s"%eth0,"@timestamp":day_yestoday,"port":"%s"%port}
            doc = hostname + " " + eth1 + " " + eth0 + " " + port
            f = open('out.csv', 'a+')
            print >> f, doc
            i = 1
            index_time = time.strftime("%Y.%m.%d", time.localtime())
            day_index = 'portscan-%s' % (index_time)
'''
            while (i<10):
                i = i+1
                try:
                    res = es.index(index=day_index,doc_type="apipython",body=doc)
                    print res
                except:
                    print 'index error****',doc
                else:
                    i = 100
'''


if __name__ == '__main__':
    # commands.getoutput(' ps -ef|grep %s|grep -v grep|wc -l ' % os.path.basename(sys.argv[0]))
    proc = 1
    if int(proc) < 5:
        for i in range(0, 1):
            main(i)
# 脚本存在的问题：未采用多线程，当ip过多时，耗时过长。日后改进