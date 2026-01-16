from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

from fastapi.security.api_key import APIKeyHeader, APIKeyQuery
from app.config import settings

header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)
query_scheme = APIKeyQuery(name="api_key", auto_error=False)

def get_api_key(
    api_key_header: str = Security(header_scheme),
    api_key_query: str = Security(query_scheme)
):
    key = api_key_header or api_key_query
    
    if not key:
        print("DEBUG: API Key missing from both header and query")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API manquante (header X-API-Key ou paramètre ?api_key=)",
        )
    
    valid_keys = [k.strip() for k in settings.API_KEYS.split(",")]
    if key not in valid_keys:
        print(f"DEBUG: Invalid API Key attempt: {key}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clé API invalide",
        )
    return key
