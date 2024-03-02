import logging
from contextlib import asynccontextmanager

from app.api.router_setup import routers_setup
from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info('Service started')

    yield

    logger.info('Service exited')


app = FastAPI(
    title='ShortenerUserApi',
    lifespan=lifespan,
)

routers_setup(app=app)
