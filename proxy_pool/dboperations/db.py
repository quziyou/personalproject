from sqlalchemy import create_engine, Integer, Column, DateTime, Numeric, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_Config
import datetime


BaseModel = declarative_base()  # 基类

# 操作的基类：ip，port(端口)，types类型(0高匿，1透明)，protocol(0 http,1 https http)，country(国家)，region(省份)，city(城市)，updatetime(更新时间)，speed(连接速度)


class Proxy(BaseModel):
    __tablename__ = 'real_proxys'

    ip = Column(VARCHAR(16), nullable=False, primary_key=True)
    port = Column(Integer, nullable=False, primary_key=True)
    types = Column(VARCHAR(16), nullable=False)
    protocol = Column(VARCHAR(16), nullable=False, default=0)
    country = Column(VARCHAR(50), nullable=False)
    region = Column(VARCHAR(50), nullable=True)
    city = Column(VARCHAR(50), nullable=True)
    isp = Column(VARCHAR(50), nullable=True)
    updatetime = Column(DateTime(), default=datetime.datetime.now)
    speed = Column(Numeric(5, 2), nullable=False)


class SqlDefault(object):
    params = {'ip': None, 'port': None, 'types': None, 'protocol': None, 'country': None, 'region': None, 'city': None, 'isp': None, 'speed': None}

    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def insert(self, value=None):
        raise NotImplemented

    def delete(self, conditions=None):
        raise NotImplemented

    def update(self, conditions=None, value=None):
        raise NotImplemented

    def select(self, count=None, conditions=None):
        raise NotImplemented


class DbOperation(SqlDefault):
    params = {'ip': Proxy.ip, 'port': Proxy.port, 'types': Proxy.types, 'protocol': Proxy.protocol,
              'country': Proxy.country, 'region': Proxy.region, 'city': Proxy.city,  'isp': Proxy.isp, 'speed': Proxy.speed}

    def __init__(self):
        # 设置连接池
        self.engine = create_engine(DB_Config['db_params'], max_overflow=5,
                                    pool_size=5, pool_timeout=30,
                                    pool_recycle=360, echo=False)
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)
        self.session.close()

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)
        self.session.close()

    def insert(self, value=None):
        proxy = Proxy(ip=value['ip'], port=value['port'], types=value['types'], protocol=value['protocol'],
                      country=value['country'],
                      region=value['region'], city=value['city'], isp=value['isp'], speed=value['speed'])
        self.session.add(proxy)
        try:
            self.session.commit()
            self.session.close()
        except BaseException as e:
            print(e)
            self.session.rollback()
            self.session.close()

    def delete(self, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(Proxy)
            for condition in conditions:
                query = query.filter(condition)
            query.delete()
            try:
                self.session.commit()
                self.session.close()
            except BaseException as e:
                print(e)
                self.session.rollback()
                self.session.close()

    def update(self, conditions=None, value=None):
        if conditions and value:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(Proxy)
            for condition in conditions:
                query = query.filter(condition)
            updatevalue = {}
            for key in list(value.keys()):
                if self.params.get(key, None):
                    updatevalue[self.params.get(key, None)] = value.get(key)
            query.update(updatevalue)
            try:
                self.session.commit()
                self.session.close()
            except BaseException as e:
                print(e)
                self.session.rollback()
                self.session.close()

    def select(self, count=None, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
        else:
            conditions = []

        query = self.session.query(Proxy.ip, Proxy.port, Proxy.speed)
        if len(conditions) > 0 and count:
            for condition in conditions:
                query = query.filter(condition)
            return query.order_by(Proxy.speed, Proxy.updatetime.desc()).limit(count).all()
        elif count:
            return query.order_by(Proxy.speed, Proxy.updatetime.desc()).limit(count).all()
        elif len(conditions) > 0:
            for condition in conditions:
                query = query.filter(condition)
            return query.order_by(Proxy.speed, Proxy.updatetime.desc()).all()
        else:
            return query.order_by(Proxy.speed, Proxy.updatetime.desc()).all()

    def close(self):
        pass
