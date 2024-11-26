from fastapi import HTTPException
from typing import Optional, Any, Dict
import uuid

class DetailedHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        internal_error: Optional[Exception] = None,
        context: Dict[str, Any] = None
    ):
        self.request_id = str(uuid.uuid4())
        self.error_response = {
            'status': 'error',
            'detail': detail,
            'request_id': self.request_id
        }
        if context:
            self.error_response['context'] = context
        super().__init__(status_code=status_code, detail=detail)

    def get_response(self) -> dict:
        return self.error_response
