import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = os.environ.get("APP_NAME")
    debug: bool = bool(os.environ.get("DEBUG"))
    secret_key: str = os.environ.get("SECRET_KEY")
    cors_allowed_origins: str = os.environ.get("CORS_ALLOWED_ORIGINS")
    version: str = "0.1"
    base_url: str = os.environ.get("BASE_URL")


class DevelopmentSettings(Settings):
    background_tasks: bool = os.environ.get("BACKGROUND_TASKS")
    parsing_delay: int = os.environ.get("PARSING_DELAY")
    available_cpu_cores: int = os.environ.get("AVAILABLE_CPU_CORES")
    pagination_limit: int = os.environ.get("PAGINATION_LIMIT")
    service_api_token: str = os.environ.get("SERVICE_API_TOKEN")


settings = Settings()
development_settings = DevelopmentSettings()
