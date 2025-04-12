import logging

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.service_layer.services import UsersServices
from app.service_layer.unit_of_work import UnitOfWork
from app.settings.database import async_session_maker
from app.utils import PasswordManager, TokenManager

logger = logging.getLogger(__name__)

__all__ = ("ServiceProvider",)


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_async_session(self) -> AsyncSession:
        return async_session_maker()

    @provide(scope=Scope.APP)
    def provide_uow(self) -> UnitOfWork:
        return UnitOfWork(session_factory=async_session_maker)

    @provide(scope=Scope.APP)
    def provide_token_manager(self) -> TokenManager:
        return TokenManager()

    @provide(scope=Scope.APP)
    def provide_password_manager(self) -> PasswordManager:
        return PasswordManager()

    @provide(scope=Scope.APP)
    def provide_user_service(
        self,
        uow: UnitOfWork,
        password_manager: PasswordManager,
    ) -> UsersServices:
        return UsersServices(
            uow=uow,
            password_manager=password_manager,
        )
