from datetime import datetime, timezone, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import SecretStr

from app.api.exceptions import DecodeTokenException
from app.schemas.tokens import STokenTypes, STokenData, STokens
from app.settings.config import settings

__all__ = ['TokenManager', 'PasswordManager']


class PasswordManager:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(
            cls,
            *,
            plain_secret_password: SecretStr | str,
            hashed_pwd: SecretStr | str,
    ) -> bool:
        plain_str_password = cls._convert_password_to_str(plain_secret_password)
        hashed_pwd_str = cls._convert_password_to_str(hashed_pwd)

        return cls._pwd_context.verify(plain_str_password, hashed_pwd_str)

    @classmethod
    def hash_password(cls, *, secret_password: SecretStr | str) -> str:
        str_password = cls._convert_password_to_str(secret_password)

        return cls._pwd_context.hash(str_password)

    @staticmethod
    def _convert_password_to_str(secret_password: SecretStr | str) -> str:
        if isinstance(secret_password, SecretStr):
            return secret_password.get_secret_value()

        return secret_password


class TokenManager:
    @staticmethod
    def decode_token(token: str) -> STokenData:
        try:
            raw_token_data = jwt.decode(
                token,
                settings().SECRET_KEY,
                settings().ALGORITHM,
            )
        except JWTError as e:
            raise DecodeTokenException(detail=e)

        return STokenData(
            email=raw_token_data.get("sub"),
            type=raw_token_data.get("type"),
            expiration=raw_token_data.get("exp"),
        )

    @classmethod
    def create_token_pair(cls, email: str) -> STokens:
        access_token = cls._create_token(
            data={
                "sub": email,
                "type": STokenTypes.access,
            },
            expires_delta=timedelta(minutes=settings().ACCESS_TOKEN_EXPIRES),
        )
        refresh_token = cls._create_token(
            data={
                "sub": email,
                "type": STokenTypes.refresh,
            },
            expires_delta=timedelta(minutes=settings().REFRESH_TOKEN_EXPIRES),
        )

        return STokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @classmethod
    def update_token_pair(cls, email: str) -> STokens:
        return cls.create_token_pair(email=email)

    @staticmethod
    def _create_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            settings().SECRET_KEY,
            settings().ALGORITHM,
        )
