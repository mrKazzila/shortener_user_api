from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, SecretStr

__all__ = ("SRequestUser", "SResponseUserDB", "SResponseUserUpdate")


class SRequestUser(BaseModel):
    email: EmailStr
    password: SecretStr


class SResponseUserDB(BaseModel):
    id: UUID
    is_active: bool
    is_email_verified: bool
    created_at: datetime
    last_login: datetime | None


class SResponseUserUpdate(BaseModel):
    password: str
