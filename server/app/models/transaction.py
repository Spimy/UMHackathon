from sqlmodel import SQLModel, Field
from typing import Optional

class TransactionItems(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: str
    item_id: str
    merchant_id: str

class TransactionData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: str
    order_time: str
    driver_arrival_time: str
    driver_pickup_time: str
    delivery_time: str
    order_value: float
    eater_id: str
    merchant_id: str
