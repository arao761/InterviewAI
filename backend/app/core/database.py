"""
Database configuration and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Fix Render's postgres:// URL to postgresql:// for SQLAlchemy 2.0 compatibility
database_url = settings.DATABASE_URL
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Create database engine with different settings for SQLite vs PostgreSQL
if database_url.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        echo=settings.DEBUG,
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        echo=settings.DEBUG,
        pool_size=5,
        max_overflow=10,
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    
    Usage:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()