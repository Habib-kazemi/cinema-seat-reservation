"""
Tests for cinema endpoints
"""
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import Cinema
from src.schemas import CinemaCreate

client = TestClient(app)


def test_create_cinema_as_admin():
    """Test creating a cinema as an admin."""
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, cinema RESTART IDENTITY CASCADE;"))
        db.commit()

        # Register an admin user
        register_response = client.post("/auth/register", json={
            "email": "admin4@example.com",
            "password": "password123",
            "full_name": "Admin User 4",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        # Login to get admin token
        login_response = client.post("/auth/login", data={
            "username": "admin4@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Create a cinema
        cinema_data = CinemaCreate(name="Test Cinema", address="Test Address")
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/admin/cinema", json=cinema_data.model_dump(), headers=headers)  # تغییر URL
        assert response.status_code == 201
        assert response.json()["name"] == "Test Cinema"
    finally:
        db.close()


def test_get_cinema():
    """Test getting list of cinema."""
    # Clean tables before test
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, cinema RESTART IDENTITY CASCADE;"))
        # Add a cinema
        db_cinema = Cinema(name="Existing Cinema", address="Existing Address")
        db.add(db_cinema)
        db.commit()

        # Register an admin user
        register_response = client.post("/auth/register", json={
            "email": "admin5@example.com",
            "password": "password123",
            "full_name": "Admin User 5",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        # Login to get admin token
        login_response = client.post("/auth/login", data={
            "username": "admin5@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Get cinemas
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/cinema/", headers=headers)
        assert response.status_code == 200
        cinema = response.json()
        assert len(cinema) >= 1
        assert any(c["name"] == "Existing Cinema" for c in cinema)
    finally:
        db.close()
