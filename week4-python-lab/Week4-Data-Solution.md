# Lab: Week 4 – Data Solution

## Solution to Activity 2
### In app/routes/reviews.py
```python
# Activity 2: Solution
@router.put("/books/{book_id}/reviews/{review_id}", response_model=ReviewResponse)
def update_review(book_id: int, review_id: int, new_review: ReviewCreate, service: ReviewService = Depends(get_review_service)):
    updated_review = service.update_review(book_id, review_id, new_review)
    if not updated_review:
        raise HTTPException(status_code=404, detail=f"Review with id {review_id} for book {book_id} not found")
    return updated_review
```
### In app/services/review_service.py
```python
# Activity 2: Solution
def update_review(self, book_id: int, review_id: int, new_review_data: ReviewCreate):
    # Check if the book exists
    book = self.db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    # Update the review
    review = self.db.query(Review).filter(Review.id == review_id, Review.book_id == book_id).first()
    if not review:
        return None
    review.review = new_review_data.review
    self.db.commit()
    return review
```

