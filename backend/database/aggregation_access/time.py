import datetime

from sqlalchemy import func, select

from backend.database.aggregation_repository import AggregationRepository
from backend.database.models import Impression
from backend.schemas.dto import TimeAggregationRecord
from backend.schemas.enums import AggregationField, EventType

DEFAULT_INTERVAL = datetime.timedelta(days=1)


class TimeAggregationAccess(AggregationRepository):
    async def get_all(
        self,
        event_type: EventType,
        interval: datetime.timedelta = DEFAULT_INTERVAL,
        decimal_places: int = 2,
    ) -> list[TimeAggregationRecord]:
        self._set_interval(interval)

        field_names, rows = await self._get_by_field(
            field=AggregationField.reg_interval,
            event_type=event_type,
            decimal_places=decimal_places,
        )
        return [
            TimeAggregationRecord.model_validate(dict(zip(field_names, row)))
            for row in rows
        ]

    async def get_page(
        self,
        event_type: EventType,
        size: int,
        offset: int,
        interval: datetime.timedelta = DEFAULT_INTERVAL,
        decimal_places: int = 2,
    ) -> list[TimeAggregationRecord]:
        self._set_interval(interval)

        field_names, rows = await self._get_by_field(
            field=AggregationField.reg_interval,
            event_type=event_type,
            decimal_places=decimal_places,
            size=size,
            offset=offset,
        )
        return [
            TimeAggregationRecord.model_validate(dict(zip(field_names, row)))
            for row in rows
        ]

    @staticmethod
    def _set_interval(interval: datetime.timedelta):
        setattr(
            Impression,
            AggregationField.reg_interval,
            func.date_bin(
                interval, Impression.reg_time, select(func.min(Impression.reg_time))
            ).label(AggregationField.reg_interval),
        )

    # async def _get_by_field(
    #     self,
    #     event_type: EventType,
    #     decimal_places: int = 2,
    #     size: int | None = None,
    #     offset: int | None = None,
    # ) -> (tuple[str], list[tuple]):
    #     field = 'reg_interval'
    #     Impression.reg_interval = func.date_bin(interval, Impression.reg_time, origin).label(field)
    #     query = self._query_aggregation(field, event_type, decimal_places)
    #     if size is not None:
    #         query = query.limit(size)
    #     if offset is not None:
    #         query = query.offset(offset)
    #
    #     result = await self._session.execute(query)
    #     return (
    #         'reg_interval',
    #         "impressions_count",
    #         "clicks_count",
    #         "events_count",
    #         "ctr",
    #         "evpm",
    #     ), result.all()

    # def _query_aggregation(
    #     self, event_type: EventType, decimal_places: int
    # ) -> Query:
    #     subquery_impressions = self._subquery_impressions()
    #     subquery_clicks = self._subquery_clicks(event_type)
    #     subquery_events = self._subquery_events(event_type)
    #
    #     field = 'reg_interval'
    #     return (
    #         select(
    #             getattr(subquery_impressions.c, field),
    #             subquery_impressions.c.impressions_count,
    #             func.coalesce(subquery_clicks.c.clicks_count, 0),
    #             func.coalesce(subquery_events.c.events_count, 0),
    #             self._ctr(
    #                 subquery_clicks, subquery_impressions, decimal_places=decimal_places
    #             ),
    #             self._evpm(
    #                 subquery_events, subquery_impressions, decimal_places=decimal_places
    #             ),
    #         )
    #         .join(
    #             subquery_clicks,
    #             getattr(subquery_impressions.c, field)
    #             == getattr(subquery_clicks.c, field),
    #             isouter=True,
    #         )
    #         .join(
    #             subquery_events,
    #             getattr(subquery_impressions.c, field)
    #             == getattr(subquery_events.c, field),
    #             isouter=True,
    #         )
    #         .order_by(field)
    #     )
    #
    # @staticmethod
    # def _subquery_impressions() -> Subquery:
    #     return (
    #         select(
    #             func.date_bin(interval, Impression.reg_time, origin).label('reg_interval'),
    #             func.count(Impression.uuid).label("impressions_count"),
    #         )
    #         .group_by('reg_interval')
    #         .subquery()
    #     )
    #
    # @staticmethod
    # def _subquery_clicks(
    #     event_type: EventType
    # ) -> Subquery:
    #     return (
    #         select(
    #             func.date_bin(interval, Impression.reg_time, origin).label('reg_interval'),
    #             func.count(Event.id).label("clicks_count")
    #         )
    #         .filter(Event.tag == event_type)
    #         .join(Event, Impression.uuid == Event.impression_uuid, isouter=True)
    #         .group_by('reg_interval')
    #         .subquery()
    #     )
    #
    # @staticmethod
    # def _subquery_events(
    #     event_type: EventType
    # ) -> Subquery:
    #     return (
    #         select(
    #             func.date_bin(interval, Impression.reg_time, origin).label('reg_interval'), func.count(Event.id).label("events_count")
    #         )
    #         .filter(Event.tag.in_([event_type, f"v{event_type}"]))
    #         .join(Event, Impression.uuid == Event.impression_uuid, isouter=True)
    #         .group_by('reg_interval')
    #         .subquery()
    #     )
