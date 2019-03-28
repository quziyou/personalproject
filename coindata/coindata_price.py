import time
import requests
from pandas import DataFrame
from collections import OrderedDict
from sqlalchemy import create_engine


def getPrice():
    currId = []
    symbol = []
    price = []
    updated = []

    url = 'https://api.coinmarketcap.com/v2/ticker/?convert=CNY'

    res = requests.get(url).json()

    for id in res['data'].keys():
        currId.append(id)
        symbol.append(res['data'][id]['symbol'])
        price.append(res['data'][id]['quotes']['CNY']['price'])
        updated.append(res['data'][id]['last_updated'])

    priceDict = OrderedDict()

    priceDict['currId'] = currId
    priceDict['symbol'] = symbol
    priceDict['price'] = price
    priceDict['updated'] = updated

    df = DataFrame(priceDict)
    createtime = int(time.time())
    df['createtime'] = createtime

    print(df)


if __name__ == '__main__':
    getPrice()
