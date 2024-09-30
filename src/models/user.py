from sqlalchemy import Column, Integer, String
from config.mysql import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"