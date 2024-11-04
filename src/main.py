from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine, select
from models.models import User, UserPublic, UserCreateOrUpdate, UserLogin
from classes.passwords import Password
from pydantic import ValidationError
from contextlib import asynccontextmanager

app = FastAPI()
_passwords = Password()
engine = create_engine("postgresql://yuvi:yuvi@localhost:5432/lrsmaster")
SQLModel.metadata.create_all(engine)


def create_all():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def on_startup(app: FastAPI):
    create_all()
    yield


@app.get("/users/list", response_model=list[UserPublic])
def list_Users():
    with Session(engine) as session:
        users = session.query(User).all()
        return users


@app.post("/users/create", response_model=UserPublic)
def create_user(user: UserCreateOrUpdate):
    hash_value = _passwords.create_secure_password(user.password)
    with Session(engine) as session:
        extra_data = {
            "password_hash": hash_value,
        }
        # print("Extra data: ", extra_data)
        try:
            user_db = User.model_validate(user, update=extra_data)
            session.add(user_db)
            session.commit()
            session.refresh(user_db)
            return user_db
        except ValidationError as e:
            return {"error": str(e)}


@app.get("/users/get/", response_model=UserPublic)
def get_user(email: str):
    with Session(engine) as session:
        user = session.get(User, email)
        return user


@app.delete("/users/delete/")
def delete_user(email: str):
    with Session(engine) as session:
        user = session.get(User, email)
        session.delete(user)
        session.commit()
        return {"message": "User deleted successfully"}


@app.post("/users/login/", response_model=bool)
def login_user(user: UserLogin):
    with Session(engine) as session:
        statement = select(User).where(User.email == user.email)
        user_db = session.exec(statement).first()
        if user_db is None:
            print("User not found")
            return {"error": "User not found"}

        return _passwords.verify_password(user.password, user_db.password_hash)

# TODO: For some reason, update function is not working ! Needs to be checked. 
# @app.put("/users/update/", response_model=UserPublic)
# def update_user(user: UserCreateOrUpdate):
#     with Session(engine) as session:
#         statement = select(User).where(User.email == user.email)
#         user_db = session.exec(statement).first()
#         if user_db is None:
#             print("User not found")
#             return {"error": "User not found"}

#         hash_value = _passwords.create_secure_password(user.password)
#         extra_data = {
#             "password_hash": hash_value,
#         }
#         user_db = User.model_validate(user, update=extra_data)

#         session.add(user_db)
#         session.commit()
#         session.refresh(user_db)
#         return user_db
