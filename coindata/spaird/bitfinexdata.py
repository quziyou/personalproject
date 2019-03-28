#!/usr/bin/env python  
#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import requests
import json
import time

def get_data():
	pair_url = 'https://api.bitfinex.com/v1/symbols_details' # 交易对链接
	data_url = 'https://api.bitfinex.com/v2/tickers?symbols=' # 交易数据链接
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
	resp = requests.get(pair_url,headers=headers,timeout=30).json() # 获取交易对
	pairs = []
	for i in resp:
		pairs.append('t'+dict(i)['pair'].upper()) # 交易对数据清洗
	symbols = ','.join(pairs)
	columns=['marketname','bid','bid_size','ask','ask_size','daily_change','daily_change_perc','last','volume','high','low']

	start_time = time.strftime('%Y-%m-%d %X',time.localtime()) # 生成时间戳
	tickersData = requests.get(data_url+symbols,headers=headers,timeout=30).json() # 获取交易数据

	# 转换数据结构

	df = pd.DataFrame(tickersData,columns=columns) 
	df['marketname'] = list(i.replace('t','').lower() for i in df['marketname'])
	baseCurrency = []
	quoteCurrency = []

	for i in df['marketname']:
		if i[-4:] == 'usdt':
			quoteCurrency.append(i[-4:])
			baseCurrency.append(i[:len(i)-4])
		else:
			quoteCurrency.append(i[-3:])
			baseCurrency.append(i[:len(i)-3])
	df['baseCurrency'] = baseCurrency
	df['quoteCurrency'] = quoteCurrency
	df['exchange'] = 'bitfinex'
	df['updatetimes'] = start_time
	df = df.drop(['bid_size','ask_size','daily_change','daily_change_perc'],axis=1)
	return df


def insert_db(df):
	engine = create_engine("mysql+pymysql://quziyou:0739KunMing@47.94.240.32:8276/coindata?charset=utf8")
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