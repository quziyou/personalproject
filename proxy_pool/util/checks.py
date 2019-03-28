import time
import json
import datetime
import requests
from spider.proxy_crawl import crawl_xici, crawl_github, crawl_cloud
from config import get_headers, CHECHINFO_IP, TEST_IP


def get_info(ip, port):  # 获取代理IP的详细信息
    url = CHECHINFO_IP
    headers = get_headers()
    proxies = {
        'http': 'http://{ip}:{port}'.format(ip=ip, port=port),
        'https': 'http://{ip}:{port}'.format(ip=ip, port=port)
    }
    params = {'ip': ip}
    try:
        start_time = time.time()
        resp = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=15).json()
        end_time = time.time()
        speed = '%.2f' % (end_time - start_time)
        text = resp['data']
        if text['country'] and text['region']:
            country = text['country']
            region = text['region']
            city = text['city']
            isp = text['isp']
            return country, region, city, isp, speed
        else:
            return None
    except BaseException as e:
        print(e)
        return None


def check_ip(ip, port):  # 检测代理IP是否可用
    url = TEST_IP
    headers = get_headers()
    proxies = {
        'http': 'http://{ip}:{port}'.format(ip=ip, port=port),
        'https': 'http://{ip}:{port}'.format(ip=ip, port=port)
    }
    try:
        start_time = time.time()
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=15).text
        end_time = time.time()
        speed = '%.2f' % (end_time - start_time)
        if ip == json.loads(resp.replace(';', '').split('=')[-1].strip())['cip']:
            return speed
        else:
            return None
    except:
        return None


def merge_info(url_dict, mydb):  # 整合代理IP信息并插入数据库
    if url_dict['host'] == 'xici':
        iplist = crawl_xici(url_dict['url'])
    elif url_dict['host'] == 'github':
        iplist = crawl_github(url_dict['url'])
    elif url_dict['host'] == 'cloud':
        iplist = crawl_cloud(url_dict['url'])

    if iplist:
        for i in iplist:
            ip, port, types, protocol = i
            ip_info = get_info(ip, port)
            if ip_info:
                country, region, city, isp, speed = ip_info
                value = {'ip': ip, 'port': port, 'types': types, 'protocol': protocol,
                         'country': country, 'region': region, 'city': city,
                         'isp': isp, 'speed': float(speed)}
                try:
                    mydb.insert(value=value)
                    time.sleep(1)
                except BaseException as e:
                    print(e)
                time.sleep(1)
            else:
                continue


def update_info(mydb):  # 检测并更新数据库中的代理IP
    ip_pool = mydb.select()
    for ip_info in ip_pool:
        ip, port, _ = ip_info
        infos = get_info(ip, port)
        count = 0
        while not infos:
            if count <= 5:
                infos = get_info(ip, port)
                count += 1
                time.sleep(5)
            else:
                infos = None
                break
        if infos:
            country, region, city, isp, speed = infos
            updatetime = datetime.datetime.now()
            conditions = {'ip': ip, 'port': port}
            value = {'country': country, 'region': region, 'city': city,
                     'isp': isp, 'speed': speed, 'updatetime': updatetime}
            mydb.update(conditions=conditions, value=value)
        else:
            conditions = {'ip': ip, 'port': port}
            mydb.delete(conditions=conditions)


if __name__ == '__main__':
    urls = 'http://www.xicidaili.com/nn/1'
