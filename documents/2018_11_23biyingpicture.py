#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = 'ross'

import os
import json
from urllib import request

var_BingPic_Dir = "D:\\image"
# If the index is 0,it will get the pic json string of current day;
# If the index is 1,it will get the pic json string of last day.
var_CurrentDayIndex = 0
var_Bing_Base_Url = "http://cn.bing.com"
var_BingPic_Url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=" + \
    str(var_CurrentDayIndex) + "&n=1&nc=1361089515117&FORM=HYLH1"

# Function:  Get the path to storage the pic.获取存储图片目录


def Get_Path_to_Storage_Pic(enddate):
    varPicPath = var_BingPic_Dir.strip()  # except the space
    if 0 == len(varPicPath):
        return None
    if not os.path.exists(varPicPath):
        os.makedirs(varPicPath, exist_ok=True)
        print("Create directory success,the pass is:%s" % (path))
    else:
        #print("The directory is exist!")
        pass
    varPicPath += "\\" + enddate + "_"  # Get the full path
    return varPicPath

# Function:  Get the pictures by the given url and storage the pic to local.通过给定的URL获取图片并将图片存储到本地
# In:        The url to get the bing pic json string
# Out：       None


def Get_Pic():
    BingPic_Url = var_BingPic_Url
    print("Get pictures from: %s" % BingPic_Url)
    webdata = request.urlopen(BingPic_Url)
    jsStr = webdata.read()
    infojson = jsStr.decode('utf-8')
    picjson = json.loads(infojson)
    images = picjson['images']
    enddate = images[0]['enddate']
    url = images[0]['url']
    picUrl = var_Bing_Base_Url + url  # 文件标准链接
    print('Get pictures url:', picUrl)
    basename = os.path.basename(url)  # 获取图片原始文件名

    picStoragePath = Get_Path_to_Storage_Pic(enddate)  # 文件存储路径

    # 存储原图片文件
    try:
        request.urlretrieve(picUrl, (picStoragePath + basename))
        print(
            'Storage picture pic success!,The pic full path is : ',
            picStoragePath + basename)
    except IOError:
        print("Storage picture pic failed!")
        os.system("pause")
        return None

    # 存储接口中图片相关json信息
    info_log = picStoragePath + 'json.log'
    try:
        fo = open(info_log, 'a')
        fo.write(infojson.replace(u'\xa9', u''))
        fo.write('\n')
    except IOError:
        print('Storage picture info failed!')
    else:
        print('Storage picture pic success!,The info full path is : ', info_log)
        fo.close()


if __name__ == "__main__":
    Get_Pic()
# 本文件用于下载每日biying首页背景图片，并将文件按日期命名，将图片文件和文件的info信息存储在固定目录下
