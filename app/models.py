from sqlmodel import SQLModel, Field
import secrets

class User(SQLModel, table=True):
    user_id: int|None = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": False, "nullable": False, "index": False})
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False, "index": True})
    location: str = Field(nullable=False)
    api_key: str | None = Field(default=None, index=True, sa_column_kwargs={"unique": True})

    @classmethod
    def generate_api_key(cls):
        return secrets.token_urlsafe(32)

