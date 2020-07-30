<<<<<<< HEAD
<<<<<<< HEAD
import xlsxwriter
import showMethods


def initExcel(path):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    return workbook, worksheet


def addHeader(header_list, worksheet):
    num_dict = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L",
                13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W",
                24: "X", 25: "Y", 26: "Z"
                }
    worksheet.set_column(0, len(header_list) - 1, 30)
    for i in range(len(header_list)):
        worksheet.write(num_dict[i + 1] + "1", header_list[i])


def getHeaderList(date, tracking, order_number, shipped_name_and_address, product_name_and_qty, allOptions):
    headerList = []
    if allOptions:
        headerList = ['date', 'tracking', 'order number', 'shipped name and address', 'product name and qty']
        return headerList
    if date:
        headerList.append("date")
    if tracking:
        headerList.append("tracking")
    if order_number:
        headerList.append("order number")
    if shipped_name_and_address:
        headerList.append("shipped name and address")
    if product_name_and_qty:
        headerList.append("product name")
        headerList.append("qty")

    return headerList


def writeInfo(excel_list, total, worksheet):
    row = 1
    col = 0
    count = 1
    total_lens = len(excel_list)
    for items in excel_list:
        showMethods.progressBar(count, total_lens, "Writing Excel")
        for item in items:
            worksheet.write(row, col, item)
            col += 1
            if col > (total - 1):
                col = 0
        row += 1
        count += 1
=======
import xlsxwriter
import showMethods


def initExcel(path):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    return workbook, worksheet


def addHeader(header_list, worksheet):
    num_dict = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L",
                13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W",
                24: "X", 25: "Y", 26: "Z"
                }
    worksheet.set_column(0, len(header_list) - 1, 30)
    for i in range(len(header_list)):
        worksheet.write(num_dict[i + 1] + "1", header_list[i])


def getHeaderList(date, tracking, order_number, shipped_name_and_address, product_name_and_qty, allOptions):
    headerList = []
    if allOptions:
        headerList = ['date', 'tracking', 'order number', 'shipped name and address', 'product name and qty']
        return headerList
    if date:
        headerList.append("date")
    if tracking:
        headerList.append("tracking")
    if order_number:
        headerList.append("order number")
    if shipped_name_and_address:
        headerList.append("shipped name and address")
    if product_name_and_qty:
        headerList.append("product name")
        headerList.append("qty")

    return headerList


def writeInfo(excel_list, total, worksheet):
    row = 1
    col = 0
    count = 1
    total_lens = len(excel_list)
    for items in excel_list:
        showMethods.progressBar(count, total_lens, "Writing Excel")
        for item in items:
            worksheet.write(row, col, item)
            col += 1
            if col > (total - 1):
                col = 0
        row += 1
        count += 1
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db
=======
import xlsxwriter
import showMethods


def initExcel(path):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    return workbook, worksheet


def addHeader(header_list, worksheet):
    num_dict = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L",
                13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W",
                24: "X", 25: "Y", 26: "Z"
                }
    worksheet.set_column(0, len(header_list) - 1, 30)
    for i in range(len(header_list)):
        worksheet.write(num_dict[i + 1] + "1", header_list[i])


def getHeaderList(date, tracking, order_number, shipped_name_and_address, product_name_and_qty, allOptions):
    headerList = []
    if allOptions:
        headerList = ['date', 'tracking', 'order number', 'shipped name and address', 'product name and qty']
        return headerList
    if date:
        headerList.append("date")
    if tracking:
        headerList.append("tracking")
    if order_number:
        headerList.append("order number")
    if shipped_name_and_address:
        headerList.append("shipped name and address")
    if product_name_and_qty:
        headerList.append("product name")
        headerList.append("qty")

    return headerList


def writeInfo(excel_list, total, worksheet):
    row = 1
    col = 0
    count = 1
    total_lens = len(excel_list)
    for items in excel_list:
        showMethods.progressBar(count, total_lens, "Writing Excel")
        for item in items:
            worksheet.write(row, col, item)
            col += 1
            if col > (total - 1):
                col = 0
        row += 1
        count += 1
>>>>>>> abd6cba59923e6eac426400fb5e8d010b55c29db
