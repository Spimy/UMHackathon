from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    cuisine_tag: str
    item_name: str
    item_price: float
    merchant_id: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: int

    class Config:
        orm_mode = True
