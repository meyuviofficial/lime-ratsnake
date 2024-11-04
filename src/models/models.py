from typing import Optional
from sqlmodel import Field, SQLModel, Column, func
from datetime import UTC, datetime
from sqlalchemy import DateTime


class UserBase(SQLModel):
    # created_at: datetime = Field(default=datetime.now, nullable=False)
    # updated_at: Optional[datetime] = Field(
    #     default_factory=lambda: datetime.now,
    #     sa_column_kwargs={"onupdate": datetime.now},
    # )
    name: str = Field(index=True)
    age: int | None = None
    email: str = Field(sa_column_kwargs={"unique": True}, primary_key=True)


class User(UserBase, table=True):
    password_hash: str = Field()


class UserCreateOrUpdate(UserBase):
    password: str


class UserPublic(UserBase):
    email: str


class UserLogin(UserBase):
    password: str
    email: str
