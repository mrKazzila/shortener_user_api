from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from app.api.routers.schemas.users import (
    SResponseUserDB,
    SResponseUserUpdate,
)
from app.api.routers.users._types import PathUserID
from app.dto.users import XUserHeader
from app.service_layer.services import UsersServices

__all__ = ("router",)


router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute,
)


@router.get(
    "/{user_id}",
    summary="Get user info",
)
async def get_user(
    user_id: PathUserID,
    user_service: FromDishka[UsersServices],
    _: FromDishka[XUserHeader],
) -> SResponseUserDB:
    user_data = await user_service.get_user_by_id(user_id=user_id)
    return SResponseUserDB(**user_data.to_dict())


@router.patch(
    "/{user_id}",
    summary="Update user info",
)
async def patch_user(
    user_id: PathUserID,
    user_data: SResponseUserUpdate,
    user_service: FromDishka[UsersServices],
    _: FromDishka[XUserHeader],
):
    await user_service.update_user_password(
        user_id=user_id,
        password=user_data.password,
    )
    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Password updated"},
    )


@router.delete(
    "/{user_id}",
    summary="Delete user profile",
)
async def delete_user(
    user_id: PathUserID,
    user_service: FromDishka[UsersServices],
    _: FromDishka[XUserHeader],
):
    await user_service.deactivate_user(user_id=user_id)
    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User deleted"},
    )
