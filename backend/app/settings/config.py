import logging
from functools import lru_cache
from pathlib import Path
from sys import exit
from typing import Annotated, cast

from annotated_types import Ge, Le, MinLen
from pydantic import PostgresDsn, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class ProjectBaseSettings(BaseSettings):
    __ROOT_DIR_ID: int = 2

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[__ROOT_DIR_ID].joinpath('env/.env'),
    )


class Settings(ProjectBaseSettings):
    """Main settings for project."""
    APP_NAME: str
    MODE: str

    ACCESS_TOKEN_EXPIRES: int = 1
    REFRESH_TOKEN_EXPIRES: int = 300
    SECRET_KEY: str = "09d25e094faa6ca2556c818136b7a9563b93f7022f6y0f4caa6cg63b88e8d4e7"
    ALGORITHM: str = "HS256"

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
        url_ = PostgresDsn.build(
            scheme=protocol,
            username=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f'{self.DB_NAME}',
        )

        return url_


@lru_cache
def settings() -> Settings:
    logger.info('Loading settings from env')

    try:
        settings_ = Settings()
        return settings_

    except ValidationError as e:
        logger.error('Error at loading settings from env. %(err)s', {'err': e})
        exit(e)
