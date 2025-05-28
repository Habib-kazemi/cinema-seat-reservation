Cinema Seat Reservation API

A RESTful API for managing cinema seat reservations, built with Python, FastAPI, and PostgreSQL.

Features

Browse movies with filters for genre and release date (GET /movies/).
Browse showtimes with filters for movie and date (GET /showtimes/).
View available seats for a showtime (GET /showtimes/{id}/seats).
Reserve and cancel seats (POST /reservations/, DELETE /reservations/{id}) with JWT authentication.
Admin management for movies, showtimes, and halls (/admin/).
User registration and login (/auth/register, /auth/login).
Fully tested with pytest for reliability.

Prerequisites

Python 3.13+
PostgreSQL database

API Endpoints

GET /movies/?genre_id={id}&release_date_gte={YYYY-MM-DD}: List movies with optional genre and release date filters.
GET /showtimes/?movie_id={id}&date={YYYY-MM-DD}: List showtimes with optional movie and date filters.
GET /showtimes/{id}/seats: Get available seats for a showtime (e.g., ["A12", "B5"]).
POST /reservations/: Create a reservation (requires JWT token).
DELETE /reservations/{id}: Cancel a reservation (requires JWT token).
POST /auth/register: Register a new user.
POST /auth/login: Login and receive a JWT token.
POST /admin/movies: Add a new movie (admin only).

Usage

Access the API at http://localhost:8000/docs for interactive Swagger UI documentation.
Use Postman or similar tools to test endpoints.
Ensure a PostgreSQL database is configured with the schema defined in src/models.py.
