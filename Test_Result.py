# -*- coding: utf-8 -*-
import xlwings as xw
import time
from scrapy.http import HtmlResponse
import requests

status_list = []


def xl_read():
    global app, wb, ws, ws2, test_link, alt_number

    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = True

    wb = app.books.open('./Test-Result.xlsx')
    ws = wb.sheets['DVT1']


def fetch(target):
    global status, result, fnotes
    html = requests.get(target).content
    resp = HtmlResponse(url=target, body=html)
    status = resp.xpath("//*[@id='MainContentPage_lblStatus_Name']//text()").extract()
    result = resp.xpath("//*[@id='MainContentPage_lblEngAssessment']//text()").extract()
    fnotes = resp.xpath("//*[@id='MainContentPage_lblALTEngrTestNotes']//text()").extract()


if __name__ == "__main__":
    print("如果使用过程中遇到问题，请联系何建华 hejh4@lenovo.com...")
    print('正在帮您查询测试结果，请耐心等待...')
    xl_read()
    '''for i in range(1,55):
        a = ws[i, 3].value
        b = ws[i, 4].value
    print(a is None or a =='\xa0' and b is not None)

    '''
    for i in range(1, 48):
        if ws[i, 5].value is None or ws[i, 4].value == '\xa0':
            alt_number = ws[i, 2].value
            test_link = ws[i, 2].hyperlink
            fetch(test_link)
            ws[i, 3].value = status
            ws[i, 4].value = result
            ws[i, 5].value = fnotes
            print('测试编号 ', alt_number, '的状态为', status, ', 测试结果为', result)
    '''for i in range(50, 60):
        if ws[i, 5].value is None or ws[i, 5].value == '\xa0':
            alt_number = ws[i, 3].value
            test_link = ws[i, 3].hyperlink
            fetch(test_link)
            ws[i, 4].value = status
            ws[i, 5].value = result
            ws[i, 6].value = fnotes
            print('测试编号 ', alt_number, '的状态为', status, ', 测试结果为', result)'''

    wb.save()
    wb.close()
    time.sleep(2)
    app.quit()
