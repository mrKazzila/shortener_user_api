import logging

from passlib.context import CryptContext

__all__ = ("PasswordManager",)

logger = logging.getLogger(__name__)


class PasswordManager:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(
        self,
        *,
        plain_password: str,
        hashed_pwd: str,
    ) -> bool:
        return self._pwd_context.verify(
            secret=plain_password,
            hash=hashed_pwd,
        )

    def hash_password(self, *, password: str) -> str:
        return self._pwd_context.hash(secret=password)
