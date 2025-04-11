from sqlalchemy.orm import sessionmaker, Session
from app import engine  
from app.models import item, merchant, restaurant_review, keyword 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
