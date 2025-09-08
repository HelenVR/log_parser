from fastapi import APIRouter, Request
from fastapi.responses import ORJSONResponse

from log_parser.application.version import VERSION

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/version', status_code=200)
async def get_logs(request: Request):
    return ORJSONResponse(content={'version': VERSION})
