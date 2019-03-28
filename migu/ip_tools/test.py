import requests

url = 'https://v15.51cto.com/?p=TElscHBlaUJ3ZktrY0VvVE4xUWJaOGI0aURPSnJnN0ozc1oreGdDcW5YS0l6a2xuTnh1aThSMGRTVitGdXNxSTR1REpoV1RaV1JPRUxPVUI4aElIMlE9PQ==&stime=1543757365&sKey=YTQxMzZmNTg1NjVjM2E1OTc0NTYwNTNmYzVlM2Q3NDY&flag=2&sname=loco_video_219000_38.ts'

resp = requests.get(url)

with open('/home/quziyou/test.flv', 'wb') as f:
    f.write(resp.content)
