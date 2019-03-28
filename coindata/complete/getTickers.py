#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import ccxt
import pymysql
import pandas as pd
import time, threading
from sqlalchemy import create_engine


def okexData():
    betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        okex = ccxt.okex()
        coindata = list(okex.fetch_tickers().values())
        columns = ['symbol', 'ask', 'bid', 'close', 'last', 'high', 'low', 'info', 'datetime']
        df = pd.DataFrame(coindata)
        df = df[columns]
        df['vol'] = [i['vol'] for i in df['info']]
        df['exchange'] = 'okex'
        df = df.drop(['info'], axis=1)
        df['datetime'] = [i.replace('T', ' ') for i in df['datetime']]
        df['datetime'] = [i.replace('Z', '') for i in df['datetime']]
        df['basecurrency'] = list(i.split('/')[0] for i in df['symbol'])
        df['quotcurrency'] = list(i.split('/')[1] for i in df['symbol'])
        df['createtime'] = starttime
        df['codeid'] = 2
        try:
            engine = create_engine("mysql+pymysql://coin:DaTa_beau@47.99.45.184:3306/coindata?charset=utf8")
            df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)
        except:
            with open('coindataerr.log','a') as f:
                f.write('%s：okex数据入库失败！\n' % betime)
                pass
    except:
        with open('coindataerr.log','a') as f:
            f.write('%s：okex数据获取失败！\n' % betime)
        pass


def binanceData():
    betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        binance = ccxt.binance()
        coindata = list(binance.fetch_tickers().values())
        columns = ['symbol', 'ask', 'bid', 'close', 'last', 'high', 'low', 'info', 'datetime']
        df = pd.DataFrame(coindata)
        df = df[columns]
        df['vol'] = [i['volume'] for i in df['info']]
        df['exchange'] = 'binance'
        df = df.drop(['info'], axis=1)
        df['datetime'] = [i.replace('T', ' ') for i in df['datetime']]
        df['datetime'] = [i.replace('Z', '') for i in df['datetime']]
        df['basecurrency'] = list(i.split('/')[0] for i in df['symbol'])
        df['quotcurrency'] = list(i.split('/')[1] for i in df['symbol'])
        df['createtime'] = starttime
        df['codeid'] = 2
        try:
            engine = create_engine("mysql+pymysql://coin:DaTa_beau@47.99.45.184:3306/coindata?charset=utf8")
            df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)
        except:
            with open('coindataerr.log','a') as f:
                f.write('%s：binance数据入库失败！\n' % betime)
                pass
    except:
        with open('coindataerr.log','a') as f:
            f.write('%s：binance数据获取失败！\n' % betime)
        pass


def bitfinexData():
    betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        bitfinex = ccxt.bitfinex()
        coindata = list(bitfinex.fetch_tickers().values())
        columns = ['symbol', 'ask', 'bid', 'close', 'last', 'high', 'low', 'info', 'datetime']
        df = pd.DataFrame(coindata)
        df = df[columns]
        df['exchange'] = 'bitfinex'
        df['vol'] = [i['volume'] for i in df['info']]
        df['datetime'] = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i))) for i in [x['timestamp'] for x in df['info']]]
        df = df.drop(['info'], axis=1)
        df['basecurrency'] = list(i.split('/')[0] for i in df['symbol'])
        df['quotcurrency'] = list(i.split('/')[1] for i in df['symbol'])
        df['createtime'] = starttime
        df['codeid'] = 2
        try:
            engine = create_engine("mysql+pymysql://coin:DaTa_beau@47.99.45.184:3306/coindata?charset=utf8")
            df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)
        except:
            with open('coindataerr.log','a') as f:
                f.write('%s：bitfinex数据入库失败！\n' % betime)
                pass
    except:
        with open('coindataerr.log','a') as f:
            f.write('%s：bitfinex数据获取失败！\n' % betime)
        pass


