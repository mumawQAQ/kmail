<<<<<<< HEAD
<<<<<<< HEAD
import imaplib
import os
import pickle
import re

import click
from bs4 import BeautifulSoup

import echoError
import datetime
import time
import reMethods
import showMethods
import excelMethods


# 根据输入的字典和值获取指定值
def __getValue(value, dic1):
    if dic1[value] is not None:
        value = dic1[value]
    return None


# 根据输入元组和值判读 是否在组中
def __getTF(value, tup):
    if value in tup:
        return True
    return False


# 获取秒数
def __getSecond(year, month, day, hour, mins, second):
    t = datetime.datetime(int(year), int(month), int(day), int(hour), int(mins), int(second))
    return time.mktime(t.timetuple())


# 根据输入的邮箱，密码，组和邮箱类型（url）
# 创建一个imaplib对象 如果创建失败则返回None
def loginEmail(email, password, group, url):
    m = imaplib.IMAP4_SSL(url, 993)
    try:
        m.login(email, password)
    except:
        echoError.errorStatement('Error:Password incorrect')
    else:
        try:
            m.select(group)
        except:
            echoError.errorStatement('Error:Group is not exist')
        else:
            click.echo(click.style('Successfully login in', fg='green'))
            return m

    return None


# 根据输入的邮箱，密码，组和邮箱类型（url）
# 序列化数组信息并保存在/src/info文件下
# 如果 src/ 文件夹不存在 则创建文件夹
def storeInfo(email, password, group, url):
    try:
        click.echo(click.style('Storing infos', fg='green'))
        path = os.getcwd()
        os.chdir(path)
        if not os.path.exists(path + "/src"):
            os.mkdir("src")
        f = open(path + '/src/info', 'wb')
        pickle.dump([email, password, group, url], f)
    except:
        echoError.errorStatement('Error:Fail to store information')


# 根据输入的imaplib对象 获取邮件id list
def getIdList(m):
    resp, items = m.search(None, 'ALL')
    items = items[0].split()
    return items


# 根据输入的要获取的内容 返回包含所有内容的list
# items 为 idlist
# dict 字典参数为 "startTime" "endTime" "options"
# options 参数可能为 "date", "tracking", "order number", "shipped name and address", "product name and qty"
def getInfo(m, items, target, dict1, name):
    startTime = None
    if dict1["startTime"] is not None:
        startTime = dict1["startTime"]
    # 如果开始时间为None则初始化为0
    if startTime is None:
        startTime = 0
    else:
        startTime = __getSecond(startTime[0], startTime[1], startTime[2], startTime[3], startTime[4], startTime[5])

    endTime = None
    if dict1["endTime"] is not None:
        endTime = dict1["endTime"]
    # 如果结束时间为None则初始化为正无穷
    if endTime is None:
        endTime = float('inf')
    else:
        endTime = __getSecond(endTime[0], endTime[1], endTime[2], endTime[3], endTime[4], endTime[5])

    options = []
    if dict1["options"] is not None:
        options = dict1["options"]
    # 测试代码
    # print("option:{}".format(options))

    # 下面的值为t/f
    allOptions = __getTF("All", options)
    # 测试代码
    # print("allOptions:{}".format(allOptions))
    if not allOptions:
        date = __getTF("date", options)
        tracking = __getTF("tracking", options)
        order_number = __getTF("order_number", options)
        shipped_name_and_address = __getTF("shipped_name_and_address", options)
        product_name_and_qty = __getTF("product_name_and_qty", options)
    else:
        date = True
        tracking = True
        order_number = True
        shipped_name_and_address = True
        product_name_and_qty = True
    try:
        workbook, worksheet = excelMethods.initExcel(name)
    except:
        echoError.errorStatement("Error: Fail to init excel")
        return
    else:
        headerList = excelMethods.getHeaderList(date, tracking, order_number, shipped_name_and_address,
                                                product_name_and_qty, allOptions)
        excelMethods.addHeader(headerList, worksheet)
    count = 1
    # 总长度
    total_lens = len(items)
    excel_list = []
    # 根据需求获取信息
    for emailId in items:
        showMethods.progressBar(count, total_lens, "Reading Emails")
        resp, data = m.fetch(emailId, "(RFC822)")
        email_body = data[0][1]
        email_body = str(email_body)

        # 格式化邮件 去除无用格式
        email_body = re.sub(r'(\\r|\\n|\\t)', '', email_body)
        # 根据发件人获取邮件类型
        emailType = reMethods.GetSenderType(email_body)

        edate = reMethods.MatchTime(email_body)
        second = reMethods.FormatTime(edate)
        second = __getSecond(second[0], second[1], second[2], second[3], second[4], second[5])
        # 确定邮件是否在指定时间区域内
        if second > endTime or second < startTime:
            count += 1
            continue
        # 确定邮件是shipping邮件
        has_shipped = reMethods.MatchStr(r'#[BY\d-]+ (have|has) shipped', email_body)
        if has_shipped is None:
            count += 1
            continue
        count += 1
        # 初始化info_list
        info_list = []
        if date:
            info_list.append(edate)
        if tracking:
            reMethods.GetTrackingNumber(emailType, info_list, email_body)
        if order_number:
            reMethods.GetOrderNumber(emailType, info_list, has_shipped,email_body)
        if shipped_name_and_address:
            reMethods.GetShippedNameAndAddress(emailType, info_list, email_body)
        if product_name_and_qty:
            reMethods.GetProductNameAndQty(emailType, info_list, excel_list, email_body)
        else:
            excel_list.append(info_list)
    excelMethods.writeInfo(excel_list,len(headerList),worksheet)
    workbook.close()
