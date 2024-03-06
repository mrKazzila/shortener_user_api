import logging
from datetime import datetime
from typing import Annotated

from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.api.exceptions import IncorrectTokenTypeException, IncorrectTokenFormatException, EmptyTokenException, \
    ExpireTokenException, UserNotFoundException
from app.api.users.auth_utils import TokenManager
from app.schemas.tokens import STokenTypes, STokenData
from app.schemas.users import SUser
from app.service_layer.services.users import UsersServices
from app.service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork

__all__ = ['get_current_user_from_access_token', 'verify_refresh_token']
logger = logging.getLogger(__name__)

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user_from_access_token(
        token: Annotated[_oauth2_scheme, Depends()],
        uow: Annotated[type(ABCUnitOfWork), Depends(UnitOfWork)],
) -> SUser:
    try:
        payload_data = TokenManager.decode_token(token)

        if payload_data.type != STokenTypes.access:
            raise IncorrectTokenTypeException

        if not payload_data.email:
            raise IncorrectTokenFormatException

        if user := await UsersServices.get_user_from_db(
                uow=uow,
                email=payload_data.email,
        ):
            return user

        raise UserNotFoundException

    except HTTPException as e:
        raise e


def _get_refresh_token_from_cookies(request: Request):
    # todo: check cookies not Request?
    if refresh_token := request.cookies.get('booking_access_token'):
        return refresh_token

    raise EmptyTokenException


async def verify_refresh_token(
        refresh_token: Annotated[str, Depends(_get_refresh_token_from_cookies)],
) -> STokenData:
    try:
        payload_data = TokenManager.decode_token(refresh_token)

        if payload_data.type != STokenTypes.refresh:
            raise IncorrectTokenTypeException

        if not payload_data.email:
            raise IncorrectTokenFormatException

        if not __check_token_expire(expire_time=payload_data.expiration):
            raise ExpireTokenException

        return payload_data

    except HTTPException as e:
        raise e


def __check_token_expire(expire_time: int) -> bool:
    current_time = int(datetime.utcnow().timestamp())
    return not expire_time or (expire_time < current_time)
