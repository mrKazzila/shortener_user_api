from datetime import UTC, datetime
from uuid import UUID

from app.service_layer.cqrs.command.abc_command import ABCCommandService


class UserCommandService(ABCCommandService):
    async def create_user(self, *, user_data: dict) -> None:
        async with self.uow as uow:
            await uow.users_repo.add(data=user_data)
            await uow.commit()

    async def verify_user_email(self, *, user_id: UUID) -> None:
        async with self.uow as uow:
            await uow.users_repo.update(
                model_id=user_id,
                **{"is_email_verified": True},
            )
            await uow.commit()

    async def update_last_login(self, *, user_id: UUID) -> None:
        async with self.uow as uow:
            await uow.users_repo.update(
                model_id=user_id,
                **{"last_login": datetime.now(UTC)},
            )
            await uow.commit()

    async def update_password(self, *, user_id: UUID, password: str) -> None:
        async with self.uow as uow:
            await uow.users_repo.update(
                model_id=user_id,
                **{"password": password},
            )
            await uow.commit()

    async def deactivate_user(self, *, user_id: UUID) -> None:
        async with self.uow as uow:
            await uow.users_repo.update(
                model_id=user_id,
                **{
                    "is_active": False,
                    "email": f"deleted_{int(datetime.now(UTC).timestamp())}",
                    "deactivated_at": datetime.now(UTC),
                },
            )
            await uow.commit()
