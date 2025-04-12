from typing import Generator, Annotated
from fastapi import Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel, create_engine, select
from sqlalchemy.orm import sessionmaker
import pandas as pd
from pathlib import Path
from .merchant import Merchant, User
from .keyword import Keyword
from .item import Item
from .review import Review
from .transaction import TransactionData, TransactionItems
from settings import DATABASE_URI

# Create a connection engine to the database
engine = create_engine(DATABASE_URI, echo=True)


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
                    item_id=row['item_id'],
                    cuisine_tag=row['cuisine_tag'],
                    item_name=row['item_name'],
                    item_price=row['item_price'],
                    merchant_id=row['merchant_id']
                )
                session.add(item)

        # Check and populate reviews
        if session.execute(select(Review)).first() is None:
            reviews_df = pd.read_csv(dataset_path / "reviews.csv")
            for _, row in reviews_df.iterrows():
                review = Review(
                    merchant_id=row['merchant_id'],
                    rating=row['rating'],
                    review=row['review']
                )
                session.add(review)

        # Check and populate transactionsData
        if session.execute(select(TransactionData)).first() is None:
            transactionData_df = pd.read_csv(
                dataset_path / "transaction_data.csv")
            for _, row in transactionData_df.iterrows():
                try:
                    transactionData = TransactionData(
                        order_id=row['order_id'],
                        order_time=row['order_time'],
                        driver_arrival_time=row['driver_arrival_time'],
                        driver_pickup_time=row['driver_pickup_time'],
                        delivery_time=row['delivery_time'],
                        order_value=row['order_value'],
                        eater_id=row['eater_id'],
                        merchant_id=row['merchant_id']
                    )
                    session.add(transactionData)
                except Exception as e:
                    print(f"Error adding transaction data: {e}")
                    continue

        # Check and populate transactionsItems
        if session.execute(select(TransactionItems)).first() is None:
            transactionItems_df = pd.read_csv(
                dataset_path / "transaction_items.csv")
            for _, row in transactionItems_df.iterrows():
                try:
                    transactionItem = TransactionItems(
                        order_id=row['order_id'],
                        item_id=row['item_id'],
                        merchant_id=row['merchant_id']
                    )
                    session.add(transactionItem)
                except Exception as e:
                    print(f"Error adding transaction data: {e}")
                    continue

        # ! Hard coded to associate an email with a merchant
        if session.execute(select(User)).first() is None:
            users = {
                'williamlaw.3001@gmail.com': '7d4e1',
                'justinyww@gmail.com': '6a0c3',
                'alexcheekh@gmail.com': '7f2c1',
                'jb.brubusiness3@gmail.com': '5c1f8'
            }

            for email, merchant_id in users.items():
                user = User(
                    user_email=email,
                    merchant_id=merchant_id
                )
                session.add(user)

        # Commit all changes
        session.commit()


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# Create the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionDep = Annotated[Session, Depends(get_session)]
