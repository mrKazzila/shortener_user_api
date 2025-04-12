import re
from typing import Annotated

from fastapi import Query

__all__ = ("QueryRefreshToken",)


_JWT_REGEX = re.compile(
    r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$",
    re.IGNORECASE,
)

QueryRefreshToken = Annotated[
    str,
    Query(
        description="Refresh token",
        regex=_JWT_REGEX.pattern,
    ),
]
