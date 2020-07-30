<<<<<<< HEAD
<<<<<<< HEAD
import copy
import re

from bs4 import BeautifulSoup

import echoError
import re


# 获取发件人类型 目前可匹配target amazon bestbuy
def GetSenderType(context):
    if MatchStr(r'<orders@oe.target.com>', context) is not None:
        return "Target"
    elif MatchStr(r'<shipment-tracking@amazon.com>', context) is not None:
        return "Amazon"
    elif MatchStr(r'<BestBuyInfo@emailinfo.bestbuy.com>', context) is not None:
        return "BestBuy"
    else:
        return None


# 获取邮件的tracking number
def GetTrackingNumber(emailType, info_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        address_table = soup.find("table", {"width": "100%", "cellspacing": "0", "cellpadding": "0", "align": "center"})
        address_info = address_table.get_text().strip().split("   ")
        tracking = address_info[1]
        info_list.append(tracking)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("td",{"width":"320","align":"center","valign":"top"})
        tracking = tag.get_text().strip().split("                                                                   ")[0]


# 获取邮件的order number
def GetOrderNumber(emailType, info_list, content):
    if emailType == "Target":
        order_number = MatchStr(r'#\d*', content)
        info_list.append(order_number)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("td", {"width": "320", "align": "center", "valign": "top"})
        order_number = tag.get_text().strip().split("                                                                   ")[1]
        info_list.append(order_number)


# 获取邮件的shipped name and address
def GetShippedNameAndAddress(emailType, info_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        address_table = soup.find("table", {"width": "100%", "cellspacing": "0", "cellpadding": "0", "align": "center"})
        address_info = address_table.get_text().strip().split("   ")
        address = address_info[0]
        info_list.append(address)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("table", {"bgcolor": "f1f2f2"}).find("span")
        if tag is not None:
            tag = str(tag).split("<br/>")
            tagTmp = tag[0].split(">")
            tag[0] = tagTmp[1]
            tagTmp = tag[-1].split("<")
            tag[-1] = tagTmp[0]
            tag = " ".join(tag)
        shipping_address_and_name = tag
        info_list.append(shipping_address_and_name)


# 获取邮件的product name and qty
def GetProductNameAndQty(emailType, info_list, excel_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        info_table = soup.find_all("table", {"width": "59%", "cellspacing": "0", "cellpadding": "0", "align": "left"})
        for element in info_table:
            productName_qty = element.get_text().strip().split("                    ")
            copy_list = copy.deepcopy(info_list)
            copy_list.extend(productName_qty)
            excel_list.append(copy_list)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.findAll("td", {"width": "303", "valign": "top"})
        for element in tag:
            tmp = []
            for i in element.findAll("table",{"align":"left"}):
                i = i.get_text()
                tmp.append(i)
            copy_list = copy.deepcopy(info_list)
            copy_list.extend(tmp)
            excel_list.append(copy_list)

# 匹配邮箱的正则
def MatchEmail(email):
    x = re.search(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', email)
    if x is not None:
        return x.group()
    else:
        return x


# 获取邮件的时间 返回的格式为[年，月，日，时，分，秒]
def MatchTime(content):
    return MatchStr(r'[A-Z][a-z]{2,},\s\d{2,}\s[A-Z][a-z]{2,}\s\d{4,}\s\d{2,}:\d{2,}:\d{2,}', content)


# 如果正则表达式，找到符合规则的内容则返回内容 否则返回None
def MatchStr(re_str, content):
    result = re.search(re_str, content)
    if result is not None:
        return result.group(0)
    return result


# 格式化日期 Thu, 28 May 2020 10:57:55
def FormatTime(content):
    month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
                  'Nov': 11, 'Dec': 12}
    day = int(checkFirst0(content[5:7]))
    month = month_dict[content[8:11]]
    year = int(content[12:17])
    hour = int(checkFirst0(content[17:19]))
    mins = int(checkFirst0(content[20:22]))
    sec = int(checkFirst0(content[23:25]))
    return [year, month, day, hour, mins, sec]


# 匹配年月日时分秒 并返回一个列表格式为[年，月，日，时，分，秒]
# 年月日必须不为0 年月日必须大于 1970-1-1 00:00:00 小于3000-1-1 00:00:00
# 时分秒可以为0
# 默认检查格式为打开 默认格式关闭时传入格式必须为 年/月/日/时/分/秒
def getTime(value, check=True):
    timeList = value.split("/")
    if check:
        if len(timeList) == 3:
            year = int(checkFirst0(timeList[0]))
            month = int(checkFirst0(timeList[1]))
            day = int(checkFirst0(timeList[2]))
            if 3000 < year or year < 1970:
                return None
            if 12 < month or month < 1:
                return None
            if 31 < day or day < 1:
                return None
            return [year, month, day, 0, 0, 0]
        elif len(timeList) == 6:
            year = int(checkFirst0(timeList[0]))
            month = int(checkFirst0(timeList[1]))
            day = int(checkFirst0(timeList[2]))
            if 3000 < year or year < 1970:
                return None
            if 12 < month or month < 1:
                return None
            if 31 < day or day < 1:
                return None
            hour = int(checkFirst0(timeList[3]))
            mins = int(checkFirst0(timeList[4]))
            sec = int(checkFirst0(timeList[5]))
            if 23 < hour or hour < 0:
                return None
            if 59 < mins or hour < 0:
                return None
            if 59 < sec or sec < 0:
                return None
            return [year, month, day, hour, mins, sec]
        else:
            return None
    else:
        return [int(timeList[0]), int(timeList[1]), int(timeList[2]), int(timeList[3]), int(timeList[4]),
                int(timeList[5])]


# 检查字符首位是否是0 如果是做去0处理
def checkFirst0(value):
    if len(value) > 1 and value[0] == "0":
        value = re.sub(r'^0', '', value)
    return value


# 根据输入元组和值判读 是否在组中
def getTF(value, tup):
    if value in tup:
        return True
    return False
=======
import copy
import re

from bs4 import BeautifulSoup

import echoError
import re


# 获取发件人类型 目前可匹配target amazon bestbuy
def GetSenderType(context):
    if MatchStr(r'<orders@oe.target.com>', context) is not None:
        return "Target"
    elif MatchStr(r'<shipment-tracking@amazon.com>', context) is not None:
        return "Amazon"
    elif MatchStr(r'<BestBuyInfo@emailinfo.bestbuy.com>', context) is not None:
        return "BestBuy"
    else:
        return None


# 获取邮件的tracking number
def GetTrackingNumber(emailType, info_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        address_table = soup.find("table", {"width": "100%", "cellspacing": "0", "cellpadding": "0", "align": "center"})
        address_info = address_table.get_text().strip().split("   ")
        tracking = address_info[1]
        info_list.append(tracking)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("td",{"width":"320","align":"center","valign":"top"})
        tracking = tag.get_text().strip().split("                                                                   ")[0]


# 获取邮件的order number
def GetOrderNumber(emailType, info_list, content):
    if emailType == "Target":
        order_number = MatchStr(r'#\d*', content)
        info_list.append(order_number)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("td", {"width": "320", "align": "center", "valign": "top"})
        order_number = tag.get_text().strip().split("                                                                   ")[1]
        info_list.append(order_number)


# 获取邮件的shipped name and address
def GetShippedNameAndAddress(emailType, info_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        address_table = soup.find("table", {"width": "100%", "cellspacing": "0", "cellpadding": "0", "align": "center"})
        address_info = address_table.get_text().strip().split("   ")
        address = address_info[0]
        info_list.append(address)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("table", {"bgcolor": "f1f2f2"}).find("span")
        if tag is not None:
            tag = str(tag).split("<br/>")
            tagTmp = tag[0].split(">")
            tag[0] = tagTmp[1]
            tagTmp = tag[-1].split("<")
            tag[-1] = tagTmp[0]
            tag = " ".join(tag)
        shipping_address_and_name = tag
        info_list.append(shipping_address_and_name)


# 获取邮件的product name and qty
def GetProductNameAndQty(emailType, info_list, excel_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        info_table = soup.find_all("table", {"width": "59%", "cellspacing": "0", "cellpadding": "0", "align": "left"})
        for element in info_table:
            productName_qty = element.get_text().strip().split("                    ")
            copy_list = copy.deepcopy(info_list)
            copy_list.extend(productName_qty)
            excel_list.append(copy_list)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.findAll("td", {"width": "303", "valign": "top"})
        for element in tag:
            tmp = []
            for i in element.findAll("table",{"align":"left"}):
                i = i.get_text()
                tmp.append(i)
            copy_list = copy.deepcopy(info_list)
            copy_list.extend(tmp)
            excel_list.append(copy_list)

# 匹配邮箱的正则
def MatchEmail(email):
    x = re.search(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', email)
    if x is not None:
        return x.group()
    else:
        return x


# 获取邮件的时间 返回的格式为[年，月，日，时，分，秒]
def MatchTime(content):
    return MatchStr(r'[A-Z][a-z]{2,},\s\d{2,}\s[A-Z][a-z]{2,}\s\d{4,}\s\d{2,}:\d{2,}:\d{2,}', content)


# 如果正则表达式，找到符合规则的内容则返回内容 否则返回None
def MatchStr(re_str, content):
    result = re.search(re_str, content)
    if result is not None:
        return result.group(0)
    return result


# 格式化日期 Thu, 28 May 2020 10:57:55
def FormatTime(content):
    month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
                  'Nov': 11, 'Dec': 12}
    day = int(checkFirst0(content[5:7]))
    month = month_dict[content[8:11]]
    year = int(content[12:17])
    hour = int(checkFirst0(content[17:19]))
    mins = int(checkFirst0(content[20:22]))
    sec = int(checkFirst0(content[23:25]))
    return [year, month, day, hour, mins, sec]


# 匹配年月日时分秒 并返回一个列表格式为[年，月，日，时，分，秒]
# 年月日必须不为0 年月日必须大于 1970-1-1 00:00:00 小于3000-1-1 00:00:00
# 时分秒可以为0
# 默认检查格式为打开 默认格式关闭时传入格式必须为 年/月/日/时/分/秒
def getTime(value, check=True):
    timeList = value.split("/")
    if check:
        if len(timeList) == 3:
            year = int(checkFirst0(timeList[0]))
            month = int(checkFirst0(timeList[1]))
            day = int(checkFirst0(timeList[2]))
            if 3000 < year or year < 1970:
                return None
            if 12 < month or month < 1:
                return None
            if 31 < day or day < 1:
                return None
            return [year, month, day, 0, 0, 0]
        elif len(timeList) == 6:
            year = int(checkFirst0(timeList[0]))
            month = int(checkFirst0(timeList[1]))
            day = int(checkFirst0(timeList[2]))
            if 3000 < year or year < 1970:
                return None
            if 12 < month or month < 1:
                return None
            if 31 < day or day < 1:
                return None
            hour = int(checkFirst0(timeList[3]))
            mins = int(checkFirst0(timeList[4]))
            sec = int(checkFirst0(timeList[5]))
            if 23 < hour or hour < 0:
                return None
            if 59 < mins or hour < 0:
                return None
            if 59 < sec or sec < 0:
                return None
            return [year, month, day, hour, mins, sec]
        else:
            return None
    else:
        return [int(timeList[0]), int(timeList[1]), int(timeList[2]), int(timeList[3]), int(timeList[4]),
                int(timeList[5])]


# 检查字符首位是否是0 如果是做去0处理
def checkFirst0(value):
    if len(value) > 1 and value[0] == "0":
        value = re.sub(r'^0', '', value)
    return value


# 根据输入元组和值判读 是否在组中
def getTF(value, tup):
    if value in tup:
        return True
    return False
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db
=======
import copy
import re

from bs4 import BeautifulSoup

import echoError
import re


# 获取发件人类型 目前可匹配target amazon bestbuy
def GetSenderType(context):
    if MatchStr(r'<orders@oe.target.com>', context) is not None:
        return "Target"
    elif MatchStr(r'<shipment-tracking@amazon.com>', context) is not None:
        return "Amazon"
    elif MatchStr(r'<BestBuyInfo@emailinfo.bestbuy.com>', context) is not None:
        return "BestBuy"
    else:
        return None


# 获取邮件的tracking number
def GetTrackingNumber(emailType, info_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        address_table = soup.find("table", {"width": "100%", "cellspacing": "0", "cellpadding": "0", "align": "center"})
        address_info = address_table.get_text().strip().split("   ")
        tracking = address_info[1]
        info_list.append(tracking)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("td",{"width":"320","align":"center","valign":"top"})
        tracking = tag.get_text().strip().split("                                                                   ")[0]


# 获取邮件的order number
def GetOrderNumber(emailType, info_list, content):
    if emailType == "Target":
        order_number = MatchStr(r'#\d*', content)
        info_list.append(order_number)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("td", {"width": "320", "align": "center", "valign": "top"})
        order_number = tag.get_text().strip().split("                                                                   ")[1]
        info_list.append(order_number)


# 获取邮件的shipped name and address
def GetShippedNameAndAddress(emailType, info_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        address_table = soup.find("table", {"width": "100%", "cellspacing": "0", "cellpadding": "0", "align": "center"})
        address_info = address_table.get_text().strip().split("   ")
        address = address_info[0]
        info_list.append(address)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.find("table", {"bgcolor": "f1f2f2"}).find("span")
        if tag is not None:
            tag = str(tag).split("<br/>")
            tagTmp = tag[0].split(">")
            tag[0] = tagTmp[1]
            tagTmp = tag[-1].split("<")
            tag[-1] = tagTmp[0]
            tag = " ".join(tag)
        shipping_address_and_name = tag
        info_list.append(shipping_address_and_name)


# 获取邮件的product name and qty
def GetProductNameAndQty(emailType, info_list, excel_list, content):
    if emailType == "Target":
        soup = BeautifulSoup(content, features='html.parser')
        info_table = soup.find_all("table", {"width": "59%", "cellspacing": "0", "cellpadding": "0", "align": "left"})
        for element in info_table:
            productName_qty = element.get_text().strip().split("                    ")
            copy_list = copy.deepcopy(info_list)
            copy_list.extend(productName_qty)
            excel_list.append(copy_list)
    elif emailType == "Amazon":
        echoError.errorStatement("Error: Amazon is not provide yet")
    elif emailType == "BestBuy":
        soup = BeautifulSoup(content, features='html.parser')
        tag = soup.findAll("td", {"width": "303", "valign": "top"})
        for element in tag:
            tmp = []
            for i in element.findAll("table",{"align":"left"}):
                i = i.get_text()
                tmp.append(i)
            copy_list = copy.deepcopy(info_list)
            copy_list.extend(tmp)
            excel_list.append(copy_list)

# 匹配邮箱的正则
def MatchEmail(email):
    x = re.search(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', email)
    if x is not None:
        return x.group()
    else:
        return x


# 获取邮件的时间 返回的格式为[年，月，日，时，分，秒]
def MatchTime(content):
    return MatchStr(r'[A-Z][a-z]{2,},\s\d{2,}\s[A-Z][a-z]{2,}\s\d{4,}\s\d{2,}:\d{2,}:\d{2,}', content)


# 如果正则表达式，找到符合规则的内容则返回内容 否则返回None
def MatchStr(re_str, content):
    result = re.search(re_str, content)
    if result is not None:
        return result.group(0)
    return result


# 格式化日期 Thu, 28 May 2020 10:57:55
def FormatTime(content):
    month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
                  'Nov': 11, 'Dec': 12}
    day = int(checkFirst0(content[5:7]))
    month = month_dict[content[8:11]]
    year = int(content[12:17])
    hour = int(checkFirst0(content[17:19]))
    mins = int(checkFirst0(content[20:22]))
    sec = int(checkFirst0(content[23:25]))
    return [year, month, day, hour, mins, sec]


# 匹配年月日时分秒 并返回一个列表格式为[年，月，日，时，分，秒]
# 年月日必须不为0 年月日必须大于 1970-1-1 00:00:00 小于3000-1-1 00:00:00
# 时分秒可以为0
# 默认检查格式为打开 默认格式关闭时传入格式必须为 年/月/日/时/分/秒
def getTime(value, check=True):
    timeList = value.split("/")
    if check:
        if len(timeList) == 3:
            year = int(checkFirst0(timeList[0]))
            month = int(checkFirst0(timeList[1]))
            day = int(checkFirst0(timeList[2]))
            if 3000 < year or year < 1970:
                return None
            if 12 < month or month < 1:
                return None
            if 31 < day or day < 1:
                return None
            return [year, month, day, 0, 0, 0]
        elif len(timeList) == 6:
            year = int(checkFirst0(timeList[0]))
            month = int(checkFirst0(timeList[1]))
            day = int(checkFirst0(timeList[2]))
            if 3000 < year or year < 1970:
                return None
            if 12 < month or month < 1:
                return None
            if 31 < day or day < 1:
                return None
            hour = int(checkFirst0(timeList[3]))
            mins = int(checkFirst0(timeList[4]))
            sec = int(checkFirst0(timeList[5]))
            if 23 < hour or hour < 0:
                return None
            if 59 < mins or hour < 0:
                return None
            if 59 < sec or sec < 0:
                return None
            return [year, month, day, hour, mins, sec]
        else:
            return None
    else:
        return [int(timeList[0]), int(timeList[1]), int(timeList[2]), int(timeList[3]), int(timeList[4]),
                int(timeList[5])]


# 检查字符首位是否是0 如果是做去0处理
def checkFirst0(value):
    if len(value) > 1 and value[0] == "0":
        value = re.sub(r'^0', '', value)
    return value


# 根据输入元组和值判读 是否在组中
def getTF(value, tup):
    if value in tup:
        return True
    return False
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db
