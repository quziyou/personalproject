import pymysql
import time



def queryData():


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
	return results


def dataDict(results):

	exchange = list(i[10] for i in results)
	symbol = list(i[6] for i in results)
	baseCurrency = list(i[11] for i in results)
	quotCurrency = list(i[12] for i in results)
	last = list(i[5] for i in results)

	dataDict = {}

	for bc in list(set(i[11] for i in results)):
		dataDict[bc] = {}
		for num in range(len(last)):
			if symbol[num].split('/')[0] == bc:
				dataDict[bc][exchange[num]] = dict(zip([quotCurrency[num]],[last[num]]))
	return dataDict



if __name__ == '__main__':
	starttime = time.time()
	queryData = queryData()
	dataDict = dataDict(queryData)
	endtime = time.time()
	time = endtime - starttime
	print(list(set(i[12] for i in queryData)))
	print('程序用时：%.02f 秒' % time)