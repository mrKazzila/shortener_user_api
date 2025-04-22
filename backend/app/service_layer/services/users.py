import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.dto.auth import AuthUserDTO
from app.dto.users import (
    CreatedUserDTO,
    UserDTO,
    UserFormDataDTO,
    UserFromDBDTO,
)
from app.exceptions.users import (
    IncorrectEmailOrPasswordException,
    OAuthUserPasswordException,
    UserAlreadyExistException,
    UserNotFoundException,
)
from app.utils import PasswordManager

if TYPE_CHECKING:
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
    ) -> CreatedUserDTO:
        if _ := await self.uow.users_repo.get(
            reference={"email": user_data.email},
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

        async with self.uow as transaction:
            user_repo = transaction.users_repo
            await user_repo.add(data=user_dict)
            await transaction.commit()

        return CreatedUserDTO(
            id=user_id,
            is_active=user_data.is_active,
        )

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

    async def authenticate_user(
        self,
        *,
        form_data: UserFormDataDTO,
    ) -> AuthUserDTO:
        if user := await self.uow.users_repo.get(
            reference={"email": form_data.email},
        ):
            if user.is_oauth:
                raise OAuthUserPasswordException()

            if not self._check_user_credentials(
                user=user,
                form_data=form_data,
            ):
                raise IncorrectEmailOrPasswordException()

            # TODO: UPDATE LAST LOGIN FOR USER

            return AuthUserDTO(
                id=user.id,
                is_active=user.is_active,
            )

        raise UserNotFoundException()

    async def update_last_login(self, email: str) -> None:
        async with self.uow as transaction:
            await transaction.users_repo.update(
                reference={"email": email},
                data={"last_login": datetime.utcnow()},
            )
            await transaction.commit()

    async def get_user_by_id(self, *, user_id: UUID) -> UserFromDBDTO:
        if user := await self.uow.users_repo.get(
            reference={"id": str(user_id)},
        ):
            return UserFromDBDTO(
                id=user.id,
                is_active=user.is_active,
                is_email_verified=user.is_email_verified,
                created_at=user.created_at,
            )

        raise UserNotFoundException()

    def _check_user_credentials(
        self,
        *,
        user: UserDTO,
        form_data: UserFormDataDTO,
    ) -> bool:
        if not user.password or not form_data.password:
            return False

        return (
            user.email == form_data.email
            and self.password_manager.verify_password(
                plain_password=form_data.password,
                hashed_pwd=user.password,
            )
        )

    async def deactivate_user(self, email: str) -> None:
        async with self.uow as transaction:
            await transaction.users_repo.update(
                reference={"email": email},
                data={
                    "is_active": False,
                    "is_deleted": True,
                    "email": f"deleted_{int(datetime.now(UTC).timestamp())}_{email}",
                },
            )
            await transaction.commit()

    async def verify_user_email(self, email: str) -> None:
        async with self.uow as transaction:
            await transaction.users_repo.update(
                reference={"email": email},
                data={"is_email_verified": True},
            )
            await transaction.commit()
