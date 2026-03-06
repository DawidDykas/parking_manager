import asyncio
from functools import wraps
from app.api.modules.database import sessionmaker
from log_config.logger_config import logger


def with_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with sessionmaker() as session:
            async with session.begin():
                return await func(session, *args, **kwargs)

    return wrapper