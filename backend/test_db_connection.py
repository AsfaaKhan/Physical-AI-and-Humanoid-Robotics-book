"""Test database connection."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config.settings import settings
from src.database.database import engine, Base
from sqlalchemy import inspect

def test_db_connection():
    try:
        print(f"Testing database connection to: {settings.DATABASE_URL}")

        # Test the connection by getting inspector
        inspector = inspect(engine)

        # Try to connect and list tables
        tables = inspector.get_table_names()
        print(f"Connected successfully! Found {len(tables)} tables: {tables}")

        # Try to create tables if they don't exist
        print("Creating tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")

        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_db_connection()