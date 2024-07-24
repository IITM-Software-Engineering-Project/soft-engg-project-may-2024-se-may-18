from sqlalchemy import Column, Integer, String, Timestamp
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

db = declarative_base()


class User(db):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    last_login = Column(Timestamp, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
