# -*- coding:utf-8 -*-

from selenium.webdriver.common.keys import Keys
import browsertool
import random
import time


phone = '13837915792'
url = 'https://wawa.fm/static/isp3/cmcc083.html?appid=9d8a121ce581499d324&channel=104&cmcc=63254000545&nonce_str=4t1hGUdSiardaQFN&order_id=1hhplqho7xd1543914266892&phone=13837915792&privence=河南&sign=f864026fb972af6afe148216d4a0ed778173e941&time_stamp=1543914338329&track=大悲咒 - 敬善媛&uri1=https%3A%2F%2Fwaw'

browser = browsertool.create_browser('open')
# browsertool.clear_cache(browser)

browser.get(url)

# 输入手机号
input_phone = browsertool.select_em(browser, '.order_form_input')
if input_phone:
    # TouchActions(browser).scroll_from_element(input_phone, 0, -200).perform()
    # TouchActions(browser).tap(input_phone).perform()
    input_phone.send_keys(phone)
    time.sleep(random.choice(range(3)))
    input_phone.clear()
    input_phone.send_keys(phone)
    input_phone.send_keys(Keys.BACK_SPACE)
    time.sleep(random.choice(range(3)))
    input_phone.send_keys(phone[-1])
    time.sleep(random.choice(range(10)))
else:
    print('没有这个元素')

# 点击获取验证码
button_code = browsertool.select_em(browser, '.set_ring')
if button_code:
    button_code.click()
    # TouchActions(browser).scroll_from_element(button_code, 0, -200).perform()
    # TouchActions(browser).tap(button_code).perform()
    time.sleep(random.choice(range(10)))
else:
    print('没有这个元素')


checkpage = browsertool.select_em(browser, '#frame')

if checkpage:
    browser.switch_to.frame(checkpage)
    # 启动订购流程
    button_code_frame = browsertool.select_em(browser, '.sendCode')
    if button_code_frame:
        print('需要验证码')
    else:
        button_okPay = browsertool.select_em(browser, '#okPay')
        if button_okPay and button_okPay.get_attribute("class") == '':
            button_okPay.click()
            # TouchActions(browser).tap(button_okPay).perform()
            time.sleep(random.choice(range(10)))
            button_code_frame = browsertool.select_em(browser, '.sendCode')
            if button_code_frame:
                print('需要验证码')

time.sleep(random.choice(range(10)))
token, cookies = browsertool.gettoken(phone)
status_month = browsertool.isopenmonth(token, cookies)
if status_month == 1:
    print('订阅成功')
    # browser.close()
else:
    print('订购失败')
    # browser.close()
