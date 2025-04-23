import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.dto.users import (
    CreatedUserDTO,
    UserDTO,
    UserFromDBDTO,
)
from app.exceptions.users import (
    UserAlreadyExistException,
    UserNotFoundException,
)

if TYPE_CHECKING:
    from app.service_layer.cqrs import QueryService, UserCommandService
    from app.utils import PasswordManager

__all__ = ("UsersServices",)

logger = logging.getLogger(__name__)


class UsersServices:
    __slots__ = ("query_service", "command_service", "password_manager")

    def __init__(
        self,
        *,
        query_service: "QueryService",
        command_service: "UserCommandService",
        password_manager: "PasswordManager",
    ) -> None:
        self.query_service = query_service
        self.command_service = command_service
        self.password_manager = password_manager

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}."

    async def create_new_user(
        self,
        *,
        user_data: UserDTO,
    ) -> CreatedUserDTO:
        if _ := await self.query_service.get_user_by_email(
            email=user_data.email,
        ):
            raise UserAlreadyExistException()

        if not user_data.is_oauth and not user_data.password:
            raise ValueError("Password is required for non-OAuth users")

        hashed_password = (
            self.password_manager.hash_password(
                password=user_data.password,
            )
            if user_data.password
            else None
        )

        user_id = uuid4()
        user_dict = self._new_user_dict_object(
            user_id=user_id,
            password=hashed_password,
            user_data=user_data,
        )

        await self.command_service.create_user(user_data=user_dict)

        return CreatedUserDTO(
            id=user_id,
            is_active=user_data.is_active,
        )

    async def get_user_by_id(self, *, user_id: UUID) -> UserFromDBDTO:
        if user := await self.query_service.get_user_by_id(user_id=user_id):
            return user
        raise UserNotFoundException()

    async def update_last_login(self, email: str) -> None:
        user = await self.query_service.get_user_by_email(email=email)
        await self.command_service.update_last_login(user_id=user.id)

    async def update_user_password(
        self,
        *,
        user_id: UUID,
        password: str,
    ) -> None:
        hashed_password = self.password_manager.hash_password(
            password=password,
        )
        user = await self.query_service.get_user_by_id(user_id=user_id)

        await self.command_service.update_password(
            user_id=user.id,
            password=hashed_password,
        )

    async def deactivate_user(self, user_id: UUID) -> None:
        if user := await self.query_service.get_user_by_id(user_id=user_id):
            if user.is_active:
                await self.command_service.deactivate_user(user_id=user.id)
            raise UserNotFoundException()
        raise UserNotFoundException()

    async def verify_user_email(self, email: str) -> None:
        user = await self.query_service.get_user_by_email(email=email)
        await self.command_service.verify_user_email(user_id=user.id)

    @staticmethod
    def _new_user_dict_object(
        *,
        user_id: UUID,
        password: str | None,
        user_data: UserDTO,
    ) -> dict[str, str | bool | datetime | UUID | None]:
        user_dict = user_data.to_dict()
        user_dict.update(
            {
                "id": user_id,
                "password": password,
                "created_at": datetime.now(UTC),
                "is_email_verified": user_data.is_oauth,
            },
        )

        return user_dict
