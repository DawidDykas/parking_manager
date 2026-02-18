from app.api.modules.database import user_session
def user_session_wrapper(func):
    async def wrapper(*args, **kwargs):
        async with user_session() as session:
            async with session.begin():
                return await func(session, *args, **kwargs)
    return wrapper