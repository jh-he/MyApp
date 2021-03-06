# -*- coding: utf-8 -*-
import time
import xlwings as xw
from tkinter import *
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service


# All submitted list
fun_label = 0
total = 0
varnum = 0
slash_qty = 0
alt_number = ''

submitted_list = []
alt_number_link_list = []
var_list = []
var = []
test_number_list = []
test_hyperlink = {}

# Test list
test_slash_lists = {'DVT MDu04': 1, 'DVT MDu20': 3, 'DVT MDu21': 4, 'DVT MDu23': 3, 'DVT MDu28': 1, 'DVT MDu30': 8,
                    'DVT MDu39': 12, 'DVT MDu42': 11, 'DVT MDu49': 21, 'DVT MDu51': 18, 'DVT MDu52': 30, 'DVT MDu55': 6,
                    'DVT MDu56': 6, 'DVT MXc03': 3}


def xl_read():
    global app, wb, ws, ws2, username, password, lab, pscode, category, subcat, perfmby, EE1, EE2, EM, ME1, ME2, MM, factory
    global vintage, softver, buildnumber, subpurpose, purdetails, requestfrom, reusepercent, qty, testcase, expdate, ntests

    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = True

    wb = app.books.open('./auto-submission.xlsm')
    ws = wb.sheets['Submission-Details']
    ws2 = wb.sheets['Submission-number']

    # password
    username = ws.range('B27').value
    password = ws.range('B28').value
    lab = ws.range('B1').value
    pscode = ws.range('B2').value
    category = ws.range('B3').value
    subcat = ws.range('B4').value
    perfmby = ws.range('B6').value

    # ALT submitter information
    EE1 = ws.range('B9').value
    EE2 = ws.range('B10').value
    EM = ws.range('B11').value
    ME1 = ws.range('E9').value
    ME2 = ws.range('E10').value
    MM = ws.range('E11').value

    # Sample info
    factory = ws.range('B13').value
    vintage = ws.range('E13').value
    softver = ws.range('B14').value
    buildnumber = ws.range('B15').value
    # project info
    subpurpose = ws.range('B17').value
    purdetails = ws.range('B18').value
    requestfrom = ws.range('B20').value
    reusepercent = 0
    qty = 0
    testcase = ''
    convert_date = ws.range('B21').value
    expdate = convert_date.strftime("%Y/%m/%d")
    ntests = int(ws.range('E3').value)


def pre_content():
    global testcase, driver
    driver.find_element_by_xpath(
        "(.//*[normalize-space(text()) and normalize-space(.)='New Tests'])[1]/following::span[2]").click()
    Select(driver.find_element_by_id("MainContentPage_ddlLab")).select_by_visible_text(lab)
    driver.find_element_by_id("MainContentPage_btnProductLookup").click()
    driver.find_element_by_id("MainContentPage_ctrLookUpLocalProduct_txtProductSearch").send_keys(pscode)
    driver.find_element_by_id("MainContentPage_ctrLookUpLocalProduct_txtProductSearch").send_keys(Keys.ENTER)
    driver.find_element_by_link_text("Select").click()
    Select(driver.find_element_by_id("MainContentPage_ddlTestCategory")).select_by_visible_text(category)
    Select(driver.find_element_by_id("MainContentPage_ddlTestSubCategory")).select_by_visible_text(subcat)
    Select(driver.find_element_by_id("MainContentPage_ddlTest")).select_by_visible_text(testcase)
    # 判断是DVT测试还是ALT测试
    if subcat in 'DVT Eval':
        Select(driver.find_element_by_id("MainContentPage_ddlTestPerformedBy")).select_by_visible_text(perfmby)
    # 判读是否符合自动填写slash线的测试
    global testshort
    if testshort in test_slash_lists.keys():
        count = test_slash_lists[testshort]
        for i in range(count):
            driver.find_element_by_id(
                "MainContentPage_controlMaterialInfo_gridProtoQuestions_txtProtoAnswer_" + str(i)).send_keys("/")


