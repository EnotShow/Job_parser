import os
from typing import Optional

from pydantic import PostgresDsn, AmqpDsn
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


class ConfigMessageBroker(BaseSettings):
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str

    @property
    def broker_url(self) -> Optional[AmqpDsn]:
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@"
            f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )


settings_db = ConfigDataBase(
    POSTGRES_USER=os.getenv("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
    POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
    POSTGRES_PORT=os.getenv("POSTGRES_PORT"),
    POSTGRES_DB=os.getenv("POSTGRES_DB"),
)

settings_broker = ConfigMessageBroker(
    RABBITMQ_USER=os.getenv("RABBITMQ_USER"),
    RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD"),
    RABBITMQ_HOST=os.getenv("RABBITMQ_HOST"),
    RABBITMQ_PORT=os.getenv("RABBITMQ_PORT"),
)
