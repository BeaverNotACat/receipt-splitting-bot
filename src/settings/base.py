from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
