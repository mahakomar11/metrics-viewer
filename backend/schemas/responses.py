from pydantic import BaseModel, Field

from backend.schemas import EventType
from backend.schemas.dto import (
    DmaAggregationRecord,
    SiteAggregationRecord,
    TimeAggregationRecord,
)


class GetEventTypesResponse(BaseModel):
    event_types: list[EventType]


class GetAggregationBySiteResponse(BaseModel):
    data: list[SiteAggregationRecord]


class GetAggregationByDmaResponse(BaseModel):
    data: list[DmaAggregationRecord]


class GetAggregationByTimeResponse(BaseModel):
    data: list[TimeAggregationRecord]


class ErrorResponse(BaseModel):
    detail: str


class AuthErrorResponse(ErrorResponse):
    detail: str = Field(..., example="No api key is set in header")
