from aiogram.types.base import Boolean
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, primary_key=True)

    nickname = Column(String)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    email = Column(String)

    city = Column(String)
    school = Column(String)
    grade = Column(Integer)
