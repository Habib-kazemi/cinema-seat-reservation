"""
Tests for authentication and authorization endpoints
"""
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import Showtime, Hall, Movie, User, Cinema

client = TestClient(app)


def test_register_and_login():
    """Test user registration and login flow."""
    # Clean users and reservations tables before test
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, reservation RESTART IDENTITY CASCADE;"))
        db.commit()

        # Register a regular user
        response = client.post("/auth/register", json={
            "email": "test_fresh1@example.com",
            "password": "password123",
            "full_name": "Test User",
            "phone_number": "1234567890"
        })
        assert response.status_code == 201
        assert "User with id" in response.json()["message"]

        # Login with regular user
        login_response = client.post("/auth/login", data={
            "username": "test_fresh1@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        assert token is not None
    finally:
        db.close()


def test_register_admin_and_login():
    """Test registering an admin and login flow."""
    # Clean users table before test
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users RESTART IDENTITY CASCADE;"))
        db.commit()

        # Register an admin user
        response = client.post("/auth/register", json={
            "email": "admin@test.com",
            "password": "admin123",
            "full_name": "Admin Test",
            "role": "ADMIN",
            "phone_number": "9876543210"
        })
        assert response.status_code == 201
        assert "User with id" in response.json()["message"]

        # Verify role in database
        db_user = db.query(User).filter(User.email == "admin@test.com").first()
        assert db_user.role == "ADMIN"

        # Login with admin user
        login_response = client.post("/auth/login", data={
            "username": "admin@test.com",
            "password": "admin123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        assert token is not None

        # Decode token to check role (manual check, requires jwt library)
        # Note: This is a placeholder; actual decoding needs jwt library
        # import jwt; payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"]); print(payload["role"])
    finally:
        db.close()


def test_unauthorized_reservation():
    """Test accessing reservation endpoint without authentication."""
    db = next(get_db())
    try:
        db.execute(text(
            "TRUNCATE reservation, showtime, hall, movie, cinema RESTART IDENTITY CASCADE;"))
        db.commit()

        # Add a cinema
        cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(cinema)
        db.commit()
        db.refresh(cinema)

        # Add a movie
        movie = Movie(
            title="Test Movie",
            genre_id=1,
            duration=120,
            release_date=datetime.now().date()
        )
        db.add(movie)

        # Add a hall
        hall = Hall(name="Hall 1", rows=10, columns=20, cinema_id=cinema.id)
        db.add(hall)

        # Add a showtime
        showtime = Showtime(
            movie_id=movie.id,
            hall_id=hall.id,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=2),
            price=15.50
        )
        db.add(showtime)
        db.commit()
        db.refresh(showtime)

        # Test unauthorized reservation
        response = client.post("/reservation/", json={
            "showtime_id": showtime.id,
            "seat_number": "A12"
        })
        assert response.status_code == 401
    finally:
        db.close()
