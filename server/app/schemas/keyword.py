from pydantic import BaseModel

class KeywordBase(BaseModel):
    keyword: str
    view: int
    menu: int
    checkout: int
    order: int

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: int

    class Config:
        orm_mode = True
