# coding:utf-8
import sys
from config import DB_Config
from util.errors import DBConnectFail


try:
    if DB_Config['db_type'] == 'sqlalchemy':
        from dboperations.db import DbOperation as DbOperation
        sql_operation = DbOperation()
        sql_operation.init_db()
    else:
        print('抱歉，暂不支持该类型数据库！')
except Exception as e:
    raise DBConnectFail


def store_data(queue2, db_proxy_num):
    successNum = 0
    failNum = 0
    while True:
        try:
            proxy = queue2.get(timeout=300)
            if proxy:

                sqlhelper.insert(proxy)
                successNum += 1
            else:
                failNum += 1
            str = 'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (successNum, failNum)
            sys.stdout.write(str + "\r")
            sys.stdout.flush()
        except BaseException as e:
            if db_proxy_num.value != 0:
                successNum += db_proxy_num.value
                db_proxy_num.value = 0
                str = 'IPProxyPool----->>>>>>>>Success ip num :%d,Fail ip num:%d' % (successNum, failNum)
                sys.stdout.write(str + "\r")
                sys.stdout.flush()
                successNum = 0
                failNum = 0


