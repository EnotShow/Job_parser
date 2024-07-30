import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class JWTSettings(BaseSettings):
    ACCESS_TOKEN_LIFETIME = int(os.environ.get("ACCESS_TOKEN_LIFETIME"))
    REFRESH_TOKEN_LIFETIME = int(os.environ.get("REFRESH_TOKEN_LIFETIME"))
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")


settings_bot = JWTSettings()
