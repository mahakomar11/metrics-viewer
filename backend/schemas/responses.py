from pydantic import BaseModel

from backend.schemas.dto import DmaAggregationRecord, SiteAggregationRecord


class GetAggregationBySiteResponse(BaseModel):
    data: list[SiteAggregationRecord]


class GetAggregationByDmaResponse(BaseModel):
    data: list[DmaAggregationRecord]
