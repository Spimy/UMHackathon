from sqlmodel import select
from models.keyword import Keyword
from models import SessionDep


def create_keyword(session: SessionDep, keyword_data: dict):
    db_keyword = Keyword(**keyword_data)
    session.add(db_keyword)
    session.commit()
    session.refresh(db_keyword)
    return db_keyword


def get_keywords(session: SessionDep, skip: int = 0, limit: int = 10):
    return session.execute(select(Keyword).offset(skip).limit(limit)).all()


def get_keywords_by_category(session: SessionDep):
    categories = ["view", "menu", "checkout", "order"]
    result = {}
    for category in categories:
        sorted_keywords = session.execute(
            select(Keyword.keyword, getattr(Keyword, category).label("category"))
            .order_by(getattr(Keyword, category).desc())
        ).all()
        result[category] = [{"keyword": k.keyword, "category": k.category} for k in sorted_keywords]
    return result

