from dataclasses import dataclass
from enum import StrEnum

from pydantic import EmailStr

__all__ = (
    "AccessTokenDTO",
    "RefreshTokenDTO",
    "TokensDTO",
    "TokenTypesDTO",
    "TokenDataDTO",
)


class TokenTypes(StrEnum):
    access = "access"
    refresh = "refresh"


@dataclass(frozen=True, slots=True, kw_only=True)
class AccessTokenDTO:
    access_token: str
    token_type: str = "bearer"


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshTokenDTO:
    refresh_token: str
    token_type: str = "bearer"


@dataclass(frozen=True, slots=True, kw_only=True)
class TokensDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass(frozen=True, slots=True, kw_only=True)
class TokenDataDTO:
    email: EmailStr
    type: TokenTypes
    expiration: int
