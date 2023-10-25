import abc

from sqlalchemy.orm import Session

from backend.schemas.dto import DmaAggregationRecord, SiteAggregationRecord
from backend.schemas.enums import EventType


class AggregationRepository(abc.ABC):
    def __init__(self, session: Session):
        self._session = session

    @abc.abstractmethod
    def get_all_by_dma(
        self, event_type: EventType, decimal_places: int = 2
    ) -> list[DmaAggregationRecord]:
        pass

    @abc.abstractmethod
    def get_all_by_site(
        self, event_type: EventType, decimal_places: int = 2
    ) -> list[SiteAggregationRecord]:
        pass
