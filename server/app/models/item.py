from sqlmodel import SQLModel, Field
from typing import Optional

class Item(SQLModel, table=True):
    item_id: Optional[int] = Field(default=None, primary_key=True)
    cuisine_tag: str
    item_name: str
    item_price: float
    merchant_id: str
