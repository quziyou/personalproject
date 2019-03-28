#!/usr/bin/python3

import time
import pymysql
import requests
import pandas as pd
from sqlalchemy import create_engine


def clearData():

	db = pymysql.connect(host='111.231.196.51', user='coin', password='coin', db='coindata', port = 3306)
	cur = db.cursor()
	sql = 'TRUNCATE coindata_rate'

	try:
		cur.execute(sql)
		results = cur.fetchall()

	except Exception as e:
		raise e
	finally:
		db.commit()
		db.close()


def getRate():
	url_rate = 'http://api.k780.com'
	currencies = ['USD','EUR','HKD','JPY','TWD']
	basecurrency = []
	updatetime = []
	createtime = time.time()
	rate = []
	df = pd.DataFrame()
	for cc in currencies:
		params = {
		  'app' : 'finance.rate',
		  'scur' : cc,
		  'tcur' : 'CNY',
		  'appkey' : '33553',
		  'sign' : 'eebdf6be20219c72a9f751b71fc14ab9',
		  'format' : 'json'}
		res = dict(requests.get(url_rate,params).json())

		if res['success'] == 0:
		    print('汇率获取失败！')
		else:
		    basecurrency.append(cc) 
		    rate.append(float(res['result']['rate']))
		    updatetime.append(res['result']['update'])
	df['basecurrency'] = basecurrency
	df['quotcurrency'] = 'CNY'
	df['rate'] = rate
	df['updatetime'] = updatetime
	df['createtime'] = createtime
	engine = create_engine("mysql+pymysql://coin:coin@111.231.196.51:3306/coindata?charset=utf8")
	df.to_sql('coindata_rate', con=engine, if_exists='append', index=False)


if __name__ == '__main__':
	clearData()
	getRate()