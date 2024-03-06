from fastapi import APIRouter, status

from app.api.healthcheck.data_types import OK_STATUS

router = APIRouter(
    prefix='/api/healthcheck',
    tags=['healthcheck'],
)


@router.get(
    path='/',
    name='Simple healthchecker',
    status_code=status.HTTP_200_OK,
)
async def get_status() -> type(OK_STATUS):
    """
    Returns the health status of the application.

    Returns:
        HealthcheckStatus: A dataclass representing the health status,
        with a default status of 'ok'.

    """
    return OK_STATUS
