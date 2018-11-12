# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:27
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : LoginPage.py



from src.functiontest.models import BasePage
from selenium.webdriver.common.by import By

# 登录
class LoginPage(BasePage):
    user_name = (By.NAME, "username")
    pass_word = (By.NAME, "password")
    btn_login = (By.CLASS_NAME, "login-btn")

    def __init__(self, driver):
        super().__init__(self, driver)
        self.driver = driver
        self.input_username = self.find_element(*self.user_name)
        self.input_password = self.find_element(*self.pass_word)
        self.btn_login = self.find_element(*self.btn_login)

    def login(self, username, password):
        self.input_username.send_keys(username)
        self.input_password.send_keys(password)
        self.btn_login.click()