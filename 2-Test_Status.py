from bs4 import BeautifulSoup
import os
import random
import sys
import zipfile

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

global driver


def login_check():
    username = 'hejh4'
    password = 'J1anhua!3'
    url = 'http://reliability.mot.com/ALTV4/Login.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    # print(soup)
    v_state = soup.select('#__VIEWSTATE')[0].attrs.get('value')
    v_stategen = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')
    event_valid = soup.select('#__EVENTVALIDATION')[0].attrs.get('value')

    form_data = {
        '__VIEWSTATE': v_state,
        '__VIEWSTATEGENERATOR': v_stategen,
        '__EVENTVALIDATION': event_valid,
        'ctl00$MainContentPage$ctrLogin$UserName': username,
        'ctl00$MainContentPage$ctrLogin$Password': password,
        'ctl00$MainContentPage$ctrLogin$LoginButton': 'Submit'
    }

    # 在session中发送登录请求，此后这个session里就存储了cookie
    login_page = requests.post(url, form_data, headers=headers)
    soup = BeautifulSoup(login_page.text, 'lxml')
    login_status = soup.find('span', class_='TreeViewNodeStyle')

    if login_status is None:
        sys.exit('Alt website login failed, please make sure your username and password filled correctly, '
                 'and have a stable internet connection. After that, please restart the program.')


def app_info():
    print("\033[0;33;40m Current Version:20210127\033[0m")
    print('If you have any problem of using this program, pls contact Jianhua He(IT Code: hejh4)\n')


def start_driver():
    global driver
    try:
        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument('--headless')
        driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', options=chrome_opt)

    except Exception as e:
        # driver.quit()
        error_msg = str(e)
        old_version = "This version of ChromeDriver only supports"
        if old_version in error_msg:
            chrome_version = error_msg.split("Current browser version is ")[1][0:14]
            driver_version = chrome_version.rpartition('.')[0]
            print("Updating ChromeDriver version to %s, please wait a few seconds..." % driver_version)

            # Download Chrome Driver
            rs = requests.get('https://npm.taobao.org/mirrors/chromedriver/')
            soup = BeautifulSoup(rs.text, 'lxml')
            for x in soup.find_all('a'):
                target_version = x.get_text()
                if driver_version in target_version:
                    break

            driver_url = 'https://npm.taobao.org/mirrors/chromedriver/' + target_version + 'chromedriver_win32.zip'
            user_agent = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/73.0.3683.103 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '
                'Version/5.1 Safari/534.50',
                'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
                'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 '
                'Chromium/10.0.642.0 Chrome/10.0.642.0 Safari/534.16',
            ]

            headers = {
                'User-Agent': random.choice(user_agent)
            }

            print('Downloading...')
            driver_zip = requests.get(driver_url, headers=headers)
            with open('./driver/chromedriver_win32.zip', 'wb') as file:
                file.write((driver_zip.content))

            # 自动解压缩zip并删除
            print('Unzipping...')
            driver_zip = './driver/chromedriver_win32.zip'
            fz = zipfile.ZipFile(driver_zip, 'r')
            for file in fz.namelist():
                fz.extractall('./driver')
                fz.close()
            if os.path.exists(driver_zip):
                os.remove(driver_zip)

            # Restart Chrome Driver
            driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', options=chrome_opt)

            print('ChromeDriver updated, program starting...')
    print('Test case Submitting...')


def login():
    driver.get("http://reliability.mot.com/ALTV4/ALTManager_Home.aspx")
    driver.find_element_by_id("MainContentPage_ctrLogin_UserName").send_keys(username)
    driver.find_element_by_id("MainContentPage_ctrLogin_Password").send_keys(password)
    driver.find_element_by_id("MainContentPage_ctrLogin_LoginButton").click()









def stop_driver():
    global driver
    print('Submit progress done, program closing, pls open the excel for details.')
    driver.close()
    driver.quit()











if __name__ == "__main__":
    app_info()
    # login_check()
    start_driver()
    driver.implicitly_wait(30)
    driver.get("http://reliability.mot.com/ALTV4/ALTManager_Home.aspx")
    driver.find_element_by_id("MainContentPage_ctrLogin_UserName").send_keys('hejh4')
    driver.find_element_by_id("MainContentPage_ctrLogin_Password").send_keys('J1anhua!3')
    s1 = driver.find_element_by_id("MainContentPage_ctrLogin_LoginButton").click()
    s2 = driver.find_element_by_xpath(
        "(.//*[normalize-space(text()) and normalize-space(.)='New Tests'])[1]/following::span[2]").click()

    stop_driver()

