# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:40
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : TestCase_LoginandIndex.py


from src.functiontest.testcases.BaseTestCase import BaseCaseClass
from src.functiontest.models.LoginPage import LoginPage
from src.functiontest.models.IndexPage import Index
from src.functiontest.futil import Util


class CheckLogin(BaseCaseClass):

    def runTest(self):
        """
        name:测试标题为：XX系统
        verbosity:0
        :return:
        """
        self.driver.get(self.url)
        loginPage = LoginPage(self.driver)
        self.assertEqual(loginPage.driver.title, u"XX系统", "标题不正确")


class CheckIndex(BaseCaseClass):

    def runTest(self):
        """
        name:测试首页存在个人资料选项
        verbosity:0
        """
        self.driver.get(self.url)
        # self.driver.switch_to_window(self.driver.window_handles[1])
        loginPage = LoginPage(self.driver)
        loginPage.login("admin", "xxx")
        indexPage = Index(self.driver)
        indexPage.chengeLanguage()
        indexPage = Index(self.driver)
        indexPage.usermenu.click()
        Util.highLight(self.driver, indexPage.userinfo)
        self.assertEqual(indexPage.userinfo.text, "Personal Data", "标题不正确")