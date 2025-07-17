"""Centralized model imports and table creation."""

from src.database import Base, engine
from src.features.users.models import User as _User  # noqa: F401
from src.features.movie.models import Movie as _Movie  # noqa: F401
from src.features.genre.models import Genre as _Genre  # noqa: F401
from src.features.hall.models import Hall as _Hall  # noqa: F401
from src.features.showtime.models import Showtime as _Showtime  # noqa: F401
from src.features.reservation.models import Reservation as _Reservation  # noqa: F401
from src.features.cinema.models import Cinema as _Cinema  # noqa: F401
# Create all tables in the database
Base.metadata.create_all(bind=engine)
