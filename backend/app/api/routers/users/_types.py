from typing import Annotated
from uuid import UUID

from fastapi import Path

__all__ = ("PathUserID",)


PathUserID = Annotated[
    UUID,
    Path(
        description="Unique user identifier (UUID)",
        example=UUID("1fbbe5e1-5441-4ca4-a012-a0cd62e94245"),
    ),
]
