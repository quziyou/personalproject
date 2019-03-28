import requests

url = 'https://api.coinmarketcap.com/v2/ticker/?convert=USD'

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
resp = requests.get(url,headers=headers,timeout=30).json()
print(resp)