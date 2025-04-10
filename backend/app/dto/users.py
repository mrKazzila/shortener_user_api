from dataclasses import dataclass

__all__ = ("UserDTO", "UserFromDBDTO")


@dataclass(frozen=True, slots=True, kw_only=True)
class UserDTO:
    email: str
    password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UserFromDBDTO:
    id: int
    email: str
    password: str
