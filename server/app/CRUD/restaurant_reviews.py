from sqlmodel import Session
from app.models.restaurant_review import RestaurantReview

def create_review(db: Session, review_data: dict):
    db_review = RestaurantReview(**review_data)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(RestaurantReview).offset(skip).limit(limit).all()
