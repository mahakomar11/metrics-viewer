import abc
import datetime

from pydantic import BaseModel


class AggregationRecord(BaseModel, abc.ABC):
    impressions_count: int
    clicks_count: int
    events_count: int
    ctr: float
    evpm: float


class SiteAggregationRecord(AggregationRecord):
    site_id: str


class DmaAggregationRecord(AggregationRecord):
    mm_dma: int


class TimeAggregationRecord(AggregationRecord):
    reg_interval: datetime.datetime
