from fastapi import APIRouter, HTTPException, Depends, Request
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.repositories.user_repository import UserRepository
from src.config.container import ApplicationContainer
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
@inject
def create_user(user: UserCreate, request:Request, user_repository:UserRepository =  Depends(Provide[ApplicationContainer.user_repository])):  
    log_info('create new user',{"user":user,"request_id":request.state.request_id})
    return user_repository.create_user(name=user.name, email=user.email)

# query all users
@router.get("/")
@inject
def read_users(request:Request,user_repository:UserRepository =  Depends(Provide[ApplicationContainer.user_repository])):
    log_info('get user',{"request_id":request.state.request_id})
    return user_repository.get_user()
