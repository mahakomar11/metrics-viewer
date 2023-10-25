from sqlalchemy import Numeric, cast, func

from backend.database.aggregation_repository import AggregationRepository
from backend.database.models import Event, Impression
from backend.schemas.dto import DmaAggregationRecord, SiteAggregationRecord
from backend.schemas.enums import AggregationField, EventType


class AggregationAccess(AggregationRepository):
    def get_all_by_dma(
        self, event_type: EventType, decimal_places: int = 2
    ) -> list[DmaAggregationRecord]:
        field_names, rows = self._get_all(
            field=AggregationField.dma,
            event_type=event_type,
            decimal_places=decimal_places,
        )
        return [
            DmaAggregationRecord.model_validate(dict(zip(field_names, row)))
            for row in rows
        ]

    def get_all_by_site(
        self, event_type: EventType, decimal_places: int = 2
    ) -> list[SiteAggregationRecord]:
        field_names, rows = self._get_all(
            field=AggregationField.site,
            event_type=event_type,
            decimal_places=decimal_places,
        )
        return [
            SiteAggregationRecord.model_validate(dict(zip(field_names, row)))
            for row in rows
        ]

    def _get_all(
        self, field: AggregationField, event_type: EventType, decimal_places: int = 2
    ) -> (tuple[str], list[tuple]):
        query = self._query_aggregation(field, event_type, decimal_places)
        return (
            field,
            "impressions_count",
            "clicks_count",
            "events_count",
            "ctr",
            "evpm",
        ), query.all()

    def _query_aggregation(
        self, field: AggregationField, event_type: EventType, decimal_places: int
    ):
        subquery_impressions = self._subquery_impressions(field)
        subquery_clicks = self._subquery_clicks(field, event_type)
        subquery_events = self._subquery_events(field, event_type)

        return (
            self._session.query(
                getattr(subquery_impressions.c, field),
                subquery_impressions.c.impressions_count,
                func.coalesce(subquery_clicks.c.clicks_count, 0),
                func.coalesce(subquery_events.c.events_count, 0),
                self._ctr(
                    subquery_clicks, subquery_impressions, decimal_places=decimal_places
                ),
                self._evpm(
                    subquery_events, subquery_impressions, decimal_places=decimal_places
                ),
            )
            .join(
                subquery_clicks,
                getattr(subquery_impressions.c, field)
                == getattr(subquery_clicks.c, field),
                isouter=True,
            )
            .join(
                subquery_events,
                getattr(subquery_impressions.c, field)
                == getattr(subquery_events.c, field),
                isouter=True,
            )
            .order_by(getattr(subquery_impressions.c, field))
        )

    def _subquery_impressions(self, field: AggregationField):
        return (
            self._session.query(
                getattr(Impression, field),
                func.count(Impression.uuid).label("impressions_count"),
            )
            .group_by(getattr(Impression, field))
            .subquery()
        )

    def _subquery_clicks(self, field: AggregationField, event_type: EventType):
        return (
            self._session.query(
                getattr(Impression, field), func.count(Event.id).label("clicks_count")
            )
            .filter(Event.tag == event_type)
            .join(Event, Impression.uuid == Event.impression_uuid, isouter=True)
            .group_by(getattr(Impression, field))
            .subquery()
        )

    def _subquery_events(self, field: AggregationField, event_type: EventType):
        return (
            self._session.query(
                getattr(Impression, field), func.count(Event.id).label("events_count")
            )
            .filter(Event.tag.in_([event_type, f"v{event_type}"]))
            .join(Event, Impression.uuid == Event.impression_uuid, isouter=True)
            .group_by(getattr(Impression, field))
            .subquery()
        )

    @staticmethod
    def _ctr(subquery_clicks, subquery_impressions, decimal_places: int):
        return cast(
            (
                100
                * func.coalesce(subquery_clicks.c.clicks_count, 0)
                / subquery_impressions.c.impressions_count
            ),
            Numeric(10, decimal_places),
        )

    @staticmethod
    def _evpm(subquery_events, subquery_impressions, decimal_places: int):
        return cast(
            (
                100
                * func.coalesce(subquery_events.c.events_count, 0)
                / subquery_impressions.c.impressions_count
            ),
            Numeric(10, decimal_places),
        )


"""
Raw SQL query:

SELECT 
    impres.site_id, 
    impres.count as impressions_count, 
    coalesce(clicks.count, 0) as clicks_count, 
    coalesce(events.count, 0) as events_count, 
    (100 * coalesce(clicks.count, 0) / impres.count) as ctr, 
    (100 * coalesce(events.count, 0) / impres.count) as evpm
FROM 
    (
        SELECT site_id, count(uuid) 
        FROM impression 
        GROUP BY site_id
    ) AS impres 
LEFT JOIN 
    (
        SELECT site_id, count(event.id) 
        FROM impression 
        LEFT JOIN event ON impression.uuid = event.impression_uuid 
        WHERE event.tag = 'registration' 
        GROUP BY site_id
    ) AS clicks
ON impres.site_id = clicks.site_id
LEFT JOIN
    (
        SELECT site_id, count(event.id)
        FROM impression 
        LEFT JOIN event ON impression.uuid = event.impression_uuid 
        WHERE event.tag = 'registration' or event.tag = 'vregistration' 
        GROUP BY site_id
    ) as events
ON impres.site_id = events.site_id
ORDER BY ctr desc;
"""  # noqa: W291
