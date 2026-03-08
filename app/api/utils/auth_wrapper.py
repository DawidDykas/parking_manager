from fastapi import HTTPException, Header, Depends
from typing import Annotated, Dict, Any
from app.api.security.jwt_auth import verify_token
from log_config.logger_config import logger
from enum import Enum


class UserRole(str, Enum):
    """Enum dla ról użytkowników"""
    ADMIN = "admin"
    USER = "user"
    OPERATOR = "operator"


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


# def require_role(*allowed_roles: UserRole):
#     """
#     Dependency factory do sprawdzania ról użytkownika.
    
#     Args:
#         allowed_roles: Role, które mają dostęp do endpointu
        
#     Returns:
#         Dependency function sprawdzający role
        
#     Example:
#         @app.get("/admin", dependencies=[Depends(require_role(UserRole.ADMIN))])
#     """
#     async def role_checker(
#         current_user: Dict[str, Any] = Depends(get_current_user)
#     ) -> Dict[str, Any]:
#         user_role = current_user.get("role", "user")
        
#         if user_role not in [role.value for role in allowed_roles]:
#             logger.warning(
#                 f"User {current_user.get('email')} with role '{user_role}' "
#                 f"attempted to access endpoint requiring {[r.value for r in allowed_roles]}"
#             )
#             raise HTTPException(
#                 status_code=403,
#                 detail="Insufficient permissions"
#             )
        
#         return current_user
    
#     return role_checker


# # Backward compatibility - deprecated
# def wrapper_auth_user(func):
#     """
#     DEPRECATED: Użyj Depends(get_current_user) zamiast tego dekoratora.
#     Pozostawione dla kompatybilności wstecznej.
#     """
#     from functools import wraps
    
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         authorization = kwargs.pop("authorization", None)
#         if not authorization or not authorization.startswith("Bearer "):
#             logger.warning("Invalid token format")
#             raise HTTPException(status_code=401, detail="Invalid token format")
        
#         token = authorization.split(" ")[1]
#         payload = verify_token(token)
#         if not payload:
#             logger.warning("Invalid or expired token")
#             raise HTTPException(status_code=401, detail="Invalid or expired token")
        
#         return await func(*args, **kwargs)
    
#     return wrapper