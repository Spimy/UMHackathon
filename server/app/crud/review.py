from sqlmodel import select
from models.review import Review
from models import SessionDep


def create_review(session: SessionDep, review_data: dict):
    db_review = Review(**review_data)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def get_reviews(session: SessionDep, skip: int = 0, limit: int = 10):
    return session.execute(select(Review).offset(skip).limit(limit)).all()

def get_reviews_by_merchant(session: SessionDep, merchant_id: str) -> list[Review]:
    statement = select(Review).where(Review.merchant_id == merchant_id)
    return session.execute(statement).scalars().all()