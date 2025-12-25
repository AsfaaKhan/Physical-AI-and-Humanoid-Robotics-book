"""Database initialization script to create all tables."""
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path so imports work
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from src.database.database import Base
from src.models.user import User, UserProfile
from src.models.session import UserSession

def init_db():
    """Initialize the database by creating all tables."""
    # Create database engine
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )

    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    # Verify tables were created by checking if we can access them
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables created: {tables}")

    return engine

if __name__ == "__main__":
    init_db()
    print("Database initialization completed!")