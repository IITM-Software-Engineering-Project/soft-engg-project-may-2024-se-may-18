from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from database.db_sql import init_db

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)
    last_login = Column(DateTime, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)



class Content(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    week_no=Column(Integer, nullable=False)
    link = Column(String(50), nullable=False)



engine = None

if not engine:
    engine = init_db()
    Base.metadata.create_all(engine, checkfirst=True)
    session = sessionmaker(bind=engine)
    print("SQL Database connected Successfully.")
