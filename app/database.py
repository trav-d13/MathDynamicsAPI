from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncSession
import os
from sqlmodel import SQLModel, Field
import secrets

from app.models import CreateUser


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

async def create_user(session: Session, user_data: CreateUser):
    pass



class User(SQLModel, table=True):
    user_id: int|None = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": False, "nullable": False, "index": False})
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False, "index": True})
    location: str = Field(nullable=False)
    api_key: str | None = Field(default=None, index=True, sa_column_kwargs={"unique": True})

    @classmethod
    def generate_api_key(cls):
        return secrets.token_urlsafe(32)