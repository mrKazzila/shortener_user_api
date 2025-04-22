from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.routers.schemas.users import SRequestUser, SResponseUserDB
from app.api.routers.users._types import QueryUserID
from app.dto.users import UserDTO
from app.service_layer.services import UsersServices

__all__ = ("router",)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute,
)


@router.post(
    "/",
    summary="Create user",
    response_model=dict[str, str],
)
async def create_user(
    user_data: SRequestUser,
    user_service: FromDishka[UsersServices],
):
    await user_service.create_new_user(
        user_data=UserDTO(
            email=str(user_data.email),
            password=user_data.password.get_secret_value(),
        ),
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created"},
    )


@router.get(
    "/",
    summary="Get user info",
)
async def get_user(
    user_id: QueryUserID,
    user_service: FromDishka[UsersServices],
) -> SResponseUserDB:
    user_data = await user_service.get_user_by_id(user_id=user_id)
    return SResponseUserDB(**user_data.to_dict())
