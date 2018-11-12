# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 22:46
# @Author  : zhushaoxin
# @Email   : 185250613@qq.com
# @File    : Utils.py


import configparser
import time
import os
# import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime
import base64
# import socket

"""
 公共方法，如创建报告文件夹、生成测试报告、发送邮件
"""

# 创建报告文件夹、日志文件夹、截图文件夹、日志文件、报告文件
def createFolder(test_path):
    # conf = ConfigParser.ConfigParser()
    # conf.read("config.conf")
    # reportFolder = conf.get("result", "resultpath") + time.strftime('%Y-%m-%d', time.localtime(time.time()))
    reportFolder = test_path + "Report\\" + time.strftime('%Y-%m-%d', time.localtime(time.time()))
    log_path = reportFolder + "\\Logs"
    screen_path = reportFolder + "\\Screenshoots"
    report_path = reportFolder + "\\Report"
    pathlist = [report_path, log_path, screen_path]
    for paths in pathlist:
        if os.path.exists(paths):
            pass
        else:
            os.makedirs(paths)
    logFile = log_path + "\\" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + ".log"
    f = open(logFile, 'a')
    f.close()

    reportname = report_path + "\\TestReport-" + time.strftime("%Y-%m-%d-%H-%M-%S",
                                                               time.localtime(time.time())) + ".html"
    f = open(reportname, 'w')

    htmlStr = '''
            <html>
            <head>
            <meta charset='utf-8' />
            <style>
            body{counter-reset:num;}
            li{list-style: none;text-indent:10px;}
            li:after{content: counter(num);counter-increment:num;}
            pre { 
                white-space: pre-wrap;
                word-wrap: break-word; 
                display:block;
                padding:5px;
                font-size:13px;
                color:#333;
                background-color:#f5f5f5;
                border:1px solid #ccc;
                border-radius:4px;
                font-family:'Consolas';
            }

            h1 {
                font-size: 16pt;
                color: gray;
            }
            .heading {
                margin-top: 0ex;
                margin-bottom: 1ex;
            }

            .heading .attribute {
                margin-top: 1ex;
                margin-bottom: 0;
            }

            .heading .description {
                margin-top: 2ex;
                margin-bottom: 3ex;
            }

            /* -- table --- */
            table {
            border-collapse: collapse; /* IE7 and lower */
            border-spacing: 0;
            width: 100%;    
            }

            .bordered {
                border: solid #ccc 1px;
                -moz-border-radius: 5px;
                -webkit-border-radius: 5px;
                border-radius: 5px;
                -webkit-box-shadow: 0 1px 1px #ccc; 
                -moz-box-shadow: 0 1px 1px #ccc; 
                box-shadow: 0 1px 1px #ccc;

            }

            .bordered td {
                border: 1px solid #ccc;
                padding: 5px; 
                font-size:14px;  
            }

            .header_row {
                font-weight: bold;
                background-color: #dce9f9;
            }

            /* -- css div popup --- */
            a {
                color:#428bca;
                text-decoration:none;
            }

            a:hover {
                text-decoration:underline;
            }

            .popup_window {
                display: none;
                /*position: relative;*/
                /*border: solid #627173 1px; */
                padding: 10px;
                background-color: #E6E6D6;
                text-align: left;
                font-size: 8pt;
                width: 500px;
            }

            .hiddenRow {
                display: none;
            }

            .displayRow {
                display: block;
            }
            .testcase   { margin-left: 2em; color: #000; font-weight: bold;}

            /* -- report -- */
            #show_detail_line {
                margin-top: 3ex;
                margin-bottom: 1ex;
            }

            </style>

            <script language="javascript" type="text/javascript">
            function showCase(level) {
                trs = document.getElementsByTagName("tr");
                for (var i = 0; i < trs.length; i++) {
                    tr = trs[i];
                    id = tr.id;
                    if (id.substr(0,2) == 'ft') {
                        if (level == 0) {
                            tr.className = 'none';
                        }
                        if (level == 1) {
                            tr.className = 'hiddenRow';
                        }
                        if (level == 2) {
                            tr.className = 'none';
                        }
                        if (level == 3) {
                            tr.className = 'hiddenRow';
                        }
                    }
                    if (id.substr(0,2) == 'pt') {
                        if (level == 0) {
                            tr.className = 'none';
                        }
                        if (level == 1) {
                            tr.className = 'none';
                        }
                        if (level == 2) {
                            tr.className = 'hiddenRow';
                        }
                        if (level == 3) {
                            tr.className = 'hiddenRow';
                        }
                    }
                    if (id.substr(0,2) == 'st') {        
                        if (level == 0) {
                            tr.className = 'none';
                        }
                        if (level == 1) {
                            tr.className = 'hiddenRow';
                        }
                        if (level == 2) {
                            tr.className = 'hiddenRow';
                        }
                        if (level == 3) {
                            tr.className = 'none';
                        }
                    }
                }
            }

            function showTestDetail(tr_id){
                table = document.getElementById('result_table')
                trs = table.getElementsByTagName("tr");
                for (var i = 0; i < trs.length; i++) {
                    tr = trs[i];
                    id = tr.id;
                    if ((id.split('_'))[1] == tr_id){
                        trn = document.getElementById(id)
                        if (trn.className == 'none' ) {
                            trn.className = 'hiddenRow';
                        }
                        else {
                            trn.className = 'none';
                        }
                    }

                }
            }


            function showFailDetail(div_id){
                var details_div = document.getElementById(div_id)
                var displayState = details_div.style.display
                if (displayState != 'block' ) {
                    displayState = 'block'
                    details_div.style.display = 'block'
                }
                else {
                    details_div.style.display = 'none'
                }
            }

            </script>    
            </head><body style='font-family:微软雅黑'>
            '''

    f.write(htmlStr)
    f.close()
    conf = configparser.ConfigParser()
    conf.read("config.conf")
    conf.set("report", "reportpath", reportFolder)
    conf.set("report", "screen_path", screen_path)
    conf.set("report", "log_path", logFile)
    conf.set("report", "report_path", reportname)
    conf.write(open("config.conf", "w"))

    conf.read(test_path + "\\TestCases\\config.conf")
    conf.set("report", "reportpath", reportFolder)
    conf.set("report", "screen_path", screen_path)
    conf.set("report", "log_path", logFile)
    conf.set("report", "report_path", reportname)
    conf.write(open("config.conf", "w"))
    filenames = [logFile, reportname]
    return filenames