=======
import imaplib
import os
import pickle
import re

import click
from bs4 import BeautifulSoup

import echoError
import datetime
import time
import reMethods
import showMethods
import excelMethods


# 根据输入的字典和值获取指定值
def __getValue(value, dic1):
    if dic1[value] is not None:
        value = dic1[value]
    return None


# 根据输入元组和值判读 是否在组中
def __getTF(value, tup):
    if value in tup:
        return True
    return False


# 获取秒数
def __getSecond(year, month, day, hour, mins, second):
    t = datetime.datetime(int(year), int(month), int(day), int(hour), int(mins), int(second))
    return time.mktime(t.timetuple())


# 根据输入的邮箱，密码，组和邮箱类型（url）
# 创建一个imaplib对象 如果创建失败则返回None
def loginEmail(email, password, group, url):
    m = imaplib.IMAP4_SSL(url, 993)
    try:
        m.login(email, password)
    except:
        echoError.errorStatement('Error:Password incorrect')
    else:
        try:
            m.select(group)
        except:
            echoError.errorStatement('Error:Group is not exist')
        else:
            click.echo(click.style('Successfully login in', fg='green'))
            return m

    return None


# 根据输入的邮箱，密码，组和邮箱类型（url）
# 序列化数组信息并保存在/src/info文件下
# 如果 src/ 文件夹不存在 则创建文件夹
def storeInfo(email, password, group, url):
    try:
        click.echo(click.style('Storing infos', fg='green'))
        path = os.getcwd()
        os.chdir(path)
        if not os.path.exists(path + "/src"):
            os.mkdir("src")
        f = open(path + '/src/info', 'wb')
        pickle.dump([email, password, group, url], f)
    except:
        echoError.errorStatement('Error:Fail to store information')


# 根据输入的imaplib对象 获取邮件id list
def getIdList(m):
    resp, items = m.search(None, 'ALL')
    items = items[0].split()
    return items


