import json
import requests
from fake_useragent import UserAgent


ua = UserAgent(use_cache_server=False)

headers = {
    'User-Agent': ua.random,
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Hosts': 'hm.baidu.com',
    'Referer': 'http://www.xicidaili.com/nn',
    'Content-Type': 'application/dict',
    'Connection': 'keep-alive'}

url = 'http://115.29.196.86:9002/api/Tone/InsertNumber'


data= {
    "Number": "333",
    "Provience": "44",
    "OpenUrl": "www.qq.com"
}


resp = requests.post(url, data=json.dumps(data), headers=headers).json()
print(resp)
