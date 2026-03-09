from fastapi import HTTPException, Header, Depends
from typing import Annotated, Dict, Any
from app.api.security.jwt_auth import verify_token
from log_config.logger_config import logger
from enum import Enum



async def get_current_user(
    authorization: Annotated[str | None, Header()] = None
) -> Dict[str, Any]:
    """
    Dependency do weryfikacji tokenu JWT.
    Zwraca payload tokenu z danymi użytkownika.
    
    Raises:
        HTTPException: Jeśli token jest nieprawidłowy lub brakuje
    """
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Missing or invalid Authorization header")
        raise HTTPException(
            status_code=401, 
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    if not payload:
        logger.warning("Invalid or expired token")
        raise HTTPException(
            status_code=401, 
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    logger.info(f"User authenticated: {payload.get('email', 'unknown')}")
    return payload
