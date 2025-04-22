from http import HTTPStatus

from app.exceptions.base import BaseCustomException


class BaseUserException(BaseCustomException):
    def __init__(self, status_code, detail: str | None = None) -> None:
        super().__init__(
            status_code=status_code
            if status_code
            else HTTPStatus.UNAUTHORIZED,
            detail=detail,
        )


class UserNotFoundException(BaseUserException):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND)


class UserAlreadyExistException(BaseUserException):
    def __init__(self) -> None:
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail="User already exist.",
        )


class IncorrectEmailOrPasswordException(BaseUserException):
    def __init__(self) -> None:
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password.",
        )


class OAuthUserPasswordException(BaseUserException):
    def __init__(self) -> None:
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="OAuth users must use provider login.",
        )
