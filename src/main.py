"""Main FastAPI application entry point."""

from fastapi import FastAPI

from .routers import halls, movies, reservations, showtimes, users

app = FastAPI(title="Cinema Seat Reservation API")

app.include_router(users, prefix="/api/auth", tags=["auth"])
app.include_router(reservations, prefix="/api/reservations",
                   tags=["reservations"])
app.include_router(movies, prefix="/api/movies", tags=["movies"])
app.include_router(showtimes, prefix="/api/showtimes", tags=["showtimes"])
app.include_router(halls, prefix="/api/halls", tags=["halls"])
