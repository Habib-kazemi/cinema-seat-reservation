"""Tests for authentication endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app

client = TestClient(app)

def test_register_and_login():
    """Test user registration and login flow."""
    # Clean users and reservations tables before test
    db = next(get_db())  # Get a database session
    try:
        db.execute(text("TRUNCATE users, reservations RESTART IDENTITY CASCADE;"))
        db.commit()
    finally:
        db.close()

    response = client.post("/api/auth/register", json={
        "email": "test_fresh1@example.com",
        "password": "password123",
        "full_name": "Test User",
    })
    print(response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["email"] == "test_fresh1@example.com"

    response = client.post("/api/auth/login", json={
        "email": "test_fresh1@example.com",
        "password": "password123",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_unauthorized_reservation():
    """Test accessing reservation endpoint without authentication."""
    response = client.post("/api/reservations/", json={
        "user_id": 1,
        "showtime_id": 1,
        "seat_number": "A12",
    })
    assert response.status_code == 401