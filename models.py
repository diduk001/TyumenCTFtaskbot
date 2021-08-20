from sqlalchemy import Column, Integer, String, Boolean

# from init import Base, session
from models import *
from config import Config

# SQLAlchemy INIT

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    chatId = Column(Integer, unique=True, primary_key=True)

    isAdmin = Column(Boolean, default=False)

    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    nickname = Column(String(50))
    age = Column(Integer)
    city = Column(String(50))
    school = Column(String(50))
    grade = Column(Integer)

    signUpStage = Column(Integer)

    def signUpUser(self):
        session.add(self)
        session.commit()

    def deleteUser(self):
        session.delete(self)
        session.commit()


def findUserChatID(chatId: int) -> User:
    found = session.query(User).filter(User.chatId == chatId)
    if found:
        return found.first()
    else:
        return None


Base.metadata.create_all(engine)
session.commit()
