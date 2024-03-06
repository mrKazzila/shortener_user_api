import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import (
    get_current_user_from_access_token,
    verify_refresh_token,
)
from app.api.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistException,
    UserNotFoundException,
)
from app.api.users.auth_utils import TokenManager
from app.schemas.tokens import STokenData, STokens
from app.schemas.users import SUser
from app.service_layer import exceptions as service_exceptions
from app.service_layer.services.users import UsersServices
from app.service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth & users"],
)


@router.post(
    "/create",
    summary="Create user",
    response_model=dict[str, str],
)
async def create_user(
    user_data: SUser,
    uow: Annotated[type(ABCUnitOfWork), Depends(UnitOfWork)],
):
    if await UsersServices.get_user_from_db(
        uow=uow,
        email=user_data.email,
    ):
        raise UserAlreadyExistException

    await UsersServices.create_new_user(uow=uow, user_data=user_data)

    return {"200": "User created"}


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

        response.set_cookie(
            key="booking_access_token",
            value=token_pair.refresh_token,
            httponly=True,
            expires=360,
        )

        return token_pair
    except HTTPException as e:
        raise e
    except Exception as e:
        if isinstance(e, service_exceptions.UserNotFoundException):
            raise UserNotFoundException
        if isinstance(e, service_exceptions.IncorrectEmailOrPasswordException):
            raise IncorrectEmailOrPasswordException


@router.post(
    "/refresh",
    summary="Refresh token",
)
def token_refresh(
    response: Response,
    refresh_token: STokenData = Depends(verify_refresh_token),
) -> STokens:
    new_token_pair = TokenManager.update_token_pair(email=refresh_token.email)

    response.set_cookie(
        key="booking_access_token",
        value=new_token_pair.refresh_token,
        httponly=True,
        expires=360,
    )

    return new_token_pair


@router.get("/me")
async def get_current_user_info(response: Response):
    return {"code": 200, "headers": response.headers}


@router.get("/test-protected1")
async def protected_route(
    current_user: SUser = Depends(get_current_user_from_access_token),
):
    return {"message": "This is a protected route"}


@router.get("/test-protected2")
async def test_protected_route(
    current_user: dict = Depends(get_current_user_from_access_token),
):
    return {
        "message": "This is a test protected route",
        "user_info": current_user,
    }
