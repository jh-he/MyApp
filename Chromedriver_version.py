from selenium import webdriver
import requests
import zipfile
import os

rs = requests.get('https://npm.taobao.org/mirrors/chromedriver/')
print(rs.text)


# 自动解压缩zip并删除
def unzip_driver():
    driver_zip = './driver/chromedriver_win32.zip'
    fz = zipfile.ZipFile(driver_zip, 'r')
    for file in fz.namelist():
        fz.extractall('./driver')
        fz.close()
    if os.path.exists(driver_zip):
        os.remove(driver_zip)


'''
try:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', chrome_options=chrome_options)
    chrome_version = driver.capabilities['browserVersion']
    driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]

    chrome_version_main = chrome_version.rpartition('.')[0]
    driver_version_main = driver_version.rpartition('.')[0]
    print(' Chrome Version:', chrome_version_main, '\n', 'Driver Version:', driver_version_main)
    driver.close()
    driver.quit()
    if chrome_version_main != driver_version_main:
        print('Chrome版本和Driver版本不匹配，请根据Chrome版本更新Driver版本，替换Driver目录下chromedriver.exe，Driver下载地址：')
        print('https://npm.taobao.org/mirrors/chromedriver/')

except Exception as e:
    print('Chrome版本和Driver版本不匹配，请更新Driver版本，Driver下载地址：')
    print('https://npm.taobao.org/mirrors/chromedriver/')
'''
