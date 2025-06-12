"""
Tests for admin endpoints
"""
from datetime import date, datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import User, Showtime, Reservation, Movie, Cinema, Hall


client = TestClient(app)


def test_create_movie_as_admin():
    """Test creating a movie as an admin."""
    db = next(get_db())
    try:
        db.execute(text("""
            TRUNCATE users, movie, hall, showtime, cinema, reservation RESTART IDENTITY CASCADE;
        """))
        db.commit()

        register_response = client.post("/auth/register", json={
            "email": "admin@example.com",
            "password": "password123",
            "full_name": "Admin User",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        db_user = db.query(User).filter(
            User.email == "admin@example.com").first()
        assert db_user.role == "ADMIN"

        login_response = client.post("/auth/login", data={
            "username": "admin@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        movie_data = {
            "title": "Test Movie",
            "genre_id": 1,
            "release_date": "2025-06-01",
            "duration": 120
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/admin/movie", json=movie_data, headers=headers)
        assert response.status_code == 201
        assert response.json()["title"] == "Test Movie"
    finally:
        db.close()


def test_approve_reservation_as_admin():
    """Test approving a reservation as an admin."""
    db = next(get_db())
    try:
        db.execute(text(
            "TRUNCATE users, movie, hall, showtime, reservation, cinema RESTART IDENTITY CASCADE;"))
        db.commit()

        # Create admin and user
        client.post("/auth/register", json={
            "email": "admin2@example.com",
            "password": "password123",
            "full_name": "Admin User",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })

        client.post("/auth/register", json={
            "email": "user@example.com",
            "password": "password123",
            "full_name": "Normal User",
            "phone_number": "1111111111"
        })

        # Check admin role
        db_user = db.query(User).filter(
            User.email == "admin2@example.com").first()
        assert db_user.role == "ADMIN"

        user = db.query(User).filter(User.email == "user@example.com").first()

        # Create movie, cinema, and hall
        db_movie = Movie(title="X", genre_id=1,
                         release_date=date(2025, 1, 1), duration=100)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)

        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()
        db.refresh(db_cinema)

        db_hall = Hall(name="Main Hall", rows=10,
                       columns=20, cinema_id=db_cinema.id)
        db.add(db_hall)
        db.commit()
        db.refresh(db_hall)

        # Create showtime
        tz = timezone(timedelta(hours=4))
        showtime = Showtime(
            movie_id=db_movie.id,
            hall_id=db_hall.id,
            start_time=datetime(2025, 6, 8, 18, 0, tzinfo=tz),
            end_time=datetime(2025, 6, 8, 20, 0, tzinfo=tz),
            price=10.0
        )
        db.add(showtime)
        db.commit()
        db.refresh(showtime)

        # Create reservation
        reservation = Reservation(
            showtime_id=showtime.id,
            user_id=user.id,
            seat_number="A1",
            price=10.0,
            status="PENDING"
        )
        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        # Login as admin
        login_response = client.post("/auth/login", data={
            "username": "admin2@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Approve reservation
        response = client.post(
            f"/admin/reservation/{reservation.id}/approve", headers=headers)
        assert response.status_code == 200
        assert response.json()["status"] == "CONFIRMED"
    finally:
        db.close()


def test_get_admin_users():
    """Test getting list of users as admin."""
    db = next(get_db())
    try:
        db.execute(text(
            "TRUNCATE users, cinema, movie, hall, showtime, reservation RESTART IDENTITY CASCADE;"))
        db.commit()

        # Create cinema, movie, hall, and showtime
        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()
        db.refresh(db_cinema)

        db_movie = Movie(title="Test Movie", genre_id=1,
                         duration=120, release_date=date(2025, 6, 1))
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)

        db_hall = Hall(name="Hall 1", rows=10,
                       columns=20, cinema_id=db_cinema.id)
        db.add(db_hall)
        db.commit()
        db.refresh(db_hall)

        tz = timezone(timedelta(hours=4))
        db_showtime = Showtime(
            movie_id=db_movie.id,
            hall_id=db_hall.id,
            start_time=datetime(2025, 6, 8, 18, 0, tzinfo=tz),
            end_time=datetime(2025, 6, 8, 20, 0, tzinfo=tz),
            price=10.0
        )
        db.add(db_showtime)
        db.commit()
        db.refresh(db_showtime)

        # Register admin and user
        register_response = client.post("/auth/register", json={
            "email": "admin3@example.com",
            "password": "password123",
            "full_name": "Admin User",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        client.post("/auth/register", json={
            "email": "user1@example.com",
            "password": "password123",
            "full_name": "User 1",
            "phone_number": "1111111111"
        })

        db_user = db.query(User).filter(
            User.email == "admin3@example.com").first()
        assert db_user.role == "ADMIN"

        # Create reservation for user1
        user = db.query(User).filter(User.email == "user1@example.com").first()
        reservation = Reservation(
            showtime_id=db_showtime.id,
            user_id=user.id,
            seat_number="A1",
            price=10.0,
            status="PENDING"
        )
        db.add(reservation)
        db.commit()
        db.refresh(reservation)

        # Login as admin
        login_response = client.post("/auth/login", data={
            "username": "admin3@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/admin/users", headers=headers)
        assert response.status_code == 200
        assert any(user["email"] ==
                   "user1@example.com" for user in response.json())
    finally:
        db.close()
