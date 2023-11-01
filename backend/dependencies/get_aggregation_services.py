from fastapi import Depends

from backend.database.aggregation_access import (
    DmaAggregationAccess,
    SiteAggregationAccess,
    TimeAggregationAccess,
)
from backend.database.session import get_session
from backend.services.aggregation import AggregationService
from backend.services.time_aggregation import TimeAggregationService
from config import Config, get_config


async def get_site_aggregation_service(
    config: Config = Depends(get_config),
) -> AggregationService:
    async for session in get_session(config):
        yield AggregationService(SiteAggregationAccess(session))


async def get_dma_aggregation_service(
    config: Config = Depends(get_config),
) -> AggregationService:
    async for session in get_session(config):
        yield AggregationService(DmaAggregationAccess(session))


async def get_time_aggregation_service(
    config: Config = Depends(get_config),
) -> TimeAggregationService:
    async for session in get_session(config):
        yield TimeAggregationService(TimeAggregationAccess(session))
