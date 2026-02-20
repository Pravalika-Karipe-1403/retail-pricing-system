import ssl

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi import Depends
from typing import Annotated
from config import get_settings

settings = get_settings()  # This will initiate the environmental variables and return the values.

#   1)creating engine
swb_engine = create_async_engine(
    'mysql+aiomysql://root:root123@localhost:3306/retail',
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)

#   2)creating Session factory
retail_async_session_factory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=swb_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# FastAPI dependency
async def __get_db_connection():
    async with retail_async_session_factory() as session:
        yield session

session = Annotated[AsyncSession, Depends(__get_db_connection)]


