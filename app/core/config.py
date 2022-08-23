from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'technical_debt'
    secret_key: str = "super secret key"

    class Config:
        env_file = ".env"


APP_VERSION = '0.1.0'
ENV = 'dev'
MICROSERVICE = 'default'


@lru_cache()
def get_settings():
    """Using cache to avoid multiple initializations."""
    return Settings()
