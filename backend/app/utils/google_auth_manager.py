import logging

from google.auth.transport import requests
from google.oauth2 import id_token

from app.dto.auth import GoogleAuthUserDTO
from app.settings.config import settings

__all__ = ("GoogleAuthManager",)

logger = logging.getLogger(__name__)


class GoogleAuthManager:
    async def authenticate_token(self, *, token: str) -> GoogleAuthUserDTO:
        try:
            id_info = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )

            if id_info["aud"] != settings.GOOGLE_CLIENT_ID:
                raise ValueError("Invalid audience")

            return GoogleAuthUserDTO(email=id_info["email"])
        except ValueError as e:
            raise e
