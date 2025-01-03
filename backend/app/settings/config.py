import logging
from functools import lru_cache
from pathlib import Path
from sys import exit
from typing import Annotated, cast

from annotated_types import Ge, Le, MinLen
from pydantic import PostgresDsn, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("settings",)

logger = logging.getLogger(__name__)


class ProjectBaseSettings(BaseSettings):
    __ROOT_DIR_ID: int = 2

    model_config = SettingsConfigDict(
        env_file=Path(__file__)
        .resolve()
        .parents[__ROOT_DIR_ID]
        .joinpath("env/.env"),
    )


class Settings(ProjectBaseSettings):
    """Main settings for project."""

    APP_NAME: str
    MODE: str

    ACCESS_TOKEN_EXPIRES: Annotated[int, Ge(1), Le(25)]
    REFRESH_TOKEN_EXPIRES: Annotated[int, Ge(100), Le(360)]
    SECRET_KEY: str
    ALGORITHM: str
    JWT_COOKIE_NAME: str

    POSTGRES_VERSION: str

    DB_PROTOCOL: str
    DB_HOST: str
    DB_PORT: cast(str, Annotated[int, Ge(1), Le(65_535)])
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: Annotated[SecretStr, MinLen(8)]

    @property
    def dsn(self, protocol=None) -> PostgresDsn:
        protocol = protocol or self.DB_PROTOCOL
        return PostgresDsn.build(
            scheme=protocol,
            username=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"{self.DB_NAME}",
        )


@lru_cache
def settings() -> Settings:
    logger.info("Loading settings from env")

    try:
        return Settings()

    except ValidationError as error_:
        logger.error("Error at loading settings from env. %s", error_)
        exit(error_)
