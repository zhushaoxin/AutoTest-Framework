# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:48
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : BaseTestCase.py


import unittest
from src.common import Logger

log = Logger.Loger()


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.loginfo("============================================================")
        self.loginfo("%s is start" % self)
        # print self._attribute.decode('utf=8')

    def tearDown(self):
        self.loginfo('test is stop')
        self.loginfo("============================================================\n")
    @staticmethod
    def loginfo(msgstr):
        log.info(msgstr)


if __name__ == "__main__":
    unittest.main()