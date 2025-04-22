from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base

__all__ = ("Users",)


class Users(Base):
    """Model for users."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
        unique=True,
        nullable=False,
        doc="Unique user identifier (UUID)",
    )
    email: Mapped[str] = mapped_column(
        doc="User email",
        type_=String(100),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        doc="User password (hash)",
        type_=String(60),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        doc="Is account active",
        default=True,
        nullable=False,
    )
    is_email_verified: Mapped[bool] = mapped_column(
        doc="Is email verified",
        default=False,
        nullable=False,
    )
    is_oauth: Mapped[bool] = mapped_column(
        doc="Is user registered via OAuth",
        default=False,
        nullable=False,
    )
    oauth_provider: Mapped[str] = mapped_column(
        doc="OAuth provider name",
        type_=String(50),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        doc="Registration date",
        type_=DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    last_login: Mapped[datetime] = mapped_column(
        doc="Last login date",
        type_=DateTime(timezone=True),
        nullable=True,
    )
