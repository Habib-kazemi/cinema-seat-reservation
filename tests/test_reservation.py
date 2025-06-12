"""
Tests for reservation endpoints
"""
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import Reservation, User, Showtime, Hall, Movie, Cinema
from src.schemas import ReservationCreate

client = TestClient(app)


def test_create_reservation():
    """Test creating a reservation with valid authentication."""
    # Clean tables before test
    db = next(get_db())
    try:
        db.execute(
            text("TRUNCATE users, reservation, showtime, hall, movie, cinema RESTART IDENTITY CASCADE;"))
        db.commit()

        # Create a cinema
        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()

        # Create a movie and hall
        db_movie = Movie(title="Test Movie", genre_id=1,
                         duration=120, release_date="2025-06-01")
        db_hall = Hall(name="Hall 1", rows=10,
                       columns=20, cinema_id=db_cinema.id)
        db.add(db_movie)
        db.add(db_hall)
        db.commit()

        # Register user
        register_response = client.post("/auth/register", json={
            "email": "test_fresh2@example.com",
            "password": "password123",
            "full_name": "Test User 2",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201
        register_data = register_response.json()

        # Create a showtime for reservation
        db_showtime = Showtime(movie_id=db_movie.id, hall_id=db_hall.id, start_time="2025-06-08 18:00:00+04",
                               end_time="2025-06-08 20:00:00+04", price=10.0)
        db.add(db_showtime)
        db.commit()

        # Login to get token
        login_response = client.post("/auth/login", data={
            "username": "test_fresh2@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Create reservation
        reservation_data = {"showtime_id": db_showtime.id, "seat_number": "A1"}
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/reservation/", json=reservation_data, headers=headers)
        assert response.status_code == 201
        assert response.json()["status"] == "PENDING"
    finally:
        db.close()


def test_get_reservation():
    """Test getting list of reservations for authenticated user."""
    # Clean tables before test
    db = next(get_db())
    try:
        db.execute(
            text("TRUNCATE users, reservation, showtime, hall, movie, cinema RESTART IDENTITY CASCADE;"))
        db.commit()

        # Create a cinema
        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()

        # Create a movie and hall
        db_movie = Movie(title="Test Movie", genre_id=1,
                         duration=120, release_date="2025-06-01")
        db_hall = Hall(name="Hall 1", rows=10,
                       columns=20, cinema_id=db_cinema.id)
        db.add(db_movie)
        db.add(db_hall)
        db.commit()

        # Register user
        register_response = client.post("/auth/register", json={
            "email": "test_fresh4@example.com",
            "password": "password123",
            "full_name": "Test User 4",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        # Create a showtime and reservation
        db_showtime = Showtime(movie_id=db_movie.id, hall_id=db_hall.id, start_time="2025-06-08 18:00:00+04",
                               end_time="2025-06-08 20:00:00+04", price=10.0)
        db.add(db_showtime)
        db.commit()
        db.refresh(db_showtime)

        db_user = db.query(User).filter(
            User.email == "test_fresh4@example.com").first()
        db_reservation = Reservation(
            showtime_id=db_showtime.id, user_id=db_user.id, seat_number="A1", price=10.0, status="PENDING")
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)

        # Login to get token
        login_response = client.post("/auth/login", data={
            "username": "test_fresh4@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Get reservations
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/reservation/", headers=headers)

        assert response.status_code == 200
        reservation = response.json()
        assert len(reservation) > 0
        assert reservation[0]["status"] == "PENDING"
    finally:
        db.close()


def test_cancel_reservation():
    """Test cancelling a reservation."""
    # Clean tables before test
    db = next(get_db())
    try:
        db.execute(
            text("TRUNCATE users, reservation, showtime, hall, movie, cinema RESTART IDENTITY CASCADE;"))
        db.commit()

        # Create a cinema
        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()

        # Create a movie and hall
        db_movie = Movie(title="Test Movie", genre_id=1,
                         duration=120, release_date="2025-06-01")
        db_hall = Hall(name="Hall 1", rows=10,
                       columns=20, cinema_id=db_cinema.id)
        db.add(db_movie)
        db.add(db_hall)
        db.commit()

        # Register and login
        register_response = client.post("/auth/register", json={
            "email": "test_fresh3@example.com",
            "password": "password123",
            "full_name": "Test User 3",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        # Create a showtime and reservation
        db_showtime = Showtime(movie_id=db_movie.id, hall_id=db_hall.id, start_time="2025-06-08 18:00:00+04",
                               end_time="2025-06-08 20:00:00+04", price=10.0)
        db.add(db_showtime)
        db_user = db.query(User).filter(
            User.email == "test_fresh3@example.com").first()
        db_reservation = Reservation(
            showtime_id=db_showtime.id, user_id=db_user.id, seat_number="A1", price=10.0, status="PENDING")
        db.add(db_reservation)
        db.commit()

        # Login to get token
        login_response = client.post("/auth/login", data={
            "username": "test_fresh3@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Cancel reservation
        headers = {"Authorization": f"Bearer {token}"}
        response = client.delete(
            f"/reservation/{db_reservation.id}", headers=headers)
        assert response.status_code == 200
        assert response.json()[
            "message"] == "Reservation cancelled successfully"
    finally:
        db.close()
