from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from app.db.db import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    review = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)

    # Relationship with the Book model
    book = relationship("Book", back_populates="reviews")

class ReviewBase(BaseModel):
    review: str

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True
