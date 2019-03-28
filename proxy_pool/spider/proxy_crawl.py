import json
import requests
from config import get_headers
from requests_html import HTMLSession
from util.browsertool import create_browser, select_em

header = get_headers()

urls = 'http://www.xicidaili.com/nn/1'

session = HTMLSession()


def crawl_xici(url):  # 爬取西刺免费代理
    headers = get_headers()
    try:
        resp = session.get(url, headers=headers)
        contents = resp.html.find('#ip_list tr')[1:]
        ip = []
        port = []
        proxy_kind = []
        proxy_type = []
        for i in range(len(contents)):
            items = contents[i]
            contents_list = items.text.split('\n')
            ip.append(contents_list[0])
            port.append(contents_list[1])
            if len(contents_list) >= 7:
                proxy_kind.append(contents_list[3])
                proxy_type.append(contents_list[4])
            else:
                proxy_kind.append(contents_list[2])
                proxy_type.append(contents_list[3])
        return list(zip(ip, port, proxy_kind, proxy_type))
    except BaseException as e:
        # print(e)
        return None


def crawl_cloud(url):  # 爬取云代理免费代理
    headers = get_headers()
    try:
        resp = session.get(url, headers=headers)
        contents = resp.html.find('#list tr')[1:]
        ip = []
        port = []
        proxy_kind = []
        proxy_type = []
        for i in range(len(contents)):
            items = contents[i]
            contents_list = items.text.split('\n')
            ip.append(contents_list[0])
            port.append(contents_list[1])
            proxy_kind.append('高匿')
            proxy_type.append(contents_list[3])
        return list(zip(ip, port, proxy_kind, proxy_type))
    except BaseException as e:
        # print(e)
        return None



def crawl_github(url):
    headers = get_headers()
    try:
        resp = requests.get(url, headers=headers, timeout=15).text
        contents = resp.split('\n')[:-2]
        ip = []
        port = []
        types = []
        protocol = []
        for i in contents:
            test = json.loads(i)
            if test['country'] == 'CN':
                ip.append(test['host'])
                port.append(test['port'])
                if test['anonymity'] == 'high_anonymous':
                    types.append('高匿')
                elif test['anonymity'] == 'anonymous':
                        types.append('匿名')
                else:
                    types.append('透明')
                protocol.append(test['type'].upper())
        return zip(ip, port, types, protocol)
    except BaseException as e:
        # print(e)
        return None


if __name__ == '__main__':
    a = crawl_xici(urls)
    for i in a:
        print(i)
