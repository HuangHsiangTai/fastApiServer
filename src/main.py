from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
mysql_user = os.getenv("MYSQL_USER")
from crud.create_user import create_user as createU
from crud.get_user import get_users as getU
from utils.mysql import  Base, engine,SessionLocal
from utils.logger import LoggingMiddleware, log_info




# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(LoggingMiddleware)
# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str
    email: str
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + SQLAlchemy + MySQL"}

# 添加一个简单的用户创建 API
@app.post("/users/")
def create_user(user: UserCreate, request:Request, db: Session = Depends(get_db)):  
    log_info('create new user',extra={"user":user,"request_id":request.state.request_id})
    return createU(db=db, name=user.name, email=user.email)

# 查询所有用户
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return getU(db)