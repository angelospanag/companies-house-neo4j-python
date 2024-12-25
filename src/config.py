from functools import lru_cache

from pydantic import SecretStr, HttpUrl, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    companies_house_api_key: SecretStr
    companies_house_base_url: HttpUrl
    neo4j_uri: AnyUrl
    neo4j_user: str
    neo4j_password: SecretStr

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
