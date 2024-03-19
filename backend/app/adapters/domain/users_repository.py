from app.adapters.base import SQLAlchemyRepository
from app.models import Users

__all__ = ("UsersRepository",)


class UsersRepository(SQLAlchemyRepository):
    """Users repository."""

    model = Users
