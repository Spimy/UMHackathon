from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from models import item, merchant, restaurant_review, keyword

DATABASE_URL = "postgresql://postgres:abcd1234@localhost:5432/UMHack"

# Create a connection engine to the database
engine = create_engine(DATABASE_URL, echo=True)

# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database
def create_db():
    SQLModel.metadata.create_all(bind=engine)
