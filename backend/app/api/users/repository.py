from adapters.repository import SQLAlchemyRepository

from api.users.models import Users


class UsersRepository(SQLAlchemyRepository):
    """Users repository."""

    model = Users

    def __repr__(self) -> str:
        return f'UsersRepository with model: {self.model}'
