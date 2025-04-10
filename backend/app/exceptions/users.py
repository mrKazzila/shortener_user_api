from app.exceptions.base import BaseCustomException


class BaseUserException(BaseCustomException):
    def __init__(self, status_code, detail: str | None = None) -> None:
        super().__init__(
            status_code=status_code
            if status_code
            else status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class UserNotFoundException(BaseUserException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND)


class UserAlreadyExistException(BaseUserException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist.",
        )


class IncorrectEmailOrPasswordException(BaseUserException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
