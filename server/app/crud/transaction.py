from datetime import datetime, timedelta
from sqlmodel import select, func
from sqlalchemy import cast, Date
from models.transaction import TransactionData, TransactionItems
from models.item import Item
from models import SessionDep


def get_merchant_transactions_summary(session: SessionDep, merchant_id: str):
    today = datetime(2023, datetime.utcnow().month,
                     datetime.utcnow().day).date()  # Set year to 2023
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    def get_summary(start_date):
        final = []

        summaries = session.execute(
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

        for row in summaries:
            (item_id, frequency, total_value) = row
            item = session.execute(select(Item.item_name).where(
                Item.item_id == item_id)).first()

            final.append({
                'item_id': item_id,
                'item_name': item[0],
                'frequency': frequency,
                'total_value': total_value,
            })

        return final

    return {
        "today": get_summary(today),
        "this_week": get_summary(start_of_week),
        "this_month": get_summary(start_of_month),
    }