# 创建html格式的测试报告
def createReport(t_result, t_info, filename, reporttype):
    # localMachine = socket.getfqdn(socket.gethostname())
    # localIP = socket.gethostbyname(localMachine)
    f = open(filename[1], 'a')

    unskip = (t_info)["CaseNum"] - (t_info)["Skip"]
    passrate = (float((t_info)["Success"]) / (float(unskip))) * 100
    htmlstr = '''
            <h3>执行概述</h3>
            <p style='font-size:12px;'>点击各数字可以筛选对应结果的用例。</p>
            <table class='bordered' style='width:1100px; text-align:center'>
            <tr class='header_row'>
            <td style='width:100px'>用例总数</td>
            <td style='width:100px'>通过</td>
            <td style='width:100px'>失败</td>
            <td style='width:100px'>跳过</td>
            <td style='width:100px'>错误</td>
            <td style='width:100px'>通过率</td>
            <td>开始时间</td><td>运行时间</td><td>日志文件</td></tr>
            <tr><td><a href='javascript:showCase(0)'>%s</a></td>
            <td><a href='javascript:showCase(1)'>%s</a></td>
            <td><a href='javascript:showCase(2)'>%s</a></td>
            <td><a href='javascript:showCase(3)'>%s</a></td>
            <td><a href='javascript:showCase(2)'>%s</a></td>
            <td>%.2f%%</td><td>%s</td><td>%s</td>
            <td><a href='%s'>%s</a></td>
            </tr></table>
            ''' % (
    (t_info)["CaseNum"], (t_info)["Success"], (t_info)["Fail"], (t_info)["Skip"], (t_info)["Error"], passrate,
    (t_info)["StartTime"], (t_info)["TakeTime"], filename[0], os.path.split(filename[0])[-1])
    f.write(htmlstr)

    htmlstr = '''
            <h3>执行详情</h3>
            <p style='font-size:12px;'>Pass：通过，Failed：失败，Skip：跳过，Error：错误。点击Failed可以查看错误详情。</p>
            <table id='result_table' class="bordered">
            <tr class='header_row'>
                <td>编号</td>
                <td style='width:300px'>测试用例</td>
                <td style='width:300px'>中文描述</td>
                <td>耗时</td>
                <td style='width:300px'>测试结果</td>
                <td>查看</td>
            </tr>
            '''
    f.write(htmlstr)

    i = 1
    j = 1
    for key in t_result.results.keys():
        htmlstr = '''
                <tr><td colspan='6' class='testcase'>
                <a class="popup_link" onfocus="this.blur();" href="javascript:showTestDetail('%s')">%s</a></td></tr>
                ''' % (str(j), key)
        f.write(htmlstr)

        value = t_result.results[key]
        count = 1
        for key1 in value.keys():
            takentime = ((value[key1])["stoptime"] - (value[key1])["starttime"]).seconds
            takentime = str(datetime.timedelta(seconds=takentime))
            if (value[key1])["Result"] == "Failed" or (value[key1])["Result"] == "Error":
                htmlstr = "<tr id='ft_%s_%s' class='none' style='color:red'>" % (str(j), str(count))
                f.write(htmlstr)

                htmlstr = '''
                        <td><li></li></td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>
                        <a class="popup_link" style='color:red;text-decoration:underline;' onfocus='this.blur();' href="javascript:showFailDetail('div_ft%s')" >%s</a>
                        <div id='div_ft%s' class="popup_window">
                        <div style='text-align: right; color:red;cursor:pointer'>
                        <a onfocus='this.blur();' onclick="document.getElementById('div_ft%s').style.display = 'none' " >X</a></div>
                        <pre>%s</pre></td>
                        <td><a href='%s' target='_blank'>查看截图</a></td></tr>
                        ''' % (key1, (value[key1])["name"], takentime, str(i), (value[key1])["Result"], str(i), str(i),
                               (value[key1])["Reason"], (value[key1])["Screenshoot"])
                f.write(htmlstr)
                i += 1

            elif (value[key1])["Result"] == "Pass":
                htmlstr = '''
                        <tr id='pt_%s_%s' class='none'>
                        <td><li></li></td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td style='color:green;'>%s</td>
                        <td></td></tr>
                        ''' % ((str(j), str(count), key1, (value[key1])["name"], takentime, (value[key1])["Result"]))
                f.write(htmlstr)

            else:
                htmlstr = '''
                        <tr id='st_%s_%s' class='none'>
                        <td><li></li></td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td></td></tr>
                        ''' % ((str(j), str(count), key1, (value[key1])["name"], takentime, (value[key1])["Result"]))
                f.write(htmlstr)
            count += 1

        j += 1
    f.write("</table></body></html>")
    f.close()

