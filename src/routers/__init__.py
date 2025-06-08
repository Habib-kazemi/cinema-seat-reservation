"""
Initialize routers for the Cinema Seat Reservation API.
"""
from .users import router as user
from .movie import router as movie
from .showtime import router as showtime
from .hall import router as hall
from .reservation import router as reservation
from .admin import router as admin
from .cinema import router as cinema
