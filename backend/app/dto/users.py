from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Self
from uuid import UUID

__all__ = ("CreatedUserDTO", "UserDTO", "UserFormDataDTO", "UserFromDBDTO")


@dataclass(frozen=True, slots=True, kw_only=True)
class UserDTO:
    email: str
    password: str | None
    is_active: bool = True
    is_email_verified: bool = False
    is_oauth: bool = False
    oauth_provider: str | None = None

    def to_dict(self: Self) -> dict[str, str | bool | None]:
        return asdict(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatedUserDTO:
    id: UUID
    is_active: bool = True


@dataclass(frozen=True, slots=True, kw_only=True)
class UserFormDataDTO:
    email: str
    password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UserFromDBDTO:
    id: UUID
    is_active: bool
    is_email_verified: bool
    created_at: datetime

    def to_dict(self: Self) -> dict[str, str | bool | datetime]:
        return asdict(self)
