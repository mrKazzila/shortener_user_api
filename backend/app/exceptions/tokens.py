from app.exceptions.base import BaseCustomException
from http import HTTPStatus


class BaseTokenException(BaseCustomException):
    def __init__(self, detail) -> None:
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=detail,
        )


class DecodeTokenException(BaseTokenException):
    def __init__(self, detail) -> None:
        super().__init__(detail=str(detail))


class IncorrectTokenFormatException(BaseTokenException):
    def __init__(self) -> None:
        super().__init__(detail="Incorrect token format.")


class IncorrectTokenTypeException(BaseTokenException):
    def __init__(self) -> None:
        super().__init__(detail="Incorrect token type.")


class EmptyTokenException(BaseTokenException):
    def __init__(self) -> None:
        super().__init__(detail="The token is missing.")


class ExpireTokenException(BaseTokenException):
    def __init__(self) -> None:
        super().__init__(detail="Your token has expired.")
