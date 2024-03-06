from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.settings.database import Base

__all__ = ['Users']


class Users(Base):
    """Model for users."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        doc='User email',
        type_=String(100),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        doc='User password (hash)',
        type_=String(500),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f'User {self.id}: {self.email}'