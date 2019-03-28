import requests
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)

headers = {
    'User-Agent': ua.random,
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    # 'Hosts': 'hm.baidu.com',
    'Referer': 'http://www.xicidaili.com/nn',
    'Connection': 'keep-alive'}

proxy = {'ip':'58.53.128.83', 'port': 3128}

url = 'http://ip.taobao.com/service/getIpInfo.php'
url2 = 'http://www.baidu.com'
url3 = 'http://pv.sohu.com/cityjson?ie=utf-8'

params = {'ip':proxy['ip']}

proxies = {
    "http": "http://{ip}:{port}".format(ip=proxy['ip'], port=proxy['port']),
    "https": "http://{ip}:{port}".format(ip=proxy['ip'], port=proxy['port']),
}

resp = requests.get(url, proxies=proxies, headers=headers, params=params, timeout=5).json()
print(resp['data'])
resp2 = requests.get(url2, proxies=proxies, headers=headers, timeout=5)
print(resp2.request.headers)
resp3 = requests.get(url3, proxies=proxies, headers=headers, timeout=5)
print(resp3.text)