'''
wb = load_workbook('0-Master_File_Reliability.xlsm', keep_vba=True)
ws_s = wb["Submit"]
ws_a = wb['ALT Number']

mrs = ws_s.max_row
mra = ws_a.max_row

# print(mrs, mra)

# print(ws_s['C2':'J52'])

dvt_dic = []
for rdvt in range(2, mrs + 1):
    temp_list = []
    if ws_s.cell(row=rdvt, column=3).value == "Y":
        # pid = rdvt
        cc = ws_s.cell(row=rdvt, column=3).value
        cd = ws_s.cell(row=rdvt, column=4).value
        ce = ws_s.cell(row=rdvt, column=5).value
        cf = ws_s.cell(row=rdvt, column=6).value
        cg = ws_s.cell(row=rdvt, column=7).value
        ch = ws_s.cell(row=rdvt, column=8).value
        ci = ws_s.cell(row=rdvt, column=9).value
        cj = ws_s.cell(row=rdvt, column=10).value

        temp_dvt = [cc, cd, ce, cf, cg, ch, ci, cj]
        dvt_dic.append(temp_dvt)
dvt_count = len(dvt_dic)
print("共计需要提交 %s 项DVT测试" % dvt_count)

car_dic = []
for rx in range(2, mrs + 1):
    if ws_s.cell(row=rx, column=12).value == "Y":
        cl = ws_s.cell(row=rx, column=12).value
        cm = ws_s.cell(row=rx, column=13).value
        cn = ws_s.cell(row=rx, column=14).value
        co = ws_s.cell(row=rx, column=15).value
        cp = ws_s.cell(row=rx, column=16).value
        cq = ws_s.cell(row=rx, column=17).value
        cr = ws_s.cell(row=rx, column=18).value

        temp_car = [cl, cm, cn, co, cp, cq, cr]
        car_dic.append(temp_car)
car_count = len(dvt_dic)

print("共计需要提交 %s 项Carrier测试" % dvt_count)

df_dvt = pd.DataFrame.from_dict(dvt_dic)
df_car = pd.DataFrame.from_dict(car_dic)

print(df_dvt)
print(df_car)
# ws['G2'] = 'passed'
# wb.save('Auto-Submission.xlsm')

'''
'''
class login(object):

    def __init__(self):
        # 构造Session
        self.session = requests.session()
        self.username = 'hejh4'
        self.password = 'J1anhua!3'

        self.url = 'http://reliability.mot.com/ALTV4/Login.aspx'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'
        }
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'lxml')
        v_state = soup.select('#__VIEWSTATE')[0].attrs.get('value')
        v_stategen = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')
        event_valid = soup.select('#__EVENTVALIDATION')[0].attrs.get('value')

        self.data = {
            '__VIEWSTATE': v_state,
            '__VIEWSTATEGENERATOR': v_stategen,
            '__EVENTVALIDATION': event_valid,
            'ctl00$MainContentPage$ctrLogin$UserName': self.username,
            'ctl00$MainContentPage$ctrLogin$Password': self.password,
            'ctl00$MainContentPage$ctrLogin$LoginButton': 'Submit'
        }

        # 在session中发送登录请求，此后这个session里就存储了cookie
        self.session.post(self.url, self.data, headers=self.headers)

    def submit(self):
        ALT_number = 'WH128516'
        report_url = "http://reliability.mot.com/ALTV4/Reports/ProtoCertTestReport_Functional.aspx?Test_Seqno=" + ALT_number
        rs = self.session.get(report_url, headers=self.headers)
        soup = BeautifulSoup(rs.text, 'lxml')
        url_buttons = soup(class_='Buttons', value='Download')
        session = requests.Session()
        session.auth = HttpNtlmAuth(self.username, self.password)
        # session.get('http://100.64.182.32:200/')
        for url_button in url_buttons:
            download_link = url_button.get('url')
            doc_name = download_link.rpartition('/')[2]
            r = session.get(download_link)
            print(r.status_code)
            with open('./Test Report/' + str(doc_name), 'wb') as file:
                file.write((r.content))


if __name__ == '__main__':
    login().submit()
'''
