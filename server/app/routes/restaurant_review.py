from fastapi import APIRouter, Depends
from sqlmodel import Session
import crud
import schemas
from models import get_session

router = APIRouter(tags=["restaurant_reviews"])


@router.post("/reviews/", response_model=schemas.RestaurantReview)
def create_review(review: schemas.RestaurantReviewCreate, db: Session = Depends(get_session)):
    return crud.create_review(db, review.dict())


@router.get("/reviews/", response_model=list[schemas.RestaurantReview])
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    return crud.get_reviews(db, skip=skip, limit=limit)
