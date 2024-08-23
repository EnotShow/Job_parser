from pydantic_settings import BaseSettings


class ConfigSMTP(BaseSettings):
    SMTP_PORT: int
    SMTP_HOST: str
    SMTP_PASSWORD: str
    MAIL_FROM: str


config_smtp = ConfigSMTP()
