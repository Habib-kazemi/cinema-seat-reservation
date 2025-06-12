"""
Admin-related API routes for managing movie, showtime, hall, cinema, and reservation.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import get_current_user
from ..database import get_db
from ..models import Hall, Movie, Showtime, User, Reservation, Status, Cinema
from ..schemas import HallCreate, HallResponse, MovieCreate, MovieResponse, ShowtimeCreate, ShowtimeResponse, ReservationResponse, UserResponse, CinemaCreate, CinemaResponse

router = APIRouter(tags=["admin"])


def check_admin(user: User = Depends(get_current_user)):
    """
    Ensure the user has admin privileges.

    Args:
        user: Current user from authentication dependency.

    Returns:
        User: The authenticated admin user.

    Raises:
        HTTPException: If the user is not an admin.
    """
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


@router.post("/cinema", response_model=CinemaResponse, status_code=status.HTTP_201_CREATED)
async def create_cinema(
        cinema: CinemaCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Create a new cinema.

    Args:
        cinema: Cinema data to create.
        db: Database session.
        _: Admin user.

    Returns:
        CinemaResponse: Created cinema details.
    """
    db_cinema = Cinema(**cinema.model_dump())
    db.add(db_cinema)
    db.commit()
    db.refresh(db_cinema)
    return db_cinema


