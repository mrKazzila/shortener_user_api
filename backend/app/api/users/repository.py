from adapters.repository import SQLAlchemyRepository

from api.users.models import User


class UsersRepository(SQLAlchemyRepository):
    model = User