def bittrexData():
    betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        bittrex = ccxt.bittrex()
        coindata = list(bittrex.fetch_tickers().values())
        columns = ['symbol', 'ask', 'bid', 'close', 'last', 'high', 'low', 'info', 'datetime']
        df = pd.DataFrame(coindata)
        df = df[columns]
        df['exchange'] = 'bittrex'
        df['vol'] = [i['Volume'] for i in df['info']]
        df['datetime'] = [i.replace('T', ' ') for i in df['datetime']]
        df['datetime'] = [i.replace('Z', '') for i in df['datetime']]
        df = df.drop(['info'], axis=1)
        df['basecurrency'] = list(i.split('/')[0] for i in df['symbol'])
        df['quotcurrency'] = list(i.split('/')[1] for i in df['symbol'])
        df['createtime'] = starttime
        df['codeid'] = 2
        try:
            engine = create_engine("mysql+pymysql://coin:DaTa_beau@47.99.45.184:3306/coindata?charset=utf8")
            df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)
        except:
            with open('coindataerr.log','a') as f:
                f.write('%s：bittrex数据入库失败！\n' % betime)
                pass
    except:
        with open('coindataerr.log','a') as f:
            f.write('%s：bittrex数据获取失败！\n' % betime)
        pass


def gateioData():
    betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        gateio = ccxt.gateio()
        coindata = list(gateio.fetch_tickers().values())
        columns = ['symbol', 'ask', 'bid', 'close', 'last', 'high', 'low', 'info', 'datetime']
        df = pd.DataFrame(coindata)
        df = df[columns]
        df['exchange'] = 'gateio'
        df['vol'] = [i['baseVolume'] for i in df['info']]
        df['datetime'] = [i.replace('T', ' ') for i in df['datetime']]
        df['datetime'] = [i.replace('Z', '') for i in df['datetime']]
        df = df.drop(['info'], axis=1)
        df['basecurrency'] = list(i.split('/')[0] for i in df['symbol'])
        df['quotcurrency'] = list(i.split('/')[1] for i in df['symbol'])
        df['createtime'] = starttime
        df['codeid'] = 2
        try:
            engine = create_engine("mysql+pymysql://coin:DaTa_beau@47.99.45.184:3306/coindata?charset=utf8")
            df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)
        except:
            with open('coindataerr.log','a') as f:
                f.write('%s：gateio数据入库失败！\n' % betime)
                pass
    except:
        with open('coindataerr.log','a') as f:
            f.write('%s：gateio数据获取失败！\n' % betime)
        pass


def hitbtcData():
    betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        hitbtc = ccxt.hitbtc()
        coindata = list(hitbtc.fetch_tickers().values())
        columns = ['symbol', 'ask', 'bid', 'close', 'last', 'high', 'low', 'info', 'datetime']
        df = pd.DataFrame(coindata)
        df = df[columns]
        df['exchange'] = 'hitbtc'
        df['vol'] = [i['volume'] for i in df['info']]
        df['datetime'] = [i.replace('T', ' ') for i in df['datetime']]
        df['datetime'] = [i.replace('Z', '') for i in df['datetime']]
        df = df.drop(['info'], axis=1)
        df['basecurrency'] = list(i.split('/')[0] for i in df['symbol'])
        df['quotcurrency'] = list(i.split('/')[1] for i in df['symbol'])
        df['createtime'] = starttime
        df['codeid'] = 2
        try:
            engine = create_engine("mysql+pymysql://coin:DaTa_beau@47.99.45.184:3306/coindata?charset=utf8")
            df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)
        except:
            with open('coindataerr.log','a') as f:
                f.write('%s：hitbtc数据入库失败！\n' % betime)
                pass
    except:
        with open('coindataerr.log','a') as f:
            f.write('%s：hitbtc数据获取失败！\n' % betime)
        pass


