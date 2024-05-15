from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
import os


async_engine: AsyncEngine = create_async_engine(
    os.getenv('DB_URI'),
    echo=True,
    future=True
)

async_session = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    from sqlmodel.ext.asyncio.session import AsyncSession
    async_session = AsyncSession(bind=async_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session