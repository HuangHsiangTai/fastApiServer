from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from typing import Callable, Iterator, List
from src.models.user import User
from src.utils.logger import log_info,log_error

class UserRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        log_info(f"initialize {__name__}")
        self._session_factory = session_factory
    def create_user(self, name: str, email: str)-> User:
        with self._session_factory() as session:
            user = User(name=name, email=email)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        
    def get_user(self)-> List[User]:
        with self._session_factory() as session:
            return session.query(User).all()