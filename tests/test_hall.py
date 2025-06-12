"""
Tests for hall endpoints
"""
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import Hall, Cinema, User
from src.schemas import HallCreate

client = TestClient(app)


def test_create_hall_as_admin():
    """Test creating a hall as an admin."""
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, cinema, hall RESTART IDENTITY CASCADE;"))
        db.commit()

        # Register an admin user
        register_response = client.post("/auth/register", json={
            "email": "admin6@example.com",
            "password": "password123",
            "full_name": "Admin User 6",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        db_user = db.query(User).filter(
            User.email == "admin6@example.com").first()
        assert db_user.role == "ADMIN"

        # Create a cinema for hall association
        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()
        db.refresh(db_cinema)

        # Login to get admin token
        login_response = client.post("/auth/login", data={
            "username": "admin6@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Create a hall
        hall_data = HallCreate(name="Hall 1", rows=10,
                               columns=20, cinema_id=db_cinema.id)
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/admin/hall", json=hall_data.model_dump(), headers=headers)
        assert response.status_code == 201
        assert response.json()["name"] == "Hall 1"
        assert response.json()["cinema_id"] == db_cinema.id
    finally:
        db.close()


def test_get_hall():
    """Test getting list of hall."""
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, cinema, hall RESTART IDENTITY CASCADE;"))
        db.commit()

        # Add a cinema
        db_cinema = Cinema(name="Existing Cinema", address="Existing Address")
        db.add(db_cinema)
        db.commit()
        db.refresh(db_cinema)

        # Add a hall
        db_hall = Hall(name="Hall 2", rows=15,
                       columns=25, cinema_id=db_cinema.id)
        db.add(db_hall)
        db.commit()

        # Register an admin user
        register_response = client.post("/auth/register", json={
            "email": "admin7@example.com",
            "password": "password123",
            "full_name": "Admin User 7",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        db_user = db.query(User).filter(
            User.email == "admin7@example.com").first()
        assert db_user.role == "ADMIN"  # چک کردن نقش

        # Login to get admin token
        login_response = client.post("/auth/login", data={
            "username": "admin7@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Get hall
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/admin/hall", headers=headers)  # اصلاح URL
        assert response.status_code == 200
        hall = response.json()
        assert len(hall) >= 1
        assert any(h["name"] == "Hall 2" and h["cinema_id"]
                   == db_cinema.id for h in hall)
    finally:
        db.close()
