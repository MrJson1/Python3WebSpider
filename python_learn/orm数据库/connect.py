from sqlalchemy import create_engine

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'root'
PASSWORD = 'qwe123'

Db_Uri = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    DATABASE,
)

engine = create_engine(Db_Uri)

#创建一个基类
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)

#创建会话
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()

if __name__=="__main__":
    conection = engine.connect()
    result = conection.execute('select 1')
    print(result.fetchone())