# 根据输入的要获取的内容 返回包含所有内容的list
# items 为 idlist
# dict 字典参数为 "startTime" "endTime" "options"
# options 参数可能为 "date", "tracking", "order number", "shipped name and address", "product name and qty"
def getInfo(m, items, target, dict1, name):
    startTime = None
    if dict1["startTime"] is not None:
        startTime = dict1["startTime"]
    # 如果开始时间为None则初始化为0
    if startTime is None:
        startTime = 0
    else:
        startTime = __getSecond(startTime[0], startTime[1], startTime[2], startTime[3], startTime[4], startTime[5])

    endTime = None
    if dict1["endTime"] is not None:
        endTime = dict1["endTime"]
    # 如果结束时间为None则初始化为正无穷
    if endTime is None:
        endTime = float('inf')
    else:
        endTime = __getSecond(endTime[0], endTime[1], endTime[2], endTime[3], endTime[4], endTime[5])

    options = []
    if dict1["options"] is not None:
        options = dict1["options"]
    # 测试代码
    # print("option:{}".format(options))

    # 下面的值为t/f
    allOptions = __getTF("All", options)
    # 测试代码
    # print("allOptions:{}".format(allOptions))
    if not allOptions:
        date = __getTF("date", options)
        tracking = __getTF("tracking", options)
        order_number = __getTF("order_number", options)
        shipped_name_and_address = __getTF("shipped_name_and_address", options)
        product_name_and_qty = __getTF("product_name_and_qty", options)
    else:
        date = True
        tracking = True
        order_number = True
        shipped_name_and_address = True
        product_name_and_qty = True
    try:
        workbook, worksheet = excelMethods.initExcel(name)
    except:
        echoError.errorStatement("Error: Fail to init excel")
        return
    else:
        headerList = excelMethods.getHeaderList(date, tracking, order_number, shipped_name_and_address,
                                                product_name_and_qty, allOptions)
        excelMethods.addHeader(headerList, worksheet)
    count = 1
    # 总长度
    total_lens = len(items)
    excel_list = []
    # 根据需求获取信息
    for emailId in items:
        showMethods.progressBar(count, total_lens, "Reading Emails")
        resp, data = m.fetch(emailId, "(RFC822)")
        email_body = data[0][1]
        email_body = str(email_body)

        # 格式化邮件 去除无用格式
        email_body = re.sub(r'(\\r|\\n|\\t)', '', email_body)
        # 根据发件人获取邮件类型
        emailType = reMethods.GetSenderType(email_body)

        edate = reMethods.MatchTime(email_body)
        second = reMethods.FormatTime(edate)
        second = __getSecond(second[0], second[1], second[2], second[3], second[4], second[5])
        # 确定邮件是否在指定时间区域内
        if second > endTime or second < startTime:
            count += 1
            continue
        # 确定邮件是shipping邮件
        has_shipped = reMethods.MatchStr(r'#[BY\d-]+ (have|has) shipped', email_body)
        if has_shipped is None:
            count += 1
            continue
        count += 1
        # 初始化info_list
        info_list = []
        if date:
            info_list.append(edate)
        if tracking:
            reMethods.GetTrackingNumber(emailType, info_list, email_body)
        if order_number:
            reMethods.GetOrderNumber(emailType, info_list, has_shipped,email_body)
        if shipped_name_and_address:
            reMethods.GetShippedNameAndAddress(emailType, info_list, email_body)
        if product_name_and_qty:
            reMethods.GetProductNameAndQty(emailType, info_list, excel_list, email_body)
        else:
            excel_list.append(info_list)
    excelMethods.writeInfo(excel_list,len(headerList),worksheet)
    workbook.close()
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db
=======
import imaplib
import os
import pickle
import re

import click
from bs4 import BeautifulSoup

import echoError
import datetime
import time
import reMethods
import showMethods
import excelMethods


# 根据输入的字典和值获取指定值
def __getValue(value, dic1):
    if dic1[value] is not None:
        value = dic1[value]
    return None


# 根据输入元组和值判读 是否在组中
def __getTF(value, tup):
    if value in tup:
        return True
    return False


# 获取秒数
def __getSecond(year, month, day, hour, mins, second):
    t = datetime.datetime(int(year), int(month), int(day), int(hour), int(mins), int(second))
    return time.mktime(t.timetuple())


# 根据输入的邮箱，密码，组和邮箱类型（url）
# 创建一个imaplib对象 如果创建失败则返回None
def loginEmail(email, password, group, url):
    m = imaplib.IMAP4_SSL(url, 993)
    try:
        m.login(email, password)
    except:
        echoError.errorStatement('Error:Password incorrect')
    else:
        try:
            m.select(group)
        except:
            echoError.errorStatement('Error:Group is not exist')
        else:
            click.echo(click.style('Successfully login in', fg='green'))
            return m

    return None


