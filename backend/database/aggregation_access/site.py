from backend.database.aggregation_repository import AggregationRepository
from backend.schemas.dto import SiteAggregationRecord
from backend.schemas.enums import AggregationField, EventType


class SiteAggregationAccess(AggregationRepository):
    def get_all(
        self, event_type: EventType, decimal_places: int = 2
    ) -> list[SiteAggregationRecord]:
        field_names, rows = self._get_by_field(
            field=AggregationField.site,
            event_type=event_type,
            decimal_places=decimal_places,
        )
        return [
            SiteAggregationRecord.model_validate(dict(zip(field_names, row)))
            for row in rows
        ]

    def get_page(
        self, event_type: EventType, size: int, offset: int, decimal_places: int = 2
    ) -> list[SiteAggregationRecord]:
        field_names, rows = self._get_by_field(
            field=AggregationField.site,
            event_type=event_type,
            decimal_places=decimal_places,
            size=size,
            offset=offset,
        )
        return [
            SiteAggregationRecord.model_validate(dict(zip(field_names, row)))
            for row in rows
        ]
