# DIALECT = 'mysql'
# DRIVER = 'pymysql'
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'db_demo1'
# USERNAME = 'root'
# PASSWORD = 'qwe123'
#
# SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}/{}?charset=utf8'.format(
#     DIALECT,DRIVER,
#     USERNAME,
#     PASSWORD,
#     HOSTNAME,
#     PORT,
#     DATABASE,
# )


HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'mydb'
USERNAME = 'root'
PASSWORD = 'qwe123'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    DATABASE,
)


SQLALCHEMY_TRACK_MODIFICATIONS = False


