from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.routes import books, ai, chroma, reviews, auth

security = HTTPBearer()

app = FastAPI(
    title="Book Management API",
    description="An API for managing books and integrating with OpenAI",
    version="1.0.0",
)

# Include routes
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(reviews.router, prefix="", tags=["Reviews"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])
app.include_router(chroma.router, prefix="/chroma", tags=["ChromaDB"])
app.include_router(auth.router, prefix="", tags=["Auth"])

