#!/usr/bin/python3

import time
import pymysql
import requests
from pandas import DataFrame
from collections import OrderedDict
from sqlalchemy import create_engine


def clearData():

	db = pymysql.connect(host='111.231.196.51', user='coin', password='coin', db='coindata', port = 3306)

	cur = db.cursor()

	sql = 'TRUNCATE coindata_currencyinfo'

	try:
		cur.execute(sql)
		results = cur.fetchall()

	except Exception as e:
		raise e

	finally:
		db.commit()
		db.close()


def getInfo():
	list_url = 'https://api.coinmarketcap.com/v2/listings/'
	currcencyId = []
	symbol = []
	coinName = []
	webSite_slug = []

	listData =requests.get(list_url).json()

	for row in listData['data']:
		currcencyId.append(row['id'])
		symbol.append(row['symbol'])
		coinName.append(row['name'])
		webSite_slug.append(row['website_slug'])

	currcencyInfo = OrderedDict()

	currcencyInfo['curr_id'] = currcencyId
	currcencyInfo['symbol'] = symbol
	currcencyInfo['coinname'] = coinName
	currcencyInfo['website_slug'] = webSite_slug
	currcencyInfo['createtime'] = time.time()

	df = DataFrame(currcencyInfo)

	engine = create_engine("mysql+pymysql://coin:coin@111.231.196.51:3306/coindata?charset=utf8")
	df.to_sql('coindata_currencyinfo', con=engine, if_exists='append', index=False)


if __name__ == '__main__':
	clearData()
	getInfo()