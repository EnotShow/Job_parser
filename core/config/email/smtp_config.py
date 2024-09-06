from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSMTP(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../../.env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    SMTP_PORT: int
    SMTP_HOST: str
    SMTP_PASSWORD: str
    MAIL_FROM: EmailStr


config_smtp = ConfigSMTP()
