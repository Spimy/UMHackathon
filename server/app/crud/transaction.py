from datetime import datetime, timedelta
from sqlmodel import select, func
from sqlalchemy import cast, Date
from models.transaction import TransactionData, TransactionItems
from models import SessionDep

def get_merchant_transactions_summary(session: SessionDep, merchant_id: str):
    today = datetime(2023, datetime.utcnow().month, datetime.utcnow().day).date()  # Set year to 2023
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    def get_summary(start_date):
        return session.execute(
            select(
                TransactionItems.item_id,
                func.count(TransactionItems.item_id).label("frequency"),
                func.sum(TransactionData.order_value).label("total_value")
            )
            .join(TransactionData, TransactionItems.order_id == TransactionData.order_id)
            .where(
                TransactionItems.merchant_id == merchant_id,
                cast(TransactionData.order_time, Date) >= start_date
            )
            .group_by(TransactionItems.item_id)
        ).all()

    return {
        "today": get_summary(today),
        "this_week": get_summary(start_of_week),
        "this_month": get_summary(start_of_month),
    }


