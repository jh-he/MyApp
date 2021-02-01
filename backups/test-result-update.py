# -*- coding: utf-8 -*-
import time
import xlwings as xw
from selenium import webdriver

alt_number = ''



def xl_read():

    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False
    app.screen_updating = True

    wb = app.books.open('./auto-submission.xlsm')
    ws = wb.sheets['Submission-number']

    for i in range(11, 20):
        Query_cell = 'C'+str(i+2)
        alt_number_link = xw.Range(Query_cell).hyperlink
        status_cell = 'G' + str(i+2)
        result_cell = 'H' + str(i+2)
        comments_cell = 'I' + str(i+2)
        status = ws.range(status_cell).value
        driver.get(alt_number_link)
        if status == 'Submitted' or status == 'Assigned' or status == 'In-Progress':
            status_update = driver.find_element_by_id("MainContentPage_lblStatus_Name").text
            test_result = driver.find_element_by_xpath("//*[@id='MainContentPage_lblTestResult']").text
            notes = driver.find_element_by_id("MainContentPage_lblALTEngrTestNotes").text
        ws.range(status_cell).value = status_update
        ws.range(result_cell).value = test_result
        ws.range(comments_cell).value = notes

        print('Status', status)
        print('Status_update', status_update)
        print('Result', test_result)
        print('Failure', notes)




if __name__ == "__main__":
    print("\033[0;31;40m\t如果使用过程中遇到问题，请联系何建华 hejh4@lenovo.com...\033[0m")
    print('正在帮您查询测试结果，请耐心等待...')

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    global driver
    driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe')
    driver.implicitly_wait(50)
    xl_read()
    # driver.get("http://reliability.mot.com/ALTV4/Reports/ProtoCertTestReport_Functional.aspx?Test_Seqno=WH122027")
    '''driver.find_element_by_id("MainContentPage_ctrLogin_UserName").send_keys(username)
    driver.find_element_by_id("MainContentPage_ctrLogin_Password").send_keys(password)
    driver.find_element_by_id("MainContentPage_ctrLogin_LoginButton").click()'''


    '''driver.close()
    driver.quit()'''

    '''wb.save()
    wb.close()
    time.sleep(2)
    app.quit()

    print('查询完成，请关闭该页面，打开工作表')'''
