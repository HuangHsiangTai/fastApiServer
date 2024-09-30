from fastapi import APIRouter, HTTPException, Depends, Request
from src.crud.user import create_user as create_u, get_users as get_u
from sqlalchemy.orm import Session
from src.config.mysql import  get_db
from pydantic import BaseModel
from src.utils.logger import log_info

router = APIRouter(
    prefix="/users",    
    tags=["users"],    
    responses={404: {"description": "Not found"}},
)


class UserCreate(BaseModel):
    name: str
    email: str

# create user
@router.post("/")
def create_user(user: UserCreate, request:Request, db: Session = Depends(get_db)):  
    log_info('create new user',{"user":user,"request_id":request.state.request_id})
    return create_u(db=db, name=user.name, email=user.email)

# query all users
@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return get_u(db)
