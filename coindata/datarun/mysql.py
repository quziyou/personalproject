import pymysql
import pandas as pd

db = pymysql.connect(host='localhost', user='root', password='0871@YeJia', db='coinData', port = 3306)

cur = db.cursor()

sql1 = 'select * from coindata_tickers'
sql2 = 'desc coindata_tickers'

try:
	cur.execute(sql1)
	results1 = cur.fetchall()
	dataframe = []
	for row in results1:
		dataframe.append(list(row))
	cur.execute(sql2)
	results2 = cur.fetchall()
	df = pd.DataFrame(dataframe,columns=list(i[0] for i in results2))
	print(df.head())

except Exception as e:
	raise e

finally:
	db.close()



