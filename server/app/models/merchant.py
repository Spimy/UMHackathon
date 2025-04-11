from sqlmodel import SQLModel, Field
from typing import Optional

class Merchant(SQLModel, table=True):
    merchant_id: Optional[str] = Field(default=None, primary_key=True)
    merchant_name: str
    join_date: str
    city_id: int
