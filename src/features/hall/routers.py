from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.utils.check_admin import check_admin
from .services import get_hall_with_showtimes, create_hall, update_hall, partial_update_hall, delete_hall
from .schemas import HallCreate, HallResponse
from typing import Optional, List

router = APIRouter(tags=["hall"])


@router.get("/{cinema_id}/hall", response_model=List[HallResponse])
async def get_hall_with_showtimes_endpoint(cinema_id: int, db: Session = Depends(get_db)):
    return get_hall_with_showtimes(cinema_id, db)


@router.post("/", response_model=HallResponse, status_code=201)
async def create_hall_endpoint(hall: HallCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    return create_hall(hall, db)


@router.put("/{hall_id}", response_model=HallResponse)
async def update_hall_endpoint(hall_id: int, hall: HallCreate, db: Session = Depends(get_db), _=Depends(check_admin)):
    return update_hall(hall_id, hall, db)


@router.patch("/{hall_id}", response_model=HallResponse)
async def partial_update_hall_endpoint(
    hall_id: int,
    name: Optional[str] = None,
    rows: Optional[int] = None,
    columns: Optional[int] = None,
    cinema_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _=Depends(check_admin)
):
    return partial_update_hall(hall_id, name, rows, columns, cinema_id, db)


@router.delete("/{hall_id}", response_model=dict)
async def delete_hall_endpoint(hall_id: int, db: Session = Depends(get_db), _=Depends(check_admin)):
    return delete_hall(hall_id, db)
