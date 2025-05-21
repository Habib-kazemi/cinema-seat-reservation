"""
Hall-related API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Hall
from ..schemas import HallCreate, HallResponse

router = APIRouter()


@router.post("/", response_model=HallResponse)
async def create_hall(hall: HallCreate, db: Session = Depends(get_db)):
    """
    Create a new cinema hall.

    Args:
        hall: Hall data including name, rows, and columns.
        db: Database session.

    Returns:
        dict: Hall ID and success message.

    Raises:
        HTTPException: If rows or columns are invalid.
    """
    try:
        # Check if rows and columns are positive
        if hall.rows <= 0 or hall.columns <= 0:
            raise HTTPException(
                status_code=400, detail="Rows and columns must be positive")

        # Create new hall
        db_hall = Hall(
            name=hall.name,
            rows=hall.rows,
            columns=hall.columns
        )
        db.add(db_hall)
        db.commit()
        db.refresh(db_hall)

        return {"id": db_hall.id, "message": "Hall created successfully"}

    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        print(f"Error in create_hall: {exc}")
        raise HTTPException(
            status_code=500, detail="Internal server error") from exc
