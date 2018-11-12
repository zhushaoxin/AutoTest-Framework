# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:48
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : InterfaceTestCase.py


import unittest
import requests
from src.interfacetest.iutil import DataEngine
from src.interfacetest.iutil import HttpEngine
from src.interfacetest.testcases.BaseTestCase import BaseCase
import datetime
from src.common import Utils
from configparser import ConfigParser


class DoInterfaceTest(BaseCase):

    def runTest(self):
        sttime = datetime.datetime.now()
        domain, caselist, header = DataEngine.getCase()  # 读取Excel获取用例数据
        self.loginfo("domain:" + domain)
        self.loginfo("header:" + str(header) + "\n")
        resultlist = []

        for case in caselist:
            '''
            case[0]  序号        case[1]  优先级    case[2]  模块        case[3]  用例描述    case[4]  是否登录
            case[5]  接口url    case[6]  方法        case[7]  参数        case[8]  期望结果
            '''
            self.loginfo("url:" + case[5])
            self.loginfo("method:" + case[6])

            starttime = datetime.datetime.now()
            url = domain + case[5]  # 拼接请求url
            method = case[6]  # 请求方法：post、get、delete
            data = eval(case[7])  # 请求数据

            isexcept = False
            if case[4] == "Y":  # 是否需要登录
                sess, isexcept = HttpEngine.login()  # 返回登录的session和登录是否异常
            else:
                sess = requests.Session()

            result = "Failed"
            if isexcept:  # 如果登录异常，直接中断
                actualre = sess
            else:  # 没有登录异常，继续执行
                re, isexcept = HttpEngine.getData(sess, url, data, header, method)  # 发送请求并获取响应结果
                if isexcept:  # 如果请求异常，直接中断
                    actualre = re
                else:
                    result, actualre = DataEngine.resultCheck(re, case[8])  # 结果匹配

            if "password" in case[7]:
                temp = eval(case[7])
                temp['password'] = "******"
                case[7] = temp
            self.loginfo("data:" + str(case[7]))
            self.loginfo("结果:" + result + ", 请求返回：" + actualre + "\n")

            stoptime = datetime.datetime.now()
            takentime = (stoptime - starttime).microseconds / 1000  # 获取时间差，单位为毫秒
            if len(actualre) > 43:
                actualre = actualre[:43] + " ..."
            actualre = actualre.replace('<', '&lt;').replace('>', '&gt;')

            result_temp = [case[2], case[3], case[5], case[7], actualre, result, takentime]
            resultlist.append(result_temp)
        sptime = datetime.datetime.now()
        passcount, failcount = DataEngine.countResult(resultlist)  # 统计结果
        totalcount = len(resultlist)
        tktime = (sptime - sttime).microseconds / 1000 / 1000.000  # 整体耗时，单位为秒
        sttime = sttime.strftime("%Y-%m-%d %H:%M:%S")
        tinfo = {'starttime': sttime, 'takentime': tktime, 'pass': passcount, 'fail': failcount, 'total': totalcount}
        conf = ConfigParser()
        conf.read("config.conf")
        reportfile = conf.get("report", "report_path")
        logfile = conf.get("report", "log_path")
        Utils.createInterfaceReport(resultlist, tinfo, reportfile, logfile)


if __name__ == "__main__":
    unittest.main()