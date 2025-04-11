from sqlmodel import Session
from app.models.keyword import Keyword


def create_keyword(db: Session, keyword_data: dict):
    db_keyword = Keyword(**keyword_data)
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword


def get_keywords(db: Session, skip: int = 0, limit: int = 10):
    return db.exec(Keyword).offset(skip).limit(limit).all()
