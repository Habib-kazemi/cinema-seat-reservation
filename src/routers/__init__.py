"""
Initialize routers for Cinema Seat Reservation API
"""
from .users import router as users
from .movies import router as movies
from .reservations import router as reservations
from .showtimes import router as showtimes
from .halls import router as halls
