from fastapi import HTTPException
from functools import wraps
from app.api.security.jwt_auth import verify_token
from log_config.logger_config import logger

def wrapper_auth_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        authorization = kwargs.pop("authorization", None)
        if not authorization or not authorization.startswith("Bearer "):
            logger.warning("Invalid token format")
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        if not payload:
            logger.warning("Invalid or expired token")
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        return await func(*args, **kwargs)
    
    return wrapper