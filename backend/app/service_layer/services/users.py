import logging

from app.api.users.auth_utils import PasswordManager
from app.schemas.users import SUser
from app.service_layer.exceptions import (
    IncorrectEmailOrPasswordException,
    UserNotFoundException,
)
from app.service_layer.unit_of_work import UnitOfWork

__all__ = ["UsersServices"]

logger = logging.getLogger(__name__)


class UsersServices:
    @classmethod
    async def create_new_user(
        cls,
        *,
        uow: UnitOfWork,
        user_data: SUser,
    ) -> None:
        handel_user_data = cls._handel_user_data(user_data=user_data)

        async with uow:
            user_repo = uow.users_repo
            await user_repo.add(data=handel_user_data)
            await uow.commit()

    @classmethod
    async def get_user_from_db(
        cls,
        *,
        uow: UnitOfWork,
        email: str,
    ) -> SUser | None:
        _reference = {"email": email}

        async with uow:
            user_repo = uow.users_repo
            result = await user_repo.get(reference=_reference)

        if result:
            return SUser(
                email=result.email,
                password=result.password,
            )

        return None

    @classmethod
    async def is_authenticate_user(
        cls,
        *,
        uow: UnitOfWork,
        form_email: str,
        form_password: str,
    ) -> bool:
        user = await cls.get_user_from_db(uow=uow, email=form_email)

        if not user:
            raise UserNotFoundException

        if is_valid_data := cls._check_user(
            user=user,
            email=form_email,
            password=form_password,
        ):
            return is_valid_data

        raise IncorrectEmailOrPasswordException

    @staticmethod
    def _handel_user_data(user_data: SUser) -> dict[str, str]:
        data = user_data.dict()
        password = data.get("password")
        data["password"] = PasswordManager.hash_password(
            secret_password=password,
        )

        return data

    @staticmethod
    def _check_user(user: SUser, email: str, password: str) -> bool:
        return user.email == email and PasswordManager.verify_password(
            plain_secret_password=password,
            hashed_pwd=user.password,
        )
