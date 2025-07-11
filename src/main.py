"""
Main application module for Cinema Seat Reservation API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import admin, hall, movie, reservation, showtime, cinema
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
app.include_router(movie, prefix="/movie", tags=["movie"])
app.include_router(showtime, prefix="/showtime", tags=["showtime"])
app.include_router(hall, prefix="/hall", tags=["hall"])
app.include_router(reservation, prefix="/reservation", tags=["reservation"])
app.include_router(admin,  tags=["admin"])
app.include_router(cinema, prefix="/cinema", tags=["cinema"])
