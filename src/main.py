from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import src.config.setting
from src.crud.user import create_user as create_u, get_users as get_u
from src.config.mysql import  Base, engine, get_db
from src.utils.logger import LoggingMiddleware, log_info




# create table
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(LoggingMiddleware)


class UserCreate(BaseModel):
    name: str
    email: str
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + SQLAlchemy + MySQL"}

# create user
@app.post("/users/")
def create_user(user: UserCreate, request:Request, db: Session = Depends(get_db)):  
    log_info('create new user',extra={"user":user,"request_id":request.state.request_id})
    return create_u(db=db, name=user.name, email=user.email)

# query all users
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return get_u(db)