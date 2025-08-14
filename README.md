Cinema Seat Reservation API
A RESTful API (OAS 3.1) for managing cinema seat reservations, built with Python, FastAPI, and SQLAlchemy. Supports browsing movies, showtimes, halls, seat reservations, and admin management.
Project Structure

src/features/auth: User registration and login.
src/features/cinema: Cinema and related hall/showtime operations.
src/features/hall: Hall retrieval with showtimes.
src/features/movie: Movie browsing.
src/features/showtime: Showtime browsing.
src/features/reservation: Seat reservations and user operations.
src/features/admin: Admin-only operations (cinemas, halls, movies, showtimes, reservations).
src/database: Database configuration.
src/utils: Utility functions (e.g., admin access checks).

Prerequisites

Python 3.10+
SQL database (e.g., PostgreSQL)
Virtual environment (recommended)
Dependencies in requirements.txt
API testing tools (e.g., Postman, curl)

Setup

Clone the repository:
git clone <repository-url>
cd cinema-seat-reservation

Install dependencies:
pip install -r requirements.txt

Configure environment variables:Create a .env file with database URL (e.g., DATABASE_URL=postgresql://user:password@localhost:5432/dbname) and secret key (e.g., SECRET_KEY=your-secret-key).

Run the application:
uvicorn src.main:app --host 0.0.0.0 --port 8000

Access Swagger UI:Open http://localhost:8000/docs for interactive API documentation.

API Endpoints
Auth

POST /api/v1/auth/registerRegister a new user.Body: { "email": str, "password": str, "role": "USER"|"ADMIN", "full_name": str, "phone_number": str }Response: { "message": "User registered successfully" }Example:
curl -X POST "http://localhost:8000/api/v1/auth/register" -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"password123","role":"USER","full_name":"Test User","phone_number":"123456789"}'

POST /api/v1/auth/loginLogin and receive JWT token.Body: username=test@example.com&password=password123 (form-data)Response: { "access_token": str, "token_type": "bearer" }Example:
curl -X POST "http://localhost:8000/api/v1/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=test@example.com&password=password123"

Movie

GET /api/v1/movieList movies with optional filters.Parameters: genre_id (query, optional), release_date_gte (query, optional), release_date_lte (query, optional).Response: List of movies. [
{
"id": 1,
"title": "Movie A",
"genre_id": 1,
"duration": 120,
"release_date": "2025-01-01",
"description": "A great movie",
"poster_url": "http://example.com/poster.jpg"
}
]

Showtime

GET /api/v1/showtimeList showtimes with optional filters.Parameters: movie_id (query, optional), showtime_date (query, optional).Response: List of showtimes with movie details. [
{
"id": 1,
"movie_id": 1,
"hall_id": 1,
"start_time": "2025-08-09T18:00:00",
"end_time": "2025-08-09T20:00:00",
"price": 10.0,
"movie": {
"id": 1,
"title": "Movie A",
"genre_id": 1,
"duration": 120,
"release_date": "2025-01-01",
"description": "A great movie",
"poster_url": "http://example.com/poster.jpg"
}
}
]

Hall

GET /api/v1/hallList halls with their showtimes.Parameters: cinema_id (query, optional).Response: List of halls with future showtimes. [
{
"id": 1,
"name": "Hall A",
"rows": 10,
"columns": 12,
"cinema_id": 1,
"showtimes": [
{
"id": 1,
"movie_id": 1,
"hall_id": 1,
"start_time": "2025-08-09T18:00:00",
"end_time": "2025-08-09T20:00:00",
"price": 10.0,
"movie": {
"id": 1,
"title": "Movie A",
"genre_id": 1,
"duration": 120,
"release_date": "2025-01-01",
"description": "A great movie",
"poster_url": "http://example.com/poster.jpg"
}
}
]
}
]

Reservation

GET /api/v1/reservationList user reservations (requires JWT).Response: List of reservations with position_id.  
[
{
"id": 1,
"user_id": 1,
"showtime_id": 1,
"position_id": 1,
"row_index": 1,
"column_index": 1,
"price": 10.0,
"status": "PENDING",
"created_at": "2025-08-08T18:00:00"
}
]

POST /api/v1/reservationCreate a reservation (requires JWT).Body: { "showtime_id": int, "row_index": int, "column_index": int }Response: Reservation details with position_id.  
{
"id": 1,
"user_id": 1,
"showtime_id": 1,
"position_id": 1,
"row_index": 1,
"column_index": 1,
"price": 10.0,
"status": "PENDING",
"created_at": "2025-08-08T18:00:00"
}

Example:
curl -X POST "http://localhost:8000/api/v1/reservation" -H "Authorization: Bearer [token]" -H "Content-Type: application/json" -d '{"showtime_id":1,"row_index":1,"column_index":1}'

DELETE /api/v1/reservation/{reservation_id}Cancel a reservation (requires JWT).Response: { "message": "Reservation cancelled successfully" }.

GET /api/v1/reservation/showtime/{showtime_id}/seatList available seats for a showtime.Parameters: showtime_id (path, required).Response: Seats with position_id and status.  
{
"showtime_id": 1,
"available_seat": [
{
"position_id": 1,
"row_index": 1,
"column_index": 1,
"status": "reserved"
},
{
"position_id": 2,
"row_index": 1,
"column_index": 2,
"status": "available"
}
]
}

Cinema

GET /api/v1/cinemaList all cinemas.Response: List of cinemas with halls.  
[
{
"id": 1,
"name": "Cinema A",
"address": "123 Main St",
"halls": [
{
"id": 1,
"name": "Hall A",
"rows": 10,
"columns": 12,
"cinema_id": 1,
"showtimes": []
}
]
}
]

