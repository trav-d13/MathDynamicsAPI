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
    """
    Initialize the database asynchronously by creating all defined tables.
    
    This function should be called when the application starts to ensure all necessary database tables exist.
    It uses the global `async_engine` created with SQLAlchemy's `create_async_engine`.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """
    Create and provide an asynchronous session context manager for database operations.

    Yields:
        AsyncSession: An instance of AsyncSession that is used for performing database transactions.

    This function is intended to be used as a dependency in FastAPI path operations to provide a session for each request.
    """
    async_session = sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def fetch_or_create_user_key(session: Session, user_data: CreateUser):
    """
    Fetch an existing user's API key or create a new user with a new API key if not found.

    Parameters:
        session (Session): The database session to execute the query within.
        user_data (CreateUser): A CreateUser instance containing the new user's data.

    Returns:
        str: The API key of the existing or newly created user.

    This function checks if a user exists with the given email address. If found, returns their API key;
    otherwise, creates a new user with a generated API key.
    """
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
    """
    Represents a User in the database.

    Attributes:
        user_id (int): The unique identifier for a user, automatically generated.
        name (str): The name of the user.
        email (str): The user's email address, must be unique.
        location (str): The user's location.
        api_key (str, optional): A unique API key for the user, used for authentication.

    Methods:
        generate_api_key: Class method to generate a new, secure API key.
    """
    user_id: int|None = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": False, "nullable": False, "index": False})
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False, "index": True})
    location: str = Field(nullable=False)
    api_key: str | None = Field(default=None, index=True, sa_column_kwargs={"unique": True})

    @classmethod
    def generate_api_key(cls):
        """
        Generate a new secure API key using Python's secrets module.

        Returns:
            str: A newly generated URL-safe API key.
        """
        return secrets.token_urlsafe(32)