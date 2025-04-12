import logging
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.routers.auth._types import QueryRefreshToken
from app.api.schemas.tokens import STokens
from app.dto.users import UserFormDataDTO
from app.service_layer.services import UsersServices
from app.utils import TokenManager

__all__ = ("router",)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@router.post("/login")
async def login_user(
    response: Response,
    form_user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: FromDishka[UsersServices],
    token_manager: FromDishka[TokenManager],
) -> STokens:
    await user_service.is_authenticate_user(
        form_data=UserFormDataDTO(
            email=form_user_data.username,
            password=form_user_data.password,
        ),
    )

    token_pair = token_manager.create_token_pair(
        email=form_user_data.username,
    )

    token_manager.set_token_to_cookie(
        response=response,
        refresh_token=token_pair.refresh_token,
    )

    return STokens(
        access_token=token_pair.access_token,
        refresh_token=token_pair.refresh_token,
    )


@router.post(
    "/refresh",
    summary="Refresh token",
)
def token_refresh(
    response: Response,
    token_manager: FromDishka[TokenManager],
    token: QueryRefreshToken,
) -> STokens:
    token_data = token_manager.verify_refresh_token(token=token)

    new_token_pair = token_manager.update_token_pair(
        email=token_data.email,
    )

    token_manager.set_token_to_cookie(
        response=response,
        refresh_token=new_token_pair.refresh_token,
    )

    return STokens(
        access_token=new_token_pair.access_token,
        refresh_token=new_token_pair.refresh_token,
    )
