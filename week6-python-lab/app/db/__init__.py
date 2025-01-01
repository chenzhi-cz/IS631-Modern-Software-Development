from app.db.db import Base, engine

# Initialize the database schema
def init_db():
    import app.models.book  # Import here to avoid circular import
    Base.metadata.create_all(bind=engine)


