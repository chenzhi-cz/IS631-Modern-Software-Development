from pydantic import BaseModel
from typing import Optional

# Pydantic models for request/response
class BookBase(BaseModel):
    title: str
    author: str
    year: int
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
