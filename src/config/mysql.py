from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# get environmental varialbe
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_NAME = os.getenv("MYSQL_DATABASE")

# for ORM model
Base = declarative_base()
# MySQL URL     
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
print(f'DATABASE_URL=${SQLALCHEMY_DATABASE_URL}')
engine = create_engine(SQLALCHEMY_DATABASE_URL)

class MySqlClient:
    def __init__(self):   
        db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = db_session()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
# get db
def get_db():
   with MySqlClient() as db:
        yield db