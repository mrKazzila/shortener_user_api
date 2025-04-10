from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.schemas.users import SUser
from app.exceptions.users import UserAlreadyExistException
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
        raise UserAlreadyExistException()

    await UsersServices.create_new_user(uow=uow, user_data=user_data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created"},
    )
