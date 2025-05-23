"""Tests for reservation endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app

client = TestClient(app)

def test_create_reservation():
    """Test creating a reservation with valid authentication."""
    # Clean users and reservations tables before test
    db = next(get_db())  # Get a database session
    try:
        db.execute(text("TRUNCATE users, reservations RESTART IDENTITY CASCADE;"))
        db.commit()
    finally:
        db.close()

    response = client.post("/api/auth/register", json={
        "email": "test_fresh2@example.com",
        "password": "password123",
        "full_name": "Test User 2",
    })
    assert response.status_code == 200

    login_response = client.post("/api/auth/login", json={
        "email": "test_fresh2@example.com",
        "password": "password123",
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post("/api/reservations/", json={
        "user_id": 1,  # Assumes user_id=1 from registration
        "showtime_id": 1,  # Assumes showtime_id=1 exists
        "seat_number": "A12",
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Reservation created successfully"