from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine, select
from models.models import *

app = FastAPI()

engine = create_engine("postgresql://yuvi:yuvi@localhost:5432/limeratsnake")
SQLModel.metadata.create_all(engine)


def create_all():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_all()


@app.get("/users/", response_model=list[User])
def list_Users():
    with Session(engine) as session:
        users = session.query(User).all()
        return users


@app.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate):
    with Session(engine) as session:
        user_db = User.model_validate(user)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
