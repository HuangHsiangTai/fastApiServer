from sqlalchemy.orm import Session
from ..models import user

def create_user(db: Session, name: str, email: str):
    db_user = user.User(name=name, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user