#!/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'leeypp'
import difflib

text1 = '''jkjkljlk
jkjlk
jlkl
jkll
'''
text2 = '''jkljlk
jkljlkjlk
jkljlk
jlkjlk
jkl
'''
text_lines1 = text1.splitlines()
text_lines2 = text2.splitlines()

d = difflib.HtmlDiff()
print d.make_file(text_lines1, text_lines2)
# 采用HtmlDiff（）类的make_file（）方法将对比后的结果生成美观的HTML文档，增加可读性
