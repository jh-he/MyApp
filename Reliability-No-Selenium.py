import requests
from bs4 import BeautifulSoup


class login(object):

    def __init__(self):
        # 构造Session
        self.session = requests.session()

        self.url = 'http://reliability.mot.com/ALTV4/Login.aspx'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36'
        }
        r = requests.get(self.url)
        # s = requests.Session()
        # r = s.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        v_state = soup.select('#__VIEWSTATE')[0].attrs.get('value')
        v_stategen = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')
        event_valid = soup.select('#__EVENTVALIDATION')[0].attrs.get('value')

        self.data = {
            '__VIEWSTATE': v_state,
            '__VIEWSTATEGENERATOR': v_stategen,
            '__EVENTVALIDATION': event_valid,
            'ctl00$MainContentPage$ctrLogin$UserName': 'hejh4',
            'ctl00$MainContentPage$ctrLogin$Password': 'J1anhua!3',
            'ctl00$MainContentPage$ctrLogin$LoginButton': 'Submit'
        }

        # 在session中发送登录请求，此后这个session里就存储了cookie
        self.session.post(self.url, self.data, headers=self.headers)

    def submit(self):
        # 登录后才能访问的网页
        submit_url = "http://reliability.mot.com/ALTV4/Registration/Submit_New.aspx"
        rs = self.session.get(submit_url, headers=self.headers)

        soup = BeautifulSoup(rs.text, 'lxml')
        print(soup)
        v_state = soup.select('#__VIEWSTATE')[0].attrs.get('value')
        v_stategen = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')
        event_valid = soup.select('#__EVENTVALIDATION')[0].attrs.get('value')

        submit_view = {
            '__VIEWSTATE': v_state,
            '__VIEWSTATEGENERATOR': v_stategen,
            '__EVENTVALIDATION': event_valid,
        }

        # 这样的方式也可以访问
        # rs = requests.get(setting_url, headers=headers, cookies=session.cookies)




if __name__ == '__main__':
    login().submit()
