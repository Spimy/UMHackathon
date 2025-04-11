from typing import Generator, Annotated
from fastapi import Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://devuser:devpassword@localhost:5432/umhackathon"

# Create a connection engine to the database
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    # Create the tables in the database
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionDep = Annotated[Session, Depends(get_session)]
