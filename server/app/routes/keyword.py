from fastapi import APIRouter, Depends
from sqlmodel import Session
import crud
import schemas
from models import get_session

router = APIRouter(tags=["keywords"])


@router.post("/keywords/", response_model=schemas.Keyword)
def create_keyword(keyword: schemas.KeywordCreate, db: Session = Depends(get_session)):
    return crud.create_keyword(db, keyword.dict())


@router.get("/keywords/", response_model=list[schemas.Keyword])
def read_keywords(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    return crud.get_keywords(db, skip=skip, limit=limit)
