import logging

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.service_layer.cqrs import QueryService, UserCommandService
from app.service_layer.services import UsersServices
from app.service_layer.unit_of_work import UnitOfWork
from app.settings.database import async_session_maker
from app.utils import (
    GoogleAuthManager,
    PasswordManager,
    TokenManager,
    UserAuthManager,
)

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
    def provide_query_service(self) -> QueryService:
        return QueryService(session_factory=async_session_maker)

    @provide(scope=Scope.APP)
    def provide_user_command_service(
        self,
        uow: UnitOfWork,
    ) -> UserCommandService:
        return UserCommandService(uow=uow)

    @provide(scope=Scope.APP)
    def provide_token_manager(self) -> TokenManager:
        return TokenManager()

    @provide(scope=Scope.APP)
    def provide_google_auth_service(self) -> GoogleAuthManager:
        return GoogleAuthManager()

    @provide(scope=Scope.APP)
    def provide_password_manager(self) -> PasswordManager:
        return PasswordManager()

    @provide(scope=Scope.APP)
    def provide_user_auth_service(
        self,
        query_service: QueryService,
        command_service: UserCommandService,
        password_manager: PasswordManager,
    ) -> UserAuthManager:
        return UserAuthManager(
            query_service=query_service,
            command_service=command_service,
            password_manager=password_manager,
        )

    @provide(scope=Scope.APP)
    def provide_user_service(
        self,
        query_service: QueryService,
        command_service: UserCommandService,
        password_manager: PasswordManager,
    ) -> UsersServices:
        return UsersServices(
            query_service=query_service,
            command_service=command_service,
            password_manager=password_manager,
        )