def poloniexData():
    betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        poloniex = ccxt.poloniex()
        coindata = list(poloniex.fetch_tickers().values())
        columns = ['symbol', 'ask', 'bid', 'close', 'last', 'high', 'low', 'info', 'datetime']
        df = pd.DataFrame(coindata)
        df = df[columns]
        df['exchange'] = 'poloniex'
        df['vol'] = [i['baseVolume'] for i in df['info']]
        df['datetime'] = [i.replace('T', ' ') for i in df['datetime']]
        df['datetime'] = [i.replace('Z', '') for i in df['datetime']]
        df = df.drop(['info'], axis=1)
        df['basecurrency'] = list(i.split('/')[0] for i in df['symbol'])
        df['quotcurrency'] = list(i.split('/')[1] for i in df['symbol'])
        df['createtime'] = starttime
        df['codeid'] = 2
        try:
            engine = create_engine("mysql+pymysql://coin:DaTa_beau@47.99.45.184:3306/coindata?charset=utf8")
            df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)
        except:
            with open('coindataerr.log','a') as f:
                f.write('%s：poloniex数据入库失败！\n' % betime)
                pass
    except:
        with open('coindataerr.log','a') as f:
            f.write('%s：poloniex数据获取失败！\n' % betime)
        pass



def ethfinexData():
    betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    try:
        ethfinex = ccxt.ethfinex()
        coindata = list(ethfinex.fetch_tickers().values())
        columns = ['symbol', 'ask', 'bid', 'close', 'last', 'high', 'low', 'info', 'datetime']
        df = pd.DataFrame(coindata)
        df = df[columns]
        df['exchange'] = 'ethfinex'
        df['vol'] = [i['volume'] for i in df['info']]
        df['datetime'] = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i))) for i in [x['timestamp'] for x in df['info']]]
        df = df.drop(['info'], axis=1)
        df['basecurrency'] = list(i.split('/')[0] for i in df['symbol'])
        df['quotcurrency'] = list(i.split('/')[1] for i in df['symbol'])
        df['createtime'] = starttime
        df['codeid'] = 2
        try:
            engine = create_engine("mysql+pymysql://coin:DaTa_beau@47.99.45.184:3306/coindata?charset=utf8")
            df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)
        except:
            with open('coindataerr.log','a') as f:
                f.write('%s：ethfinex数据入库失败！\n' % betime)
                pass
    except:
        with open('coindataerr.log','a') as f:
            f.write('%s：ethfinex数据获取失败！\n' % betime)
        pass


if __name__ == '__main__':
    while True:
        betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            db = pymysql.connect("47.99.45.184", "coin", "DaTa_beau", "coindata")
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM coindata_tickers")
            data = cursor.fetchone()
        except:
            with open('coindataerr.log', 'a') as f:
                f.write('%s：数据库连接失败！\n' % betime)

        if data[0] != 0:
            starttime = time.time()
            t1 = threading.Thread(target=okexData, name='okex')
            t2 = threading.Thread(target=binanceData, name='binance')
            t3 = threading.Thread(target=bitfinexData, name='bitfinex')
            t4 = threading.Thread(target=bittrexData, name='bittrex')
            t5 = threading.Thread(target=gateioData, name='gateio')
            t6 = threading.Thread(target=hitbtcData, name='hitbtc')
            t7 = threading.Thread(target=poloniexData, name='poloniex')
            t8 = threading.Thread(target=ethfinexData, name='ethfinex')
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()
            t6.start()
            t7.start()
            t8.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
            t6.join()
            t7.join()
            t8.join()
        else:
            betime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            starttime = time.time()
            t1 = threading.Thread(target=okexData, name='okex')
            t2 = threading.Thread(target=binanceData, name='binance')
            t3 = threading.Thread(target=bitfinexData, name='bitfinex')
            t4 = threading.Thread(target=bittrexData, name='bittrex')
            t5 = threading.Thread(target=gateioData, name='gateio')
            t6 = threading.Thread(target=hitbtcData, name='hitbtc')
            t7 = threading.Thread(target=poloniexData, name='poloniex')
            t8 = threading.Thread(target=ethfinexData, name='ethfinex')
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()
            t6.start()
            t7.start()
            t8.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            t5.join()
            t6.join()
            t7.join()
            t8.join()
        
        cursor.execute("UPDATE coindata_tickers SET codeid = 0 WHERE codeid = 1")
        cursor.execute("UPDATE coindata_tickers SET codeid = 1 WHERE codeid = 2")
        db.commit()
        cursor.close()
        db.close()
        time.sleep(15)
