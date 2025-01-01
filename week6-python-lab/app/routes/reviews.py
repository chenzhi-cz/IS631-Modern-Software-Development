from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session

from app.db.db import SessionLocal
from app.models.review import ReviewCreate, ReviewResponse
from app.services.review_service import ReviewService
from app.models.book import Book
from app.models.review import Review
from app.services.cognito_service import CognitoService, bearer_scheme, CognitoUserRole

router = APIRouter()

cognito_service = CognitoService()


# 1) Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2) Dependency to get a ReviewService instance
def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
    return ReviewService(db)

@router.get("/books/{book_id}/reviews", response_model=list[ReviewResponse])
def get_reviews(
    book_id: int,
    service: ReviewService = Depends(get_review_service)
):
    reviews = service.get_reviews_by_book_id(book_id)
    if not reviews:
        raise HTTPException(status_code=404, detail=f"No reviews found for book {book_id}")
    return reviews

@router.post("/books/{book_id}/reviews", response_model=ReviewResponse)
def add_review(
    book_id: int,
    review: ReviewCreate,
    token: str = Security(bearer_scheme),
    service: ReviewService = Depends(get_review_service),
):
    # Decode and validate the access token
    claims = cognito_service.decode_token(token.credentials)
    cognito_service.check_user_role(claims, CognitoUserRole)

    # Proceed with adding the review
    new_review = service.add_review(book_id, review)
    if not new_review:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return new_review

@router.put("/books/{book_id}/reviews/{review_id}", response_model=ReviewResponse)
def update_review(
    book_id: int,
    review_id: int,
    new_review: ReviewCreate,
    service: ReviewService = Depends(get_review_service),
):
    updated_review = service.update_review(book_id, review_id, new_review)
    if not updated_review:
        raise HTTPException(status_code=404, detail=f"Review with id {review_id} for book {book_id} not found")
    return updated_review

@router.delete("/books/{book_id}/reviews/{review_id}")
def delete_review(
    book_id: int,
    review_id: int,
    service: ReviewService = Depends(get_review_service),
):
    success = service.delete_review(book_id, review_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Review with id {review_id} for book {book_id} not found")
    return {"message": "Review deleted successfully"}
