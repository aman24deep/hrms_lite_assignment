from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
engine = create_engine(settings.database_url)

# Database session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()


# Dependency to get database session in route handlers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Always close the connection when done
