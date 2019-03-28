# -*- coding:utf-8 -*-

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from config import get_headers
from selenium import webdriver


headers = get_headers()


# 创建一个浏览器引擎

def create_browser(op_type):
    if op_type == 'close':
        chrome_options = webdriver.ChromeOptions()
        # mobile_emulation = {"deviceName": "Galaxy S5"}
        chrome_options.add_argument('--headless')
        # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        for key, value in headers.items():
            chrome_options.add_argument(key + '=' + value)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.delete_all_cookies()
        return browser
    elif op_type == 'open':
        chrome_options = webdriver.ChromeOptions()
        # mobile_emulation = {"deviceName": "Galaxy S5"}
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--proxy-server=http://123.7.61.8:53281')
        # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        for key, value in headers.items():
            chrome_options.add_argument(key + '=' + value)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.delete_all_cookies()
        return browser
    else:
        return None


# 利用CSS定位检测元素是否存在
def check_frame_em(browser, css):  # frame上检测
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        return True
    except BaseException:
        return False


def check_em(browser, css):  # 基层检测
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        return True
    except BaseException:
        return False


# 利用CSS定位元素
def select_frame_em(browser, css):  # frame上选择
    status = check_frame_em(browser, css)
    if status:
        wait = WebDriverWait(browser, 10)
        em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        return em
    else:
        return None


def select_em(browser, css):  # 基层选择
    status = check_em(browser, css)
    if status:
        wait = WebDriverWait(browser, 10)
        em = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        return em
    else:
        return None
