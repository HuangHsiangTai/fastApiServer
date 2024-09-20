from sqlalchemy.orm import Session
from ..models import user

def get_users(db: Session):
    return db.query(user.User).all()