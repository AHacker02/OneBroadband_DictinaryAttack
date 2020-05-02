import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = 'http://customer.onebroadband.in/Customer/Default.aspx'


def __init__(self, username, password='1234'):
    self.username = username
    self.password = password


def login(self):
    pass


def execute(self):
    with webdriver.chrome() as driver:
        driver.get(URL)
