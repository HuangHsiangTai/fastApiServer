from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Callable , Generator
from contextlib import contextmanager, AbstractContextManager
from src.utils.logger import log_info,log_error
import os
# get environmental varialbe
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_NAME = os.getenv("MYSQL_DATABASE")

# for ORM model
Base = declarative_base()

class MySqlClient:
    def __init__(self, user: str, password:str, database:str, host:str) -> None:
        mysql_url= f"mysql+pymysql://{user}:{password}@{host}/{database}"
        log_info(f"initialize {__name__}",extra={mysql_url:mysql_url})
        self._engine = create_engine(mysql_url)
        self._session_facctory = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)
    @contextmanager
    def session(self) -> Generator[Callable[..., AbstractContextManager[Session]], None, None]:
        session: Session = self._session_facctory()
        try:
            yield session 
        except Exception:
            log_error("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()  