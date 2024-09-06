from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigEmail(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../../.env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    ADMINS: str
    TEMPLATE_ROOT: str
    AVAILABLE_TYPES: str


config_email = ConfigEmail()
