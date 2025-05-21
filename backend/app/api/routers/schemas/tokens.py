from uuid import UUID

from pydantic import BaseModel

__all__ = (
    "SRequestGoogleAuth",
    "SRequestRefreshToken",
    "SResponseTokens",
    "SResponseGoogleAuthToken",
)


class _SBaseTokenRequest(BaseModel):
    token: str


class SRequestGoogleAuth(_SBaseTokenRequest): ...


class SRequestRefreshToken(_SBaseTokenRequest): ...


class SResponseTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SResponseGoogleAuthToken(SResponseTokens):
    user_id: UUID
