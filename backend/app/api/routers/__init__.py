from app.api.routers.healthcheck import router as healthcheck_router
from app.api.routers.users import router as users_router

ROUTERS = {users_router, healthcheck_router}

__all__ = ("ROUTERS",)
