from fastapi import APIRouter, HTTPException, Path, Depends
from dotenv import load_dotenv
from app.services.book_service import BookService
import openai
import os

load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Ensure it is set in the .env file.")

router = APIRouter()

book_service = BookService()  # Use the updated BookService with preloaded books


@router.get("/recommendation/{book_id}", response_model=dict)
def introduce_book(book_id: int):
    """
    Generate an introduction for a book using OpenAI API.
    """
    # Fetch the book from the in-memory store
    book = book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Construct a prompt for OpenAI
    prompt = (
        f"Introduce the book '{book['title']}' by {book['author']}, published in {book['year']}. "
        f"Here is the description: {book.get('description', 'No description available')}."
    )

    # Call OpenAI API
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150,
            temperature=0.6
        )
        introduction = response.choices[0].text.strip()
        return {"book_id": book_id, "introduction": introduction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
