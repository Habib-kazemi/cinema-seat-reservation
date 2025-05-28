"""
Main application module for Cinema Seat Reservation API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import admin, halls, movies, reservations, showtimes
from .routers.auth import router as auth

app = FastAPI(title="Cinema Seat Reservation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint for the API."""
    return {"message": "Welcome to Cinema Seat Reservation API. Visit /docs for API documentation."}

app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(movies, prefix="/movies", tags=["movies"])
app.include_router(showtimes, prefix="/showtimes", tags=["showtimes"])
app.include_router(halls, prefix="/halls", tags=["halls"])
app.include_router(reservations, prefix="/reservations", tags=["reservations"])
app.include_router(admin, prefix="/admin", tags=["admin"])
