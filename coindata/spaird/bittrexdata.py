#!/usr/bin/env python  
#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
import pandas as pd
import pymysql
import requests
import json
import time

def get_data():
	data_url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}

	resp = requests.get(data_url,headers=headers,timeout=30).json()['result'] # 实现一次全盘数据抓取
	columns = [] 
	dataset = []
	baseCurrency = []
	quoteCurrency = []

	for x in list(resp[0].keys()):
		columns.append(x.lower()) # 数据表列名处理

	for i in resp:
	 	dataset.append(list(i.values())) # 数据表数值获取

	df = pd.DataFrame(dataset,columns=columns) #整合成数据表

	for i in df['marketname']:
		quoteCurrency.append(i[:i.find('-')].lower()) # 获取标价币

	for i in df['marketname']:
		baseCurrency.append(i[i.find('-')+1:].lower()) # 获取本币

	df['marketname'] = list(i.lower().replace('-','') for i in df['marketname'])
	df['updatetimes'] = list(i.replace('T',' ') for i in df['timestamp'])
	df = df.drop(['created','basevolume','openbuyorders','opensellorders','prevday','timestamp'],axis=1)
	df['quoteCurrency'] = quoteCurrency
	df['baseCurrency'] = baseCurrency
	df['exchange'] = 'bittrex'
	df.sort_index(axis = 0,ascending = True)
	return df

def insert_db(df):
	engine = create_engine("mysql+pymysql://quziyou:0739KunMing@localhost:8276/coindata?charset=utf8")
	df.to_sql('coindata_tickers',con=engine,if_exists='append',index=False)


if __name__ == '__main__':
	while True:
		try:
			start_time = time.strftime('%Y-%m-%d %X',time.localtime())
			df = get_data()
			try:
				start_time = time.strftime('%Y-%m-%d %X',time.localtime())
				insert_db(df)
			except:
				with open('/var/log/coindata/coindata_log.log','a') as f:
					f.write(str(start_time) +'：bittrex-数据库写入异常！\n')
		except:
			with open('/var/log/coindata/coindata_log.log','a') as f:
				f.write(str(start_time) +'：bittrex-网络请求超时，未能获取交易数据！\n')
		time.sleep(10)