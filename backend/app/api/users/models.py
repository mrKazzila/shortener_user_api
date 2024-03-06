from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column

from app.settings.database import Base

int_pk = Annotated[int, mapped_column(primary_key=True)]

