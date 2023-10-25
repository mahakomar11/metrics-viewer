from fastapi import Depends

from backend.database.aggregation_access import AggregationAccess
from backend.database.session import get_session
from backend.services.aggregation import AggregationService
from config import Config, get_config


def get_aggregation_service(config: Config = Depends(get_config)) -> AggregationService:
    for session in get_session(config):
        yield AggregationService(AggregationAccess(session))
