# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 22:46
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : Main.py


import unittest
import os
from importlib import reload
from src.common import Utils
from sys import argv
from src.common import TestRunner
from src.common import Logger


def runTest(case_dir, patter):
    reload(TestRunner)
    discover = unittest.defaultTestLoader.discover(case_dir + "\\testcases", pattern=patter)
    runner = TestRunner.AutoTestRunner()
    result, infos = runner.run(discover)
    return result, infos


def run(cadir):
    filename = Utils.createFolder(cadir[0])  # 创建文件夹
    log = Logger.Loger()
    log.info(cadir[2] + u"测试开始")
    log.info(u"开始创建文件夹和文件")
    log.info(u"日志文件：" + filename[0])
    log.info(u"报告文件：" + filename[1])
    log.info(u"文件夹和文件创建成功")
    log.info(u"开始执行测试用例")
    result, infos = runTest(cadir[0], cadir[1])  # 收集和执行测试用例
    log.info(u"测试用例执行完成，开始写入报告")
    if cadir[2] == "functiontest":
        Utils.createReport(result, infos, filename, cadir[3])  # 测试结果写入报告
    log.info(u"报告写入结束，测试结束")
    log.info(u"开始发送邮件……")
    isSuccess = Utils.sendMail(filename[1], cadir[3])
    log.info(isSuccess)
    log.info("================================================================\n")


if __name__ == '__main__':
    projectpath = os.path.dirname(os.path.realpath(__file__))
    test_dir = projectpath + '\\functiontest\\'  # 功能测试用例路径
    test_dir1 = projectpath + '\\interfacetest\\'  # 接口测试用例路径
    casedirs = []
    # argv=["","all"]
    if argv[1] == "interface":
        casedirs.append([test_dir1, "*TestCase.py", "interfacetest", "接口"])
    elif argv[1] == "function":
        casedirs.append([test_dir, "TestCase*.py", "functiontest", "功能"])
    else:
        casedirs.append([test_dir1, "*TestCase.py", "interfacetest", "接口"])
        casedirs.append([test_dir, "TestCase*.py", "functiontest", "功能"])

    for cadir in casedirs:
        run(cadir)