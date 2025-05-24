"""
Initialize routers for the Cinema Seat Reservation API.
"""
from .users import router as users
from .movies import router as movies
from .showtimes import router as showtimes
from .halls import router as halls
from .reservations import router as reservations
from .admin import router as admin
