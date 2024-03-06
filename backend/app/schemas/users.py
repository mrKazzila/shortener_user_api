from pydantic import BaseModel, EmailStr, SecretStr

__all__ = ["SUser", "SUserDB"]


class SUser(BaseModel):
    email: EmailStr
    password: SecretStr


class SUserDB(SUser):
    id: int
