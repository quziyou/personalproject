#!/usr/bin/env python  
#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
import pandas as pd
import pymysql
import requests
import json
import time


	# 生成交易对信息字典

def get_symbols():
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}

    symbol = []
    quoteCurrency = []
    baseCurrency = []

    symbol_url = 'https://api.hitbtc.com/api/2/public/symbol'
    symbols = requests.get(symbol_url,headers=headers,timeout=20).json() # 获取交易对详情

    for i in symbols: # 截取并处理交易对本币、标价币信息
    	symbol.append(i['id'].lower())
    	quoteCurrency.append(i['quoteCurrency'].lower())
    	baseCurrency.append(i['baseCurrency'].lower())

    symbol_quoteCurrency = dict(zip(symbol,quoteCurrency)) # 生成交易对-标价币字典
    symbol_baseCurrency = dict(zip(symbol,baseCurrency)) # 生成交易对-本币字典

    return symbol_baseCurrency,symbol_quoteCurrency


	# 获取交易数据，清洗并整合成预期数据结构

def get_data(symbol_baseCurrency,symbol_quoteCurrency):
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
	data_url = 'https://api.hitbtc.com/api/2/public/ticker' # hitbtc交易所api接口
	datas = requests.get(data_url,headers=headers,timeout=30).json() # 获取ticker数据
	dataset = []
	df_quoteCurrency = []
	df_baseCurrency = []
	columns = ['ask','bid','last','open','low','high','volume','volumequote','updatetimes','marketname']

	for i in datas:
		dataset.append(list(dict(i).values()))

	df = pd.DataFrame(dataset,columns=columns)
	df = df.drop(['open','volumequote'],axis=1) # 删除多余列
	df['updatetimes'] = list(i.replace('T',' ').replace('Z','') for i in df['updatetimes'])
	df['marketname'] = list(i.lower() for i in df['marketname'])

	for x in df['marketname']:
		df_quoteCurrency.append(symbol_quoteCurrency[x])
		df_baseCurrency.append(symbol_baseCurrency[x])

	df['baseCurrency'] = df_baseCurrency # 生成本币名称列
	df['quoteCurrency'] = df_quoteCurrency # 生成标价币名称列
	df['exchange'] = 'hitbtc' # 生成交易所名称列
	return df


def inser_db(df):
	engine = create_engine("mysql+pymysql://zhuoshuijun:0739KunMing@47.94.240.32:8276/coindata?charset=utf8")
	df.to_sql('coindata_tickers',con=engine,if_exists='append',index=False)

if __name__ == '__main__':
	while True:
		try:
			start_time = time.strftime('%Y-%m-%d %X',time.localtime())
			symbol_baseCurrency,symbol_quoteCurrency = get_symbols()
			try:
				start_time = time.strftime('%Y-%m-%d %X',time.localtime())
				df = get_data(symbol_baseCurrency,symbol_quoteCurrency)
				try:
					inser_db(df)
				except:
					with open('/var/log/coindata/coindata_log.log','a') as f:
						f.write(str(start_time) +'：hitbtc-数据库写入异常！\n')
			except:
				with open('/var/log/coindata/coindata_log.log','a') as f:
					f.write(str(start_time) +'：hitbtc-网络请求超时，未能获取交易数据！\n')
		except:
			with open('/var/log/coindata/coindata_log.log','a') as f:
				f.write(str(start_time) +'：hitbtc-网络请求超时，未能获取交易对信息！\n')
		time.sleep(10)
