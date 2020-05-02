import requests
from bs4 import BeautifulSoup

HOME_URL = 'http://customer.onebroadband.in/Customer/Default.aspx'
LOGIN_URL = 'http://customer.onebroadband.in/Customer/LoginClient.aspx?h8=1'
IFRAME_URL = 'http://customer.onebroadband.in/Customer/Gauge.aspx'


class User:

    def __init__(self, username, password='1234'):
        self.username = username
        self.password = password
        self.mac = None
        self.plan = None

    def execute(self):
        with requests.Session() as request:
            home_page = BeautifulSoup(request.get(HOME_URL).content, 'html.parser')
            payload = {'__VIEWSTATE': home_page.find(id='__VIEWSTATE').get('value'),
                       '__VIEWSTATEGENERATOR': home_page.find(id='__VIEWSTATEGENERATOR').get('value'),
                       '__EVENTVALIDATION': home_page.find(id='__EVENTVALIDATION').get('value'),
                       'txtUserName': self.username,
                       'txtPassword': self.password,
                       'hdnloginwith': 'username',
                       'save': 'LogIn'
                       }

            login_page = BeautifulSoup(request.post(LOGIN_URL, data=payload).content, 'html.parser')
            if login_page.find('iframe'):
                frame = BeautifulSoup(request.get(IFRAME_URL).content, 'html.parser')
                self.mac = frame.find(id='lblMacAddress').text
                self.plan = frame.find(id='lblPlanName').text

    def __str__(self):
        return f'{self.username},{self.mac},{self.plan}\n'

    def __bool__(self):
        return self.mac is not None
