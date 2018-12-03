from email_V1.connect import Base,session
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref


class companySalary(Base):
    __tablename__ = 'companySalary2'
    companySalary_id = Column(Integer, primary_key=True, autoincrement=True)
    companySalary_overview_url = Column(String(500))
    salaries = Column(String(10000),nullable=False)
    companyinfo_id = Column(Integer,ForeignKey('companyinfo.companyinfo_id'),nullable=True)

    # __table_arhs__ = {
    #     'mysql_engine': 'InnoDb'
    # }


class companylocation(Base):
    __tablename__ = 'companylocation2'
    companylocation_id = Column(Integer,primary_key=True,autoincrement=True)
    companyIocation_sum = Column(String(10000),nullable=True)
    companylocation_overview_url = Column(String(500), nullable=False)
    companyinfo_id = Column(Integer,ForeignKey('companyinfo.companyinfo_id'),nullable=True,autoincrement=True)

    # __table_arhs__ = {
    #     'mysql_engine': 'InnoDb'
    # }


class companyinfo(Base):
    __tablename__ = 'companyinfo'
    companyinfo_id = Column(Integer, primary_key=True, autoincrement=True)
    companyinfo_overview_url = Column(String(500), nullable=False)
    companyName = Column(String(1000),nullable=True)
    Website = Column(String(5000),nullable=True)
    Headquarters = Column(String(500))
    size = Column(String(50))
    Founded = Column(String(500))
    Type = Column(String(50))
    Industry = Column(String(500))
    Revenue = Column(String(500))
    Competitors = Column(String(500))
    rate = Column(String(50))
    companylocation = relationship('companylocation', backref='companyinfo')
    companySalary = relationship('companySalary', backref='companyinfo')

    # __table_arhs__ = {
    #     'mysql_engine': 'InnoDb'
    # }

class email_info(Base):
    __tablename__ = 'email_info'
    request_id = Column(String(100),primary_key=True)
    email = Column(String(50))
    status_code = Column(String(10),nullable=False)

    # __table_arhs__ = {
    #     'mysql_engine': 'InnoDb'
    # }

if __name__ =="__main__":
    #执行此代码，就会把创建好的 Module 映射到数据库中
    Base.metadata.create_all()
