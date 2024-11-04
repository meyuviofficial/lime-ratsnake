from sqlmodel import SQLModel, create_engine

engine = create_engine("postgresql://yuvi:yuvi@localhost:5432/limeratsnake")
SQLModel.metadata.create_all(engine)

