from sqlmodel import SQLModel, Field
from typing import Optional

class Transactions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: str
    merchant_id: str
    order_time:str
    order_value: float
