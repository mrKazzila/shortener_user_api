from fastapi import HTTPException, status

__all__ = (
    # User
    "UserNotFoundException",
    "UserAlreadyExistException",
    "IncorrectEmailOrPasswordException",
    # Token
    "DecodeTokenException",
    "IncorrectTokenFormatException",
    "EmptyTokenException",
    "ExpireTokenException",
)


# === User ===
class UserNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND)


class UserAlreadyExistException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist.",
        )


class IncorrectEmailOrPasswordException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )


# === Token ===
class BaseTokenException(HTTPException):
    def __init__(self, detail) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
