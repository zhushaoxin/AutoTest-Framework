# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:37
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : BaseTestCase.py


import unittest
from src.common import Logger
from selenium import webdriver

log = Logger.Loger()


class BaseCaseClass(unittest.TestCase):

    def setUp(self):
        #         options = webdriver.ChromeOptions()
        #         options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        #         options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default");
        #         self.driver = webdriver.Chrome(chrome_options=options)
        self.driver = webdriver.Ie()
        self.url = "http://baidu.com"

    def tearDown(self):
        self.driver.close()

    @staticmethod
    def loginfo(msgstr):
        log.info(msgstr)