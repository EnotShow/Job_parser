from pydantic_settings import BaseSettings


class ConfigEmail(BaseSettings):
    ADMINS: str
    TEMPLATE_ROOT: str
    AVAILABLE_TYPES: str


config_email = ConfigEmail()
