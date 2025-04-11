from typing import Generator, Annotated
from fastapi import Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel, create_engine, select
from sqlalchemy.orm import sessionmaker
import pandas as pd
from pathlib import Path
from .merchant import Merchant
from .keyword import Keyword
from .item import Item
from .restaurant_review import RestaurantReview

DATABASE_URL = "postgresql://devuser:devpassword@localhost:5432/umhackathon"

# Create a connection engine to the database
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    # Create the tables in the database
    SQLModel.metadata.create_all(engine)


def populate_database():
    """
    Populate the database tables from CSV files in the _dataset directory only if they are empty
    """
    dataset_path = Path(__file__).parent.parent / "_dataset"

    # Create a session
    with Session(engine) as session:
        # Check and populate merchants
        if session.execute(select(Merchant)).first() is None:
            merchants_df = pd.read_csv(dataset_path / "merchant.csv")
            for _, row in merchants_df.iterrows():
                merchant = Merchant(
                    merchant_id=row['merchant_id'],
                    merchant_name=row['merchant_name'],
                    join_date=row['join_date'],
                    city_id=row['city_id']
                )
                session.add(merchant)

        # Check and populate keywords
        if session.execute(select(Keyword)).first() is None:
            keywords_df = pd.read_csv(dataset_path / "keywords.csv")
            for _, row in keywords_df.iterrows():
                keyword = Keyword(
                    keyword=row['keyword'],
                    view=row['view'],
                    menu=row['menu'],
                    checkout=row['checkout'],
                    order=row['order']
                )
                session.add(keyword)

        # Check and populate items
        if session.execute(select(Item)).first() is None:
            items_df = pd.read_csv(dataset_path / "items.csv")
            for _, row in items_df.iterrows():
                item = Item(
                    cuisine_tag=row['cuisine_tag'],
                    item_name=row['item_name'],
                    item_price=row['item_price'],
                    merchant_id=row['merchant_id']
                )
                session.add(item)

        # Commit all changes
        session.commit()


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionDep = Annotated[Session, Depends(get_session)]
