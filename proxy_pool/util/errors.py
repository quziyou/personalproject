# coding:utf-8
import config


class TestUrlFail(Exception):
    def __str__(self):
        msg = "访问{test_ip}失败，请检查网络连接".format(test_ip=config.TEST_IP)
        return msg


class DBConnectFail(Exception):
    def __str__(self):
        msg = "使用DB_CONNECT_STRING:{}--连接数据库失败".format(config.DB_Config['db_params'])
        return msg
