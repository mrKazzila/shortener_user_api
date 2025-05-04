import logging
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.routers.schemas.tokens import (
    SRequestGoogleAuth,
    SRequestRefreshToken,
    SResponseGoogleAuthToken,
    SResponseTokens,
)
from app.dto.tokens import UserTokenDTO
from app.dto.users import UserDTO, UserFormDataDTO
from app.service_layer.services import UsersServices
from app.utils import GoogleAuthManager, TokenManager, UserAuthManager

__all__ = ("router",)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@router.post("/login")
async def login_user(
    form_user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    token_manager: FromDishka[TokenManager],
    user_auth_manager: FromDishka[UserAuthManager],
) -> SResponseTokens:
    user = await user_auth_manager.authenticate_user(
        form_data=UserFormDataDTO(
            email=form_user_data.username,
            password=form_user_data.password,
        ),
    )

    token_pair = token_manager.create_token_pair(
        user_data=UserTokenDTO(
            id=user.id,
            is_active=user.is_active,
        ),
    )

    return SResponseTokens(
        access_token=token_pair.access_token,
        refresh_token=token_pair.refresh_token,
    )


@router.post("/google")
async def login_with_google(
    google_data: SRequestGoogleAuth,
    google_auth: FromDishka[GoogleAuthManager],
    user_service: FromDishka[UsersServices],
    token_manager: FromDishka[TokenManager],
) -> SResponseGoogleAuthToken:
    google_user = await google_auth.authenticate_token(
        token=google_data.token,
    )

    user = await user_service.query_service.get_user_by_email(
        email=google_user.email,
    )

    if not user:
        user = await user_service.create_new_user(
            user_data=UserDTO(
                email=google_user.email,
                password=google_user.password,
                is_email_verified=google_user.is_email_verified,
                is_oauth=google_user.is_oauth,
                oauth_provider=google_user.provider,
            ),
        )

    await user_service.update_last_login(email=google_user.email)

    token_pair = token_manager.create_token_pair(
        user_data=UserTokenDTO(
            id=user.id,
            is_active=user.is_active,
        ),
    )

    return SResponseGoogleAuthToken(
        user_id=user.id,
        access_token=token_pair.access_token,
        refresh_token=token_pair.refresh_token,
    )


@router.post("/refresh")
async def token_refresh(
    token: SRequestRefreshToken,
    token_manager: FromDishka[TokenManager],
) -> SResponseTokens:
    token_data = token_manager.verify_refresh_token(token=token.token)

    new_token_pair = token_manager.update_token_pair(
        user_token_data=UserTokenDTO(
            id=token_data.id,
            is_active=token_data.is_active,
        ),
    )

    return SResponseTokens(
        access_token=new_token_pair.access_token,
        refresh_token=new_token_pair.refresh_token,
    )