GET /api/v1/cinema/{cinema_id}/hallList halls for a cinema.Parameters: cinema_id (path, required).Response: List of halls.  
[
{
"id": 1,
"name": "Hall A",
"rows": 10,
"columns": 12,
"cinema_id": 1,
"showtimes": []
}
]

GET /api/v1/cinema/{cinema_id}/showtimeList showtimes for a cinema.Parameters: cinema_id (path, required).Response: List of showtimes with movie details.  
[
{
"id": 1,
"movie_id": 1,
"hall_id": 1,
"start_time": "2025-08-09T18:00:00",
"end_time": "2025-08-09T20:00:00",
"price": 10.0,
"movie": {
"id": 1,
"title": "Movie A",
"genre_id": 1,
"duration": 120,
"release_date": "2025-01-01",
"description": "A great movie",
"poster_url": "http://example.com/poster.jpg"
}
}
]

Admin (Requires Admin Authentication)

POST /api/v1/admin/cinemaCreate a cinema.Body: { "name": str, "address": str }Response: Created cinema details.

PUT /api/v1/admin/cinema/{cinema_id}Update a cinema.Body: { "name": str, "address": str }Response: Updated cinema details.

PATCH /api/v1/admin/cinema/{cinema_id}Partially update a cinema.Parameters: name (query, optional), address (query, optional).Response: Updated cinema details.

DELETE /api/v1/admin/cinema/{cinema_id}Delete a cinema (if no dependent halls).Response: { "message": "Cinema deleted successfully" }.

POST /api/v1/admin/hallCreate a hall.Body: { "name": str, "rows": int, "columns": int, "cinema_id": int }Response: Created hall details.

PUT /api/v1/admin/hall/{hall_id}Update a hall.Body: Same as create.Response: Updated hall details.

PATCH /api/v1/admin/hall/{hall_id}Partially update a hall.Parameters: name, rows, columns, cinema_id (query, optional).Response: Updated hall details.

DELETE /api/v1/admin/hall/{hall_id}Delete a hall (if no dependent showtimes).Response: { "message": "Hall deleted successfully" }.

POST /api/v1/admin/movieCreate a movie.Body: { "title": str, "genre_id": int, "duration": int, "release_date": str, "description": str, "poster_url": str }Response: Created movie details.

PUT /api/v1/admin/movie/{movie_id}Update a movie.Body: Same as create.Response: Updated movie details.

PATCH /api/v1/admin/movie/{movie_id}Partially update a movie.Parameters: title, genre_id, duration, release_date, description, poster_url (query, optional).Response: Updated movie details.

DELETE /api/v1/admin/movie/{movie_id}Delete a movie (if no dependent showtimes).Response: { "message": "Movie deleted successfully" }.

POST /api/v1/admin/showtimeCreate a showtime.Body: { "movie_id": int, "hall_id": int, "start_time": str, "end_time": str, "price": float }Response: Created showtime with movie details.

PUT /api/v1/admin/showtime/{showtime_id}Update a showtime.Body: Same as create.Response: Updated showtime details.

PATCH /api/v1/admin/showtime/{showtime_id}Partially update a showtime.Parameters: movie_id, hall_id, start_time, end_time, price (query, optional).Response: Updated showtime details.

DELETE /api/v1/admin/showtime/{showtime_id}Delete a showtime (if no dependent reservations).Response: { "message": "Showtime deleted successfully" }.

GET /api/v1/admin/userList users with reservations.Response: List of users.

GET /api/v1/admin/total_saleGet total sales with filters.Parameters: cinema_id, showtime_id, start_date, end_date (query, optional).Response: { "total_sale": float }.

POST /api/v1/admin/reservation/{reservation_id}/approveApprove a pending reservation.Response: Updated reservation with position_id.

POST /api/v1/admin/reservation/{reservation_id}/rejectReject a reservation.Response: Updated reservation with position_id.

Authentication

User Endpoints: Require JWT token in Authorization: Bearer [token] header.
Admin Endpoints: Require JWT token with admin role, validated by check_admin.
Tokens obtained via /auth/register and /auth/login.

Notes

HTTP Status Codes: 200 (OK), 201 (Created), 400 (Bad Request), 403 (Forbidden), 404 (Not Found).
Position ID: Included in reservation and seat responses (position_id) for frontend use.
Seat Status: Included in /reservation/showtime/{showtime_id}/seat as available or reserved.
Showtime Creation: Validates time slot conflicts and movie duration.
Admin Restrictions: Create/update/delete operations restricted to admin role.
OpenAPI: Swagger UI at http://localhost:8000/docs or /openapi.json.

Development Notes

Database Models: Defined in src/models.py (e.g., User, Reservation, Cinema).
Logging: Configured in src/config/logging_config.py, logs in src/logs/.
Tests: Initial pytest tests included in requirements.txt (under development).

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/branch-name).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature/branch-name).
Create a pull request.

## Deployment

- **Database**: Deployed on Supabase with migrations applied (alembic).
- **Application**: Deployed on Render using FastAPI and Gunicorn in Docker.
- **Environment Variables**:
  - DATABASE_URL: Supabase connection string with sslmode=require
  - SECRET_KEY: JWT secret key
  - ENVIRONMENT: Set to "production"
  - WEB_CONCURRENCY: Set to 4
- **Build Command**: `bash ./build.sh`
- **Start Command**: `gunicorn -k uvicorn.workers.UvicornWorker src.main:app`
