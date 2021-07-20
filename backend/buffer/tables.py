from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    _table_args__ = {"schema": "dbo"}  # не обязательно
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    pswd = Column(String)
    email = Column(String, unique=True)
