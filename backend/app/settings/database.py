import uuid

from asyncpg import Connection
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.settings.config import settings

__all__ = ("async_session_maker", "ENGINE_URL")

ENGINE_URL: str = str(settings().dsn)


# fix asyncpg.exceptions.InvalidSQLStatementNameError:
# prepared statement "__asyncpg_stmt_4c" does not exist
# discussion
# https://github.com/sqlalchemy/sqlalchemy/issues/6467#issuecomment-1187494311
class SQLAlchemyConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid.uuid4()}__"


engine: AsyncEngine = create_async_engine(
    url=ENGINE_URL,
    echo=True,
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
        "connection_class": SQLAlchemyConnection,
    },
    pool_pre_ping=True,
    poolclass=NullPool,
)

async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
