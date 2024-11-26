from fastapi import HTTPException
from typing import Optional, Any, Dict
import uuid
import traceback
import sys
from loguru import logger

class DetailedHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        internal_error: Optional[Exception] = None,
        context: Dict[str, Any] = None
    ):
        self.request_id = str(uuid.uuid4())
        self.internal_error = internal_error
        self.error_trace = None
        self.context = context or {}
        
        if internal_error:
            self.error_trace = {
                'request_id': self.request_id,
                'error_type': type(internal_error).__name__,
                'message': str(internal_error),
                'traceback': traceback.format_tb(internal_error.__traceback__),
                'sys_info': {
                    'python_version': sys.version,
                    'platform': sys.platform
                },
                'context': self.context
            }
            
            # Log detailed error information
            logger.error(
                f"Detailed error occurred: {detail}",
                error_trace=self.error_trace
            )
        
        super().__init__(status_code, detail)
