from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKey, APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from config import Config, get_config

AUTH_ERROR = "Api key is invalid"


api_key_header = APIKeyHeader(name="Api-Key", auto_error=False)


async def get_api_key(
    api_key: APIKey | str = Security(api_key_header),
    config: Config = Depends(get_config),
):
    if api_key is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="No api key is set in header"
        )

    if api_key != config.api_key:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=AUTH_ERROR)

    return api_key
