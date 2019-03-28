import pymysql
import pandas as pd

db = pymysql.connect(host='localhost', user='root', password='0871@YeJia', db='coinData', port = 3306)

cur = db.cursor()

sql = 'select * from coindata_tickers'

try:
	cur.execute(sql)
	results = cur.fetchall()

except Exception as e:
	raise e

finally:
	db.close()

exchange = list(i[10] for i in results)
symbol = list(i[6] for i in results)
baseCurrency = list(i[11] for i in results)
quotCurrency = list(i[12] for i in results)
last = list(i[5] for i in results)

data = {}

for bc in list(set(i[11] for i in results)):
	data[bc] = {}
	for num in range(len(last)):
		if symbol[num].split('/')[0] == bc:
			data[bc][exchange[num]] = dict(zip([quotCurrency[num]],[last[num]]))
	

print(data['OMG'])