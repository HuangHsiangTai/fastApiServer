from fastapi import FastAPI
from src.utils.logger import LoggingMiddleware, log_info
from src.config.container import ApplicationContainer
from src.utils.router import RouterModule
from src.api import users, internal


def create_app()-> FastAPI:
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)
    app_container = ApplicationContainer()
    # Configure the FastAPI app to use the container
    app.container = app_container
    modules = [users,internal]
    for module in modules:
        assert isinstance(module, RouterModule), f"Module {module} must have a 'router' attribute"
        app.include_router(module.router)
    return app    

app = create_app()
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI + SQLAlchemy + MySQL"}