def post_content():
    # 填写其它项
    driver.find_element_by_id("MainContentPage_txtEE1CoreID").send_keys(EE1)
    if EE2 is not None:
        driver.find_element_by_id("MainContentPage_txtEE2CoreID").send_keys(EE2)
    if EM is not None:
        driver.find_element_by_id("MainContentPage_txtEMCoreID").send_keys(EM)
    driver.find_element_by_id("MainContentPage_txtME1CoreID").send_keys(ME1)
    if ME2 is not None:
        driver.find_element_by_id("MainContentPage_txtME2CoreID").send_keys(ME2)
    if MM is not None:
        driver.find_element_by_id("MainContentPage_txtMMCoreID").send_keys(MM)
    Select(driver.find_element_by_id("MainContentPage_ddlFactory")).select_by_visible_text(factory)
    Select(driver.find_element_by_id("MainContentPage_ddlVintageList")).select_by_visible_text(vintage)
    driver.find_element_by_id("MainContentPage_txtSoftwareVersion").send_keys(softver)
    driver.find_element_by_id("MainContentPage_txtBuildNumber").send_keys(buildnumber)
    Select(driver.find_element_by_id("MainContentPage_ddlSubmissionPurpose")).select_by_visible_text(subpurpose)
    driver.find_element_by_id("MainContentPage_txtSubmission_Purpose_Details").send_keys(purdetails)
    Select(driver.find_element_by_id("MainContentPage_ddlRequestFrom")).select_by_visible_text(requestfrom)
    driver.find_element_by_id("MainContentPage_txtExpStartDate").send_keys(expdate)
    driver.find_element_by_id("MainContentPage_txtQuantity").send_keys(qty)
    driver.find_element_by_id("MainContentPage_txtMaterialReusePercentage").send_keys(reusepercent)
    # 选择ALT测试function list


