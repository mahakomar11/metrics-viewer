from backend.database.aggregation_repository import AggregationRepository
from backend.schemas.dto import DmaAggregationRecord, SiteAggregationRecord
from backend.schemas.enums import EventType


class AggregationService:
    def __init__(self, aggregation_repository: AggregationRepository):
        self.aggregation_repository = aggregation_repository

    def get_by_site(self, event_type: EventType) -> list[SiteAggregationRecord]:
        return self.aggregation_repository.get_all_by_site(event_type)

    def get_by_dma(self, event_type: EventType) -> list[DmaAggregationRecord]:
        return self.aggregation_repository.get_all_by_dma(event_type)
