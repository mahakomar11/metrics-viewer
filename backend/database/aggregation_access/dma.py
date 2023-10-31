from backend.database.aggregation_repository import AggregationRepository
from backend.schemas.dto import DmaAggregationRecord
from backend.schemas.enums import AggregationField, EventType


class DmaAggregationAccess(AggregationRepository):
    def get_all(
        self, event_type: EventType, decimal_places: int = 2
    ) -> list[DmaAggregationRecord]:
        field_names, rows = self._get_by_field(
            field=AggregationField.dma,
            event_type=event_type,
            decimal_places=decimal_places,
        )
        return [
            DmaAggregationRecord.model_validate(dict(zip(field_names, row)))
            for row in rows
        ]

    def get_page(
        self, event_type: EventType, size: int, offset: int, decimal_places: int = 2
    ) -> list[DmaAggregationRecord]:
        field_names, rows = self._get_by_field(
            field=AggregationField.dma,
            event_type=event_type,
            decimal_places=decimal_places,
            size=size,
            offset=offset,
        )
        return [
            DmaAggregationRecord.model_validate(dict(zip(field_names, row)))
            for row in rows
        ]
