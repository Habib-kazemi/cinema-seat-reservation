from fastapi import Depends, HTTPException, status
from src.features.auth.services import get_current_user
from src.features.users.schemas import Role
from src.features.users.models import User


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
