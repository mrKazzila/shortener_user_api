import logging
from typing import TYPE_CHECKING

from app.dto.auth import AuthUserDTO
from app.dto.users import (
    UserFormDataDTO,
    UserFromDBDTO,
)
from app.exceptions.users import (
    IncorrectEmailOrPasswordException,
    OAuthUserPasswordException,
    UserNotFoundException,
)

if TYPE_CHECKING:
    from app.service_layer.cqrs import QueryService, UserCommandService
    from app.utils import PasswordManager

__all__ = ("UserAuthManager",)

logger = logging.getLogger(__name__)


class UserAuthManager:
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

    async def authenticate_user(
        self,
        *,
        form_data: UserFormDataDTO,
    ) -> AuthUserDTO:
        if user := await self.query_service.get_user_by_email(
            email=form_data.email,
        ):
            self._check_user_credentials(user=user, form_data=form_data)
            await self.command_service.update_last_login(user_id=user.id)

            return AuthUserDTO(
                id=user.id,
                is_active=user.is_active,
            )

        raise UserNotFoundException()

    def _check_user_credentials(
        self,
        *,
        user: UserFromDBDTO,
        form_data: UserFormDataDTO,
    ) -> None:
        if user.is_oauth:
            raise OAuthUserPasswordException()

        if not user.password or not form_data.password:
            raise IncorrectEmailOrPasswordException()

        is_password_valid = self.password_manager.verify_password(
            plain_password=form_data.password,
            hashed_pwd=user.password,
        )
        is_valid_email = bool(user.email == form_data.email)

        if not (is_valid_email and is_password_valid):
            raise IncorrectEmailOrPasswordException()
