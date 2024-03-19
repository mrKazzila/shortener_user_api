from enum import StrEnum

from pydantic import BaseModel, EmailStr

__all__ = (
    "SAccessToken",
    "SRefreshToken",
    "STokens",
    "STokenTypes",
    "STokenData",
)


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
