from fastapi import Depends

from backend.database.aggregation_access import (
    DmaAggregationAccess,
    SiteAggregationAccess,
)
from backend.database.session import get_session
from backend.services.aggregation import AggregationService
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
