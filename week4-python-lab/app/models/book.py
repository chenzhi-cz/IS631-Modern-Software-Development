from sqlalchemy import Column, Integer, String
from app.db.db import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    # Relationship with reviews
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

# Pydantic Models for Request/Response
class BookBase(BaseModel):
    title: str
    author: str
    year: int
    description: str | None = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
