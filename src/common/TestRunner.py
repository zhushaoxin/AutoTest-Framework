# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 22:46
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : TestRunner.py


import sys
import time
import datetime
import unittest
from PIL import ImageGrab
import random
import configparser
import re
from src.common import Logger

log = Logger.Loger()
TestResult = unittest.TestResult


class _TestResult(TestResult):

    def __init__(self, verbosity=1):
        super().__init__(self)
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.verbosity = verbosity
        self.results = {}

    def startTest(self, test):
        TestResult.startTest(self, test)
        class_name = test.__class__.__name__
        if class_name in self.results.keys():
            self.results[class_name].setdefault(test, {})
        else:
            self.results.setdefault(class_name, {})
            self.results[class_name].setdefault(test, {})
        casename = None
        verbosity = None
        if test._testMethodDoc != None:
            casename = (re.findall(r"name:(.+?)\n", test._testMethodDoc))[0]
            verbosity = (re.findall(r"verbosity:(.+?)\n", test._testMethodDoc))[0]
        (self.results[class_name])[test].setdefault("name", casename)
        (self.results[class_name])[test].setdefault("verbosity", verbosity)
        starttime = datetime.datetime.now()
        # starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        (self.results[class_name])[test].setdefault("starttime", starttime)
        log.info("————————————————————————————————————————————————————————————")
        log.info("%s start testing" % test)

    def stopTest(self, test):
        TestResult.stopTest(self, test)
        stoptime = datetime.datetime.now()
        # stoptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        class_name = test.__class__.__name__
        (self.results[class_name])[test].setdefault("stoptime", stoptime)
        log.info("%s stop testing" % test)
        log.info("————————————————————————————————————————————————————————————\n")

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        class_name = test.__class__.__name__
        (self.results[class_name])[test].setdefault("Result", "Pass")
        (self.results[class_name])[test].setdefault("Reason", "")
        (self.results[class_name])[test].setdefault("Screenshoot", "")
        log.info("%s is Pass" % test)  # 打印成功信息
        log.info("%s is Pass" % test)

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        # 失败截图
        addr = self.getScreen()
        class_name = test.__class__.__name__
        (self.results[class_name])[test].setdefault("Result", "Error")
        (self.results[class_name])[test].setdefault("Reason", self._exc_info_to_string(err, test))
        (self.results[class_name])[test].setdefault("Screenshoot", addr)
        log.info("%s is Error" % test)
        log.info(self._exc_info_to_string(sys.exc_info(), test))

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        addr = self.getScreen()
        class_name = test.__class__.__name__
        (self.results[class_name])[test].setdefault("Result", "Failed")
        (self.results[class_name])[test].setdefault("Reason", self._exc_info_to_string(err, test))
        (self.results[class_name])[test].setdefault("Screenshoot", addr)
        log.info("%s is Failed" % test)
        log.info(self._exc_info_to_string(sys.exc_info(), test))  # 打印失败信息

    def addSkip(self, test, reason):
        self.skip_count += 1
        TestResult.addSkip(self, test, reason)
        class_name = test.__class__.__name__
        if class_name in self.results.keys():
            self.results[class_name].setdefault(test, {})
        else:
            self.results.setdefault(class_name, {})
        (self.results[class_name])[test].setdefault("Result", "Skip")
        (self.results[class_name])[test].setdefault("Reason", reason)
        (self.results[class_name])[test].setdefault("Screenshoot", "")
        log.info("%s is skiped, reason is %s" % (test, reason))

    def getScreen(self):
        # 失败截图
        conf = configparser.ConfigParser()
        conf.read("config.conf")
        ssFolder = conf.get("report", "screen_path")
        screenshootpath = ssFolder + "\\"
        im = ImageGrab.grab()
        rand = random.randint(1000, 9999)
        addr = screenshootpath + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(rand) + ".png"
        im.save(addr)
        return addr


class AutoTestRunner():
    """
    """

    def __init__(self, stream=sys.stdout, verbosity=1):
        self.stream = stream
        self.verbosity = verbosity
        self.startTime = datetime.datetime.now()

    # 基于用例的优先级筛选用例
    def baseVerbosityRun(self, test, verbosity):
        suite = unittest.TestSuite()
        for suites in test._tests:
            for sui in suites._tests:
                if sui.countTestCases > 0:
                    for s in sui:
                        if s._testMethodDoc != None:
                            vb = (re.findall(r"verbosity:(.+?)\n", s._testMethodDoc))[0]
                            if int(vb) == verbosity:
                                suite.addTest(s)
        return suite

    def run(self, test):
        result = _TestResult(self.verbosity)
        # suite = self.baseVerbosityRun(test,1) #按优先级执行
        # suite(result)
        test(result)
        '''
                        将失败的用例加入suite，为失败重跑做准备
        suite = unittest.TestSuite()
        teresult = result.results
        for case in teresult.keys():
            if (teresult[case])["Result"] == "Failed":
                suite.addTest(case)
        '''

        self.stopTime = datetime.datetime.now()
        timeTaken = (self.stopTime - self.startTime).seconds
        run = result.testsRun
        log.info("Ran %d case%s in %.3fs" % (run, run != 1 and "s" or "", timeTaken))
        timeTaken = str(datetime.timedelta(seconds=timeTaken))
        infos = {"Success": result.success_count, "Fail": result.failure_count, "Error": result.error_count,
                 "Skip": result.skip_count, "CaseNum": run,
                 "StartTime": self.startTime.strftime("%Y-%m-%d %H:%M:%S"),
                 "StopTime": self.stopTime.strftime("%Y/%m/%d %H:%M:%S"), "TakeTime": timeTaken}

        return (result, infos)


class TestProgram(unittest.TestProgram):
    def runTests(self):
        if self.testRunner is None:
            self.testRunner = AutoTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)


main = TestProgram

if __name__ == "__main__":
    main(module=None)