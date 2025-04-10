from sqlmodel import SQLModel, Field
from typing import Optional

class Keyword(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword: str
    view: int
    menu: int
    checkout: int
    order: int
