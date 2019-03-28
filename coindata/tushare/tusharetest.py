import pandas as pd
import tushare as ts


ts.set_token('63cb7eb3f64f6383d4460d70e37a63908e067aa3375e1336d8967b38')
pro = ts.pro_api()

df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='15min', start_date='20180905', end_date='20180907')

print(df.columns)