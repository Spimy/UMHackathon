from pydantic import BaseModel
from typing import Optional

# Base schema for the item data
class ItemBase(BaseModel):
    cuisine_tag: str
    item_name: str
    item_price: float
    merchant_id: str

# Schema for creating a new item
class ItemCreate(ItemBase):
    pass

# Schema for returning an item (with an ID)
class Item(ItemBase):
    item_id: int

    class Config:
        orm_mode = True
