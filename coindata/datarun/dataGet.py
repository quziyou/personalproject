import ccxt
import pymysql
import pandas as pd
import time, threading
from sqlalchemy import create_engine

def bitfinexData():
    bitfinex = ccxt.bitfinex()
    coindata = list(bitfinex.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'bitfinex'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def bittrexData():
    bittrex = ccxt.bittrex()
    coindata = list(bittrex.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'bittrex'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def okexData():
    okex = ccxt.okex()
    coindata = list(okex.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'okex'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def bitstampData():
    bitstamp = ccxt.bitstamp()
    coindata = list(bitstamp.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'bitstamp'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def hitbtcData():
    hitbtc = ccxt.hitbtc()
    coindata = list(hitbtc.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'hitbtc'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def huobiData():
    huobi = ccxt.huobi()
    coindata = list(huobi.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'huobi'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def btcchinaData():
    btcchina = ccxt.btcchina()
    coindata = list(btcchina.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'btcchina'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def cryptopiaData():
    cryptopia = ccxt.cryptopia()
    coindata = list(cryptopia.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'cryptopia'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def gateioData():
    gateio = ccxt.gateio()
    coindata = list(gateio.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'gateio'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


def poloniexData():
    poloniex = ccxt.poloniex()
    coindata = list(poloniex.fetch_tickers().values())

    columns = ['ask', 'bid', 'close', 'high', 'low', 'last', 'symbol', 'average', 'baseVolume', 'timestamp']
    df = pd.DataFrame(coindata)
    df = df[columns]
    df['exchange'] = 'poloniex'
    df['createtime'] = starttime
    df['baseCurrency'] = list(i.split('/')[0] for i in df['symbol'])
    df['quotCurrency'] = list(i.split('/')[1] for i in df['symbol'])

    engine = create_engine("mysql+pymysql://quziyou:0739#KunMing@47.94.240.32:5389/coinData?charset=utf8")
    df.to_sql('coindata_tickers', con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    while True:
        starttime = time.time()
        t1 = threading.Thread(target=bitfinexData, name='bitfinex')
        t2 = threading.Thread(target=bittrexData, name='bittrex')
        t3 = threading.Thread(target=okexData, name='okex')
        t4 = threading.Thread(target=hitbtcData, name='hitbtc')
        t5 = threading.Thread(target=cryptopiaData, name='cryptopia')
        t6= threading.Thread(target=gateioData, name='gateio')
        t7 = threading.Thread(target=poloniexData, name='poloniex')
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        time.sleep(20)