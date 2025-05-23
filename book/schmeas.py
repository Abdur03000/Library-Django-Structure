from pydantic import BaseModel, HttpUrl
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None


class BookCreate(BookBase):
    cover_image: Optional[str]


class BookUpdate(BookBase):
    cover_image: Optional[str]


class Book(BookBase):
    id: int
    cover_image: Optional[str]

    model_config = {
        "from_attributes": True
    }
