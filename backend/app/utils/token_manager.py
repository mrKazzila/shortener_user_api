from datetime import datetime, timedelta, UTC

from fastapi import Response
from jose import JWTError, jwt

from app.dto.tokens import TokenDataDTO, TokensDTO, TokenTypes
from app.exceptions.tokens import (
    DecodeTokenException,
    ExpireTokenException,
    IncorrectTokenFormatException,
    IncorrectTokenTypeException,
)
from app.settings.config import settings


class TokenManager:
    __slots__ = (
        "_secret_key",
        "_algorithm",
        "_jwt_cookie_name",
        "_access_token_expires",
        "_refresh_token_expires",
    )

    def __init__(self):
        _settings = settings()

        self._secret_key = _settings.SECRET_KEY
        self._algorithm = _settings.ALGORITHM
        self._jwt_cookie_name = _settings.JWT_COOKIE_NAME
        self._access_token_expires = _settings.ACCESS_TOKEN_EXPIRES
        self._refresh_token_expires = _settings.REFRESH_TOKEN_EXPIRES

    def set_token_to_cookie(
        self,
        *,
        response: Response,
        refresh_token: str,
    ) -> None:
        response.set_cookie(
            key=self._jwt_cookie_name,
            value=refresh_token,
            httponly=True,
            expires=3600,
        )

    def verify_refresh_token(self, *, token: str) -> TokenDataDTO:
        try:
            payload_data = self.decode_token(token=token)

            self.validate_token_payload(
                payload_data=payload_data,
                token_type=TokenTypes.refresh,
            )

            self.validate_token_expire(
                expire_time=payload_data.expiration,
            )

            return payload_data

        except Exception as error:
            raise error

    def decode_token(self, *, token: str) -> TokenDataDTO:
        try:
            raw_token_data = jwt.decode(
                token,
                self._secret_key,
                self._algorithm,
            )
        except JWTError as error:
            raise DecodeTokenException(detail=str(error))

        return TokenDataDTO(
            email=raw_token_data.get("sub"),
            type=raw_token_data.get("type"),
            expiration=raw_token_data.get("exp"),
        )

    def create_token_pair(self, *, email: str) -> TokensDTO:
        access_token = self._create_token(
            data={"sub": email, "type": TokenTypes.access},
            expires_delta=timedelta(minutes=self._access_token_expires),
        )
        refresh_token = self._create_token(
            data={"sub": email, "type": TokenTypes.refresh},
            expires_delta=timedelta(minutes=self._refresh_token_expires),
        )

        return TokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def update_token_pair(self, *, email: str) -> TokensDTO:
        return self.create_token_pair(email=email)

    @staticmethod
    def validate_token_payload(
        *,
        payload_data: TokenDataDTO,
        token_type: TokenTypes,
    ):
        if payload_data.type != token_type:
            raise IncorrectTokenTypeException()

        if not payload_data.email:
            raise IncorrectTokenFormatException()

        if not payload_data.expiration:
            raise IncorrectTokenFormatException()

    @classmethod
    def validate_token_expire(cls, *, expire_time: int):
        if cls._check_token_expire(token_expire_time=expire_time):
            raise ExpireTokenException()

    def _create_token(self, *, data: dict, expires_delta: timedelta) -> str:
        to_encode = {**data}
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._secret_key, self._algorithm)

    @staticmethod
    def _check_token_expire(*, token_expire_time: int) -> bool:
        current_time = int(datetime.now(UTC).timestamp())
        return current_time > token_expire_time
