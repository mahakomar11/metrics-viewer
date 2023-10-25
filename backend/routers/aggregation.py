from fastapi import APIRouter, Depends, Query

from backend.dependencies.get_aggregation_service import get_aggregation_service
from backend.schemas import (
    EventType,
    GetAggregationByDmaResponse,
    GetAggregationBySiteResponse,
)
from backend.services.aggregation import AggregationService

router = APIRouter(tags=["Aggregation"])


@router.get("/site", status_code=200, response_model=GetAggregationBySiteResponse)
def get_aggregation_by_site(
    event_type: EventType = Query(default=EventType.registration),
    aggregation_service: AggregationService = Depends(get_aggregation_service),
):
    return GetAggregationBySiteResponse(
        data=aggregation_service.get_by_site(event_type=event_type)
    )


@router.get("/site/page", status_code=200, response_model=GetAggregationBySiteResponse)
def get_aggregation_by_site_page(
    event_type: EventType = Query(default=EventType.registration),
    size: int = Query(default=10),
    offset: int = Query(default=0),
    aggregation_service: AggregationService = Depends(get_aggregation_service),
):
    return GetAggregationBySiteResponse(
        data=aggregation_service.get_by_site(event_type=event_type)[
            offset : offset + size  # noqa: E203
        ]
    )


@router.get("/dma", status_code=200, response_model=GetAggregationByDmaResponse)
def get_aggregation_by_dma(
    event_type: EventType = Query(default=EventType.registration),
    aggregation_service: AggregationService = Depends(get_aggregation_service),
):
    return GetAggregationByDmaResponse(
        data=aggregation_service.get_by_dma(event_type=event_type)
    )


@router.get("/dma/page", status_code=200, response_model=GetAggregationByDmaResponse)
def get_aggregation_by_dma_page(
    event_type: EventType = Query(default=EventType.registration),
    size: int = Query(default=10),
    offset: int = Query(default=0),
    aggregation_service: AggregationService = Depends(get_aggregation_service),
):
    return GetAggregationByDmaResponse(
        data=aggregation_service.get_by_dma(event_type=event_type)[
            offset : offset + size  # noqa: E203
        ]
    )
