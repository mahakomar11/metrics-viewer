from backend.database.aggregation_repository import AggregationRepository
from backend.schemas.dto import AggregationRecord
from backend.schemas.enums import EventType


class AggregationService:
    def __init__(self, aggregation_repository: AggregationRepository):
        self.aggregation_repository = aggregation_repository

    async def get_all(self, event_type: EventType) -> list[AggregationRecord]:
        return await self.aggregation_repository.get_all(event_type)

    async def get_page(
        self, event_type: EventType, size: int, offset: int
    ) -> list[AggregationRecord]:
        return await self.aggregation_repository.get_page(
            event_type, size=size, offset=offset
        )
