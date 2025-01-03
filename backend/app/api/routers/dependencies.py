import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.api.routers.exceptions import UserNotFoundException
from app.api.routers.auth.auth_utils import TokenManager
from app.schemas.tokens import STokenData, STokenTypes
from app.schemas.users import SUser
from app.service_layer.services import UsersServices
from app.service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork

__all__ = ("get_current_user_from_access_token", "verify_refresh_token")

logger = logging.getLogger(__name__)
_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user_from_access_token(
    token: Annotated[_oauth2_scheme, Depends()],
    uow: Annotated[type(ABCUnitOfWork), Depends(UnitOfWork)],
) -> SUser:
    try:
        payload_data = TokenManager.decode_token(token=token)

        TokenManager.validate_token_payload(
            payload_data=payload_data,
            token_type=STokenTypes.access,
        )

        if user := await UsersServices.get_user_from_db(
            uow=uow,
            email=payload_data.email,
        ):
            return user
        raise UserNotFoundException

    except HTTPException as error_:
        raise error_


async def verify_refresh_token(
    refresh_token: Annotated[
        str,
        Depends(TokenManager.get_refresh_token_from_cookies),
    ],
) -> STokenData:
    try:
        payload_data = TokenManager.decode_token(token=refresh_token)

        TokenManager.validate_token_payload(
            payload_data=payload_data,
            token_type=STokenTypes.refresh,
        )

        TokenManager.validate_token_expire(
            expire_time=payload_data.expiration,
        )

        return payload_data

    except HTTPException as error_:
        raise error_
