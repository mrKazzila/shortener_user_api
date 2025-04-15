import re
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints

__all__ = (
    "SAccessToken",
    "SRefreshToken",
    "STokens",
    "STokenTypes",
    "STokenData",
    "SRefreshTokenRequest",
)



_JWT_REGEX = re.compile(
    r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$",
    re.IGNORECASE,
)
_JWTString = Annotated[
    str,
    StringConstraints(pattern=_JWT_REGEX.pattern),
]


class SRefreshTokenRequest(BaseModel):
    token: _JWTString = Field(description="Refresh token")


class STokenBase(BaseModel):
    token_type: str = "bearer"


class SAccessToken(STokenBase):
    access_token: str


class SRefreshToken(STokenBase):
    refresh_token: str


class STokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class STokenTypes(StrEnum):
    access = "access"
    refresh = "refresh"


class STokenData(BaseModel):
    email: EmailStr
    type: STokenTypes
    expiration: int
