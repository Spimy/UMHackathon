from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://username:password@localhost/dbname"

# Create a connection engine to the database
engine = create_engine(DATABASE_URL, echo=True)

# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database
def create_db():
    SQLModel.metadata.create_all(bind=engine)
