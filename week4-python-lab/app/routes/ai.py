from fastapi import APIRouter, HTTPException, Path, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.book import BookResponse
from app.services.book_service import BookService
from app.db.db import SessionLocal
import openai
import os

load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Ensure it is set in the .env file.")

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/recommendation/{book_id}", response_model=dict)
def introduce_book(book_id: int = Path(..., title="The ID of the book to introduce"), db: Session = Depends(get_db)):
    """
    Generate an introduction for a book using OpenAI's text-generation API.
    """
    # Get the book details from the database
    service = BookService(db)
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Construct a prompt for OpenAI
    prompt = (
        f"Introduce the book '{book.title}' by {book.author}, published in {book.year}. "
        f"Here is the description: {book.description or 'No description available'}."
    )

    # Call OpenAI API
    try:
        openai.api_key = openai_api_key

        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150
        )
        introduction = response.choices[0].text.strip()
        return {
            "book_id": book_id,
            "introduction": introduction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
