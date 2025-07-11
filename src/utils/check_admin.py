from fastapi import Depends, HTTPException, status
from src.routers.auth import get_current_user
from src.models import User, Role


def check_admin(user: User = Depends(get_current_user)):
    """
    Ensure the user has admin privileges.

    Args:
        user: Current user from authentication dependency.

    Returns:
        User: The authenticated admin user.

    Raises:
        HTTPException (403): If the user is not an admin.
    """
    if user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user
