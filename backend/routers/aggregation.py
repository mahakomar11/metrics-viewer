import datetime

from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from backend.dependencies import (
    get_api_key,
    get_dma_aggregation_service,
    get_site_aggregation_service,
    get_time_aggregation_service,
)
from backend.schemas import (
    AuthErrorResponse,
    EventType,
    GetAggregationByDmaResponse,
    GetAggregationBySiteResponse,
    GetAggregationByTimeResponse,
)
from backend.services.aggregation import AggregationService
from backend.services.time_aggregation import TimeAggregationService

router = APIRouter(
    tags=["Aggregation"],
    dependencies=[Depends(get_api_key)],
    responses={
        HTTP_401_UNAUTHORIZED: {
            "model": AuthErrorResponse,
            "description": "Authorization Error",
        }
    },
)

interval_query = Query(
    default=datetime.timedelta(days=1),
    description="""
    Time interval in ISO8601 format. Examples:
    P1M (1 month), P5D (5 days), P1D (1 day),
    P0DT5H (5 hours), P0DT1H (1 hour),
    P0DT0H30M (30 min), P0DT0H10M (10 min)
    """,
)


@router.get(
    "/site", status_code=HTTP_200_OK, response_model=GetAggregationBySiteResponse
)
async def get_aggregation_by_site(
    event_type: EventType = Query(default=EventType.registration),
    aggregation_service: AggregationService = Depends(get_site_aggregation_service),
):
    """
    Get CTR and EvPM metrics aggregated by site.
    """
    return GetAggregationBySiteResponse(
        data=await aggregation_service.get_all(event_type=event_type)
    )


@router.get("/site/page", status_code=200, response_model=GetAggregationBySiteResponse)
async def get_aggregation_by_site_page(
    event_type: EventType = Query(default=EventType.registration),
    size: int = Query(default=10, title="Number of records to return"),
    offset: int = Query(default=0, title="Number of first records to skip"),
    aggregation_service: AggregationService = Depends(get_site_aggregation_service),
):
    """
    Get CTR and EvPM metrics aggregated by site, part of records, ordered by site.
    """
    return GetAggregationBySiteResponse(
        data=await aggregation_service.get_page(
            event_type=event_type, size=size, offset=offset
        )
    )


@router.get("/dma", status_code=200, response_model=GetAggregationByDmaResponse)
async def get_aggregation_by_dma(
    event_type: EventType = Query(default=EventType.registration),
    aggregation_service: AggregationService = Depends(get_dma_aggregation_service),
):
    """
    Get CTR and EvPM metrics aggregated by DMA.
    """
    return GetAggregationByDmaResponse(
        data=await aggregation_service.get_all(event_type=event_type)
    )


@router.get("/dma/page", status_code=200, response_model=GetAggregationByDmaResponse)
async def get_aggregation_by_dma_page(
    event_type: EventType = Query(default=EventType.registration),
    size: int = Query(default=10),
    offset: int = Query(default=0),
    aggregation_service: AggregationService = Depends(get_dma_aggregation_service),
):
    """
    Get CTR and EvPM metrics aggregated by DMA, part of records, ordered by DMA.
    """
    return GetAggregationByDmaResponse(
        data=await aggregation_service.get_page(
            event_type=event_type, size=size, offset=offset
        )
    )


@router.get("/time", status_code=200, response_model=GetAggregationByTimeResponse)
async def get_aggregation_by_time(
    event_type: EventType = Query(default=EventType.registration),
    interval: datetime.timedelta = interval_query,
    aggregation_service: TimeAggregationService = Depends(get_time_aggregation_service),
):
    """
    Get CTR and EvPM metrics aggregated by registration intervals.
    """
    return GetAggregationByTimeResponse(
        data=await aggregation_service.get_all(event_type=event_type, interval=interval)
    )


@router.get("/time/page", status_code=200, response_model=GetAggregationByTimeResponse)
async def get_aggregation_by_time_page(
    event_type: EventType = Query(default=EventType.registration),
    interval: datetime.timedelta = interval_query,
    size: int = Query(default=10),
    offset: int = Query(default=0),
    aggregation_service: TimeAggregationService = Depends(get_time_aggregation_service),
):
    """
    Get CTR and EvPM metrics aggregated by registration intervals, part of records, ordered by DMA.
    """
    return GetAggregationByTimeResponse(
        data=await aggregation_service.get_page(
            event_type=event_type, size=size, offset=offset, interval=interval
        )
    )
