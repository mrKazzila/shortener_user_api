import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.routers import exceptions as api_exceptions
from app.api.routers.auth.auth_utils import TokenManager
from app.api.routers.dependencies import (
    verify_refresh_token,
)
from app.schemas.tokens import STokenData, STokens
from app.service_layer import exceptions as service_exceptions
from app.service_layer.services import UsersServices
from app.service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork

__all__ = ("router",)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login_user(
    response: Response,
    form_user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: Annotated[type(ABCUnitOfWork), Depends(UnitOfWork)],
) -> STokens:
    try:
        await UsersServices.is_authenticate_user(
            uow=uow,
            form_email=form_user_data.username,
            form_password=form_user_data.password,
        )

        token_pair = TokenManager.create_token_pair(
            email=form_user_data.username,
        )

        TokenManager.set_token_to_cookie(
            response=response,
            refresh_token=token_pair.refresh_token,
        )

        return token_pair

    except service_exceptions.UserNotFoundException:
        raise api_exceptions.UserNotFoundException

    except service_exceptions.IncorrectEmailOrPasswordException:
        raise api_exceptions.IncorrectEmailOrPasswordException

    except HTTPException as error_:
        raise error_


@router.post(
    "/refresh",
    summary="Refresh token",
)
def token_refresh(
    response: Response,
    refresh_token: STokenData = Depends(verify_refresh_token),
) -> STokens:
    new_token_pair = TokenManager.update_token_pair(email=refresh_token.email)

    TokenManager.set_token_to_cookie(
        response=response,
        refresh_token=new_token_pair.refresh_token,
    )

    return new_token_pair
