import logging
from urllib.parse import urljoin

from app.api.shortener import schemas, utils
from app.service_layer.unit_of_work import UnitOfWork
from app.settings.config import settings

logger = logging.getLogger(__name__)
