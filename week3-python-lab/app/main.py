from fastapi import FastAPI
from app.routes import books, ai

app = FastAPI(
    title="Book Management API",
    description="An API for managing books and integrating with OpenAI",
    version="1.0.0",
)

# Include routes
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])
