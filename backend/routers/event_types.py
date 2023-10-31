from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from backend.dependencies import get_api_key
from backend.schemas import AuthErrorResponse, EventType, GetEventTypesResponse

router = APIRouter(
    tags=["Event Types"],
    dependencies=[Depends(get_api_key)],
    responses={
        HTTP_401_UNAUTHORIZED: {
            "model": AuthErrorResponse,
            "description": "Authorization Error",
        }
    },
)


@router.get("", status_code=HTTP_200_OK, response_model=GetEventTypesResponse)
def get_event_types():
    """
    Get all possible event types.
    """
    return GetEventTypesResponse(event_types=map(str, EventType))
