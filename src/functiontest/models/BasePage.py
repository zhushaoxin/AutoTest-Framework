# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:27
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : BasePage.py


from selenium import webdriver

TIME_OUT = 5  # 超时时间


class BasePage(object):
    def __init__(self, driver):
        """初始化浏览器"""
        self.driver = driver
        try:
            self.driver = webdriver.Chrome()
        except Exception as e:
            print(e)

    def opendriver(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(TIME_OUT)

    def find_element(self, by, value):
        """查找元素"""
        try:
            return self.driver.find_element(by=by, value=value)
        except Exception as e:
            print(e)

    def find_elements(self, by, value):
        """查找元素集合"""
        try:
            return self.driver.find_elements(by=by, value=value)
        except Exception as e:
            print(e)

    def is_element_isexist(self, By, Value):
        """判断元素是否存在"""
        try:
            self.driver.find_element(by=By, value=Value)
            return True
        except Exception as e:
            print(e)
            return False

    def close(self):
        """当前关闭浏览器tab"""
        try:
            self.driver.close()
        except Exception as e:
            print(e)

    def quit(self):
        """退出浏览器进程"""
        try:
            self.driver.quit()
        except Exception as e:
            print(e)