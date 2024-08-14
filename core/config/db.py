import os
from typing import Optional

from pydantic import PostgresDsn, AmqpDsn, RedisDsn
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class ConfigDataBase(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DB_ECHO_LOG: bool = False

    @property
    def database_url(self) -> Optional[PostgresDsn]:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


class ConfigCacheBroker(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    @property
    def broker_url(self) -> Optional[RedisDsn]:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/"


settings_db = ConfigDataBase(
    POSTGRES_USER=os.getenv("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
    POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
    POSTGRES_PORT=os.getenv("POSTGRES_PORT"),
    POSTGRES_DB=os.getenv("POSTGRES_DB"),
)

settings_broker = ConfigCacheBroker(
    REDIS_HOST=os.getenv("REDIS_HOST", "localhost"),
    REDIS_PORT=os.getenv("REDIS_PORT", "6379"),
    REDIS_PASSWORD=os.getenv("REDIS_PASSWORD", None),
)
