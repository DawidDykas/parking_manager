from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    
)

from typing import AsyncIterator
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

async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


engine = get_engine(url = database_settings.url_database)
sessionmaker = get_sessionmaker(engine = engine)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with sessionmaker() as session:
        async with session.begin():  
            try:
                yield session  
            except:
                await session.rollback()
                raise