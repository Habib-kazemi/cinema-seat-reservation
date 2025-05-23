# Cinema Seat Reservation API

## Authentication

- **POST /api/auth/register**
  - Description: Register a new user.
  - Request Body: `{ "email": str, "password": str, "full_name": str, "phone_number": str | null }`
  - Response: `{ "id": int, "email": str, "full_name": str, "role": str, "phone_number": str | null }`
- **POST /api/auth/login**
  - Description: Authenticate user and return JWT token.
  - Request Body: `{ "email": str, "password": str }`
  - Response: `{ "access_token": str, "token_type": "bearer" }`

## Reservations

- **POST /api/reservations/**
  - Description: Create a new reservation (requires JWT authentication).
  - Headers: `Authorization: Bearer <token>`
  - Request Body: `{ "user_id": int, "showtime_id": int, "seat_number": str }`
  - Response: `{ "id": int, "message": str }`

## Movies, Genres, Showtimes, Halls

- (Existing endpoints defined in respective routers)