def alt_funcs_sel():
    checkboxes_num = len(driver.find_elements_by_xpath('//input[@type="checkbox"]'))
    table = driver.find_element_by_id('MainContentPage_controlProductFunction_gridProductFunction')
    table_rows = table.find_elements_by_tag_name('tr')

    def fun_labels():
        global fun_label
        global total
        for f in range(checkboxes_num - 1):
            txt_col = table_rows[f + 1].find_elements_by_tag_name('td')[0].text
            if txt_col != '':
                fun_label += 1
        total = fun_label + checkboxes_num

    fun_labels()
    window = Tk()
    window.title("Select ALT Functions")
    winWidth = 1200
    winHeight = 700
    # 获取屏幕分辨率
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    # 计算主窗口在屏幕上的坐标
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    # 设置窗口宽高固定
    # window.resizable(0, 0)
    vbar = Scrollbar(window, orient=VERTICAL)
    canvas = Canvas(window, yscrollcommand=vbar.set)
    vbar.config(command=canvas.yview)
    vbar.pack(side=RIGHT, fill=Y)
    frame0 = Frame(canvas)
    canvas.pack(side=TOP, expand=True, fill=BOTH)
    canvas.create_window(0, 0, window=frame0, anchor='nw')
    frame1 = Frame(frame0, width=200, height=700)
    frame2 = Frame(frame0, width=200, height=700)
    frame3 = Frame(frame0, width=200, height=700)
    frame4 = Frame(frame0, width=200, height=700)
    frame5 = Frame(frame0, width=200, height=700)
    frame1.grid(row=0, column=0)
    frame2.grid(row=0, column=1)
    frame3.grid(row=0, column=2)
    frame4.grid(row=0, column=3)
    frame5.grid(row=0, column=4)

    lbl_text = StringVar()
    Label(window, width=50, textvariable=lbl_text, fg='RED').pack()

    j = 0
    col_num = total // 5
    cbs = []
    for i in range(checkboxes_num - 1):
        row = i + 1
        txt_col1 = table_rows[row].find_elements_by_tag_name('td')[0].text
        txt_col2 = table_rows[row].find_elements_by_tag_name('td')[1].text
        if txt_col1 != '':
            j += 2
        else:
            j += 1

        if j < (total // 5):
            frm = frame1
        elif j < (total * 2 // 5):
            frm = frame2
        elif j < (total * 3 // 5):
            frm = frame3
        elif j < (total * 4 // 5):
            frm = frame4
        elif j < (total * 5 // 5):
            frm = frame5
        var.append(IntVar())
        if txt_col1 != '':
            Label(frm, text=txt_col1, font='Arial 8 bold').pack(side=TOP, anchor='w')
            cb = Checkbutton(frm, text=txt_col2, variable=var[-1])
            cbs.append(cb)
            cb.pack(side=TOP, anchor='w')

        else:
            cb = Checkbutton(frm, text=txt_col2, variable=var[-1])
            cbs.append(cb)
            cb.pack(side=TOP, anchor='w')

        def sel_all():
            if check_all.get() == 1:
                for c in cbs:
                    c.select()
                    c.config(state=DISABLED)

            if check_all.get() == 0:
                for c in cbs:
                    c.deselect()
                    c.config(state=NORMAL)

    def btn_cmd():
        global var_list
        global varnum
        for c in range(checkboxes_num - 1):
            v = var[c].get()
            var_list.append(v)
            varnum += v
        if varnum == 0:
            lbl_text.set('Pls select ALT Functions...')
        if varnum != 0:
            lbl_text.set('')
            window.destroy()

    check_all = IntVar()
    Checkbutton(window, text='Select All', variable=check_all, command=sel_all).pack()

    Button(window, text='OK', width=15, command=btn_cmd).pack()
    window.update()
    canvas.config(scrollregion=canvas.bbox("all"))
    window.mainloop()

    def alt_funcs_web():
        global var_list
        for index, val in enumerate(var_list):
            if val == 1:
                driver.find_element_by_id(
                    "MainContentPage_controlProductFunction_gridProductFunction_chkFunctionList_" + str(index)).click()
            else:
                continue

    alt_funcs_web()


def alt_eval_function():
    if subcat == 'ALT':
        driver.find_element_by_id("MainContentPage_controlProductFunction_chkSelectAll").click()
    # driver.find_element_by_id("MainContentPage_btnSubmit").click()


def submit():
    driver.find_element_by_id("MainContentPage_btnSubmit").click()
    al = driver.switch_to.alert
    time.sleep(1)
    al.accept()


def return_test_number():
    driver.get("http://reliability.mot.com/ALTV4/Registration/SubmissionModifyList.aspx")
    alt_table = driver.find_element_by_id('MainContentPage_gridSubmittedTest')
    table_rows = alt_table.find_elements_by_tag_name('tr')
    global alt_number
    alt_number = table_rows[1].find_elements_by_tag_name('td')[0].text
    hyperlink = 'http://reliability.mot.com/ALTV4/Reports/ProtoCertTestReport_Functional.aspx?Test_Seqno=' + alt_number
    sub_date = table_rows[1].find_elements_by_tag_name('td')[1].text
    product = table_rows[1].find_elements_by_tag_name('td')[2].text
    test = table_rows[1].find_elements_by_tag_name('td')[3].text
    status = table_rows[1].find_elements_by_tag_name('td')[4].text
    test_number_list.append(alt_number)
    test_hyperlink[alt_number] = hyperlink
    alt_list = [vintage, qty, alt_number, sub_date, product, test, status]
    submitted_list.append(alt_list)
    # alt_number_link_list.append(hyperlink)



def table_increase_row():
    ws2.range(f'2:{ntests + 1}').api.Insert()
    rng = ws2.range(f'A2:H{ntests + 1}')
    '''rng.color = None
    rng.api.Font.Bold = False
    rng.api.HorizontalAlignment = -4131'''

def fill_alt_table():
    ws2.range('A2').value = submitted_list
    for j in range(ntests):
        num = test_number_list[j]
        link = test_hyperlink[num]
        ws2[j + 1, 2].add_hyperlink(link, num)
    rng = ws2.range(f'A2:I{ntests + 1}')
    rng.color = None
    rng.api.Font.Bold = False
    rng.api.HorizontalAlignment = -4131

    '''rng2 = 'C2:C' + str(ntests+1)
    ws2.range(rng2).api.Font.Name = 'Arial'
    ws2.range(rng2).api.Font.Size = 9'''
    # Set Format of inserted rows


if __name__ == "__main__":
    print("\033[0;31;40m\t如果使用过程中遇到问题，请联系何建华 hejh4@lenovo.com...\033[0m")
    print('正在帮您提交测试单号，请耐心等待...')
    xl_read()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', chrome_options=chrome_options)
    driver.implicitly_wait(50)
    driver.get("http://reliability.mot.com/ALTV4/ALTManager_Home.aspx")
    driver.find_element_by_id("MainContentPage_ctrLogin_UserName").send_keys(username)
    driver.find_element_by_id("MainContentPage_ctrLogin_Password").send_keys(password)
    driver.find_element_by_id("MainContentPage_ctrLogin_LoginButton").click()

    print('Submitting ALT Test:')
    for i in range(1, 2):
        if ws[i, 6].value == 'Y':
            qty = int(ws[i, 8].value)
            if ws[i, 7].value is None:
                testcase = ws[i, 9].value
                subcat = 'ALT'
                testshort = ws[i, 9].value
            elif ws[i, 7].value == 'Eval':
                testcase = ws[i, 9].value + ' - ' + ws[i, 7].value
                subcat = 'ALT Eval'
                testshort = ws[i, 9].value
            pre_content()
            post_content()
            alt_funcs_sel()
            submit()
            return_test_number()
            print(alt_number, testcase)

    print('Submitting DVT Test:')
    for i in range(2, 55):
        if ws[i, 6].value == 'Y':
            qty = int(ws[i, 8].value)
            if ws[i, 7].value is None:
                testshort = ws[i, 9].value
                testcase = ws[i, 9].value + ' - ' + ws[i, 10].value
                subcat = 'DVT'
            elif ws[i, 7].value == 'Eval':
                testshort = ws[i, 9].value
                testcase = ws[i, 9].value + ' ' + ws[i, 7].value + ' - ' + ws[i, 10].value
                subcat = 'DVT Eval'
            pre_content()
            post_content()
            submit()
            return_test_number()
            print(alt_number, testcase)

    table_increase_row()
    fill_alt_table()

    driver.close()
    driver.quit()

    # service.stop()
    wb.save()
    wb.close()
    time.sleep(2)
    app.quit()

    print('提交全部完成，请关闭该页面，打开工作表')
