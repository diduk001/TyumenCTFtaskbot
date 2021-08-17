from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKeyConstraint
from init import Base, session


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(Integer, unique=True, primary_key=True)

    is_admin = Column(Boolean, default=False)

    nickname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    age = Column(Integer)
    email = Column(String(50), nullable=False)

    city = Column(String(50), nullable=False)
    school = Column(String(50), nullable=False)
    grade = Column(Integer)


def registerUser(user: User):
    session.add(user)
    session.commit()
