import datetime

from backend.database.aggregation_access import TimeAggregationAccess
from backend.schemas.dto import AggregationRecord
from backend.schemas.enums import EventType


class TimeAggregationService:
    def __init__(self, aggregation_repository: TimeAggregationAccess):
        self.aggregation_repository = aggregation_repository

    async def get_all(
        self, event_type: EventType, interval: datetime.timedelta
    ) -> list[AggregationRecord]:
        return await self.aggregation_repository.get_all(event_type, interval=interval)

    async def get_page(
        self,
        event_type: EventType,
        size: int,
        offset: int,
        interval: datetime.timedelta,
    ) -> list[AggregationRecord]:
        return await self.aggregation_repository.get_page(
            event_type, size=size, offset=offset, interval=interval
        )
