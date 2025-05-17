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
    return {"message": "Cinema Seat Reservation API"}
