from dataclasses import asdict, dataclass
from typing import Self

__all__ = ("UserDTO", "UserFromDBDTO", "UserFormDataDTO")


@dataclass(frozen=True, slots=True, kw_only=True)
class UserDTO:
    email: str
    password: str

    def to_dict(self: Self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserFromDBDTO:
    id: int
    email: str
    password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UserFormDataDTO(UserDTO):
    pass
