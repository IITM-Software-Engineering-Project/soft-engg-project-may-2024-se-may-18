from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()


def init_db():
    db_uri = os.getenv('DATABASE_URL').replace(
        "postgresql://", "cockroachdb://")
    try:
        create_engine(db_uri)
        print("Connected to Cockroach DB.")
    except Exception as e:
        print("Failed to connect to database.")
        print(f"{e}")
