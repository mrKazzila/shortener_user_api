from typing import Any, Type, TypeVar

from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.abc_repository import ABCRepository
from settings.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class SQLAlchemyRepository(ABCRepository):
    __slots__ = ('session',)
    model: Type[ModelType] = None

    def __init__(self, *, session: AsyncSession) -> None:
        self.session = session

    async def add(self, *, data: dict):
        """Add new entity."""
        statement = insert(self.model).values(**data).returning(self.model)
        statement_result = await self.session.execute(statement=statement)

        return statement_result.scalar_one()

    async def update(self, *, model_id: int, **update_data: Any):
        """Update entity some data."""
        statement = update(self.model).filter_by(id=model_id).values(**update_data)
        await self.session.execute(statement)
