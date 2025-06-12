"""
Tests for movie endpoints
"""
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from src.database import get_db
from src.main import app
from src.models import Movie, User


client = TestClient(app)


def test_create_movie_as_admin():
    """Test creating a movie as an admin."""
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, movie RESTART IDENTITY CASCADE;"))
        db.commit()

        # Register an admin user
        register_response = client.post("/auth/register", json={
            "email": "admin10@example.com",
            "password": "password123",
            "full_name": "Admin User 10",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        db_user = db.query(User).filter(
            User.email == "admin10@example.com").first()
        assert db_user.role == "ADMIN"  # چک کردن نقش

        # Login to get admin token
        login_response = client.post("/auth/login", data={
            "username": "admin10@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a movie
        movie_data = {
            "title": "Test Movie 2",
            "genre_id": 1,  # فرض بر وجود genre_id=1
            "release_date": "2025-06-01",  # رشته ISO
            "duration": 120
        }
        response = client.post(
            "/admin/movie", json=movie_data, headers=headers)  # اصلاح URL
        assert response.status_code == 201
        assert response.json()["title"] == "Test Movie 2"
    finally:
        db.close()


def test_get_movie():
    """Test getting list of movies."""
    db = next(get_db())
    try:
        db.execute(text("TRUNCATE users, movie RESTART IDENTITY CASCADE;"))
        db_movie = Movie(title="Existing Movie", genre_id=1,
                         duration=120, release_date="2025-06-01")
        db.add(db_movie)
        db.commit()

        # Register an admin user
        register_response = client.post("/auth/register", json={
            "email": "admin11@example.com",
            "password": "password123",
            "full_name": "Admin User 11",
            "role": "ADMIN",
            "phone_number": "1234567890"
        })
        assert register_response.status_code == 201

        # Login to get admin token
        login_response = client.post("/auth/login", data={
            "username": "admin11@example.com",
            "password": "password123"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Get movies
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/movie/", headers=headers)
        assert response.status_code == 200
        movie = response.json()
        assert len(movie) >= 1
        assert any(m["title"] == "Existing Movie" for m in movie)
    finally:
        db.close()
