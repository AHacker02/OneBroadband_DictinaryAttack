import requests
from bs4 import BeautifulSoup
from user import User


def login(user: User):
    """The function tries to login with the username.
    :returns User object"""

    home_url = 'http://customer.onebroadband.in/Customer/Default.aspx'
    login_url = 'http://customer.onebroadband.in/Customer/LoginClient.aspx?h8=1'
    iframe_url = 'http://customer.onebroadband.in/Customer/Gauge.aspx'

    # Open homepage%
    try:
        with requests.Session() as request:
            home_page = BeautifulSoup(request.get(home_url).content, 'html.parser')
            payload = {'__VIEWSTATE': home_page.find(id='__VIEWSTATE').get('value'),
                       '__VIEWSTATEGENERATOR': home_page.find(id='__VIEWSTATEGENERATOR').get('value'),
                       '__EVENTVALIDATION': home_page.find(id='__EVENTVALIDATION').get('value'),
                       'txtUserName': user.username,
                       'txtPassword': user.password,
                       'hdnloginwith': 'username',
                       'save': 'LogIn'
                       }

            # Try to login with the username
            login_page = BeautifulSoup(request.post(login_url, data=payload).content, 'html.parser')
            if login_page.find('iframe'):
                frame = BeautifulSoup(request.get(iframe_url).content, 'html.parser')
                user.mac = frame.find(id='lblMacAddress').text
                user.plan = frame.find(id='lblPlanName').text
    except requests.exceptions.ConnectionError:
        print('Connection Error')
        exit(0)
