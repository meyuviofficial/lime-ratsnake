from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int | None = None
    email: str


class UserCreate(SQLModel):
    name: str
    age: int | None = None
    email: str


class UserPublic(SQLModel):
    name: str
    age: int | None = None