@router.delete("/cinema/{cinema_id}", response_model=dict)
async def delete_cinema(cinema_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Delete a cinema by ID.

    Args:
        cinema_id: ID of the cinema to delete.
        db: Database session.
        _: Admin user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the cinema is not found.
    """
    cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
    db.delete(cinema)
    db.commit()
    return {"message": "Cinema deleted successfully"}


@router.get("/hall", response_model=List[HallResponse])
async def get_hall(db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Retrieve a list of all cinema hall.

    Args:
        db: Database session.
        _: Admin user.

    Returns:
        List[HallResponse]: List of all hall with their details.
    """
    halls = db.query(Hall).all()
    return halls


@router.post("/hall", response_model=HallResponse, status_code=status.HTTP_201_CREATED)
async def create_hall(hall: HallCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Create a new cinema hall.

    Args:
        hall: Hall data including name, rows, columns, and cinema_id.
        db: Database session.
        _: Admin user.

    Returns:
        HallResponse: Created hall details.

    Raises:
        HTTPException: If rows, columns, or cinema_id are invalid.
    """
    try:
        # Check if cinema exists
        cinema = db.query(Cinema).filter(Cinema.id == hall.cinema_id).first()
        if not cinema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
        # Check if rows and columns are positive
        if hall.rows <= 0 or hall.columns <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rows and columns must be positive")

        # Create new hall
        db_hall = Hall(
            name=hall.name,
            rows=hall.rows,
            columns=hall.columns,
            cinema_id=hall.cinema_id
        )
        db.add(db_hall)
        db.commit()
        db.refresh(db_hall)

        return db_hall

    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error") from exc


@router.put("/hall/{hall_id}", response_model=HallResponse)
async def update_hall(
    hall_id: int,
    hall: HallCreate,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    """
    Update a cinema hall completely by ID.

    Args:
        hall_id: ID of the hall to update.
        hall: Updated hall data.
        db: Database session.
        _: Admin user.

    Returns:
        HallResponse: Updated hall details.

    Raises:
        HTTPException: If hall or cinema is not found, or if rows/columns are invalid.
    """
    db_hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not db_hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")

    cinema = db.query(Cinema).filter(Cinema.id == hall.cinema_id).first()
    if not cinema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")

    if hall.rows <= 0 or hall.columns <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rows and columns must be positive")

    db_hall.name = hall.name
    db_hall.rows = hall.rows
    db_hall.columns = hall.columns
    db_hall.cinema_id = hall.cinema_id
    db.commit()
    db.refresh(db_hall)
    return db_hall


@router.patch("/hall/{hall_id}", response_model=HallResponse)
async def partial_update_hall(
    hall_id: int,
    name: Optional[str] = None,
    rows: Optional[int] = None,
    columns: Optional[int] = None,
    cinema_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    """
    Partially update a cinema hall by ID.

    Args:
        hall_id: ID of the hall to update.
        name: Updated name (optional).
        rows: Updated rows (optional).
        columns: Updated columns (optional).
        cinema_id: Updated cinema ID (optional).
        db: Database session.
        _: Admin user.

    Returns:
        HallResponse: Updated hall details.

    Raises:
        HTTPException: If hall or cinema is not found, or if rows/columns are invalid.
    """
    db_hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not db_hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")

    if name is not None:
        db_hall.name = name
    if rows is not None:
        if rows <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Rows must be positive")
        db_hall.rows = rows
    if columns is not None:
        if columns <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Columns must be positive")
        db_hall.columns = columns
    if cinema_id is not None:
        cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
        if not cinema:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cinema not found")
        db_hall.cinema_id = cinema_id

    db.commit()
    db.refresh(db_hall)
    return db_hall


@router.delete("/hall/{hall_id}", response_model=dict)
async def delete_hall(hall_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Delete a cinema hall by ID.

    Args:
        hall_id: ID of the hall to delete.
        db: Database session.
        _: Admin user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the hall is not found.
    """
    hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hall not found")
    db.delete(hall)
    db.commit()
    return {"message": "Hall deleted successfully"}


@router.post("/movie", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
async def create_movie(movie: MovieCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Create a new movie.

    Args:
        movie: Movie data to create.
        db: Database session.
        _: Admin user.

    Returns:
        MovieResponse: Created movie details.
    """
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.put("/movie/{movie_id}", response_model=MovieResponse)
async def update_movie(
    movie_id: int,
    movie: MovieCreate,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    """
    Update a movie completely by ID.

    Args:
        movie_id: ID of the movie to update.
        movie: Updated movie data.
        db: Database session.
        _: Admin user.

    Returns:
        MovieResponse: Updated movie details.

    Raises:
        HTTPException: If movie is not found.
    """
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    for key, value in movie.dict().items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.patch("/movie/{movie_id}", response_model=MovieResponse)
async def partial_update_movie(
    movie_id: int,
    title: Optional[str] = None,
    genre_id: Optional[int] = None,
    duration: Optional[int] = None,
    release_date: Optional[str] = None,
    description: Optional[str] = None,
    poster_url: Optional[str] = None,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    """
    Partially update a movie by ID.

    Args:
        movie_id: ID of the movie to update.
        title: Updated title (optional).
        genre_id: Updated genre ID (optional).
        duration: Updated duration (optional).
        release_date: Updated release date (optional).
        description: Updated description (optional).
        poster_url: Updated poster URL (optional).
        db: Database session.
        _: Admin user.

    Returns:
        MovieResponse: Updated movie details.

    Raises:
        HTTPException: If movie is not found.
    """
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    if title is not None:
        db_movie.title = title
    if genre_id is not None:
        db_movie.genre_id = genre_id
    if duration is not None:
        db_movie.duration = duration
    if release_date is not None:
        db_movie.release_date = release_date
    if description is not None:
        db_movie.description = description
    if poster_url is not None:
        db_movie.poster_url = poster_url

    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.delete("/movie/{movie_id}", response_model=dict)
async def delete_movie(movie_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Delete a movie by ID.

    Args:
        movie_id: ID of the movie to delete.
        db: Database session.
        _: Admin user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the movie is not found.
    """
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted successfully"}


@router.post("/showtime", response_model=ShowtimeResponse, status_code=status.HTTP_201_CREATED)
async def create_showtime(
    showtime: ShowtimeCreate, db: Session = Depends(get_db), _=Depends(check_admin)
):
    """
    Create a new showtime.

    Args:
        showtime: Showtime data to create.
        db: Database session.
        _: Admin user.

    Returns:
        ShowtimeResponse: Created showtime details.
    """
    db_showtime = Showtime(**showtime.model_dump())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime


@router.put("/showtime/{showtime_id}", response_model=ShowtimeResponse)
async def update_showtime(
    showtime_id: int,
    showtime: ShowtimeCreate,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    """
    Update a showtime completely by ID.

    Args:
        showtime_id: ID of the showtime to update.
        showtime: Updated showtime data.
        db: Database session.
        _: Admin user.

    Returns:
        ShowtimeResponse: Updated showtime details.

    Raises:
        HTTPException: If showtime is not found.
    """
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not db_showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")

    for key, value in showtime.dict().items():
        setattr(db_showtime, key, value)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime


@router.patch("/showtime/{showtime_id}", response_model=ShowtimeResponse)
async def partial_update_showtime(
    showtime_id: int,
    movie_id: Optional[int] = None,
    hall_id: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    price: Optional[float] = None,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    """
    Partially update a showtime by ID.

    Args:
        showtime_id: ID of the showtime to update.
        movie_id: Updated movie ID (optional).
        hall_id: Updated hall ID (optional).
        start_time: Updated start time (optional).
        end_time: Updated end time (optional).
        price: Updated price (optional).
        db: Database session.
        _: Admin user.

    Returns:
        ShowtimeResponse: Updated showtime details.

    Raises:
        HTTPException: If showtime is not found.
    """
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not db_showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")

    if movie_id is not None:
        db_showtime.movie_id = movie_id
    if hall_id is not None:
        db_showtime.hall_id = hall_id
    if start_time is not None:
        db_showtime.start_time = start_time
    if end_time is not None:
        db_showtime.end_time = end_time
    if price is not None:
        db_showtime.price = price

    db.commit()
    db.refresh(db_showtime)
    return db_showtime


@router.delete("/showtime/{showtime_id}", response_model=dict)
async def delete_showtime(showtime_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Delete a showtime by ID.

    Args:
        showtime_id: ID of the showtime to delete.
        db: Database session.
        _: Admin user.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If the showtime is not found.
    """
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Showtime not found")
    db.delete(showtime)
    db.commit()
    return {"message": "Showtime deleted successfully"}


@router.get("/users", response_model=List[UserResponse])
async def get_users_with_reservations(db: Session = Depends(get_db), _=Depends(check_admin)):
    """
    Retrieve a list of user who have made reservation.

    Args:
        db: Database session.
        _: Admin user.

    Returns:
        List[UserResponse]: List of user with their details who have reservation.
    """
    users = db.query(User).join(Reservation, User.id ==
                                Reservation.user_id).distinct().all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No user with reservation found")
    return users


@router.post("/reservation/{reservation_id}/approve", response_model=ReservationResponse)
async def approve_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    """
    Approve a pending reservation.

    Args:
        reservation_id: ID of the reservation to approve.
        db: Database session.
        _: Admin user.

    Returns:
        ReservationResponse: Updated reservation details.

    Raises:
        HTTPException: If reservation is not found or not in PENDING status.
    """
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    if reservation.status != Status.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Reservation is not pending")
    reservation.status = Status.CONFIRMED
    db.commit()
    db.refresh(reservation)
    return reservation


@router.post("/reservation/{reservation_id}/reject", response_model=ReservationResponse)
async def reject_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    """
    Reject a pending reservation.

    Args:
        reservation_id: ID of the reservation to reject.
        db: Database session.
        _: Admin user.

    Returns:
        ReservationResponse: Updated reservation details.

    Raises:
        HTTPException: If reservation is not found or not in PENDING status.
    """
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    if reservation.status != Status.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Reservation is not pending")
    reservation.status = Status.CANCELED
    db.commit()
    db.refresh(reservation)
    return reservation
