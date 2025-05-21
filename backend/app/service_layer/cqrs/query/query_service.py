from uuid import UUID

from app.adapters import UsersRepository
from app.dto.users import UserFromDBDTO
from app.service_layer.cqrs.query.abc_query import ABCQueryService


class QueryService(ABCQueryService):
    async def get_user_by_email(self, *, email: str) -> UserFromDBDTO | None:
        return await self._get_user(reference={"email": email})

    async def get_user_by_id(self, *, user_id: UUID) -> UserFromDBDTO | None:
        return await self._get_user(reference={"id": str(user_id)})

    async def _get_user(self, *, reference: dict) -> UserFromDBDTO | None:
        async with self.session_factory() as session:
            user = await UsersRepository(session=session).get(
                reference=reference,
            )
            if not user:
                return None

            return UserFromDBDTO(
                id=user.id,
                email=user.email,
                password=user.password,
                is_active=user.is_active,
                is_email_verified=user.is_email_verified,
                is_oauth=user.is_oauth,
                created_at=user.created_at,
                last_login=user.last_login,
                deactivated_at=user.deactivated_at,
            )
