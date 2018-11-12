# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:27
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : IndexPage.py



from src.functiontest.models import BasePage
from selenium.webdriver.common.by import By

# 首页
class Index(BasePage):
    user_menu = (By.ID, "userSetting")
    user_info = (By.XPATH, "//a[@href='user/userInfo']")
    language_span = (By.ID, "changeLanguage")
    chinese_li = (By.XPATH, "//li[@value='zh_cn']")
    english_li = (By.XPATH, "//li[@value='en']")

    def __init__(self, driver):
        super().__init__(self, driver)
        self.driver = driver
        self.usermenu = self.find_element(*self.user_menu)
        self.userinfo = self.find_element(*self.user_info)
        self.languagespan = self.find_element(*self.language_span)
        self.chinase = self.find_element(*self.chinese_li)
        self.english = self.find_element(*self.english_li)

    def chengeLanguage(self):
        self.languagespan.click()
        self.english.click()
        self.driver.implicitly_wait(5)