# 创建html格式的接口测试报告
def createInterfaceReport(resultlist, t_info, reportfile, logfile):
    # localMachine = socket.getfqdn(socket.gethostname())
    # localIP = socket.gethostbyname(localMachine)
    f = open(reportfile, 'a')

    passrate = (float((t_info)["pass"]) / float((t_info)["total"])) * 100
    htmlstr = '''
            <h3>执行概述</h3>
            <table class='bordered' style='width:1000px; text-align:center'>
            <tr class='header_row'>
                <td style='width:100px'>用例总数</td>
                <td style='width:100px'>通过</td>
                <td style='width:100px'>失败</td>
                <td style='width:100px'>通过率</td>
                <td>开始时间</td><td>运行时间</td><td>日志文件</td></tr>
                <tr><td><a href='javascript:showCase(0)'>%s</a></td>
                <td><a href='javascript:showCase(1)'>%s</a></td>
                <td><a href='javascript:showCase(2)'>%s</a></td>
                <td>%.2f%%</td>
                <td>%s</td>
                <td>%.3fs</td>
                <td><a href='%s'>%s</a></td>
            </tr></table>
            ''' % (
    (t_info)["total"], (t_info)["pass"], (t_info)["fail"], passrate, t_info['starttime'], t_info['takentime'], logfile,
    os.path.split(logfile)[-1])
    f.write(htmlstr)

    htmlstr = '''
            <h3>执行详情</h3>
            <table id='result_table' class="bordered">
            <tr class='header_row'>
                <td>编号</td>
                <td>模块</td>
                <td>用例描述</td>
                <td>接口</td>
                <td>参数</td>
                <td>请求结果</td>
                <td>测试结果</td>
                <td>耗时(毫秒)</td>
            </tr>
            '''
    f.write(htmlstr)

    i = 1
    for result in resultlist:
        if result[5] == "Failed":
            htmlstr = "<tr id='ft_%s' class='none' style='color:red'>" % str(i)
        else:
            htmlstr = "<tr id='pt_%s' class='none' style='color:green'>" % str(i)
        htmlstr += '''
                <td><li></li></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td style='word-wrap:break-word; max-width:500px;'>%s</td>
                <td>%s</td>
                <td>%s ms</td></tr>
                ''' % (result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        f.write(htmlstr.encode('utf-8'))
        i += 1

    f.write("</table></body></html>")
    f.close()

# 发送邮件
def sendMail(reportname, reporttype):
    conf = configparser.ConfigParser()
    conf.read("config.conf")
    mail_from = conf.get("mail", "mail_from")  # 发件箱
    mail_tolist = conf.get("mail", "mail_tolist")  # 收件人列表
    mail_host = conf.get("mail", "mail_host")  # 服务器
    mail_user = conf.get("mail", "mail_user")  # 用户名
    mail_pass = conf.get("mail", "mail_pass")  # 密码
    mail_pass = base64.b64decode(mail_pass)

    f = open(reportname, 'r')
    content = f.read()
    msg = MIMEMultipart()
    puretext = MIMEText(content, _subtype='html', _charset='utf-8')  # 设置html格式邮件
    htmlpart = MIMEApplication(open(reportname, 'rb').read())
    htmlpart.add_header('Content-Disposition', 'attachment', filename=os.path.basename(reportname))
    msg.attach(puretext)
    msg.attach(htmlpart)
    sub = reporttype + "自动化测试报告-" + time.strftime("%Y/%m/%d", time.localtime(time.time()))
    msg['Subject'] = sub  # 设置主题
    msg['From'] = mail_from
    msg['To'] = mail_tolist
    sendmailinfo = ""
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # 连接smtp服务器
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(mail_from, mail_tolist, msg.as_string())  # 发送邮件
        s.close()
        sendmailinfo = "邮件发送成功！"
    except Exception as e:
        sendmailinfo = "邮件发送失败，错误信息：" + str(e)
    return sendmailinfo