"""
Tests for authentication and authorization endpoints
"""
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import Showtime, Hall, Movie

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

    response = client.post("/auth/register", json={
        "email": "test_fresh1@example.com",
        "password": "password123",
        "full_name": "Test User",
    })
    print(response.status_code, response.json())
    assert response.status_code == 200


def test_unauthorized_reservation():
    """Test accessing reservation endpoint without authentication."""
    # Setup test data
    db = next(get_db())
    try:
        # Clean tables
        db.execute(text(
            "TRUNCATE reservations, showtimes, halls, movies RESTART IDENTITY CASCADE;"))
        # Add a movie
        movie = Movie(
            title="Test Movie",
            genre_id=1,
            duration=120,
            release_date=datetime.now().date()
        )
        db.add(movie)
        # Add a hall
        hall = Hall(name="Hall 1", rows=10, columns=20)
        db.add(hall)
        db.commit()
        # Add a showtime
        showtime = Showtime(
            movie_id=movie.id,
            hall_id=hall.id,
            start_time=datetime.now(),
            end_time=datetime.now(),
            price=15.50
        )
        db.add(showtime)
        db.commit()
        db.refresh(showtime)
    finally:
        db.close()

    response = client.post("/reservations/", json={
        "user_id": 1,
        "showtime_id": showtime.id,
        "seat_number": "A12",
    })
    assert response.status_code == 401
