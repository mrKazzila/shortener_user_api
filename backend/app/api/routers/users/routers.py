from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.routers import exceptions as api_exceptions
from app.api.routers.dependencies import (
    get_current_user_from_access_token,
)
from app.schemas.users import SUser
from app.service_layer.services import UsersServices
from app.service_layer.unit_of_work import ABCUnitOfWork, UnitOfWork

__all__ = ("router",)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
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
        raise api_exceptions.UserAlreadyExistException

    await UsersServices.create_new_user(uow=uow, user_data=user_data)

    return JSONResponse(content={"message": "User created"})


@router.get("/test-protected2")
async def test_protected_route(
    current_user: dict = Depends(get_current_user_from_access_token),
):
    return {
        "message": "This is a test protected route",
        "user_info": current_user,
    }
