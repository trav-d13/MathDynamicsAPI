from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncSession
import os
from sqlmodel import SQLModel, Field
import secrets

from app.models import CreateUser
from sqlalchemy.future import select


async_engine: AsyncEngine = create_async_engine(
    os.getenv('DB_URI'),
    echo=True,
    future=True
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def fetch_or_create_user_key(session: Session, user_data: CreateUser):
    result = await session.execute(select(User).where(User.email == user_data.email))  # Query to check if the user already exists
    existing_user = result.scalars().first()

    if existing_user:
        return existing_user.api_key  # Return the existing user id if found
    else:  # If the user does not exist, create a new user
        new_user = User(name=user_data.name,
                        email=user_data.email,
                        location=user_data.country,
                        api_key=User.generate_api_key())
        session.add(new_user)
        await session.commit()  # save changes to the database
        return new_user.api_key  # Return the api key



class User(SQLModel, table=True):
    user_id: int|None = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": False, "nullable": False, "index": False})
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False, "index": True})
    location: str = Field(nullable=False)
    api_key: str | None = Field(default=None, index=True, sa_column_kwargs={"unique": True})

    @classmethod
    def generate_api_key(cls):
        return secrets.token_urlsafe(32)