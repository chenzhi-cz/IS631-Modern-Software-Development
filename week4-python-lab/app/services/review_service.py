from sqlalchemy.orm import Session
from app.models.review import Review, ReviewCreate
from app.models.book import Book

class ReviewService:
    def __init__(self, db: Session):
        self.db = db

    def get_reviews_by_book_id(self, book_id: int):
        return self.db.query(Review).filter(Review.book_id == book_id).all()

    def add_review(self, book_id: int, review_data: ReviewCreate):
        # Check if the book exists
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            return None
        # Add the review
        new_review = Review(book_id=book_id, **review_data.dict())
        self.db.add(new_review)
        self.db.commit()
        self.db.refresh(new_review)
        return new_review

    def delete_review(self, book_id: int, review_id: int):
        review = self.db.query(Review).filter(Review.id == review_id, Review.book_id == book_id).first()
        if not review:
            return None
        self.db.delete(review)
        self.db.commit()
        return True