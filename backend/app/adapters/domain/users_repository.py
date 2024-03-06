from app.adapters.base import SQLAlchemyRepository
from app.models import Users

__all__ = ["UsersRepository"]


class UsersRepository(SQLAlchemyRepository):
    """Users repository."""

    model = Users

    def __repr__(self) -> str:
        return f"UsersRepository for model: {self.model}"
