from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from src.config import get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verificar_api_key(
    api_key: str | None = Security(api_key_header),
    settings = Depends(get_settings),
):
    if api_key is None or api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key ausente ou inválida.",
        )