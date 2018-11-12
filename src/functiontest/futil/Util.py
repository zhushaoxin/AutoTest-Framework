# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:26
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : Util.py


# 高亮显示元素
def highLight(driver,element):
    js = '''
        element = arguments[0];
        element.setAttribute('style','border: 3px solid red;')
        '''
    driver.execute_script(js,element)