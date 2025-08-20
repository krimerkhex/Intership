from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    USER: str
    PASSWORD: str
    NAME: str
    HOST: str
    PORT: int
    URL: PostgresDsn


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env"],
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )
    db: DatabaseConfig


config = Config()
