# -*- coding:utf-8 -*-

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium import webdriver
import requests
import random
import json


ua = UserAgent(use_cache_server=False)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'user-agent': '%s' % ua.random,
    'referer': 'http://http://wap.wawa.fm'
    }


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


# 清理缓存
def get_clear_browsing_button(driver):
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    driver.get('chrome://settings/clearBrowserData')
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)
    get_clear_browsing_button(driver).click()
    wait.until_not(get_clear_browsing_button)


# 验证订阅是否成功
def gettoken(phone):
    url = 'https://m.12530.com/order/rest/login/url.do?callback=CMloginDone&data={"youCallbackName":"CMloginDone","channelCode":"0021085","loginType":"3","key":"4b00f9cb46fc4088bfd8bc0b185d2dd2","msisdn":"' + phone + '"}&0.7808647957243932v4s.0a.d0dc41a48cd44e369f12f579a6aae0b1n.4b112bba83d14290a068da51f45b2884RNum0.44625488580527617'
    df = requests.get(url, headers=headers)
    token = json.loads(df.text.split('(')[1].replace(')', ''))['token']
    cookies = df.cookies.get_dict()
    return token, cookies


def isopenmonth(token, cookies):
    url = 'https://m.12530.com/order/rest/crbt/month/query.do?callback=CMisOpenMonth&data={"youCallbackName":"CMisOpenMonth","channelCode":"0021085","token":"%s","serviceId":"698039020100000108"}&0.360744490051056v4s.0a.d0dc41a48cd44e369f12f579a6aae0b1n.4b112bba83d14290a068da51f45b2884RNum0.44625488580527617' % token
    df = requests.get(url, headers=headers, cookies=cookies)
    cookies = df.cookies.get_dict()
    status_month = json.loads(df.text.split('(')[1].replace(')', ''))['status']
    return cookies, status_month
