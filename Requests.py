import requests
import json
import time
import xlwt
import xlrd
from xlutils.copy import copy


def getRRDinfo(startPage, endPage):
    data = []
    for page in range(startPage, endPage):
        url = 'https://www.renrendai.com/uplan/product/getUplanProductBuyers?startNum=%d&limit=10&financePlanId' \
              '=31254' \
              % page
        response = requests.post(url).text
        list = json.loads(response).get('data').get('list')
        # print(list)
        for item in list:
            '''print('用户ID：%s' % item.get('userId'))
            print('出借人：%s' % item.get('nickName'))
            print('出借本金：%s' % item.get('amount'))
            print('出借时间：%s' % item.get('createTime'))'''

            timeNum = item.get('createTime')
            timeTemp = float(timeNum / 1000)
            tupTime = time.localtime(timeTemp)
            standardTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)
            data.append([item.get('userId'), item.get('nickName'), item.get('amount'), standardTime])
    return data


def saveRRDinfo(data):
    wb = xlrd.open_workbook('人人贷出借记录.xls')
    newb = copy(wb)
    # workbook= xlwt.Workbook(encoding='utf-8')
    worksheet = newb.add_sheet('U续12-1018')
    for row in range(len(data)):
        for column in range(len(data[0])):
            worksheet.write(row, column, data[row][column])
        newb.save('人人贷出借记录.xls')


if __name__ == '__main__':
    saveRRDinfo(getRRDinfo(0, 1))





'''from bs4 import BeautifulSoup
import requests
import time
import sys
from datetime import datetime, timedelta

# import pandas as pd

# code = input("Enter the NYSE stock symbol: ")

# Your Choice Stock
source = requests.get('https://www.renrendai.com/uplan/product/getUplanProductBuyers?startNum=0&limit=10'
                      '&financePlanId=31091').text
soup = BeautifulSoup(source, 'lxml')
data = soup.find_all("list")



timeNum = 1571104879000
timeTemp = float(timeNum / 1000)
tupTime = time.localtime(timeTemp)
standardTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)
print(standardTime)
print(soup)
print(data)'''
