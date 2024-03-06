import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import routers_setup

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
