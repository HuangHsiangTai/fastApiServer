from sqlalchemy.orm import Session
from src.models.user import User

def create_user(db: Session, name: str, email: str)-> User:
    db_user = User(name=name, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session)-> list[User]:
    a = db.query(User).all()
    return db.query(User).all()