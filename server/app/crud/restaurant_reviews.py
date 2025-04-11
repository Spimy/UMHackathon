from sqlmodel import select
from models.restaurant_review import RestaurantReview
from models import SessionDep


def create_review(session: SessionDep, review_data: dict):
    db_review = RestaurantReview(**review_data)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


def get_reviews(session: SessionDep, skip: int = 0, limit: int = 10):
    return session.execute(select(RestaurantReview).offset(skip).limit(limit)).all()
