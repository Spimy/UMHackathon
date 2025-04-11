from fastapi import APIRouter, Depends
from sqlmodel import Session
import crud
import schemas
from models import get_db

router = APIRouter(tags=["items"])


@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item.dict())


@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return
    # return crud.get_items(db, skip=skip, limit=limit)
