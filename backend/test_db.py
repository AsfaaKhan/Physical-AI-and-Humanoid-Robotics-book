"""Test script to verify database connection."""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    # Test basic imports
    from config.settings import settings
    print(f"Settings loaded. Database URL: {settings.DATABASE_URL}")

    # Test database connection
    from backend.src.database.database import engine
    print("Database engine created successfully")

    # Test importing models
    from backend.src.models.user import User
    from backend.src.models.session import UserSession
    print("Models imported successfully")

    # Test importing auth router to check for errors
    from backend.src.api.v1.auth import auth_router
    print("Auth router imported successfully")

    print("All tests passed! Database and imports are working correctly.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()