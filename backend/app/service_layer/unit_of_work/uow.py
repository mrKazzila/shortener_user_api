from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters import UsersRepository
from app.service_layer.unit_of_work.abc_uow import ABCUnitOfWork
from app.settings.database import async_session_maker

__all__ = ["UnitOfWork"]


class UnitOfWork(ABCUnitOfWork):
    __slots__ = ("session_factory",)

    def __init__(self) -> None:
        self.session_factory = async_session_maker

        self._session = None
        self._users_repo = None

    @property
    def session(self) -> AsyncSession:
        if not self._session:
            self._session = self.session_factory()
        return self._session

    @property
    def users_repo(self) -> UsersRepository:
        if not self._users_repo:
            self._users_repo = UsersRepository(session=self.session)
        return self._users_repo

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
