# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 23:47
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : HttpEngine.py


import requests

def getData(s, url, data, header, method):
    re = object
    isexcept = False
    if method == "post":
        try:
            re = s.post(url, headers=header, data=data)
        except requests.exceptions.ConnectionError as e:
            re = e
            isexcept = True

    if method == "get":
        try:
            re = s.get(url, headers=header, data=data)
        except requests.exceptions.ConnectionError as e:
            re = e
            isexcept = True

    if method == "delete":
        try:
            re = s.delete(url + "/" + data)
        except requests.exceptions.ConnectionError as e:
            re = e
            isexcept = True

    if method == "put":
        try:
            re = s.put(url)
        except requests.exceptions.ConnectionError as e:
            re = e
            isexcept = True

    return re, isexcept


def login():
    isexcept = False
    try:
        url = "http://baidu.com/login"
        header = {"Referer": "http://baidu.com"}
        data = {"username": "admin", "password": "xxx"}
        s = requests.Session()
        s.post(url, headers=header, data=data)
    except requests.exceptions.ConnectionError as e:
        s = e
        isexcept = True
    return s, isexcept