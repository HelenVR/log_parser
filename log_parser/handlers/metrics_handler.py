from fastapi import APIRouter, Request
from fastapi.responses import ORJSONResponse
from loguru import logger


from log_parser.application.version import API_VERSION
from log_parser.application.models import ApiErrorResponse, ApiResponseStatuses
from log_parser.data_parser import LogParser

router = APIRouter(
    prefix=f"/api/{API_VERSION}",
    responses={404: {"description": "Not found"}},
)


@router.get('/get_metrics', status_code=200)
async def get_logs(request: Request):
    log_parser: LogParser = request.app.state.log_parser
    try:
        nginx_data = await log_parser.parse_logs()
    except Exception as e:
        error = f'Failed to parse nginx logs: {e.__class__.__name__}, {e}'
        logger.error(error)
        return ORJSONResponse(content=ApiErrorResponse(error=error, status=ApiResponseStatuses.failure.value))
    try:
        nginx_statistics = await log_parser.get_statistics(nginx_data)
        return ORJSONResponse(content=nginx_statistics)
    except Exception as e:
        error = f'Failed to get nginx statistics: {e.__class__.__name__}, {e}'
        logger.error(error)
        return ORJSONResponse(content=ApiErrorResponse(error=error, status=ApiResponseStatuses.failure.value))
