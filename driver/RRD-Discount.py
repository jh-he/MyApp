import requests
import json
import urllib.request
import time
import xlwt
import xlrd
from xlutils.copy import copy

url = 'https://m.renrendai.com/h5/event/quit/getDiscountQuitInfoList'

headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 10; motorola edge Build/QPD30.114-80; wv) AppleWebKit/537.36 ("
                  "KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.101 Mobile Safari/537.36 SCHEME/renrendaiinvestment/WEAPP/60101",
    'Connection': 'keep-alive',
    'Host': 'm.renrendai.com',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://m.renrendai.com/h5/event/quit/index?bounceDisabled=1&titleColor=FFFFFF&navBarBgColor'
                '=0F4E97'
}

params = {'size': 100

          }



def function foo():
    httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', "/echo/json");
    httpRequest.send();
    return httpRequest.responseText

var result = foo();




response = requests.get(url, headers=headers, params=params).text
quitDiscoutList = json.loads(response)

print(quitDiscoutList)
