import uvicorn
from fastapi import FastAPI

from backend.routers.aggregation import router as aggregation_router
from config import get_config

config = get_config()

APP = FastAPI(
    title="Metrics viewer API",
    description="API for getting metrics aggregation",
    docs_url=config.api_prefix + "/docs",
    openapi_url=config.api_prefix + "/openapi.json",
)

APP.include_router(aggregation_router, prefix=config.api_prefix + "/aggregation")


if __name__ == "__main__":
    uvicorn.run(APP, host="0.0.0.0", port=8000)
