from dependency_injector import containers, providers
from src.utils.logger import log_info
from src.config.mysql import MySqlClient
from src.repositories.user_repository import UserRepository



class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["..api.users","..api.internal"])
    # Import and use the Config container
    config = providers.Configuration(yaml_files=["config.yml"])
    mysql=providers.Singleton(MySqlClient, user=config.mysql.user, password=config.mysql.password, database=config.mysql.database, host=config.mysql.host)
    user_repository = providers.Factory(
        UserRepository,
        session_factory=mysql.provided.session
    )
