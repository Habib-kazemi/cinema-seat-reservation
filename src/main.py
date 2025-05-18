"""
Main entry point for the cinema seat reservation app
"""
from fastapi import FastAPI
from .routers import users, movies

app = FastAPI(title="Cinema Seat Reservation API")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(movies.router, prefix="/api/movies", tags=["movies"])


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message for the Cinema Seat Reservation API.

    Returns:
        dict: A JSON response with a welcome message.
    """
    return {"message": "Cinema Seat Reservation API"}
