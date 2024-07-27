from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()


def init_db():
    try:
        print("Connecting to SQL database.")
        engine = create_engine(os.getenv('DATABASE_SQL_URL'))
        return engine
    except Exception as e:
        print("Failed to connect to database.")
        print(f"{e}")
