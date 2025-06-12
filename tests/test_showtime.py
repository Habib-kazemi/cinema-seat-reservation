"""
Tests for showtime endpoints
"""
from datetime import datetime, timezone, timedelta, date
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import Showtime, Movie, Hall, Cinema, User

client = TestClient(app)


def test_create_showtime_as_admin():
    """Test creating a showtime as an admin."""
    db = next(get_db())
    try:
        db.execute(
            text("TRUNCATE users, cinema, movie, hall, showtime RESTART IDENTITY CASCADE;"))
        db.commit()

        # Create cinema
        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()
        db.refresh(db_cinema)

        # Create movie and hall
        db_movie = Movie(title="Test Movie", genre_id=1,
                         duration=120, release_date=date(2025, 6, 1))
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)

        db_hall = Hall(name="Hall 3", rows=10,
                       columns=20, cinema_id=db_cinema.id)
        db.add(db_hall)
        db.commit()
        db.refresh(db_hall)

        # Register an admin user
        register_response = client.post("/auth/register", json={
            "email": "admin8@example.com",
            "password": "password123",
            "full_name": "Admin User 8",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        db_user = db.query(User).filter(
            User.email == "admin8@example.com").first()
        assert db_user.role == "ADMIN"

        # Login to get admin token
        login_response = client.post("/auth/login", data={
            "username": "admin8@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a showtime
        tz = timezone(timedelta(hours=4))
        showtime_data = {
            "movie_id": db_movie.id,
            "hall_id": db_hall.id,
            "start_time": datetime(2025, 6, 9, 18, 0, 0, tzinfo=tz).isoformat(),
            "end_time": datetime(2025, 6, 9, 20, 0, 0, tzinfo=tz).isoformat(),
            "price": 12.50
        }
        response = client.post(
            "/admin/showtime", json=showtime_data, headers=headers)  # تغییر URL
        assert response.status_code == 201
    finally:
        db.close()


def test_get_showtime():
    """Test getting list of showtime."""
    db = next(get_db())
    try:
        db.execute(
            text("TRUNCATE users, cinema, movie, hall, showtime RESTART IDENTITY CASCADE;"))
        db.commit()

        # Create cinema
        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()

        # Create movie and hall
        db_movie = Movie(title="Test Movie", genre_id=1,
                         duration=120, release_date=date(2025, 6, 1))
        db_hall = Hall(name="Hall 4", rows=10,
                       columns=20, cinema_id=db_cinema.id)
        db.add(db_movie)
        db.add(db_hall)
        db.commit()
        db.refresh(db_movie)
        db.refresh(db_hall)

        # Create showtime
        tz = timezone(timedelta(hours=4))
        db_showtime = Showtime(
            movie_id=db_movie.id,
            hall_id=db_hall.id,
            start_time=datetime(2025, 6, 9, 18, 0, 0, tzinfo=tz),
            end_time=datetime(2025, 6, 9, 20, 0, 0, tzinfo=tz),
            price=12.50
        )
        db.add(db_showtime)
        db.commit()
        db.refresh(db_showtime)

        # Register an admin user
        register_response = client.post("/auth/register", json={
            "email": "admin9@example.com",
            "password": "password123",
            "full_name": "Admin User 9",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        # Login to get admin token
        login_response = client.post("/auth/login", data={
            "username": "admin9@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Get showtimes
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/showtime/", headers=headers)
        assert response.status_code == 200
        showtimes = response.json()
        assert len(showtimes) > 0
    finally:
        db.close()
