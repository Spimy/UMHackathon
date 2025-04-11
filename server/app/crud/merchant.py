from sqlmodel import Session
from app.models.merchant import Merchant


def create_merchant(db: Session, merchant_data: dict):
    db_merchant = Merchant(**merchant_data)
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant


def get_merchants(db: Session, skip: int = 0, limit: int = 10):
    return db.exec(Merchant).offset(skip).limit(limit).all()
