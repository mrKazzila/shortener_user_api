from app.api.middlewares.error_middleware import ErrorMiddleware

MIDDLEWARES = {ErrorMiddleware}

__all__ = ("MIDDLEWARES",)
