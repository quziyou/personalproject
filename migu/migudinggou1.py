import browsertool
import time

browser = browsertool.create_browser('open')

url = 'https://wawa.fm/static/isp3/cmcc085.html?appid=9d8a121ce581499d324&channel=104&cmcc=60076224582&nonce_str=bPqrYPCiitOGLfaH&phone=13607007109&sign=9eb3fd49395d9dabba48431c01cdee25bc832b37&time_stamp=1542876015818&track=%E7%8E%AF%E5%8D%AB%E5%B7%A5%E4%BA%BA%E4%B9%8B%E6%AD%8C%20-%20%E8%93%89%E8%93%89'

browser.get(url)

payButton = browsertool.select_frame_em(browser, '.okPay')

if payButton:
    time.sleep(5)
    payButton.click()
    time.sleep(5)
    browser.switch_to.default_content()
    for i in browser.find_elements_by_tag_name('body'):
        print(i.text)
else:
    print('没有这个元素!')
