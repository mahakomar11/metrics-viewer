from fastapi import Depends

from backend.database.aggregation_access import (
    DmaAggregationAccess,
    SiteAggregationAccess,
)
from backend.database.session import get_session
from backend.services.aggregation import AggregationService
from config import Config, get_config


def get_site_aggregation_service(
    config: Config = Depends(get_config),
) -> AggregationService:
    for session in get_session(config):
        yield AggregationService(SiteAggregationAccess(session))


def get_dma_aggregation_service(
    config: Config = Depends(get_config),
) -> AggregationService:
    for session in get_session(config):
        yield AggregationService(DmaAggregationAccess(session))
