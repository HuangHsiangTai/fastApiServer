from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict
from src.config.container import ApplicationContainer
from src.utils.logger import log_info
from dependency_injector.wiring import inject, Provide

router = APIRouter(
    prefix="/internal",    
    tags=["internal"],    
    responses={404: {"description": "Not found"}},
)


# query mysql configuration
@router.get("/mysql")
@inject
def read_mysql(config:Dict[str,any] = Depends(Provide[ApplicationContainer.config])):
    log_info("read_mysql",extra={"config":config})
    return config
