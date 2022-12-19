from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    title: str
    url: str
    description: str
    category: str
    icon: Optional[str]


class ItemLink(BaseModel):
    url: str

class GroupLink(BaseModel):
    url: str
    title: str 
