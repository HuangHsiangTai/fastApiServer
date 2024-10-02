import src.models.user
from src.config.mysql import engine, Base


def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")