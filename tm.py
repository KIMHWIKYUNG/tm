#-*-coding:utf-8-*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, SmallInteger, Unicode, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import json

Base = declarative_base()


class Time(Base): #조직
  __tablename__ = 'time'
  timeCode = Column(String(4), primary_key=True)
  behavior = Column(String(50))
  eTime = Column(DateTime)


engine = create_engine("mysql://root:1127@52.192.89.97/timeManagement", encoding='utf8', echo=True)
Base.metadata.create_all(engine)
