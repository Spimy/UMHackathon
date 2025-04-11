from fastapi import APIRouter, Depends
from sqlmodel import Session
from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()

@router.post("/merchants/", response_model=schemas.Merchant)
def create_merchant(merchant: schemas.MerchantCreate, db: Session = Depends(get_db)):
    return crud.create_merchant(db, merchant.dict())

@router.get("/merchants/", response_model=list[schemas.Merchant])
def read_merchants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_merchants(db, skip=skip, limit=limit)
