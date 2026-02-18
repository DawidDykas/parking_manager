from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase
from config.setting import database_settings


def get_engine(url: str):
    return create_async_engine(url, echo=False, future=True)

def get_sessionmaker(engine):
    return async_sessionmaker(bind=engine, 
                              autoflush=False, 
                              autocommit=False, 
                              expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def init_user_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


user_engine = get_engine(url = database_settings.url_database_user)
user_session = get_sessionmaker(engine = user_engine)