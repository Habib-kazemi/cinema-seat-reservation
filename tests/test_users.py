"""
Tests for users endpoints (admin access)
"""
from datetime import date, datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import User, Cinema, Movie, Hall, Showtime, Reservation

client = TestClient(app)


def test_get_users_as_admin():
    """Test getting list of users as admin."""
    db = next(get_db())
    try:
        db.execute(text(
            "TRUNCATE users, cinema, movie, hall, showtime, reservation RESTART IDENTITY CASCADE;"))
        db.commit()

        # Create cinema
        db_cinema = Cinema(name="Test Cinema", address="Test Address")
        db.add(db_cinema)
        db.commit()
        db.refresh(db_cinema)

        # Create movie
        db_movie = Movie(title="Test Movie", genre_id=1,
                         duration=120, release_date=date(2025, 6, 1))
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)

        # Create hall
        db_hall = Hall(name="Hall 1", rows=10,
                       columns=20, cinema_id=db_cinema.id)
        db.add(db_hall)
        db.commit()
        db.refresh(db_hall)

        # Create showtime
        tz = timezone(timedelta(hours=4))
        db_showtime = Showtime(
            movie_id=db_movie.id,
            hall_id=db_hall.id,
            start_time=datetime(2025, 6, 9, 18, 0, tzinfo=tz),
            end_time=datetime(2025, 6, 9, 20, 0, tzinfo=tz),
            price=10.0
        )
        db.add(db_showtime)
        db.commit()
        db.refresh(db_showtime)

        # Register an admin user
        admin_reg = client.post("/auth/register", json={
            "email": "admin12@example.com",
            "password": "password123",
            "full_name": "Admin User 12",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert admin_reg.status_code == 201

        # Register regular user
        user1_reg = client.post("/auth/register", json={
            "email": "user3@example.com",
            "password": "password123",
            "full_name": "User 3",
            "phone_number": "0987654321"
        })
        assert user1_reg.status_code == 201

        # Create reservation for user3
        user = db.query(User).filter(User.email == "user3@example.com").first()
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
            "username": "admin12@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Get users
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/admin/users", headers=headers)
        assert response.status_code == 200
        users = response.json()
        assert len(users) >= 1  # At least user3
        assert any(u["email"] == "user3@example.com" for u in users)
    finally:
        db.close()
