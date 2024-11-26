from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.errors import DetailedHTTPException
import uuid
from loguru import logger

async def error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except DetailedHTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                'status': 'error',
                'detail': e.detail,
                'request_id': e.request_id
            }
        )
    except Exception as e:
        error_id = str(uuid.uuid4())
        logger.exception(f"Unhandled error: {error_id}")
        return JSONResponse(
            status_code=500,
            content={
                'status': 'error',
                'detail': 'Internal server error',
                'request_id': error_id
            }
        )

__all__ = ['error_handler']
