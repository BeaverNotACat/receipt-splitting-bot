from advanced_alchemy.config import SQLAlchemyAsyncConfig

import src.adapters.database.orm  # noqa: F401
from src.settings import Settings

config = SQLAlchemyAsyncConfig(connection_string=str(Settings().DATABASE_DSN))
