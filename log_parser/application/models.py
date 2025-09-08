from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ApiErrorResponse(BaseModel):
    status: str
    error: Optional[str] = None


class ApiResponseStatuses(Enum):
    success = 'OK'
    failure = 'FAILED'
