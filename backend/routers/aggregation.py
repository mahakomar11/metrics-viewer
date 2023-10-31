from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from backend.dependencies import (
    get_api_key,
    get_dma_aggregation_service,
    get_site_aggregation_service,
)
from backend.schemas import (
    AuthErrorResponse,
    EventType,
    GetAggregationByDmaResponse,
    GetAggregationBySiteResponse,
)
from backend.services.aggregation import AggregationService

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
