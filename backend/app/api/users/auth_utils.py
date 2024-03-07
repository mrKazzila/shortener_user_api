from datetime import datetime, timedelta
from typing import NoReturn

from fastapi import Request, Response
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import SecretStr

from app.api.exceptions import (
    DecodeTokenException,
    EmptyTokenException,
    ExpireTokenException,
    IncorrectTokenFormatException,
    IncorrectTokenTypeException,
)
from app.schemas.tokens import STokenData, STokens, STokenTypes
from app.settings.config import settings

__all__ = ["TokenManager", "PasswordManager"]


class PasswordManager:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(
        cls,
        *,
        plain_secret_password: SecretStr | str,
        hashed_pwd: SecretStr | str,
    ) -> bool:
        plain_str_password = cls._convert_password_to_str(
            secret_password=plain_secret_password,
        )
        hashed_pwd_str = cls._convert_password_to_str(
            secret_password=hashed_pwd,
        )

        return cls._pwd_context.verify(
            secret=plain_str_password,
            hash=hashed_pwd_str,
        )

    @classmethod
    def hash_password(cls, *, secret_password: SecretStr | str) -> str:
        str_password = cls._convert_password_to_str(
            secret_password=secret_password,
        )
        return cls._pwd_context.hash(secret=str_password)

    @staticmethod
    def _convert_password_to_str(*, secret_password: SecretStr | str) -> str:
        if isinstance(secret_password, SecretStr):
            return secret_password.get_secret_value()
        return secret_password


class TokenManager:
    _secret_key = settings().SECRET_KEY
    _algorithm = settings().ALGORITHM
    _jwt_cookie_name = settings().JWT_COOKIE_NAME

    @classmethod
    def set_token_to_cookie(
        cls,
        *,
        response: Response,
        refresh_token: str,
    ) -> None:
        response.set_cookie(
            key=cls._jwt_cookie_name,
            value=refresh_token,
            httponly=True,
            expires=360,
            max_age=-1,
        )

    @classmethod
    def get_refresh_token_from_cookies(cls, *, request: Request) -> str:
        if refresh_token := request.cookies.get(cls._jwt_cookie_name):
            return refresh_token
        raise EmptyTokenException

    @classmethod
    def decode_token(cls, *, token: str) -> STokenData:
        try:
            raw_token_data = jwt.decode(
                token,
                cls._secret_key,
                cls._algorithm,
            )
        except JWTError as e:
            raise DecodeTokenException(detail=e)

        return STokenData(
            email=raw_token_data.get("sub"),
            type=raw_token_data.get("type"),
            expiration=raw_token_data.get("exp"),
        )

    @classmethod
    def create_token_pair(cls, *, email: str) -> STokens:
        access_token = cls._create_token(
            data={"sub": email, "type": STokenTypes.access},
            expires_delta=timedelta(minutes=settings().ACCESS_TOKEN_EXPIRES),
        )
        refresh_token = cls._create_token(
            data={"sub": email, "type": STokenTypes.refresh},
            expires_delta=timedelta(minutes=settings().REFRESH_TOKEN_EXPIRES),
        )

        return STokens(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    def update_token_pair(cls, *, email: str) -> STokens:
        return cls.create_token_pair(email=email)

    @staticmethod
    def validate_token_payload(
        *,
        payload_data: STokenData,
        token_type: STokenTypes,
    ) -> NoReturn:
        if payload_data.type != token_type:
            raise IncorrectTokenTypeException

        if not payload_data.email:
            raise IncorrectTokenFormatException

        if not payload_data.expiration:
            raise IncorrectTokenFormatException

    @classmethod
    def validate_token_expire(cls, *, expire_time: int) -> NoReturn:
        if cls._check_token_expire(token_expire_time=expire_time):
            raise ExpireTokenException

    @classmethod
    def _create_token(cls, *, data: dict, expires_delta: timedelta) -> str:
        to_encode = {**data}

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, cls._secret_key, cls._algorithm)

    @staticmethod
    def _check_token_expire(*, token_expire_time: int) -> bool:
        current_time = int(datetime.utcnow().timestamp())
        return bool(current_time > token_expire_time)