# 根据输入的邮箱，密码，组和邮箱类型（url）
# 序列化数组信息并保存在/src/info文件下
# 如果 src/ 文件夹不存在 则创建文件夹
def storeInfo(email, password, group, url):
    try:
        click.echo(click.style('Storing infos', fg='green'))
        path = os.getcwd()
        os.chdir(path)
        if not os.path.exists(path + "/src"):
            os.mkdir("src")
        f = open(path + '/src/info', 'wb')
        pickle.dump([email, password, group, url], f)
    except:
        echoError.errorStatement('Error:Fail to store information')


# 根据输入的imaplib对象 获取邮件id list
def getIdList(m):
    resp, items = m.search(None, 'ALL')
    items = items[0].split()
    return items


# 根据输入的要获取的内容 返回包含所有内容的list
# items 为 idlist
# dict 字典参数为 "startTime" "endTime" "options"
# options 参数可能为 "date", "tracking", "order number", "shipped name and address", "product name and qty"
def getInfo(m, items, target, dict1, name):
    startTime = None
    if dict1["startTime"] is not None:
        startTime = dict1["startTime"]
    # 如果开始时间为None则初始化为0
    if startTime is None:
        startTime = 0
    else:
        startTime = __getSecond(startTime[0], startTime[1], startTime[2], startTime[3], startTime[4], startTime[5])

    endTime = None
    if dict1["endTime"] is not None:
        endTime = dict1["endTime"]
    # 如果结束时间为None则初始化为正无穷
    if endTime is None:
        endTime = float('inf')
    else:
        endTime = __getSecond(endTime[0], endTime[1], endTime[2], endTime[3], endTime[4], endTime[5])

    options = []
    if dict1["options"] is not None:
        options = dict1["options"]
    # 测试代码
    # print("option:{}".format(options))

    # 下面的值为t/f
    allOptions = __getTF("All", options)
    # 测试代码
    # print("allOptions:{}".format(allOptions))
    if not allOptions:
        date = __getTF("date", options)
        tracking = __getTF("tracking", options)
        order_number = __getTF("order_number", options)
        shipped_name_and_address = __getTF("shipped_name_and_address", options)
        product_name_and_qty = __getTF("product_name_and_qty", options)
    else:
        date = True
        tracking = True
        order_number = True
        shipped_name_and_address = True
        product_name_and_qty = True
    try:
        workbook, worksheet = excelMethods.initExcel(name)
    except:
        echoError.errorStatement("Error: Fail to init excel")
        return
    else:
        headerList = excelMethods.getHeaderList(date, tracking, order_number, shipped_name_and_address,
                                                product_name_and_qty, allOptions)
        excelMethods.addHeader(headerList, worksheet)
    count = 1
    # 总长度
    total_lens = len(items)
    excel_list = []
    # 根据需求获取信息
    for emailId in items:
        showMethods.progressBar(count, total_lens, "Reading Emails")
        resp, data = m.fetch(emailId, "(RFC822)")
        email_body = data[0][1]
        email_body = str(email_body)

        # 格式化邮件 去除无用格式
        email_body = re.sub(r'(\\r|\\n|\\t)', '', email_body)
        # 根据发件人获取邮件类型
        emailType = reMethods.GetSenderType(email_body)

        edate = reMethods.MatchTime(email_body)
        second = reMethods.FormatTime(edate)
        second = __getSecond(second[0], second[1], second[2], second[3], second[4], second[5])
        # 确定邮件是否在指定时间区域内
        if second > endTime or second < startTime:
            count += 1
            continue
        # 确定邮件是shipping邮件
        has_shipped = reMethods.MatchStr(r'#[BY\d-]+ (have|has) shipped', email_body)
        if has_shipped is None:
            count += 1
            continue
        count += 1
        # 初始化info_list
        info_list = []
        if date:
            info_list.append(edate)
        if tracking:
            reMethods.GetTrackingNumber(emailType, info_list, email_body)
        if order_number:
            reMethods.GetOrderNumber(emailType, info_list, has_shipped,email_body)
        if shipped_name_and_address:
            reMethods.GetShippedNameAndAddress(emailType, info_list, email_body)
        if product_name_and_qty:
            reMethods.GetProductNameAndQty(emailType, info_list, excel_list, email_body)
        else:
            excel_list.append(info_list)
    excelMethods.writeInfo(excel_list,len(headerList),worksheet)
    workbook.close()
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db
