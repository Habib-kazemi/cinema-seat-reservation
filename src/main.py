from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.features.users.routers import router as user_router
from src.features.movie.routers import router as movie_router
from src.features.showtime.routers import router as showtime_router
from src.features.hall.routers import router as hall_router
from src.features.reservation.routers import router as reservation_router
from src.features.admin.routers import router as admin_router
from src.features.auth.routers import router as auth_router
from src.features.cinema.routers import router as cinema_router

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
    return {"message": "Welcome to Cinema Seat Reservation API. Visit /docs for API documentation."}

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(movie_router, prefix="/api/v1/movie", tags=["movie"])
app.include_router(
    showtime_router, prefix="/api/v1/showtime", tags=["showtime"])
app.include_router(hall_router, prefix="/api/v1/hall", tags=["hall"])
app.include_router(reservation_router,
                   prefix="/api/v1/reservation", tags=["reservation"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(cinema_router, prefix="/api/v1/cinema", tags=["cinema"])
