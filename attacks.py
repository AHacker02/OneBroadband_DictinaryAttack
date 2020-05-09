import requests
from bs4 import BeautifulSoup


def login(username, password='1234'):
    """The function tries to login with the username.
    :returns Dictionary {"username":,"Mac":,"Plan"}"""

    home_url = 'http://customer.onebroadband.in/Customer/Default.aspx'
    login_url = 'http://customer.onebroadband.in/Customer/LoginClient.aspx?h8=1'
    iframe_url = 'http://customer.onebroadband.in/Customer/Gauge.aspx'

    user = {"Username": username,
            "Password": password,
            "Mac": None,
            "Plan": None
            
            }

    # Open homepage
    with requests.Session() as request:
        home_page = BeautifulSoup(request.get(home_url).content, 'html.parser')
        payload = {'__VIEWSTATE': home_page.find(id='__VIEWSTATE').get('value'),
                   '__VIEWSTATEGENERATOR': home_page.find(id='__VIEWSTATEGENERATOR').get('value'),
                   '__EVENTVALIDATION': home_page.find(id='__EVENTVALIDATION').get('value'),
                   'txtUserName': user["Username"],
                   'txtPassword': user["Password"],
                   'hdnloginwith': 'username',
                   'save': 'LogIn'
                   }

        # Try to login with the username
        login_page = BeautifulSoup(request.post(login_url, data=payload).content, 'html.parser')
        if login_page.find('iframe'):
            frame = BeautifulSoup(request.get(iframe_url).content, 'html.parser')
            user["Mac"] = frame.find(id='lblMacAddress').text
            user["Plan"] = frame.find(id='lblPlanName').text
