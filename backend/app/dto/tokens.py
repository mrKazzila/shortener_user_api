from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

__all__ = (
    "TokenDataDTO",
    "TokensDTO",
    "TokenTypes",
    "UserTokenDTO",
)


class TokenTypes(StrEnum):
    access = "access"
    refresh = "refresh"


@dataclass(frozen=True, slots=True, kw_only=True)
class TokensDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass(frozen=True, slots=True, kw_only=True)
class UserTokenDTO:
    id: UUID
    is_active: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class TokenDataDTO(UserTokenDTO):
    type: TokenTypes
    expiration: int
