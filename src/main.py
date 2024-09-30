from fastapi import FastAPI
import src.config.setting
from src.config.mysql import  Base, engine
from src.utils.logger import LoggingMiddleware, log_info
from src.utils.router import RouterModule
from src.api import users


# create table
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(LoggingMiddleware)

modules = [users]
for module in modules:
    assert isinstance(module, RouterModule), f"Module {module} must have a 'router' attribute"
    app.include_router(module.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + SQLAlchemy + MySQL"}