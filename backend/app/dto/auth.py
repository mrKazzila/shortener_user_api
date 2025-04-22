from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

__all__ = (
    "AuthUserDTO",
    "GoogleAuthUserDTO",
)


class OauthProviders(StrEnum):
    GOOGLE = "google"


@dataclass(frozen=True, slots=True, kw_only=True)
class GoogleAuthUserDTO:
    email: str
    password: None = None
    is_active: bool = True
    is_email_verified: bool = True
    is_oauth: bool = True
    provider: str = OauthProviders.GOOGLE


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthUserDTO:
    id: UUID
    is_active: bool
