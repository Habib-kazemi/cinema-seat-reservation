"""
Tests for admin endpoints
"""
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app

client = TestClient(app)


def test_create_movie_as_admin():
    """Test creating a movie as an admin."""
    # Clean users and movies tables before test
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, movies RESTART IDENTITY CASCADE;"))
        db.commit()
    finally:
        db.close()

    # Register an admin user
    response = client.post("/auth/register", json={
        "email": "admin@example.com",
        "password": "password123",
        "full_name": "Admin User",
    })
    assert response.status_code == 200
