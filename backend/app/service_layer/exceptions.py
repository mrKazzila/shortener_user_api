__all__ = ("UserNotFoundException", "IncorrectEmailOrPasswordException")


class UserNotFoundException(Exception):
    pass


class IncorrectEmailOrPasswordException(Exception):
    pass
