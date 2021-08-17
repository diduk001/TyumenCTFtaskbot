from models import *
from config import Config

# SQLAlchemy INIT

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(Config.DATABASE_URI)
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property()


Base.metadata.create_all(bind=engine)
