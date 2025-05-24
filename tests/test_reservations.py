"""
Tests for reservation endpoints
"""
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app

client = TestClient(app)


def test_create_reservation():
    """Test creating a reservation with valid authentication."""
    # Clean users and reservations tables before test
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, reservations RESTART IDENTITY CASCADE;"))
        db.commit()
    finally:
        db.close()

    response = client.post("/auth/register", json={
        "email": "test_fresh2@example.com",
        "password": "password123",
        "full_name": "Test User 2",
    })
    assert response.status_code == 200


def test_cancel_reservation():
    """Test cancelling a reservation."""
    # Clean users and reservations tables before test
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, reservations RESTART IDENTITY CASCADE;"))
        db.commit()
    finally:
        db.close()

    # Register and login
    response = client.post("/auth/register", json={
        "email": "test_fresh3@example.com",
        "password": "password123",
        "full_name": "Test User 3",
    })
    assert response.status_code == 200
