from typing import Annotated

from sqlalchemy.orm import mapped_column

from settings.database import Base

int_pk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    pass
