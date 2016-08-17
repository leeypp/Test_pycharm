#!/usr/bin/python
# -*- coding:utf-8 -*-
import difflib
import sys

try:
    textfile1=sys.argv[1]
    textfile2=sys.argv[2]
    print "捕获到的第一个值是：",textfile1
    print '捕获到的第二个值是：',textfile2
except Exception,e:
    print "Error:"+str(e)
    print str(e)
    print "Usage: simple3.py filename1 filename2"
    sys.exit()
# sys.argv[]是用来获取命令行参数的，sys.argv[0]表示代码本身文件路径;比如在CMD命令行输入 “python  test.py -help”，那么sys.argv[0]就代表“test.py”
# sys.startswith() 是用来判断一个对象是以什么开头的，比如在python命令行输入“'abc'.startswith('ab')”就会返回True

def readfile(filename):
    try:
        fileHandle = open (filename, 'rb' )
        text=fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as error:
       print('Read file Error:'+str(error))
       sys.exit()

if textfile1=="" or textfile2=="":
    print "Usage: simple3.py filename1 filename2"
    sys.exit()


text1_lines = readfile(textfile1)
text2_lines = readfile(textfile2)

d = difflib.HtmlDiff()
print d.make_file(text1_lines, text2_lines)
##python *.py nginx.conf1 nginx.conf2
