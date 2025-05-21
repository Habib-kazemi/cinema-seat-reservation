"""
Main entry point for the cinema seat reservation app
"""
from fastapi import FastAPI
from .routers import users, movies, reservations, showtimes, halls

app = FastAPI(title="Cinema Seat Reservation API")

app.include_router(users, prefix="/api/users", tags=["users"])
app.include_router(movies, prefix="/api/movies", tags=["movies"])
app.include_router(reservations, prefix="/api/reservations",
                   tags=["reservations"])
app.include_router(showtimes, prefix="/api/showtimes", tags=["showtimes"])
app.include_router(halls, prefix="/api/halls", tags=["halls"])


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message for the Cinema Seat Reservation API.

    Returns:
        dict: A JSON response with a welcome message.
    """
    return {"message": "Cinema Seat Reservation API"}
