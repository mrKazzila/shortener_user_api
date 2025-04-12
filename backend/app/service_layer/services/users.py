import logging
from typing import TYPE_CHECKING

from app.dto.users import UserDTO, UserFormDataDTO
from app.exceptions.users import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistException,
    UserNotFoundException,
)
from app.utils import PasswordManager

if TYPE_CHECKING:
    from app.adapters.domain.users_repository import UsersRepository
    from app.service_layer.unit_of_work import UnitOfWork
    from app.utils import PasswordManager

__all__ = ("UsersServices",)

logger = logging.getLogger(__name__)


class UsersServices:
    __slots__ = ("uow", "password_manager")

    def __init__(
        self,
        uow: "UnitOfWork",
        password_manager: "PasswordManager",
    ) -> None:
        self.uow = uow
        self.password_manager = password_manager

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}. {self.uow}"

    async def create_new_user(
        self,
        *,
        user_data: UserDTO,
    ) -> None:
        async with self.uow as transaction:
            user_repo = transaction.users_repo

            if await self.get_user_from_db(
                user_repo=user_repo,
                email=user_data.email,
            ):
                raise UserAlreadyExistException()

            handel_user_data: UserDTO = self._handel_user_data(
                user_data=user_data,
            )

            await user_repo.add(data=handel_user_data.to_dict())
            await transaction.commit()

    async def is_authenticate_user(
        self,
        *,
        form_data: UserFormDataDTO,
    ) -> bool:
        async with self.uow as transaction:
            user_repo = transaction.users_repo

            user = await self.get_user_from_db(
                user_repo=user_repo,
                email=form_data.email,
            )

        if not user:
            raise UserNotFoundException()

        if is_valid_data := self._check_user(
            user=user,
            user_from_form=form_data,
        ):
            return is_valid_data

        raise IncorrectEmailOrPasswordException()

    @staticmethod
    async def get_user_from_db(
        *,
        user_repo: "UsersRepository",
        email: str,
    ) -> UserDTO | None:
        _reference = {"email": email}

        if result := await user_repo.get(reference=_reference):
            return UserDTO(
                email=result.email,
                password=result.password,
            )
        return None

    def _handel_user_data(self, *, user_data: UserDTO) -> UserDTO:
        hashed_password = self.password_manager.hash_password(
            password=user_data.password,
        )
        return UserDTO(
            email=user_data.email,
            password=hashed_password,
        )

    def _check_user(
        self,
        *,
        user: UserDTO,
        user_from_form: UserFormDataDTO,
    ) -> bool:
        is_valid_pass = self.password_manager.verify_password(
            plain_password=user_from_form.password,
            hashed_pwd=user.password,
        )
        return user.email == user_from_form.email and is_valid_pass
