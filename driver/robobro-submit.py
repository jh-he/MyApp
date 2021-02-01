from robobrowser import RoboBrowser
import requests
import webbrowser

url = "http://reliability.mot.com"
login_url = url + "/ALTV4/Login.aspx"

username = 'hjh4'
password = 'J1anhua!2'

br = RoboBrowser(history=True, parser='lxml')

br.open(login_url)

signin = br.get_form(id='form1')
signin['ctl00$MainContentPage$ctrLogin$UserName'].value = username
signin['ctl00$MainContentPage$ctrLogin$Password'].value = password
signin['ctl00$MainContentPage$ctrLogin$LoginButton'].value = 'Submit'
print(br.url)
br.submit_form(signin)
