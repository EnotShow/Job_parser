import os
from typing import Optional

from pydantic import PostgresDsn
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
"""
POSTGRES_DB=job_parser
POSTGRES_USER=postgres
POSTGRES_PASSWORD=492949
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

postgresql+asyncpg://postgres:492949@localhost:5432/job_parser
"""

settings_db = ConfigDataBase(
    POSTGRES_USER=os.getenv("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
    POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
    POSTGRES_PORT=os.getenv("POSTGRES_PORT"),
    POSTGRES_DB=os.getenv("POSTGRES_DB"),
)
