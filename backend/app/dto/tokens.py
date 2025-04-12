from dataclasses import dataclass
from enum import StrEnum

__all__ = (
    "AccessTokenDTO",
    "RefreshTokenDTO",
    "TokensDTO",
    "TokenTypes",
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
    email: str
    type: TokenTypes
    expiration: int
