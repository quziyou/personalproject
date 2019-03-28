import time
import random
import pymysql
from fake_useragent import UserAgent
from requests_html import HTMLSession


ua = UserAgent(verify_ssl=False)

header = {
    'User-Agent': ua.random,
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Hosts': 'hm.baidu.com',
    'Referer': 'http://www.xicidaili.com/nn',
    'Connection': 'keep-alive'}


def mysql_connect():  # 创建数据库连接
    db = pymysql.connect(
        host='47.94.240.32',
        user='quziyou',
        password='0739@KunMing',
        db='proxy_info',
        port=5389)
    return db


def get_ip(headers, db, page_num):
    url = 'http://www.xicidaili.com/nn/'
    cursor = db.cursor()
    session = HTMLSession()
    for i in range(page_num):
        url = url + str(i + 1)
        r = session.get(url, headers=headers)
        ip = []
        port = []
        addr = []
        proxy_kind = []
        proxy_type = []
        proxy_speed = []
        connect_speed = []

        contents = r.html.find('#ip_list tr')[1:]

        for i in range(len(contents)):
            items = contents[i]
            contents_list = items.text.split('\n')
            if len(contents_list) >= 7:
                ip.append(contents_list[0])
                port.append(contents_list[1])
                addr.append(contents_list[2])
                proxy_kind.append(contents_list[3])
                proxy_type.append(contents_list[4])
                proxy_speed.append(
                    float(
                        items.find('.bar')[0].attrs['title'].split('秒')[0]))
                connect_speed.append(
                    float(items.find('.bar')[1].attrs['title'].split('秒')[0]))
            else:
                ip.append(contents_list[0])
                port.append(contents_list[1])
                addr.append('null')
                proxy_kind.append(contents_list[2])
                proxy_type.append(contents_list[3])
                proxy_speed.append(
                    float(
                        items.find('.bar')[0].attrs['title'].split('秒')[0]))
                connect_speed.append(
                    float(items.find('.bar')[1].attrs['title'].split('秒')[0]))
        data = [
            x for x in zip(
                ip,
                port,
                addr,
                proxy_kind,
                proxy_type,
                proxy_speed,
                connect_speed)]

        sql = '''INSERT INTO xici_proxy(ip, port, addr, proxy_kind, proxy_type, proxy_speed, connect_speed) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        try:
            cursor.executemany(sql, data)
            db.commit()
            print('完成第{}次插入数据'.format(i+1))
            time.sleep(random.choice(range(10)))
        except BaseException:
            db.rollback()
            time.sleep(random.choice(range(10)))
            print('数据插入失败！')
    cursor.close()


if __name__ == '__main__':
    db = mysql_connect()
    get_ip(header, db, 50)
    db.close()
