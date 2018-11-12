# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:47
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : DataEngine.py


from src.interfacetest.iutil.XlsEngine import XlsEngine_rd
import os

'''获取用例'''
def getCase():
    filepath = os.path.abspath('.')
    filename =  filepath + "/interfacetest/Data/InterfaceData.xlsx"
    data = XlsEngine_rd(filename)
    data.xlrd_open()
    sheet = data.xlrd_object.sheet_by_index(0)
    rows = sheet.nrows
    domain = sheet.cell_value(1,1)
    header_temp = sheet.cell_value(2,1)
    header=eval(header_temp)
    case_list=[]
    for i in range(3,rows):
        case_list.append(sheet.row_values(i))
    return domain,case_list,header

'''结果检查'''
def resultCheck(actual_result, expect_result):
    result = "Failed"
    actualre = actual_result.content
    area = (expect_result.split(':'))[0]
    expect = (expect_result.split(':'))[1]
    if area == "response_code":
        if str(actual_result.status_code) == expect:
            result = "Pass"
            actualre = "response_code:"+expect
    if area == "content":
        expect = expect_result.replace("content:","").encode('utf-8')
        actual = actual_result.content
        if expect in str(actual):
            result = "Pass"
            actualre = expect
    return result,actualre

'''结果统计'''
def countResult(resultlist):
    passcount=0
    failcount=0
    for result in resultlist:
        if result[5] == 'Pass':
            passcount+=1
        else:
            failcount+=1
    return passcount,failcount